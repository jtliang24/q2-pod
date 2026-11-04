/* M1 Plus: a page's title-bar back button, pressed by Previous in Knob: Navigation. patch/navigation.c includes this where it stood (docs/m1plus-roadmap.md U1c). */
#if M1PLUS
/* A page's title-bar back button: V2.1's, which each page's init makes in navbar_btnreturn_style
 * with on_back_onclick as its click (its pages take no Return). The first one showing, depth first.
 * A widget with no style reads NULL, not the default (value_str of a NULL string). The payload's own
 * pages have none: the status bar's chevron (previous_back) closes them with a Return. */
static void *back_of(void *w, int depth) {
    if (!w || depth > 8 || !widget_get_visible(w)) return (void *)0;
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
 * handler turns into a close or a step back a screen. Home has no back. */
static int previous_back(const void *info) {
    (void)info;
    /* The hold menu has no back button: Previous closes it as OK does */
    if (st.qm_dialog && window_manager_get_top_window(window_manager()) == st.qm_dialog) {
        qm_close();
        return 0;
    }
    void *top = window_manager_get_top_window(window_manager()), *button = back_of(top, 0);
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
 * (chevron_sync). Its press and release belong to it: the window manager gives no other window the pointer, and the
 * tap, made when the finger lifts inside the chevron, is previous_back. Nothing else sees either event. */
static int chevron_input(void *e) {
    if (!e || !st.bar_back) return 0;
    unsigned type = (unsigned)I(e, EVENT_TYPE);
    if (type != EVT_INPUT_POINTER_DOWN && type != EVT_INPUT_POINTER_MOVE && type != EVT_POINTER_UP) return 0;
    int in = I(e, EVENT_X) < BAR_BACK_W && I(e, EVENT_Y) < STATUS_H;
    if (type == EVT_INPUT_POINTER_DOWN) st.chev_down = in && widget_get_visible(st.bar_back);
    if (!st.chev_down) return 0;
    if (type == EVT_POINTER_UP) {
        st.chev_down = 0;
        if (in) timer_add(previous_back, (void *)0, 0); /* not inside the dispatch that closes the page */
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
static int knob_nav_active(void) {
    pod_settings();
    /* Bluetooth receiver mode keeps the knob's volume: usable() no longer refuses it (1.3.8, the
     * Q2's wheel navigates the gear's Audio settings there). */
    if (!st.knob_mode || !usable() || now_playing() || bt__recv_pageflag) return 0;
    return allowed_top(window_manager_get_top_window(window_manager()));
}
#endif
#include "m1plus_nav_home.c"
#include "m1plus_nav_np.c"
