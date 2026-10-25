/* The names the M1 Plus port adds to the shared C files, at the Q2's values: patch/offsets.inc
 * includes this after upstream's own names. Each is V1.32's, or an upstream literal the shared code
 * now names; patch/m1plus_offsets.inc gives V2.1's. */
#ifndef M1PLUS
#define M1PLUS 0
#endif
#define UI_W 375
#define CHOICE_CHECK "select" /* a CHOICE picker's checked option's image */
#define UI_H 320
#define BOTTOM 290
#define CORNER_R 80
#define STATUS_MARGIN 52
#define BAR_CORNER_R 76
#define W_CHILDREN 0x5c
#define W_VT 0x74
#define EVT_POINTER_UP 0x103
/* A press as the input thread queues it for window_manager_dispatch_input_event (tslib_run: 0xff
 * on the first sample with pressure, then 0x101 moves, 0x103 on release; V2.1 0x637634); the wm
 * turns it into EVT_POINTER_DOWN for widgets. */
#define EVT_INPUT_POINTER_DOWN 0xff
#define EVT_INPUT_POINTER_MOVE 0x101
/* The stock settings lists the payload adds rows to, and the icons its rows borrow (each in the
 * firmware's UI assets and images; tools/build.py checks them against the rootfs). V2.1 names its
 * lists <page>_scrollview, and its 40 px settings icons pset_ and sset_. */
#define VIEW_ABOUT "scroll_view_about"
#define VIEW_SYSSET "scroll_view_sysset"
#define VIEW_POWER "scroll_view_powermanager"
#define VIEW_DISPLAY "scroll_view_display"
#define VIEW_PLAYSET "scroll_view_playset"
#define VIEW_BLUETOOTH "scroll_view_bluetooth"
#define BT_ROW_H 78
#define ICON_CHARGE "usb_chargeswitch"
#define ICON_POWER "system_powermanager"
#define ICON_KEYLOCK "system_keylock"
#define ICON_DISPLAY "system_display"
#define ICON_COVERMODE "playset_covermode"
#define ICON_FOLDERJUMP "playset_folderjump"
#define ICON_MEMPLAY "playset_memplay" /* Resume Songs' row */
#define ICON_BALANCE "playset_balance" /* Mono Audio's row */
#define ICON_GAPLESS "playset_gapless"
#define ICON_DSDOUTPUT "playset_dsdoutput" /* MQA's row */
/* The payload's own widgets' styles: V1.32's, or V2.1's nearest of the same widget type, colour,
 * size and alignment (V2.1 has no centred 18 px label, no right-aligned 20 px scrolling label: their
 * nearest are 20 px and 16 px). */
#define STYLE_LISTITEM_BLACK "s_listitem_black"
#define STYLE_BTN_LISTITEM "s_btn_listitem"
#define STYLE_LABEL_WHITE18C "s_label_white18c"
#define STYLE_LABEL_WHITE20C "s_label_white20c"
#define STYLE_LABEL_WHITE20L "s_label_white20l"
#define STYLE_SCRLABEL_WHITE20C "s_scrlabel_white20c"
#define STYLE_SCRLABEL_WHITE20L "s_scrlabel_white20l"
#define STYLE_SCRLABEL_WHITE20R "s_scrlabel_white20r"
#define STYLE_SCRLABEL_WHITE24L "s_scrlabel_white24l"
#define EVT_WINDOW_FOREGROUND 0x12b
#define SPOT_TITLE_Y (SPOT_ART_Y + 41)
#define SPOT_ARTIST_Y (SPOT_ART_Y + 75)
#define SPOT_ALBUM_Y (SPOT_ART_Y + 103)
#define SPOT_TAG_X 16
#define SPOT_HEART_X (UI_W - (IPOD ? 72 : 55)) /* local Now Playing's heart (tools/ipod.py img_fav) */
#define SPOT_HEART_Y 176
/* Now Playing's heart and its stock click, which toggles My Fav for the playing track (manage_myfav)
 * and the heart with it; playing_page_init binds it with the window. */
#define VIEW_FAV "img_fav"
#define FAV_CLICK_ADDR 0x52b154
#define ICON_FAV "play_fav"
#define ICON_UNFAV "play_unfav"
/* The playlist page's row click, which in add mode 2 (Now Playing's hold) adds the queue's selected
 * record, with the row as context. */
#define PLAYLIST_PICK_ADDR 0x4b1d24
/* Lock screen (lockscreen.c): the lock window's clock and battery, which Large lays out again. */
#define VIEW_LOCK_TIME "clock_time"
#define VIEW_LOCK_DATE "clock_date"
#define VIEW_LOCK_LEVEL "label_battery"
#define LOCK_CLOCK_Y 14
#define VIEW_LOCK_BATTERY "img_battery"
/* M1 Plus: a press held still this long on a library row opens its hold menu (ringnav_input). */
#define LONG_PRESS_MS 500
#define KEY_VOLUMEDOWN 221
#define KEY_VOLUMEUP 220
#define KEY_POWER 210
#define WM_KEY_SLEEP KEY_CENTER
#define ANIM_X_FROM 0x68
#define slide_stride(w) (slide_menu_item_width(w) + I(w, SLIDE_SPACER))
#define INITCONFIG_SPEED_RET 0x51339c /* player_initconfig's mclSetPlaySpeed call returns here */
#define SORTSELECT_BACK "img_return"
#define SORTSELECT_VIEW "scroll_view"
#define VIEW_SORTSELECT_TITLE "scrlabel_title"
#define STYLE_SORTSELECT_ROW STYLE_LISTITEM_BLACK
#define STYLE_SORTSELECT_LABEL STYLE_SCRLABEL_WHITE24L
#define ICON_SORTSELECT_CHECK "select"
#define SORTSELECT_W UI_W
#define SORTSELECT_ROW 66
#define SORTSELECT_LABEL_X 30
#define SORTSELECT_CHOICE_W (UI_W - 65)
#define SORTSELECT_LABEL_W (UI_W - 109)
#define SORTSELECT_CHECK_X (UI_W - 35)
#define SORTSELECT_CHECK_W 24
#define VIEW_BOOTVOL_SWITCH "img_bootswitch" /* in view_navbar, after the title */
#define VIEW_BOOTVOL_SWITCH_ICON "img_bootswitch"
#define VIEW_BOOTVOL "view_bootvol"
#define VIEW_BOOTVOL_SLIDER "slider_bootvol"
#define VIEW_BOOTVOL_DEC "img_dec"
#define VIEW_BOOTVOL_ADD "img_add"
#define VIEW_BOOTVOL_VALUE "label_vol"
#define ICON_SWITCH_ON "switch_on"
#define ICON_SWITCH_OFF "switch_off"
#define BT_PAIRLIST 0xa38110 /* stock pdeq_btpairlist */
#define PH_GRID_H 240
#define VIS_H 186
#define BOOK_ROWS 10
/* tidal_start: the register mcl_tidalStartPlayer's caller keeps its song id in (patch/tidal.c) */
#define TIDAL_ID_REG "$s2"
