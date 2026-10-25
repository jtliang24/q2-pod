/* M1 Plus: page_list's rows in V2.1's settings-row look. patch/coverflow.c includes this where they stood (docs/m1plus-roadmap.md section 7). */
#if M1PLUS
/* One PAGE_ROW_H row of a page_list, as V2.1 builds its settings rows and list_row_core the Q2 Pod
 * page's (m1plus_nav_rows.c): a ROW_STYLE list_item, the caption left at PAGE_ROW_X in ROW_LABEL_STYLE
 * and, with a detail (Most Played's, View Queue's), the caption above it and the detail in 16px
 * #AAAAAA. The labels scroll as text()'s do. Returns the row. */
static void *row_label(void *item, int y, int h) {
    void *label = hscroll_label_create(item, PAGE_ROW_X, y, PAGE_ROW_W, h);
    widget_use_style(label, ROW_LABEL_STYLE);
    set_hscroll_label_attribute(label);
    widget_set_prop_int(label, "loop", 1);
    return label;
}
void *page_row_detail(void *view, int index, const char *caption, const char *detail,
                      int (*click)(void *, void *)) {
    void *item = list_item_create(view, 0, index * PAGE_ROW_H, UI_W, PAGE_ROW_H);
    widget_use_style(item, ROW_STYLE);
    widget_set_text_utf8(row_label(item, detail ? 9 : 20, 24), caption);
    if (detail) {
        void *label = row_label(item, 36, 20);
        widget_set_prop_int(label, "style:normal:text_color", (int)0xffaaaaaau);
        widget_set_prop_int(label, "style:normal:font_size", 16);
        widget_set_text_utf8(label, detail);
    }
    widget_on(item, EVT_CLICK, click, (void *)(long)index);
    return item;
}

/* A row that opens another list: V2.1's chevron at the right, as on the Q2 Pod page. */
void page_row_into(void *view, int index, const char *caption, int (*click)(void *, void *)) {
    void *item = page_row_detail(view, index, caption, 0, click);
    image_base_set_image(image_create(item, 295, 21, 13, 22), ROW_CHEVRON);
}
#endif
