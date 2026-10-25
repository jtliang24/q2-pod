/* M1 Plus: a page's title-bar back button, pressed by Previous in Knob: Navigation. patch/navigation.c includes this where it stood (docs/m1plus-roadmap.md U1c). */
#if M1PLUS
/* A page's title-bar back button: V2.1's, which each page's init makes in navbar_btnreturn_style
 * with on_back_onclick as its click (its pages take no Return), or the payload's (back_button, the
 * same style, a Return). The first one showing, depth first. A widget with no style reads NULL, not
 * the default (value_str of a NULL string). */
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
/* Previous as Back, after its key's dispatch (the click closes the page): the top page's back
 * button, clicked. */
static int previous_back(const void *info) {
    (void)info;
    /* The hold menu has no back button: Previous closes it as OK does */
    if (st.qm_dialog && window_manager_get_top_window(window_manager()) == st.qm_dialog) {
        qm_close();
        return 0;
    }
    void *button = back_of(window_manager_get_top_window(window_manager()), 0);
    char click[0x30];
    if (button && widget_get_prop_bool(button, "enable", 1))
        stock_dispatch_trampoline(button, pointer_event_init(click, EVT_CLICK, button, 0, 0));
    return 0; /* not RET_REPEAT: one shot */
}

/* Display's Knob: Navigation. The knob's turns are Previous and Next (volume up is Previous, up the
 * list, unless Knob Up: List Down) and its press Centre, on their release, which is where V2.1
 * changes the volume (on_wm_keyup_fun opens the volume dialog for 220/221); V2.1 binds no key-down
 * handler. Only where ringnav navigates: elsewhere the turn would do nothing, so Now Playing, the
 * volume dialog, Bluetooth receiver and USB DAC modes (their pages are no context, and usable()
 * leaves both modes to stock) and a dark screen keep the volume. */
static int knob_nav_active(void) {
    pod_settings();
    /* Bluetooth receiver mode keeps the knob's volume: usable() no longer refuses it (1.3.8, the
     * Q2's wheel navigates the gear's Audio settings there). */
    if (!st.knob_mode || !usable() || now_playing() || bt__recv_pageflag) return 0;
    return allowed_top(window_manager_get_top_window(window_manager()));
}
#endif
#include "m1plus_nav_home.c"
