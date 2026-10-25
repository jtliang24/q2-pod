/* M1 Plus: the hold menu's Go to Album and Go to Artist, and a Folder play's Now Playing, on V2.1's
 * pages. patch/navigation.c includes this before qm_goto (docs/m1plus-roadmap.md U4). */
#if M1PLUS
/* V2.1 has no artistinfo_page, and its playerjumpinfo_page shows the playing song's album. An artist's
 * albums are album_page with V2.1's Artists row context, {CLASS_ARTISTS, record}: loadAlbumList takes
 * the album artist (or the artist, as Artists is set) from the record. An album is albuminfo_page with
 * Album's row context, its showlist row << 16 | CLASS_ALBUMS, which loadAlbumdetailList (hooked as
 * ringnav_album_detail) reads the album and artist from: the record goes last in the showlist, which
 * the page's load then replaces with the album's songs. Either page sets cur_classtype and reloads the
 * showlist, which a page underneath draws from again as it comes back (Recent's showed the album's
 * songs on the device), so both are put back as the page closes, as qm_restore puts classinfo back. */
static unsigned goto_class __attribute__((section(".scratch")));
static void *goto_list __attribute__((section(".scratch")));
static int goto_restore(void *page, void *event) {
    void *list = P(p_deque_showlist, 0);
    I(g_class_type, 0) = (int)goto_class;
    if (goto_list && list) {
        deque_clear(list);
        deque_assign(list, goto_list);
    }
    if (goto_list) deque_destroy(goto_list);
    goto_list = 0;
    return 0;
}
static void m1plus_goto(void *r, int album) {
    void *wm = window_manager(), *page = window_manager_get_top_window(wm), *list = P(p_deque_showlist, 0);
    goto_class = (unsigned)I(g_class_type, 0);
    if (goto_list) deque_destroy(goto_list);
    goto_list = list ? _create_deque("stSongInfo") : 0;
    if (goto_list) {
        deque_init(goto_list);
        deque_assign(goto_list, list);
    }
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

/* V2.1's Folder file click opens playing_page without looking for one already open (FOLDER_PLAY, its
 * navigator_to_with_context): after Go to Folder from Now Playing, a play opened a second Now Playing
 * over the folders, and the first one, under them, went stale. That one closes first, unanimated and
 * unseen, as Coverflow's scoped page closes the artist page under it, so Back from the new one goes to
 * the folder. V2.1's album track click instead goes back down to it (0x525860). */
int m1plus_play_page(const char *name, void *context) {
    void *wm = window_manager();
    for (unsigned i = widget_count_children(wm); i-- > 0;) {
        void *w = widget_get_child(wm, i);
        if (!tk_strcmp(widget_get_prop_str(w, "name", ""), "playing_page")) {
            window_manager_close_window_force(wm, w);
            break;
        }
    }
    return navigator_to_with_context(name, context);
}
#endif
