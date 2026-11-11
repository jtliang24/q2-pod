/* M1 Plus: coverflow.c's Q2-only statics, named so the M1 compile takes them unused; nothing calls them, so
 * --gc-sections drops them (docs/m1plus-sync.md). patch/coverflow.c includes this at its end. */
#if M1PLUS
/* Split's pane (home_foreground, its counts and card reads in navigation.c home_pane_read, a Q2-only
 * Streaming helper): only Classic's theme sets pane_icon_x, and Classic is unported on M1 (its own
 * geometry set boots V1.32's immediates), so coverflow_home never arms it. */
static void *const m1_unported_home_foreground __attribute__((unused)) = (void *)home_foreground;
/* Library on Home (home_library): Classic's HOMELIB option, unported with it; V2.1's Home binds its
 * Library row as every row (home_bind). */
static void *const m1_unported_home_library __attribute__((unused)) = (void *)home_library;
/* Classic's Home Streaming pane is unported along with its Library pane. */
static void *const m1_unported_home_streaming __attribute__((unused)) = (void *)home_streaming;
#endif
