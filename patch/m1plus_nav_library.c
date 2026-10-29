/* M1 Plus: the Q2 Pod Home card's page, with Streaming's rows. patch/navigation.c includes this where it stood (docs/m1plus-roadmap.md U1c). */
#if M1PLUS
extern int coverflow_row(void *ctx, void *event); /* coverflow.c */
static int airplay_open(void *ctx, void *event);
/* The Q2 Pod Home card's page (coverflow.c home_card): the Library's added rows, which V2.1 has no
 * menu for (its Home is the library, and its categories stay there), in V2.1's rows and the Library's
 * order, with Coverflow, Q2's own Home card, after the media. Then Streaming's rows: V2.1 has no
 * Streaming page (its Tidal is a Home card), so Spotify, Internet Radio and AirPlay are here. */
extern void videos_open(const char *root); /* m1plus_books_video.c */
/* The Videos row lists the videos, as on 1.4.5 (videos_open); the Q2's opens Folder view. */
static int videos_click(void *ctx, void *event) {
    char root[sizeof st.media_root];
    if (media_find(VIDEOS, root)) videos_open(root);
    return 0;
}
int library_open(void *ctx, void *event) {
    (void)ctx;
    (void)event;
    if (st.lib_page || !(st.lib_page = page_open("library_page", page_closed, page_keyup))) return 0;
    static const char *const icons[] = { "local_podcasts", "local_audiobooks", "local_photos",
                                         "local_books", "local_videos" };
    char path[sizeof st.media_root];
    int media[VIDEOS], scrobbles = scrobble_ready(), apps = addon_scan(), n = 9 + scrobbles + apps;
    for (int k = 0; k < VIDEOS; k++) n += media[k] = media_find(k + 1, path);
    void *view = page_list(st.lib_page, st.lib_page, 0, "Q2 Pod", n, 64);
    library_into(view, "local_shuffle", shuffle_menu, 0, "Shuffle");
    library_into(view, "local_fav", ratings_menu, 0, "Ratings");
    library_into(view, "local_frequentplay", most_played, 0, "Most Played");
    library_into(view, "local_longsongs", long_songs, 0, "Long Songs");
    library_into(view, "local_era", era_menu, 0, "Era");
    for (int k = 0; k < VIDEOS; k++)
        if (media[k])
            library_into(view, icons[k], k + 1 == VIDEOS ? videos_click : media_click, (void *)(long)(k + 1),
                         MEDIA[k]);
    library_row(view, "local_coverflow", coverflow_row, 0, "Coverflow");
    library_into(view, "row_spotify", spot_open, 0, "Spotify"); /* stream_*'s at 40 px (tools/m1plus.py) */
    for (int k = 0; k < apps; ++k) /* the card apps on the card (addon.c), as Streaming lists them */
        library_into(view, "stream_app", addon_open, (void *)(long)k, addon_name(k));
    library_into(view, "row_radio", radio_open, 0, "Internet Radio");
    library_into(view, "stream_airplay", airplay_open, 0, "AirPlay");
    if (scrobbles) library_row(view, "local_scrobble", upload_scrobbles, 0, "Upload Scrobbles");
    return 0;
}
/* No Tidal Downloads row (navigation.c tidal_downloads, Streaming's on the Q2): on M1, tidal_start
 * passes no song id, so tidal_play downloads nothing (docs/m1plus-roadmap.md U4). Named here so the
 * M1 compile takes the unused page; nothing calls it, so it isn't linked. */
static void *const m1_unported_tidal_downloads __attribute__((unused)) = (void *)tidal_downloads;
/* No Configuration row (navigation.c stream_config, Streaming's on the Q2, 1.2.9): Spotify's and
 * Tidal's cache sizes and Stop Streaming Services. Its icon (stream_config.png) is the Q2's
 * (docs/m1plus-roadmap.md U3's batch). Named as tidal_downloads is. */
static void *const m1_unported_stream_config __attribute__((unused)) = (void *)stream_config;
/* No trailing dots on a playlist row (navigation.c more_image, the Q2's qm_hold, 1.3.8): they open
 * playlistsmore_page, which V2.1 doesn't have; the M1's hold opens the editor itself
 * (m1plus_nav_playlist_hold.inc). Named as tidal_downloads is. */
static void *const m1_unported_more_image __attribute__((unused)) = (void *)more_image;
#endif
