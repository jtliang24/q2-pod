/* M1 Plus: Display settings' rows, one list. patch/navigation.c includes this before ringnav_display
 * (docs/m1plus-roadmap.md U4). */
#if M1PLUS
/* systemset_display_page_init: V2.1's own rows, then Artist Albums, Coverflow Sort and Refresh
 * Coverflow, then the volume knob's role (read by knob_nav_active) and Navigation's direction. The
 * Q2's Appearance, Coverflow and Controls sub-pages (1.5.0) wait: on M1 Controls would hold the knob
 * rows alone, with no Return key for Hold Return and no wheel for Wheel QS or Wheel Sensitivity. V2.1's
 * display rows have no icons. */
int ringnav_display(void *win, void *ctx) {
    int result = stock_display_trampoline(win, ctx);
    static const char *const cf_icon[] = { 0 };
    static const char *const cf_icons[] = { 0, 0 };
    static const char *const knob_icons[] = { 0, 0 };
    pod_rows(win, VIEW_DISPLAY, POD_ARTIST_CF, 1, cf_icon);
    pod_rows(win, VIEW_DISPLAY, POD_CF_SORT, 2, cf_icons);
    pod_rows(win, VIEW_DISPLAY, POD_KNOB, 2, knob_icons);
    return result;
}
#endif
