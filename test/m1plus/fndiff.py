#!/usr/bin/env python3
"""The payload functions two M1 Plus builds differ in: added, removed or changed. Usage:
python3 test/m1plus/fndiff.py OLD_BUILD NEW_BUILD

Each build directory keeps the payload's objects (navigation.o and the *.c.o), and each function
symbol's bytes are compared. A function changed when its bytes differ once each relocated field is
masked, or when its relocations reach other symbols or string literals (by their text). Moved code
and shifted addresses don't show. Only what patch.elf links is listed; navigation.c is built without
-ffunction-sections, so its unported hooks' handlers are linked, and listed, all the same. A sync lists what upstream changed in code the M1 runs, for
the device checklist (docs/m1plus-sync.md)."""
import pathlib, struct, sys

# R_MIPS_* field masks: 32 (word), 26 (j/jal target), HI16/LO16/GPREL16/GOT16/CALL16/PC16 (16 bits).
FIELD = {2: 0xffffffff, 4: 0x03ffffff, 5: 0xffff, 6: 0xffff, 7: 0xffff, 9: 0xffff, 10: 0xffff, 11: 0xffff}


def sections(path):
    """{function: (masked bytes, [(offset, type, target)])} of one ELF32 LE object: each FUNC symbol's
    bytes, so a section holding several (navigation.c is built without -ffunction-sections) splits."""
    d = path.read_bytes()
    shoff, = struct.unpack_from('<I', d, 0x20)
    shentsize, shnum, shstrndx = struct.unpack_from('<HHH', d, 0x2e)
    sh = [struct.unpack_from('<IIIIIIIIII', d, shoff + i * shentsize) for i in range(shnum)]
    def cstr(off): return d[off:d.index(b'\0', off)]
    names = [cstr(sh[shstrndx][4] + s[0]).decode() for s in sh]
    symtab = next(i for i, s in enumerate(sh) if s[1] == 2)
    strtab = sh[symtab][6]
    syms, funcs = [], []
    for k in range(sh[symtab][5] // 16):
        st_name, value, size, info, other, shndx = struct.unpack_from('<IIIBBH', d, sh[symtab][4] + 16 * k)
        name = cstr(sh[strtab][4] + st_name).decode() or (names[shndx] if 0 < shndx < len(names) else '')
        if name.startswith(('$.str', '.L.str')) and 0 < shndx < len(sh):  # a string literal: by its text
            name = 'string ' + repr(cstr(sh[shndx][4] + value).decode(errors='replace'))
        syms.append(name)
        if info & 0xf == 2 and 0 < shndx < len(sh) and names[shndx].startswith('.text'):
            funcs.append((shndx, value, size, name))
    out = {}
    for i, s in enumerate(sh):
        if not names[i].startswith('.text') or s[1] != 1: continue
        body = bytearray(d[s[4]:s[4] + s[5]])
        relocs = []
        for r in sh:
            if r[1] != 9 or r[7] != i: continue  # SHT_REL applying to this section
            for k in range(r[5] // 8):
                off, info = struct.unpack_from('<II', d, r[4] + 8 * k)
                kind, sym = info & 0xff, info >> 8
                if off + 4 <= len(body) and kind in FIELD:
                    w, = struct.unpack_from('<I', body, off)
                    struct.pack_into('<I', body, off, w & ~FIELD[kind] & 0xffffffff)
                relocs.append((off, kind, syms[sym]))
        for _, value, size, name in sorted(f for f in funcs if f[0] == i):
            out[name] = (bytes(body[value:value + size]),
                         sorted((o - value, t, x) for o, t, x in relocs if value <= o < value + size))
    return out


def linked(elf):
    """The names in a linked ELF's symbol table."""
    d = elf.read_bytes()
    shoff, = struct.unpack_from('<I', d, 0x20)
    shentsize, shnum = struct.unpack_from('<HH', d, 0x2e)
    sh = [struct.unpack_from('<IIIIIIIIII', d, shoff + i * shentsize) for i in range(shnum)]
    symtab = next(s for s in sh if s[1] == 2); strtab = sh[symtab[6]][4]
    return {d[strtab + n:d.index(b'\0', strtab + n)].decode()
            for n, in (struct.unpack_from('<I', d, symtab[4] + 16 * k) for k in range(symtab[5] // 16))}


def functions(build):
    """{(object, function): (bytes, relocs)} over a build's payload objects, for the functions its
    patch.elf links (--gc-sections drops the rest, an unported hook's code among them)."""
    build = pathlib.Path(build)
    objs = sorted(build.glob('*.o'))
    if not objs: sys.exit(f'{build}: no payload objects (*.o)')
    keep = linked(build/'patch.elf')
    out = {}
    for o in objs:
        for fn, v in sections(o).items():
            if fn in keep: out[(o.name, fn)] = v
    return out


def main():
    if len(sys.argv) != 3: sys.exit(__doc__)
    old, new = functions(sys.argv[1]), functions(sys.argv[2])
    rows = [('-', k) for k in sorted(old.keys() - new.keys())] + [('+', k) for k in sorted(new.keys() - old.keys())]
    rows += [('~', k) for k in sorted(old.keys() & new.keys()) if old[k] != new[k]]
    for mark, (obj, fn) in sorted(rows, key=lambda r: (r[1], r[0])):
        print(f'{mark} {obj}: {fn}')
    print(f'{sum(m == "~" for m, _ in rows)} changed, {sum(m == "+" for m, _ in rows)} added, '
          f'{sum(m == "-" for m, _ in rows)} removed, of {len(new)} functions')


if __name__ == '__main__':
    main()
