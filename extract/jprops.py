"""The value type the Android platform reads for each PropId, from jadx's
Java output of the base APK's dex.

The platform keeps one handler per prop name in a registry class (the one
that throws "prop <name> handled twice"). Each handler is a small wrapper
class around a Function2, and the platform's dispatch loop picks the
accessor that converts the stored value by the wrapper's class. This module
reads those three places and the registration calls, so every name it
reports comes from the code, not from a hand-written list. Class and method
names are minified and change between builds; nothing here depends on them.

jadx must run with --no-replace-consts. Otherwise it writes a literal that
equals some other class's constant as that constant
(AppStateModule.APP_STATE_BACKGROUND for "background"), and the
registration no longer names its prop.
"""

import glob
import os
import re
import shutil
import subprocess
import tempfile
import zipfile

# The type names written to propid-types.tsv, by what the accessor returns.
KINDS = ("Bool", "Number", "String", "Map", "List", "Edges", "Slot", "Any", "?")
KEY_KINDS = ("Bool", "Int", "Long", "Double", "String", "Map", "List", "Any")

PACKAGE = re.compile(r"^package ([\w.]+);", re.M)


def run_jadx(jadx_home, base_apk, out_dir):
    """Decompiles the base APK's dex with jadx's command-line entry point
    (never the GUI) into out_dir, and returns its sources directory."""
    jars = glob.glob(os.path.join(jadx_home, "lib", "*.jar"))
    if not jars:
        raise FileNotFoundError(f"no jadx jars under {jadx_home}/lib")
    dex_dir = tempfile.mkdtemp(prefix="dex-")
    try:
        with zipfile.ZipFile(base_apk) as z:
            dexes = []
            for n in z.namelist():
                if re.fullmatch(r"classes\d*\.dex", n):
                    path = os.path.join(dex_dir, n)
                    with open(path, "wb") as f:
                        f.write(z.read(n))
                    dexes.append(path)
        cmd = ["java", "-Xmx6g", "-cp", os.pathsep.join(jars), "jadx.cli.JadxCLI",
               "--no-res", "--no-replace-consts", "--show-bad-code", "-j", "2", "-q", "-d", out_dir, *sorted(dexes)]
        # jadx exits 1 when it fails on any method; the tables don't need
        # all of them, and a missing class shows up as a failed lookup.
        subprocess.run(cmd, check=False)
    finally:
        shutil.rmtree(dex_dir, ignore_errors=True)
    return os.path.join(out_dir, "sources")


class Source:
    def __init__(self, root):
        self.root = root
        self.files = {}
        for dirpath, _dirs, files in os.walk(root):
            for f in files:
                if f.endswith(".java"):
                    path = os.path.join(dirpath, f)
                    with open(path, encoding="utf-8", errors="replace") as fh:
                        self.files[path] = fh.read()

    def with_text(self, *needles):
        return [(p, t) for p, t in self.files.items() if all(n in t for n in needles)]

    def class_name(self, path):
        rel = os.path.relpath(path, self.root)[:-5]
        return rel.replace(os.sep, ".")

    def resolve(self, from_path, name):
        """The file of class `name` as written in from_path."""
        if "." in name:
            cand = os.path.join(self.root, *name.split(".")) + ".java"
        else:
            cand = os.path.join(os.path.dirname(from_path), name + ".java")
        return cand if cand in self.files else None


def _simple(name):
    return name.rsplit(".", 1)[-1]


def _method_body(text, start):
    """The text of the brace block that starts at or after `start`."""
    i = text.index("{", start)
    depth = 0
    for j in range(i, len(text)):
        if text[j] == "{":
            depth += 1
        elif text[j] == "}":
            depth -= 1
            if depth == 0:
                return text[i:j + 1]
    return text[i:]


def read_props(src, propids):
    """{prop name: {kind: set(classes)}} for registered handlers, plus
    {prop name: set(classes)} for props the platform looks up by id."""
    # The registry.
    regs = src.with_text('" handled twice"', "LinkedHashMap")
    if len(regs) != 1:
        raise LookupError(f"{len(regs)} prop registry classes")
    reg_path, reg = regs[0]
    reg_cls = _simple(src.class_name(reg_path))
    wrap_of = {}    # registry method -> wrapper class (simple name)
    direct = set()  # methods taking a wrapper object
    for m in re.finditer(r"public final void (\w+)\((String|Iterable) \w+, (\w+(?:\.\w+)*) \w+\) \{", reg):
        body = _method_body(reg, m.end() - 1)
        if m.group(3) == "Function2":
            w = re.search(r"new ([\w.]+)\(\w+\)", body)
            if w:
                wrap_of[m.group(1)] = _simple(w.group(1))
        else:
            direct.add(m.group(1))

    # The value decoder names the list and map classes.
    dec = src.with_text('"unknown value tag "')
    list_cls = map_cls = map_path = None
    for dpath, t in dec:
        lm = re.search(r"case 7:\s*([\w.]+) \w+ = new \1\(\)", t)
        mm = re.search(r"case 8:\s*([\w.]+) \w+ = new \1\(\)", t)
        if lm and mm:
            list_cls, map_cls = _simple(lm.group(1)), _simple(mm.group(1))
            map_path = src.resolve(dpath, mm.group(1))
    if list_cls is None:
        raise LookupError("value decoder not found")

    # The dispatch loop: one instanceof branch per wrapper.
    wrappers = set(wrap_of.values())
    kind_of = {}
    for path, t in src.with_text("instanceof", ".invoke(this, "):
        found = set(re.findall(r"instanceof ([\w.]+)\)", t)) & wrappers
        if len(found) < len(wrappers) - 1:
            continue
        # The last wrapper is the else branch: it hands over the slot index.
        for m in re.finditer(r"\(\(([\w.]+)\) \w+\)\.\w+\.invoke\(this, Integer\.valueOf\(", t):
            kind_of[_simple(m.group(1))] = "Slot"
        for m in re.finditer(r"(?:if|else if) \(\w+ instanceof ([\w.]+)\) \{", t):
            w = _simple(m.group(1))
            branch = _method_body(t, m.end() - 1)
            if "float[]" in branch:
                kind_of[w] = "Edges"
                continue
            acc = re.search(r"\.invoke\(this, (\w+)\.(\w+)\(\w+\)\)", branch)
            if not acc:
                continue
            decl = re.search(r"([\w.]+) " + acc.group(1) + r" = ", t)
            acc_path = src.resolve(path, decl.group(1)) if decl else None
            if acc_path is None:
                continue
            at = src.files[acc_path]
            sig = re.search(r"public (?:final )?([\w.]+) " + acc.group(2) + r"\(int \w+\) \{", at)
            if not sig:
                continue
            ret, body = _simple(sig.group(1)), _method_body(at, sig.end() - 1)
            if ret == "Boolean":
                kind_of[w] = "Bool"
            elif ret == "String":
                kind_of[w] = "String"
            elif ret == "Object":
                kind_of[w] = "Any"
            elif ret == list_cls:
                kind_of[w] = "List"
            elif ret == map_cls:
                kind_of[w] = "Map"
            elif re.search(r"== 3 \|\| \w+ == 4 \|\| \w+ == 5", body):
                kind_of[w] = "Number"
        break
    if not kind_of:
        raise LookupError("prop dispatch not found")

    # Registration calls on registry objects.
    names = set(propids)
    read = {}
    var_decl = re.compile(r"\b(?:[\w.]+\.)?" + re.escape(reg_cls) + r" (\w+) = ")
    for path, t in src.files.items():
        if reg_cls not in t:
            continue
        vars_ = set(var_decl.findall(t))
        if not vars_:
            continue
        cls = src.class_name(path)
        alt = "|".join(sorted(map(re.escape, vars_)))
        one = re.compile(r"\b(?:" + alt + r")\.(\w+)\(\s*\"([^\"]+)\"\s*,\s*(?:new ([\w.]+)\()?")
        many = re.compile(r"\b(?:" + alt + r")\.(\w+)\(\s*[\w.]+\(new String\[\]\{([^}]*)\}\)\s*,"
                          r"\s*(?:new ([\w.]+)\()?")
        for rx, multi in ((one, False), (many, True)):
            for m in rx.finditer(t):
                meth, arg, wnew = m.group(1), m.group(2), m.group(3)
                if meth in wrap_of:
                    kind = kind_of.get(wrap_of[meth], "?")
                elif meth in direct and wnew:
                    kind = kind_of.get(_simple(wnew), "?")
                else:
                    continue
                for n in (re.findall(r"\"([^\"]+)\"", arg) if multi else [arg]):
                    if n in names:
                        read.setdefault(n, {}).setdefault(kind, set()).add(cls)

    # Keys of nested objects: tag 8 objects carry PropIds as keys too, and
    # the platform reads them out of its map class by name.
    keyed = map_keys(src, map_path, list_cls, names) if map_path else {}

    # Props looked up by id through the platform's name->id map.
    by_id = {}
    table = [(p, t) for p, t in src.files.items()
             if "String[]" in t and '"background"' in t and '"opacity"' in t and '"press"' in t]
    for tpath, tt in table:
        tcls = _simple(src.class_name(tpath))
        mf = re.search(r"public static final HashMap (\w+);", tt)
        if not mf:
            continue
        ref = f"{tcls}.{mf.group(1)}"
        for path, t in src.files.items():
            if ref not in t or path == tpath:
                continue
            for n in re.findall(r"\(\s*\w+,\s*\"([A-Za-z0-9]+)\"\s*\)\)\.intValue\(\)", t):
                if n in names:
                    by_id.setdefault(n, set()).add(src.class_name(path))
    return read, keyed, by_id


def map_keys(src, map_path, list_cls, names):
    """{key: {type: set(classes)}} for string-keyed reads out of the map
    class, typed by the accessor's signature."""
    map_cls = _simple(src.class_name(map_path))
    mt = src.files[map_path]
    acc = {}  # method -> (type, key is the first argument, static)
    sig = re.compile(r"public (static )?(?:final )?([\w.]+) (\w+)\(([^)]*)\) \{")
    for m in sig.finditer(mt):
        ret, meth = _simple(m.group(2)), m.group(3)
        params = [x.split()[0] for x in m.group(4).split(",") if x.strip()]
        if "String" not in params or len(params) > 2:
            continue
        kind = {"boolean": "Bool", "double": "Double", "int": "Int", "long": "Long", "String": "String",
                "Object": "Any", list_cls: "List", map_cls: "Map"}.get(ret)
        if kind:
            acc[meth] = (kind, params[0] == "String", bool(m.group(1)))
    out = {}
    decl = re.compile(r"\b(?:[\w.]+\.)?" + re.escape(map_cls) + r" (\w+)\b")
    for path, t in src.files.items():
        if map_cls not in t:
            continue
        cls = src.class_name(path)
        recv = [re.escape(map_cls)] + sorted(re.escape(v) for v in set(decl.findall(t)))
        rx = re.compile(r"\b(" + "|".join(recv) + r")\.(\w+)\(([^()\"]*?)\"([A-Za-z0-9]+)\"")
        for m in rx.finditer(t):
            r, meth, before, key = m.groups()
            if meth not in acc or key not in names:
                continue
            kind, key_first, static = acc[meth]
            if static != (r == map_cls) or key_first != (before.strip() == ""):
                continue
            out.setdefault(key, {}).setdefault(kind, set()).add(cls)
    return out


def table_lines(propids, read, keyed, by_id):
    out = []
    for i, n in enumerate(propids):
        if n in read or n in keyed:
            kinds = sorted(read.get(n, {}), key=KINDS.index)
            kinds += ["key:" + k for k in sorted(keyed.get(n, {}), key=KEY_KINDS.index)]
            where = sorted({c for d in (read.get(n, {}), keyed.get(n, {})) for cs in d.values() for c in cs})
            out.append(f"{i}\t{n}\t{'/'.join(kinds)}\t{','.join(where)}")
        elif n in by_id:
            out.append(f"{i}\t{n}\tby-id\t{','.join(sorted(by_id[n]))}")
        else:
            out.append(f"{i}\t{n}\t-\tunread")
    return out
