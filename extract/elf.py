"""A small ELF reader (32- and 64-bit, little-endian): sections, dynamic
symbols and relative relocations, including Android's packed APS2 format.
It only reads bytes; nothing in the file is executed."""

import struct

SHT_NOBITS = 8
SHT_RELA = 4
SHT_REL = 9
SHT_DYNSYM = 11
SHT_RELR = 19
SHT_ANDROID_REL = 0x60000001
SHT_ANDROID_RELA = 0x60000002

# e_machine -> (Android ABI, R_<arch>_RELATIVE)
MACHINES = {
    183: ("arm64-v8a", 1027),
    62: ("x86_64", 8),
    40: ("armeabi-v7a", 23),
    3: ("x86", 8),
}


class Section:
    def __init__(self, name, type_, addr, offset, size, link):
        self.name, self.type, self.addr = name, type_, addr
        self.offset, self.size, self.link = offset, size, link

    def contains(self, va):
        return self.addr <= va < self.addr + self.size


class Elf:
    def __init__(self, data):
        if data[:4] != b"\x7fELF" or data[5] != 1:
            raise ValueError("not a little-endian ELF file")
        self.data = data
        self.is64 = data[4] == 2
        self.word = 8 if self.is64 else 4
        self.wfmt = "<Q" if self.is64 else "<I"
        (self.machine,) = struct.unpack_from("<H", data, 0x12)
        if self.is64:
            (shoff,) = struct.unpack_from("<Q", data, 0x28)
            shentsize, shnum, shstrndx = struct.unpack_from("<HHH", data, 0x3A)
            shfmt = "<IIQQQQIIQQ"
        else:
            (shoff,) = struct.unpack_from("<I", data, 0x20)
            shentsize, shnum, shstrndx = struct.unpack_from("<HHH", data, 0x2E)
            shfmt = "<IIIIIIIIII"
        raw = []
        for i in range(shnum):
            name, type_, _fl, addr, offset, size, link, _info, _al, _es = \
                struct.unpack_from(shfmt, data, shoff + i * shentsize)
            raw.append((name, type_, addr, offset, size, link))
        stroff = raw[shstrndx][3]
        self.sections = []
        for name, type_, addr, offset, size, link in raw:
            e = data.index(b"\0", stroff + name)
            n = data[stroff + name:e].decode("ascii", "replace")
            self.sections.append(Section(n, type_, addr, offset, size, link))
        self._relative = None

    @property
    def abi(self):
        return MACHINES.get(self.machine, (f"machine-{self.machine}", None))[0]

    def section(self, name):
        for s in self.sections:
            if s.name == name:
                return s
        return None

    def bytes_of(self, name):
        s = self.section(name)
        if s is None or s.type == SHT_NOBITS:
            return b""
        return self.data[s.offset:s.offset + s.size]

    def va_to_offset(self, va):
        for s in self.sections:
            if s.type != SHT_NOBITS and s.addr and s.contains(va):
                return s.offset + (va - s.addr)
        return None

    def read(self, va, length):
        o = self.va_to_offset(va)
        if o is None or length < 0 or o + length > len(self.data):
            return None
        return self.data[o:o + length]

    def word_at(self, va):
        o = self.va_to_offset(va)
        if o is None:
            return None
        return struct.unpack_from(self.wfmt, self.data, o)[0]

    def dynamic_symbols(self):
        """(name, kind, defined) for every .dynsym entry."""
        out = []
        for s in self.sections:
            if s.type != SHT_DYNSYM:
                continue
            strsec = self.sections[s.link]
            ent = 24 if self.is64 else 16
            for j in range(1, s.size // ent):
                o = s.offset + j * ent
                if self.is64:
                    name, info, _other, shndx = struct.unpack_from("<IBBH", self.data, o)
                else:
                    name, _v, _sz, info, _other, shndx = struct.unpack_from("<IIIBBH", self.data, o)
                e = self.data.index(b"\0", strsec.offset + name)
                n = self.data[strsec.offset + name:e].decode("utf-8", "replace")
                kind = {0: "notype", 1: "object", 2: "func", 6: "tls", 10: "ifunc"}.get(info & 15, str(info & 15))
                out.append((n, kind, shndx != 0))
        return out

    def symbol(self, wanted):
        """(value, size) of the defined .dynsym entry named `wanted`, or None."""
        for s in self.sections:
            if s.type != SHT_DYNSYM:
                continue
            strsec = self.sections[s.link]
            ent = 24 if self.is64 else 16
            key = wanted.encode() + b"\0"
            for j in range(1, s.size // ent):
                o = s.offset + j * ent
                if self.is64:
                    name, _info, _other, shndx, value, size = struct.unpack_from("<IBBHQQ", self.data, o)
                else:
                    name, value, size, _info, _other, shndx = struct.unpack_from("<IIIBBH", self.data, o)
                p = strsec.offset + name
                if shndx != 0 and self.data[p:p + len(key)] == key:
                    return value, size
        return None

    def pointer_at(self, va):
        """The pointer stored at `va` once the loader has relocated it: the
        target of a relative relocation there, else the word itself."""
        rel = self.relative_relocs()
        return rel[va] if va in rel else self.word_at(va)

    def relative_relocs(self):
        """{place: target} for every R_*_RELATIVE relocation."""
        if self._relative is not None:
            return self._relative
        want = MACHINES.get(self.machine, (None, None))[1]
        tmask = 0xFFFFFFFF if self.is64 else 0xFF
        rel = {}
        for s in self.sections:
            body = self.data[s.offset:s.offset + s.size]
            if s.type in (SHT_RELA, SHT_REL):
                fmt = {(True, SHT_RELA): "<QQq", (False, SHT_RELA): "<IIi",
                       (True, SHT_REL): "<QQ", (False, SHT_REL): "<II"}[(self.is64, s.type)]
                n = struct.calcsize(fmt)
                for ent in struct.iter_unpack(fmt, body[:len(body) // n * n]):
                    if ent[1] & tmask == want:
                        rel[ent[0]] = ent[2] if s.type == SHT_RELA else self.word_at(ent[0])
            elif s.type in (SHT_ANDROID_RELA, SHT_ANDROID_REL):
                for off, info, addend in _aps2(body):
                    if info & tmask == want:
                        rel[off] = addend if s.type == SHT_ANDROID_RELA else self.word_at(off)
            elif s.type == SHT_RELR:
                for off in _relr(body, self.word):
                    rel[off] = self.word_at(off)
        self._relative = rel
        return rel


def _sleb_stream(b, pos):
    while pos < len(b):
        r = s = 0
        while True:
            x = b[pos]
            pos += 1
            r |= (x & 0x7F) << s
            s += 7
            if x < 0x80:
                break
        if x & 0x40:
            r -= 1 << s
        yield r


def _aps2(body):
    """Android packed relocations, as bionic's packed_reloc_iterator reads them."""
    if body[:4] != b"APS2":
        raise ValueError("packed relocations without the APS2 magic")
    it = _sleb_stream(body, 4)
    count = next(it)
    offset = next(it)
    info = addend = 0
    done = 0
    while done < count:
        size = next(it)
        flags = next(it)
        by_info, by_offset, by_addend, has_addend = flags & 1, flags & 2, flags & 4, flags & 8
        delta = next(it) if by_offset else 0
        if by_info:
            info = next(it)
        if has_addend and by_addend:
            addend += next(it)
        elif not has_addend:
            addend = 0
        for _ in range(size):
            offset += delta if by_offset else next(it)
            if not by_info:
                info = next(it)
            if has_addend and not by_addend:
                addend += next(it)
            yield offset, info, addend
        done += size


def _relr(body, word):
    fmt = "<Q" if word == 8 else "<I"
    bits = word * 8 - 1
    base = 0
    for (w,) in struct.iter_unpack(fmt, body):
        if w & 1 == 0:
            yield w
            base = w + word
        else:
            for i in range(bits):
                if (w >> (i + 1)) & 1:
                    yield base + i * word
            base += bits * word
