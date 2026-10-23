/* M1 Plus: the photo viewer by touch. patch/photos.c includes this where it stood (docs/m1plus-roadmap.md U1c). */
#if M1PLUS
/* The viewer's touch (navigation.c slide_swipe): a swipe moves a photo per screen width, as the
 * paint draws them, and a tap shows or hides the caption. The back button's press is its own. */
static int swiped(void *ctx, void *e) {
    (void)ctx;
    if (ph.screen != VIEWER || !ph.slide) return 0;
    int xy[2] = { I(e, EVENT_X), I(e, EVENT_Y) };
    widget_to_local(ph.viewer, xy);
    if (slide_swipe(ph.slide, e, xy[0] < BACK_W && xy[1] < 48 ? 0 : UI_W, 0)) toggle_info(0, 0);
    return 0;
}
#endif
