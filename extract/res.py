"""Reads resources.arsc: every entry of one resource type, with the
configuration it is defined for and its value. Only the chunks needed for
that are decoded."""

import struct

import axml

RES_TABLE = 0x0002
RES_STRING_POOL = 0x0001
RES_PACKAGE = 0x0200
RES_TYPE = 0x0201

FLAG_SPARSE = 0x01
FLAG_OFFSET16 = 0x02
ENTRY_COMPLEX = 0x0001
ENTRY_COMPACT = 0x0008

TYPE_REFERENCE = 0x01
TYPE_STRING = 0x03

DENSITY = {120: "ldpi", 160: "mdpi", 213: "tvdpi", 240: "hdpi", 320: "xhdpi", 480: "xxhdpi",
           640: "xxxhdpi", 0xFFFE: "anydpi", 0xFFFF: "nodpi"}
UI_TYPE = {2: "desk", 3: "car", 4: "television", 5: "appliance", 6: "watch", 7: "vrheadset"}


def _chunks(d, o, end):
    while o + 8 <= end:
        ctype, hsize, size = struct.unpack_from("<HHI", d, o)
        if size < 8:
            break
        yield ctype, hsize, o, size
        o += size


def _locale(code):
    if code == b"\0\0":
        return ""
    if code[0] & 0x80:  # packed three-letter code
        a, b = code[1] & 0x1F, ((code[1] & 0xE0) >> 5) | ((code[0] & 0x03) << 3)
        c = (code[0] & 0x7C) >> 2
        return "".join(chr(0x61 + x) for x in (a, b, c))
    return code.decode("ascii", "replace")


def qualifiers(cfg):
    """A ResTable_config as aapt2 writes it in a directory name, for the
    fields resources use in practice."""
    size = struct.unpack_from("<I", cfg, 0)[0]
    cfg = cfg[:size].ljust(64, b"\0")
    mcc, mnc = struct.unpack_from("<HH", cfg, 4)
    lang, region = _locale(cfg[8:10]), _locale(cfg[10:12])
    orientation, _touch, density = struct.unpack_from("<BBH", cfg, 12)
    sdk = struct.unpack_from("<H", cfg, 24)[0]
    layout, ui = cfg[28], cfg[29]
    sw, wdp, hdp = struct.unpack_from("<HHH", cfg, 30)
    layout2, color = cfg[48], cfg[49]
    out = []
    if mcc:
        out.append(f"mcc{mcc}")
    if mnc:
        out.append(f"mnc{mnc}")
    if lang:
        out.append(lang + (f"-r{region}" if region else ""))
    out += {0x40: ["ldltr"], 0x80: ["ldrtl"]}.get(layout & 0xC0, [])
    if sw:
        out.append(f"sw{sw}dp")
    if wdp:
        out.append(f"w{wdp}dp")
    if hdp:
        out.append(f"h{hdp}dp")
    out += {1: ["small"], 2: ["normal"], 3: ["large"], 4: ["xlarge"]}.get(layout & 0x0F, [])
    out += {0x10: ["notlong"], 0x20: ["long"]}.get(layout & 0x30, [])
    out += {1: ["notround"], 2: ["round"]}.get(layout2 & 0x03, [])
    out += {1: ["nowidecg"], 2: ["widecg"]}.get(color & 0x03, [])
    out += {4: ["lowdr"], 8: ["highdr"]}.get(color & 0x0C, [])
    out += {1: ["port"], 2: ["land"], 3: ["square"]}.get(orientation, [])
    if ui & 0x0F in UI_TYPE:
        out.append(UI_TYPE[ui & 0x0F])
    out += {0x10: ["notnight"], 0x20: ["night"]}.get(ui & 0x30, [])
    if density:
        out.append(DENSITY.get(density, f"{density}dpi"))
    if sdk:
        out.append(f"v{sdk}")
    return "-".join(out)


def entries(arsc, type_prefix):
    """Yields (type, name, qualifiers, value) for each entry whose type name
    starts with `type_prefix`. `value` is the path for a file resource,
    ("ref", id) for a reference, ("data", type, data) for other plain
    values, and ("bag",) for a complex entry."""
    if struct.unpack_from("<H", arsc, 0)[0] != RES_TABLE:
        raise ValueError("not a resource table")
    hsize, total = struct.unpack_from("<HI", arsc, 2)
    globals_ = []
    for ctype, _h, o, size in _chunks(arsc, hsize, total):
        if ctype == RES_STRING_POOL:
            globals_ = axml._string_pool(arsc, o)
        elif ctype == RES_PACKAGE:
            yield from _package(arsc, o, size, globals_, type_prefix)


def _package(d, o, size, globals_, prefix):
    hsize = struct.unpack_from("<H", d, o + 2)[0]
    type_off, _lpt, key_off = struct.unpack_from("<III", d, o + 8 + 4 + 256)
    types = axml._string_pool(d, o + type_off)
    keys = axml._string_pool(d, o + key_off)
    for ctype, h, c, csize in _chunks(d, o + hsize, o + size):
        if ctype != RES_TYPE:
            continue
        tid, flags = d[c + 8], d[c + 9]
        count, start = struct.unpack_from("<II", d, c + 12)
        tname = types[tid - 1]
        if not tname.startswith(prefix):
            continue
        cfg = d[c + 20:c + h]
        quals = qualifiers(cfg)
        offs = c + h
        if flags & FLAG_SPARSE:
            slots = [(struct.unpack_from("<H", d, offs + 4 * k + 2)[0] * 4) for k in range(count)]
        elif flags & FLAG_OFFSET16:
            slots = [v * 4 if v != 0xFFFF else None
                     for v in struct.unpack_from(f"<{count}H", d, offs)]
        else:
            slots = [v if v != 0xFFFFFFFF else None for v in struct.unpack_from(f"<{count}I", d, offs)]
        for off in slots:
            if off is None:
                continue
            e = c + start + off
            esize, eflags = struct.unpack_from("<HH", d, e)
            if eflags & ENTRY_COMPACT:
                key, dtype, data = esize, eflags >> 8, struct.unpack_from("<I", d, e + 4)[0]
            else:
                key = struct.unpack_from("<I", d, e + 4)[0]
                if eflags & ENTRY_COMPLEX:
                    yield tname, keys[key], quals, ("bag",)
                    continue
                dtype, data = d[e + esize + 3], struct.unpack_from("<I", d, e + esize + 4)[0]
            if dtype == TYPE_STRING:
                yield tname, keys[key], quals, globals_[data]
            elif dtype == TYPE_REFERENCE:
                yield tname, keys[key], quals, ("ref", data)
            else:
                yield tname, keys[key], quals, ("data", dtype, data)
