/* M1 Plus: stand-ins for stock routines V2.1 lacks, each used only where peq_platform.h defines no such
 * routine (on the Q2 it defines them all but tk_strcmp). patch/peq.h includes this in its target branch
 * (docs/m1plus-roadmap.md U1c). */
#ifndef tk_strcmp
#include "m1plus_peq_strcmp.h"
#if !M1PLUS
#define tk_strcmp strcmp
#endif
#endif
#ifndef set_hscroll_label_attribute
static inline void set_hscroll_label_attribute(void *w) { (void)w; }
#endif
#ifndef slide_menu_set_spacer
#define slide_menu_set_spacer(s, sp) ((void)0)
#endif
#ifndef window_manager_get_input_device_status
#if M1PLUS
#define window_manager_get_input_device_status(wm) ((char *)(wm) + 0xf8)
#else
#define window_manager_get_input_device_status(wm) ((char *)"")
#endif
#endif
#ifndef folder_reinit_navbarname
static inline int folder_reinit_navbarname(void) { return 0; }
#endif
#ifndef batch_init_selectrecord
static inline int batch_init_selectrecord(int n) { (void)n; return 0; }
#endif
#ifndef batch_set_selectitem
static inline int batch_set_selectitem(int n) { (void)n; return 0; }
#endif
#ifndef switch_charge_enable
static inline int switch_charge_enable(int n) { (void)n; return 0; }
#endif
#if !defined(getMusicByAlbumArtist) && defined(getMusicByAlbumAndAlbumSonger)
/* V2.1 has none: its album query's All songs flag drops the album (where albumsonger like the
 * artist, or ="" for none); the album is copied even then, so it can't be null */
static inline int getMusicByAlbumArtist(const char *artist) {
    return getMusicByAlbumAndAlbumSonger("", artist, 1);
}
#endif
#if !defined(config_playmode) && defined(dmrSendPlayMode)
/* V2.1 has none: its Play mode page's sequence (0x49fc78). The mode goes through the payload's
 * mclSetPlayMode hook, as stock's own call does; then the remote apps, the DLNA renderer, and the
 * saved setting. */
int ringnav_mode(int mode);
static inline int config_playmode(int mode, int notify) {
    int result = ringnav_mode(mode);
    if (notify) notifyPlayMode();
    dmrSendPlayMode(mode);
    write_int_config(mode, "PLAYSET", "PLAYMODE");
    return result;
}
#elif !defined(config_playmode)
static inline int config_playmode(int mode, int notify) { (void)mode; (void)notify; return 0; }
#endif
#ifndef window_manager_dispatch_input_event
extern int window_manager_dispatch_input_event(void *, void *);
#endif
#ifndef slide_menu_scroll_to_next
static inline int slide_menu_scroll_to_next(void *w) { (void)w; return 0; }
#endif
#ifndef slide_menu_scroll_to_prev
static inline int slide_menu_scroll_to_prev(void *w) { (void)w; return 0; }
#endif
