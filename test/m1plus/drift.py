#!/usr/bin/env python3
"""How far upstream has moved past UPSTREAM_BASE, and which tags to merge next, by the cadence in
docs/m1plus-sync.md. A merge is due at TRIGGER (commits, or lines upstream changed in files the M1 also
changes: the conflict surface), at a structural change, or MAX_DAYS after the base's tag. It merges the
furthest settled tag within LIMIT. When even that leaves a merge due, the merge is past due: the plan is
a series of steps that leapfrogs to it. It lists; it doesn't fail."""
import argparse, re, subprocess, sys, time
sys.path.insert(0, sys.path[0] + '/..')  # test/
from q2compare import ROOT, base_commit, git

TRIGGER = {'commits': 100, 'surface': 2000}
LIMIT = {k: v * 3 // 2 for k, v in TRIGGER.items()}  # a step's size: a little past TRIGGER, not a stub after it
SETTLE = 12 * 3600  # a tag is settled once it is this old and no tag followed it this soon
MAX_DAYS = 14  # merge a settled tag at least this often, however small
# Memory layout and toolchain: each change to these goes in a step of its own, flashed (1.3.9's scratch move).
STRUCTURAL = ['patch/link.ld', 'flake.nix', 'flake.lock']
RELEASE = re.compile(r'^(\d+)\.(\d+)\.(\d+)$')  # upstream's tags; not ours (1.4.2-m1.1) or upstream/1.4.1


def commit_time(ref):
    return int(git('log', '-1', '--format=%ct', ref, text=True))


def tags_after(base):
    """Upstream's release tags past base, in version order, as (name, commit time)."""
    out = []
    for name in git('tag', '--list', text=True).split():
        m = RELEASE.match(name)
        if m and git('rev-parse', f'{name}^{{commit}}', text=True).strip() != base and subprocess.run(
                ['git', '-C', ROOT, 'merge-base', '--is-ancestor', base, name]).returncode == 0:
            out.append((tuple(map(int, m.groups())), name))
    return [(name, commit_time(name)) for _, name in sorted(out)]


def fork_files(base):
    """Upstream's files that this branch changes: where upstream's changes can conflict. README.md is the
    fork's own, and its conflicts keep ours."""
    upstream = set(git('ls-tree', '-r', '--name-only', base, text=True).splitlines())
    return {p for p in git('diff', '--name-only', base, 'HEAD', text=True).splitlines()
            if p in upstream and p != 'README.md'}


def drift(a, b, files):
    surface = 0
    for line in git('diff', '--numstat', a, b, text=True).splitlines():
        added, deleted, path = line.split('\t', 2)
        if path in files and added != '-':
            surface += int(added) + int(deleted)
    return {'commits': int(git('rev-list', '--count', f'{a}..{b}', text=True)), 'surface': surface}


def structural(a, b):
    return git('diff', '--name-only', a, b, '--', *STRUCTURAL, text=True).split()


def fits(d, limits):
    return all(d[k] < limits[k] for k in limits) if limits is TRIGGER else all(d[k] <= limits[k] for k in limits)


def due(base_name, names, settled, files, now):
    """Why a merge is due, or None: the drift to the newest settled tag reaches TRIGGER, a structural
    change has come, or MAX_DAYS have passed since the base's tag."""
    ready = [n for n in names if n in settled]
    if not ready: return None
    if not fits(drift(base_name, ready[-1], files), TRIGGER): return f'{ready[-1]} reaches the trigger'
    if any(structural(base_name, n) for n in names): return 'a structural change'
    age = (now - commit_time(base_name)) / 86400
    return f'{age:.0f} days since {base_name}' if age >= MAX_DAYS else None


def plan(base_name, names, settled, files):
    """The steps from base to the newest settled tag, as (from, to, drift, note): each the furthest
    settled tag within LIMIT, and a structural change in a step of its own."""
    steps, cur = [], base_name
    while True:
        rest = names[names.index(cur) + 1:] if cur in names else names
        ready = [n for n in rest if n in settled]
        if not ready: return steps
        # The first tag whose layout differs from cur's: a change reverted before its step ends isn't one.
        first_s = next((n for n in rest if structural(cur, n)), None)
        window, note = ready, ''
        if first_s:
            before = [n for n in ready if rest.index(n) < rest.index(first_s)]
            if before:
                window, note = before, f'stops short of {first_s}\'s structural change'
            elif structural(cur, ready[0]):  # the structural change, and the hotfixes it settled with
                to = ready[0]
                steps.append((cur, to, drift(cur, to, files),
                              f'structural: {", ".join(structural(cur, to))}; flash it'))
                cur = to
                continue
        within = [n for n in window if fits(drift(cur, n, files), LIMIT)]
        to = within[-1] if within else window[0]
        if not within: note = (note + '; ' if note else '') + 'over the limit, but the nearest settled tag'
        steps.append((cur, to, drift(cur, to, files), note))
        cur = to


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--fetch', action='store_true', help='git fetch upstream --tags first')
    args = ap.parse_args()
    if args.fetch:
        git('fetch', '--quiet', 'upstream', '--tags')
    base_name, base = base_commit(None)
    tags, now = tags_after(base), time.time()
    files = fork_files(base)
    settled = set()
    for i, (name, t) in enumerate(tags):
        nxt = tags[i + 1][1] if i + 1 < len(tags) else None
        if now - t >= SETTLE and (nxt is None or nxt - t >= SETTLE):
            settled.add(name)

    print(f'Base {base_name} ({time.strftime("%Y-%m-%d", time.localtime(commit_time(base)))}); '
          f'conflict surface: {len(files)} upstream files the M1 changes')
    print(f'{"tag":<8} {"date":<16} {"commits":>7} {"surface":>7}  state')
    for i, (name, t) in enumerate(tags):
        d = drift(base, name, files)
        prev = tags[i - 1][0] if i else base
        state = 'settled' if name in settled else 'superseded' if i + 1 < len(tags) else 'new'
        s = structural(prev, name)
        print(f'{name:<8} {time.strftime("%Y-%m-%d %H:%M", time.localtime(t)):<16} {d["commits"]:>7} '
              f'{d["surface"]:>7}  {state}{"  STRUCTURAL: " + ", ".join(s) if s else ""}')
    if not tags:
        print('(no upstream tags past the base: run with --fetch)')

    names = [n for n, _ in tags]
    why = due(base_name, names, settled, files, now)
    steps = plan(base_name, names, settled, files) if why else []
    print(f'\nTrigger {TRIGGER["commits"]} commits or {TRIGGER["surface"]} surface lines; '
          f'step limit {LIMIT["commits"]} or {LIMIT["surface"]}.')
    if not steps:
        print('Not due.')
    else:
        print(f'{"Past due" if len(steps) > 1 else "Due"} ({why}): '
              f'{" → ".join([steps[0][0]] + [s[1] for s in steps])}')
        for a, b, d, why in steps:
            print(f'  {a} → {b}: {d["commits"]} commits, {d["surface"]} surface lines{"  (" + why + ")" if why else ""}')


if __name__ == '__main__':
    main()
