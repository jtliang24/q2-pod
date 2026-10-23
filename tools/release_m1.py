#!/usr/bin/env python3
"""Package the M1 Plus build locally; optionally upload and publish one verified release.

tools/release.py is upstream's and packages only the Q2. An M1 Plus release carries upstream's VERSION
and an M1 revision, named <VERSION>-m1.<n> by docs/m1plus-changelog.md's top entry."""
import argparse
import hashlib
import importlib.util
import io
import json
import pathlib
import re
import subprocess
import sys
import tarfile
import tempfile
import zipfile
from build import ROOT, VERSION, check, run, sha, source_sha256
from m1plus import M1PLUS_ZIP_SHA, M1PLUS_BIN_SHA, M1PLUS_DEMO_SHA, build

REPO = 'jtliang24/q2-pod'  # the fork: upstream's releases are the Q2's
MODEL = 'Shanling M1 Plus'
CHANGELOG = 'docs/m1plus-changelog.md'


def m1_tag(name):
    """The updater's 5-character identity of release name: V, VERSION's digits, then the M1 revision
    (1.2.2-m1.1 is V1221). The revision is one digit, so a release's tag never equals a Q2 one (V122S,
    V122I), a --dev one (lowercase last) or another release's."""
    found = re.fullmatch(r'(\d)\.(\d)\.(\d)-m1\.([1-9])', name)
    check(found, f'{name}: not an M1 release name (x.y.z-m1.n, n 1-9)')
    return 'V' + ''.join(found.groups())


def release_name():
    """docs/m1plus-changelog.md's top entry, - **<VERSION>-m1.<n>**: a release edits only that file
    (and VERSION, at a sync)."""
    entry = re.search(r'^- \*\*(\S+?)\*\*:', (ROOT/CHANGELOG).read_text(), re.M)
    check(entry, f'{CHANGELOG} has no - **<version>-m1.<n>**: entry')
    name = entry.group(1)
    m1_tag(name)
    check(name.startswith(VERSION + '-m1.'), f'{CHANGELOG}: the top entry {name} is not for VERSION {VERSION}')
    return name


def asset(name):
    return f'M1Plus.Firmware.{name}.zip'


def notes(name):
    """The entry's bold heading, then its text as bullets: one a sentence, or its nested bullets as written."""
    lines = (ROOT/CHANGELOG).read_text().splitlines()
    i = next(i for i, l in enumerate(lines) if l.startswith(f'- **{name}**'))
    title, text = lines[i][2:].split(':', 1)
    if not text.strip():
        body = []
        for l in lines[i+1:]:
            if not l.startswith('  '): break
            body.append(l[2:])
        return '\n'.join([title, *body])
    return '\n'.join([title, *('- '+s for s in re.split(r'(?<=[.!?]) +(?=[A-Z*"])', text.strip()))])


INSTALL = f'''Install, on stock V2.1 or any Q2 Pod build:
1. Unzip `{{asset}}` and copy `update.bin` to the root of the card.
2. Open **System settings → System Update → TF card update**, and leave the card in until the player restarts.

Back to stock: put Shanling's V2.1 `update.bin` at the root of the card and run the same TF card update.
'''


def release_body(out, record):
    name = record['tag']
    manifest = json.loads((out/'m1plus'/'manifest.json').read_text())
    return '\n'.join([notes(name), '', f'Q2 Pod {VERSION} for the {MODEL}, built on its stock firmware V2.1.', '',
                      INSTALL.format(asset=asset(name)), 'SHA-256:',
                      f'- {asset(name)}: `{record["assets"][asset(name)]}`',
                      f'- update.bin ({manifest["version"]}): `{manifest["update_sha256"]}`']) + '\n'


def validate(directory, name):
    """The manifest's identity, the archive against it and V2.1's updater rule, then the M1 gates."""
    m = json.loads((directory/'manifest.json').read_text())
    tag = m1_tag(name)
    check(m.get('model') == MODEL and m.get('release') == name and m.get('version') == tag and
          m.get('variant') == 'stock' and not m.get('dev'), 'Wrong release identity')
    check(m.get('input_sha256') in (M1PLUS_ZIP_SHA, M1PLUS_BIN_SHA) and m.get('stock_demo_sha256') == M1PLUS_DEMO_SHA,
          'Wrong stock identity')
    check(m.get('logo_source') == 'stock', 'A release keeps V2.1\'s own splash')
    for file, key in [('rootfs.squashfs', 'rootfs_sha256'), ('update.bin', 'update_sha256')]:
        check(sha((directory/file).read_bytes()) == m[key], f'{directory/file}: hash mismatch')
    with tarfile.open(directory/'update.bin') as t:
        check(t.getnames() == ['firmware_v20.info', 'recovery-update', 'recovery-update/xImage',
                               'recovery-update/rootfs.squashfs'], 'Unexpected update members')
        info = t.extractfile('firmware_v20.info').read().decode().splitlines()
        check(info[:2] == [MODEL, tag] and len(info) == 4, 'Wrong update identity')
        for line, member, key in zip(info[2:], ['recovery-update/xImage', 'recovery-update/rootfs.squashfs'],
                                    ['kernel_sha256', 'rootfs_sha256']):
            data = t.extractfile(member).read()
            check(line.split() == [hashlib.md5(data).hexdigest(), member] and sha(data) == m[key],
                  'Update payload mismatch')
    # test/build.py checks V2.1's names, test/patch.py the payload and test/boot.py demo under QEMU.
    for test, *args in (('peq',), ('build', '--build', directory), ('patch', directory), ('boot', directory),
                        ('playback', directory), ('m4b', directory), ('ldac', directory)):
        subprocess.run([sys.executable, ROOT/f'test/{test}.py', *map(str, args)], check=True)


def archive_bytes(directory):
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for file in ('update.bin', 'manifest.json'):
            info = zipfile.ZipInfo(file, (2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            z.writestr(info, (directory/file).read_bytes())
    return stream.getvalue()


def package(stock, out):
    check(not out.exists(), 'Release output must be a fresh directory')
    name = release_name()
    out.mkdir(parents=True)
    source = source_sha256()
    revision = run('git', '-C', ROOT, 'rev-parse', 'HEAD').strip()
    for suffix in ('', '-repeat'):
        build(stock, out/('m1plus'+suffix), ROOT/'assets/boot-logo.jpg', m1_release=(name, m1_tag(name)))
    # The byte comparisons below prove the repeat build; validate the first only.
    validate(out/'m1plus', name)
    a, b = out/'m1plus', out/'m1plus-repeat'
    check((a/'update.bin').read_bytes() == (b/'update.bin').read_bytes(), 'Non-reproducible update.bin')
    data = archive_bytes(a)
    check(data == archive_bytes(b), 'Non-reproducible ZIP')
    (out/asset(name)).write_bytes(data)
    check(source == source_sha256() and revision == run('git', '-C', ROOT, 'rev-parse', 'HEAD').strip(),
          'Source changed during release build')
    record = dict(tag=name, revision=revision, source_sha256=source, assets={asset(name): sha(data)})
    (out/'SHA256SUMS').write_text(f'{sha(data)}  {asset(name)}\n')
    (out/'release-notes.md').write_text(release_body(out, record))
    (out/'release.json').write_text(json.dumps(record, indent=2)+'\n')
    print(f'{name} ({m1_tag(name)}) validated and reproducible: {out}')


def upload(out, publish=False):
    record = json.loads((out/'release.json').read_text())
    name = record['tag']
    check(name == release_name() and record['source_sha256'] == source_sha256(), 'Wrong release source/tag')
    check(set(record['assets']) == {asset(name)}, 'Wrong release assets')
    # package() validated this tree; the ZIP bytes and source hash prove it is unchanged.
    data = (out/asset(name)).read_bytes()
    check(sha(data) == record['assets'][asset(name)] and data == archive_bytes(out/'m1plus'), 'Release ZIP mismatch')
    check((out/'SHA256SUMS').read_text() == f'{sha(data)}  {asset(name)}\n', 'Release checksums mismatch')
    (out/'release-notes.md').write_text(release_body(out, record))
    gh = ['gh', '--repo', REPO, 'release']
    # Listing distinguishes an absent tag from an authentication/network failure.
    releases = json.loads(run(*gh, 'list', '--limit', '1000', '--json', 'tagName,isDraft'))
    existing = next((r for r in releases if r['tagName'] == name), None)
    if existing:
        check(existing['isDraft'], 'Refusing to overwrite a published release')
    run(*gh, 'edit' if existing else 'create', name, '--draft', '--target', record['revision'],
        '--title', f'{name} (M1 Plus)', '--notes-file', out/'release-notes.md')
    run(*gh, 'upload', name, out/asset(name), '--clobber')
    with tempfile.TemporaryDirectory(prefix='m1-release-verify-') as tmp:
        run(*gh, 'download', name, '--dir', tmp)
        check((pathlib.Path(tmp)/asset(name)).read_bytes() == data, f'Remote asset mismatch: {asset(name)}')
    if publish:
        run(*gh, 'edit', name, '--draft=false')
    print(f'{"Published" if publish else "Verified draft"}: https://github.com/{REPO}/releases/tag/{name}')


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    commands = ap.add_subparsers(dest='command', required=True)
    p = commands.add_parser('package')
    p.add_argument('stock', type=pathlib.Path, help="stock V2.1's update.bin, or the vendor ZIP")
    p.add_argument('--out', type=pathlib.Path, required=True)
    p = commands.add_parser('upload')
    p.add_argument('out', type=pathlib.Path)
    p.add_argument('--publish', action='store_true')
    a = ap.parse_args()
    try:
        if a.command == 'package':
            # Validation runs the MIPS suite, so fail before two builds, not after them.
            check(importlib.util.find_spec('unicorn') is not None,
                  'Release validation needs the requirements.txt environment: pip install -r requirements.txt')
            package(a.stock, a.out.resolve())
        else:
            upload(a.out.resolve(), publish=a.publish)
    except (OSError, ValueError, KeyError, StopIteration, subprocess.CalledProcessError) as exc:
        ap.error(str(exc))
