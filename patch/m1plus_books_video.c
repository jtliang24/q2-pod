/* M1 Plus: quitting a video with a tap on q2video's back chevron. patch/books.c includes this where it stood (docs/m1plus-roadmap.md U1c). */
#if M1PLUS
/* ringnav_input's touches while q2video plays. M1 Plus has no Return key: q2video draws a back
 * chevron at the top left (video.c back_glyph), and a tap pressed and lifted in its VIDEO_BACK_PX
 * square there quits, as Return does. Any other touch does nothing. */
#define VIDEO_BACK_PX 64 /* video.c BACK_PX */
void video_touch(void *e) {
    unsigned type = (unsigned)I(e, EVENT_TYPE);
    int in = I(e, EVENT_X) < VIDEO_BACK_PX && I(e, EVENT_Y) < VIDEO_BACK_PX;
    if (type == EVT_INPUT_POINTER_DOWN)
        vid.back = in;
    else if (type == EVT_INPUT_POINTER_MOVE)
        vid.back &= in;
    else if (type == EVT_POINTER_UP) {
        if (vid.back && in) video_key(KEY_RETURN);
        vid.back = 0;
    }
}
/* The Q2 Pod page's Videos row (m1plus_nav_library.c): the videos, by path, as 1.4.5's Videos row
 * listed them; the Q2's opens Folder view, whose video rows play through its folder_click hook,
 * unported on M1 (docs/m1plus-unported.md). */
static void m1_scan_videos(const char *dir, int depth) {
    void *d = opendir(dir);
    char path[600];
    for (struct dirent *e; d && bk.n < BOOKS_MAX && (e = readdir(d));) {
        if (e->d_name[0] == '.') continue;
        tk_snprintf(path, sizeof path, "%s/%s", dir, e->d_name);
        if ((e->d_type == 8 || !e->d_type) && book_kind(e->d_name) == 3) {
            if ((bk.path[bk.n] = strdup(path))) ++bk.n;
        } else if ((e->d_type == 4 || !e->d_type) && depth)
            m1_scan_videos(path, 0);
    }
    if (d) closedir(d);
}
static int m1_play_video(void *ctx, void *event) {
    video_play(bk.path[(int)(long)ctx]);
    return 0;
}
void videos_open(const char *root) {
    if (bk.page) return;
    void *page = bk.page = page_open("books_page", closed, keyup);
    if (!page) return;
    BLOB_IO(BOOK_MARKS, bk.marks, 0);
    void *f = widget_factory();
    int h = widget_get_prop_int(page, "h", BOTTOM);
    bk.list = widget_factory_create_widget(f, "view", page, 0, 0, UI_W, h);
    bk.reader = widget_factory_create_widget(f, "view", page, 0, 0, UI_W, h);
    bk.sheet = widget_factory_create_widget(f, "view", bk.reader, 0, 0, UI_W, h);
    bk.info = bottom_caption(bk.reader, h);
    back_button(bk.reader);
    view_show(bk.reader, 0);
    bk.buf = calloc(BOOK_WIN, 1);
    bk.path = calloc(BOOKS_MAX, sizeof *bk.path);
    if (bk.buf && bk.path) m1_scan_videos(root, 1);
    if (bk.n) qsort(bk.path, (unsigned)bk.n, sizeof *bk.path, by_string);
    bk.view = page_list(page, bk.list, 0, bk.n ? "Videos" : "No videos", bk.n, 48);
    char name[256];
    for (int k = 0; k < bk.n; ++k) page_row_detail(bk.view, k, title(bk.path[k], name), 0, m1_play_video);
}
#endif
