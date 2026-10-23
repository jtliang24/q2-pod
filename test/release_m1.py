#!/usr/bin/env python3
"""tools/release_m1.py's names, identity checks and failure paths, without network access or proprietary firmware."""
import json
import pathlib
import subprocess
import tempfile
from unittest.mock import patch
import sys; sys.path.insert(0, sys.path[0] + '/../tools')  # tools/ first
import build
import m1plus
import release_m1 as r

# The tag: V, VERSION's digits and the M1 revision. Never a Q2 tag, a --dev one or another release's.
assert r.m1_tag('1.2.2-m1.1') == 'V1221' and r.m1_tag('1.3.9-m1.9') == 'V1399'
for bad in ('1.2.2', '1.2.2-m1.0', '1.2.2-m1.10', '1.2.2-m2.1', '1.2.22-m1.1', 'V1221'):
    try: r.m1_tag(bad)
    except ValueError: pass
    else: raise AssertionError(f'Accepted {bad}')
tags = {r.m1_tag(f'{x}.{y}.{z}-m1.{n}') for x in range(10) for y in range(10) for z in range(10) for n in range(1, 10)}
dev = {build.dev_tag(n, e) for n in range(1, 36**3) for e in 'SI'}
assert len(tags) == 9000 and all(len(t) == 5 for t in tags)
assert not tags & dev and not tags & {f'V{x}{y}{z}{e}' for x in range(10) for y in range(10) for z in range(10) for e in 'SI'}

with tempfile.TemporaryDirectory() as tmp:
    root = pathlib.Path(tmp)
    (root/'docs').mkdir()
    changelog = root/r.CHANGELOG
    patch('release_m1.ROOT', root).start()
    v = build.VERSION
    # The top entry names the release, and must carry VERSION.
    changelog.write_text(f'# M1 Plus changelog\n\n- **{v}-m1.2**: Two. Three.\n- **{v}-m1.1**: One.\n')
    assert r.release_name() == f'{v}-m1.2' and r.notes(f'{v}-m1.2') == f'**{v}-m1.2**\n- Two.\n- Three.'
    for text in ('# M1 Plus changelog\n', '- **0.0.1-m1.1**: Old.\n', f'- **{v}**: Q2 style.\n'):
        changelog.write_text(text)
        try: r.release_name()
        except ValueError: pass
        else: raise AssertionError(f'Accepted {text!r}')
    # A nested entry keeps its bullets as written, one level out, up to the next entry.
    changelog.write_text(f'- **{v}-m1.1**:\n  - A.\n    - B.\n- **0.0.1-m1.1**: Old.\n')
    name = r.release_name()
    assert r.notes(name) == f'**{name}**\n- A.\n  - B.'

    # validate(): the release's identity, then the stock's, then the splash; then the files (absent here).
    good = dict(model=r.MODEL, release=name, version=r.m1_tag(name), variant='stock', dev=False,
                input_sha256=m1plus.M1PLUS_BIN_SHA, stock_demo_sha256=m1plus.M1PLUS_DEMO_SHA, logo_source='stock')
    d = root/'build'
    d.mkdir()
    for change, error in ((dict(), None), (dict(input_sha256=m1plus.M1PLUS_ZIP_SHA), None),
                          (dict(model='Shanling Q2'), 'release identity'), (dict(version='V122S'), 'release identity'),
                          (dict(dev=21), 'release identity'), (dict(release=f'{v}-m1.2'), 'release identity'),
                          (dict(input_sha256=build.Q2_TAR_SHA), 'stock identity'),
                          (dict(stock_demo_sha256=build.DEMO_SHA), 'stock identity'), (dict(logo_source='custom'), 'splash')):
        (d/'manifest.json').write_text(json.dumps(good | change))
        try:
            r.validate(d, name)
        except FileNotFoundError:
            assert error is None, change  # past the identity checks: no rootfs.squashfs here
        except ValueError as e:
            assert error and error in str(e), (change, e)
        else:
            raise AssertionError('validate() passed without a build')

    # package(): a failed or non-reproducible build leaves no release record.
    def fake_build(stock, directory, logo, m1_release=None, flip=False):
        assert m1_release == (name, r.m1_tag(name))
        directory.mkdir()
        (directory/'update.bin').write_bytes(b'b' if flip and directory.name.endswith('repeat') else b'a')
        (directory/'manifest.json').write_text(json.dumps(dict(version=m1_release[1], update_sha256='0')))
    for failure in ('build', 'reproducible'):
        out = root/f'package-{failure}'
        def builder(stock, directory, logo, m1_release=None):
            if failure == 'build' and directory.name.endswith('repeat'): raise ValueError('simulated build failure')
            fake_build(stock, directory, logo, m1_release, flip=True)
        with patch('release_m1.build', side_effect=builder), patch('release_m1.validate'), \
             patch('release_m1.run', return_value='revision'):
            try: r.package(pathlib.Path('update.bin'), out)
            except ValueError as e: assert ('simulated' if failure == 'build' else 'Non-reproducible') in str(e), e
            else: raise AssertionError(f'Accepted a {failure} failure')
        assert not (out/'release.json').exists()
    out = root/'package'
    with patch('release_m1.build', side_effect=fake_build), patch('release_m1.validate'), \
         patch('release_m1.run', return_value='revision'):
        r.package(pathlib.Path('update.bin'), out)
    record = json.loads((out/'release.json').read_text())
    zip_name = r.asset(name)
    assert record['tag'] == name and set(record['assets']) == {zip_name} and zip_name == f'M1Plus.Firmware.{name}.zip'
    body = (out/'release-notes.md').read_text()
    assert body.startswith(f'**{name}**\n- A.\n') and 'Back to stock' in body and f'- {zip_name}: `' in body
    assert f'update.bin ({r.m1_tag(name)})' in body and 'TF card update' in body

    # upload(): a failed step leaves the release a draft; only a verified one is published.
    for failure in ('upload', 'download', 'corrupt', None):
        calls = []
        def gh(*args):
            calls.append(args)
            command = args[4]
            if command == 'list': return '[]'
            if command == failure: raise subprocess.CalledProcessError(1, args)
            if command == 'download':
                (pathlib.Path(args[-1])/zip_name).write_bytes((out/zip_name).read_bytes() if failure != 'corrupt' else b'bad')
            return ''
        with patch('release_m1.run', side_effect=gh):
            try: r.upload(out, True)
            except (ValueError, subprocess.CalledProcessError): assert failure
            else: assert failure is None
        assert all(c[:3] == ('gh', '--repo', r.REPO) for c in calls)
        assert any('--draft=false' in c for c in calls) == (failure is None)
    # A published release is never overwritten, and a changed ZIP fails before GitHub is contacted.
    with patch('release_m1.run', side_effect=lambda *a: json.dumps([dict(tagName=name, isDraft=False)])):
        try: r.upload(out)
        except ValueError as e: assert 'published' in str(e)
        else: raise AssertionError('Overwrote a published release')
    (out/zip_name).write_bytes(b'changed')
    with patch('release_m1.run') as gh:
        try: r.upload(out)
        except ValueError: pass
        else: raise AssertionError('Accepted a changed ZIP')
        gh.assert_not_called()
print('M1 Plus release: tags, changelog entry, identity checks and build/upload failure paths passed.')
