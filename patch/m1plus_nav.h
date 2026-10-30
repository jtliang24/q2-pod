/* M1 Plus: navigation.c's declarations of the M1's own routines, and V2.1 stand-ins for V1.32 ones.
 * patch/navigation.c includes this after its headers (docs/m1plus-roadmap.md U1c). */
#if M1PLUS
extern int coverflow_centre(int x, int y); /* coverflow.c */
extern void video_touch(void *e);          /* books.c */
/* Knob: Navigation on Home (m1plus_nav_home.c, included after its callers) */
static int home_key(void *top, unsigned key);
static void home_input(void *e);
static void home_paint(void *w, void *canvas);
/* Upstream 1.5.5's scheduling wrapper has no V2.1 call site yet (MAINSCHEDULING_CALL).
 * It remains inert until that port; V2.1 still runs its native scheduler. */
#define player_mainscheduling() 0
#endif
