/* M1 Plus: the lists' selection, as Stock's outline over V2.1's rows. patch/navigation.c includes this.
 * Upstream 1.5.9 draws only the iPod's bar, behind the rows (paint_selection, from
 * widget_on_paint_background); V2.1's rows are opaque until the iPod row styles make them transparent
 * (docs/m1plus-ipod-ui.md 4.1), so the M1 Plus keeps 1.5.8's Stock outline, drawn over them from
 * ringnav_paint. */
#if M1PLUS
/* RADIUS, FILL_RGB, FILL_ALPHA, SHADE_ALPHA, OUTLINE_RGB and OUTLINE_ALPHA come from offsets.inc;
 * the colors pack their bytes at compile time (little-endian r,g,b,a). The outline is translucent
 * neutral white, never the playing red, seated on a dark shade of the stock surface so bright
 * album art cannot wash it out. */
#define FILL_COLOR ((FILL_ALPHA << 24) | FILL_RGB)
#define SHADE_COLOR ((SHADE_ALPHA << 24) | FILL_RGB)
#define OUTLINE_COLOR ((OUTLINE_ALPHA << 24) | OUTLINE_RGB)

/* Load and settle the painted surface's selection, then draw it: a neutral outline over the rows.
 * The outline is one neutral white line seated on a dark shade line: the shade is the stock
 * dark surface at an alpha high enough to hold the white over bright album art, and being the same
 * color as the dark rows it vanishes on the stock theme. The translucent fill keeps the row
 * readable over artwork without borrowing the red "playing" language or the native focus flag.
 * Small rows and degenerate geometry keep the square fallback. */
static void outline_selection(void *w, void *canvas) {
    if (!w || !canvas || !kind(w)) return;
    void *top = window_manager_get_top_window(window_manager());
    int i, shown = !st.touch_mode;
    if (surface((void *)0, (void *)0) != w) return;
    if (!load(&g_menu, w, !window_manager_get_pointer_pressed(window_manager()))) {
        cancel_center();
        return;
    }
    if (st.center_timer && !pending_matches(top, &g_menu)) cancel_center();
    if (g_menu.kind == 3) return; /* Home shows its selected card. */
    i = reconcile(&g_menu, !moving(&g_menu) && !window_manager_get_pointer_pressed(window_manager()));
    /* Touch hides the selection until the wheel or a button, except on Home (iPod's list) and a
     * pop-up's buttons, which open on their first (Cancel). */
    int home = home_menu(top);
    if (i < 0 || (!shown && !home && g_menu.kind != 4)) return;
    rect_t r = bounds(&g_menu, i), old;
    /* A boundary detent nudges the selection against the end until it springs back. */
    if (fx_live(w) && st.bump_dir) r.y -= st.bump_dir * BUMP_PX;
    if (r.w < 5 || r.h < 5 || !P(canvas, CANVAS_LCD)) return;
    void *lcd = P(canvas, CANVAS_LCD);
    unsigned fill_color = (unsigned)I(lcd, LCD_FILL_COLOR);
    unsigned stroke_color = (unsigned)I(lcd, LCD_STROKE_COLOR);
    if (!clip_surface(canvas, &g_menu, &old)) return;
    rect_t outer = { r.x + 1, r.y + 1, r.w - 2, r.h - 2 };
    rect_t inner = { outer.x + 1, outer.y + 1, outer.w - 2, outer.h - 2 };
    int drawn = 0;
    /* Two concentric one-pixel rounded strokes, shade outside and white inside, not one
     * border_width=2 call: the effect then does not depend on how a canvas backend
     * interprets the width argument. Geometry is checked before the call, and radius 9/8
     * both stay above the stock "square at <= 2" cutoff. The stock rounded stroke returns
     * non-zero when its backend cannot draw (for example a canvas without a vgcanvas), and
     * the safe square fallback then keeps the outline visible. */
    if (outer.w > 2 * RADIUS && outer.h > 2 * RADIUS) {
        unsigned fill = FILL_COLOR;
        canvas_fill_rounded_rect(canvas, &outer, (void *)0, &fill, RADIUS);
        unsigned shade = SHADE_COLOR;
        unsigned white = OUTLINE_COLOR;
        drawn = canvas_stroke_rounded_rect(canvas, &outer, (void *)0, &shade, RADIUS, 1) == 0;
        if (drawn)
            drawn =
                canvas_stroke_rounded_rect(canvas, &inner, (void *)0, &white, RADIUS - 1, 1) == 0;
    }
    if (!drawn) {
        canvas_set_stroke_color(canvas, SHADE_COLOR);
        canvas_stroke_rect(canvas, outer.x, outer.y, outer.w, outer.h);
        canvas_set_stroke_color(canvas, OUTLINE_COLOR);
        canvas_stroke_rect(canvas, inner.x, inner.y, inner.w, inner.h);
    }
    /* Save/restore explicitly: this firmware's canvas_save/restore cover neither clip nor
     * either color, and the global alpha is deliberately never touched. */
    stock_canvas_set_fill_color(canvas, fill_color);
    stock_canvas_set_stroke_color(canvas, stroke_color);
    canvas_set_clip_rect(canvas, &old);
}
#endif
