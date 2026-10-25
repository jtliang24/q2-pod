/* M1 Plus: ringnav_input's touches: the long-press, and q2video's back chevron. patch/navigation.c includes this where it stood (docs/m1plus-roadmap.md U1c). */
#if M1PLUS
    lp_input(e);
    home_input(e);
    if (e && video_on()) video_touch(e);
    if (!video_on()) {
        int result = stock_input_trampoline(wm, e);
        if (e && I(e, EVENT_TYPE) == EVT_POINTER_UP) st.lp_swallow = 0; /* its click is past */
        return result;
    }
#endif
