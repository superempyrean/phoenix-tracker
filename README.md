# phoenix-tracker

The vocabulary of each Discord Phoenix build that rekindle depends on: the
wire's constants, the PropId table, element kinds, host modules and
methods, platform events, exports, the guest's data models, experiment
names and crate versions. Each is a sorted text table with one entry per
line, so `git diff` between two builds reads as a changelog. Addresses,
disassembly and struct offsets don't belong here.

This repository is private and has no license.

## Layout

`latest/` holds the tables of the newest build. Every build is one commit
that rewrites `latest/`, with a message naming the build
(`android 356207`), and a tag of the same name with a dash
(`android-356207`). There is no per-build copy of the tables. A tag already
freezes them, and a second copy would double every diff. To read an older
build, check out its tag or run `git show android-356207:latest/propids.tsv`.

| File | Contents |
|------|----------|
| `build.txt` | package, version name and code, libdiscord version, each APK with its sha256, and the libraries each ABI ships |
| `propids.tsv` | PropId and name, all of them |
| `kinds.txt` | the element kinds the platform interns, by index |
| `wire.txt` | turn version and ops, value tags, the host frame header and kinds, UI event ops |
| `host-calls.txt` | host modules and methods (`KeyCommands`, `KeyCommands.set`) and their ids |
| `events.txt` | platform events (`@frame`, `@screenReader`) and their ids |
| `atoms.tsv` | every other name in the same id table, mostly record keys |
| `ui-events.tsv` | the UI event names a node lists in `on`, with their PropIds |
| `exports.txt` | the host's dynamic exports, names only |
| `models/<Name>.txt` | the guest's serde fields for User, Member, Message, Channel, Role, Attachment, the cosmetics and the rest |
| `experiments.txt` | date-prefixed experiment names, and whether the host, the Hermes bundle or the dex names them |
| `guest-modules.txt` | the `wasm-app*` feature crates |
| `first-party-crates.txt` | every `crates/<name>` the host's source paths name |
| `gateway-events.txt` | the gateway dispatch events the host registers a handler for, in registry order |
| `reducers.tsv` | the per-domain gateway reducers behind `LIBDISCORD_REDUCERS_TABLE`: domain and event |
| `cache-tables.txt` | the tables of the host's cache store, in enum order |
| `drawables.tsv` | every drawable resource in the base APK: name, qualifiers and type, with the `ic_mana_*` count |
| `propid-types.tsv` | each PropId with the type the Android platform reads it as, and the classes that read it |
| `abi/<abi>/libs.tsv` | native libraries in the split: name, size, sha256 |
| `abi/<abi>/rustc.txt` | each library's `.comment` lines, `/rustc/<commit>/` paths and toolchain paths |
| `abi/<abi>/crates.txt` | vendored crates as `name@version`, from the host's source paths |

`host-calls.txt`, `events.txt` and `atoms.tsv` come from one id table of
1839 names that the guest and the platform share. They are split
into three files because they change for different reasons.

Tables are written once when every ABI that ships the host agrees on them.
Only genuinely per-ABI data goes under `abi/<abi>/`. `crates.txt` is there
because the dependencies differ: build 356207 links `chacha20`, `poly1305`
and `rand_chacha` on x86_64 only. If any other table differs between ABIs,
the extractor writes each ABI's copy under `abi/<abi>/`, lists the table in
`ABI-DIFFERENCES.txt` and exits with an error. Pass
`--allow-abi-differences` once you have looked at it.

The x86 split carries no Phoenix host (`liblibdiscord_wasm_host.so`), so
Phoenix doesn't ship for 32-bit x86. Only its `libs.tsv` and `rustc.txt` are
written.

A build with no Phoenix host in any split (357202) changes only
`build.txt`, the ABI tables, `drawables.tsv` and `experiments.txt`. The
extractor deletes the Phoenix tables and rewrites `wire.txt` for it.
Before staging anything, restore them with `git ls-files -d | xargs git
checkout --` and `git checkout -- latest/wire.txt`, so the next Phoenix
build diffs against the last one that had them.

## Running the extractor

The extractor needs Python 3.10 or later and nothing outside the standard
library. Pass the base APK and every ABI split:

```sh
python -I extract/extract.py \
  --apk discord-356207-base.apk \
  --apk discord-356207-config.arm64_v8a.apk \
  --apk discord-356207-config.armeabi_v7a.apk \
  --apk discord-356207-config.x86.apk \
  --apk discord-356207-config.x86_64.apk \
  --out latest
```

It reads the APKs as zip files, parses their members as bytes and never
runs anything from them, so keep `-I`. The one exception is
`propid-types.tsv`, which needs Java. `--jadx` names a jadx install
(`lib/*.jar`); the extractor copies the base APK's dex to a temporary
directory and runs jadx's command-line entry point on it
(`java -cp ... jadx.cli.JadxCLI --no-res --no-replace-consts --show-bad-code`),
never the GUI. That adds about a minute and a half. `--jadx-sources`
reuses an earlier jadx output made with the same flags. Without either
option the table is skipped, and `diff.py` reports it as removed. It replaces everything in `--out`.
A run over the five APKs of 356207 takes about 16 seconds, most of it in
reading code literals out of the two 64-bit hosts. The output is
deterministic. Never commit an APK, a `.so`, a dex or a bundle;
`.gitignore` refuses the usual names.

The extractor prints its cross-checks, and a failed one fails the run:

- the host's PropId table equals its own id->name array, and the platform's
  name array in `classes.dex`;
- the host's id table equals the platform's method table;
- every kind the platform interns occurs in the host.

## Diffing two builds

```sh
python -I extract/diff.py HEAD~1 HEAD
python -I extract/diff.py android-356207 android-357000
python -I extract/diff.py some/dir other/dir
```

Two revisions are read from `latest/` at each (`--path` changes that). Two
directories are compared as they are. The report lists added and removed
entries per table. For the id tables it also lists renames (an id whose
name changed) and calls out renumbering, a name whose PropId, method id or
kind index moved, because rekindle's anchors key on those numbers.
`git diff HEAD~1 -- latest/` shows the same changes line by line.

## What is extracted and what comes from the spec

Everything except `wire.txt` and the names in `ui-events.tsv` is read from
the build. In `wire.txt` each line says `extracted` or `spec`, and a check
column says what the build confirmed:

- The turn's version byte, the op codes 1 to 10 and the names of ops 1 to 9
  are read from the platform's turn decoder in `classes.dex`.
- The value tags 0 to 12 are confirmed by the platform value decoder's
  switch. Their names are the spec's.
- The 16-byte host frame header and kinds 1 to 4 are confirmed by the
  platform's `GuestHost.invoke`. The kind names are the spec's.
- The UI event ops are the spec's. The names of ops 1 and 3 to 8 are
  confirmed by the guest's event-name run in the host. The op numbers have
  no cheap check and are manual.

The spec is `docs/research/phoenix-wire-protocol.md` in rekindle-private.

How the other tables are found, briefly:

- PropIds: the host's sorted `(&str, id)` table whose ids are exactly
  0..n-1, found by shape and by three known names, not by address.
- Host calls, events and atoms: the host's sorted `(&str, id)` table that
  starts with `-` and holds `@` names. The platform's copy is the method
  whose 1839 strings read `"<name> <id>"`.
- Kinds and op names: string arrays built in the platform's static
  initializers, picked by their contents.
- Models from Serialize impls (User, Member, Message, Channel and its
  parts, Role, Attachment, Embed and its parts, Emoji, PollMedia,
  SnapshotMessage, MemberRoles): a function that loads the struct's name
  and then one field name per call. The fields are in declaration order.
- Models from Deserialize visitors (CurrentUser, DisplayNameStyles,
  PrimaryGuild, AvatarDecorationData, NameplateData, RoleColors, RoleTags):
  a visitor names no struct, so the extractor takes the smallest one whose
  fields include a few anchor fields set in `extract.py`. The fields are
  sorted. If a build adds a field to one of these, it shows up. If a build
  renames an anchor field, the model goes missing with a warning.
- Experiments: `&str` slices in the host's data, and strings in the Hermes
  bundle and the dex, matching a `YYYY-MM-name` pattern.
- Gateway events: the host's array of `{name ptr, name len, handler}`
  entries. The extractor finds the one entry named `MESSAGE_CREATE` and
  walks both ways until an entry stops holding an upper-case name in
  `.rodata` and a handler in `.text`. The pointers are read through the
  relocations (RELA, Android's packed APS2 and RELR). The technique is
  phoenix-unlock's registry walk.
- Reducers: the exported `LIBDISCORD_REDUCERS_TABLE` is a slice of
  `(&str domain, &[entry])` with the same entry shape. The extractor reads
  it through the symbol and checks it against the walk from the
  `READY_SUPPLEMENTAL` entry, which covers the same entries back to back.
- Cache tables: the store's table enum. Its `as_str` compiles to an i32
  offset table and a length table in `.rodata`; the extractor finds the
  pair from the variant `guild_versions`, not by scanning strings. On
  32-bit ARM the names are a pointer array that starts right after
  another enum's, so where it begins can't be told from data alone, and
  armeabi-v7a contributes no cache tables.
- Drawables: `resources.arsc`'s drawable type chunks give each entry's
  configuration and value. An XML drawable's type is its root element,
  read from the file's binary XML.
- Prop types: the platform keeps one handler per prop name in a registry
  class (the one that throws `prop <name> handled twice`), each wrapped in
  a class that its dispatch loop maps to one typed accessor. The extractor
  reads the registry's methods, the dispatch loop, the accessors and every
  registration call from jadx's Java, so no class or method name is
  hard-coded. Nested objects (span pieces, `forceValue`, motion specs) use
  PropIds as keys too; their reads through the platform's map class are
  listed as `key:<type>`.

Models come from the arm64-v8a and x86_64 hosts. The extractor doesn't
decode 32-bit ARM code, so armeabi-v7a contributes no models. On 356207
its host lacks one experiment name the 64-bit hosts have
(`2026-10-android-seamless-pip`), most likely because that build inlines
the string. The extractor warns about it and records the union.

The value variant the guest writes for each PropId isn't recorded. Reading
it takes disassembly of the guest's setter calls, which this extractor
avoids. `propid-types.tsv` records the reading side, which accepts a
narrower set of tags than the guest could send.

## CI later

The intended shape: a scheduled job fetches each new build from the
mobile build tracker, runs the extractor over `latest/`, and opens a pull
request whose diff is that rewrite of `latest/`. The PR body and the new
`CHANGELOG.md` entry are `diff.py HEAD~1 HEAD` on the result. Merging it is
the build's one commit, and the tag follows.
