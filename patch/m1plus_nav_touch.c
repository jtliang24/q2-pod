/* M1 Plus: Return synthesis, and the touch long-press that opens a row's hold menu. patch/navigation.c includes this where it stood (docs/m1plus-roadmap.md U1c). */
#if M1PLUS
/* A Return press and release, as the input thread queues a key's (the window manager drops a
 * release whose press it never saw: input_device_status). */
void dispatch_key_return(void) {
    unsigned ev[12] = { 0 };
    ev[1] = sizeof ev; /* event_t's size */
    ev[EVENT_KEY / 4] = KEY_RETURN;
    ev[EVENT_TYPE / 4] = EVT_KEY_DOWN;
    stock_input_trampoline(window_manager(), (void *)ev);
    ev[EVENT_TYPE / 4] = EVT_KEY_UP;
    stock_input_trampoline(window_manager(), (void *)ev);
}

/* Touch long-press: a press held still LONG_PRESS_MS on a row or tile of a library page opens
 * that row's hold menu, as Play/Pause held on a highlighted row does (qm_hold takes the row under
 * the finger). The native press is aborted, as a claimed pull is (pull_event), and the release's
 * click swallowed, so the row doesn't open as well. A press that moves is the list's scroll. */
/* Internet Radio's stations and Spotify's tracks: their holds (radio_hold, spot_hold) take the
 * highlighted row, as Play/Pause held does, so the row under the finger is highlighted first. */
static int lp_select(void *top) {
    const char *name = widget_get_prop_str(top, "name", "");
    if (tk_strcmp(name, "radio_page") && tk_strcmp(name, "spotbrowse_page")) return 0;
    void *w = surface_under(top, (void *)0, (void *)0, 0);
    int cur = w && load(&g_menu, w, 0) && g_menu.kind == 1 ? lp_entry(&g_menu) : -1;
    if (cur < 0) return 0;
    ringnav_select(w, g_menu.id[cur], g_menu.rows);
    return 1;
}

/* The pages a hold can act on: V2.1's library pages, the payload's track lists (Most Played,
 * Ratings' and Long Songs', Coverflow's tracks), Coverflow's covers, the stations and the tracks. */
static int lp_page(void *top) {
    const char *name = top ? widget_get_prop_str(top, "name", "") : "";
    int ctx = top ? context_id(name) : -1;
    return ctx >= 0 && (contexts[ctx].kind >= CTX_FOLDER || page_tracks(top) || coverflow_album(top) ||
                        !tk_strcmp(name, "radio_page") || !tk_strcmp(name, "spotbrowse_page"));
}

static int lp_fire(const void *unused) {
    (void)unused;
    st.lp_timer = 0;
    void *wm = window_manager(), *top = window_manager_get_top_window(wm);
    if (!top || top != st.lp_top || !window_manager_get_pointer_pressed(wm)) return 0;
    st.lp_touch = 1;
    const char *fav = (void *)0;
    int taken = lp_select(top) && ((fav = radio_hold(top)) || spot_hold(top));
    if (fav) toast(fav);
    if (!taken) taken = qm_hold();
    st.lp_touch = 0;
    if (!taken) return 0;
    st.lp_swallow = 1;
    unsigned abort_event[12];
    pointer_event_init(abort_event, EVT_POINTER_ABORT, top, st.lp_x, st.lp_y);
    widget_dispatch_event_to_target_recursive(top, abort_event);
    return 0; /* RET_REMOVE */
}

static void lp_input(void *e) {
    unsigned type = e ? (unsigned)I(e, EVENT_TYPE) : 0;
    if (type == EVT_INPUT_POINTER_DOWN) {
        st.lp_swallow = 0;
        stop_timer(&st.lp_timer);
        void *top = window_manager_get_top_window(window_manager());
        if (!lp_page(top)) return;
        st.lp_top = top;
        st.lp_x = I(e, EVENT_X);
        st.lp_y = I(e, EVENT_Y);
        rearm(&st.lp_timer, lp_fire, LONG_PRESS_MS);
    } else if (st.lp_timer && type == EVT_INPUT_POINTER_MOVE) {
        int dx = I(e, EVENT_X) - st.lp_x, dy = I(e, EVENT_Y) - st.lp_y;
        if (dx >= PULL_CLAIM_PX || -dx >= PULL_CLAIM_PX || dy >= PULL_CLAIM_PX || -dy >= PULL_CLAIM_PX)
            stop_timer(&st.lp_timer);
    } else if (type == EVT_POINTER_UP)
        stop_timer(&st.lp_timer);
}
#endif
