/* M1 Plus: About's CFW. Version row in V2.1's own rows. patch/navigation.c includes this where it stood (docs/m1plus-roadmap.md U1c). */
#if M1PLUS
/* V2.1's About (systemset_about_page_init's widget_foreach callback, 0x4a12c0): each row is a
 * list_item holding one hscroll_label, getFormatString's title and the value as "%s:%s"; FW. Version
 * is scrlabel1, from demo's version literal (the updater tag). It shows the stock firmware's again,
 * and a row in the same widgets and styles after it shows this build's. */
static void about_row(void *label, const char *key, const char *value) {
    char title[0x100], text[0x200];
    getFormatString(key, title, sizeof title);
    tk_snprintf(text, sizeof text, "%s:%s", title, value);
    widget_set_text_utf8(label, text);
}
int ringnav_about(void *win, void *ctx) {
    int result = stock_about_trampoline(win, ctx);
    void *view = win ? widget_lookup(win, VIEW_ABOUT, 1) : (void *)0;
    void *fw = win ? widget_lookup(win, ABOUT_FW_LABEL, 1) : (void *)0;
    if (view && fw) {
        about_row(fw, "about_version", STOCK_VERSION);
        void *item = list_item_create(view, 0, 0, 0, 0);
        widget_use_style(item, ROW_STYLE);
        void *label = hscroll_label_create(item, 12, 20, 260, 21);
        widget_use_style(label, ROW_LABEL_STYLE);
        char cfw[0x100];
        tk_snprintf(cfw, sizeof cfw, "CFW. Version:%s", Q2POD_VERSION);
        widget_set_text_utf8(label, cfw);
        widget_restack(item, 2);
    }
    return result;
}
#endif
