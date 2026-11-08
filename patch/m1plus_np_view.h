/* M1 Plus: what Now Playing's two pages share (docs/m1plus-ipod-ui.md 4.6). V2.1's playing_page.bin is the local page and
 * spotify.c's spot_np builds Spotify and Soloify's in code; each fills an np_src_t from its player and owns an np_view_t,
 * and patch/m1plus_np_view.c writes one from the other. The Q2 has neither. */
#ifndef M1PLUS_NP_VIEW_H
#define M1PLUS_NP_VIEW_H

/* A page's player now. A title or artist of 0 is the page's own to write: V2.1's timer writes the local page's. count 0 has
 * no "3 of 12". */
typedef struct {
    const char *title, *artist, *album;
    unsigned pos_ms, dur_ms, index, count;
    int playing;
} np_src_t;

/* A page's widgets, 0 for what is not np_write's: V2.1 writes the local page's elapsed time and shows its own play state.
 * hash: of the texts shown, 0 to refresh. bold: bold_label's last answer. shown: playing + 1, as play last styled. */
typedef struct {
    void *win, *title, *artist, *album, *elapsed, *remain, *counter, *play;
    unsigned hash, shown;
    int bold;
} np_view_t;

/* The bar's numbers and colours, for a w x h widget (np_bar_fill): the fill's width (0: none), and the line's y and height in
 * the widget, its corners, the fill's colour and the track's. V2.1's slider draws the local page's from fill and h; Spotify's
 * view paints all of it. */
typedef struct {
    int x, y, h, radius;
    unsigned fill, track;
} np_bar_t;

void np_write(np_view_t *v, const np_src_t *s);
np_bar_t np_bar_fill(unsigned pos_ms, unsigned dur_ms, int scrubbing, int w, int h);
void np_view_theme(const np_view_t *v);
void *spot_album(void); /* the Spotify page's album label, which paint_caps draws in Minimal; 0 without the page */
void spot_theme(void);  /* the Theme's change, on the Spotify page */

#endif
