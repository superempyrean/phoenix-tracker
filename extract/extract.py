"""Extracts the tracked tables from one Phoenix Android build.

    python -I extract/extract.py --apk base.apk --apk split.apk ... [--out latest]

APK contents are untrusted. They are read as zip members and parsed as
bytes; nothing from them is executed or written to disk except the tables.
"""

import argparse
import hashlib
import os
import re
import shutil
import sys
import time
import zipfile

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import axml  # noqa: E402
import dex  # noqa: E402
import elf  # noqa: E402
import hermes  # noqa: E402
import literals  # noqa: E402

HOST = "liblibdiscord_wasm_host.so"
ABIS = ["arm64-v8a", "armeabi-v7a", "x86", "x86_64"]

# Tables that may legitimately differ between ABIs.
PER_ABI_OK = {"crates.txt"}

# UI event names a node lists in its `on` property. The names come from the
# spec; their PropIds are looked up in the extracted table.
UI_EVENT_NAMES = ["press", "tap", "longPress", "change", "submit", "focus", "blur", "layout"]

# Models read from the guest's serde Serialize impls: serialize_struct(name)
# followed by one serialize_field(key) per field, in declaration order.
SERIALIZE_MODELS = [
    "User", "Member", "MemberRoles", "Message", "SnapshotMessage", "Attachment",
    "Channel", "ChannelDmFields", "ChannelThreadFields", "ChannelForumFields",
    "ChannelVoiceFields", "ChannelExtraFields", "Role", "Emoji", "Embed",
    "EmbedAuthor", "EmbedField", "EmbedFooter", "EmbedMedia", "PollMedia",
]

# Models read from Deserialize visitors, which name no struct. Each is the
# smallest visitor whose field set contains the anchor fields. The fields
# are written sorted, since a visitor's order is not declaration order.
DESERIALIZE_MODELS = {
    "CurrentUser": {"email", "mfa_enabled", "purchased_flags"},
    "DisplayNameStyles": {"font_id", "effect_id", "colors"},
    "PrimaryGuild": {"identity_guild_id", "tag", "badge"},
    "AvatarDecorationData": {"asset", "sku_id", "expires_at"},
    "NameplateData": {"asset", "palette", "sku_id"},
    "RoleColors": {"primary_color", "secondary_color", "tertiary_color"},
    "RoleTags": {"bot_id", "integration_id", "premium_subscriber"},
}

EXPERIMENT = re.compile(r"20\d\d-\d\d-[a-z][a-z0-9_-]*[a-z0-9]")
DATE_INSIDE = re.compile(r"(?<=[a-z0-9])(?=20\d\d-\d\d-)")
SNAKE = re.compile(r"[a-z][a-z0-9_]*")
CAMEL = re.compile(r"[A-Z][A-Za-z0-9]+")
CRATE = re.compile(rb"(?:index\.crates\.io-[0-9a-f]+/|_crates__)([A-Za-z0-9_.-]+?)-"
                   rb"(\d+\.\d+\.\d+(?:-[0-9A-Za-z.]+)?(?:\+[0-9A-Za-z.]+)?)/")
FIRST_PARTY = re.compile(rb"crates/([a-z0-9][a-z0-9_-]*)/src/")
RUSTC = re.compile(rb"/rustc/([0-9a-f]{40})/")
TOOLCHAIN = re.compile(rb"rust-[a-z]+-(\d+\.\d+\.\d+[A-Za-z0-9.-]*)/lib/rustlib")

warnings = []


def warn(msg):
    warnings.append(msg)
    print(f"warning: {msg}", file=sys.stderr)


class Table:
    def __init__(self, header, lines):
        self.header = header
        self.lines = lines

    def text(self):
        return "".join(f"# {h}\n" for h in self.header) + "".join(f"{x}\n" for x in self.lines)

    def __eq__(self, other):
        return self.lines == other.lines


# ---------------------------------------------------------------- the APKs

class Apk:
    def __init__(self, path):
        self.path = path
        self.zip = zipfile.ZipFile(path)
        self.names = self.zip.namelist()
        self.manifest = {}
        self.meta = {}
        for tag, attrs in axml.elements(self.zip.read("AndroidManifest.xml")):
            if tag == "manifest":
                self.manifest = attrs
            elif tag == "meta-data" and "name" in attrs:
                self.meta[attrs["name"]] = attrs.get("value")
        self.abis = sorted({n.split("/")[1] for n in self.names if n.startswith("lib/") and n.count("/") == 2})
        self.is_base = "classes.dex" in self.names

    def sha256(self):
        h = hashlib.sha256()
        with open(self.path, "rb") as f:
            for chunk in iter(lambda: f.read(1 << 20), b""):
                h.update(chunk)
        return h.hexdigest()


# ------------------------------------------------------------ the platform

def platform_tables(base):
    """Tables from classes*.dex in the base APK (the Android platform)."""
    found = {"kinds": None, "op_names": None, "prop_names": None, "methods": None,
             "op_switch": None, "tag_switch": None, "version_check": False,
             "frame_ints": None, "child_edits": False}
    strings = set()
    for dn in sorted(n for n in base.names if re.fullmatch(r"classes\d*\.dex", n)):
        dx = dex.Dex(base.zip.read(dn))
        strings.update(dx.strings())
        for m in dx.methods():
            for arr in m.string_arrays:
                if found["kinds"] is None and {"view", "text", "navigator", "canvas"} <= set(arr):
                    found["kinds"] = arr
                if found["op_names"] is None and len(arr) > 3 and arr[0] == "" and arr[1:3] == ["create", "update"]:
                    found["op_names"] = arr
                if found["prop_names"] is None and len(arr) > 100 and {"background", "opacity", "press"} <= set(arr):
                    found["prop_names"] = arr
            pairs = [s for s in m.strings if re.fullmatch(r"\S+ \d+", s)]
            if found["methods"] is None and len(pairs) > 100 and any(p.startswith("@") for p in pairs):
                found["methods"] = pairs
            if "unknown op " in m.strings and m.switches:
                found["op_switch"] = m.switches[0][1]
                # The decoder reads the first byte and compares it with a literal.
                found["version_check"] = "view wire version " in m.strings and m.ints[:2] == [0, 1]
            if "unknown value tag " in m.strings and m.switches:
                found["tag_switch"] = m.switches[0][1]
            if m.name == "invoke" and m.cls.endswith("/GuestHost;"):
                found["frame_ints"] = m.ints
    found["child_edits"] = any(s.startswith("childEdits ") for s in strings)
    found["strings"] = strings
    return found


def hermes_strings(base):
    if "assets/index.android.bundle" not in base.names:
        return None, []
    data = base.zip.read("assets/index.android.bundle")
    try:
        return hermes.strings(data)
    except ValueError as e:
        warn(f"Hermes bundle: {e}")
        return None, []


# ---------------------------------------------------------------- the host

def _slice(e, rel, va, ro):
    ptr = rel.get(va)
    if ptr is None or not ro.contains(ptr):
        return None
    n = e.word_at(va + e.word)
    if n is None or not 0 < n <= 256:
        return None
    b = e.read(ptr, n)
    try:
        s = b.decode("utf-8")
    except (UnicodeDecodeError, AttributeError):
        return None
    if any(ord(c) < 32 for c in s):
        return None
    return s


def keyed_tables(e):
    """Sorted runs of (name, id) records in .data.rel.ro: a &str and an id."""
    rel = e.relative_relocs()
    ro = e.section(".rodata")
    sec = e.section(".data.rel.ro")
    w = e.word
    out = []
    va, end = sec.addr, sec.addr + sec.size
    while va < end:
        run = []
        v = va
        while v + 3 * w <= end:
            s = _slice(e, rel, v, ro)
            ident = e.word_at(v + 2 * w)
            if s is None or ident is None or ident >= 1 << 16:
                break
            if run and s.encode() <= run[-1][0].encode():
                break
            run.append((s, ident))
            v += 3 * w
        if len(run) >= 50:
            out.append((va, run))
            va = v
        else:
            va += w
    return out


def slice_array(e, start_name, n):
    """The array of n &str slices whose first entry is start_name."""
    rel = e.relative_relocs()
    ro = e.section(".rodata")
    for va in sorted(rel):
        if _slice(e, rel, va, ro) == start_name:
            got = [_slice(e, rel, va + 2 * e.word * k, ro) for k in range(n)]
            if None not in got:
                yield got


def host_tables(e, tables, notes):
    """Fills `tables` with what the host .so yields on this ABI."""
    data = e.data
    keyed = keyed_tables(e)

    # PropIds: the sorted name->id table whose ids are exactly 0..n-1.
    props = None
    for _va, run in keyed:
        # The longest prefix whose ids are exactly 0..k-1 (a run can run on
        # into the next table).
        k, top, seen = 0, -1, set()
        for j, (_, i) in enumerate(run):
            if i in seen:
                break
            seen.add(i)
            top = max(top, i)
            if top == j:
                k = j + 1
        names = {s for s, _ in run[:k]}
        if {"background", "opacity", "press"} <= names:
            props = sorted(run[:k], key=lambda r: r[1])
            break
    if props is None:
        warn(f"{e.abi}: PropId table not found")
    else:
        by_id = [s for s, _ in props]
        arrays = list(slice_array(e, by_id[0], len(by_id)))
        notes["propid_array"] = any(a == by_id for a in arrays)
        tables["propids.tsv"] = Table(
            ["PropId -> name. Source: the host's sorted name->id table, checked against its id->name array.",
             "Status: extracted."],
            [f"{i}\t{s}" for i, s in enumerate(by_id)])
        notes["propids"] = by_id

    # The id table shared by host modules, methods, events and record keys.
    methods = None
    for _va, run in keyed:
        if run[0] == ("-", 0) and any(s.startswith("@") for s, _ in run):
            methods = run
            break
    if methods is None:
        warn(f"{e.abi}: method id table not found")
    else:
        notes["methods"] = methods
        rows = sorted(methods, key=lambda r: (r[1], r[0]))
        calls = [f"{i}\t{s}" for s, i in rows if s[:1].isupper()]
        events = [f"{i}\t{s}" for s, i in rows if s.startswith("@")]
        atoms = [f"{i}\t{s}" for s, i in rows if not s[:1].isupper() and not s.startswith("@")]
        tables["host-calls.txt"] = Table(
            ["Host modules and methods (Module, Module.method) -> id, as a CALL frame names them.",
             "Source: the host's id table, checked against the platform's method table. Status: extracted."], calls)
        tables["events.txt"] = Table(
            ["Platform events (@name) -> id, the method field of an EVENT frame.",
             "Source: the host's id table, checked against the platform's method table. Status: extracted."], events)
        tables["atoms.tsv"] = Table(
            ["The rest of the same id table: record keys and other names (\"-\" is id 0).",
             "Source: the host's id table. Status: extracted."], atoms)

    # Exports.
    exp = sorted({n for n, kind, defined in e.dynamic_symbols()
                  if defined and kind in ("func", "object", "ifunc", "tls") and not n.startswith("_")})
    tables["exports.txt"] = Table(["The host's dynamic exports, names only. Source: .dynsym. Status: extracted."], exp)

    # Crates and source paths.
    crates = sorted({f"{m.group(1).decode()}@{m.group(2).decode()}" for m in CRATE.finditer(data)})
    tables["crates.txt"] = Table(
        ["Vendored crates (name@version) from the host's source paths. Status: extracted."], crates)
    first = sorted({m.group(1).decode() for m in FIRST_PARTY.finditer(data)})
    tables["guest-modules.txt"] = Table(
        ["The guest's wasm-app feature crates, from crates/<name>/src/ paths in the host. Status: extracted."],
        [c for c in first if c.startswith("wasm-app")])
    tables["first-party-crates.txt"] = Table(
        ["Every first-party crate named by a crates/<name>/src/ path in the host. Status: extracted."], first)

    # Experiment names: the host keeps them as &str slices in its data.
    exps = set()
    rel = e.relative_relocs()
    ro = e.section(".rodata")
    for va in rel:
        s = _slice(e, rel, va, ro)
        if s is not None and EXPERIMENT.fullmatch(s):
            exps.add(s)
    notes["host_experiments"] = exps

    # Code literals: models. Not available on 32-bit ARM.
    try:
        lits = literals.Literals(e)
    except NotImplementedError as ex:
        notes["no_code"] = str(ex)
        return
    known = {s for lst in lits.by_function.values() for s, exact in lst if exact}
    models = {}
    by_name = {}
    for fn, lst in sorted(lits.by_function.items()):
        if len(lst) < 3 or not lst[0][1] or not CAMEL.fullmatch(lst[0][0]):
            continue
        fields = []
        for s, exact in lst[1:]:
            f = field_name(s, exact, known)
            if f is None:
                break
            fields.append(f)
        else:
            by_name.setdefault(lst[0][0], []).append(fields)
    for name in SERIALIZE_MODELS:
        cands = by_name.get(name, [])
        if not cands:
            warn(f"{e.abi}: no Serialize impl found for {name}")
            continue
        best = max(cands, key=lambda f: (len(f), f))
        models[name] = Table([f"{name}: fields in declaration order, from the guest's Serialize impl.",
                              "Status: extracted."], best)
    visitors = []
    for fn, lst in sorted(lits.by_function.items()):
        if any("missing field" in s or "duplicate field" in s for s, _ in lst):
            fields = {f for s, exact in lst if (f := field_name(s, exact, known)) is not None}
            visitors.append(fields)
    for name, anchors in DESERIALIZE_MODELS.items():
        cands = sorted((f for f in visitors if anchors <= f), key=lambda f: (len(f), sorted(f)))
        if not cands:
            warn(f"{e.abi}: no Deserialize visitor found for {name}")
            continue
        models[name] = Table([f"{name}: fields, sorted, from the smallest Deserialize visitor naming "
                              + ", ".join(sorted(anchors)) + ".", "Status: extracted (anchored by those fields)."],
                             sorted(cands[0]))
    for name, t in models.items():
        tables[f"models/{name}.txt"] = t



def field_name(s, exact, known):
    """A serde field name from a literal. An exact literal must be a whole
    name. An inexact one (no length beside its pointer) is cut to its
    longest prefix that the build also references with a length."""
    m = SNAKE.match(s)
    if not m:
        return None
    if exact:
        return s if m.end() == len(s) else None
    # Cut at the longest prefix the build also references with a length.
    name, rest = m.group(0), s[m.end():]
    for k in range(len(name), 1, -1):
        if name[:k] in known:
            return name[:k]
    if rest and rest[0].isascii() and rest[0].isprintable():
        return None  # a run of names with no known boundary
    # The name ends at binary data. Shorter names there are usually data too.
    return name if len(name) >= 3 else None


def name_in(name, rows):
    return any(r.split("	", 1)[0] == name for r in rows)


def rustc_lines(name, e):
    out = []
    for line in e.bytes_of(".comment").split(b"\0"):
        if line.strip():
            out.append(f"{name}\tcomment\t{line.decode('utf-8', 'replace').strip()}")
    for h in sorted({m.group(1).decode() for m in RUSTC.finditer(e.data)}):
        out.append(f"{name}\trustc-commit\t{h}")
    for t in sorted({m.group(1).decode() for m in TOOLCHAIN.finditer(e.data)}):
        out.append(f"{name}\ttoolchain\t{t}")
    return out


# ------------------------------------------------------------- wire.txt

def wire_table(p, host_data, props):
    rows = []

    def row(section, code_, name, status, check):
        rows.append(f"{section}\t{code_}\t{name}\t{status}\t{check}")

    row("turn-version", 1, "-", "extracted" if p["version_check"] else "spec",
        "the platform's turn decoder compares the first byte with 1" if p["version_check"] else "manual")
    spec_ops = ["create", "update", "children", "delete", "root", "focus", "scrollTo", "requestFrame",
                "motion", "childEdits"]
    names = p["op_names"] or []
    switch = p["op_switch"] or []
    for code_, spec in enumerate(spec_ops, 1):
        if code_ < len(names) and code_ in switch:
            ok = names[code_] == spec
            if not ok:
                warn(f"turn op {code_}: platform names it {names[code_]!r}, the spec {spec!r}")
            row("turn-op", code_, names[code_], "extracted",
                "code: the platform decoder's switch; name: the platform's op-name array")
        elif code_ in switch:
            row("turn-op", code_, spec, "spec",
                "code: the platform decoder's switch; name: manual"
                + (" (a \"childEdits ...\" error string exists)" if spec == "childEdits" and p["child_edits"] else ""))
        else:
            row("turn-op", code_, spec, "spec", "manual")
    extra = [c for c in switch if c > len(spec_ops)]
    for c in extra:
        warn(f"the platform decoder handles turn op {c}, which the spec doesn't name")
        row("turn-op", c, "?", "extracted", "code: the platform decoder's switch; name: unknown")

    tags = ["Null", "False", "True", "I32", "I64", "F64", "String", "Array", "ObjectByPropId",
            "Vec4F32", "MapStringValue", "Words", "WordsPatch"]
    tswitch = p["tag_switch"] or []
    for code_, name in enumerate(tags):
        row("value-tag", code_, name, "spec",
            "code: the platform value decoder's switch; name: manual" if code_ in tswitch else "manual")
    for c in [c for c in tswitch if c >= len(tags)]:
        warn(f"the platform value decoder handles tag {c}, which the spec doesn't name")
        row("value-tag", c, "?", "extracted", "code: the platform value decoder's switch")

    row("propid-count", len(props) if props else "?", "-", "extracted" if props else "spec",
        "the host's PropId table and the platform's name array")

    ints = p["frame_ints"] or []
    hdr_ok = 16 in ints
    row("frame-header-size", 16, "-", "extracted" if hdr_ok else "spec",
        "the platform's invoke compares the frame length with 16" if hdr_ok else "manual")
    kinds_ok = 1 in ints and 5 in ints
    for code_, name in enumerate(["CALL", "REPLY", "EVENT", "BATCH"], 1):
        row("frame-kind", code_, name, "spec",
            "code: the platform's invoke accepts kinds 1 to 4; name: manual" if kinds_ok else "manual")

    run = b"uikeyCommandinsetswindowframeIntervalframemotion"
    run_ok = host_data is not None and run in host_data
    row("ui-event-prefix", "u32 0", "-", "spec", "manual")
    row("ui-event-version", 1, "-", "spec", "manual")
    ui = ["ui", "back", "keyCommand", "insets", "window", "frameInterval", "frame", "motion", "navSides"]
    for code_, name in enumerate(ui, 1):
        if name in ("back", "navSides"):
            check = "manual"
        else:
            check = "name: found in the guest's event-name run in the host; code: manual" if run_ok else "manual"
        row("ui-event-op", code_, name, "spec", check)
    return Table(
        ["Wire constants. Columns: section, code, name, status, check.",
         "\"extracted\" means the extractor read the value from this build. \"spec\" lines are the recovered",
         "spec (rekindle's docs/research/phoenix-wire-protocol.md); their check column says what this build confirmed."],
        rows)


# --------------------------------------------------------------------- main

def write_tree(out, shared, per_abi):
    if os.path.isdir(out):
        for entry in os.listdir(out):
            path = os.path.join(out, entry)
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
    os.makedirs(out, exist_ok=True)

    def put(rel, table):
        path = os.path.join(out, *rel.split("/"))
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(table.text())

    for rel, t in sorted(shared.items()):
        put(rel, t)
    for abi, tabs in sorted(per_abi.items()):
        for rel, t in sorted(tabs.items()):
            put(f"abi/{abi}/{rel}", t)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--apk", action="append", required=True, help="base APK and ABI splits")
    ap.add_argument("--out", default="latest")
    ap.add_argument("--allow-abi-differences", action="store_true",
                    help="exit 0 even if a vocabulary table differs between ABIs")
    args = ap.parse_args()
    t0 = time.time()

    apks = [Apk(p) for p in args.apk]
    bases = [a for a in apks if a.is_base]
    if len(bases) != 1:
        sys.exit("error: pass exactly one base APK (the one with classes.dex)")
    base = bases[0]
    code_ = base.manifest.get("versionCode")
    for a in apks:
        if a.manifest.get("versionCode") != code_:
            sys.exit(f"error: {a.path} is version {a.manifest.get('versionCode')}, the base is {code_}")

    shared = {}
    per_abi = {}

    # build.txt
    build = [
        f"package\t{base.manifest.get('package')}",
        f"version-name\t{base.manifest.get('versionName')}",
        f"version-code\t{code_}",
        f"libdiscord-version\t{base.meta.get('libdiscord_version')}",
        f"compile-sdk\t{base.manifest.get('compileSdkVersion')}",
    ]
    for a in sorted(apks, key=lambda a: (not a.is_base, a.manifest.get("split", ""))):
        build.append(f"apk\t{a.manifest.get('split', 'base')}\t{os.path.basename(a.path)}\tsha256:{a.sha256()}")

    # The platform.
    p = platform_tables(base)
    hv, hstrings = hermes_strings(base)
    if hv is not None:
        build.append(f"hermes-bytecode-version\t{hv}")
    if p["kinds"] is None:
        warn("kind table not found in the platform")
    else:
        shared["kinds.txt"] = Table(["Element kinds the platform interns, in table order (index, name).",
                                     "Source: classes.dex. Status: extracted."],
                                    [f"{i}\t{k}" for i, k in enumerate(p["kinds"])])

    # The ABI splits.
    abi_lines = []
    host_by_abi = {}
    for a in apks:
        for abi in a.abis:
            libs = sorted(n for n in a.names if n.startswith(f"lib/{abi}/") and n.endswith(".so"))
            rows, rustc = [], []
            for n in libs:
                b = a.zip.read(n)
                name = n.rsplit("/", 1)[1]
                rows.append(f"{name}\t{len(b)}\t{hashlib.sha256(b).hexdigest()}")
                try:
                    rustc += rustc_lines(name, elf.Elf(b))
                except ValueError:
                    pass
                if name == HOST:
                    host_by_abi[abi] = b
            tabs = per_abi.setdefault(abi, {})
            tabs["libs.tsv"] = Table([f"Native libraries in the {abi} split: name, size, sha256."], rows)
            tabs["rustc.txt"] = Table([f"Compiler facts per library ({abi}): .comment lines, /rustc/<commit>/ paths,"
                                       " toolchain paths."], rustc)
            abi_lines.append(f"abi\t{abi}\t{len(libs)} libs\t" + ("host" if name_in(HOST, rows) else "no host"))

    build += sorted(abi_lines)

    # The host, per ABI, then compared.
    results = {}
    notes_by_abi = {}
    for abi, b in sorted(host_by_abi.items()):
        e = elf.Elf(b)
        tabs, notes = {}, {}
        host_tables(e, tabs, notes)
        results[abi] = tabs
        notes_by_abi[abi] = notes
        if "no_code" in notes:
            print(f"note: {abi}: models skipped ({notes['no_code']})", file=sys.stderr)
    if not results:
        warn("no ABI split carries the host")

    differing = []
    names = sorted({n for tabs in results.values() for n in tabs})
    for n in names:
        have = {abi: tabs[n] for abi, tabs in results.items() if n in tabs}
        first = next(iter(have.values()))
        if all(t == first for t in have.values()):
            shared[n] = first
        else:
            for abi, t in have.items():
                per_abi[abi][n] = t
            if n not in PER_ABI_OK:
                differing.append(n)
                warn(f"{n} differs between ABIs: " + ", ".join(sorted(have)))

    # Cross-checks against the platform.
    pnotes = next((notes_by_abi[a] for a in ABIS if a in notes_by_abi), {})
    props = pnotes.get("propids")
    checks = []
    if props is not None:
        checks.append(("host PropId table matches its id->name array",
                       all(n.get("propid_array") for n in notes_by_abi.values())))
        if p["prop_names"] is not None:
            checks.append((f"host PropIds ({len(props)}) match the platform's name array ({len(p['prop_names'])})",
                           props == p["prop_names"]))
    if pnotes.get("methods") is not None and p["methods"] is not None:
        host = sorted(f"{s} {i}" for s, i in pnotes["methods"])
        plat = sorted(p["methods"])
        checks.append((f"host id table ({len(host)}) matches the platform's method table ({len(plat)})", host == plat))
    if p["kinds"] is not None and host_by_abi:
        hd = host_by_abi[next(a for a in ABIS if a in host_by_abi)]
        missing = [k for k in p["kinds"] if k.encode() not in hd]
        checks.append(("every platform kind string occurs in the host", not missing))
    for desc, ok in checks:
        print(f"check: {'ok  ' if ok else 'FAIL'} {desc}", file=sys.stderr)
        if not ok:
            warn(f"check failed: {desc}")

    # Tables built from several sources.
    host_data = host_by_abi.get(next((a for a in ABIS if a in host_by_abi), None))
    shared["wire.txt"] = wire_table(p, host_data, props)
    if props is not None:
        pid = {s: i for i, s in enumerate(props)}
        shared["ui-events.tsv"] = Table(
            ["UI event names (spec) and their PropIds (extracted), as a node lists them in `on`."],
            [f"{pid[n]}\t{n}" if n in pid else f"?\t{n}" for n in sorted(UI_EVENT_NAMES, key=lambda n: pid.get(n, 1 << 20))])

    exps = {}
    hexps = {abi: n["host_experiments"] for abi, n in notes_by_abi.items() if "host_experiments" in n}
    union = set().union(*hexps.values()) if hexps else set()
    for abi, h in sorted(hexps.items()):
        if h != union:
            warn(f"{abi}: host experiment names missing: {', '.join(sorted(union - h))}")
    for s in union:
        exps.setdefault(s, set()).add("host")
    for s in hstrings:
        if EXPERIMENT.fullmatch(s):
            exps.setdefault(s, set()).add("bundle")
    for s in p["strings"]:
        if EXPERIMENT.fullmatch(s):
            exps.setdefault(s, set()).add("dex")
    shared["experiments.txt"] = Table(
        ["Date-prefixed experiment and flag names, and where they occur (host, bundle, dex). Status: extracted."],
        [f"{s}\t{','.join(sorted(src))}" for s, src in sorted(exps.items())])

    shared["build.txt"] = Table(["Build identity, APKs and ABIs. Status: extracted."], build)
    if differing:
        shared["ABI-DIFFERENCES.txt"] = Table(
            ["Vocabulary tables that differ between ABIs. Each ABI's copy is under abi/<abi>/."], differing)

    write_tree(args.out, shared, per_abi)
    print(f"wrote {args.out} in {time.time() - t0:.1f}s", file=sys.stderr)
    if differing and not args.allow_abi_differences:
        sys.exit(f"error: tables differ between ABIs: {', '.join(differing)}")
    if any(w.startswith("check failed") for w in warnings):
        sys.exit("error: a cross-check failed")


if __name__ == "__main__":
    main()
