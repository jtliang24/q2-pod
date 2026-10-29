/* V2.1 uses playmore_dialog, whose seven rows live in its UI asset, rather than a
 * PLAYMORE_ROWS kind table. Download Cover & Lyrics is listitem3. Keep the native
 * 50 px rows, 28 px icons and 20 px labels, with an unnamed new row under that one. */
int ringnav_playermore(void *win, void *ctx) {
    int result = stock_playermore_trampoline(win, ctx);
    void *view = win ? widget_lookup(win, "playmore_scrollview", 1) : 0;
    if (!view || widget_count_children(view) != PLAYMORE_COUNT || !al_playing()) return result;
    void *item = list_item_create(view, 0, 0, 310, 50);
    widget_use_style(item, ROW_STYLE);
    widget_on(item, EVT_CLICK, al_click, 0);
    image_base_set_image(image_create(item, 12, 11, 28, 28), "p_onlinesearch");
    void *label = hscroll_label_create(item, 48, 15, 250, 20);
    widget_use_style(label, "srlabel_item_white_style");
    set_hscroll_label_attribute(label);
    widget_restack(item, PLAYMORE_SEARCH + 1);
    widget_on(label, EVT_DESTROY, al_gone, label);
    al.label = label;
    al_show();
    widget_layout(view);
    return result;
}

/* Preserve the cover accept's native thumbnail refresh and return. Its generated JPEG also
 * goes beside the song. Resolve the search's keyword filename against the queue, so changing
 * tracks cannot give the new song the old search's cover. CUE songs keep stock's behavior. */
int m1plus_cover_save(const char *src, const char *dst, int w, int h) {
    int result = toolsThumbSpecCover(src, dst, w, h);
    char key[0x600], name[0x200], path[0x200 + 8];
    online_getkeyword_info(key);
    void *r = lrc_name(name, sizeof name, key) ? lrc_song(name) : 0;
    if (result == 1 && r && lrc_path(path, sizeof path, P(r, REC_PATH), ".jpg"))
        lrc_copy(dst, path);
    return result;
}
