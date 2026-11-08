"""tools/ipod.py with the M1 Plus's screen (docs/m1plus-ipod-ui.md Phase 2): a second copy of the module,
loaded with the M1's PROFILE, so sys.modules['ipod'] stays the Q2's that tools/m1plus.py imports from.

The profile is the screen from patch/m1plus_offsets.inc: UI_W, UI_H, STATUS_H, and GLASS_R (0, the square corners),
and the layout names a Phase 4 item has given V2.1's values (4.2: BATT_ROOM, as the 320 px bar fits it; 4.3: the
settings rows' SET_ROW, SET_TOP, SET_ROWS and V2.1's SET_STOCK_ROW; 4.4: the library rows' LIB_PITCH, LIB_BODY and
LIB_ART, which ipod.py's PITCH, BODY and ART take; 4.5: Home's HOME_ROW and its labels' HOME_DOT_X and HOME_LABEL_END).
Every other layout name keeps the Q2's value until its item.

Phase 3 adds the V2.1 patch around that copy: patch/m1plus_ipod.json (V1.32's pages mapped onto V2.1's, every
other section empty), and patch_asset and patch_code, which m1plus.build() runs on every build. A Phase 4 item adds
its page to REWRITES and its sites to the JSON; 4.1 adds the `styles` section, through patch_style."""
import functools
import importlib.util
import json
import re
import struct
from build import ROOT, check, fileoff, sha

M1 = {m[1]: int(m[2], 0) for m in re.finditer(r'^#define\s+(\w+)\s+(0x[0-9A-Fa-f]+|\d+)\b',
                                               (ROOT/'patch/m1plus_offsets.inc').read_text(), re.M)}
PROFILE = {name: M1[name] for name in ('UI_W', 'UI_H', 'STATUS_H', 'GLASS_R', 'BATT_ROOM', 'SET_ROW', 'SET_TOP', 'SET_ROWS',
                                       'SET_STOCK_ROW', 'LIB_PITCH', 'LIB_BODY', 'LIB_ART', 'HOME_ROW', 'HOME_DOT_X',
                                       'HOME_LABEL_END')}


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

# 4.2: V2.1's system_bar.bin is a system_bar of view_bar_left (img_playstate, img_volume, label_volume, img_digital), a
# digit_clock (bar_dclock), view_bar_right (img_btclass, img_synclink, img_wifi), and the battery as a progress bar
# (pgbar_battery) over its icon (img_battery). show_sysbar_face (0x544b48, each second) finds them by name and sets
# their images and text, never their geometry.
STATUS_BAR = 'system_bar.bin'
STATUS_NAMES = ['view_bar_left', 'bar_dclock', 'view_bar_right', 'pgbar_battery', 'img_battery']
STATUS_LEFT = ['img_playstate', 'img_volume', 'label_volume', 'img_digital']
STATUS_RIGHT = ['img_btclass', 'img_synclink', 'img_wifi']
# Shown on the iPod bar: the back chevron and the play state on the left; Bluetooth, Wi-Fi and the payload's battery
# (view_battery) on the right. The volume, the digital badge, the link badge and V2.1's own battery stay in the bar,
# still updated by V2.1, but never drawn.
STATUS_SHOWN = ['img_back', 'img_playstate', 'img_btclass', 'img_wifi', 'view_battery']
STATUS_HIDDEN = ['img_volume', 'label_volume', 'img_digital', 'img_synclink', 'pgbar_battery', 'img_battery']
BACK_W = M1['BAR_BACK_W']  # the chevron's image and tap width, the bar's height tall
CLOCK_W = 90  # V2.1's digit_clock width; "12:59 PM" is CLOCK_TEXT px at the bar's font


def status_bar(root):
    """V2.1's status bar as the iPod's: square-cornered margins, the play state, Bluetooth, Wi-Fi and the payload's
    battery slot, the clock centred, and a back chevron at the far left (shown by the payload when a page is open)."""
    check(root[0] == 'system_bar' and [n[2].get('name') for n in root[3]] == STATUS_NAMES, 'Unexpected status bar')
    left, clock, right, pgbar, battery = root[3]
    check([n[2].get('name') for n in left[3]] == STATUS_LEFT and [n[2].get('name') for n in right[3]] == STATUS_RIGHT,
          'Unexpected status bar widgets')
    gap, margin, height = ipod.inc('STATUS_GAP'), ipod.STATUS_MARGIN, ipod.STATUS_H
    root[2]['style:normal:bg_color'] = '#000000'
    # Clear, not black: AWTK draws the border over the bar's fill, and Light Mode flips black to paper.
    root[2].update({f'style:{s}:border_color': '#00000000' for s in ('normal', 'disable', 'focused')})
    named = {n[2]['name']: n for n in left[3] + right[3]}
    named['img_playstate'][1][2], named['img_wifi'][1][2], named['img_btclass'][1][2] = 12, 14, 42
    back = ['image', [0, 0, BACK_W, height], {'name': 'img_back', 'image': 'bar_back', 'draw_type': 'center',
                                              'visible': 'false'}, []]
    # The payload's battery (view_battery) is sized and painted at run time; it hides until the first sync.
    slot = ['view', [0, 0, ipod.BATT_H_W, 0], {'name': 'view_battery', 'visible': 'false'}, []]
    left[3] = [back, named['img_playstate']]
    right[3] = [named['img_btclass'], named['img_wifi'], slot]
    shown = [left, right]
    left[1], right[1] = [0, 0, ipod.UI_W // 2 - CLOCK_W // 2, height], [ipod.UI_W // 2 + CLOCK_W // 2, 0, ipod.UI_W // 2 - CLOCK_W // 2, height]
    left[2]['children_layout'] = f'default(r=1,c=0,x=0,s={gap})'
    right[2]['children_layout'] = f'default(r=1,c=0,a=right,xm={margin},s={gap})'
    # The clock: V2.1's own digit_clock, centred.
    clock[1] = [(ipod.UI_W - CLOCK_W) // 2, 0, CLOCK_W, 100]
    clock[2]['self_layout'] = f'default(x={(ipod.UI_W - CLOCK_W) // 2},y=0,w={CLOCK_W},h=100%)'
    # Room: the right group's ink, with every glyph, stays clear of the widest clock text; the left's play state too.
    room = int(ipod.UI_W - margin - (ipod.UI_W / 2 + ipod.CLOCK_TEXT / 2 + ipod.CLOCK_GAP))
    reach = ipod.BT_REACH + 2 * gap + 14 + max(ipod.BATT_PCT_W, ipod.BATT_H_W, ipod.inc('BATT_INSIDE_W') + ipod.inc('BATT_NUB_W'))
    check(ipod.BATT_ROOM == room and reach <= room, f'Status bar battery needs {reach}px of {room}px')
    check(BACK_W + gap + 12 <= ipod.UI_W // 2 - ipod.CLOCK_TEXT // 2 - ipod.CLOCK_GAP, 'Status bar left group meets the clock')
    # Widgets V2.1 shows each second but the iPod doesn't draw: at the bar's left, transparent (opacity 0, which AWTK
    # doesn't paint), not off-screen as the Q2's are. V2.1's face resizes and sets them each second, and on V2.1 an
    # invalidate left of the screen loses that frame's flush to the panel: the page painted with it stays in the back
    # buffer until something repaints it (docs/m1plus-progress.md section 63).
    moved = [named[k] for k in ('img_volume', 'label_volume', 'img_digital', 'img_synclink')]
    root[3] += moved
    for n in moved + [pgbar, battery]:
        n[1], n[2]['opacity'] = [0, 0, n[1][2], height], '0'
    return root


def back_chevron():
    """The chevron the bar's img_back draws: a slim white `<` in a BACK_W x STATUS_H canvas, rendered at 4x."""
    draw = ("scale 4,4 fill none stroke-width 2.2 stroke white stroke-linecap round stroke-linejoin round "
            "path 'M17,7 L9,15 L17,23'")
    return ipod.imagemagick('-size', f'{BACK_W * 4}x{ipod.STATUS_H * 4}', 'xc:none', '-draw', draw, '-filter', 'Lanczos',
                            '-resize', f'{BACK_W}x{ipod.STATUS_H}!', *ipod.PNG_OUT, data=b'')


def status_icon(name, data):
    """The audited V2.1 status image (hashed in `status_icons`) as the iPod's slim glyph of the same name."""
    ipod.STATUS_ICONS = AUDIT['status_icons']  # the copy checks V2.1's hashes, not the Q2's
    return ipod.status_icon(name, data)


# 4.3: V2.1's settings pages (navbar_only) lose their navigationbar_view as the Q2's lose view_navbar
# (ipod.settings_page): hidden and disabled, its return button left for back_of (patch/m1plus_nav_back.c), their
# lists holding SET_ROWS SET_ROW rows that ipod_list_layout maps (V2.1's are 64 high, memplay's 60). The Lock Screen
# page keeps its toolbar, which holds its on/off switch (image_switch), as the Q2's TOOLBAR_SWITCHES do. Date & Time
# and Power have no page toolbar: each slide of their slide_view has its own (navigationbar_view, numbered), and a
# slide's list stops at the slide's foot (the slide indicator under it). V2.1's scroll view and scroll bar have fixed
# heights (the Q2's scroll view follows its list, h=100%): they take the list's.
NAVBAR = 'navigationbar_view'
SETTINGS_TOOLBAR_SWITCHES = ('systemset/screensaver_page.bin',)
SETTINGS_SLIDES = ('systemset/datetime_page.bin', 'systemset/powermanager_page.bin')
SETTINGS_STOCK_ROWS = (ipod.SET_STOCK_ROW, 60)


def settings_page(path):
    """The rewrite of V2.1's settings page path: ipod.settings_page on the page, or on each of its slides."""
    def toolbar(node):
        nav = [n for n in node[3] if n[2].get('name', '').startswith(NAVBAR)]
        check(len(nav) == 1 and nav[0][0] == 'view' and nav[0][1] == [0, 0, ipod.UI_W, 50], f'{path}: unexpected toolbar')
        return nav[0]

    def rewrite(root):
        if path not in SETTINGS_SLIDES:
            nav = toolbar(root)
            check(nav[2]['name'] == NAVBAR, f'{path}: unexpected toolbar')
            ipod.settings_page(path, root, nav, SETTINGS_STOCK_ROWS)
        else:
            holder, = [n for n in root[3] if n[2].get('name') == 'slide_view_view']
            slides, = [n for n in holder[3] if n[0] == 'slide_view']
            for slide in slides[3]:
                ipod.settings_page(path, slide, toolbar(slide), SETTINGS_STOCK_ROWS, bottom=slide[1][3])
        for n in ipod.walk(root):
            if n[0] == 'list_view':
                check([c[0] for c in n[3]] == ['scroll_view', 'scroll_bar_m'], f'{path}: unexpected settings list')
                for c in n[3]:
                    c[1][3] = n[1][3]
        return root
    return rewrite


# 4.4: V2.1's library pages, through ipod.library_page with V2.1's row sizes. Their rows are built in code (the
# constructors patch_code edits); the pages hold the lists, an empty navigationbar_view (V2.1 fills it at run time:
# Return, the title, Search, Multi-select, Back to player) and the rows' 60 px template. The title bar is hidden and
# disabled, as the Q2's view_navbar is, its run-time return button still Previous's and the chevron's (back_of); the
# Playlists page keeps its own, as the Q2's does. Each list then reaches BOTTOM from the top, LIB_ROWS LIB_PITCH rows,
# and its scroll view, table client and scroll bar, which have fixed heights on V2.1, take its height; the table
# clients span the screen, as the Q2's do, the scroll bar over the rows' right edge.
LIBRARY_PAGES = ('allmusic_page.bin', 'album_page.bin', 'albuminfo_page.bin', 'localclass_page.bin', 'playlist_page.bin',
                 'folder_page.bin')
LIBRARY_STOCK = ipod.LIBRARY_STOCK | {'playlist': 'playlist_page.bin', 'list_y': (50,), 'pitch': M1['LIB_STOCK_PITCH'],
                                      'body': M1['LIB_STOCK_BODY'], 'client': 310, 'titles': (), 'art': ()}


def library_page(path):
    """The rewrite of V2.1's library page path."""
    def rewrite(root):
        nav = [n for n in root[3] if n[2].get('name') == NAVBAR]
        check(len(nav) == 1 and nav[0][1] == [0, 0, ipod.UI_W, 50] and not nav[0][3], f'{path}: unexpected toolbar')
        lists = [n for n in root[3] if n[0] in ('list_view', 'table_view')]
        check(len(lists) == 1 and lists[0][1][3] == ipod.BOTTOM - 50, f'{path}: unexpected list')
        ipod.library_page(path, root, nav[0], LIBRARY_STOCK)
        lst = lists[0]
        layout = lst[2].get('self_layout')
        if layout:  # Folders' table places itself (y=50, h=400), over its geometry
            check(layout == f'default(x=0,y=50,w=100%,h={ipod.BOTTOM - 50})', f'{path}: unexpected list layout')
            lst[2]['self_layout'] = f'default(x=0,y={lst[1][1]},w=100%,h={lst[1][3]})'
        for c in lst[3]:
            check(c[0] in ('scroll_view', 'table_client', 'scroll_bar_m'), f'{path}: unexpected list child')
            if c[1][3] == ipod.BOTTOM - 50:
                c[1][3] = lst[1][3]
            if c[0] == 'table_client' and c[1][2] == LIBRARY_STOCK['client'] and 'self_layout' not in c[2]:
                c[1][2] = ipod.UI_W
        for n in ipod.walk(root):
            layout = n[2].get('self_layout', '')
            if n[0] == 'table_row' and layout == f"default(w=100%,h={LIBRARY_STOCK['pitch']})":
                n[2]['self_layout'] = f'default(w=100%,h={ipod.PITCH})'
        return root
    return rewrite


# 4.5: V2.1's Home (home_page.bin) is a gesture view (app_gesture) holding the card grid (home_svview: home_sview, a
# slide_view home_page_init's builder 0x534064 fills, and its dots home_sindicator) and the playing strip
# (home_bottomview), then the serial-error label (label_snerr) its init shows on a bad serial. The iPod Home replaces
# the gesture view with the Q2's Home (ipod.ipod_home) in portrait: the art (img_homeart) across the top, HOME_ART_H
# high; the main list (list_view_home) and the Settings list (list_view_homeset, hidden) of HOME_ROW rows; and the
# carousel (slide_menu with img_left and img_right, hidden and taking no taps until chosen). The serial-error label
# stays last, over all of it. V2.1 names no Home widget but these (its init's lookups are audited in
# `home.safe_returns`), so nothing of V2.1's binds the new ones: the payload binds every row (coverflow_home), and every
# label carries its text.
HOME_PAGE = 'home_page.bin'
HOME_GRID = ['home_svview', 'home_bottomview']
HOME_TEXT = {'playing': 'Now Playing', 'localmusic': 'Library', 'coverflow': 'Coverflow', 'folder': 'Folder',
             'rockbox': 'Shortcut', 'stream': 'Streaming', 'settings': 'Settings', 'playset': 'Playback', 'sysset': 'System'}
HOME_LABEL_STYLE = 'srlabel_leftwhite20_style'  # patch/m1plus_offsets.inc STYLE_SCRLABEL_WHITE20L
CARD_LABEL_STYLE = 'label_centerwhite20_style'  # STYLE_LABEL_WHITE20C
# Carousel: V1.32's slide_menu card (a CARD square: its 190 px art 23 from the top, the caption at 232), centred
# on the screen and in the page's height, with the previous and next arrows at the screen's edges; each card's art is
# the V2.1 Home card art of its role, at 190 px (tools/m1plus.py home_cards).
CARD, CARD_ART, ARROW_W = M1['HOME_CARD'], 190, 48
HOME_CARD_ART = {'playing': 'mymusic', 'localmusic': 'playlist', 'coverflow': 'album', 'folder': 'folder',
                 'rockbox': 'fav', 'stream': 'hifimusic', 'settings': 'sysset'}


def home_list(name, rows, extra=None):
    """ipod.home_list with V2.1's label style and every label's text."""
    node = ipod.home_list(name, rows, extra)
    for view, row in zip(node[3][0][3], rows):
        label = view[3][0]
        check(label[0] == 'hscroll_label', f'{name}: unexpected Home row')
        label[2]['style'] = HOME_LABEL_STYLE
        label[2]['text'] = HOME_TEXT[row]
    return node


def home_card(row):
    """A Carousel card: its art, clickable as the lists' rows are, and its caption."""
    art = {'name': 'img_' + row, 'draw_type': 'center', 'clickable': 'true',
           **{f'style:{s}:bg_image': f'home_card_{row}' for s in ('normal', 'selected', 'disable', 'focused')},
           'style:pressed:bg_image': f'home_card_{row}_down'}
    label = {'self_layout': 'default(x=0,y=232,w=100%,h=28)', 'name': 'label_' + row, 'style': CARD_LABEL_STYLE,
             'text': HOME_TEXT[row]}
    return ['view', [0, 0, 0, 0], {'name': 'btn_' + row}, [['image', [(CARD - CARD_ART) // 2, 23, CARD_ART, CARD_ART], art, []],
                                                            ['label', [0, 232, 0, 28], label, []]]]


def home_page(root):
    """V2.1's Home as the iPod's, in portrait."""
    check([n[2].get('name') for n in root[3]] == ['app_gesture', 'label_snerr'], 'Unexpected Home')
    gesture, snerr = root[3]
    check(gesture[0] == 'gesture' and [n[2].get('name') for n in gesture[3]] == HOME_GRID, 'Unexpected Home grid')
    check(snerr[0] == 'label' and snerr[2].get('text') == 'SN Error', 'Unexpected serial-error label')
    menu_y, hidden = (ipod.BOTTOM - CARD) // 2, {'visible': 'false', 'sensitive': 'false'}
    menu = ['slide_menu', [ipod.UI_W // 2 - 750, menu_y, 1500, CARD],
            {'self_layout': f'default(x={ipod.UI_W // 2 - 750},y={menu_y},w=1500,h={CARD})', 'name': 'slide_menu',
             'min_scale': '1', 'value': '0', 'dirty_rect_tolerance': '4', 'style:normal:bg_color': '#00000000', **hidden},
            [home_card(row) for row in ipod.HOME_ROWS]]
    arrows = [['image', [x, menu_y, ARROW_W, CARD], {'name': name, 'image': name.replace('img_', 'home_'),
                                                    'draw_type': 'center', 'style:normal:y_offset': '-25',
                                                    'clickable': 'true', **hidden}, []]
              for name, x in (('img_left', 0), ('img_right', ipod.UI_W - ARROW_W))]
    art = ['image', [0, 0, ipod.UI_W, M1['HOME_ART_H']], {'name': 'img_homeart', 'draw_type': 'fill'}, []]
    root[3] = [art, home_list('home', ipod.HOME_ROWS), home_list('homeset', ipod.HOME_SETS, {'visible': 'false'}), menu,
               *arrows, snerr]
    return root


def home_arrow(name):
    """The carousel's previous or next control: a slim white chevron, ARROW_W x ARROW_W, rendered at 4x."""
    path = "'M30,10 L16,24 L30,38'" if name == 'home_left' else "'M18,10 L32,24 L18,38'"
    draw = f'scale 4,4 fill none stroke-width 3 stroke white stroke-linecap round stroke-linejoin round path {path}'
    return ipod.imagemagick('-size', f'{ARROW_W * 4}x{ARROW_W * 4}', 'xc:none', '-draw', draw, '-filter', 'Lanczos',
                            '-resize', f'{ARROW_W}x{ARROW_W}!', *ipod.PNG_OUT, data=b'')


# V2.1 page path -> function(root) that edits the decoded page in place. A Phase 4 item adds its pages here.
REWRITES = {STATUS_BAR: status_bar, HOME_PAGE: home_page} | {
    p: settings_page(p) for p in AUDIT['navbar_only'] if p not in SETTINGS_TOOLBAR_SWITCHES} | {
    p: library_page(p) for p in LIBRARY_PAGES}


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
    """The audited code edits (immediates, row layout calls, then the list_view layout slot) on data, V2.1's demo;
    returns the manifest's changes."""
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
    # 4.4: Folders' and an album's tracks' rebinds resize the row's label (by multi-select), as the Q2's folder rebind
    # does (0x522410): the width is the row layouter's (compact_row_layout).
    for address in (0x532f6c, 0x527918):
        word(address, 0x0320f809, 0, 'library rebind retains the width owned by its row layouter')
    # 4.3: the settings rows, through V2.1's list_view layouter's layout slot (data, vtable 0x9047a0 + 8).
    word(M1['LIST_VIEW_LAYOUT_SLOT'], M1['LIST_VIEW_LAYOUT'], symbols['ipod_list_layout'],
         'settings lists stack SET_ROW rows and map their children')
    # 4.5: Home. V2.1's initializer and refresh stay, each returning where a widget the iPod Home removes is gone (pinned);
    # the playing strip's tap is not bound; the boot resume stays on Home, as the Q2's (ipod.patch_code).
    home = AUDIT['home']
    for address, instruction, purpose in home['safe_returns']:
        pin(data, int(address, 16), int(instruction, 16), purpose)
    for event_at, event, address, instruction, purpose in home['unbound']:
        pin(data, int(event_at, 16), int(event, 16), 'the pointer-up event id')
        word(int(address, 16), int(instruction, 16), 0, purpose)
    address, instruction, purpose = home['boot_resume']
    word(int(address, 16), int(instruction, 16), ipod.jal(symbols['ringnav_boot']), purpose)
    return changes


def pin(data, address, instruction, purpose):
    """A V2.1 word the iPod code relies on as it is."""
    check(struct.unpack_from('<I', data, fileoff(data, address))[0] == instruction, f'{address:#x}: unexpected instruction ({purpose})')
