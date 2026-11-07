/* M1 Plus: ringnav_input's touches: the long-press, and q2video's back chevron. patch/navigation.c includes this where it stood (docs/m1plus-roadmap.md U1c). */
#if M1PLUS
    /* A window switch can filter the held Previous's release before on_wm_keyup_fun (ringnav). Keep the
     * latch armed through stock dispatch so ringnav can spend it, then clear it even if stock filtered it. */
    if (e && I(e, EVENT_TYPE) == EVT_KEY_UP && m1_return_latch &&
        I(e, EVENT_KEY) == (g_rotate_mode == 1 ? KEY_FWD_BTN : KEY_BACK_BTN)) {
        int result = stock_input_trampoline(wm, e);
        m1_return_latch = 0;
        return result;
    }
    if (touch_closes(e) || chevron_input(e)) return 0;
    lp_input(e);
    home_input(e);
    if (e && video_on()) video_touch(e);
    if (!video_on()) {
        int result = stock_input_trampoline(wm, e);
        if (e && I(e, EVENT_TYPE) == EVT_POINTER_UP) st.lp_swallow = 0; /* its click is past */
        return result;
    }
#endif
