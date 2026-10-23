/* M1 Plus: Playback settings' rows again after V2.1's rebuild. patch/navigation.c includes this where it stood (docs/m1plus-roadmap.md U1c). */
#if M1PLUS
/* V2.1 rebuilds the list whole, stock's rows only, each time the page comes back to the front (from
 * EQ, Default Vol or Crossfade's page): its init binds EVT_WINDOW_FOREGROUND to the list's builder
 * (0x4a0c50), which destroys every row first. This adds ours again after it. AWTK runs a widget's
 * handlers newest first (emitter_on_with_tag puts each at the head, 0x6f4668), so it is bound
 * before stock's init binds its own. */
static int audioset_again(void *win, void *event) {
    (void)event;
    audioset_rows(win);
    return 0;
}
int ringnav_audioset(void *win, void *ctx) {
    if (win) widget_on(win, EVT_WINDOW_FOREGROUND, audioset_again, win);
    int result = stock_audioset_trampoline(win, ctx);
    audioset_rows(win);
    return result;
}
#endif
