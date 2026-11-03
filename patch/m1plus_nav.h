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
/* V1.32 routines V2.1 has no twin of that the iPod code the M1 now compiles reaches (M1PLUS_SHIMS in
 * tools/m1plus.py, listed by test/m1plus/ports.py); the Phase 4 item that ports each retires its stand-in. */
int player_start(void *queue, int index, int class, int mode) { return 0; } /* ringnav_boot's: no hook calls it */
int buzzeer_switch(int on) { return 0; } /* Key Tone: V2.1 has no buzzer command (progress 15) */
/* Now Playing's position timer (4.6): the scrub has no timer to stop and restart */
int playing_timer_start(void *win) { return 0; }
int playing_timer_clear(void *win) { return 0; }
/* AWTK's tk_str_end_with, which V2.1's AWTK lacks */
int tk_str_end_with(const char *str, const char *part) {
    unsigned n = 0, m = 0;
    while (str[n]) ++n;
    while (part[m]) ++m;
    if (m > n) return 0;
    for (unsigned i = 0; i < m; ++i)
        if (str[n - m + i] != part[i]) return 0;
    return 1;
}
/* V2.1 has no unload by name; the covers it would drop (the big cover's art, Home's, 4.5 and 4.6) are not drawn yet */
int image_manager_unload_bitmap_by_name(void *manager, const char *name) { return 0; }
/* The Q2 touch wheel's raw travel (playback.c, Q2 only): V2.1's knob posts keys, so these stay zero. */
volatile int wheel_raw __attribute__((section(".scratch")));
volatile int wheel_travel __attribute__((section(".scratch")));
volatile int wheel_held __attribute__((section(".scratch")));
/* RETURN_RELEASE_LATCH (m1plus_offsets.inc): V2.1 has no long Return to arm it */
unsigned char m1_return_latch;
#endif
