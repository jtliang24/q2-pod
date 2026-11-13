#!/usr/bin/env python3
"""The M1 Plus gates, in order, on one --dev build: every step every run, stopping at the first failure.

    python3 test/m1plus/gates.py BUILD            # all 19: q2compare --suites, a fresh build in BUILD, its gates
    python3 test/m1plus/gates.py BUILD --base TAG  # at a sync: q2compare against the tag merged
    python3 test/m1plus/gates.py BUILD --from boot  # after a test-only fix: the failed gate onward, same build
    python3 test/m1plus/gates.py BUILD --release  # tools/release_m1.py validate()'s subset, on a release build
    python3 test/m1plus/gates.py --list [--release]

Run it inside the devShell (direnv or nix develop). A run without the build step checks BUILD's
manifest source_sha256 against the tree first: a hashed-source edit (tools/*, patch/*, assets/**) needs
a fresh build and every gate, so --from and --only refuse a stale build. Edits under test/ keep it.

Logs and summary.txt (`step: exit N after Ts`) go to --out, by default work/gates/<timestamp>/.
Environment: GATES_PYTEST (the unit/fw runner, default this Python's pytest, else work/sync/venv's),
GATES_CLANG (a wrapped host clang for unit/fw, default nixpkgs#clang's wrapper), GATES_FFMPEG (an
ffmpeg binary for q2compare's suites, default nixpkgs#ffmpeg-headless; lame and flac come from nixpkgs)."""
import argparse, datetime, importlib.util, json, os, pathlib, shlex, shutil, subprocess, sys, time
sys.path.insert(0, sys.path[0] + '/../../tools')  # tools/ first
from build import ROOT, source_sha256

M1_ZIP = ROOT/'stock/M1 Plus Firmware V2.1.zip'
Q2_ZIP = ROOT/'stock/Q2 Firmware V1.32.zip'
MODEL = 'Shanling M1 Plus'


def nix_out(attr):
    """A nixpkgs package's first output path, from the flake's own nixpkgs input."""
    r = subprocess.run(['nix', 'build', '--inputs-from', ROOT, f'nixpkgs#{attr}', '--no-link', '--print-out-paths'],
                       check=True, stdout=subprocess.PIPE, text=True)
    return pathlib.Path(r.stdout.split()[0])


def q2compare(ctx):
    # 1.3.8's chapters and 1.6.7's player suites run /usr/bin/ffmpeg, and take lame and flac from PATH:
    # bind an ffmpeg in over an overlay (a tmpfs /usr/bin hides /bin/sh on merged-/usr hosts).
    ffmpeg = pathlib.Path(os.environ.get('GATES_FFMPEG') or nix_out('ffmpeg-headless')/'bin/ffmpeg')
    path = ':'.join([str(ffmpeg.parent), str(nix_out('lame')/'bin'), str(nix_out('flac.bin')/'bin'),
                     os.environ['PATH']])
    # TMPDIR=/tmp: under the devShell's long TMPDIR, peq's Tidal check fails on -Wformat-truncation.
    return ['bwrap', '--dev-bind', '/', '/', '--overlay-src', '/usr/bin', '--tmp-overlay', '/usr/bin',
            '--ro-bind', ffmpeg, '/usr/bin/ffmpeg', 'env', 'TMPDIR=/tmp', f'PATH={path}',
            sys.executable, 'test/q2compare.py', *([ctx.base] if ctx.base else []), '--suites', '--zip', Q2_ZIP]


def replaceable(build):
    """The build step deletes BUILD first, so BUILD must be missing or an M1 --dev build."""
    m = manifest(build)
    if build.exists() and not (m and m.get('model') == MODEL and m.get('dev')):
        sys.exit(f'{build} exists and is not an M1 --dev build: the build step replaces only one of those')


def build(ctx):
    replaceable(ctx.build)
    shutil.rmtree(ctx.build, ignore_errors=True)
    return [sys.executable, 'tools/build.py', M1_ZIP, '--dev', '--out', ctx.build]


def pytest(ctx, suite):
    if os.environ.get('GATES_PYTEST'):
        runner = shlex.split(os.environ['GATES_PYTEST'])
    elif importlib.util.find_spec('pytest'):
        runner = [sys.executable, '-m', 'pytest']
    elif (ROOT/'work/sync/venv/bin/python').is_file():
        runner = [ROOT/'work/sync/venv/bin/python', '-m', 'pytest']
    else:
        sys.exit('No pytest: set GATES_PYTEST, or make work/sync/venv with pytest in it')
    # The devShell's clang can't link a host .so (no crti.o): put the wrapped clang first, as a short
    # directory of two links rather than the wrapper's whole bin, which would shadow cc and ld too.
    links = ctx.out/'clangbin'
    if not links.is_dir():
        wrapper = pathlib.Path(os.environ.get('GATES_CLANG') or nix_out('clang')/'bin/clang').parent
        links.mkdir()
        for tool in ('clang', 'clang++'):
            (links/tool).symlink_to(wrapper/tool)
    return ['env', 'TMPDIR=/tmp', f'PATH={links}:{os.environ["PATH"]}', *runner, '-q', f'test/{suite}']


def boot(*flags, caps=None):
    def cmd(ctx):
        return [sys.executable, 'test/m1plus/boot.py', ctx.build, *flags,
                *(['--captures', ctx.out/caps] if caps else [])]
    return cmd


def suite(path, takes_build=True):
    return lambda ctx: [sys.executable, f'test/{path}.py', *([ctx.build] if takes_build else [])]


# name: (command builder, in the release subset). The order is the run order.
STEPS = {
    'q2compare': (q2compare, False),
    'peq': (suite('peq', False), 'only'),  # q2compare's suites run it; validate() runs it on its own
    'build': (build, False),
    # hook jumps, demo and rootfs diffs, updater rule, boot scripts
    'audit': (lambda ctx: [sys.executable, 'test/m1plus/build.py', '--build', ctx.build], True),
    # the payload under Unicorn, plus KNOWN GAP and NOT PORTED lines. Never with GAPS_DUMP: gaprun
    # then exits 0 whatever fails.
    'patch': (lambda ctx: ['env', '-u', 'GAPS_DUMP', sys.executable, 'test/m1plus/patch.py', ctx.build], True),
    # V2.1's demo under QEMU, stock vs patched (walked alongside), touch and key walk
    'boot': (boot(caps='boot-caps'), True),
    # saved V2.1 Home cards change nothing: the same build without them is the control
    'menu': (boot('--home-menu', caps='menu-caps'), False),
    # Home in Split, a card with long songs, a book and two photos: Library, Folder, Coverflow, Streaming, Shuffle
    'media': (boot('--media', caps='media-caps'), False),
    # Now Playing and Centred in both themes: back, bar, art, the volume band, the big cover
    'np': (boot('--now-playing'), False),
    # Spotify's page on a fake Soloify in both themes: layout, touch, scrub, the band, Hold Return, the
    # message view, and a paused session after local music
    'solo': (boot('--soloify'), False),
    # Back and Previous after a tap in the status bar, on Coverflow, Internet Radio and a V2.1 page
    'bar': (boot('--bar-keys'), False),
    'playback': (suite('m1plus/playback'), True),
    'm4b': (suite('m1plus/m4b'), True),
    'id3': (suite('m1plus/id3'), False),
    'headset': (suite('m1plus/headset_io'), False),
    'ldac': (suite('ldac'), True),
    'bluealsa': (suite('bluealsa'), False),
    # every hook, site and name classified: ported, native, Q2 only or NOT PORTED
    'ports': (suite('m1plus/ports', False), False),
    'unit': (lambda ctx: pytest(ctx, 'unit'), False),
    'fw': (lambda ctx: pytest(ctx, 'fw'), False),
}
FULL = [s for s, (_, rel) in STEPS.items() if rel != 'only']
RELEASE = [s for s, (_, rel) in STEPS.items() if rel]


def manifest(build):
    try:
        return json.loads((build/'manifest.json').read_text())
    except (OSError, ValueError):
        return None


class Context:
    def __init__(self, build, out, base):
        self.build, self.out, self.base = build, out, base


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('build', nargs='?', type=pathlib.Path, help='the M1 build directory (the build step makes it)')
    ap.add_argument('--from', dest='start', choices=FULL, metavar='STEP', help='rerun from STEP on the same build')
    ap.add_argument('--only', nargs='+', choices=list(STEPS), metavar='STEP', help='just these steps (debugging)')
    ap.add_argument('--release', action='store_true', help="validate()'s subset, on a release build: " +
                    ' '.join(RELEASE))
    ap.add_argument('--base', help="q2compare's base tag (default UPSTREAM_BASE; a sync passes the tag it merges)")
    ap.add_argument('--out', type=pathlib.Path, help='logs and summary.txt (default work/gates/<timestamp>/)')
    ap.add_argument('--list', action='store_true', help='print the steps and exit')
    args = ap.parse_args()
    steps = RELEASE if args.release else FULL
    if args.list:
        print('\n'.join(steps))
        return
    if not args.build: ap.error('BUILD is required')
    if sum(map(bool, (args.start, args.only, args.release))) > 1: ap.error('--from, --only and --release exclude each other')
    if args.start: steps = steps[steps.index(args.start):]
    if args.only: steps = [s for s in STEPS if s in args.only]
    build_dir = args.build.resolve()
    if 'build' in steps: replaceable(build_dir)
    if 'build' not in steps and any(s not in ('q2compare', 'peq', 'ports', 'unit', 'fw') for s in steps):
        m = manifest(build_dir)
        if not m: sys.exit(f'{build_dir}: no manifest.json; run every gate (the build step makes it)')
        if m.get('source_sha256') != source_sha256():
            sys.exit(f'{build_dir} was built from other sources (source_sha256): a hashed-source edit needs a '
                     'fresh build and every gate, so run without --from/--only')
    out = (args.out or ROOT/'work/gates'/datetime.datetime.now().strftime('%Y%m%d-%H%M%S')).resolve()
    out.mkdir(parents=True, exist_ok=True)
    ctx = Context(build_dir, out, args.base)
    env = {**os.environ, 'PYTHONUNBUFFERED': '1'}
    summary = open(out/'summary.txt', 'a')
    def report(line):
        print(line, flush=True)
        summary.write(line + '\n'); summary.flush()
    print(f'gates: {" ".join(steps)}\nlogs: {out}', flush=True)
    for s in steps:
        cmd = [str(a) for a in STEPS[s][0](ctx)]
        start = time.monotonic()
        with open(out/f'{s}.log', 'w') as log:
            log.write('$ ' + shlex.join(cmd) + '\n'); log.flush()
            rc = subprocess.run(cmd, cwd=ROOT, env=env, stdout=log, stderr=subprocess.STDOUT).returncode
        report(f'{s}: exit {rc} after {round(time.monotonic() - start)}s')
        if rc:
            report(f'FAILED at {s}: see {out/s}.log; after a test-only fix, rerun with --from {s}')
            sys.exit(rc)
    report('all passed')


if __name__ == '__main__':
    main()
