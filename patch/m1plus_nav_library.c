/* M1 Plus: the Library and Streaming entry pages, Home's Library and Streaming rows. patch/navigation.c includes this where it stood (docs/m1plus-roadmap.md U1c). */
#if M1PLUS
static int airplay_open(void *ctx, void *event);
/* V2.1 has neither page: its Home grid held the library's categories and its services as cards. The iPod Home
 * (docs/m1plus-ipod-ui.md 4.5) opens the Library, upstream's rows in its order with V2.1's own categories and
 * maintenance, and Streaming, V2.1's native services with the payload's. */
extern void videos_open(const char *root); /* m1plus_books_video.c */
/* The Videos row lists the videos, as on 1.4.5 (videos_open); the Q2's opens Folder view. */
static int videos_click(void *ctx, void *event) {
    char root[sizeof st.media_root];
    if (media_find(VIDEOS, root)) videos_open(root);
    return 0;
}
/* Tag a service row so Configuration updates the page beneath it immediately. */
static void m1_svc_row(void *row, int i, char *hide) {
    prop(row, SVC_PROP, i + 1);
    if (svc_find(hide, i)) widget_set_visible(row, 0, 0);
}
/* Bind the native dispatcher with the row as its context: its only widget read is the name
 * (0x533ba4), parsed as a native Home id. Albums builds its own {class, record} context. The ids
 * index V2.1's Home table (get_homemenu_showinfo, 0x97c940): 0 hifimusic, 1 tidal,
 * 2 sset_updatemusic, 3 mymusic, 5 album, 6 songer, 7 genre, 8 composer, 9 hr, 11 many, 12 recent,
 * 13 recentadd, 14 playlist, 15 cdripper. The dispatcher checks the network for 0 and 1. */
static void m1_native_row(void *view, const char *icon, const char *name, const char *title) {
    void *row = library_into(view, icon, 0, 0, title);
    image_set_draw_type(widget_get_child(row, 0), IMAGE_DRAW_SCALE_DOWN);
    widget_set_name(row, name);
    widget_on(row, EVT_CLICK, m1_home_click, row);
}

/* Tidal's main page with no session opens its login page from its init (tidal_tidal_main_init's navigator_to,
 * 0x4b9e98, CALL_SITES TIDAL_LOGIN). With a saved login it builds itself under the login and stays; without one it
 * returns unbuilt, so the login takes its place, as HiFi Music's page replaces itself with its login (0x487eec):
 * the login's Back (navigator_back, LOGIN_BACK) then returns to Streaming, not to an empty page. */
int m1_tidal_login(const char *name) {
    return theTidal[TIDAL_SAVED_LOGIN] ? navigator_to(name) : navigator_replace(name);
}

int streaming_open(void *ctx, void *event) {
    if (st.stream_page || !(st.stream_page = page_open("streaming_page", page_closed, page_keyup))) return 0;
    int apps = addon_scan(), soloify = soloify_installed();
    st.svc_n = apps + soloify;
    svc_soloify = soloify;
    char hide[SVC_HIDE];
    svc_hidden(hide);
    void *view = page_list(st.stream_page, st.stream_page, 0, "Streaming", 6 + apps + soloify, LIB_PITCH);
    widget_set_name(view, "scroll_view");
    /* Native Tidal had no visibility switch; retain that behavior and all existing service ids. */
    m1_native_row(view, "tidal", "1", "Tidal");
    m1_native_row(view, "hifimusic", "0", "HiFi Music"); /* V2.1's own store, a native Home card */
    m1_svc_row(library_into(view, "row_spotify", spot_open, 0, "Spotify"), 0, hide); /* stream_*'s at 40 px (tools/m1plus.py) */
    if (soloify) /* the second backend of the Spotify page, its icon Spotify's for now */
        m1_svc_row(library_into(view, "row_spotify", spot_open, (void *)1, "Soloify"), 1, hide);
    for (int k = 0; k < apps; ++k) /* the card apps on the card (addon.c), as Streaming lists them */
        m1_svc_row(library_into(view, "stream_app", addon_open, (void *)(long)k, addon_name(k)), k + 1 + soloify, hide);
    m1_svc_row(library_into(view, "row_radio", radio_open, 0, "Internet Radio"), st.svc_n + 1, hide);
    m1_svc_row(library_into(view, "stream_airplay", airplay_open, 0, "AirPlay"), st.svc_n + 2, hide);
    library_into(view, "row_stream_config", stream_config, 0, "Configuration");
    return 0;
}

int library_page_open(void *ctx, void *event) {
    (void)ctx;
    (void)event;
    if (st.lib_page || !(st.lib_page = page_open("library_page", page_closed, page_keyup))) return 0;
    static const char *const icons[] = { "local_podcasts", "local_audiobooks", "local_photos",
                                         "local_books", "local_videos" };
    char path[sizeof st.media_root];
    int media[VIDEOS], scrobbles = scrobble_ready(), n = 17 + scrobbles;
    for (int k = 0; k < VIDEOS; k++) n += media[k] = media_find(k + 1, path);
    void *view = page_list(st.lib_page, st.lib_page, 0, "Library", n, LIB_PITCH);
    library_into(view, "local_shuffle", shuffle_menu, 0, "Shuffle");
    m1_native_row(view, "songer", "6", "Artists");
    m1_native_row(view, "album", "5", "Albums");
    m1_native_row(view, "songsort", "3", "All Songs");
    m1_native_row(view, "genre", "7", "Genres");
    library_into(view, "local_era", era_menu, 0, "Era");
    m1_native_row(view, "playlist", "14", "Playlists");
    library_into(view, "local_fav", ratings_menu, 0, "Ratings");
    m1_native_row(view, "recentadd", "13", "Recently Added");
    m1_native_row(view, "recent", "12", "Recently Played");
    library_into(view, "local_frequentplay", most_played, 0, "Most Played");
    m1_native_row(view, "many", "11", "Frequent");
    m1_native_row(view, "hr", "9", "Hi-Res");
    library_into(view, "local_longsongs", long_songs, 0, "Long Songs");
    for (int k = 0; k < VIDEOS; k++)
        if (media[k])
            library_into(view, icons[k], k + 1 == VIDEOS ? videos_click : media_click, (void *)(long)(k + 1), MEDIA[k]);
    m1_native_row(view, "composer", "8", "Composers");
    if (scrobbles) library_row(view, "local_scrobble", upload_scrobbles, 0, "Upload Scrobbles");
    /* Maintenance last, as upstream's Update Local Music: V2.1's CD ripper card (the USB host for the drive) first. */
    m1_native_row(view, "cdripper", "15", "CD Ripper");
    m1_native_row(view, "sset_updatemusic", "2", "Update Local Music");
    return 0;
}
/* No Tidal Downloads row (navigation.c tidal_downloads, Streaming's on the Q2): on M1, tidal_start
 * passes no song id, so tidal_play downloads nothing (docs/m1plus-roadmap.md U4). Named here so the
 * M1 compile takes the unused page; nothing calls it, so it isn't linked. */
static void *const m1_unported_tidal_downloads __attribute__((unused)) = (void *)tidal_downloads;
/* No trailing dots on a playlist row (navigation.c more_image, the Q2's qm_hold, 1.3.8): they open
 * playlistsmore_page, which V2.1 doesn't have; the M1's hold opens the hold menu, whose More… is the
 * editor (m1plus_nav_playlist_hold.inc). Named as tidal_downloads is. */
static void *const m1_unported_more_image __attribute__((unused)) = (void *)more_image;
#endif
