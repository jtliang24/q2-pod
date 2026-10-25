/* M1 Plus: Knob: Navigation on V2.1's Home grid. patch/m1plus_nav_back.c includes this (docs/m1plus-roadmap.md section 7). */
#if M1PLUS
/* V2.1's Home is a slide_view (home_sview) of pages of up to HOME_CARDS cards, each a view holding
 * its clickable image and its label (0x534064, 0x533d8c; the Q2 Pod card is laid out the same,
 * home_card). None of it is a pane ringnav moves through, so in Knob: Navigation the knob's turns
 * step a focus through the cards in reading order, page by page, the slide_view following to the
 * focused card's page, and its press clicks the card's image: V2.1's card click (0x533b80) or the
 * Q2 Pod card's. The lists' frame shows the focus; a touch hides it, and the next turn shows it on
 * the first card of the page in view. Previous stays Previous track on Home (m1plus_nav_knob.inc). */
#define HOME_MAX 24 /* V2.1's 18 cards and the Q2 Pod card, with room */

/* Home's cards in reading order, each with its page's index; their count. */
static unsigned home_cards(void *slides, void **cards, unsigned char *pages) {
    unsigned n = 0;
    for (unsigned p = 0, np = widget_count_children(slides); p < np; p++) {
        void *page = widget_get_child(slides, p);
        for (unsigned c = 0, nc = widget_count_children(page); c < nc && n < HOME_MAX; c++) {
            pages[n] = (unsigned char)p;
            cards[n++] = widget_get_child(page, c);
        }
    }
    return n;
}

static void *home_slides(void *top) {
    return home_menu(top) ? widget_lookup(top, VIEW_HOME_SLIDES, 1) : (void *)0;
}

/* The card's image: the first child that isn't its label. */
static void *home_image(void *card) {
    for (unsigned i = 0, n = widget_count_children(card); i < n; i++) {
        void *w = widget_get_child(card, i);
        if (tk_strcmp(widget_get_type(w), "label")) return w;
    }
    return (void *)0;
}

/* The focused card, if Home's grid still holds it where it was focused: a rebuild (the Home
 * editor, a language change) makes new cards and drops the focus. */
static int home_focus(void *slides, void **cards, unsigned char *pages, unsigned *n) {
    *n = slides ? home_cards(slides, cards, pages) : 0;
    int at = st.home_at - 1;
    return at >= 0 && at < (int)*n && cards[at] == st.home_card ? at : -1;
}

static void home_show(void *slides, void *card, int at, unsigned page) {
    st.home_at = at + 1;
    st.home_card = card;
    if ((unsigned)widget_get_prop_int(slides, "active", 0) != page)
        slide_view_set_active_ex(slides, page, 1);
    widget_invalidate_force(slides, (void *)0);
}

/* A turn steps the focus, the first showing it on the page in view; at the first and last card a
 * turn stops, and one after a pause of EDGE_PAUSE_MS wraps, as the lists' end detent. Centre clicks
 * the focused card. Returns whether it took the key. */
static int home_key(void *top, unsigned key) {
    if ((key != KEY_PREV && key != KEY_NEXT && key != KEY_CENTER) || !knob_nav_active() ||
        window_manager_is_animating(window_manager()))
        return 0;
    void *slides = home_slides(top), *cards[HOME_MAX];
    unsigned char pages[HOME_MAX];
    unsigned n;
    int at = home_focus(slides, cards, pages, &n);
    if (!n) return 0;
    if (key == KEY_CENTER) {
        void *image = at >= 0 ? home_image(cards[at]) : (void *)0;
        if (!image) return 0;
        char click[0x30];
        stock_dispatch_trampoline(image, pointer_event_init(click, EVT_CLICK, image, 0, 0));
        return 1;
    }
    int dir = key == KEY_NEXT ? 1 : -1;
    unsigned now = (unsigned)time_now_ms();
    if (at < 0) {
        unsigned active = (unsigned)widget_get_prop_int(slides, "active", 0);
        for (at = 0; at < (int)n - 1 && pages[at] < active; at++) {}
        st.home_edge_dir = 0;
    } else if (at + dir < 0 || at + dir >= (int)n) {
        if (st.home_edge_dir != dir || now - st.home_edge_at < EDGE_PAUSE_MS) {
            st.home_edge_dir = dir; /* every stopped detent re-arms: a spin stops at the end */
            st.home_edge_at = now;
            return 1;
        }
        at = dir > 0 ? 0 : (int)n - 1;
        st.home_edge_dir = 0;
    } else {
        at += dir;
        st.home_edge_dir = 0;
    }
    home_show(slides, cards[at], at, pages[at]);
    return 1;
}

/* A touch on Home hides the focus. */
static void home_input(void *e) {
    if (!st.home_at || !e || I(e, EVENT_TYPE) != EVT_INPUT_POINTER_DOWN) return;
    void *slides = home_slides(window_manager_get_top_window(window_manager()));
    if (!slides) return;
    st.home_at = 0;
    st.home_card = (void *)0;
    widget_invalidate_force(slides, (void *)0);
}

/* The focused card's frame, the lists' (paint_selection): a fill and two one-pixel rounded
 * strokes, shade outside and white inside, inset from the card's edges. */
static void home_paint(void *w, void *canvas) {
    if (!st.home_at || !w || w != st.home_card || !canvas || !P(canvas, CANVAS_LCD)) return;
    void *slides = home_slides(window_manager_get_top_window(window_manager()));
    if (!slides || P(P(w, W_PARENT), W_PARENT) != slides) return;
    void *lcd = P(canvas, CANVAS_LCD);
    unsigned fill_color = (unsigned)I(lcd, LCD_FILL_COLOR);
    unsigned stroke_color = (unsigned)I(lcd, LCD_STROKE_COLOR);
    rect_t outer = { HOME_FRAME_INSET, HOME_FRAME_INSET, I(w, W_W) - 2 * HOME_FRAME_INSET,
                     I(w, W_H) - 2 * HOME_FRAME_INSET };
    rect_t inner = { outer.x + 1, outer.y + 1, outer.w - 2, outer.h - 2 };
    if (outer.w <= 2 * RADIUS || outer.h <= 2 * RADIUS) return;
    unsigned fill = FILL_COLOR, shade = SHADE_COLOR, white = OUTLINE_COLOR;
    canvas_fill_rounded_rect(canvas, &outer, (void *)0, &fill, RADIUS);
    int drawn = canvas_stroke_rounded_rect(canvas, &outer, (void *)0, &shade, RADIUS, 1) == 0 &&
                canvas_stroke_rounded_rect(canvas, &inner, (void *)0, &white, RADIUS - 1, 1) == 0;
    if (!drawn) {
        canvas_set_stroke_color(canvas, SHADE_COLOR);
        canvas_stroke_rect(canvas, outer.x, outer.y, outer.w, outer.h);
        canvas_set_stroke_color(canvas, OUTLINE_COLOR);
        canvas_stroke_rect(canvas, inner.x, inner.y, inner.w, inner.h);
    }
    canvas_set_fill_color(canvas, fill_color);
    canvas_set_stroke_color(canvas, stroke_color);
}
#endif
