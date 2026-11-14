/* M1 Plus: the shared helpers only the M1 Plus payload has, and view_show for both models. patch/peq.h
 * includes this beside its own helpers (docs/m1plus-roadmap.md U1c). */
#if M1PLUS
int peq_back(void *top); /* peq_ui.c: the chevron's back on the PEQ page, 1 if top is it */
void dispatch_key_return(void); /* navigation.c: previous_back's Return, for a payload page */
int ringnav_knob_nav(void); /* navigation.c: the knob navigates here (Knob: Navigation) */
#endif
/* The PEQ tab bar's focus card (tabs_paint): where the wheel or knob is. The M1's knob moves it only in Knob:
 * Navigation; with Knob: Volume a tap's card marked a focus nothing could move (V039m). */
#if M1PLUS
#define peq_focus_shown() ringnav_knob_nav()
#else
#define peq_focus_shown() 1
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

/* Payload page lists use the M1 library pitch; PEQ's own 48 px rows still use page_h. */
#if M1PLUS
#define page_row_height(h) LIB_PITCH
#else
#define page_row_height(h) page_h(h)
#endif
