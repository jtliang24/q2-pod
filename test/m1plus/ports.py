#!/usr/bin/env python3
"""The port report: every Q2 hook, call site and offsets.inc name, and what the M1 Plus does with it.
A hook or site the M1 doesn't have needs an M1PLUS_PORTS row (tools/m1plus.py), so a sync's new ones
fail this until each is classified; a row the M1 no longer needs fails it too. --unported prints only
the unported rows, for the roadmap's U4."""
import argparse, collections, re, sys
sys.path.insert(0, sys.path[0] + '/../../tools')  # tools/ first
from build import ROOT, HOOKS, IPOD_HOOKS
from m1plus import CALL_SITES, M1PLUS_HOOKS, M1PLUS_PORTS

STATUSES = ('ported', 'native', 'q2only', 'unported')
DEFINE = re.compile(r'^\s*#\s*define\s+(\w+)\b\s*(.*)$', re.M)


def defines(text):
    return {name: value.split('/*')[0].strip() for name, value in DEFINE.findall(text)}


def report():
    """Rows of (kind, name, status, why), and the problems that fail the run."""
    rows, problems = [], []
    ports = dict(M1PLUS_PORTS)
    for name, status_why in ports.items():
        if status_why[0] not in STATUSES: problems.append(f'{name}: status {status_why[0]!r} is not one of {STATUSES}')
    m1_symbols = {symbol: m1 for m1, (_, symbol, _) in M1PLUS_HOOKS.items()}
    for name, (_, symbol, _) in (HOOKS | IPOD_HOOKS).items():
        same = name if name in M1PLUS_HOOKS else m1_symbols.get(symbol)
        row = ports.pop(name, None)
        if same:
            if row: problems.append(f'hook {name}: M1PLUS_PORTS says {row[0]}, but the M1 hooks it ({same}); drop the row')
            rows.append(('hook', name, 'ported', '' if same == name else f'as {same}'))
        elif row: rows.append(('hook', name, *row))
        elif name in IPOD_HOOKS: rows.append(('hook', name, 'q2only', 'the iPod UI (roadmap 5)'))
        else: problems.append(f'hook {name} ({symbol}): not on M1 and not in M1PLUS_PORTS')
    for name in CALL_SITES['q2']:
        row = ports.pop(name, None)
        if name in CALL_SITES['m1plus']:
            if row: problems.append(f'site {name}: M1PLUS_PORTS says {row[0]}, but CALL_SITES has it for M1; drop the row')
            rows.append(('site', name, 'ported', ''))
        elif row: rows.append(('site', name, *row))
        else: problems.append(f'site {name}: not on M1 and not in M1PLUS_PORTS')
    problems += [f'{name}: M1PLUS_PORTS has a row, but the Q2 has no such hook or call site' for name in ports]
    # Names: the M1 compile fails on any name shared code the M1 builds uses without a value, so a Q2
    # name with none is used only by Q2 code.
    inc = (ROOT/'patch/offsets.inc').read_text()
    q2 = defines(inc[inc.index('#else'):]) | defines((ROOT/'patch/m1plus_q2.inc').read_text())
    q2.pop('M1PLUS')
    m1 = defines((ROOT/'patch/m1plus_offsets.inc').read_text())
    for name in q2:
        if name not in m1: rows.append(('name', name, 'q2only', 'used only by Q2 code'))
        elif m1[name] == 'M1_UNPORTED': rows.append(('name', name, 'unported', 'its code is unreachable on M1'))
        else: rows.append(('name', name, 'ported', ''))
    problems += [f'name {name}: M1_UNPORTED, but the Q2 has no such name'
                 for name, value in m1.items() if value == 'M1_UNPORTED' and name not in q2]
    return rows, problems


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--unported', action='store_true', help='print only the unported rows')
    args = ap.parse_args()
    rows, problems = report()
    if problems: sys.exit('Port report:\n' + '\n'.join(f'  {p}' for p in problems))
    if not args.unported:
        counts = collections.Counter((kind, status) for kind, _, status, _ in rows)
        for kind in ('hook', 'site', 'name'):
            total = sum(n for (k, _), n in counts.items() if k == kind)
            print(f'{kind}s: {total} ({", ".join(f"{counts[kind, s]} {s}" for s in STATUSES if counts[kind, s])})')
        print()
        for status in ('ported', 'native', 'q2only'):
            for kind, name, s, why in rows:
                if s == status and why and why != 'used only by Q2 code':
                    print(f'{status:8} {kind} {name}: {why}')
        print()
        m1_only = sorted(set(M1PLUS_HOOKS) - set(HOOKS | IPOD_HOOKS) -
                         {why[3:] for _, _, s, why in rows if why.startswith('as ')})
        print(f'M1-only hooks: {", ".join(m1_only)}')
        print(f'Names used only by Q2 code: {", ".join(n for k, n, s, _ in rows if k == "name" and s == "q2only")}')
        print()
    for kind, name, status, why in rows:
        if status == 'unported': print(f'NOT PORTED {kind} {name}: {why}')
    if not args.unported:
        print(f'Port report: {len(rows)} Q2 hooks, call sites and names, each classified for M1 Plus.')


if __name__ == '__main__':
    main()
