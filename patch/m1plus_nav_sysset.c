/* M1 Plus: System Setting's Apps row. patch/navigation.c includes this before ringnav_systemset
 * (docs/m1plus-roadmap.md U4). */
#if M1PLUS
/* Whether w, or a widget under it, draws the image named image (a V2.1 row's icon). */
static int draws_image(void *w, const char *image, int depth) {
    const char *name = w ? widget_get_prop_str(w, "image", (void *)0) : 0;
    if (name && !tk_strcmp(name, image)) return 1;
    for (unsigned i = 0, n = depth < 4 && w ? widget_count_children(w) : 0; i < n; ++i)
        if (draws_image(widget_get_child(w, i), image, depth + 1)) return 1;
    return 0;
}
/* reorder keeps V2.1's rows as built, so the Apps row list_row appended, the last, goes before V2.1's
 * System Update row (its system_update icon), as 1.4.2 orders them on the Q2; About stays last. It
 * opens a page, so it draws V2.1's chevron, as page_row_into's rows do. */
static void apps_before_update(void *view) {
    unsigned n = view ? widget_count_children(view) : 0;
    void *apps = n ? widget_get_child(view, n - 1) : 0;
    if (apps) image_base_set_image(image_create(apps, 295, 21, 13, 22), ROW_CHEVRON);
    for (unsigned i = 0; apps && i + 1 < n; ++i)
        if (draws_image(widget_get_child(view, i), "system_update", 0)) {
            widget_restack(apps, i);
            return;
        }
}
#endif
