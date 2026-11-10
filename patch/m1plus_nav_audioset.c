/* M1 Plus: Playback settings' rows again after V2.1's rebuild. patch/navigation.c includes this where it stood (docs/m1plus-roadmap.md U1c). */
#if M1PLUS
/* Playback settings' rows after stock's, flat as before upstream 1.6.4's Library & Folders page (navigation.c
 * library_open, not ported: docs/m1plus-unported.md); reorder takes the Q2's row ids, so V2.1's list keeps its
 * order. */
static void audioset_rows(void *win) {
    static const char *const icons[] = { ICON_COVERMODE, ICON_FOLDERJUMP };
    pod_rows(win, VIEW_PLAYSET, POD_YEAR_OLD, 2, icons);
    pod_rows(win, VIEW_PLAYSET, POD_ARTIST_AZ, 1, icons);
    void *view = win ? widget_lookup(win, VIEW_PLAYSET, 1) : (void *)0;
    if (view) xfade_row(list_row_into(view, ICON_GAPLESS, xfade_open, (void *)0)); /* crossfade.c */
    if (view) {
        char name[256];
        root_read(name);
        st.root_label = list_row(view, ICON_FOLDERJUMP, root_click, 0);
        root_text(name);
        resume_row(list_row_into(view, ICON_MEMPLAY, xfade_open, (void *)2)); /* crossfade.c */
        mono_row(list_row(view, ICON_BALANCE, mono_click, 0));
        swap_row(list_row(view, ICON_BALANCE, swap_click, 0));
        mqa_row(list_row(view, ICON_DSDOUTPUT, mqa_click, 0)); /* crossfade.c */
    }
    reorder(view, playset_order, sizeof playset_order);
}
/* Named as m1plus_nav_library.c's tidal_downloads is: the Q2's Library & Folders page's order. */
static const void *const m1_unported_library_order __attribute__((unused)) = library_order;
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
