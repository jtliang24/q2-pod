/* M1 Plus: a playlist row's hold. patch/navigation.c includes this in qm_hold, where the Q2's opens
 * the playlist's More page (docs/m1plus-roadmap.md U4). */
#if M1PLUS
    /* It opens the playlist's editor: V2.1 has no playlistsmore_page, deletes playlists by its own
     * multi-select, and renames none. A playlist's list_item is named its pdeq_playlist index
     * (playlist_listitem_layout, 0x53e6d0), which its click reads too (0x53d34c); the page's New and
     * Import rows aren't numbers. The Add to Playlist picker shares the page's name, and its add mode
     * tells the two apart. */
    if (!tk_strcmp(name, "playlist_page") && !I(PLAYLIST_ADD_MODE, 0)) {
        const char *id = widget_get_prop_str(g_menu.at[cur], "name", "");
        if (*id < '0' || *id > '9' || (!key && !LP_TOUCH)) return 0;
        st.qm_press = LP_TOUCH ? 0 : *(unsigned long long *)((char *)key + INPUT_KEY_TIME);
        drop_input();
        ple_open((void *)(long)atoi(id), 0);
        return 1;
    }
#endif
