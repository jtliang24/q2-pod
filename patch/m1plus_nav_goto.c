/* M1 Plus: the hold menu's Go to Album and Go to Artist on V2.1's pages. patch/navigation.c includes
 * this before qm_goto (docs/m1plus-roadmap.md U4). */
#if M1PLUS
/* V2.1 has no artistinfo_page, and its playerjumpinfo_page shows the playing song's album. An artist's
 * albums are album_page with V2.1's Artists row context, {CLASS_ARTISTS, record}: loadAlbumList takes
 * the album artist (or the artist, as Artists is set) from the record. An album is albuminfo_page with
 * Album's row context, its showlist row << 16 | CLASS_ALBUMS, which loadAlbumdetailList (hooked as
 * ringnav_album_detail) reads the album and artist from: the record goes last in the showlist, which
 * the page's load then replaces with the album's songs. Either page sets cur_classtype, which the page
 * underneath reads again, so it is put back as the page closes, as qm_restore puts classinfo back. */
static unsigned goto_class __attribute__((section(".scratch")));
static int goto_restore(void *page, void *event) {
    I(g_class_type, 0) = (int)goto_class;
    return 0;
}
static void m1plus_goto(void *r, int album) {
    void *wm = window_manager(), *page = window_manager_get_top_window(wm), *list = P(p_deque_showlist, 0);
    goto_class = (unsigned)I(g_class_type, 0);
    if (album && list) {
        _deque_push_back(list, r);
        navigator_to_with_context("albuminfo_page", (void *)(long)((deque_size(list) - 1) << 16 | CLASS_ALBUMS));
    } else if (!album) {
        struct {
            int cls;
            void *r;
        } context = { CLASS_ARTISTS, r };
        navigator_to_with_context("album_page", &context);
    }
    void *top = window_manager_get_top_window(wm);
    if (top != page) widget_on(top, EVT_WINDOW_CLOSE, goto_restore, top);
}
#endif
