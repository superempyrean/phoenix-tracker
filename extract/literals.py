"""String literals referenced from code, grouped by function.

Rust passes a `&str` as a pointer and a length. This module finds the
pointer (ADRP+ADD on arm64, a RIP-relative LEA on x86_64) and, where the
length is a constant moved into the next argument register right after,
the length too. Functions are bounded by the .eh_frame_hdr search table.
Only bytes are decoded; nothing is executed. 32-bit ARM is not supported."""

import array
import bisect
import re
import struct


def function_starts(elf):
    h = elf.section(".eh_frame_hdr")
    if h is None:
        return None
    hb = elf.data[h.offset:h.offset + h.size]
    _ver, _eptr, fcnt_enc, tab_enc = hb[0:4]
    if fcnt_enc != 0x03 or tab_enc != 0x3B:  # udata4 count, datarel|sdata4 table
        return None
    (cnt,) = struct.unpack_from("<I", hb, 8)
    return sorted(h.addr + struct.unpack_from("<i", hb, 12 + 8 * k)[0] for k in range(cnt))


def _arm64_stops(y):
    """A branch: the length search stays in one block."""
    return (y & 0x7C000000 == 0x14000000      # B, BL
            or y & 0xFF000010 == 0x54000000   # B.cond
            or y & 0x7E000000 == 0x34000000   # CBZ, CBNZ
            or y & 0x7E000000 == 0x36000000   # TBZ, TBNZ
            or y & 0xFE1F0000 == 0xD61F0000)  # BR, BLR, RET


def _arm64_refs(elf):
    s = elf.section(".text")
    w = array.array("I")
    w.frombytes(elf.data[s.offset:s.offset + s.size])
    base, n = s.addr, len(w)
    pend = {}
    out = []
    for i in range(n):
        x = w[i]
        if x & 0x9F000000 == 0x90000000:  # ADRP
            imm = (((x >> 5) & 0x7FFFF) << 2) | ((x >> 29) & 3)
            if imm & (1 << 20):
                imm -= 1 << 21
            pend[x & 31] = (i, ((base + 4 * i) & ~0xFFF) + (imm << 12))
        elif x & 0xFFC00000 == 0x91000000:  # ADD Xd, Xn, #imm12
            rn = (x >> 5) & 31
            p = pend.get(rn)
            if p and i - p[0] <= 16:
                held = {x & 31}  # registers holding the pointer
                ln = None
                for j in range(i + 1, min(i + 12, n)):
                    y = w[j]
                    if _arm64_stops(y):
                        break
                    if y & 0x7FE00000 == 0x52800000 and (y & 31) - 1 in held:  # MOVZ len
                        ln = (y >> 5) & 0xFFFF
                        break
                    if y & 0xFFE0FFE0 == 0xAA0003E0 and (y >> 16) & 31 in held:  # MOV Xd, Xm
                        held.add(y & 31)
                    elif y & 0x9F000000 == 0x90000000 or y & 0xFFC00000 == 0x91000000:  # ADRP, ADD
                        held.discard(y & 31)  # redefined
                        if not held:
                            break
                out.append((base + 4 * i, p[1] + ((x >> 10) & 0xFFF), ln))
    return out


# SysV argument order: the length of a &str goes in the register after its pointer.
_NEXT_ARG = {7: 6, 6: 2, 2: 1, 1: 8, 8: 9}
_LEA = re.compile(rb"[\x48\x4c]\x8d[\x05\x0d\x15\x1d\x25\x2d\x35\x3d]", re.S)


def _x86_64_refs(elf):
    s = elf.section(".text")
    b = elf.data[s.offset:s.offset + s.size]
    out = []
    for m in _LEA.finditer(b):
        p = m.start()
        rex, modrm = b[p], b[p + 2]
        reg = ((modrm >> 3) & 7) | (8 if rex & 4 else 0)
        (disp,) = struct.unpack_from("<i", b, p + 3)
        target = s.addr + p + 7 + disp
        ln = None
        want = _NEXT_ARG.get(reg)
        if want is not None:
            q = p + 7
            for _ in range(4):  # a few instructions after the LEA
                if q + 6 > len(b):
                    break
                if want < 8 and b[q] == 0xB8 + want:
                    ln = struct.unpack_from("<I", b, q + 1)[0]
                    break
                if want >= 8 and b[q] == 0x41 and b[q + 1] == 0xB8 + want - 8:
                    ln = struct.unpack_from("<I", b, q + 2)[0]
                    break
                step = _x86_len(b, q)
                if not step:
                    break
                q += step
        out.append((s.addr + p, target, ln))
    return out


def _x86_len(b, q):
    """Length of a MOV or LEA between registers and memory (opcodes 89, 8B,
    8D, with or without a REX prefix), enough to step from a LEA to the MOV
    of its length. 0 for anything else, which stops the search."""
    p = q + (1 if b[q] & 0xF0 == 0x40 else 0)
    if b[p] not in (0x89, 0x8B, 0x8D):
        return 0
    modrm = b[p + 1]
    mod, rm = modrm >> 6, modrm & 7
    n = p + 2 - q
    if mod == 3:
        return n
    if rm == 4:  # SIB byte
        n += 1
        if mod == 0 and b[p + 2] & 7 == 5:
            return n + 4
    if mod == 0:
        return n + (4 if rm == 5 else 0)
    return n + (1 if mod == 1 else 4)


class Literals:
    """Literal references of one ELF, by function."""

    def __init__(self, elf):
        self.elf = elf
        if elf.machine == 183:
            refs = _arm64_refs(elf)
        elif elf.machine == 62:
            refs = _x86_64_refs(elf)
        else:
            raise NotImplementedError(f"code references for {elf.abi}")
        starts = function_starts(elf)
        if not starts:
            raise NotImplementedError("no .eh_frame_hdr search table")
        ro = elf.section(".rodata")
        refs = [r for r in refs if ro.contains(r[1])]
        self.targets = sorted({t for _, t, _ in refs})
        self.by_function = {}
        for pc, t, ln in refs:
            f = starts[bisect.bisect_right(starts, pc) - 1]
            self.by_function.setdefault(f, []).append(self.text(t, ln))

    def text(self, target, ln):
        """The literal at `target`: `ln` bytes when the length is known,
        otherwise up to the next referenced literal (at most 64 bytes)."""
        if ln is None or ln > 4096:
            j = bisect.bisect_right(self.targets, target)
            nxt = self.targets[j] if j < len(self.targets) else target + 64
            ln, exact = min(nxt - target, 64), False
        else:
            exact = True
        raw = self.elf.read(target, ln) or b""
        return raw.decode("utf-8", "replace"), exact
