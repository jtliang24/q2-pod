#!/usr/bin/env python3
"""Q2 output against the upstream base: build UPSTREAM_BASE (from git archive) and this tree, Legacy and
iPod, from the vendor ZIP, and require byte-identical update.tar. On a difference, print the manifest
components that differ. --suites then runs the base's Q2 suites, as this tree has them, on its builds."""
import argparse, concurrent.futures, io, json, os, pathlib, shutil, subprocess, sys, tarfile, tempfile
sys.path.insert(0, sys.path[0] + '/../tools')  # tools/ first
from build import ROOT, ZIP_SHA, sha

VARIANTS = {'legacy': [], 'ipod': ['--ipod']}
# Every upstream tree's tools/build.py takes only the audited ZIP, so both sides build from it.
ZIPS = [ROOT/'stock/Q2 Firmware V1.32.zip']
CACHE = ROOT/'work/q2compare'  # the base's builds, by commit: a base never changes
# source_sha256 hashes tools/*.py and patch/*, which the M1 files are in; tools is the toolchain's versions.
IGNORED = {'source_sha256', 'tools'}
# How each of the base's test/*.py runs: on each Q2 build ('build' as --build), once, once with the
# arguments a function gives from the stock rootfs (stock_fs), the builds and a scratch directory, or not
# here. A suite the base adds fails the run until it is listed, so a sync can't skip it unseen.
HCIPLAYER, MCU = 'usr/bin/hciplayer', 'usr/data/libmcu-bare.bin'
SUITES = {
    'build': 'each', 'patch': 'each', 'playback': 'each', 'id3': 'each', 'm4b': 'each',
    'headset_io': 'each', 'ldac': 'each', 'bluealsa': 'each',
    'peq': 'host', 'mp3': 'host', 'remote': 'host', 'coverflow': 'host', 'release': 'host',
    'chapters': 'host',  # 1.3.8; --stock-root and --qemu add its bundled-FFmpeg checks
    'alsa': None,  # takes a qemu-mipsel binary as well as a build
    'ui_preview': None,  # draws review sheets of two builds; it checks nothing
    # 1.5.0's power and FLAC suites, on the stock files they patch; module_* are the others' libraries
    'aic': lambda fs, builds, tmp: [fs], 'aic_build': lambda fs, builds, tmp: [fs, *builds],
    'pwm': lambda fs, builds, tmp: [fs], 'pwm_mcu': lambda fs, builds, tmp: [fs],
    'pwm_build': lambda fs, builds, tmp: [fs, *builds], 'mcu_sleep_host': lambda fs, builds, tmp: [fs],
    'mcu_park': lambda fs, builds, tmp: [fs/MCU], 'mcu_sleep': lambda fs, builds, tmp: [fs/MCU],
    'rotator': lambda fs, builds, tmp: [fs/'module_driver/soc_rotator.ko'],
    'rotator_build': lambda fs, builds, tmp: builds,
    # flac_build fails on 1.5.0's own tree: its release-gate case predates the fast paths on by default
    # (69a9cbf) and reads a ZIP that isn't there. flac_frame takes upstream's FLAC fixture corpus.
    'flac_build': None, 'flac_frame': None, 'flac_lpc': lambda fs, builds, tmp: [fs/HCIPLAYER],
    'flac_output': lambda fs, builds, tmp: [fs/HCIPLAYER, '--work', tmp],
    'flac_sync': lambda fs, builds, tmp: ['--stock', fs/HCIPLAYER, '--out', tmp],
    'module_mips': None, 'module_regions': None,
}
# A suite's own environment: flac_sync's MIPS compile takes $CC, which the devShell sets to gcc.
ENVS = {'flac_sync': {'CC': 'clang'}}


def git(*args, **kw):
    return subprocess.run(['git', '-C', ROOT, *args], check=True, stdout=subprocess.PIPE, **kw).stdout


def base_commit(ref):
    """The base to compare with, as (name, commit). UPSTREAM_BASE's ref must still be its commit."""
    line = next(l for l in (ROOT/'UPSTREAM_BASE').read_text().splitlines() if l and not l.startswith('#'))
    name, recorded = line.split()
    commit = git('rev-parse', '--verify', f'{ref or name}^{{commit}}', text=True).strip()
    if (ref or name) == name and commit != recorded:
        sys.exit(f'UPSTREAM_BASE: {name} is {commit} here, not {recorded}')
    return ref or name, commit


def find_zip(path):
    for p in [path] if path else ZIPS:
        if p.is_file():
            if sha(p.read_bytes()) != ZIP_SHA: sys.exit(f'{p}: SHA-256 differs from the audited ZIP')
            return p.resolve()
    sys.exit(f'The vendor ZIP is needed (every upstream build takes only it): put it at {ZIPS[0]}, or pass --zip')


def snapshot(dest):
    """This tree as it stands, tracked and untracked files but not ignored ones, so an edit during the
    run can't mix into its builds, and the suites' source_sha256 checks see the sources built."""
    for name in git('ls-files', '-z', '--cached', '--others', '--exclude-standard').split(b'\0'):
        src = ROOT/os.fsdecode(name)
        if name and (src.is_file() or src.is_symlink()):
            (dest/os.fsdecode(name)).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest/os.fsdecode(name), follow_symlinks=False)


def build(src, zip_path, out, flags):
    env = {k: v for k, v in os.environ.items() if k != 'SOURCE_DATE_EPOCH'}  # mksquashfs refuses it
    out.mkdir(parents=True)
    with open(out.with_suffix('.log'), 'w') as log:
        r = subprocess.run([sys.executable, 'tools/build.py', zip_path, '--out', out, *flags], cwd=src, env=env,
                           stdout=log, stderr=subprocess.STDOUT)
    if r.returncode:
        tail = out.with_suffix('.log').read_text().splitlines()[-15:]
        raise RuntimeError(f'{out} failed to build:\n' + '\n'.join(tail))
    return json.loads((out/'manifest.json').read_text())


def base_source(commit):
    """The base's tree, from git archive once, in work/q2compare/<commit>/src."""
    d = CACHE/commit
    if not (d/'src').is_dir():
        tmp = d/'src.tmp'
        shutil.rmtree(tmp, ignore_errors=True); tmp.mkdir(parents=True)
        tarfile.open(fileobj=io.BytesIO(git('archive', commit))).extractall(tmp, filter='tar')
        tmp.rename(d/'src')


def base_build(commit, zip_path, variant, fresh):
    """The base's build of one variant, built once and kept in work/q2compare/<commit>/."""
    d = CACHE/commit
    if fresh or not (d/variant/'update.tar').is_file():
        shutil.rmtree(d/variant, ignore_errors=True)
        shutil.rmtree(d/f'{variant}.tmp', ignore_errors=True)
        build(d/'src', zip_path, d/f'{variant}.tmp', VARIANTS[variant])
        (d/f'{variant}.tmp').rename(d/variant)
    return d/variant


def differences(a, b):
    """The base's manifest a against the tree's b: each component that differs, most telling first."""
    lines = []
    for k in sorted((a.keys() | b.keys()) - IGNORED):
        x, y = a.get(k), b.get(k)
        if x == y: continue
        if k == 'patch_symbols' and x and y:
            moved = sorted((int(x[n], 16), n, y[n]) for n in x.keys() & y.keys() if x[n] != y[n])
            lines.append(f'  patch_symbols: {len(moved)} moved, from {moved[0][1]} ({hex(moved[0][0])} -> {moved[0][2]})'
                         if moved else '  patch_symbols: none moved')
            lines += [f'    only in {side}: {", ".join(sorted(names))}' for side, names in
                      (('the base', x.keys() - y.keys()), ('this tree', y.keys() - x.keys())) if names]
        elif k == 'changed_assets' and x is not None and y is not None:
            lines += [f'  changed_assets: {p}' for p in sorted(x.keys() | y.keys()) if x.get(p) != y.get(p)]
        else:
            lines.append(f'  {k}: {json.dumps(x)[:80]} -> {json.dumps(y)[:80]}')
    return lines


def stock_fs(build):
    """V1.32's rootfs, unpacked once from a build's stock.squashfs into work/q2compare/stockfs."""
    d = CACHE/'stockfs'
    if not d.is_dir():
        tmp = CACHE/'stockfs.tmp'
        shutil.rmtree(tmp, ignore_errors=True); tmp.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(['unsquashfs', '-no-xattrs', '-ignore-errors', '-d', tmp, build/'stock.squashfs'], check=True,
                       stdout=subprocess.DEVNULL)
        tmp.rename(d)
    return d


def suites(commit, src, builds, out):
    """The base's suites, from this tree's test/ (upstream's text there), on this tree's builds."""
    names = [p[len('test/'):-3] for p in git('ls-tree', '--name-only', commit, 'test/', text=True).split()
             if p.endswith('.py')]
    unknown = [n for n in names if n not in SUITES]
    if unknown: sys.exit(f'The base has suites q2compare.py does not run: {", ".join(unknown)}. Add them to SUITES')
    missing = [n for n in names if not (src/f'test/{n}.py').is_file()]
    if missing: sys.exit(f'This tree dropped the base\'s suites: {", ".join(missing)}')
    jobs = [(n, None, []) for n in names if SUITES[n] == 'host']
    jobs += [(n, v, ['--build', d] if n == 'build' else [d]) for v, d in builds.items()
             for n in names if SUITES[n] == 'each']
    if any(callable(SUITES[n]) for n in names):
        fs = stock_fs(next(iter(builds.values())))
        for n in names:
            if callable(SUITES[n]): (out/'scratch'/n).mkdir(parents=True, exist_ok=True)
        jobs += [(n, None, SUITES[n](fs, list(builds.values()), out/'scratch'/n)) for n in names if callable(SUITES[n])]
    (out/'logs').mkdir(exist_ok=True)
    def run(job):
        n, v, args = job
        log = out/'logs'/f'{v or "host"}-{n}.log'
        with open(log, 'w') as f:
            rc = subprocess.run([sys.executable, f'test/{n}.py', *map(str, args)], cwd=src, stdout=f,
                                stderr=subprocess.STDOUT, env={**os.environ, **ENVS.get(n, {})}).returncode
        last = (log.read_text().strip().splitlines() or [''])[-1][:100]
        return rc, f'{"ok    " if rc == 0 else "FAILED"} {v or "host"} {n}: {last}'
    with concurrent.futures.ThreadPoolExecutor(max(1, (os.cpu_count() or 2) // 2)) as pool:
        results = list(pool.map(run, jobs))
    for _, line in results: print(line)
    # The suites are upstream's text but for M1 seams; a changed one is where a Q2 case could go missing.
    changed = [n for n in names if (src/f'test/{n}.py').read_bytes() != (CACHE/commit/f'src/test/{n}.py').read_bytes()]
    print(f'Suites whose text differs from the base\'s: {", ".join(changed) or "none"}')
    failed = sum(rc != 0 for rc, _ in results)
    if failed: sys.exit(f'{failed} of {len(jobs)} suites failed; logs in {out/"logs"}')
    print(f'All {len(jobs)} suite runs passed.')


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('base', nargs='?', help='tag or commit to compare with (default: UPSTREAM_BASE)')
    ap.add_argument('--zip', type=pathlib.Path, help=f'the vendor ZIP (default: {ZIPS[0]})')
    ap.add_argument('--fresh', action='store_true', help="rebuild the base's builds instead of reusing them")
    ap.add_argument('--suites', action='store_true', help="then run the base's Q2 suites on this tree's builds")
    ap.add_argument('--keep', type=pathlib.Path, help="a fresh directory to keep this tree's snapshot and builds in")
    args = ap.parse_args()
    name, commit = base_commit(args.base)
    zip_path = find_zip(args.zip)
    if args.keep and args.keep.exists(): sys.exit(f'{args.keep} exists: --keep takes a fresh directory')
    tmp = None if args.keep else tempfile.TemporaryDirectory(prefix='q2-compare-')
    out = (args.keep or pathlib.Path(tmp.name)).resolve()
    src = out/'src'; src.mkdir(parents=True)
    snapshot(src)
    base_source(commit)
    print(f'Comparing with {name} ({commit[:7]}); this tree in {out}' if args.keep else
          f'Comparing with {name} ({commit[:7]})', flush=True)
    with concurrent.futures.ThreadPoolExecutor(4) as pool:
        base = {v: pool.submit(base_build, commit, zip_path, v, args.fresh) for v in VARIANTS}
        tree = {v: pool.submit(build, src, zip_path, out/v, flags) for v, flags in VARIANTS.items()}
        base = {v: f.result() for v, f in base.items()}
        tree = {v: f.result() for v, f in tree.items()}
    differ = False
    for v in VARIANTS:
        m = json.loads((base[v]/'manifest.json').read_text())
        if m.get('tools') != tree[v].get('tools'):  # a cached base from another toolchain: build it again
            print(f'{v}: the base was built with {m.get("tools")}; rebuilding it', flush=True)
            base_build(commit, zip_path, v, True)
            m = json.loads((base[v]/'manifest.json').read_text())
        if (base[v]/'update.tar').read_bytes() == (out/v/'update.tar').read_bytes():
            print(f'{v}: update.tar identical ({tree[v]["update_sha256"][:12]})')
        else:
            differ = True
            print(f'{v}: update.tar DIFFERS from {name}\'s', *differences(m, tree[v]), sep='\n')
    if differ: sys.exit(1)
    if args.suites: suites(commit, src, {v: out/v for v in VARIANTS}, out)
    print(f'Q2 Legacy and iPod update.tar are byte-identical to {name}\'s build.')


if __name__ == '__main__':
    main()
