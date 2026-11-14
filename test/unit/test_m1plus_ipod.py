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


def test_clear_icon_is_audited(monkeypatch):
    """The unticked ring is rewritten only from V2.1's audited bytes (V064m pass)."""
    monkeypatch.setattr(m1plus_ipod.ipod, 'imagemagick', lambda *a, data: pytest.fail('ran ImageMagick'))
    with pytest.raises(ValueError, match='^unselect.png: unaudited ring icon$'):
        m1plus_ipod.clear_icon('unselect.png', b'not V2.1')


def test_clear_icon(monkeypatch):
    """White, alpha times grey: ImageMagick's arguments on the audited bytes."""
    calls = []
    monkeypatch.setitem(m1plus_ipod.AUDIT['clear_icons'], 'unselect.png', m1plus_ipod.sha(b'ring'))
    monkeypatch.setattr(m1plus_ipod.ipod, 'imagemagick', lambda *a, data: calls.append((a, data)) or b'png')
    assert m1plus_ipod.clear_icon('unselect.png', b'ring') == b'png'
    (args, data), = calls
    assert data == b'ring' and args[-1] == 'png:-' and ('-alpha', 'shape') in zip(args, args[1:])


def w(name, *children, kind='view', at=None, **props):
    return [kind, list(at or [0, 0, 10, 10]), {'name': name, **props}, list(children)]


def names(nodes):
    return [n[2].get('name') for n in nodes]


def bar_groups():
    """V2.1's bar groups: view_bar_left's play state and volume badges, view_bar_right's Bluetooth, link and Wi-Fi."""
    left = w('view_bar_left', *(w(n, kind='image', at=[0, 0, 20, 30]) for n in m1plus_ipod.STATUS_LEFT))
    right = w('view_bar_right', *(w(n, kind='image', at=[0, 0, 20, 30]) for n in m1plus_ipod.STATUS_RIGHT))
    return [left, w('bar_dclock', kind='digit_clock', at=[115, 0, 90, 30]), right,
            w('pgbar_battery', kind='progress_bar', at=[280, 8, 22, 12]), w('img_battery', kind='image', at=[278, 6, 30, 18])]


def status_bar():
    """V2.1's system_bar.bin: the two groups, its digit clock between them and the battery as a bar over its icon."""
    return ['system_bar', [0, 0, 320, 30], {'name': 'system_bar'}, bar_groups()]


def test_status_bar():
    """The chevron alone on the left; Bluetooth, the play state, Wi-Fi and the payload's battery slot on the right; the
    clock centred; the badges V2.1 still updates transparent in place at the bar's left."""
    root = m1plus_ipod.status_bar(status_bar())
    ui_w, height = m1plus_ipod.ipod.UI_W, m1plus_ipod.ipod.STATUS_H
    left, clock, right, pgbar, battery, *moved = root[3]
    assert names(left[3]) == ['img_back'] and left[3][0][1] == [0, 0, m1plus_ipod.BACK_W, height]
    assert left[3][0][2]['visible'] == 'false' and left[3][0][2]['image'] == 'bar_back'
    assert names(right[3]) == m1plus_ipod.STATUS_SHOWN[1:]
    assert [n[1][2] for n in right[3][:3]] == [42, 12, 14] and right[3][3][2]['visible'] == 'false'
    half = m1plus_ipod.CLOCK_W // 2
    assert left[1] == [0, 0, ui_w // 2 - half, height] and right[1] == [ui_w // 2 + half, 0, ui_w // 2 - half, height]
    assert clock[1][0] * 2 + clock[1][2] == ui_w and clock[2]['self_layout'].startswith(f'default(x={clock[1][0]},y=0,')
    assert right[2]['children_layout'].startswith('default(r=1,c=0,a=right,')
    assert names(moved) == ['img_volume', 'label_volume', 'img_digital', 'img_synclink']
    assert {n[2]['name'] for n in [*moved, pgbar, battery]} == set(m1plus_ipod.STATUS_HIDDEN)
    assert all(n[1][:2] == [0, 0] and n[1][3] == height and n[2]['opacity'] == '0' for n in [*moved, pgbar, battery])
    assert root[2]['style:normal:bg_color'] == '#000000' and root[2]['style:focused:border_color'] == '#00000000'


@pytest.mark.parametrize('change,message', [
    (lambda r: r[3].reverse(), 'Unexpected status bar'), (lambda r: r.__setitem__(0, 'view'), 'Unexpected status bar'),
    (lambda r: r[3][0][3].pop(), 'Unexpected status bar widgets'),
    (lambda r: r[3][2][3][0][2].update(name='img_bt'), 'Unexpected status bar widgets')])
def test_status_bar_wants_stock(change, message):
    root = status_bar()
    change(root)
    with pytest.raises(ValueError, match=f'^{message}$'):
        m1plus_ipod.status_bar(root)


def test_status_bar_battery_room(monkeypatch):
    """BATT_ROOM is what the 320 px bar leaves the right group, and the widest group must fit it."""
    monkeypatch.setattr(m1plus_ipod.ipod, 'BATT_ROOM', m1plus_ipod.ipod.BATT_ROOM + 1)
    with pytest.raises(ValueError, match='^Status bar battery needs'):
        m1plus_ipod.status_bar(status_bar())
    monkeypatch.setattr(m1plus_ipod.ipod, 'BATT_ROOM', m1plus_ipod.ipod.BATT_ROOM - 1)
    monkeypatch.setattr(m1plus_ipod.ipod, 'CLOCK_GAP', m1plus_ipod.ipod.CLOCK_GAP + 1)
    with pytest.raises(ValueError, match='^Status bar battery needs'):
        m1plus_ipod.status_bar(status_bar())


def volume():
    """V2.1's volume_dialog.bin: a 42 px strip of its icon, bar and level over a full page under the bar."""
    ui_w, top, bottom = m1plus_ipod.ipod.UI_W, m1plus_ipod.ipod.STATUS_H, m1plus_ipod.ipod.BOTTOM
    strip = w('view_page1', *(w(n) for n in ('img_vol', m1plus_ipod.M1_STR['VIEW_VOL'], 'label_vol')))
    page = w('view_page2', self_layout=f'default(x=0,y={top},w=100%,h={bottom})')
    return ['dialog', [0, 0, ui_w, 42], {'name': 'volume_dialog', 'highlight': 'default(alpha=0)'}, [strip, page]]


def test_volume_dialog():
    """Clear and full screen, unhighlighted, its strip filling it with nothing of V2.1's drawn: vol_paint draws it."""
    root = m1plus_ipod.volume_dialog(volume())
    strip, page = root[3]
    assert root[1] == [0, 0, m1plus_ipod.ipod.UI_W, m1plus_ipod.ipod.UI_H] and 'highlight' not in root[2]
    assert all(n[2][f'style:{s}:bg_color'] == '#00000000' for n in (root, strip) for s in STATES)
    assert all(root[2][f'style:{s}:border_color'] == '#00000000' for s in STATES)
    assert strip[2]['self_layout'] == 'default(x=0,y=0,w=100%,h=100%)'
    icon, bar, label = strip[3]
    assert icon[2]['opacity'] == '0' and bar[2]['visible'] == label[2]['visible'] == 'false'
    assert page == volume()[3][1]


@pytest.mark.parametrize('change,message', [
    (lambda r: r[2].update(highlight='default(alpha=100)'), 'Unexpected volume dialog'),
    (lambda r: r[1].__setitem__(3, 43), 'Unexpected volume dialog'), (lambda r: r[3].reverse(), 'Unexpected volume pages'),
    (lambda r: r[3][0][3].pop(), 'Unexpected volume strip'), (lambda r: r[3][1][2].update(self_layout=''), 'Unexpected volume strip')])
def test_volume_dialog_wants_stock(change, message):
    root = volume()
    change(root)
    with pytest.raises(ValueError, match=f'^{message}$'):
        m1plus_ipod.volume_dialog(root)


def bigcover():
    """V2.1's bigcover_page.bin: the art, a square from the top left, then the title at y 340 and the artist."""
    art = w(m1plus_ipod.M1_VIEW_BIGCOVER, kind='image', at=[0, 0, m1plus_ipod.BC_ART, m1plus_ipod.BC_ART], draw_type='scale_auto',
            image=m1plus_ipod.M1_STR['ICON_BIGCOVER'])
    return ['window', [0, 0, 320, 480], {'name': 'bigcover_page'},
            [art, w('scrlabel_title', kind='hscroll_label', at=[0, 340, m1plus_ipod.BC_ART, 22]), w('scrlabel_artist', kind='hscroll_label')]]


def test_bigcover_page():
    """Full screen and black, the art a centred square, a shade over its foot with the title centred in it, the artist
    transparent (V2.1's refresh shows it)."""
    root = m1plus_ipod.bigcover_page(bigcover())
    art, shade, title, artist = root[3]
    ui_h, side, shade_h = m1plus_ipod.ipod.UI_H, m1plus_ipod.BC_ART, m1plus_ipod.BC_SHADE_H
    y = (ui_h - side) // 2
    assert root[2]['fullscreen'] == 'true' and all(root[2][f'style:{s}:bg_color'] == '#000000' for s in STATES)
    assert art[1] == [0, y, side, side] and art[2]['self_layout'] == f'default(x=0,y={y},w={side},h={side})'
    assert shade[1] == [0, y + side - shade_h, side, shade_h] and shade[2]['name'] == 'view_shade'
    pad = m1plus_ipod.ipod.inc('BC_TITLE_PAD')
    assert title[1] == [pad, y + side - shade_h + (shade_h - 22) // 2, side - 2 * pad, 22]
    assert artist[2]['opacity'] == '0'


@pytest.mark.parametrize('change,message', [
    (lambda r: r[2].update(fullscreen='true'), 'Unexpected big cover'), (lambda r: r[3].pop(), 'Unexpected big cover'),
    (lambda r: r[3][0][2].update(draw_type='center'), 'Unexpected big cover layout'),
    (lambda r: r[3][1][1].__setitem__(1, 300), 'Unexpected big cover layout')])
def test_bigcover_page_wants_stock(change, message):
    root = bigcover()
    change(root)
    with pytest.raises(ValueError, match=f'^{message}$'):
        m1plus_ipod.bigcover_page(root)


def quick():
    """V2.1's dropdown_dialog.bin: the sysbar, the eight switches over their labels in two rows (y 14 and 114), and the
    brightness row of the slider between its two suns."""
    controls = []
    for i, (icon, label) in enumerate(zip(m1plus_ipod.QS_ICONS, m1plus_ipod.QS_LABELS)):
        controls += [w('img_' + icon, kind='image', at=[i % 4 * 80, (14, 114)[i // 4], 50, 50]),
                     w('label_' + label, kind='label', **{'style:normal:font_size': '18'})]
    light = w('view_backlight', w('image0', kind='image', at=[0, 0, 20, 20]), w('slider_backlight', kind='slider', slide_with_bar='true'),
              w('image1', kind='image', at=[0, 0, 20, 20]), **{'style:normal:bg_image': 'pill', 'style:normal:round_radius': '8'})
    sysbar = w('view_sysbar', *bar_groups())
    return ['dialog', [0, -340, m1plus_ipod.ipod.UI_W, 340], {'name': 'dropdown_dialog'}, [sysbar, w('view_switchs', *controls), light]]


def test_quick_settings():
    """Four columns of icons with 16 px labels under them, the brightness row plain under them where the volume panel
    covers it, and the sysbar as the bar's: the clock centred, Bluetooth, the play state and Wi-Fi right of it."""
    root = m1plus_ipod.quick_settings(quick())
    sysbar, menu, light = root[3]
    col, pitch = m1plus_ipod.QS_COLUMN, m1plus_ipod.QS_PITCH
    named = {n[2]['name']: n for n in menu[3]}
    for i, (icon, label) in enumerate(zip(m1plus_ipod.QS_ICONS, m1plus_ipod.QS_LABELS)):
        x, y = i % 4 * col, i // 4 * pitch
        assert named['img_' + icon][1] == [x + (col - 50) // 2, y, 50, 50], icon
        text = named['label_' + label]
        assert text[1][1] == y + 50 + m1plus_ipod.QS_LABEL_GAP and text[1][0] * 2 + text[1][2] == 2 * x + col, label
        assert all(text[2][f'style:{s}:font_size'] == '16' and text[2][f'style:{s}:text_align_h'] == 'center' for s in STATES)
    assert menu[1] == [0, m1plus_ipod.QS_TOP, m1plus_ipod.ipod.UI_W, 2 * pitch - m1plus_ipod.QS_ROW_GAP]
    assert light[1][1] == m1plus_ipod.M1['VOL_PANEL_Y'] and light[1][3] == m1plus_ipod.M1['VOL_PANEL_H']
    assert not any('bg_image' in k or 'round_radius' in k for k in light[2])
    dim, slider, bright = light[3]
    assert dim[1][0] + bright[1][0] + 20 == m1plus_ipod.ipod.UI_W and slider[1][0] * 2 + slider[1][2] == m1plus_ipod.ipod.UI_W
    left, clock, right, pgbar, battery, *hidden = sysbar[3]
    assert left[3] == [] and names(right[3]) == ['img_btclass', 'img_playstate', 'img_wifi']
    assert clock[1][0] * 2 + clock[1][2] == m1plus_ipod.ipod.UI_W and right[1][0] == clock[1][0] + clock[1][2]
    assert names(hidden) == ['img_volume', 'label_volume', 'img_digital', 'img_synclink'] and all(n[2]['opacity'] == '0' for n in hidden)


@pytest.mark.parametrize('change,message', [
    (lambda r: r[1].__setitem__(1, -300), 'Unexpected quick settings'),
    (lambda r: r[3][1][3].pop(), 'Unexpected quick settings controls'),
    (lambda r: r[3][1][3][0][1].__setitem__(2, 40), 'wifiswitch: unexpected quick settings control'),
    (lambda r: r[3][2][3][1][2].pop('slide_with_bar'), 'Unexpected brightness row'),
    (lambda r: r[3][0][3].pop(), 'Unexpected quick settings sysbar'),
    (lambda r: r[3][0][3][2][3].pop(), 'Unexpected quick settings sysbar widgets')])
def test_quick_settings_wants_stock(change, message):
    root = quick()
    change(root)
    with pytest.raises(ValueError, match=f'^{message}$'):
        m1plus_ipod.quick_settings(root)


def test_quick_settings_brightness_under_the_volume_panel(monkeypatch):
    """vol_paint's panel must cover the brightness row exactly."""
    monkeypatch.setitem(m1plus_ipod.M1, 'VOL_PANEL_Y', m1plus_ipod.M1['VOL_PANEL_Y'] + 1)
    with pytest.raises(ValueError, match='^The volume panel must cover the brightness row$'):
        m1plus_ipod.quick_settings(quick())


def home():
    """V2.1's home_page.bin: the gesture view of the card grid and the playing strip, then the serial-error label."""
    gesture = w('app_gesture', w('home_svview'), w('home_bottomview'), kind='gesture')
    return ['window', [0, 0, 320, 480], {'name': 'home_page'}, [gesture, w('label_snerr', kind='label', text='SN Error')]]


def test_home_page():
    """The art across the top, the main and Settings lists (every label V2.1's style and its text), the hidden Carousel
    and its arrows, and the serial-error label still last."""
    root = m1plus_ipod.home_page(home())
    ipod = m1plus_ipod.ipod
    art, main, sets, menu, left, right, snerr = root[3]
    assert art[1] == [0, 0, ipod.UI_W, m1plus_ipod.M1['HOME_ART_H']] and art[2]['name'] == 'img_homeart'
    for lst, rows in ((main, ipod.HOME_ROWS), (sets, ipod.HOME_SETS)):
        labels = [view[3][0] for view in lst[3][0][3]]
        assert [l[2]['text'] for l in labels] == [m1plus_ipod.HOME_TEXT[r] for r in rows]
        assert all(l[2]['style'] == m1plus_ipod.HOME_LABEL_STYLE for l in labels)
    assert main[2]['name'] == 'list_view_home' and sets[2]['name'] == 'list_view_homeset' and sets[2]['visible'] == 'false'
    card = m1plus_ipod.CARD
    assert menu[0] == 'slide_menu' and menu[1][1] * 2 + card == ipod.BOTTOM and menu[1][0] * 2 + menu[1][2] == ipod.UI_W
    assert names(menu[3]) == ['btn_' + r for r in ipod.HOME_ROWS]
    assert all(n[2]['visible'] == n[2]['sensitive'] == 'false' for n in (menu, left, right))
    assert (left[1][0], right[1][0] + right[1][2]) == (0, ipod.UI_W) and (left[2]['image'], right[2]['image']) == ('home_left', 'home_right')
    assert snerr == home()[3][1]


@pytest.mark.parametrize('change,message', [
    (lambda r: r[3].reverse(), 'Unexpected Home'), (lambda r: r[3][0].__setitem__(0, 'view'), 'Unexpected Home grid'),
    (lambda r: r[3][0][3].pop(), 'Unexpected Home grid'), (lambda r: r[3][1][2].update(text=''), 'Unexpected serial-error label')])
def test_home_page_wants_stock(change, message):
    root = home()
    change(root)
    with pytest.raises(ValueError, match=f'^{message}$'):
        m1plus_ipod.home_page(root)


def test_home_card():
    """A Carousel card: its art clickable, pressed showing the _down art, the caption under it."""
    art, label = m1plus_ipod.home_card('folder')[3]
    assert art[2]['clickable'] == 'true' and art[2]['style:pressed:bg_image'] == 'home_card_folder_down'
    assert art[1][0] * 2 + art[1][2] == m1plus_ipod.CARD and label[2]['text'] == 'Folder'


def playing():
    """V2.1's playing_page.bin: app_gesture > view_local (its widgets as NP_LOCAL) and view_dlna, 438 high."""
    M1 = m1plus_ipod.M1
    cover = w(m1plus_ipod.M1_VIEW_COVER, kind='image')
    lyrics = w('view_lyrics', w('view_lrc', w('scroll_lrc', kind='scroll_view', self_layout='default(x=0,y=0,w=100%,h=100%)'), at=[33, 26, 254, 228]),
               w('label_lyricmsg', kind='label', at=[0, 100, 320, 28]))
    slide = w('slide_view', w('view', cover), lyrics, w('view_info'), kind='slide_view', self_layout='default(x=0,y=0,w=100%,h=254)')
    dots = w('slide_indicator', kind='slide_indicator', **{'style:normal:fg_color': '#000', 'style:normal:selected_fg_color': '#fff'})
    column = w('slide_view_view', slide, dots, *(w(n, kind='label') for n in ('label_playtime', 'label_playlen', 'label_index')),
               w('btn_more', kind='button'), w('btn_fav', kind='button'))
    buttons = w('view_buttons', *(w(n, kind='button') for n in m1plus_ipod.NP_BUTTONS), at=[0, 372, 320, 66])
    local = w('view_local', column, w('img_hr', kind='image', at=[280, 10, 28, 18], visible='false'),
              w('scrlabel_title', kind='hscroll_label'), w('scrlabel_artist', kind='hscroll_label'),
              w('btn_return', kind='button', at=[0, 0, 80, 36]),
              w('slider_play', kind='slider', at=[M1['NP_BAR_X'], 342, M1['NP_BAR_W'], 30], **{'style:normal:icon': 'thumb'}),
              w('img_repeata', kind='image', at=[M1['NP_BAR_X'], 380, 8, 8]), w('img_repeatb', kind='image', at=[M1['NP_BAR_X'], 380, 8, 8]),
              buttons, at=[0, 0, 320, 438])
    gesture = w('app_gesture', local, w('view_dlna', at=[0, 0, 320, 438]), kind='gesture', at=[0, 0, 320, 438])
    return ['window', [0, 0, 320, 480], {'name': 'playing_page'}, [gesture]]


def test_playing_page():
    """The top row (back, position, HR badge, heart, More), the art slide with the title, artist and album, the dots, the
    bar between the times and the transport row, all where m1plus_offsets.inc places them."""
    M1, ipod = m1plus_ipod.M1, m1plus_ipod.ipod
    root = m1plus_ipod.playing_page(playing())
    gesture, = root[3]
    local, dlna = gesture[3]
    assert gesture[1] == local[1] == dlna[1] == [0, 0, ipod.UI_W, ipod.BOTTOM] and root[2]['style:normal:bg_color'] == '#000000'
    assert names(local[3]) == ['slide_view_view', 'label_ipod_pos', 'img_hr', 'btn_fav', 'btn_more', 'btn_return', 'slider_play',
                               'img_repeata', 'img_repeatb', 'label_playtime', 'label_ipod_remain', 'view_buttons']
    column, pos, badge, fav, more, back, slider, a, b, elapsed, remain, buttons = local[3]
    assert names(column[3]) == ['slide_view', 'slide_indicator', 'label_playlen', 'label_index']
    slide_h = M1['NP_DOTS_Y'] - M1['NP_SLIDE_Y']
    slide, dots, total, index = column[3]
    assert column[1] == [0, M1['NP_SLIDE_Y'], ipod.UI_W, slide_h + 10] and slide[1][3] == slide_h and dots[1] == [0, slide_h, ipod.UI_W, 10]
    cover, title, artist, album = slide[3][0][3]
    assert cover[2]['clickable'] == 'true' and cover[1] == [M1['NP_ART_X'], M1['NP_ART_Y'] - M1['NP_SLIDE_Y'], M1['NP_ART'], M1['NP_ART']]
    assert names([title, artist, album]) == ['scrlabel_title', 'scrlabel_artist', 'label_ipod_album'] and album[2]['text'] == ''
    assert title[2]['delay'] == title[2]['lull'] == str(ipod.inc('MARQUEE_HOLD_MS'))
    assert (dots[2]['style:normal:fg_color'], dots[2]['style:normal:selected_fg_color']) == ('#555555', '#eeeeee')
    top = M1['NP_TOP_H']
    assert back[1] == [0, 0, M1['NP_BACK_W'], top] and more[1][0] + more[1][2] == ipod.UI_W and fav[1][0] + fav[1][2] == more[1][0]
    assert badge[1][0] + badge[1][2] + 4 == fav[1][0] and pos[1][0] == M1['NP_BACK_W'] + 8 and pos[1][0] + pos[1][2] == badge[1][0]
    assert index[2]['visible'] == total[2]['visible'] == 'false'
    assert slider[1] == [M1['NP_BAR_X'], M1['NP_BAR_CY'] - M1['NP_BAR_TOUCH'] // 2, M1['NP_BAR_W'], M1['NP_BAR_TOUCH']]
    assert slider[2]['style'] == 's_ipod_progress' and slider[2]['style:normal:icon'] == ''
    assert a[1][1] == b[1][1] == M1['NP_AB_Y'] and elapsed[1][1] == remain[1][1] == M1['NP_TIMES_Y']
    assert elapsed[1][0] == M1['NP_BAR_X'] and remain[1][0] + remain[1][2] == ipod.UI_W - M1['NP_BAR_X']
    assert buttons[1][1] == M1['NP_BUTTONS_Y'] and names(buttons[3]) == m1plus_ipod.NP_BUTTONS
    view_lrc, msg = slide[3][1][3]
    assert view_lrc[1] == [0, 0, ipod.UI_W, slide_h - 20] and view_lrc[3][0][2]['children_layout'].startswith('list_view(x=0,y=')
    assert msg[1][1] == (slide_h - 28) // 2


def _child(root, *path):
    node = root
    for name in path:
        node = next(n for n in node[3] if n[2].get('name') == name)
    return node


@pytest.mark.parametrize('change,message', [
    (lambda r: r[2].update(name='x'), 'Unexpected Now Playing page'),
    (lambda r: r[3][0][3].reverse(), 'Unexpected Now Playing views'),
    (lambda r: _child(r, 'app_gesture', 'view_local')[3].pop(), 'Unexpected Now Playing view'),
    (lambda r: _child(r, 'app_gesture', 'view_local', 'slide_view_view')[3].pop(), 'Unexpected Now Playing column'),
    (lambda r: _child(r, 'app_gesture', 'view_local', 'view_buttons')[3].pop(), 'Unexpected transport row'),
    (lambda r: _child(r, 'app_gesture')[1].__setitem__(3, 440), 'Unexpected Now Playing size'),
    (lambda r: _child(r, 'app_gesture', 'view_local', 'slide_view_view', 'slide_view')[2].update(self_layout=''), 'Unexpected Now Playing slides'),
    (lambda r: _child(r, 'app_gesture', 'view_local', 'slider_play')[1].__setitem__(1, 340), 'Unexpected progress bar'),
    (lambda r: _child(r, 'app_gesture', 'view_local', 'img_hr')[2].update(visible='true'), 'Unexpected top row'),
    (lambda r: _child(r, 'app_gesture', 'view_local', 'img_repeatb')[1].__setitem__(0, 0), 'Unexpected img_repeatb')])
def test_playing_page_wants_stock(change, message):
    root = playing()
    change(root)
    with pytest.raises(ValueError, match=f'^{message}$'):
        m1plus_ipod.playing_page(root)


def test_playing_page_lyrics_fit(monkeypatch):
    """Three lyric slots must fit the page above its 20 px foot."""
    monkeypatch.setitem(m1plus_ipod.ipod.O, 'LYRIC_SLOT', (m1plus_ipod.M1['NP_DOTS_Y'] - m1plus_ipod.M1['NP_SLIDE_Y'] - 20) // 3 + 1)
    with pytest.raises(ValueError, match='^Three lyric lines must fit the page$'):
        m1plus_ipod.playing_page(playing())


def settings(rows=64):
    """A V2.1 settings page: the 50 px toolbar, then its list of rows a scroll view and V2.1's scroll bar, each 400 high."""
    lst = w('list_view', w('scroll_view', kind='scroll_view', at=[0, 0, 320, 400]), w('scroll_bar', kind='scroll_bar_m', at=[314, 0, 6, 400]),
            kind='list_view', at=[0, 50, 320, 400], default_item_height=str(rows))
    return ['window', [0, 0, 320, 480], {'name': 'audiosetting_page'}, [w(m1plus_ipod.NAVBAR, at=[0, 0, 320, 50]), lst]]


def test_settings_page():
    """The toolbar hidden and disabled, the list SET_ROWS rows of SET_ROW from SET_TOP, its scroll view and bar as tall."""
    ipod = m1plus_ipod.ipod
    root = m1plus_ipod.REWRITES['audiosetting_page.bin'](settings())
    nav, lst = root[3]
    assert nav[2]['visible'] == nav[2]['enable'] == 'false'
    g = ipod.SET0
    assert lst[1] == [0, g.set_top, 320, g.set_rows * g.set_row] and lst[2]['default_item_height'] == str(g.set_row)
    assert [c[1][3] for c in lst[3]] == [g.set_rows * g.set_row] * 2
    assert g.set_top + g.set_rows * g.set_row <= ipod.BOTTOM


@pytest.mark.parametrize('page', m1plus_ipod.M1_SETTINGS)
def test_m1_settings_pickers(page):
    """V2.1's own pickers (aesthetics 7b) take the settings rewrite: no toolbar, and the scroll bar (Update Local
    Music's is 372 high) as tall as the list."""
    g = m1plus_ipod.ipod.SET0
    root = settings()
    root[3][1][3][1][1][3] = 372
    nav, lst = m1plus_ipod.REWRITES[page](root)[3]
    assert nav[2]['visible'] == nav[2]['enable'] == 'false' and page in m1plus_ipod.AUDIT['m1_only']
    assert lst[2]['default_item_height'] == str(g.set_row) and [c[1][3] for c in lst[3]] == [g.set_rows * g.set_row] * 2


@pytest.mark.parametrize('change,message', [
    (lambda r: r[3][0][1].__setitem__(2, 300), 'audiosetting_page.bin: unexpected toolbar'),
    (lambda r: r[3][0][2].update(name=m1plus_ipod.NAVBAR + '_x'), 'audiosetting_page.bin: unexpected toolbar'),
    (lambda r: r[3][1][2].update(default_item_height='78'), 'audiosetting_page.bin: unexpected settings list'),
    (lambda r: r[3][1][3].pop(), 'audiosetting_page.bin: unexpected settings list')])
def test_settings_page_wants_stock(change, message):
    root = settings()
    change(root)
    with pytest.raises(ValueError, match=f'^{message}$'):
        m1plus_ipod.REWRITES['audiosetting_page.bin'](root)


def library():
    """A V2.1 library page: an empty toolbar V2.1 fills at run time, then a table of 60 px rows from y 50 to BOTTOM, its
    310 px client and its scroll bar."""
    tall = m1plus_ipod.ipod.BOTTOM - 50
    pitch = m1plus_ipod.M1['LIB_STOCK_PITCH']
    row = w('table_row', kind='table_row', at=[0, 0, 310, pitch], self_layout=f'default(w=100%,h={pitch})')
    table = w('table_view', w('table_client', row, kind='table_client', at=[0, 0, 310, tall]),
              w('scroll_bar', kind='scroll_bar_m', at=[310, 0, 10, tall]), kind='table_view', at=[0, 50, 320, tall])
    return ['window', [0, 0, 320, 480], {'name': 'allmusic_page'}, [w(m1plus_ipod.NAVBAR, at=[0, 0, 320, 50]), table]]


def test_library_page():
    """The toolbar hidden, the table from the top to BOTTOM, its client the screen's width, the rows at the iPod pitch."""
    ipod = m1plus_ipod.ipod
    root = m1plus_ipod.REWRITES['allmusic_page.bin'](library())
    nav, table = root[3]
    assert nav[2]['visible'] == nav[2]['enable'] == 'false'
    assert table[1] == [0, 0, 320, ipod.BOTTOM]
    client, bar = table[3]
    assert client[1] == [0, 0, ipod.UI_W, ipod.BOTTOM] and bar[1][3] == ipod.BOTTOM
    assert client[3][0][2]['self_layout'] == f'default(w=100%,h={ipod.PITCH})'


def test_library_page_folders_layout():
    """Folders' table places itself over its geometry, so its layout follows."""
    root = library()
    root[3][1][2]['self_layout'] = f'default(x=0,y=50,w=100%,h={m1plus_ipod.ipod.BOTTOM - 50})'
    table = m1plus_ipod.REWRITES['folder_page.bin'](root)[3][1]
    assert table[2]['self_layout'] == f'default(x=0,y=0,w=100%,h={m1plus_ipod.ipod.BOTTOM})'


@pytest.mark.parametrize('change,message', [
    (lambda r: r[3][0][3].append(w('btn')), 'allmusic_page.bin: unexpected toolbar'),
    (lambda r: r[3][1][1].__setitem__(3, 300), 'allmusic_page.bin: unexpected list'),
    (lambda r: r[3].append(w('list_view', kind='list_view')), 'allmusic_page.bin: unexpected list'),
    (lambda r: r[3][1][2].update(self_layout='default(x=0,y=50,w=100%,h=300)'), 'allmusic_page.bin: unexpected list layout'),
    (lambda r: r[3][1][3].append(w('x', kind='label')), 'allmusic_page.bin: unexpected list child')])
def test_library_page_wants_stock(change, message):
    root = library()
    change(root)
    with pytest.raises(ValueError, match=f'^{message}$'):
        m1plus_ipod.REWRITES['allmusic_page.bin'](root)


def test_every_rewrite_is_tested():
    """Each REWRITES entry's function has a synthetic tree here: the eight pages, the settings pages and the library."""
    tested = {m1plus_ipod.status_bar, m1plus_ipod.home_page, m1plus_ipod.playing_page, m1plus_ipod.bigcover_page,
              m1plus_ipod.volume_dialog, m1plus_ipod.quick_settings, m1plus_ipod.confirm_dialog, m1plus_ipod.msginfo_dialog}
    pages = set(m1plus_ipod.REWRITES)
    factories = pages - {p for p, f in m1plus_ipod.REWRITES.items() if f in tested}
    assert factories == {p for p in m1plus_ipod.AUDIT['navbar_only'] if p not in m1plus_ipod.SETTINGS_TOOLBAR_SWITCHES} | set(
        m1plus_ipod.M1_SETTINGS) | set(m1plus_ipod.LIBRARY_PAGES)
