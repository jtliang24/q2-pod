/* M1 Plus: a page's title-bar back button, pressed by Previous in Knob: Navigation. patch/navigation.c includes this where it stood (docs/m1plus-roadmap.md U1c). */
#if M1PLUS
/* A page's title-bar back button: V2.1's, which each page's init makes in navbar_btnreturn_style
 * with on_back_onclick as its click (its pages take no Return). The first one showing, depth first.
 * A widget with no style reads NULL, not the default (value_str of a NULL string). The payload's own
 * pages have none: the status bar's chevron (previous_back) closes them with a Return. A settings page's
 * navigationbar_view (each slide's, numbered, on a slide page) is hidden and disabled by the iPod rewrite
 * (ipod-ui 4.3, ipod.settings_page), its button still enabled: it is searched, as the page's one back. */
static void *back_of(void *w, int depth) {
    if (!w || depth > 8 ||
        (!widget_get_visible(w) &&
         !tk_str_start_with(widget_get_prop_str(w, "name", ""), "navigationbar_view")))
        return (void *)0;
    const char *style =
        !tk_strcmp(widget_get_type(w), "button") ? widget_get_prop_str(w, "style", "") : 0;
    if (style && !tk_strcmp(style, STYLE_NAVBAR_RETURN)) return w;
    for (unsigned i = 0, n = widget_count_children(w); i < n; i++) {
        void *found = back_of(widget_get_child(w, i), depth + 1);
        if (found) return found;
    }
    return (void *)0;
}
static int keyboard(void *w) { return w && !tk_strcmp(widget_get_type(w), "keyboard"); }
/* The top window, or under AWTK's input-method keyboard (a kb_* window over the page whose edit has the focus, as on
 * HiFi Music's login) the window it types into: Back is that page's, not a Return in the keyboard, which only moves the
 * focus to the next edit. */
static void *back_window(void) {
    void *wm = window_manager(), *top = window_manager_get_top_window(wm);
    if (!keyboard(top)) return top;
    int under = 0; /* past the keyboard, down the window manager's children */
    for (unsigned i = widget_count_children(wm); i-- > 0;) {
        void *w = widget_get_child(wm, i);
        if (under && !keyboard(w)) return w;
        under |= w == top;
    }
    return top;
}
/* Back, from Previous in Knob: Navigation (after its key's dispatch: the click closes the page) and from the
 * status bar's chevron: the top page's back button, clicked; else a dialog closes, as its tap outside does; else a
 * payload page (Coverflow, Photos, Books, Radio, Spotify, the PEQ, the QR page) takes a Return, which its key-up
 * handler turns into a close or a step back a screen. Home's back is its Settings list's, to the menu it opened from
 * (coverflow_home_back); Home itself has none. */
static int previous_back(const void *info) {
    (void)info;
    /* The hold menu has no back button: Previous closes it as OK does */
    if (st.qm_dialog && window_manager_get_top_window(window_manager()) == st.qm_dialog) {
        qm_close();
        return 0;
    }
    void *top = back_window(), *button = back_of(top, 0);
    if (coverflow_home_back(top)) return 0;
    char click[0x30];
    if (button && widget_get_prop_bool(button, "enable", 1))
        stock_dispatch_trampoline(button, pointer_event_init(click, EVT_CLICK, button, 0, 0));
    /* A V2.1 dialog without one (Now Playing's ⋯ menu and its queue) closes, as its tap outside does:
     * the queue's own close is navigator_back (dialog_playqueue_dialog_init). */
    else if (!button && top && !tk_strcmp(widget_get_type(top), "dialog"))
        navigator_back();
    else if (!button && top && !peq_back(top) && !home_menu(top))
        dispatch_key_return();
    return 0; /* not RET_REPEAT: one shot */
}

/* The status bar's back chevron (img_back, the left BAR_BACK_W of the bar): shown while the top window is not Home
 * (chevron_sync). Its tap area is BAR_BACK_HIT_W wide, the bar's height, and in Minimal SET_TOP into the page, the gap
 * above a settings list's first row (Classic's lists sit flush under the bar). A press there belongs to it, release
 * included: the window manager gives no other window the pointer, and the tap, made when the finger lifts inside that
 * area, is previous_back. Nothing else sees either event.
 * Now Playing's pages hide it for their own back, under the bar (NP_TOP_H tall): there the same area runs from the
 * screen's top to that row's foot, a press in it goes Back through the page's button (previous_back), and its hold is
 * the chevron's. Only those pages reach so low: Folder's first row starts inside it. */
/* Hold Return by touch (ipod-ui 4.4): the chevron held LONG_PRESS_MS, as a row's hold (lp_input), opens Now Playing
 * as Previous's hold does (hold_previous), in either Knob mode; its release is then spent. */
static int chevron_hold(const void *unused) {
    (void)unused;
    st.chev_timer = 0;
    /* The chevron owns the press before stock dispatch, so AWTK never sets its pointer-pressed flag. */
    if (!st.chev_down) return 0;
    st.chev_held = 1;
    compact_now_playing();
    return 0; /* RET_REMOVE */
}
static int chevron_np_corner(void) {
    void *top = window_manager_get_top_window(window_manager());
    return usable() && top && (top == st.np_win || spot_page(top));
}
static int chevron_input(void *e) {
    if (!e || !st.bar_back) return 0;
    unsigned type = (unsigned)I(e, EVENT_TYPE);
    if (type == EVT_POINTER_ABORT) {
        int owned = st.chev_down;
        stop_timer(&st.chev_timer);
        st.chev_down = st.chev_held = 0;
        return owned;
    }
    if (type != EVT_INPUT_POINTER_DOWN && type != EVT_INPUT_POINTER_MOVE && type != EVT_POINTER_UP) return 0;
    int x = I(e, EVENT_X), y = I(e, EVENT_Y);
    int corner = chevron_np_corner();
    int in = x < BAR_BACK_HIT_W && y < STATUS_H + (corner ? NP_TOP_H : theme()->set_top);
    if (type == EVT_INPUT_POINTER_DOWN) {
        stop_timer(&st.chev_timer);
        st.chev_held = 0;
        st.chev_down = in && (corner || widget_get_visible(st.bar_back));
        st.chev_x = x;
        st.chev_y = y;
        if (st.chev_down) rearm(&st.chev_timer, chevron_hold, LONG_PRESS_MS);
    }
    if (!st.chev_down) return 0;
    int dx = x - st.chev_x, dy = y - st.chev_y; /* a drag is no hold, as a row's (lp_input) */
    if (type == EVT_INPUT_POINTER_MOVE &&
        (dx >= PULL_CLAIM_PX || -dx >= PULL_CLAIM_PX || dy >= PULL_CLAIM_PX || -dy >= PULL_CLAIM_PX))
        stop_timer(&st.chev_timer);
    if (type == EVT_POINTER_UP) {
        stop_timer(&st.chev_timer);
        st.chev_down = 0;
        if (in && !st.chev_held) timer_add(previous_back, (void *)0, 0); /* not inside the dispatch that closes the page */
        st.chev_held = 0;
    }
    return 1;
}

/* The status bar's play state is a Play/Pause button (ipod-ui 4.2), over BAR_PLAY_HIT_W round the icon wherever the right
 * group has put it, the bar's height, only while the bar shows it and takes the touch: no dark or locked screen, dialog
 * or full-screen page, which all have that press for themselves. V2.1 keeps the press and its moves, so a pull down from
 * here still opens its dropdown (on_wm_tsmove_fun); only the lift's x changes, out of the x 80 to 270 where on_wm_tsup_fun
 * opens the VOLUME page, which still resets the power timers. A still tap is the Play key itself, so it follows whichever
 * player the key does; a drag is nothing. The rest of the bar keeps VOLUME, but not on the lock screen, which V2.1's
 * handler doesn't check: there a lift from a press in the bar changes as the icon's does. A press from lower down is the
 * lock screen's own gesture, its lift left alone. */
static int bar_play_key(const void *unused) {
    (void)unused;
    dispatch_key(KEY_PLAY);
    return 0;
}
static int bar_play_hit(int x, int y) {
    void *wm = window_manager(), *top = window_manager_get_top_window(wm);
    if (y >= STATUS_H || !st.bar_state || !widget_get_visible(st.bar_state) || !usable() || !top || video_on() ||
        window_manager_is_animating(wm) || tk_strcmp(widget_get_type(top), "window") ||
        widget_get_prop_bool(top, "fullscreen", 0))
        return 0;
    int left = I(P(st.bar_state, W_PARENT), W_X) + I(st.bar_state, W_X) + I(st.bar_state, W_W) / 2 - BAR_PLAY_HIT_W / 2;
    return x >= left && x < left + BAR_PLAY_HIT_W;
}
static void bar_play_input(void *e) {
    unsigned type = e ? (unsigned)I(e, EVENT_TYPE) : 0;
    if (type == EVT_INPUT_POINTER_DOWN) {
        st.bar_play_x = I(e, EVENT_X);
        st.bar_play_y = I(e, EVENT_Y);
        st.bar_play_down = bar_play_hit(st.bar_play_x, st.bar_play_y);
    } else if (type == EVT_POINTER_ABORT)
        st.bar_play_down = 0;
    if (type == EVT_POINTER_UP && g_lockscreen_pageflag && st.bar_play_y < STATUS_H && I(e, EVENT_Y) < STATUS_H)
        I(e, EVENT_X) = 0;
    if (!st.bar_play_down || (type != EVT_INPUT_POINTER_MOVE && type != EVT_POINTER_UP)) return;
    int dx = I(e, EVENT_X) - st.bar_play_x, dy = I(e, EVENT_Y) - st.bar_play_y;
    if (dx >= PULL_CLAIM_PX || -dx >= PULL_CLAIM_PX || dy >= PULL_CLAIM_PX || -dy >= PULL_CLAIM_PX)
        st.bar_play_down = 2;
    if (type != EVT_POINTER_UP) return;
    if (st.bar_play_down == 1) timer_add(bar_play_key, (void *)0, 0); /* not inside this pointer's dispatch */
    st.bar_play_down = 0;
    I(e, EVENT_X) = 0;
}

/* A press takes AWTK's key target for the window under it (widget_on_pointer_down_children: at the window manager, any
 * window), the bar's as much as a page's, and only another press moves it. So after a tap in the bar every key went to
 * the bar: a payload page's Return (previous_back) and its other keys never reached its key-up handler, and Back and
 * Previous did nothing until the page was tapped. The press ends here, so the page has its keys back. VOLUME's dialog
 * takes the target itself and returns it on closing; this leaves it to do so. */
static void bar_key_target(void *e) {
    unsigned type = e ? (unsigned)I(e, EVENT_TYPE) : 0;
    if (type != EVT_POINTER_UP && type != EVT_POINTER_ABORT) return;
    void *bar = *(void *const *)system_bar;
    if (bar && P(window_manager(), W_KEY_TARGET) == bar) widget_set_focused(back_window(), 1);
}

/* Display's Knob: Navigation. The knob's turns are Previous and Next (volume up is Previous, up the
 * list, unless Knob Up: List Down) and its press Centre, on their release, which is where V2.1
 * changes the volume (on_wm_keyup_fun opens the volume dialog for 220/221); V2.1 binds no key-down
 * handler. Only where ringnav navigates: elsewhere the turn would do nothing, so Now Playing, the
 * volume dialog, Bluetooth receiver and USB DAC modes (their pages are no context, and usable()
 * leaves both modes to stock) and a dark screen keep the volume. Now Playing's press is the scrub's
 * (m1plus_nav_np.c), taken before V2.1's key-up. */
static int knob_gate(void) {
    pod_settings();
    /* Bluetooth receiver mode keeps the knob's volume: usable() no longer refuses it (1.3.8, the
     * Q2's wheel navigates the gear's Audio settings there). */
    return st.knob_mode && usable() && !now_playing() && !bt__recv_pageflag;
}
static int knob_nav_active(void) {
    return knob_gate() && allowed_top(window_manager_get_top_window(window_manager()));
}
int ringnav_knob_nav(void) { return knob_nav_active(); }
/* Previous is Back wherever ringnav navigates, and on V2.1's pages that keep the knob's volume but have a back
 * button: its sliders (Channel Balance, Startup and Max Volume, Brightness, Bluetooth volume, and the payload's
 * Crossfade, on Startup Volume's page) and the lock screen's About. On V039m Previous stayed a media key there.
 * Now Playing's enlarged art and Spotify's page, with its own back, keep it a media key, as Now Playing does. */
static int knob_back_active(void) {
    if (!knob_gate()) return 0;
    void *top = back_window(); /* a page under the keyboard too */
    return allowed_top(top) ||
           (back_of(top, 0) && tk_strcmp(widget_get_prop_str(top, "name", ""), "bigcover_page") &&
            tk_strcmp(widget_get_prop_str(top, "name", ""), "spotify_page"));
}
/* Hold Return (ipod-ui 4.4): Previous held wherever it is Back (knob_back_active), V2.1's key-long for it (AWTK's,
 * after 1000 ms: HOLD_KEYS is Q2 only), opens Now Playing, as Return's hold does on the Q2 (or goes Home, with Hold
 * Return: Home). Home keeps Previous a track key but on its Settings list, and Now Playing V2.1's own hold. The latch spends its release
 * (m1plus_nav_knob.inc), which would go back. */
static int hold_previous(unsigned key) {
    void *top = window_manager_get_top_window(window_manager());
    if (key != (g_rotate_mode == 1 ? KEY_FWD_BTN : KEY_BACK_BTN) || !top || !knob_back_active() ||
        (home_menu(top) && !coverflow_home_sets(top)) ||
        !tk_strcmp(widget_get_prop_str(top, "name", ""), "playing_page"))
        return 0;
    compact_now_playing();
    m1_return_latch = 1;
    return 1;
}
#endif
#include "m1plus_nav_np.c"
