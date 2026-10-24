#!/usr/bin/env python3
"""Bring a tag's test cases into an M1 Plus suite copy. Usage:
python3 test/m1plus/suitemerge.py OLD_BASE TAG SUITE

The copies in test/m1plus/ guard upstream's cases behind a hook or site (`if 'NAME' in SITES:`), which
re-indents them, so `git merge-file` makes each guarded section a conflict. This merge matches lines by
their text alone: each hunk of upstream's diff (OLD_BASE's test/SUITE.py to TAG's) goes where its lines
are in the copy, at the copy's indentation there. A hunk whose lines the copy changed or moved is
printed instead, for a hand merge. The copy is rewritten in place; run the suite on a fresh M1 build
after (docs/m1plus-sync.md)."""
import difflib, pathlib, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parents[2]


def show(ref, path):
    return subprocess.run(['git', '-C', ROOT, 'show', f'{ref}:{path}'], check=True, capture_output=True,
                          text=True).stdout.splitlines(True)


def indent(line):
    return len(line) - len(line.lstrip(' '))


def merge(ours, base, theirs):
    """(merged lines, [(base i1, i2, theirs j1, j2)] left for a hand merge)."""
    b2o = {}  # a base line's line in the copy, for each line they share, up to indentation
    strip = lambda lines: [l.strip() for l in lines]
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, strip(base), strip(ours), autojunk=False).get_opcodes():
        if tag == 'equal': b2o.update((i1 + k, j1 + k) for k in range(i2 - i1))
    edits, manual = [], []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, base, theirs, autojunk=False).get_opcodes():
        if tag == 'equal': continue
        if i2 > i1:  # the replaced lines must sit together in the copy
            mapped = [b2o.get(b) for b in range(i1, i2)]
            placed = None not in mapped and mapped == list(range(mapped[0], mapped[0] + len(mapped)))
            at = (mapped[0], mapped[-1] + 1, i1, mapped[0]) if placed else None
        else:  # an insertion: between two base lines that are neighbours in the copy too
            before, after = b2o.get(i1 - 1), b2o.get(i1)
            if before is not None and after in (None, before + 1): at = (before + 1, before + 1, i1 - 1, before)
            elif before is None and after is not None: at = (after, after, i1, after)
            else: at = None
        if at is None:
            manual.append((i1, i2, j1, j2)); continue
        o1, o2, anchor_b, anchor_o = at
        shift = indent(ours[anchor_o]) - indent(base[anchor_b])
        new = [(' ' * shift + l if shift >= 0 else l[-shift:]) if l.strip() else l for l in theirs[j1:j2]]
        edits.append((o1, o2, new))
    merged = list(ours)
    for o1, o2, new in sorted(edits, reverse=True):
        merged[o1:o2] = new
    return merged, manual


if __name__ == '__main__':
    if len(sys.argv) != 4: sys.exit(__doc__)
    old, tag, suite = sys.argv[1:]
    copy = ROOT/'test/m1plus'/f'{suite}.py'
    base, theirs = show(old, f'test/{suite}.py'), show(tag, f'test/{suite}.py')
    merged, manual = merge(copy.read_text().splitlines(True), base, theirs)
    copy.write_text(''.join(merged))
    for i1, i2, j1, j2 in manual:
        print(f'--- by hand: test/{suite}.py {old} lines {i1 + 1}-{i2}, {tag} lines {j1 + 1}-{j2}')
        print(''.join('-' + l for l in base[i1:i2]) + ''.join('+' + l for l in theirs[j1:j2]), end='')
    print(f'{copy.relative_to(ROOT)}: {tag} merged over {old}; {len(manual)} hunks by hand')
