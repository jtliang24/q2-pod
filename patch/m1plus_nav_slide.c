/* M1 Plus: a finger on a carousel (Coverflow's covers, the photo viewer). patch/navigation.c includes this where it stood (docs/m1plus-roadmap.md U1c). */
#if M1PLUS
#define FLICK_MS 300 /* a drag released this soon after the press moves at least one item */

static int floor_div(int a, int b) { return a / b - (a % b < 0); } /* b > 0 */

/* The offset nearest live that leaves a whole item centred and, bounded, a real one (index i of
 * n, committed as i - offset / stride). */
static int slide_snap(int live, int stride, int i, int n, int bounded) {
    int goal = floor_div(2 * live + stride, 2 * stride) * stride;
    if (bounded && goal > i * stride) goal = i * stride;
    if (bounded && goal < (i - n + 1) * stride) goal = (i - n + 1) * stride;
    return goal;
}

/* The carousel s from offset live to goal, through the knob's animator (home_done commits
 * index - goal / stride); straight there without one. */
static void slide_settle(void *s, int live, int goal) {
    void *a = P(s, SLIDE_ANIMATOR);
    int i = I(s, SLIDE_INDEX), n = (int)widget_count_children(s), stride = slide_stride(s);
    I(s, SLIDE_OFFSET) = live;
    if (!a) {
        a = widget_animator_scroll_create(s, HOME_SLIDE_MS, 0, SLIDE_EASING);
        if (a && !widget_animator_on(a, EVT_ANIM_END, home_done, s)) {
            widget_animator_destroy(a);
            a = (void *)0;
        }
        P(s, SLIDE_ANIMATOR) = a;
        if (!a) {
            I(s, SLIDE_OFFSET) = 0;
            slide_menu_set_value(s, ((i - goal / stride) % n + n) % n);
            widget_invalidate_force(s, 0);
            return;
        }
        widget_set_focused(widget_get_child(s, i), 0);
    }
    widget_animator_pause(a);
    widget_animator_scroll_set_params(a, live, 0, goal, 0);
    I(a, ANIM_ELAPSED) = I(a, ANIM_START_TIME) = 0;
    I(a, ANIM_DURATION) = HOME_SLIDE_MS;
    widget_animator_start(a);
}

/* k items on from the one at rest, as a tap on a side cover: Coverflow's touch. */
void slide_step(void *s, int k, int bounded) {
    int stride = slide_stride(s), n = (int)widget_count_children(s);
    if (stride <= 0 || !n || P(s, SLIDE_ANIMATOR)) return;
    slide_settle(s, 0, slide_snap(-k * stride, stride, I(s, SLIDE_INDEX), n, bounded));
}

/* A finger on a carousel the payload paints over an insensitive slide_menu: Coverflow's covers
 * and the photo viewer, whose view passes its pointer events here. V2.1's slide_menu steps by its
 * own height (260 and 450 px), wider than an item as painted, so its own drag would lag the finger
 * and a swipe would have to cross more than the screen. Here the finger moves the offset a stride
 * per px, an item as painted; the release settles on the nearest item, or the next for a flick. A
 * press on a moving carousel catches it, and px 0 on the press is one the carousel doesn't take
 * (the back button's). Returns 1 on the release of a tap, a press that neither moved nor caught
 * anything. */
int slide_swipe(void *s, void *e, int px, int bounded) {
    unsigned type = (unsigned)I(e, EVENT_TYPE), now = time_now_ms();
    int x = I(e, EVENT_X), stride = slide_stride(s), n = (int)widget_count_children(s);
    void *a = P(s, SLIDE_ANIMATOR);
    if (type == EVT_INPUT_POINTER_DOWN) {
        st.sw_slide = px > 0 ? s : (void *)0;
        if (!st.sw_slide) return 0;
        if (a) widget_animator_pause(a);
        st.sw_px = px;
        st.sw_x = x;
        st.sw_at = now;
        st.sw_live = I(s, SLIDE_OFFSET);
        st.sw_drag = 0;
        return 0;
    }
    if (s != st.sw_slide || stride <= 0 || !n) return 0;
    int dx = x - st.sw_x, i = I(s, SLIDE_INDEX);
    if (dx >= PULL_CLAIM_PX || -dx >= PULL_CLAIM_PX) st.sw_drag = 1;
    int live = st.sw_drag ? st.sw_live + dx * stride / st.sw_px : I(s, SLIDE_OFFSET);
    if (bounded) { /* past an end by at most the knob's bounce */
        int hi = i * stride + stride / CF_BOUNCE, lo = (i - n + 1) * stride - stride / CF_BOUNCE;
        live = live > hi ? hi : live < lo ? lo : live;
    }
    if (type == EVT_INPUT_POINTER_MOVE) {
        if (st.sw_drag && live != I(s, SLIDE_OFFSET)) {
            I(s, SLIDE_OFFSET) = live;
            widget_invalidate_force(s, 0);
        }
        return 0;
    }
    if (type != EVT_POINTER_UP && type != EVT_POINTER_ABORT) return 0;
    st.sw_slide = (void *)0;
    if (!st.sw_drag && !a) return type == EVT_POINTER_UP;
    int goal = st.sw_drag || !a ? slide_snap(live, stride, i, n, bounded) : I(a, ANIM_X_TO);
    if (st.sw_drag && type == EVT_POINTER_UP && now - st.sw_at < FLICK_MS &&
        goal == slide_snap(st.sw_live, stride, i, n, bounded))
        goal = slide_snap(goal + (dx > 0 ? stride : -stride), stride, i, n, bounded);
    slide_settle(s, live, goal);
    return 0;
}
#endif
