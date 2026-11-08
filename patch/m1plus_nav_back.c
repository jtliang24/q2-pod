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
    void *top = window_manager_get_top_window(window_manager()), *button = back_of(top, 0);
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
 * area, is previous_back. Nothing else sees either event. */
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
    int in = x < BAR_BACK_HIT_W && y < STATUS_H + (ipod_classic() ? 0 : SET_TOP);
    if (type == EVT_INPUT_POINTER_DOWN) {
        stop_timer(&st.chev_timer);
        st.chev_held = 0;
        st.chev_down = in && widget_get_visible(st.bar_back);
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
 * Now Playing's enlarged art keeps it a media key, as Now Playing does. */
static int knob_back_active(void) {
    if (!knob_gate()) return 0;
    void *top = window_manager_get_top_window(window_manager());
    return allowed_top(top) ||
           (back_of(top, 0) && tk_strcmp(widget_get_prop_str(top, "name", ""), "bigcover_page"));
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
