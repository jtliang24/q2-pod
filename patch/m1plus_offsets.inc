/* The M1 Plus's values for every name of patch/offsets.inc, which includes this file for M1PLUS: V2.1
 * layout, ABI and asset names, each found in V2.1's own code or assets (docs/m1plus-roadmap.md ground
 * rules). An upstream name missing here fails the M1 compile, so a sync gives each new one a V2.1
 * value or compiles its feature out. Names V2.1 shares with V1.32 keep V1.32's comments. */

/* A name whose code can't run on M1, since the hook or call site that reaches it isn't ported
 * (M1PLUS_PORTS 'unported'): #define NAME M1_UNPORTED. test/m1plus/ports.py lists each. A name that
 * code the M1 runs uses gets its V2.1 value instead. */
#define M1_UNPORTED 0
/* The same for an address code reads through I() or P(): 0 there would be arithmetic on a null pointer,
 * a GNU extension -Werror refuses. Low memory is unmapped, so a read faults as one at 0 would. */
#define M1_UNPORTED_ADDR 4

#define UI_W 320
#define UI_H 480
#define BOTTOM 450
#define CORNER_R 0
#define STATUS_MARGIN 0
#define BAR_CORNER_R 0
#define I(p, o) (*(int *)((char *)(p) + (o)))
#define P(p, o) (*(void **)((char *)(p) + (o)))
#define FNV_SEED 2166136261u /* FNV-1a offset basis */
#define W_X 0x00
#define W_Y 0x04
#define W_W 0x08
#define W_H 0x0c
#define W_FOCUS 0x24            /* stock focused flag byte (tests) */
/* V2.1's widget_t has one field fewer before its parent: the block to the vtable is 4 lower (parent
 * window_close and widget_to_global, emitter widget_off_by_func, children layout
 * widget_set_children_layout, vtable widget_get_type 0x70); subclasses still start at 0x78. */
#define W_PARENT 0x44
#define W_CHILDREN 0x58
#define W_EMITTER 0x5c
#define W_CHILDREN_LAYOUT 0x64
#define W_VT 0x70
#define CHILDREN_LAYOUT_VTABLE 0x10
#define DEFAULT_LAYOUT_X_MARGIN 0x18
#define DEFAULT_LAYOUT_SPACING 0x1a
#define EMIT_TYPE 0x08
#define EMIT_PENDING_REMOVE 0x14 /* emitter_remove_item sets it there; V2.1 keeps no other flag */
#define EMIT_NEXT 0x20
#define ROW_HEIGHT 0x78         /* table_client row height */
#define ROW_INDEX 0x78          /* table_row logical index (same slot) */
#define SLIDE_INDEX 0x78        /* slide_menu current index (same slot) */
#define TABLE_ROWS 0x7c         /* table_client logical row count */
#define SELECTOR_INDEX 0x7c     /* text_selector selected option (same slot) */
#define VIEW_CONTENT_H 0x7c     /* scroll_view content height (same slot) */
#define SCROLL_X 0x80           /* scroll_view horizontal offset */
#define TABLE_TOP 0x80          /* table_client viewport top (same slot) */
#define SCROLL_Y 0x84           /* scroll_view viewport top */
#define VIEW_HORIZONTAL 0x90    /* scroll_view xslidable */
#define VIEW_VERTICAL 0x91      /* scroll_view yslidable */
#define VIEW_SNAP 0x92          /* scroll_view snap_to_page */
#define TABLE_ANIMATOR 0xd0
#define VIEW_ANIMATOR 0xe8
#define EVENT_TYPE 0x00
#define EVENT_KEY 0x18
#define EVENT_TARGET 0x10
#define EVENT_X 0x18           /* pointer_event_init @0x640298 */
#define EVENT_Y 0x1c
#define EVT_POINTER_DOWN 0x100 /* wm registers on_wm_tsdown_before_fun for this type @0x523ef0 */
#define EVT_POINTER_MOVE_BEFORE 0x102 /* wm move-before forwards this type to the down hook @0x523ed4 */
#define EVT_POINTER_UP_BEFORE 0x104
#define EVT_POINTER_UP 0x103
#define EVT_POINTER_ABORT 0x107
/* A press as the input thread queues it for window_manager_dispatch_input_event (tslib_run: 0xff
 * on the first sample with pressure, then 0x101 moves, 0x103 on release; V2.1 0x637634); the wm
 * turns it into EVT_POINTER_DOWN for widgets. */
#define EVT_INPUT_POINTER_DOWN 0xff
#define EVT_INPUT_POINTER_MOVE 0x101
#define EVT_DESTROY 0x0c
/* The stock settings lists the payload adds rows to, and the icons its rows borrow (each in the
 * firmware's UI assets and images; tools/build.py checks them against the rootfs). V2.1 names its
 * lists <page>_scrollview, and its 40 px settings icons pset_ and sset_. */
#define VIEW_ABOUT "about_scrollview"
#define ABOUT_FW_LABEL "scrlabel1"            /* About's FW. Version row */
#define ROW_STYLE "list_item_style"            /* V2.1's settings row (list_row_core) */
#define ROW_LABEL_STYLE "srlabel_leftwhite21_style"
#define ROW_CHEVRON "right_arrow"
#define VIEW_SYSSET "sysset_scrollview"
#define VIEW_POWER "standby_scrollview" /* Idle (powermanager_page) */
#define VIEW_DISPLAY "display_scrollview"
#define VIEW_PLAYSET "playset_scrollview"
#define VIEW_BLUETOOTH "bluetooth_scrollview"
#define BT_ROW_H 64 /* its rows' height (the list builder's list_item_create) */
#define ICON_CHARGE "usb_chargeswitch"
#define ICON_POWER "sset_powermanager"
#define ICON_KEYLOCK "sset_keylock"
#define ICON_DISPLAY "sset_display"
#define ICON_COVERMODE "pset_covermode"
#define ICON_FOLDERJUMP "pset_jumpfolder"
#define ICON_MEMPLAY "pset_memplay" /* Resume Songs' row */
#define ICON_BALANCE "pset_balance" /* Mono Audio's row */
#define ICON_GAPLESS "pset_gapless"
/* The payload's own widgets' styles: V1.32's, or V2.1's nearest of the same widget type, colour,
 * size and alignment (V2.1 has no centred 18 px label, no right-aligned 20 px scrolling label: their
 * nearest are 20 px and 16 px). */
#define STYLE_LISTITEM_BLACK "list_item_black_style"
#define STYLE_BTN_LISTITEM "btn_listmore_style"
#define STYLE_LABEL_WHITE18C "label_centerwhite20_style"
#define STYLE_LABEL_WHITE20C "label_centerwhite20_style"
#define STYLE_LABEL_WHITE20L "navbar_leftlabel_white"
#define STYLE_SCRLABEL_WHITE20C "srlabel_msgwhite_style"
#define STYLE_SCRLABEL_WHITE20L "srlabel_leftwhite20_style"
#define STYLE_SCRLABEL_WHITE20R "srlabel_item_right_gray16_styl"
#define STYLE_SCRLABEL_WHITE24L "srlabel_leftwhite22_style"
/* V2.1's title-bar back button (btn_return in its pages' navigationbar_view), which back_button copies. */
#define STYLE_NAVBAR_RETURN "navbar_btnreturn_style"
#define ICON_RETURN "return"
#define ICON_RETURN_DOWN "return_down"
#define BACK_W 48 /* back_button's width, the payload's title-bar height: titles start after it */
/* V2.1's Home: home_page_init's grid builder (0x534064) fills home_sview, a slide_view, with one
 * 320x364 page view per HOME_CARDS ids of pdeq_choicemenu and sets home_sindicator's max to the pages.
 * Each card (0x533d8c) is a HOME_CARD_W x HOME_CARD_H view, two columns from HOME_CARD_X, rows from 0:
 * a clickable 66 px image at HOME_ICON_X, HOME_ICON_Y in home_<name>_style (bg_image <name>, pressed
 * <name>_down) and a line-wrapped label under it in STYLE_HOME_LABEL, from Home's own style file. */
#define VIEW_HOME_SLIDES "home_sview"
#define VIEW_HOME_DOTS "home_sindicator"
#define STYLE_HOME_LABEL "label_centerwhitehome_white"
#define HOME_CARDS 6
#define HOME_PAGE_W 320
#define HOME_PAGE_H 364
#define HOME_CARD_X 6
#define HOME_CARD_W 154
#define HOME_CARD_H 118
#define HOME_ICON_X 44
#define HOME_ICON_Y 20
#define HOME_ICON 66
#define HOME_LABEL_Y 92
#define HOME_LABEL_H 36
/* V2.1's AWTK numbers its events differently from V1.32's from focus on: one lower to the key
 * events (one entry fewer before them), two higher from the window events. Each is V2.1's value in
 * the same stock function that uses V1.32's: widget_on_keydown (0x670908: 0x10f, 0x111, long
 * 0x110), widget_on_keyup (0x670d10: 0x114 before children), home_page_init's on_wm_keyup_fun
 * (0x113), widget_set_focused_internal (0x10d, 0x10e), and the pages' window and value bindings. */
#define EVT_KEY_DOWN 0x10f
#define EVT_KEY_DOWN_BEFORE 0x111
#define EVT_KEY_UP 0x113
#define EVT_KEY_UP_BEFORE 0x114
#define EVT_WINDOW_BACKGROUND 0x12c
#define EVT_WINDOW_FOREGROUND 0x12d /* playset_playset_page_init binds its list's rebuild to it */
#define EVT_WINDOW_CLOSE 0x12e
#define PULL_SEARCH_PX 48       /* device tuning: release distance from the initial touch */
#define PULL_CLAIM_PX 8
#define QUICK_EDGE_PX 31        /* stock on_wm_tsmove_fun @0x4e8d10 */
#define EVT_CLICK 0x10c
#define EVT_FOCUS 0x10d
#define EVT_BLUR 0x10e
#define EVT_IM_ACTION 0x13c /* the keyboard's OK, input_method_dispatch_action @0x656a0c (V1.32's 0x13a) */
#define EVT_SCROLL 0x14e /* stock scroll_view on_scroll @0x5efa40; table setter emits this too */
#define EVT_SCROLL_END 0x14f /* stock lists queue their visible covers on this (album page registers @0x4a43d0) */
#define VIEW_ON_SCROLL 0x100 /* scroll_view callback installed by list_view, called by touch @0x5efa5c */
#define CANVAS_X 0x00
#define CANVAS_Y 0x04
#define CANVAS_LCD 0x30
#define CANVAS_ALIGN_V 0x28
#define CANVAS_ALIGN_H 0x2c
#define LCD_FILL_COLOR 0xbc
#define LCD_STROKE_COLOR 0xc0
#define LCD_TEXT_COLOR 0xb8     /* lcd_set_text_color @0x6474c4 */
/* Selection outline tuning. RADIUS > 2 or the stock rounded path squares off; tests read these.
 * The shade uses the same stock dark surface as the fill at an alpha that keeps the outline
 * above 3:1 on pure white art (0x99 is the floor); on dark rows it matches the stock background
 * exactly and disappears. The line is translucent white at OUTLINE_ALPHA, so it reads as a soft
 * grey on the dark theme instead of a hard white edge; lower OUTLINE_ALPHA or SHADE_ALPHA
 * together and the contrast margin over bright art erodes. */
#define RADIUS 9
#define FILL_RGB 0x2b2b2b
#define FILL_ALPHA 0x40
#define SHADE_ALPHA 0xb3
#define OUTLINE_RGB 0xffffff
#define OUTLINE_ALPHA 0xb3
/* iPod accents, in the order of the Accent setting (IPOD/ACCENT in config.ini; 0 is the default):
 * { selection top, bottom, light tone, red tone, highlight }, 0xRRGGBB. Equal stops keep
 * selection flat on the Q2 panel; retain the fine top highlight. White text holds
 * 4.5:1 on every top. The light tone, the top lightened 12% toward white (Graphite keeps #6E6E6E),
 * is the Now Playing progress fill (3:1 or more on TRACK_COLOR). The highlight is the bar's one-pixel
 * top edge: the light tone, except Graphite's restrained #555555 over its flat bar. The red tone is what stock red #FF1448 becomes (switches, ticks, red text and
 * buttons): Graphite's is silver, so a lit switch reads against the grey off state; the others
 * reuse the light tone, 3:1 or more under white.
 * Crimson keeps every stock color. */
#define ACCENTS { 0x424242, 0x424242, 0x6e6e6e, 0xd8d8d8, 0x555555 }, /* Graphite */ \
                { 0xe8123f, 0xe8123f, 0xeb2f56, 0xff1448, 0xeb2f56 }, /* Crimson */ \
                { 0x13838d, 0x13838d, 0x30929b, 0x30929b, 0x30929b }, /* Tidal */ \
                { 0x8c732c, 0x8c732c, 0x9a8446, 0x9a8446, 0x9a8446 }  /* Champagne */
#define CRIMSON 1
/* The confirm pop-up's stock red discs (confirm_ok, confirm_cancel and their pressed images) take
 * this dark surface under every accent, Crimson included, through the same red-blend mapping: the
 * OK disc becomes CONFIRM_SURFACE, Cancel's lighter tint a mid grey, and the near-white glyphs stay
 * near white (14.2:1 and 5.6:1). The wheel's focus is the accent tile behind the disc, framed white. */
#define CONFIRM_SURFACE 0x2b2b2b
#define CONFIRM_IMAGE "confirm_"
/* Quick settings' active controls (drop_wifiopen, drop_btopen, drop_highgain, ...) are the same
 * red discs with white glyphs, so they take CONFIRM_SURFACE too. Their inactive discs stay stock
 * #444444 and disabled ones keep their grey glyphs. The brightness suns (DROPDOWN_SUN*) sit on
 * black, not a disc, so they keep the accent's red tone. */
#define DROPDOWN_IMAGE "drop_"
/* Stock's red button backgrounds (btn_enter, btn_red and their pressed images) sit under a white
 * label that is not in the image, so they take the light tone like an image with white on its red. */
#define BUTTON_IMAGE "btn_"
#define DROPDOWN_SUN "drop_ligh"
/* An active control's white glyph turns CONFIRM_SURFACE on an accent tone brighter than this
 * (perceived 0-255, 0.299 R + 0.587 G + 0.114 B): Graphite's silver; the others keep white. */
#define GLYPH_LIGHT_MAX 160
/* bitmap_t (docs/internals.md#accent): format u16 @0xe, 1 RGBA, 2 ABGR, 3 BGRA, 4 ARGB, 4 bytes a pixel
 * by bitmap_get_bpp_of_format; per format, the byte offsets of r, g, b and a. */
#define BITMAP_RGBA_AT { { 0, 1, 2, 3 }, { 3, 2, 1, 0 }, { 2, 1, 0, 3 }, { 1, 2, 3, 0 } }
#define STOCK_RED 0xff1448
#define RED_TOLERANCE 8 /* per channel, 0-255: how far a color may sit from a red/neutral blend */
/* iPod black status chrome (Classic: BAR_CLASSIC); TRACK_COLOR is Now Playing's progress track. */
#define BAR_COLOR 0x000000
#define TRACK_COLOR 0x1c1c1c
#define NP_TIMES_PX 14 /* Now Playing's times, and the volume text in their place */
#define NP_ART_RADIUS 12 /* Now Playing's art corners (paint_cover), as stock's play_defaultcover scaled to the art */
/* A radius-r corner's arc at row y (0 the outermost): how far in it starts, in 1/16 pixels. */
static inline int arc_out(int r, int y) {
    if (!r) return 0;
    int d = 2 * (r - y) - 1, v = (4 * r * r - d * d) * 64, s = 0;
    while ((s + 1) * (s + 1) <= v) ++s;
    return 16 * r - s;
}
#define PLACEHOLDER (IPOD ? "default_album_flow" : "default_album_big") /* Cover Flow's and Spotify's missing art */
#define VOL_POLL_MS 50 /* how often the volume indicator checks for a change */
/* The volume panel off Now Playing (vol_paint): exactly over Quick Settings' brightness row
 * (tools/ipod.py checks it), its rounded corners clear of the 80px glass corners. */
#define VOL_PANEL_X 26
#define VOL_PANEL_Y 256
#define VOL_PANEL_H 48
#define VOL_PANEL_PAD 20
#define VOL_PANEL_BAR 10
#define VOL_PANEL_TEXT 52
#define VOL_PANEL_PX 20 /* the panel's number */
#define VOL_PANEL_TRACK 0x5a5a5a
/* The centred 16px clock and battery clear the rounded glass; widths are checked with the stock font. */
#define CLOCK_EDGE 57
#define STATUS_GAP 4
#define BATT_PCT_W 42
#define BATT_PCT_PX 16
#define BATT_BODY_W 16
#define BATT_BODY_H 11
#define BATT_INSIDE_W 32
#define BATT_INSIDE_H 16
#define BATT_INSIDE_NUB_H 6
#define BATT_INSIDE_TEXT_DY 1
#define BATT_INSIDE_PX 13
#define BATT_NUB_W 2
#define BATT_NUB_H 5
#define BATT_PX 16
#define BATT_GAP 2
/* Icon + Percent: BATT_PX digits' ink (rows 8-20 of the 30 px bar, line box centred) sits a row
 * above the centred BATT_BODY_H icon (rows 10-20), so the icon rises BATT_PCT_DY to share its centre. */
#define BATT_PCT_DY 1
#define BATT_CHARGE_RGB 0x34c759
#define BATT_LOW_RGB 0xff1448
#define BATT_ROOM 94
/* Plain Bluetooth ink and codec reaches from the right edge of their stock canvases. */
#define BT_REACH 10
#define BT_CODECS { "bar_sbc", "bar_aac", "bar_aptx", "bar_aptxhd", "bar_ldac" }
#define BT_CODEC_REACH { 22, 12, 27, 41, 36 }
#define BT_GLYPH "bar_btcon" /* the white Bluetooth glyph; stock's bar_bt is the grey one */
/* A new codec badge shows CODEC_MS, then fades out and the glyph in, CODEC_STEPS steps of
 * CODEC_STEP_MS each way. */
#define CODEC_MS 1000
#define CODEC_STEP_MS 25
#define CODEC_STEPS 6
/* iPod: the full-screen art (stock's bigcover_page) shows the song name BC_MS, then it and its shade
 * fade out in BC_STEPS steps, BC_STEP_MS apart. */
#define BC_MS 3000
#define BC_STEP_MS 50
#define BC_STEPS 8
/* iPod drill rows: the stock list_into image sits where stock rows put their own img_into, its left
 * edge CHEVRON_W from the row's right edge (8 px margin + 50 px image), so every `>` lines up. */
#define CHEVRON_W 58
/* iPod Home: Split gives the menu half the screen (HOME_SPLIT_W) in both themes, the art the rest right of it;
 * Minimal's Full rows are full width. Labels end HOME_LABEL_END from the row's edge. The selection
 * dot (HOME_DOT px) sits at HOME_DOT_X, clear of the bottom row's corner, HOME_DOT_GAP before the
 * labels (HOME_TEXT_X in tools/ipod.py). */
#define HOME_FULL_ROW 320
#define HOME_LABEL_END 16
#define HOME_SPLIT_LABEL_END 8 /* Split: the art, not a corner, is beside the labels */
#define HOME_DOT_X 12
#define HOME_DOT 6
#define HOME_DOT_GAP 8
#define HOME_SPLIT_W 160
#define HOME_CLASSIC_ROW 314
#define HOME_TOP 8 /* Minimal's decorative inset; Classic starts below the status bar. */
#define HOME_CHEVRON_SHIFT 6
#define HOME_CLASSIC_TEXT_X 20
#define HOME_CLASSIC_LABEL_END (CHEVRON_W - 10)
#define BAR_CLASSIC 0x242424
#define NP_BAR_CLASSIC 8
#define NP_BAR_MINIMAL 4
#define MINIMAL_FILL 0xeeeeec
#define MINIMAL_CHEVRON 0x777777
/* Minimal's small capitals are SUDO_TRACK px apart (draw_spaced); secondary text is SUDO_MUTED. */
#define SUDO_TRACK 2
#define SUDO_MUTED 0x8c8c8c
#define HOME_CAPS_PX 18 /* Minimal's Home labels */
#define MARK_PX 14 /* and the status bar's idle Q2 */
/* Minimal's selection is a card SEL_INSET px in from each side of the row, corners SEL_RADIUS. */
#define SEL_INSET 6
#define SEL_RADIUS 6
#define TILE_INSET 2 /* album cards stay inside their tile on all four sides */
#define TILE_CLEARANCE 4 /* artwork and labels sit this far inside the card */
#define EDIT_OK_PX 18 /* the date, time and sleep timer pages' OK label, on that card */
/* Minimal's Now Playing album is NP_CAPS_PX capitals, NP_CAPS_INSET in from its label's edge as
 * stock hscroll_label insets the title and artist (margin_left, default 2, 0x5e8378). */
#define NP_CAPS_PX 15
#define NP_CAPS_INSET 2
#define PAGE_SLIDE_MS 120
#define NP_ARTIST_RGB 0xcccccc
/* Now Playing's text (local, Spotify and Radio): the title over the artist and album, the album
 * lighter than the other grey text so it reads at a glance. */
#define NP_TITLE_PX 22
#define NP_META_PX 18
#define NP_ALBUM_RGB 0xbbbbbb
/* Spotify's and Internet Radio's Now Playing layout (tools/ipod.py NP_*, which checks they match):
 * the art and the text 16px from the sides, 12 apart, the bar and times clear of the glass's corners.
 * The title, artist and album beside the art on the Q2; on the M1's portrait screen, under it, with
 * the page's tag after the back button and Radio's heart at the top right. */
#define SPOT_ART_X 50
#define SPOT_ART_Y 50
#define SPOT_ART_PX 220
#define SPOT_TEXT_X 16
#define SPOT_TEXT_W 288
#define SPOT_TITLE_Y 280
#define SPOT_ARTIST_Y 312
#define SPOT_ALBUM_Y 338
#define SPOT_BAR_X 12
#define SPOT_BAR_Y 374
#define SPOT_BAR_W 296
#define SPOT_BAR_H 8
#define SPOT_TIMES_Y 392
#define SPOT_TIME_X 12
#define SPOT_TAG_X BACK_W
#define SPOT_HEART_X (UI_W - 54)
#define SPOT_HEART_Y 0
/* iPod settings rows (docs/ipod.md#settings): Minimal starts SET_TOP below the status bar, Classic flush, and
 * holds SET_ROWS complete SET_ROW rows. Stock builds each row as a list_item holding a
 * SET_STOCK_W x SET_STOCK_BODY button at x SET_STOCK_X with a SET_STOCK_ICON icon, a label and a
 * 50px trailing image (chevron, tick or switch); items made SET_STOCK_ROW high are normalised to
 * SET_ROW. The icon shrinks to SET_ICON at SET_ICON_X, the text starts SET_GAP after it (or at
 * SET_TEXT_X without one) and trailing images end SET_EDGE from the right edge; test/build.py
 * and test/patch.py check them against the rounded glass in the first and last visible rows. */
#define SET_ROW 68
#define SET_TOP 8
#define SET_ROWS 4
#define SET_ICON 40
#define SET_ICON_X 28
#define SET_GAP 12
#define SET_TEXT_X 20
#define SET_EDGE 24
#define SET_STOCK_ROW 78
#define SET_STOCK_BODY 70
#define SET_STOCK_X 20
#define SET_STOCK_W 335
#define SET_STOCK_ICON 52
#define SET_STOCK_TRAIL 276   /* the usual trailing image x in the stock button */
#define SET_RIGHT_SIDE 150    /* stock children starting here keep to the right edge */
#define LIST_DEFAULT_ITEM_HEIGHT 0x7c  /* list_view default_item_height */
#define IMAGE_DRAW_SCALE_DOWN 5        /* "scale_down" in the stock draw type table @0x9272c0 */
#define IMAGE_DRAW_CENTER 1            /* "center", the same table */
/* iPod fast-scroll letter: the selected row's first character in white, LETTER_PX high, on a
 * LETTER_BOX square of the stock dark surface at LETTER_ALPHA, centred over the list. */
#define LETTER_BOX 80
#define LETTER_RADIUS 12
#define LETTER_ALPHA 0xd9
#define LETTER_PX 60
#define LETTER_MS 400
/* iPod Now Playing scrub: SCRUB_STEP seconds per detent times the list ramp, previewed until
 * centre or Return commits it, or SCRUB_MS without input commits it and puts the wheel back on volume. */
#define SCRUB_STEP 5
#define DOUBLE_CLICK_MS 250 /* a second centre press within this is a double press */
#define WAKE_MS 500 /* Wake: Double press, the screen-off double press; looser, done blind in a hand */
#define SCRUB_MS 3000
#define LYRIC_STEP 25 /* px per wheel tick on the lyrics page: one stock lyric row */
/* With the screen off the UI loop idles this long a turn instead of stock's 8 ms, about 10 turns a
 * second; screen-off keys (volume, play/pause, wake) wait at most this much longer. */
#define SCREEN_OFF_SLEEP_MS 100
/* Screen off, nothing playing (media_playing) and the DAC already off (check_dacoff_state, about 31
 * s after playback stops; g_dacoff_time -1): the turn idles DARK_IDLE_SLEEP_MS, about 4 turns a
 * second, so a Q2 left dark without Standby stops waking the CPU for nothing. The first key waits
 * at most that; Wake's second press is timed at the screen-off pace. */
#define DARK_IDLE_SLEEP_MS 250
/* Bluetooth absolute volume is read back this often with the screen off and no volume limit to
 * hold, or after the headset refused it (bt_volume_poll); 400 ms otherwise. A headset's own volume
 * keys show on the M1 that late. */
#define BT_VOLUME_SLOW_MS 2000
/* Screen on, once IDLE_MS pass without input or a window animation, each turn idles IDLE_SLEEP_MS
 * (about 30 passes a second; the first input after waits at most that). */
#define IDLE_MS 2000
#define IDLE_SLEEP_MS 25
/* Charge limit: the charger stops at CHARGE_STOP percent and starts again at CHARGE_RESUME,
 * checked every CHARGE_POLL_MS. */
#define CHARGE_STOP 80
#define CHARGE_RESUME 75
#define CHARGE_POLL_MS 5000
/* Standby limit (docs/internals.md#standby-limit): its three choices after Off, in hours of one
 * Standby, after which the Q2 powers off. On M1 the row is off: toolsIntoStandby isn't hooked. */
#define STANDBY_LIMIT_1 1
#define STANDBY_LIMIT_2 8
#define STANDBY_LIMIT_3 24
/* The Wi-Fi signal (ringnav_wifi_signal) is read from the driver again at most every
 * WIFI_SIGNAL_MS; its two pollers each ask about once a second. */
#define WIFI_SIGNAL_MS 1000
/* Resume (docs/internals.md#resume): tracks of Q2POD RESUMEMIN minutes or longer (crossfade.c
 * resume_min) keep their place in the RESUME_SLOTS most recent; a place within RESUME_EDGE_S of
 * either end is forgotten. Saved on a track change, a pause and every RESUME_SAVE_S of play;
 * restored if the track has played less than RESUME_START_S when first seen playing. */
#define RESUME_SLOTS 512
#define RESUME_EDGE_S 30
#define RESUME_SAVE_S 60
#define RESUME_START_S 5
/* Play counts (docs/internals.md#play-counts): a track over LISTEN_MIN_S counts once half of it,
 * or LISTEN_MAX_S, has been heard; PLAYS_SLOTS counts are kept, the lowest replaced when full, and
 * Most Played lists the top PLAYS_TOP. */
#define LISTEN_MIN_S 30
#define LISTEN_MAX_S 240
#define PLAYS_SLOTS 512
#define PLAYS_TOP 100
/* Ratings (docs/internals.md#ratings): RATE_SLOTS songs keep 1-4 hearts (5 is My Fav); holding
 * Now Playing's heart RATE_HOLD_MS opens the picker. */
#define RATE_SLOTS 4096
#define RATE_HOLD_MS 500
/* Now Playing's heart and its stock click, which toggles My Fav for the playing track (manage_myfav)
 * and the heart with it; playing_page_init binds it with the window. */
#define VIEW_FAV "btn_fav"
#define FAV_CLICK_ADDR 0x53b480
#define STYLE_FAV "btn_imgfav_style"
#define ICON_FAV "p_fav"
#define ICON_UNFAV "p_unfav"
/* The playlist page's row click, which in add mode 2 (Now Playing's hold) adds the queue's selected
 * record, with the row as context. */
#define PLAYLIST_PICK_ADDR 0x53d300
/* Lock screen (lockscreen.c): the lock window's clock and battery, which Large lays out again. */
#define VIEW_LOCK_TIME "dclock_time"
#define VIEW_LOCK_DATE "dclock_date"
#define VIEW_LOCK_LEVEL "pgbar_battery"
#define LOCK_CLOCK_Y 60 /* Large's top line: all above the now-playing card at 362 */
/* The Lock screen page (systemset_screensaver_page_init): view_covers holds V2.1's picture grid,
 * 90 x 135 pictures three to a row, over its Time show and About rows; its visit binds the first
 * SAVER_PICTURES pictures' clicks to V2.1's pick (saver_pick). */
#define VIEW_SAVER_COVERS "view_covers"
#define VIEW_SAVER_TIME "listitem_time"
#define VIEW_SAVER_ABOUT "listitem_about"
#define ICON_SAVER_CLOCK "screensaver_timeshow" /* Time show's own, on the Clock row */
#define SAVER_PICTURES 6
#define SAVER_X 12
#define SAVER_COL 103
#define SAVER_ROW 143
#define SAVER_ITEM 58 /* Time show to About */
#define VIEW_LOCK_BATTERY "img_battery"
/* M1 Plus: a press held still this long on a library row opens its hold menu (ringnav_input). */
#define LONG_PRESS_MS 500
/* Long Songs (docs/internals.md#long-songs): songs longer than this. */
#define LONG_SONG_S 600
/* End bump and wrap, audited row lists only (see ring_list in patch/navigation.c). A detent past an
 * end nudges the outline; further detents stop there while the wheel keeps turning, and the first
 * same-direction detent after a pause of EDGE_PAUSE_MS moves to the other end of the same list. */
#define BUMP_PX 6
#define BUMP_MS 120
#define EDGE_PAUSE_MS 300 /* well above WHEEL_RUN_MS, so a spin never counts as a pause */
#define BAR_VALUE 0x7c /* scroll_bar native value, maintained by list/table scroll callbacks */
#define KEY_VOLUMEDOWN 221
#define KEY_VOLUMEUP 220
#define KEY_POWER 210
#define KEY_PLAY 213
#define KEY_BACK_BTN 214 /* on_wm_keyup_fun: 214 prev_quick_click, 215 next_quick_click (0x4cdb14) */
#define KEY_FWD_BTN 215
#define KEY_RETURN 170
#define KEY_CENTER 218
#define KEY_PREV 172
#define KEY_NEXT 173
#define WM_KEY_SLEEP KEY_POWER
/* Stock drops wheel ticks while KEY_LOCKOUT is set, 800 ms after Centre, so a press that brushes
 * the wheel cannot scroll; only its first LOCKOUT_KEEP x 100 ms are kept (ringnav). */
#define LOCKOUT_KEEP 2
/* Wheel ticks during a page's slide or before its list loads wait up to HOLD_MS, at most HOLD_MAX
 * of them, then play into the page one per HOLD_POLL_MS, so a turn begun on Back or Select carries
 * on instead of being lost. */
#define HOLD_MS 1200
#define HOLD_MAX 8
#define HOLD_POLL_MS 16
/* The wheel (playback.c wheel_sample): knob units per tick at 50% Wheel sensitivity (a seventh of
 * a turn), 200 a turn, and stock's poster encoderknob_thread_run+0x150, which dispatches the
 * thread info's key event. */
#define WHEEL_TICK_UNITS 28
#define WHEEL_INFO_EVENT 0x20 /* event type: 0x110 key down, 0x114 key up */
#define WHEEL_INFO_KEY 0x38   /* the event's key (EVENT_KEY) */
/* V2.1 has no wheel lockout and no Return key latch. on_wm_keyup_fun (0x4cd9ac) drops a power
 * (knob) release while this byte or g_power_longkey (tools/build.py M1PLUS_RAW_GLOBALS) is set and
 * clears both; to_poweroptions sets this one after into_standby returns (0x4ce6d4). */
#define BOOT_KEY_GUARD 0xa041a3

/* slide_menu_scroll_to @0x5f3400 and completion @0x5f3654; animator
 * start @0x665ab0, time_elapse @0x6660d4, scroll_set_params @0x682124. */
/* V2.1's slide_menu has no spacer: on_scroll_done (0x6123f4) moves value - round(xoffset / h),
 * and scroll_to (0x612278) keeps xoffset at 0x88 and its animator at 0xb8, which it registers for
 * 0x127. widget_animator_t is 4 bytes on: time_elapse (0x673678) and scroll_set_params (0x68cd04). */
#define SLIDE_OFFSET 0x88
#define SLIDE_ANIMATOR 0xb8
#define ANIM_ELAPSED 0x14
#define ANIM_START_TIME 0x1c
#define ANIM_DURATION 0x24
#define ANIM_X_TO 0x64
#define ANIM_X_FROM 0x6c
#define EVT_ANIM_END 0x127
#define slide_stride(w) I(w, W_H)
#define SLIDE_EASING 8          /* stock scroll_to easing */

/* Play/Pause hold queue menu (docs/internals.md). AWTK input_device_status lives at
 * wm+0x98 (window_manager_get_input_device_status @0x66e734): 16 key records of 0x18 bytes from
 * +0x30, each {key, long fired, u64 press time @8, aborted @0x10}. */
#define EVT_KEY_LONG 0x110
#define INPUT_KEYS 0x18
#define INPUT_KEY_SIZE 0x18
#define INPUT_KEY_COUNT 16
#define INPUT_KEY_TIME 0x08
/* stSongInfo rows of p_deque_showlist and the mcl queue. */
#define REC_ID 0x00             /* -1/-2: unknown album/artist */
/* tidal_play's Downloads naming only: on M1, tidal_start passes no song id, so it streams stock's
 * way first. V2.1's get_tidal_trackurl (0x512ed0) hands its URL thread (0x51c288) the whole row. */
#define REC_TIDAL_ID M1_UNPORTED
/* tidal_start passes no song id: V2.1's two callers (0x500d5c, 0x51c7b0) keep no audited id, so stock
 * streams, uncached (patch/tidal.c, roadmap U4). */
#define TIDAL_ID_REG "$zero"
#define REC_NAME 0x08          /* the file name; REC_TITLE is the tag's, empty when untagged */
#define REC_PATH 0x0c
#define REC_TITLE 0x10
#define REC_ALBUM 0x14
#define REC_ARTIST 0x18
#define REC_ALBUM_ARTIST 0x24   /* albumsonger; empty or null in folder-queue records */
#define REC_TYPE 0x34           /* 8 song, 4 directory */
#define REC_TRACK 0x3c          /* the tag's track and disc numbers, 0 when untagged */
#define REC_DISC 0x40
#define REC_CUE_START 0x48      /* a CUE track's start and end seconds, 0 otherwise */
#define REC_CUE_END 0x4c
/* g_play_id3_info, as player_get_id3info (0x5146bc) parses the playing file: its path, then tags. */
#define ID3_ALBUM 0x404
#define ID3_ARTIST 0x504
#define ID3_TITLE 0x684
/* toolsGetMusicInfo's info (ID3_ALBUM's base): abmartist, its id3 field 6, copied to +0x580 @0x5ecbc4 as
 * V1.32 does. ringnav_music_info isn't hooked on M1 (toolsGetMusicInfo, roadmap U4); now_tag reads it. */
#define MUSIC_INFO_ALBUM_ARTIST 0x580
#define ID3_ALBUM_ARTIST (ID3_ALBUM + MUSIC_INFO_ALBUM_ARTIST) /* a CUE track's, from its file (ringnav_id3_path) */
/* Lyrics from tags (ringnav_lyric): mclLoadExLyric isn't hooked on M1 (roadmap U3's batch), and the
 * M1's libtag_c.so.2.0.1 is another build than the Q2's, so its offsets are to be found too. */
#define MCL_LYRICS M1_UNPORTED_ADDR
#define MCL_LYRIC_LOCK M1_UNPORTED
#define TAGLIB_NEW_GOT M1_UNPORTED_ADDR
#define TAGLIB_FILE_NEW M1_UNPORTED
#define TAGLIB_PROPERTY_GET M1_UNPORTED
#define TAGLIB_PROPERTY_FREE M1_UNPORTED
#define CLASS_ALBUMS 0xf003     /* all albums: rows open getMusicByAlbum (load_localclass_list 0xff10) */
#define MUSIC_WHERE "fileurl not like '/mnt/mmc/audiobooks/%' and fileurl not like '/mnt/mmc/podcasts/%' and fileurl not like '%.m4b'"
#define CLASS_ARTIST_ALBUMS 0xff01 /* an artist's albums (load_localclass_list 0xff11) */
/* The albums row the album page opened: its init's context >> 16, which it keeps */
#define ALBUMINFO_ROW 0xa06680  /* albuminfo_page_init (0x526828) */
/* Static mcl queue state (mclLoadPlayList @0x5aa8d4, mclNextSong @0x5adbbc). */
/* V2.1 keeps the same block, the words at the same offsets from MCL_POS: mclGetPlayPos (0x5d4290),
 * mclGetPlayType, mclGetPlayMode, mclGetLastPos, mclGetRandomNum (the pool), mclCheckMplayerSocket
 * and mclGetJumpFolder/mclGetGaplessMode (bytes) read them; mclSetPlayMode (0x5d278c) closes a
 * preload with MCL_PRELOAD and MCL_FD, and the preload pick (0x5d0ea4) sets MCL_PREPOS.
 * config_mplayer (0x4d869c) re-applies speed and mode as V1.32's player_initconfig does. */
#define MCL_POOL 0xa0aae8
#define MCL_LASTPOS 0xa0abc8
#define MCL_PREPOS 0xa0abcc
#define MCL_PRELOAD 0xa0abd0
#define MCL_TYPE 0xa0abd8
#define MCL_POS 0xa0abdc
#define MCL_MODE 0xa0abe0
#define MCL_JUMPFOLDER 0xa0ab88
#define MCL_GAPLESS 0xa0ab89
#define MCL_FD 0xa0abec
#define INITCONFIG_SPEED_RET 0x4d86c4
#define INITCONFIG_MODE_RET 0x4d8738
/* config_init applies the saved play mode itself at boot, before memory play reads the queue: its
 * mclSetPlayMode call (jalr 0x4e596c) returns here. V1.32's goes through ringnav_bootmode. */
#define BOOT_MODE_RET 0x4e5974
/* mclUsbAudioSetVol (0x5ac574): the USB DAC's volume control, -1 before the first set, -2 when it
 * has none and hciplayer's soft volume (mcl-softvolflag) applies instead (0x5a8498 opens hw:1). */
#define USB_MIXER 0xa0aba4 /* mclUsbAudioSetVol (0x5d4694), MCL_POS - 0x38 as in V1.32 */
/* Stock sortselect_dialog callbacks the menu replaces: both set g_sort_changeflag, which makes
 * allmusic reload and scroll to the top on return. */
#define SORTSELECT_CLOSE 0x47d0f0
#define SORTSELECT_BACK "button_return"
#define SORTSELECT_VIEW "scrollview_sortselect"
/* The hold menu's rows as V2.1 builds its own (dialog_sortselect_dialog_init 0x47d440): in its
 * 260 px popup (the asset's self_layout), 50 px rows, the label at 12, the check image at 224. */
#define VIEW_SORTSELECT_TITLE "hscroll_label"
#define STYLE_SORTSELECT_ROW "list_itemsort_style"
#define STYLE_SORTSELECT_LABEL "srlabel_leftwhite20_style"
#define ICON_SORTSELECT_CHECK "mulselected"
#define SORTSELECT_W 260
#define SORTSELECT_ROW 50
#define SORTSELECT_LABEL_X 12
#define SORTSELECT_CHOICE_W 184 /* a choice's label, beside its check */
#define SORTSELECT_LABEL_W 236  /* an action's, the row less its margins */
#define SORTSELECT_CHECK_X 224
#define SORTSELECT_CHECK_W 26

/* Coverflow (docs/internals.md). slide_menu dispatches EVT_VALUE_CHANGED after its
 * index moves (0x5f320c). The stock scan thread handle (dialog_updatemusic_dialog_init) and its
 * done flag (wait_scan sets it) have no symbols: a scan runs while the handle is set and the
 * flag is clear. */
#define EVT_VALUE_CHANGED 0x11c
#define EVT_VALUE_CHANGING 0x11d
/* playset_bootvol_page_init binds these, each with the window as context; Crossfade re-dresses the
 * page (crossfade.c) and unbinds them first. */
#define BOOTVOL_SWITCH 0x49d328   /* btn_memory's click */
#define BOOTVOL_DEC 0x49d39c      /* btn_dec's click */
#define BOOTVOL_ADD 0x49d4c8      /* btn_add's click */
#define BOOTVOL_CHANGING 0x49d418 /* vol_slider's EVT_VALUE_CHANGING; nothing binds EVT_VALUE_CHANGED */
#define VIEW_BOOTVOL_TITLE "label_title"
#define VIEW_BOOTVOL_SWITCH "btn_memory"
#define VIEW_BOOTVOL_SWITCH_LABEL "label_memory"
#define VIEW_BOOTVOL_SWITCH_ICON "img_switchmemory"
#define VIEW_BOOTVOL "bootvol_view"
#define VIEW_BOOTVOL_SLIDER "vol_slider"
#define VIEW_BOOTVOL_DEC "btn_dec"
#define VIEW_BOOTVOL_ADD "btn_add"
#define VIEW_BOOTVOL_VALUE "label_vol"
#define ICON_SWITCH_ON "sset_on"
#define ICON_SWITCH_OFF "sset_off"
#define SCAN_THREAD 0xa03a44
#define SCAN_DONE 0xa03a40
#define BT_PAIRLIST 0xa041c0 /* stock pdeq_btpairlist (a symbol in V2.1) */
/* Coverflow text: iPod keeps every label CF_EDGE from the sides, where the lowest track row's text
 * clears the bottom corners; both builds keep the captions there. Album names and artists scroll
 * within that. Under the covers (CF_TEXT_Y), the album name is CF_NAME_PX white and the artist
 * CF_ARTIST_PX in CF_GREY (stock secondary text) right under it. */
#define CF_EDGE 16
#define CF_NAME_PX 24
#define CF_NAME_H 32
#define CF_ARTIST_PX 20
#define CF_ARTIST_H 28
#define CF_GREY 0xffaaaaaa /* color_t #AAAAAA */
#define CF_VIEW_W 320
#define CF_VIEW_H 260
#define CF_CX 160
#define CF_TOP 16
#define CF_EYE 300
#define CF_X1 100
#define CF_XS 40
#define CF_Z1 80
#define CF_ZS 18
#define CF_BRIGHT1 192
#define CF_BRIGHT2 128
#define CF_REFLECT 24
#define CF_REFLECT_TOP (IPOD ? 48 : 64)
#define CF_STRIDE 100
#define CF_TEXT_Y 268

#define PH_COLS 3
#define PH_GRID_X 4
#define PH_TILE_W 104
#define PH_TILE_H 96
#define PH_THUMB_W 96
#define PH_THUMB_H 88
#define PH_SHOT_W 320
#define PH_SHOT_H 450
#define PH_GRID_H 402

#define PEQ_GRAPH_H 120
#define PEQ_GRAPH_X 12
#define PEQ_GRAPH_DB 15
#define PEQ_PLOT_TOP 8
#define PEQ_PLOT_BOTTOM 98

#define VIS_H 240
#define BOOK_ROWS 16
#define PH_GREY 0xff333333 /* color_t #333333 */
#define PHOTOS_MAX 500 /* ponytail: ringnav navigates at most MAX_ENTRIES (512) rows; page beyond */
/* iPod visualizer (patch/visualizer.c, docs/ipod.md#visualizer), Now Playing's fourth page. The
 * page shows the audio VIS_LATENCY_MS behind what hciplayer last handed the filter: its ao_alsa asks
 * for a 500 ms buffer in 16 periods (0x438a2c: buffer_time 500000 us) and refills it a period at a
 * time, so a block waits about 500 ms less half a period to a period; Bluetooth adds its own, so this
 * stays the knob for sync. VIS_FPS frames a second; spectrum bars
 * fall VIS_DECAY of full scale a second, their caps hold VIS_HOLD_MS then fall at VIS_GRAVITY full
 * scale a second squared. Levels span VIS_FLOOR_DB below full scale; the VU meters read 0 VU at
 * VIS_VU_REF_DB dBFS RMS and light their peak LED from VIS_LED_DB dBFS for VIS_HOLD_MS. A paint that
 * found the page unsettled (under a closing window, mid-slide) looks again VIS_RETRY_MS later. */
#define VIS_LATENCY_MS 480
#define VIS_RETRY_MS 250
#define VIS_FPS 25
#define VIS_BARS 32
#define VIS_DECAY 1.6f
#define VIS_HOLD_MS 400
#define VIS_GRAVITY 3.0f
#define VIS_FLOOR_DB 60
#define VIS_VU_REF_DB -14
#define VIS_LED_DB -1
