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
import copy
import functools
import importlib.util
import json
import re
import struct
from typing import Any, cast
from build import ROOT, check, need, fileoff, sha

M1 = {m[1]: int(m[2], 0) for m in re.finditer(r'^#define\s+(\w+)\s+(0x[0-9A-Fa-f]+|\d+)\b',
                                               (ROOT/'patch/m1plus_offsets.inc').read_text(), re.M)}
PROFILE = {name: M1[name] for name in ('UI_W', 'UI_H', 'STATUS_H', 'GLASS_R', 'BATT_ROOM', 'SET_ROW', 'SET_TOP', 'SET_ROWS',
                                       'SET_STOCK_ROW', 'LIB_PITCH', 'LIB_BODY', 'LIB_ART', 'HOME_ROW', 'HOME_DOT_X',
                                       'HOME_LABEL_END', 'CONFIRM_TOP')}


def load(profile=PROFILE):
    """A fresh tools/ipod.py, its constants computed for profile."""
    spec = need(importlib.util.spec_from_file_location('m1plus_ipod_screen', ROOT/'tools/ipod.py'), 'Missing M1 screen module')
    module = cast(Any, importlib.util.module_from_spec(spec))  # PROFILE is injected before the module executes
    module.PROFILE = profile
    need(spec.loader, 'Missing M1 screen loader').exec_module(module)
    return module


ipod = load()

M1_STR = {m[1]: m[2] for m in re.finditer(r'^#define\s+(\w+)\s+"([^"]*)"', (ROOT/'patch/m1plus_offsets.inc').read_text(), re.M)}
M1_VIEW_COVER, M1_VIEW_BIGCOVER, M1_VIEW_FAV, M1_VIEW_MORE = (M1_STR[n] for n in ('VIEW_COVER', 'VIEW_BIGCOVER', 'VIEW_FAV', 'VIEW_MORE'))

AUDIT = json.loads((ROOT/'patch/m1plus_ipod.json').read_text())
UI_ASSETS = AUDIT['assets'] | AUDIT['navbar_only'] | AUDIT['slide_only'] | {p: r['sha256'] for p, r in AUDIT['m1_only'].items()}

# 4.2: V2.1's system_bar.bin is a system_bar of view_bar_left (img_playstate, img_volume, label_volume, img_digital), a
# digit_clock (bar_dclock), view_bar_right (img_btclass, img_synclink, img_wifi), and the battery as a progress bar
# (pgbar_battery) over its icon (img_battery). show_sysbar_face (0x544b48, each second) finds them by name and sets
# their images and text, never their geometry.
STATUS_BAR = 'system_bar.bin'
STATUS_NAMES = ['view_bar_left', 'bar_dclock', 'view_bar_right', 'pgbar_battery', 'img_battery']
STATUS_LEFT = ['img_playstate', 'img_volume', 'label_volume', 'img_digital']
STATUS_RIGHT = ['img_btclass', 'img_synclink', 'img_wifi']
# Shown on the iPod bar: the back chevron on the left; Bluetooth, the play state, Wi-Fi and the payload's battery
# (view_battery) on the right. The volume, the digital badge, the link badge and V2.1's own battery stay in the bar,
# still updated by V2.1, but never drawn. The play state sits right of Bluetooth, whose 42 px canvas has its ink at the
# right edge: left of it the icon would stand BT_REACH's 32 px hole away and in the clock, and it would move as a codec
# badge fades. V2.1 finds them all by recursive lookups and never names the groups.
STATUS_SHOWN = ['img_back', 'img_btclass', 'img_playstate', 'img_wifi', 'view_battery']
STATUS_HIDDEN = ['img_volume', 'label_volume', 'img_digital', 'img_synclink', 'pgbar_battery', 'img_battery']
BACK_W = M1['BAR_BACK_W']  # the chevron's image and tap width, the bar's height tall
CLOCK_W = 90  # V2.1's digit_clock width; "12:59 PM" is CLOCK_TEXT px at the bar's font


def status_bar(root):
    """V2.1's status bar as the iPod's: square-cornered margins, Bluetooth, the play state, Wi-Fi and the payload's
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
    left[3] = [back]
    right[3] = [named['img_btclass'], named['img_playstate'], named['img_wifi'], slot]
    shown = [left, right]
    left[1], right[1] = [0, 0, ipod.UI_W // 2 - CLOCK_W // 2, height], [ipod.UI_W // 2 + CLOCK_W // 2, 0, ipod.UI_W // 2 - CLOCK_W // 2, height]
    left[2]['children_layout'] = f'default(r=1,c=0,x=0,s={gap})'
    right[2]['children_layout'] = f'default(r=1,c=0,a=right,xm={margin},s={gap})'
    # The clock: V2.1's own digit_clock, centred.
    clock[1] = [(ipod.UI_W - CLOCK_W) // 2, 0, CLOCK_W, 100]
    clock[2]['self_layout'] = f'default(x={(ipod.UI_W - CLOCK_W) // 2},y=0,w={CLOCK_W},h=100%)'
    # Room: the right group's ink, with every glyph, stays clear of the widest clock text; the left's chevron too.
    room = int(ipod.UI_W - margin - (ipod.UI_W / 2 + ipod.CLOCK_TEXT / 2 + ipod.CLOCK_GAP))
    reach = ipod.BT_REACH + 3 * gap + 12 + 14 + max(ipod.BATT_PCT_W, ipod.BATT_H_W, ipod.inc('BATT_INSIDE_W') + ipod.inc('BATT_NUB_W'))
    check(ipod.BATT_ROOM == room and reach <= room, f'Status bar battery needs {reach}px of {room}px')
    check(BACK_W <= ipod.UI_W // 2 - ipod.CLOCK_TEXT // 2 - ipod.CLOCK_GAP, 'Status bar left group meets the clock')
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


# The play state shows what a tap on it does, as the big transport button: pause while playing, play while paused.
# V2.1's two faces (show_sysbar_face, dropdown_showface) and the payload's bar_state_sync pick bar_play while playing,
# and no UI file names either image, so each ships the other's glyph.
STATUS_DRAWN = {'bar_play.png': 'bar_pause.png', 'bar_pause.png': 'bar_play.png'}


def status_icon(name, data):
    """The audited V2.1 status image (hashed in `status_icons`) as the iPod's slim glyph, of the same name but for
    STATUS_DRAWN."""
    drawn = STATUS_DRAWN.get(name, name)
    ipod.STATUS_ICONS = {**AUDIT['status_icons'], drawn: AUDIT['status_icons'][name]}  # the copy checks V2.1's hashes, not the Q2's
    return ipod.status_icon(drawn, data)


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
# the V2.1 Home card art of its role, at 190 px (tools/m1plus.py home_cards), but the Shortcut's: its target is a
# setting (Controls: Shortcut), so its card has art of its own (home_card_shortcut) and the caption names the target.
CARD, CARD_ART, ARROW_W = M1['HOME_CARD'], 190, 48
HOME_CARD_ART = {'playing': 'mymusic', 'localmusic': 'playlist', 'coverflow': 'album', 'folder': 'folder',
                 'stream': 'hifimusic', 'settings': 'sysset'}


def home_list(name, rows, extra=None):
    """ipod.home_list with V2.1's label style and every label's text."""
    node = ipod.home_list(name, rows, ipod.SET0, extra)
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


def home_card_shortcut(down=False):
    """The Carousel's Shortcut card art, CARD_ART square, rendered at 4x: the Controls page's Shortcut row icon
    (V2.1's pset_covermode, 40 px) as a Home card, an accent-blue disc with a white box and the arrow out of its corner.
    Pressed (down), at half brightness, as V2.1's *_down card art."""
    box = "'M52,100 L52,64 Q52,52 64,52 L126,52 Q138,52 138,64 L138,126 Q138,138 126,138 L90,138'"
    corner = "'M56,116 L70,116 Q74,116 74,120 L74,134 Q74,138 70,138 L56,138 Q52,138 52,134 L52,120 Q52,116 56,116 Z'"
    arrow = "'M88,102 L118,72 M96,72 L118,72 L118,94'"
    half = CARD_ART / 2
    draw = ['-fill', '#5B7CF9', '-draw', f'scale 4,4 circle {half},{half} {half},0.5', '-fill', 'none', '-stroke', 'white',
            '-strokewidth', '10', '-draw',
            f'scale 4,4 stroke-linecap round stroke-linejoin round path {box} path {corner} path {arrow}']
    shade = ['-channel', 'RGB', '-evaluate', 'multiply', '0.5', '+channel'] if down else []
    return ipod.imagemagick('-size', f'{CARD_ART * 4}x{CARD_ART * 4}', 'xc:none', *draw, '-filter', 'Lanczos',
                            '-resize', f'{CARD_ART}x{CARD_ART}!', *shade, *ipod.PNG_OUT, data=b'')


# 4.6: V2.1's Now Playing is app_gesture > view_local + view_dlna, where the Q2's is flat. The iPod page keeps V2.1's tree
# and its transport row (view_buttons, unchanged inside): the top row (btn_return, the back; the position; the HR badge,
# the heart and More), the art slide holding the art, title, artist and album, the dots, the bar and the times. The gesture
# and its views span the window, so the band vol_paint draws over the bar and the times is in the window's coordinates:
# both are view_local's children. V2.1's lookups of all of them are recursive (`playing.recursive_lookups`). The bar keeps
# V2.1's x and width, which getx_by_playtime's A-B dots assume, as they assume the row under the bar
# (`playing.ab_dots`). label_index and label_playlen stay, hidden: V2.1 still writes them. view_dlna stays as V2.1 has it.
PLAYING_PAGE = 'playing_page.bin'
NP_LOCAL = ['slide_view_view', 'img_hr', 'scrlabel_title', 'scrlabel_artist', 'btn_return', 'slider_play', 'img_repeata',
            'img_repeatb', 'view_buttons']
NP_COLUMN = ['slide_view', 'slide_indicator', 'label_playtime', 'label_playlen', 'label_index', 'btn_more', 'btn_fav']
NP_BUTTONS = ['btn_playmode', 'btn_prev', 'btn_play', 'image_wait', 'btn_next', 'btn_queue']
TEXT_STATES = ('normal', 'disable', 'focused')


def np_text(node, px, color, hold=False):
    """A Now Playing label's size and colour in every state a label styles, left-aligned unless it is a time."""
    node[2].update({f'style:{s}:font_size': str(px) for s in TEXT_STATES})
    node[2].update({f'style:{s}:text_color': color for s in TEXT_STATES})
    if hold:
        # V2.1's lull only pauses between loops; delay holds a new song's start too, as the album's marquee
        node[2].update({f'style:{s}:text_align_h': 'left' for s in TEXT_STATES})
        node[2].update(delay=str(ipod.inc('MARQUEE_HOLD_MS')), lull=str(ipod.inc('MARQUEE_HOLD_MS')))


def np_tree(root):
    """V2.1's exact Now Playing, checked: its named widgets, and view_local's and the column's own children."""
    check(root[2].get('name') == 'playing_page' and [n[2].get('name') for n in root[3]] == ['app_gesture'],
          'Unexpected Now Playing page')
    gesture, = root[3]
    check([n[2].get('name') for n in gesture[3]] == ['view_local', 'view_dlna'], 'Unexpected Now Playing views')
    local = gesture[3][0]
    check([n[2].get('name') for n in local[3]] == NP_LOCAL, 'Unexpected Now Playing view')
    named = {n[2].get('name'): n for n in ipod.walk(local)}
    check([n[2].get('name') for n in named['slide_view_view'][3]] == NP_COLUMN, 'Unexpected Now Playing column')
    check([n[2].get('name') for n in named['view_buttons'][3]] == NP_BUTTONS, 'Unexpected transport row')
    check([n[2].get('name') for n in named['slide_view'][3]] == ['view', 'view_lyrics', 'view_info'], 'Unexpected Now Playing pages')
    return gesture, local, named


def np_bar(slider, cy, touch):
    """The progress bar, through ipod.np_slider, in a touch-high slider centred on row cy, at V2.1's x and width."""
    check(slider[1] == [12, 342, 296, 30] and slider[1][::2] == [M1['NP_BAR_X'], M1['NP_BAR_W']], 'Unexpected progress bar')
    ipod.np_slider(slider, M1['NP_BAR_X'], cy, M1['NP_BAR_W'], ipod.inc('NP_BAR_MINIMAL'))
    slider[1] = [M1['NP_BAR_X'], cy - touch // 2, M1['NP_BAR_W'], touch]
    # V2.1 draws a style it doesn't know as the widget's default, whose thumb is the rounded_* icon: none, in every state.
    slider[2].update({f'style:{state}:icon': '' for state in ('normal', 'pressed', 'over', 'disable', 'focused')})


def playing_page(root):
    """V2.1's Now Playing as the iPod's, keeping its transport row."""
    gesture, local, named = np_tree(root)
    view_dlna = gesture[3][1]
    width, height = ipod.UI_W, ipod.BOTTOM
    check(gesture[1] == [0, 0, width, 438] and local[1] == view_dlna[1] == [0, 0, width, 438], 'Unexpected Now Playing size')
    gesture[1], local[1], view_dlna[1] = [0, 0, width, height], [0, 0, width, height], [0, 0, width, height]
    gesture[2]['self_layout'] = f'default(x=0,y=0,w={width},h={height})'
    root[2]['style:normal:bg_color'] = '#000000'  # paint_cover's corners are the page's black

    column, slide = named['slide_view_view'], named['slide_view']
    art_page, lyrics_page, info_page = slide[3]
    slide_y, slide_h = M1['NP_SLIDE_Y'], M1['NP_DOTS_Y'] - M1['NP_SLIDE_Y']
    column[1] = [0, slide_y, width, slide_h + 10]
    check(slide[2]['self_layout'] == 'default(x=0,y=0,w=100%,h=254)', 'Unexpected Now Playing slides')
    slide[1][3] = slide_h
    slide[2]['self_layout'] = f'default(x=0,y=0,w=100%,h={slide_h})'

    # The art slide: the art, then the title, artist and album under it.
    cover, = art_page[3]
    check(cover[2]['name'] == M1_VIEW_COVER, 'Unexpected Now Playing art')
    cover[1] = [M1['NP_ART_X'], M1['NP_ART_Y'] - slide_y, M1['NP_ART'], M1['NP_ART']]
    cover[2]['clickable'] = 'true'  # its tap opens the big cover (navigation.c np_art_click)
    title, artist = named['scrlabel_title'], named['scrlabel_artist']
    album = copy.deepcopy(artist)
    album[2].update(name='label_ipod_album', text='')
    title[1] = [M1['NP_TEXT_X'], M1['NP_TITLE_Y'] - slide_y, M1['NP_TEXT_W'], 28]
    artist[1] = [M1['NP_TEXT_X'], M1['NP_ARTIST_Y'] - slide_y, M1['NP_TEXT_W'], 22]
    album[1] = [M1['NP_TEXT_X'], M1['NP_ALBUM_Y'] - slide_y, M1['NP_TEXT_W'], 22]
    np_text(title, ipod.NP_TITLE_PX, '#FFFFFF', hold=True)
    np_text(artist, ipod.NP_META_PX, f'#{ipod.inc("NP_ARTIST_RGB"):06X}', hold=True)
    np_text(album, ipod.NP_META_PX, f'#{ipod.inc("NP_ALBUM_RGB"):06X}', hold=True)
    art_page[3] += [title, artist, album]

    # The lyrics page is the payload's (patch/lyrics.c): its rows span the page and start a slot down, ending 20 px above
    # the page's foot; "No lyrics" stays in its middle. The info page keeps V2.1's rows.
    view_lrc, msg = named['view_lrc'], named['label_lyricmsg']
    lrc = named['scroll_lrc']
    check(view_lrc[1] == [33, 26, 254, 228] and lrc[2].get('self_layout') == 'default(x=0,y=0,w=100%,h=100%)' and
          'children_layout' not in lrc[2] and msg[1] == [0, 100, width, 28], 'Unexpected lyrics page')
    check(3 * ipod.inc('LYRIC_SLOT') <= slide_h - 20, 'Three lyric lines must fit the page')
    view_lrc[1] = [0, 0, width, slide_h - 20]
    lrc[2]['children_layout'] = f'list_view(x=0,y={ipod.inc("LYRIC_SLOT")},s=0)'
    msg[1][1] = (slide_h - 28) // 2

    dots = named['slide_indicator']
    for key in dots[2]:
        if key.endswith(':selected_fg_color'): dots[2][key] = '#eeeeee'
        elif key.endswith(':fg_color'): dots[2][key] = '#555555'
    dots[1] = [0, slide_h, width, 10]
    # Without an anchor, the indicator centres its dots as the slide_view stands, mid-swipe too (tools/ipod.py).
    dots[2].update(self_layout=f'default(x=0,y={slide_h},w=100%,h=10)', anchor_x=f'{width // 2}px', anchor_y='0px')

    # The top row: the back, the position, the HR badge, then the heart and More at its right.
    top, back_w, icon_w = M1['NP_TOP_H'], M1['NP_BACK_W'], M1['NP_ICON_W']
    fav, more, index = named[M1_VIEW_FAV], named[M1_VIEW_MORE], named['label_index']
    back, badge = named['btn_return'], named['img_hr']
    check(back[1] == [0, 0, 80, 36] and badge[1] == [280, 10, 28, 18] and badge[2].get('visible') == 'false', 'Unexpected top row')
    back[1] = [0, 0, back_w, top]
    more[1], fav[1] = [width - icon_w, 0, icon_w, top], [width - 2 * icon_w, 0, icon_w, top]
    badge[1] = [width - 2 * icon_w - badge[1][2] - 4, (top - badge[1][3]) // 2, *badge[1][2:]]
    pos = copy.deepcopy(index)
    pos[1] = [back_w + 8, 0, badge[1][0] - back_w - 8, top]
    pos[2].update(name='label_ipod_pos', text='')
    pos[2].update({f'style:{s}:text_align_h': 'left' for s in TEXT_STATES})
    np_text(pos, 16, ipod.NP_GREY)
    index[2]['visible'] = 'false'

    # The bar and the times, each view_local's child; the A-B dots' row stays V2.1's, under the bar.
    slider, elapsed, total = named['slider_play'], named['label_playtime'], named['label_playlen']
    np_bar(slider, M1['NP_BAR_CY'], M1['NP_BAR_TOUCH'])
    remain = copy.deepcopy(total)
    remain[2].update(name='label_ipod_remain', text='')
    total[2]['visible'] = 'false'
    times_y, time_w = M1['NP_TIMES_Y'], 80
    elapsed[1] = [M1['NP_BAR_X'], times_y, time_w, 16]
    remain[1] = [width - M1['NP_BAR_X'] - time_w, times_y, time_w, 16]
    for n in (elapsed, remain):
        np_text(n, ipod.inc('NP_TIMES_PX'), ipod.NP_GREY)
    for name in ('img_repeata', 'img_repeatb'):
        check(named[name][1][0] == M1['NP_BAR_X'], f'Unexpected {name}')
        named[name][1][1] = M1['NP_AB_Y']
    buttons = named['view_buttons']
    check(buttons[1] == [0, 372, width, 66], 'Unexpected transport row')
    buttons[1][1] = M1['NP_BUTTONS_Y']

    column[3] = [slide, dots, total, index]
    local[3] = [column, pos, badge, fav, more, back, slider, named['img_repeata'], named['img_repeatb'], elapsed, remain, buttons]
    return root


# Display's Centred Now Playing (IPOD NPCENTRED) opens V2.1's own page, as PLAYING_STOCK (navigation.c ringnav_ui_load), named
# playing_page too, as the Q2's opens its stock one. It keeps V2.1's layout and transport, with the iPod's bar (the accent and
# Theme), the marquee holds, the page's black under the art's corners, and lyrics across their column. Its back is V2.1's
# top-left btn_return, as on the iPod page, with no chevron.
PLAYING_STOCK = 'playing_page_stock.bin'
NP_STOCK_BAR_CY = 342 + 30 // 2


def playing_stock(data):
    """V2.1's Now Playing with the light fixes, for Centred Now Playing."""
    check(sha(data) == UI_ASSETS[PLAYING_PAGE], f'{PLAYING_PAGE}: unaudited UI asset')
    root = ipod.decode(data)
    _, _, named = np_tree(root)
    root[2]['style:normal:bg_color'] = '#000000'
    named[M1_VIEW_COVER][2]['clickable'] = 'true'  # its tap opens the big cover (navigation.c np_art_click)
    for name in ('scrlabel_title', 'scrlabel_artist'):
        named[name][2].update(delay=str(ipod.inc('MARQUEE_HOLD_MS')), lull=str(ipod.inc('MARQUEE_HOLD_MS')))
    np_bar(named['slider_play'], NP_STOCK_BAR_CY, 30)
    view, msg = named['view_lrc'], named['label_lyricmsg']
    check(view[1] == [33, 26, 254, 228] and msg[1] == [0, 100, ipod.UI_W, 28] and 'self_layout' not in msg[2], 'Unexpected lyrics page')
    view[2]['self_layout'] = 'default(x=0,y=0,w=100%,h=-20)'
    msg[2]['self_layout'] = 'default(x=0,y=100,w=100%,h=28)'
    return ipod.encode(root)


# The volume dialog: V2.1's 320x42 strip over the status bar becomes the payload's drawing (navigation.c vol_paint), as the
# Q2's does: the dialog full screen and clear, the strip's children hidden, the band over Now Playing's bar and times, the
# panel elsewhere. V2.1 shows the strip's img_vol each time (0x47d78c), so it stays, transparent. The knob's and keys'
# opener passes context 1, the strip (on_wm_keyup_fun); a tap on the status bar passes 2 (on_wm_tsup_fun), and a tap on the
# strip's top 30 px switches to 2 (on_volume_tsup_fun): view_page2, V2.1's full VOLUME page, which stays as V2.1 has it, under
# the status bar, and vol_paint leaves alone. Any other tap on the strip closes it, now anywhere on the screen. The init's
# move is to 0,0 (`playing.volume_init`).
VOLUME = 'dialog/volume_dialog.bin'


def volume_dialog(root):
    """V2.1's volume dialog, clear and full screen, for vol_paint."""
    check(root[2].get('name') == 'volume_dialog' and root[2].get('highlight') == 'default(alpha=0)' and root[1] == [0, 0, ipod.UI_W, 42],
          'Unexpected volume dialog')
    check([n[2].get('name') for n in root[3]] == ['view_page1', 'view_page2'], 'Unexpected volume pages')
    strip, page = root[3]
    check([n[2].get('name') for n in strip[3]] == ['img_vol', M1_STR['VIEW_VOL'], 'label_vol'] and
          page[2].get('self_layout') == f'default(x=0,y={ipod.STATUS_H},w=100%,h={ipod.BOTTOM})', 'Unexpected volume strip')
    del root[2]['highlight']
    root[1] = [0, 0, ipod.UI_W, ipod.UI_H]
    for state in TEXT_STATES:
        for node in (root, strip):
            node[2][f'style:{state}:bg_color'] = '#00000000'
        root[2][f'style:{state}:border_color'] = '#00000000'
    strip[2]['self_layout'] = 'default(x=0,y=0,w=100%,h=100%)'
    icon, bar, label = strip[3]
    icon[2]['opacity'] = '0'
    bar[2]['visible'] = label[2]['visible'] = 'false'
    return root


# The big cover (a tap on Now Playing's art or Enlarged Art's countdown opens it, any tap closes it): V2.1's page, as the
# Q2's: full screen, its art a centred square, a shade with the title on its foot. bigcover_page_init (0x529a24) binds the
# window's tap and fills the labels by name; each time, its refresh (0x52952c) sets the artist visible, so the artist stays,
# transparent. The square glass gives the screen's width: bc_fit sizes the box to the cover's shape on the first paint.
BIGCOVER = 'bigcover_page.bin'
BC_ART = ipod.UI_W
BC_SHADE_H = 50


def bigcover_page(root):
    """V2.1's big cover as the iPod's."""
    check(root[2].get('name') == 'bigcover_page' and 'fullscreen' not in root[2] and
          [n[2].get('name') for n in root[3]] == [M1_VIEW_BIGCOVER, 'scrlabel_title', 'scrlabel_artist'], 'Unexpected big cover')
    art, title, artist = root[3]
    check(art[1] == [0, 0, BC_ART, BC_ART] and art[2].get('draw_type') == 'scale_auto' and art[2].get('image') == M1_STR['ICON_BIGCOVER'] and
          title[1] == [0, 340, BC_ART, 22], 'Unexpected big cover layout')
    root[2]['fullscreen'] = 'true'
    root[2].update({f'style:{s}:bg_color': '#000000' for s in TEXT_STATES})
    y = (ipod.UI_H - BC_ART) // 2
    foot = y + BC_ART - BC_SHADE_H
    art[1] = [0, y, BC_ART, BC_ART]
    art[2]['self_layout'] = f'default(x=0,y={y},w={BC_ART},h={BC_ART})'
    shade = ['view', [0, foot, BC_ART, BC_SHADE_H], {'name': 'view_shade', 'style:normal:bg_color': '#00000082'}, []]
    pad = ipod.inc('BC_TITLE_PAD')
    title[1] = [pad, foot + (BC_SHADE_H - title[1][3]) // 2, BC_ART - 2 * pad, title[1][3]]
    artist[2]['opacity'] = '0'
    root[3] = [art, shade, title, artist]
    return root


# 4.7: Quick Settings is V2.1's pull-down, dialog/dropdown_dialog (QUICK_NAME): a sysbar of the bar's widgets, which
# dropdown_showface fills by name each second and never moves; eight 50 px switches over their labels (view_switchs),
# each bound by name in dialog_dropdown_dialog_init; and the brightness row (view_backlight). The Q2's grid
# (ipod.quick_settings) on the M1's 320 px: four 80 px columns, V2.1's own 50 px art, 16 px labels under each icon, and
# a plain slider exactly under the volume panel (vol_paint), as the Q2's.
QUICK = 'dialog/dropdown_dialog.bin'
QS_ICONS = ['wifiswitch', 'btswitch', 'keylockswitch', 'gainswitch', 'usbmode', 'outputswitch', 'playset', 'sysset']
QS_LABELS = ['wifi', 'bt', 'lock', 'gain', 'usbmode', 'outputway', 'playset', 'sysset']
QS_TOP, QS_ICON, QS_LABEL_GAP, QS_LABEL_H, QS_ROW_GAP = 40, 50, 6, 40, ipod.QS_ROW_GAP
QS_COLUMN = ipod.UI_W // 4
QS_LABEL_W = QS_COLUMN - 4
QS_PITCH = QS_ICON + QS_LABEL_GAP + QS_LABEL_H + QS_ROW_GAP
QS_SUN = 20  # V2.1's drop_lighticon art
QS_SYSBAR = ['view_bar_left', 'bar_dclock', 'view_bar_right', 'pgbar_battery', 'img_battery']


def quick_settings(root):
    """V2.1's pull-down as the iPod's Quick Settings."""
    check(root[2].get('name') == 'dropdown_dialog' and root[1] == [0, -340, ipod.UI_W, 340] and
          [n[2].get('name') for n in root[3]] == ['view_sysbar', 'view_switchs', 'view_backlight'], 'Unexpected quick settings')
    sysbar, menu, light = root[3]
    named = {n[2]['name']: n for n in menu[3]}
    check(sorted(named) == sorted([f'img_{k}' for k in QS_ICONS] + [f'label_{v}' for v in QS_LABELS]),
          'Unexpected quick settings controls')
    for i, (icon, label) in enumerate(zip(QS_ICONS, QS_LABELS)):
        image, text = named['img_' + icon], named['label_' + label]
        check(image[1][2:] == [QS_ICON, QS_ICON] and image[1][1] == (14, 114)[i // 4] and
              text[2].get('style:normal:font_size') == '18', f'{icon}: unexpected quick settings control')
        x, y = i % 4 * QS_COLUMN, i // 4 * QS_PITCH
        image[1] = [x + (QS_COLUMN - QS_ICON) // 2, y, QS_ICON, QS_ICON]
        text[1] = [x + (QS_COLUMN - QS_LABEL_W) // 2, y + QS_ICON + QS_LABEL_GAP, QS_LABEL_W, QS_LABEL_H]
        for state in TEXT_STATES:
            text[2].update({f'style:{state}:font_size': '16', f'style:{state}:text_align_v': 'top',
                            f'style:{state}:text_align_h': 'center'})
    menu[1] = [0, QS_TOP, ipod.UI_W, 2 * QS_PITCH - QS_ROW_GAP]
    slider, dim, bright = (next(n for n in light[3] if n[2]['name'] == k) for k in ('slider_backlight', 'image0', 'image1'))
    check(len(light[3]) == 3 and dim[1][2:] == bright[1][2:] == [QS_SUN, QS_SUN] and
          slider[2].get('slide_with_bar') == 'true', 'Unexpected brightness row')
    touch = M1['VOL_PANEL_H']
    light[1] = [0, menu[1][1] + menu[1][3] + QS_ROW_GAP, ipod.UI_W, touch]
    check(light[1][1] == M1['VOL_PANEL_Y'] and light[1][1] + touch <= -root[1][1], 'The volume panel must cover the brightness row')
    # Plain, as the Q2's: no pill behind the row; the suns centred under the first and last columns.
    light[2] = {k: v for k, v in light[2].items() if 'bg_image' not in k and 'round_radius' not in k}
    edge = (QS_COLUMN - QS_SUN) // 2
    dim[1] = [edge, (touch - QS_SUN) // 2, QS_SUN, QS_SUN]
    bright[1] = [ipod.UI_W - edge - QS_SUN, (touch - QS_SUN) // 2, QS_SUN, QS_SUN]
    track = [edge + QS_SUN + 12, 0, ipod.UI_W - 2 * (edge + QS_SUN + 12), touch]
    props = ipod.plain_slider(slider[2], ipod.NP_TRACK, ipod.NP_FILL, ipod.QS_BAR)  # the accent at runtime (quick_fill)
    props.update(self_layout='default(x={},y=0,w={},h={})'.format(*track[::2], touch), dragger_size=str(touch))
    props.pop('dragger_adapt_to_icon', None)
    slider[1], slider[2] = track, props
    # The sysbar as the bar (status_bar): the clock centred, Bluetooth, the play state and Wi-Fi at its right, V2.1's
    # battery last; the volume, digital and link badges transparent in place (opacity 0), never moved off screen.
    check([n[2].get('name') for n in sysbar[3]] == QS_SYSBAR, 'Unexpected quick settings sysbar')
    left, clock, right, pgbar, battery = sysbar[3]
    check([n[2].get('name') for n in left[3]] == STATUS_LEFT and [n[2].get('name') for n in right[3]] == STATUS_RIGHT,
          'Unexpected quick settings sysbar widgets')
    bar = {n[2]['name']: n for n in left[3] + right[3]}
    bar['img_playstate'][1][2], bar['img_wifi'][1][2], bar['img_btclass'][1][2] = 12, 14, 42
    height, gap = ipod.STATUS_H, ipod.inc('STATUS_GAP')
    clock[1] = [(ipod.UI_W - CLOCK_W) // 2, 0, CLOCK_W, height]
    right[1] = [clock[1][0] + CLOCK_W, 0, battery[1][0] - gap - clock[1][0] - CLOCK_W, height]
    right[2]['children_layout'] = f'default(r=1,c=0,a=right,s={gap})'
    right[3] = [bar['img_btclass'], bar['img_playstate'], bar['img_wifi']]
    hidden = [bar[k] for k in ('img_volume', 'label_volume', 'img_digital', 'img_synclink')]
    left[3] = []
    sysbar[3] += hidden
    for n in hidden:
        n[1], n[2]['opacity'] = [0, 0, n[1][2], height], '0'
    return root


# 4.7: the confirm pop-up. V2.1's is a 260x180 box, centred, its Cancel and OK half-width buttons along its foot (y 131);
# dialog_confirminfo_dialog_init adds its prompts, Delete File's check and the countdown line at x 0, 260 wide, all
# ending by y 106. The Q2's form (ipod.confirm_rows): a full-width sheet from the top, the prompt above full-width Cancel
# and OK rows from CONFIRM_TOP, under which the page shows dimmed. Stock binds both buttons by name (btn_cancel,
# btn_enter), so they keep theirs.
CONFIRM = 'dialog/confirminfo_dialog.bin'
CONFIRM_STOCK = ([0, 0, 260, 180], [[1, 131, 128, 48], [131, 131, 128, 48]])
CONFIRM_H = M1['CONFIRM_TOP'] + 2 * ipod.CONFIRM_ROW
CONFIRM_EDGE = '#666666'  # V2.1's dialog edge (msginfo_bg's, confirminfo_bg's): about #9b9b9b in Light Mode
CONFIRM_PROMPTS_END = 106  # m1plus_ipod.json confirm.prompt_rows: Delete File's check, y 66 and 40 tall


def confirm_dialog(root):
    """V2.1's confirm pop-up as the iPod's: the Q2's sheet, its rows from CONFIRM_TOP."""
    check(root[2].get('name') == 'confirminfo_dialog' and (root[1], [n[1] for n in root[3]]) == CONFIRM_STOCK and
          [(n[0], n[2].get('name')) for n in root[3]] == [('button', 'btn_cancel'), ('button', 'btn_enter')] and
          CONFIRM_PROMPTS_END <= ipod.CONFIRM_TOP == M1['CONFIRM_TOP'], 'Unexpected confirm dialog')
    root[1] = [0, 0, ipod.UI_W, CONFIRM_H]
    root[2]['self_layout'] = f'default(x=0,y=0,w=100%,h={CONFIRM_H})'
    for state in TEXT_STATES:  # the Q2's stock sheet: black, square, no art
        for key in ('round_radius', 'bg_image'):
            del root[2][f'style:{state}:{key}']
        root[2][f'style:{state}:bg_color'] = '#000000'
    ipod.confirm_rows(root)
    # The sheet ends above the page (the Q2's fills the screen), and V2.1 dims nothing under it: its init clears the
    # highlight (set_dialog_highlight sets ""). Light Mode flips the black sheet to the page's paper, so a 1 px rule
    # along its foot, V2.1's own dialog edge grey, which flips with it, keeps the two apart; only the foot, so the
    # border stays clear over the bar's ends.
    for state in TEXT_STATES:
        root[2].update({f'style:{state}:border_color': CONFIRM_EDGE, f'style:{state}:border': 'bottom',
                        f'style:{state}:border_width': '1'})
    check([n[1] for n in root[3]] == [[0, M1['CONFIRM_TOP'], ipod.UI_W, ipod.CONFIRM_ROW],
                                      [0, M1['CONFIRM_TOP'] + ipod.CONFIRM_ROW, ipod.UI_W, ipod.CONFIRM_ROW]] and
          CONFIRM_H == root[1][3], 'Unexpected confirm rows')


# V2.1's toast (Added To Playlist and the rest): a clear 260x180 dialog over msginfo_bg, a black box with a #666666 edge,
# whose labels its init makes white. The style hook flips the labels to ink in Light Mode, but not the art, so the text
# went dark on black (V063m pass, finding F). Drawn in styles instead, the box, edge and text flip together.
MSGINFO = 'dialog/msginfo_dialog.bin'


def msginfo_dialog(root):
    """V2.1's toast box in styles: black, a 1 px edge in CONFIRM_EDGE, its corners; size, place and highlight kept."""
    style = {f'style:{s}:{k}': v for s in TEXT_STATES for k, v in (('bg_color', '#00000000'), ('bg_image', 'msginfo_bg'),
                                                                   ('border_color', '#00000000'), ('round_radius', '12'))}
    check(root[0] == 'dialog' and root[1] == [0, 0, 260, 180] and not root[3] and root[2] == {
        'name': 'msginfo_dialog', 'highlight': 'default(alpha=100)', 'self_layout': 'default(x=c,y=m,w=260,h=180)', **style},
          'Unexpected toast dialog')
    for state in TEXT_STATES:
        del root[2][f'style:{state}:bg_image']
        root[2].update({f'style:{state}:bg_color': '#000000', f'style:{state}:border_color': CONFIRM_EDGE,
                        f'style:{state}:border': 'all', f'style:{state}:border_width': '1'})


# V2.1's unticked ring (unselect: check_button_style's, Delete Song?'s check, and the M1's choice rows and Theme picker) is a
# white ring over a 50% black disc; the Q2's is the ring alone. Light Mode's image flip (navigation.c ringnav_image_add)
# takes an image mostly dark as a plate and leaves it, so the ring went white on the paper and the disc showed as a grey
# dot, read as ticked (V064m pass). Shipped as the Q2's: each pixel white, its alpha its alpha times its grey, so the
# ring keeps its exact coverage and the disc goes. Over black it looks the same.
def clear_icon(name, data):
    """The audited V2.1 ring (`clear_icons`) without the black under it: white, alpha = alpha x grey."""
    check(sha(data) == AUDIT['clear_icons'].get(name), f'{name}: unaudited ring icon')
    return ipod.imagemagick('png:-', '(', '+clone', '-alpha', 'extract', ')',
                            '(', '-clone', '0', '-alpha', 'off', '-channel', 'R', '-separate', '+channel', ')',
                            '-delete', '0', '-compose', 'multiply', '-composite', '-background', 'white', '-alpha', 'shape',
                            *ipod.PNG_OUT, data=data)


def quiet_icon(name, data):
    """The audited V2.1 control image (`quiet_icons`) as the iPod's quiet glyph of the same name, greyer when pressed."""
    check(sha(data) == AUDIT['quiet_icons'].get(name), f'{name}: unaudited control icon')
    return ipod.imagemagick('png:-', '-trim', '+repage', '-filter', 'Lanczos', '-resize', '24x24',
                            '-channel', 'RGB', '-fill', '#aaaaaa' if name.endswith('down.png') else '#eeeeee',
                            '-colorize', '100', '+channel', '-gravity', 'center', '-background', 'none',
                            '-extent', '28x28', *ipod.PNG_OUT, data=data)


# V2.1 page path -> function(root) that edits the decoded page in place. A Phase 4 item adds its pages here.
REWRITES = {STATUS_BAR: status_bar, HOME_PAGE: home_page, PLAYING_PAGE: playing_page, BIGCOVER: bigcover_page, VOLUME: volume_dialog,
            QUICK: quick_settings, CONFIRM: confirm_dialog, MSGINFO: msginfo_dialog} | {
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
    # 4.6: V2.1's status bar tap opens the VOLUME page (on_wm_tsup_fun, a window manager handler: any window's pointer-up)
    # within 42 px of the screen's top, its stock title's first rows. The iPod's top row starts under the 30 px bar, and
    # its heart must not open the page too. The other names the page relies on are pinned as they are.
    playing = AUDIT['playing']
    for address, instruction, new, purpose in playing['status_tap']:
        word(int(address, 16), int(instruction, 16), int(new, 16), purpose)
    for group in ('recursive_lookups', 'ab_dots', 'volume_init'):
        for address, instruction, purpose in playing[group]:
            pin(data, int(address, 16), int(instruction, 16), purpose)
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
