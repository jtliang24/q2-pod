"""tools/ipod.py with the M1 Plus's screen (docs/m1plus-ipod-ui.md Phase 2): a second copy of the module,
loaded with the M1's PROFILE, so sys.modules['ipod'] stays the Q2's that tools/m1plus.py imports from.

The profile is the screen alone, from patch/m1plus_offsets.inc: UI_W, UI_H, STATUS_H, and GLASS_R (0, the
square corners). Every layout name keeps the Q2's value until its Phase 4 item gives it V2.1's, and no
build uses this copy before Phase 3 (the V2.1 audit)."""
import importlib.util
import re
from build import ROOT

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
