/* M1 Plus: the declarations navigation.h's files share of the M1's own routines (docs/m1plus-roadmap.md U1c).
 * navigation.h includes this after its headers; the V2.1 stand-ins and the M1's globals are m1plus_nav_shims.c's. */
#if M1PLUS
extern int coverflow_centre(int x, int y); /* coverflow.c */
extern void video_touch(void *e);          /* books.c */
extern int coverflow_home_sets(void *top); /* coverflow.c: Home shows its Settings list */
/* Upstream 1.5.5's scheduling wrapper has no V2.1 call site yet (MAINSCHEDULING_CALL).
 * It remains inert until that port; V2.1 still runs its native scheduler. */
#define player_mainscheduling() 0
/* RETURN_RELEASE_LATCH (m1plus_offsets.inc): armed by Previous's hold (hold_previous), spent by its release */
extern unsigned char m1_return_latch;
/* 1.7.3's split keeps these static in their files; the M1's calls from navigation.c reach them through these */
int m1_ple_open(void *ctx, void *event); /* playlists.c ple_open: qm_run's playlist editor */
void m1_rate_close(int save);            /* ratings.c rate_close: a tap outside the picker (m1plus_nav_touch.c) */
extern int spot_band(void *win, void **bar, void **times); /* spotify.c */
static inline int spot_page(void *w) { return w && !tk_strcmp(widget_get_prop_str(w, "name", ""), "spotify_page"); }
/* m1plus_nav_stream.c (navigation.c), for Streaming's page (m1plus_nav_library.c, home.c): Soloify's row */
extern int svc_soloify;
int soloify_installed(void);
#endif
