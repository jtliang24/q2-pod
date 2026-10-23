/* M1 Plus: the shared helpers only the M1 Plus payload has, and view_show for both models. patch/peq.h
 * includes this beside its own helpers (docs/m1plus-roadmap.md U1c). */
#if M1PLUS
void *back_button(void *parent);
void dispatch_key_return(void); /* navigation.c: back_button's Return */
#endif
#if M1PLUS
int slide_swipe(void *s, void *e, int px, int bounded); /* navigation.c: a finger on a carousel */
void slide_step(void *s, int k, int bounded);
#endif
/* A page's full-size view shown or hidden. AWTK's hit test skips insensitive children but not
 * hidden ones, so on the M1 Plus's touch screen a hidden view over a list would take its taps. The
 * Q2 has the same hit test; its build is kept as it was. */
#if M1PLUS
#define view_show(w, on) (widget_set_visible(w, on, 0), widget_set_sensitive(w, on))
#else
#define view_show(w, on) widget_set_visible(w, on, 0)
#endif
