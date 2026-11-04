"""tools/ipod.py with the M1 Plus's screen (docs/m1plus-ipod-ui.md Phase 2): a second copy of the module,
loaded with the M1's PROFILE, so sys.modules['ipod'] stays the Q2's that tools/m1plus.py imports from.

The profile is the screen alone, from patch/m1plus_offsets.inc: UI_W, UI_H, STATUS_H, and GLASS_R (0, the
square corners). Every layout name keeps the Q2's value until its Phase 4 item gives it V2.1's.

Phase 3 adds the V2.1 patch around that copy: patch/m1plus_ipod.json (V1.32's pages mapped onto V2.1's, every
other section empty), and patch_asset and patch_code, which m1plus.build() runs on every build. A Phase 4 item adds
its page to REWRITES and its sites to the JSON; 4.1 adds the `styles` section, through patch_style."""
import functools
import importlib.util
import json
import re
from build import ROOT, check, sha

M1 = {m[1]: int(m[2], 0) for m in re.finditer(r'^#define\s+(\w+)\s+(0x[0-9A-Fa-f]+|\d+)\b',
                                               (ROOT/'patch/m1plus_offsets.inc').read_text(), re.M)}
PROFILE = {name: M1[name] for name in ('UI_W', 'UI_H', 'STATUS_H', 'GLASS_R')}


def load(profile=PROFILE):
    """A fresh tools/ipod.py, its constants computed for profile."""
    spec = importlib.util.spec_from_file_location('m1plus_ipod_screen', ROOT/'tools/ipod.py')
    module = importlib.util.module_from_spec(spec)
    module.PROFILE = profile
    spec.loader.exec_module(module)
    return module


ipod = load()

AUDIT = json.loads((ROOT/'patch/m1plus_ipod.json').read_text())
UI_ASSETS = AUDIT['assets'] | AUDIT['navbar_only'] | AUDIT['slide_only']

# V2.1 page path -> function(root) that edits the decoded page in place. A Phase 4 item adds its pages here.
REWRITES = {}


def patch_asset(path, data):
    """The page as the iPod UI wants it: audited, round-tripped, then its REWRITES entry applied, else unchanged."""
    check(sha(data) == UI_ASSETS[path], f'{path}: unaudited UI asset')
    root = ipod.decode(data)
    check(ipod.encode(root) == data, f'{path}: UI round trip differs')
    kind = 'dialog' if path.startswith('dialog/') else 'system_bar' if path == 'system_bar.bin' else 'window'
    check(root[0] == kind, f'{path}: expected a {kind} page')
    if path not in REWRITES:
        return data
    REWRITES[path](root)
    return ipod.encode(root)


def patch_style(rel, data):
    """The style file rel (styles/<rel>) with the audited edits (the iPod rows' transparent backgrounds, press greys and
    white accent text), through the copy's patch_style: it checks the file's hash and every edit's state count."""
    return ipod.patch_style(data, AUDIT['styles'][rel])


def patch_code(data, symbols):
    """The audited code edits (immediates, then row layout calls) on data, V2.1's demo; returns the manifest's changes."""
    changes = []
    word = functools.partial(ipod.patch_word, data, changes=changes)
    for group in AUDIT['immediates']:
        value = {'pitch': ipod.PITCH, 'body': ipod.BODY, 'art': ipod.ART, 'art_inset': ipod.ART_INSET,
                 'scroll': ipod.BOTTOM - 50, 'np_bar_x': ipod.NP_BAR[0],
                 'np_bar_w': ipod.NP_BAR[2]}.get(group['value'], group['value'])
        for address, instruction in group['sites']:
            old = int(instruction, 16)
            word(int(address, 16), old, (old & 0xffff0000) | value, group['purpose'])
    group = AUDIT['row_layout_calls']
    for address, instruction in group['sites']:
        word(int(address, 16), int(instruction, 16), ipod.jal(symbols['compact_set_row_layout']), group['purpose'])
    return changes
