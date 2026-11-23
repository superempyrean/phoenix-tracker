"""Prints a changelog between two builds' tables.

    python -I extract/diff.py OLD NEW [--path latest] [--repo .]

OLD and NEW are two directories of tables, or two git revisions (tags,
commits, HEAD~1), in which case the tables are read from --path at each
revision.
"""

import argparse
import os
import subprocess
import sys

# Tables of "id<TAB>name" lines, diffed by name and by id.
ID_TABLES = {"propids.tsv", "host-calls.txt", "events.txt", "atoms.tsv", "kinds.txt", "ui-events.tsv"}
# Tables whose ids other code depends on: a changed id is called out.
RENUMBER_WARN = {"propids.tsv": "PropId", "host-calls.txt": "method id", "events.txt": "event id",
                 "atoms.tsv": "id", "kinds.txt": "kind index"}


def lines(text):
    return [x for x in text.splitlines() if x and not x.startswith("#")]


def read_dir(root):
    out = {}
    for dirpath, _dirs, files in os.walk(root):
        for f in files:
            path = os.path.join(dirpath, f)
            rel = os.path.relpath(path, root).replace(os.sep, "/")
            with open(path, encoding="utf-8") as fh:
                out[rel] = lines(fh.read())
    return out


def git(repo, *args):
    return subprocess.run(["git", "-C", repo, *args], check=True, capture_output=True).stdout.decode("utf-8")


def read_rev(repo, rev, path):
    prefix = path.rstrip("/") + "/"
    out = {}
    for name in git(repo, "ls-tree", "-r", "--name-only", rev, "--", prefix).splitlines():
        out[name[len(prefix):]] = lines(git(repo, "show", f"{rev}:{name}"))
    return out


def diff_ids(name, old, new):
    def parse(ls):
        by_name, by_id = {}, {}
        for x in ls:
            i, n = x.split("\t", 1)
            by_name[n] = i
            by_id.setdefault(i, []).append(n)
        return by_name, by_id

    oname, oid = parse(old)
    nname, nid = parse(new)
    added = {n: nname[n] for n in nname if n not in oname}
    removed = {n: oname[n] for n in oname if n not in nname}
    renamed = []
    for n, i in sorted(removed.items(), key=lambda r: r[1]):
        cand = [m for m in nid.get(i, []) if m in added]
        if len(cand) == 1:
            renamed.append((i, n, cand[0]))
    for i, a, b in renamed:
        removed.pop(a)
        added.pop(b)
    renumbered = [(n, oname[n], nname[n]) for n in oname if n in nname and oname[n] != nname[n]]
    out = []
    key = lambda r: (len(r[1]), r[1], r[0])  # noqa: E731
    for n, i in sorted(added.items(), key=key):
        out.append(f"  added    {i}\t{n}")
    for n, i in sorted(removed.items(), key=key):
        out.append(f"  removed  {i}\t{n}")
    for i, a, b in renamed:
        out.append(f"  renamed  {i}\t{a} -> {b}")
    if renumbered:
        what = RENUMBER_WARN.get(name, "id")
        out.append(f"  RENUMBERED: {len(renumbered)} {what}s changed")
        for n, a, b in sorted(renumbered, key=lambda r: (len(r[1]), r[1])):
            out.append(f"  renumbered {n}\t{a} -> {b}")
    return out


def diff_lines(old, new):
    o, n = set(old), set(new)
    out = [f"  added    {x}" for x in new if x not in o]
    out += [f"  removed  {x}" for x in old if x not in n]
    if not out and old != new:
        out.append("  order changed")
    return out


def diff_keyed(old, new, width):
    """Lines keyed by their first `width` tab-separated fields."""
    def parse(ls):
        return {tuple(x.split("\t")[:width]): x for x in ls}
    o, n = parse(old), parse(new)
    out = [f"  added    {n[k]}" for k in n if k not in o]
    out += [f"  removed  {o[k]}" for k in o if k not in n]
    out += [f"  changed  {o[k]}\n        -> {n[k]}" for k in o if k in n and o[k] != n[k]]
    return out


def diff_trees(old, new):
    report = []
    for name in sorted(set(old) | set(new)):
        if name not in new:
            report.append((name, ["  table removed"]))
            continue
        if name not in old:
            report.append((name, [f"  table added ({len(new[name])} entries)"]))
            continue
        a, b = old[name], new[name]
        if a == b:
            continue
        base = name.rsplit("/", 1)[-1]
        if base in ID_TABLES:
            out = diff_ids(base, a, b)
        elif base == "wire.txt":
            out = diff_keyed(a, b, 2)
        elif base in ("libs.tsv", "build.txt"):
            out = diff_keyed(a, b, 1 if base == "libs.tsv" else 2)
        else:
            out = diff_lines(a, b)
        report.append((name, out))
    return report


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("old")
    ap.add_argument("new")
    ap.add_argument("--path", default="latest", help="table directory inside the repository (revision mode)")
    ap.add_argument("--repo", default=".", help="git repository (revision mode)")
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    if os.path.isdir(args.old) and os.path.isdir(args.new):
        old, new = read_dir(args.old), read_dir(args.new)
    else:
        old = read_rev(args.repo, args.old, args.path)
        new = read_rev(args.repo, args.new, args.path)
    report = diff_trees(old, new)
    if not report:
        print("no changes")
    for name, out in report:
        print(f"{name}")
        for x in out:
            print(x)
        print()


if __name__ == "__main__":
    main()
