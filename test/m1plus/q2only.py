#!/usr/bin/env python3
"""Upstream's changes to Q2-only code: each line that git diff <base> <tag> adds under patch/ and that,
in this tree, sits in a Q2-only branch (#if !M1PLUS, or the #else of #if M1PLUS). Such a branch has an
M1 counterpart, its other side or the patch/m1plus_* file that side includes, which the merge leaves as
it was. So each line printed is a change to make there too, or to rule out. Run it after a sync's
merge, before UPSTREAM_BASE moves: base defaults to UPSTREAM_BASE. It lists; it doesn't fail."""
import argparse, difflib, re, sys
sys.path.insert(0, sys.path[0] + '/..')  # test/
from q2compare import ROOT, base_commit, git

HUNK = re.compile(r'^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@', re.M)


def q2_only(lines):
    """For each line (1-based), whether it sits in a Q2-only preprocessor branch."""
    stack, out = [], [False]
    for line in lines:
        d = line.strip()
        if re.match(r'#\s*if', d):
            stack.append('q2' if re.match(r'#\s*if\s+!\s*M1PLUS\b', d) else
                         'm1' if re.match(r'#\s*if\s+M1PLUS\b', d) else '')
        elif re.match(r'#\s*el', d) and stack:  # #else, #elif: the other side, if it was ours
            stack[-1] = {'q2': 'm1', 'm1': 'q2'}.get(stack[-1], '')
        elif re.match(r'#\s*endif', d) and stack:
            stack.pop()
        out.append('q2' in stack)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('tag', help='the upstream tag or commit just merged')
    ap.add_argument('--base', help='the upstream base it was merged over (default: UPSTREAM_BASE)')
    args = ap.parse_args()
    _, base = base_commit(args.base)
    tag = git('rev-parse', '--verify', f'{args.tag}^{{commit}}', text=True).strip()
    found = 0
    for path in git('diff', '--name-only', base, tag, '--', 'patch/', text=True).split():
        if not (ROOT/path).is_file(): continue
        added = set()  # the tag's line numbers that the range added
        for m in HUNK.finditer(git('diff', '-U0', base, tag, '--', path, text=True)):
            added.update(range(int(m[1]), int(m[1]) + int(m[2] or 1)))
        theirs = git('show', f'{tag}:{path}', text=True).splitlines()
        ours = (ROOT/path).read_text().splitlines()
        inside = q2_only(ours)
        for op, a0, a1, b0, _ in difflib.SequenceMatcher(None, theirs, ours, autojunk=False).get_opcodes():
            if op != 'equal': continue
            for k in range(a1 - a0):
                if a0 + k + 1 in added and inside[b0 + k + 1]:
                    print(f'{path}:{b0 + k + 1}: {ours[b0 + k].strip()}')
                    found += 1
    print(f'{found} upstream lines in Q2-only branches, {args.tag} over {base[:7]}: check each one\'s M1 side.')


if __name__ == '__main__':
    main()
