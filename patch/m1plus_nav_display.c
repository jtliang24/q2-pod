/* M1 Plus: Display settings and its sub-pages. patch/navigation.c includes this before the Q2's ringnav_display
 * (docs/m1plus-roadmap.md U1c). */
#if M1PLUS
/* systemset_display_page_init: V2.1's four rows (Brightness, Screen Off, Lock screen, Atmosphere Lamp), then
 * Appearance, Coverflow and Controls (ipod-ui 4.3), each opening stock's page again (display_open) with its stock
 * rows dropped and its own instead, as the Q2's do. Appearance holds Theme, Light Mode, Accent, Home and Battery
 * (4.5), Theme opening the built-ins' page (1.6.7; Minimal and Modern, Classic is unported); Coverflow Artist
 * Albums, Coverflow Sort and Refresh Coverflow; Controls Shortcut (4.5), Smart Awake, Hold Return and the volume
 * knob's two rows. Upstream 1.6.4 moved Smart Awake to Display and Controls to System, with
 * Key Tone and Buttons lock: the M1 keeps its layout until it is ported (docs/m1plus-unported.md). No Night Shift
 * (m1plus_offsets.inc LCD_*), no Corners (the glass is square), no Centred Now Playing row here, no Wheel QS or
 * Wheel Sensitivity (no wheel).
 * ponytail: stock's page opened over itself; its own rows' state is never touched on a sub-page. */
int ringnav_display(void *win, void *ctx) {
    static const char *const titles[] = { 0, "Appearance", "Cover Flow", "Controls", "Theme" },
                             *const sub_icons[] = { 0, ICON_DISPLAY, ICON_COVERMODE, ICON_FOLDERJUMP };
    static const char *const cf_icons[] = { ICON_COVERMODE, ICON_COVERMODE, "system_update" };
    static const char *const hold_icon[] = { ICON_FOLDERJUMP }, *const knob_icons[] = { ICON_FOLDERJUMP, ICON_FOLDERJUMP };
    /* Click With Headphones (9): Key Tone, no buzzer */
    static const unsigned char appearance[] = { 3, 6, 0, 1, 2, 8 }, controls[] = { 4, 7 };
    int sub = display_sub, result = stock_display_trampoline(win, ctx);
    void *view = win ? widget_lookup(win, VIEW_DISPLAY, 1) : (void *)0;
    if (!view) return result;
    if (!sub) {
        for (int i = DISPLAY_APPEARANCE; i <= DISPLAY_CONTROLS; ++i)
            widget_set_text_utf8(list_row_into(view, sub_icons[i], display_open, (void *)(long)i), titles[i]);
        return result;
    }
    widget_destroy_children(view);
    void *nav = widget_lookup(win, "view_navbar", 1), *title = nav ? widget_get_child(nav, 0) : 0;
    if (title) widget_set_text_utf8(title, titles[sub]);
    if (sub == DISPLAY_THEMES) { /* the Theme row's page (setting_row, 1.6.7): the M1's built-ins, as the Q2's */
        accent();
        for (int t = 0; t < THEME_N; ++t)
            widget_set_text_utf8(
                list_row(view, t == st.theme ? CHOICE_CHECK : "unselect", theme_pick, (void *)(long)t),
                themes[t].name);
        theme_view = view;
        return result;
    }
    /* Only this page's rows keep a label (the Theme page keeps Appearance's, open under it): a theme pick
     * (theme_select) relabels the theme's options, which the M1 spreads over Appearance and Controls, and a closed
     * page's label is a freed widget */
    for (unsigned i = 0; i < sizeof st.setting_label / sizeof *st.setting_label; ++i) st.setting_label[i] = (void *)0;
    if (sub == DISPLAY_COVERFLOW) {
        pod_rows(win, VIEW_DISPLAY, POD_ARTIST_CF, 1, cf_icons);
        pod_rows(win, VIEW_DISPLAY, POD_CF_SORT, 2, cf_icons + 1);
        return result;
    }
    const unsigned char *rows = sub == DISPLAY_APPEARANCE ? appearance : controls;
    for (unsigned k = 0, n = sub == DISPLAY_APPEARANCE ? sizeof appearance : sizeof controls; k < n; ++k)
        setting_row(view, rows[k]);
    if (sub != DISPLAY_CONTROLS) return result;
    /* Hold Return (Previous's hold and the chevron's, ipod-ui 4.4), then the volume knob's role (read by
     * knob_nav_active) and Navigation's direction */
    pod_rows(win, VIEW_DISPLAY, POD_HOLD_HOME, 1, hold_icon);
    pod_rows(win, VIEW_DISPLAY, POD_KNOB, 2, knob_icons);
    return result;
}
#endif
