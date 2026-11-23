"""A minimal DEX reader. It walks each method's bytecode once and keeps what
the extractor needs: the strings and integer literals it loads, the keys of
its switches, and the string arrays it builds. Bytecode is never run."""

import struct

# Code-unit width of each opcode (Dalvik formats).
SIZE = [1] * 256
for _op in (0x02, 0x05, 0x08, 0x13, 0x15, 0x16, 0x19, 0x1A, 0x1C, 0x1F, 0x20, 0x22, 0x23, 0x29, 0xFE, 0xFF):
    SIZE[_op] = 2
for _op in (0x03, 0x06, 0x09, 0x14, 0x17, 0x1B, 0x24, 0x25, 0x26, 0x2A, 0x2B, 0x2C, 0xFC, 0xFD):
    SIZE[_op] = 3
SIZE[0x18] = 5
SIZE[0xFA] = SIZE[0xFB] = 4
for _r in (range(0x2D, 0x3E), range(0x44, 0x6E), range(0x90, 0xB0), range(0xD0, 0xE3)):
    for _op in _r:
        SIZE[_op] = 2
for _r in (range(0x6E, 0x73), range(0x74, 0x79)):
    for _op in _r:
        SIZE[_op] = 3


class Method:
    __slots__ = ("cls", "name", "strings", "ints", "switches", "string_arrays")

    def __init__(self, cls, name):
        self.cls, self.name = cls, name
        self.strings = []        # const-string operands, in order
        self.ints = []           # integer literals, in order
        self.switches = []       # ("packed"|"sparse", [keys])
        self.string_arrays = []  # [str, ...] built with filled-new-array or aput-object


class Dex:
    def __init__(self, data):
        if data[:4] != b"dex\n":
            raise ValueError("not a DEX file")
        self.d = data
        u32 = self.u32
        self.sid_n, self.sid_o = u32(0x38), u32(0x3C)
        self.tid_o = u32(0x44)
        self.mid_o = u32(0x5C)
        self.cd_n, self.cd_o = u32(0x60), u32(0x64)
        self._strings = [None] * self.sid_n

    def u16(self, o):
        return struct.unpack_from("<H", self.d, o)[0]

    def u32(self, o):
        return struct.unpack_from("<I", self.d, o)[0]

    def s32(self, o):
        return struct.unpack_from("<i", self.d, o)[0]

    def uleb(self, o):
        r = s = 0
        while True:
            b = self.d[o]
            o += 1
            r |= (b & 0x7F) << s
            s += 7
            if b < 0x80:
                return r, o

    def string(self, i):
        s = self._strings[i]
        if s is None:
            o = self.u32(self.sid_o + 4 * i)
            _, o = self.uleb(o)
            e = self.d.index(b"\0", o)
            # MUTF-8; the strings this extractor reads are ASCII.
            s = self.d[o:e].decode("utf-8", "replace")
            self._strings[i] = s
        return s

    def strings(self):
        return [self.string(i) for i in range(self.sid_n)]

    def type_name(self, i):
        return self.string(self.u32(self.tid_o + 4 * i))

    def methods(self):
        for c in range(self.cd_n):
            base = self.cd_o + 32 * c
            cls = self.type_name(self.u32(base))
            cdata = self.u32(base + 24)
            if not cdata:
                continue
            o = cdata
            sf, o = self.uleb(o)
            inf, o = self.uleb(o)
            dm, o = self.uleb(o)
            vm, o = self.uleb(o)
            for _ in range(sf + inf):
                _, o = self.uleb(o)
                _, o = self.uleb(o)
            for cnt in (dm, vm):
                midx = 0
                for _ in range(cnt):
                    diff, o = self.uleb(o)
                    _, o = self.uleb(o)
                    code, o = self.uleb(o)
                    midx += diff
                    if code:
                        name = self.string(self.u32(self.mid_o + 8 * midx + 4))
                        yield self._walk(Method(cls, name), code)

    def _walk(self, m, code):
        d = self.d
        n = self.u32(code + 12)
        ib = code + 16
        sreg = {}   # register -> string it holds
        ireg = {}   # register -> int it holds
        arrays = {}  # register -> {index: string} for new-array of String
        string_type = None
        i = 0
        while i < n:
            a = ib + 2 * i
            op, hi = d[a], d[a + 1]
            if op == 0 and hi in (1, 2, 3):  # switch and array payloads
                if hi == 1:
                    i += self.u16(a + 2) * 2 + 4
                elif hi == 2:
                    i += self.u16(a + 2) * 4 + 2
                else:
                    w, cnt = self.u16(a + 2), self.u32(a + 4)
                    i += (cnt * w + 1) // 2 + 4
                continue
            if op in (0x1A, 0x1B):
                s = self.string(self.u16(a + 2) if op == 0x1A else self.u32(a + 2))
                m.strings.append(s)
                sreg[hi] = s
                ireg.pop(hi, None)
            elif op == 0x12:
                v = ((hi >> 4) ^ 8) - 8
                m.ints.append(v)
                ireg[hi & 15] = v
                sreg.pop(hi & 15, None)
            elif op in (0x13, 0x14):
                v = struct.unpack_from("<h", d, a + 2)[0] if op == 0x13 else self.s32(a + 2)
                m.ints.append(v)
                ireg[hi] = v
                sreg.pop(hi, None)
            elif op == 0x23:  # new-array vA, vB, type
                t = self.type_name(self.u16(a + 2))
                if t == "[Ljava/lang/String;":
                    arrays[hi & 15] = {}
                    m.string_arrays.append(arrays[hi & 15])
            elif op == 0x4D:  # aput-object vAA, vBB, vCC
                arr, idx = d[a + 2], d[a + 3]
                if arr in arrays and hi in sreg and idx in ireg:
                    arrays[arr][ireg[idx]] = sreg[hi]
            elif op in (0x24, 0x25):  # filled-new-array(/range)
                t = self.type_name(self.u16(a + 2))
                if t == "[Ljava/lang/String;":
                    if op == 0x24:
                        cnt, g, w = hi >> 4, hi & 15, self.u16(a + 4)
                        regs = [w & 15, (w >> 4) & 15, (w >> 8) & 15, (w >> 12) & 15, g][:cnt]
                    else:
                        c0 = self.u16(a + 4)
                        regs = list(range(c0, c0 + hi))
                    if all(r in sreg for r in regs):
                        m.string_arrays.append({k: sreg[r] for k, r in enumerate(regs)})
            elif op in (0x2B, 0x2C):
                p = a + 2 * self.s32(a + 2)
                cnt = self.u16(p + 2)
                if op == 0x2B:
                    k0 = self.s32(p + 4)
                    m.switches.append(("packed", [k0 + j for j in range(cnt)]))
                else:
                    m.switches.append(("sparse", [self.s32(p + 4 + 4 * j) for j in range(cnt)]))
            elif 0x01 <= op <= 0x09 or op in (0x0A, 0x0B, 0x0C) or 0x44 <= op <= 0x4C or 0x4E <= op <= 0x51 \
                    or 0x52 <= op <= 0x58 or 0x60 <= op <= 0x66 or 0x90 <= op <= 0xE2 or op in (0x1C, 0x1F, 0x22, 0x21):
                # Writes a register: forget what it held.
                dst = hi & 15 if (SIZE[op] == 1 or 0x52 <= op <= 0x58 or 0xB0 <= op <= 0xCF or 0xD0 <= op <= 0xD7 or op == 0x21) else hi
                if op in (0x02, 0x05, 0x08):
                    dst = hi
                elif op in (0x03, 0x06, 0x09):
                    dst = self.u16(a + 2)
                sreg.pop(dst, None)
                ireg.pop(dst, None)
            i += SIZE[op]
        m.string_arrays = [[arr[k] for k in sorted(arr)] for arr in m.string_arrays
                           if arr and sorted(arr) == list(range(len(arr)))]
        return m
