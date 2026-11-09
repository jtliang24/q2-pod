/* M1 Plus: navigation.c's declarations of the M1's own routines, and V2.1 stand-ins for V1.32 ones.
 * patch/navigation.c includes this after its headers (docs/m1plus-roadmap.md U1c). */
#if M1PLUS
extern int coverflow_centre(int x, int y); /* coverflow.c */
extern void video_touch(void *e);          /* books.c */
static int chevron_input(void *e); /* m1plus_nav_back.c, included after its callers */
static void bar_play_input(void *e); /* m1plus_nav_back.c, likewise */
extern int coverflow_home_sets(void *top); /* coverflow.c: Home shows its Settings list */
/* Upstream 1.5.5's scheduling wrapper has no V2.1 call site yet (MAINSCHEDULING_CALL).
 * It remains inert until that port; V2.1 still runs its native scheduler. */
#define player_mainscheduling() 0
/* V1.32 routines V2.1 has no twin of that the iPod code the M1 now compiles reaches (M1PLUS_SHIMS in
 * tools/m1plus.py, listed by test/m1plus/ports.py); the Phase 4 item that ports each retires its stand-in. */
int buzzeer_switch(int on) { return 0; } /* Key Tone: V2.1 has no buzzer command (progress 15) */
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
/* AWTK's unload by name, which V2.1's AWTK lacks (ipod-ui 4.5): V2.1's image_manager_lookup (0x655850) finds the
 * cached bitmap by name and copies it, not owning its buffer, into a bitmap_t (72 bytes); image_manager_unload_bitmap
 * (0x656004) removes every cached entry with that buffer, which frees it. The copy is not used after. Home drops the
 * player's cover file this way when the next track writes the same name. */
int image_manager_unload_bitmap_by_name(void *manager, const char *name) {
    unsigned bitmap[64]; /* bitmap_t */
    if (!manager || !name || image_manager_lookup(manager, name, bitmap)) return 1; /* RET_FAIL; not cached */
    return image_manager_unload_bitmap(manager, bitmap);
}
/* The Q2 touch wheel's raw travel (playback.c, Q2 only): V2.1's knob posts keys, so these stay zero. */
volatile int wheel_raw __attribute__((section(".scratch")));
volatile int wheel_travel __attribute__((section(".scratch")));
volatile int wheel_held __attribute__((section(".scratch")));
/* RETURN_RELEASE_LATCH (m1plus_offsets.inc): armed by Previous's hold (hold_previous), spent by its release */
unsigned char m1_return_latch;
#endif
