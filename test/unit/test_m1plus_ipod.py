"""tools/m1plus_ipod.py's page rewrites on small synthetic V2.1 trees built to the shape each one checks for."""
import pytest

from tools import m1plus_ipod

STATES = ('normal', 'disable', 'focused')


def confirm():
    """V2.1's confirminfo_dialog.bin: a centred 260x180 box, its art and corners, Cancel and OK along its foot."""
    style = {f'style:{s}:{k}': v for s in STATES for k, v in (('round_radius', '12'), ('bg_color', '#00000000'),
                                                              ('bg_image', 'confirminfo_bg'), ('border_color', '#00000000'))}
    root = ['dialog', [0, 0, 260, 180], {'self_layout': 'default(x=c,y=m,w=260,h=180)', 'name': 'confirminfo_dialog', **style}, []]
    root[3] = [['button', [1, 131, 128, 48], {'name': 'btn_cancel', 'tr_text': 'msg_no'}, []],
               ['button', [131, 131, 128, 48], {'name': 'btn_enter', 'tr_text': 'msg_yes'}, []]]
    return root


def test_confirm_dialog():
    root = confirm()
    m1plus_ipod.confirm_dialog(root)
    top, w = m1plus_ipod.M1['CONFIRM_TOP'], m1plus_ipod.M1['UI_W']
    assert top == 112 and root[1] == [0, 0, w, top + 96] and root[2]['self_layout'] == 'default(x=0,y=0,w=100%,h=208)'
    assert all(root[2][f'style:{s}:bg_color'] == '#000000' for s in STATES)
    # its foot's 1 px rule: Light Mode flips the sheet to the page's paper (V063m pass, finding E)
    assert all((root[2][f'style:{s}:border_color'], root[2][f'style:{s}:border'], root[2][f'style:{s}:border_width']) ==
               ('#666666', 'bottom', '1') for s in STATES)
    assert not any(k.endswith(('round_radius', 'bg_image')) for k in root[2])
    for i, (n, name, text) in enumerate(zip(root[3], ('btn_cancel', 'btn_enter'), ('Cancel', 'OK'))):
        assert n[0] == 'button' and n[1] == [0, top + 48 * i, w, 48]
        assert (n[2]['name'], n[2]['text'], n[2]['focusable']) == (name, text, 'false') and 'tr_text' not in n[2]


@pytest.mark.parametrize('change', [lambda r: r[2].update(name='x'), lambda r: r[1].__setitem__(3, 181),
                                    lambda r: r[3][0][2].update(name='img_cancel'), lambda r: r[3].pop(),
                                    lambda r: r[3][1][1].__setitem__(1, 130), lambda r: r[3][0].__setitem__(0, 'image')])
def test_confirm_dialog_wants_stock(change):
    root = confirm()
    change(root)
    with pytest.raises(ValueError, match='^Unexpected confirm dialog$'):
        m1plus_ipod.confirm_dialog(root)


def test_confirm_dialog_rows_clear_the_prompts(monkeypatch):
    """A CONFIRM_TOP over Delete File's check (y 66, 40 tall) would put a row on it."""
    monkeypatch.setitem(m1plus_ipod.M1, 'CONFIRM_TOP', m1plus_ipod.CONFIRM_PROMPTS_END - 1)
    monkeypatch.setattr(m1plus_ipod.ipod, 'CONFIRM_TOP', m1plus_ipod.CONFIRM_PROMPTS_END - 1)
    with pytest.raises(ValueError, match='^Unexpected confirm dialog$'):
        m1plus_ipod.confirm_dialog(confirm())


def msginfo():
    """V2.1's msginfo_dialog.bin: a clear 260x180 dialog over msginfo_bg, its corners; its init adds the labels."""
    style = {f'style:{s}:{k}': v for s in STATES for k, v in (('bg_color', '#00000000'), ('bg_image', 'msginfo_bg'),
                                                              ('border_color', '#00000000'), ('round_radius', '12'))}
    return ['dialog', [0, 0, 260, 180], {'highlight': 'default(alpha=100)', 'name': 'msginfo_dialog',
                                         'self_layout': 'default(x=c,y=m,w=260,h=180)', **style}, []]


def test_msginfo_dialog():
    """The toast's box in styles, so Light Mode flips it with its text (V063m pass, finding F)."""
    root = msginfo()
    m1plus_ipod.msginfo_dialog(root)
    assert root[1] == [0, 0, 260, 180] and root[3] == []
    assert (root[2]['name'], root[2]['highlight'], root[2]['self_layout']) == (
        'msginfo_dialog', 'default(alpha=100)', 'default(x=c,y=m,w=260,h=180)')
    assert not any(k.endswith('bg_image') for k in root[2])
    for s in STATES:
        assert [root[2][f'style:{s}:{k}'] for k in ('bg_color', 'border_color', 'border', 'border_width', 'round_radius')] == [
            '#000000', '#666666', 'all', '1', '12']
    assert m1plus_ipod.REWRITES[m1plus_ipod.MSGINFO] is m1plus_ipod.msginfo_dialog


@pytest.mark.parametrize('change', [lambda r: r[2].update(name='x'), lambda r: r[1].__setitem__(3, 181),
                                    lambda r: r[3].append(['button', [0, 128, 100, 52], {}, []]),
                                    lambda r: r[2].update({'style:normal:bg_image': 'confirminfo_bg'})])
def test_msginfo_dialog_wants_stock(change):
    """rippercompleted_dialog's tree, a button over confirminfo_bg, isn't this one."""
    root = msginfo()
    change(root)
    with pytest.raises(ValueError, match='^Unexpected toast dialog$'):
        m1plus_ipod.msginfo_dialog(root)
