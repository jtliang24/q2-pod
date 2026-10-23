/* M1 Plus: Coverflow's covers by touch. patch/coverflow.c includes this where it stood (docs/m1plus-roadmap.md U1c). */
#if M1PLUS
/* The covers' touch (navigation.c slide_swipe): a swipe turns them a cover per CF_STRIDE px, as
 * the frame draws them (the flat fallback's at its own stride). A tap on the centre cover opens
 * it, as Centre does, and one on a side cover brings that cover to the centre. The back button's
 * press is its own. */
static int touched(void *ctx, void *e) {
    (void)ctx;
    if (cf.screen != COVERS || !cf.slide || cf.timer) return 0;
    int xy[2] = { I(e, EVENT_X), I(e, EVENT_Y) }, depth = fx.frame != 0;
    widget_to_local(cf.covers, xy);
    int px = xy[0] < BACK_W && xy[1] < 48 ? 0 : depth ? CF_STRIDE : slide_stride(cf.slide);
    int bounded = coverflow_bounded(cf.slide);
    int top = I(cf.slide, W_Y), d = xy[0] - CF_CX, far = d < 0 ? -d : d;
    if (!slide_swipe(cf.slide, e, px, bounded) || xy[1] < top || xy[1] >= top + I(cf.slide, W_H))
        return 0;
    if (far < ART_SIZE / 2) /* the centre cover */
        return pick((void *)(long)I(cf.slide, SLIDE_INDEX), 0);
    int k = !depth || far < CF_X1 + CF_XS / 2 ? 1 : 2 + (far - CF_X1 - CF_XS / 2) / CF_XS;
    slide_step(cf.slide, d < 0 ? -k : k, bounded);
    return 0;
}

/* A touch long-press's point (screen pixels) on the centre cover, whose album menu it opens
 * (navigation.c qm_hold), at rest. */
int coverflow_centre(int x, int y) {
    if (!cf.slide || cf.screen != COVERS || P(cf.slide, SLIDE_ANIMATOR) || I(cf.slide, SLIDE_OFFSET))
        return 0;
    int xy[2] = { x, y }, top = fx.frame ? CF_TOP : I(cf.slide, W_Y);
    widget_to_local(cf.covers, xy);
    return xy[0] >= CF_CX - ART_SIZE / 2 && xy[0] < CF_CX + ART_SIZE / 2 && xy[1] >= top &&
           xy[1] < top + ART_SIZE;
}
#endif
