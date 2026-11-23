"""Reads the attributes of Android's binary XML (AndroidManifest.xml in an
APK). Only start-element chunks and the string pool are decoded."""

import struct

TYPE_STRING = 0x03
TYPE_INT_DEC = 0x10
TYPE_INT_HEX = 0x11
TYPE_BOOL = 0x12


def _string_pool(d, o):
    _t, hsize, _size, count, _styles, flags, str_start, _sty = struct.unpack_from("<HHIIIIII", d, o)
    utf8 = flags & 0x100
    offs = struct.unpack_from(f"<{count}I", d, o + hsize)
    base = o + str_start
    out = []
    for so in offs:
        p = base + so
        if utf8:
            n = d[p]
            p += 2 if n & 0x80 else 1
            n = d[p]
            if n & 0x80:
                n = ((n & 0x7F) << 8) | d[p + 1]
                p += 2
            else:
                p += 1
            out.append(d[p:p + n].decode("utf-8", "replace"))
        else:
            n = struct.unpack_from("<H", d, p)[0]
            p += 2
            if n & 0x8000:
                n = ((n & 0x7FFF) << 16) | struct.unpack_from("<H", d, p)[0]
                p += 2
            out.append(d[p:p + 2 * n].decode("utf-16-le", "replace"))
    return out


def elements(d):
    """Yields (tag, {attribute: value}) for each element, in document order."""
    if struct.unpack_from("<H", d, 0)[0] != 0x0003:
        raise ValueError("not binary XML")
    o = struct.unpack_from("<H", d, 2)[0]
    strings = []
    while o < len(d):
        ctype, hsize, size = struct.unpack_from("<HHI", d, o)
        if ctype == 0x0001:
            strings = _string_pool(d, o)
        elif ctype == 0x0102:
            _ns, name, astart, asize, acount = struct.unpack_from("<IIHHH", d, o + hsize)
            attrs = {}
            p = o + hsize + astart
            for _ in range(acount):
                _ans, aname, raw, _sz, _r0, dtype, data = struct.unpack_from("<IIIHBBI", d, p)
                key = strings[aname] if aname < len(strings) else str(aname)
                if dtype == TYPE_STRING:
                    val = strings[data]
                elif dtype in (TYPE_INT_DEC, TYPE_INT_HEX):
                    val = data
                elif dtype == TYPE_BOOL:
                    val = bool(data)
                elif raw != 0xFFFFFFFF and raw < len(strings):
                    val = strings[raw]
                else:
                    val = data
                attrs[key] = val
                p += asize
            yield strings[name], attrs
        o += size
