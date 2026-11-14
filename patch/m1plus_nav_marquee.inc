/* M1 Plus: keep the 1.6.7 selected-row marquee until V2.1's global scrolling hooks are ported. */
#if M1PLUS
static int marq_poll(const void *info) {
    (void)info;
    st.marq_timer = 0;
    void *w = usable() ? surface((void *)0, (void *)0) : (void *)0;
    int i = st.sel_row;
    void *row = w && w == st.sel_w && load_rows(&g_menu, w) && i >= 0 && i < g_menu.n &&
                        g_menu.id[i] == st.marq_id
                    ? g_menu.at[i]
                    : (void *)0;
    if (!row || row != st.marq_row) {
        marq_stop();
        st.marq_row = (void *)0; /* the next paint with a selection starts over */
        return 0;
    }
    if (st.marq_label) { /* a pass and the hold after it: back to the start, for the next */
        marq_stop();
        if (++st.marq_passes < MARQUEE_PASSES)
            st.marq_timer = timer_add(marq_poll, (void *)0, MARQUEE_HOLD_MS);
        return 0;
    }
    void *label = row_scroller(row, 2);
    /* stock's two margins (2 px each by default, 0x5e8428) count towards its ellipsis */
    int over = label ? I(label, HSCROLL_TEXT_W) + 4 - I(label, W_W) : 0;
    if (over <= 0 || !((const char *)label)[HSCROLL_ONLY_FOCUS]) return 0; /* until it moves */
    unsigned ms = (unsigned)over * MARQUEE_MS / MARQUEE_PX;
    widget_set_prop_int(label, "loop", 0);
    widget_set_prop_int(label, "duration", (int)ms);
    st.marq_label = label;
    widget_on(label, EVT_DESTROY, marq_gone, (void *)0);
    hscroll_label_set_only_focus(label, 0);
    hscroll_label_start(label);
    st.marq_timer = timer_add(marq_poll, (void *)0, ms + MARQUEE_HOLD_MS);
    return 0;
}
static int marq_moved(const void *info) {
    (void)info;
    marq_stop();
    st.marq_passes = 0;
    st.marq_timer = timer_add(marq_poll, (void *)0, MARQUEE_HOLD_MS);
    return 0;
}

#endif
