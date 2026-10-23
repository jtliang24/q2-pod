/* M1 Plus: the Q2 Pod card on V2.1's Home grid. patch/coverflow.c includes this where it stood (docs/m1plus-roadmap.md U1c). */
#if M1PLUS
extern int library_open(void *ctx, void *event); /* navigation.c: the Q2 Pod page */

/* The Q2 Pod card: after V2.1's own, in the next slot of its Home grid, laid out as its builder lays
 * out its cards (0x533d8c), on a new page when the last is full. The image has no name, so V2.1's
 * card click (0x533b80, atoi of the name) never sees it; its own opens the Q2 Pod page. A rebuild of
 * the grid (Home menu edited, language changed) destroys it with V2.1's cards, and home_card_again
 * puts it back. Nothing is added when the grid isn't as V2.1 builds it. */
static void home_card(void *win) {
    void *slides = win ? widget_lookup(win, VIEW_HOME_SLIDES, 1) : (void *)0;
    void *dots = win ? widget_lookup(win, VIEW_HOME_DOTS, 1) : (void *)0;
    void *menu = P(pdeq_choicemenu, 0);
    if (!slides || !dots || !menu || widget_lookup(slides, "q2pod_card", 1)) return;
    unsigned n = deque_size(menu), pages = widget_count_children(slides), slot = n % HOME_CARDS;
    if (pages != (n + HOME_CARDS - 1) / HOME_CARDS) return;
    void *page = slot ? widget_get_child(slides, pages - 1) : (void *)0;
    if (!page) {
        page = view_create(slides, 0, 0, HOME_PAGE_W, HOME_PAGE_H);
        slide_indicator_set_max(dots, pages + 1);
    }
    void *card = view_create(page, HOME_CARD_X + slot % 2 * HOME_CARD_W, slot / 2 * HOME_CARD_H,
                             HOME_CARD_W, HOME_CARD_H);
    widget_set_name(card, "q2pod_card");
    void *icon = image_create(card, HOME_ICON_X, HOME_ICON_Y, HOME_ICON, HOME_ICON);
    widget_set_prop_int(icon, "clickable", 1);
    widget_set_prop_str(icon, "style:normal:bg_image", "home_q2pod");
    widget_set_prop_str(icon, "style:pressed:bg_image", "home_q2pod_down");
    widget_on(icon, EVT_CLICK, library_open, 0);
    void *label = label_create(card, 0, HOME_LABEL_Y, HOME_CARD_W, HOME_LABEL_H);
    widget_use_style(label, STYLE_HOME_LABEL);
    label_set_line_wrap(label, 1);
    widget_set_text_utf8(label, "Q2 Pod");
}
/* Bound before V2.1's init binds its own, so it runs after V2.1's rebuild (newest runs first). */
static int home_card_again(void *win, void *event) {
    (void)event;
    home_card(win);
    return 0;
}

/* The Q2 Pod page's Coverflow row (navigation.c). */
int coverflow_row(void *ctx, void *event) { return coverflow_open(ctx, event); }
#endif
