/* M1 Plus: V2.1's settings rows for the payload's list_row. patch/navigation.c includes this where it stood (docs/m1plus-roadmap.md U1c). */
#if M1PLUS
/* A stock settings row as V2.1 builds them (playset's, 0x4a0578): a list_item_style list_item (64
 * high, the list's item height), a 40 px icon at 12,10, a 21 px srlabel_leftwhite21_style label at
 * 60,20 (no icon: at 12), and, opening a page, right_arrow at 295. The click is the row's. Returns
 * the label. */
static void *list_row_core(void *view, const char *icon, int (*click)(void *, void *), void *ctx,
                           int w, int into) {
    (void)w;
    void *item = list_item_create(view, 0, 0, 0, 0);
    widget_use_style(item, ROW_STYLE);
    if (click) widget_on(item, EVT_CLICK, click, ctx);
    if (icon) image_base_set_image(image_create(item, 12, 10, 40, 40), icon);
    void *label = hscroll_label_create(item, icon ? 60 : 12, 20, into ? 220 : 240, 21);
    widget_use_style(label, ROW_LABEL_STYLE);
    if (into) image_base_set_image(image_create(item, 295, 21, 13, 22), ROW_CHEVRON);
    return label;
}
#endif
