/* M1 Plus: a touch long-press's row in the hold menu. patch/navigation.c includes this where it stood (docs/m1plus-roadmap.md U1c). */
#if M1PLUS
/* A touch long-press's row: the entry under the pressed point, as an index into m. The point must
 * be on the list itself, since a recycled table keeps rows past its viewport. V2.1's
 * widget_to_local adds each widget's own scroll offset (get_offset), the list's too, so the
 * point is in the list's content; bounds() and m->height are on screen, so take the list's
 * offset off again, as bounds() does: a scroll view's (SCROLL_X, SCROLL_Y), a table's TABLE_TOP. */
static int lp_entry(menu_t *m) {
    int xy[2] = { st.lp_x, st.lp_y };
    widget_to_local(m->w, xy);
    xy[1] -= view_top(m);
    if (m->kind == 1) xy[0] -= I(m->w, SCROLL_X);
    if (xy[0] < 0 || xy[1] < 0 || xy[0] >= I(m->w, W_W) || xy[1] >= m->height) return -1;
    for (int i = 0; i < m->n; ++i) {
        rect_t r = bounds(m, i);
        if (xy[0] >= r.x && xy[0] < r.x + r.w && xy[1] >= r.y && xy[1] < r.y + r.h) return i;
    }
    return -1;
}
#define LP_TOUCH st.lp_touch
#endif
