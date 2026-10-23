/* M1 Plus: the Q2 Pod Home card's page, with Streaming's rows. patch/navigation.c includes this where it stood (docs/m1plus-roadmap.md U1c). */
#if M1PLUS
extern int coverflow_row(void *ctx, void *event); /* coverflow.c */
static int airplay_open(void *ctx, void *event);
/* The Q2 Pod Home card's page (coverflow.c home_card): the Library's added rows, which V2.1 has no
 * menu for (its Home is the library, and its categories stay there), in V2.1's rows and the Library's
 * order, with Coverflow, Q2's own Home card, after the media. Then Streaming's rows: V2.1 has no
 * Streaming page (its Tidal is a Home card), so Spotify, Internet Radio and AirPlay are here. */
int library_open(void *ctx, void *event) {
    (void)ctx;
    (void)event;
    if (st.lib_page || !(st.lib_page = page_open("library_page", page_closed, page_keyup))) return 0;
    static const char *const icons[] = { "local_podcasts", "local_audiobooks", "local_photos",
                                         "local_books", "local_videos" };
    char path[sizeof st.media_root];
    int media[VIDEOS], scrobbles = scrobble_ready(), n = 8 + scrobbles;
    for (int k = 0; k < VIDEOS; k++) n += media[k] = media_find(k + 1, path);
    void *view = page_list(st.lib_page, st.lib_page, 0, "Q2 Pod", n, 64);
    library_into(view, "local_shuffle", shuffle_menu, 0, "Shuffle");
    library_into(view, "local_fav", ratings_menu, 0, "Ratings");
    library_row(view, "local_frequentplay", most_played, 0, "Most Played");
    library_row(view, "local_longsongs", long_songs, 0, "Long Songs");
    for (int k = 0; k < VIDEOS; k++)
        if (media[k]) library_row(view, icons[k], media_click, (void *)(long)(k + 1), MEDIA[k]);
    library_row(view, "local_coverflow", coverflow_row, 0, "Coverflow");
    library_into(view, "stream_spotify", spot_open, 0, "Spotify");
    library_into(view, "stream_radio", radio_open, 0, "Internet Radio");
    library_into(view, "stream_airplay", airplay_open, 0, "AirPlay");
    if (scrobbles) library_row(view, "local_scrobble", upload_scrobbles, 0, "Upload Scrobbles");
    return 0;
}
/* No Tidal Downloads row (navigation.c tidal_downloads, Streaming's on the Q2): on M1, tidal_start
 * passes no song id, so tidal_play downloads nothing (docs/m1plus-roadmap.md U4). Named here so the
 * M1 compile takes the unused page; nothing calls it, so it isn't linked. */
static void *const m1_unported_tidal_downloads __attribute__((unused)) = (void *)tidal_downloads;
#endif
