"""Reads the string table of a Hermes bytecode bundle. The header layout
changes between bytecode versions, so the layout is checked against the
table it implies instead of being trusted."""

import struct

MAGIC = 0x1F1903C103BC1FC6
HEADER_SIZE = 128
# Bytes per small function header, by bytecode version. Unknown versions are
# tried with each size, and a size is taken only if the string table decodes.
FUNCTION_HEADER = {98: 12}


def strings(d):
    magic, version = struct.unpack_from("<QI", d, 0)
    if magic != MAGIC:
        raise ValueError("not a Hermes bytecode bundle")
    (_flen, _gci, nfunc, nkind, nident, nstr, novf, storage) = struct.unpack_from("<8I", d, 32)
    sizes = [FUNCTION_HEADER[version]] if version in FUNCTION_HEADER else [12, 16, 20, 24]
    for fsize in sizes:
        small = HEADER_SIZE + nfunc * fsize + nkind * 4 + nident * 4
        ovf = small + nstr * 4
        stor = ovf + novf * 8
        if stor + storage > len(d):
            continue
        out = []
        for i in range(nstr):
            (x,) = struct.unpack_from("<I", d, small + 4 * i)
            utf16, off, ln = x & 1, (x >> 1) & 0x7FFFFF, x >> 24
            if ln == 255:
                if off >= novf:
                    break
                off, ln = struct.unpack_from("<II", d, ovf + 8 * off)
            nbytes = ln * 2 if utf16 else ln
            if off + nbytes > storage:
                break
            b = d[stor + off:stor + off + nbytes]
            out.append(b.decode("utf-16-le", "replace") if utf16 else b.decode("latin-1"))
        else:
            return version, out
    raise ValueError(f"Hermes bytecode version {version}: string table not found")
