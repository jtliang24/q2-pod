/* M1 Plus: the Lock screen page's picture grid in V2.1's page. patch/lockscreen.c includes this where it stood (docs/m1plus-roadmap.md U1c). */
#if M1PLUS
/* A picture past V2.1's six (ctx its index): V2.1's own pick, as its first six's clicks run it. */
static int saver_more(void *ctx, void *event) {
    void *img = event ? P(event, EVENT_TARGET) : (void *)0;
    if (img) saver_pick(widget_get_window(img), (int)(long)ctx);
    return 0;
}

/* systemset_screensaver_page_init (V2.1 has no rows routine to hook). Its grid holds six pictures,
 * placing a seventh on off the screen, with no click: two rows over Time show and About in
 * view_covers. With the built-ins there are up to twelve, so everything moves into a scroll view
 * over view_covers: every picture in V2.1's grid, then Time show, Clock (navigation.c's
 * POD_LOCKCLOCK, with Time show's icon) and About. Pictures past the sixth run V2.1's pick, and the
 * built-ins' thumbnails are found for lockscreen_paint. */
int lockscreen_page(void *win, void *ctx) {
    static const char *const icons[] = { ICON_SAVER_CLOCK };
    int result = stock_saverpage_trampoline(win, ctx);
    void *covers = win ? widget_lookup(win, VIEW_SAVER_COVERS, 1) : (void *)0, *list = PICTURES;
    void *time = covers ? widget_lookup(covers, VIEW_SAVER_TIME, 0) : (void *)0;
    void *about = covers ? widget_lookup(covers, VIEW_SAVER_ABOUT, 0) : (void *)0;
    if (!time || !about || !list) return result;
    void *view = scroll_view_create(covers, 0, 0, I(covers, W_W), I(covers, W_H));
    widget_set_name(view, "saver_list");
    widget_set_prop_int(view, "yslidable", 1);
    widget_set_prop_int(view, "xslidable", 0);
    for (unsigned n = widget_count_children(covers) - 1; n--;) {
        void *child = widget_get_child(covers, 0);
        widget_remove_child(covers, child);
        widget_add_child(view, child);
    }
    unsigned n = deque_size(list);
    for (unsigned i = 0; i < n; ++i) {
        char name[16];
        tk_snprintf(name, sizeof name, "imgcover%u", i);
        void *img = widget_lookup(view, name, 0);
        if (!img) continue;
        widget_move_resize(img, SAVER_X + i % 3 * SAVER_COL, i / 3 * SAVER_ROW, I(img, W_W), I(img, W_H));
        if (i >= SAVER_PICTURES) widget_on(img, EVT_CLICK, saver_more, (void *)(long)i);
        int id = wall_id(deque_at(list, i));
        if (id < 0) continue;
        image_base_set_image(img, ""); /* V2.1 set the name as a file:// path */
        lk.thumb[id] = img;
        widget_on(img, EVT_DESTROY, forget, img);
    }
    int y = (int)(n + 2) / 3 * SAVER_ROW + (I(time, W_Y) - 2 * SAVER_ROW);
    pod_rows(win, "saver_list", 7 /* POD_LOCKCLOCK */, 1, icons);
    void *clock = widget_get_child(view, widget_count_children(view) - 1);
    widget_move_resize(time, 0, y, I(time, W_W), I(time, W_H));
    widget_move_resize(clock, 0, y + SAVER_ITEM, I(time, W_W), I(time, W_H));
    widget_move_resize(about, 0, y + 2 * SAVER_ITEM, I(about, W_W), I(about, W_H));
    widget_set_prop_int(view, "virtual_h", y + 2 * SAVER_ITEM + I(about, W_H));
    return result;
}
#endif
