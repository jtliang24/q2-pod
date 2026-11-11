/* M1 Plus: the validated knob step, until the Q2 wheel follower is ported. */
#if M1PLUS
int carousel_glide(void *w, int goal, unsigned ms, int easing) {
    void *a = P(w, SLIDE_ANIMATOR);
    if (!a) {
        a = widget_animator_scroll_create(w, ms, 0, easing);
        if (a && !widget_animator_on(a, EVT_ANIM_END, home_done, w)) {
            widget_animator_destroy(a);
            a = (void *)0;
        }
        P(w, SLIDE_ANIMATOR) = a;
        if (!a) {
            int n = (int)widget_count_children(w),
                stride = slide_stride(w);
            int id = n && stride > 0 ? (I(w, SLIDE_INDEX) - goal / stride) % n : 0;
            I(w, SLIDE_OFFSET) = 0;
            slide_menu_set_value(w, id < 0 ? id + n : id);
            widget_set_focused(widget_get_child(w, I(w, SLIDE_INDEX)), 1);
            return 0;
        }
        widget_set_focused(widget_get_child(w, I(w, SLIDE_INDEX)), 0);
    }
    widget_animator_pause(a);
    widget_animator_scroll_set_params(a, I(w, SLIDE_OFFSET), 0, goal, 0);
    I(a, ANIM_ELAPSED) = I(a, ANIM_START_TIME) = 0;
    I(a, ANIM_DURATION) = ms;
    P(a, ANIM_EASING) =
        easing_get(easing); /* scroll_create's own, so a reused one takes this run's */
    widget_animator_start(a);
    return 1;
}

static void home_step(void *w, int dir, unsigned now, int jump) {
    int n = (int)widget_count_children(w);
    int stride = slide_stride(w);
    int fast =
        st.home_surface == w && st.home_dir == dir && now - st.last_home <= HOME_FAST_WINDOW_MS;
    void *a = P(w, SLIDE_ANIMATOR);
    int live = I(w, SLIDE_OFFSET);
    int goal = a ? I(a, ANIM_X_TO) : 0;
    /* Reversal discards the unfinished destination and heads to the adjacent card
     * behind the live position. Same-direction ticks extend the intended destination. */
    if (a && (goal - live) * dir > 0) {
        goal = (live / stride) * stride;
        if (dir > 0 ? goal >= live : goal <= live) goal -= dir * stride;
    } else
        goal -= dir * stride;
    unsigned letter = 0;
    int from = (I(w, SLIDE_INDEX) - goal / stride - dir) % n;
    if (from < 0) from += n;
    int steps = jump ? coverflow_jump(w, from, dir, &letter) : 1;
    goal -= dir * stride * (steps - 1);
    int to = I(w, SLIDE_INDEX) - goal / stride;
    if (coverflow_bounded(w) && (to < 0 || to >= n)) {
        goal += dir * stride * steps;
        if (a && (goal - live) * dir < 0) return; /* still arriving at the end */
        I(w, SLIDE_OFFSET) = live = goal - dir * stride / CF_BOUNCE;
    }
    st.cf_letter = letter;
    st.cf_letter_at = now;
    st.cf_letter_surface = w;
    if (letter)
        rearm(&st.cf_letter_timer, cf_letter_expire, LETTER_MS);
    else
        stop_timer(&st.cf_letter_timer);
    if (!carousel_glide(w, goal, fast ? HOME_FAST_SLIDE_MS : HOME_SLIDE_MS, SLIDE_EASING)) {
        st.home_surface = (void *)0;
        return;
    }
    st.home_surface = w;
    st.last_home = now;
    st.home_dir = dir;
}
#endif
