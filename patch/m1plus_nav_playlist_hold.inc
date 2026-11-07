/* M1 Plus: a playlist row's hold. patch/navigation.c includes this in qm_hold, where the Q2's opens
 * the playlist's hold menu (docs/m1plus-roadmap.md U4, docs/m1plus-ipod-ui.md 4.4). */
#if M1PLUS
    /* It opens the hold menu's playlist rows (QM_PLAYLIST: Play Next, Add to Queue, Shuffle, More…), as the Q2's
     * does; More… opens the playlist's editor (qm_run), as V2.1 has no playlistsmore_page, deletes playlists by its
     * own multi-select, and renames none. A playlist's list_item is named its pdeq_playlist index
     * (playlist_listitem_layout, 0x53e6d0), which its click reads too (0x53d34c); the page's New and Import rows
     * aren't numbers. The Add to Playlist picker shares the page's name, and its add mode tells the two apart. */
    if (!tk_strcmp(name, "playlist_page")) {
        if (I(PLAYLIST_ADD_MODE, 0)) return 0; /* the picker keeps stock's hold; never fall through to song rows */
        const char *id = widget_get_prop_str(g_menu.at[cur], "name", "");
        void *lists = P(p_deque_playlist, 0);
        unsigned at = (unsigned)atoi(id);
        void *r = *id >= '0' && *id <= '9' && lists && at < deque_size(lists) ? deque_at(lists, at) : 0;
        if ((!key && !LP_TOUCH) || !r || !(st.qm_timer = timer_add(qm_open, (void *)0, 0))) return 0;
        st.qm_kind = QM_PLAYLIST;
        st.qm_cls = 0xf001; /* its songs load as a song list, as Shuffle's (play_folder) */
        st.qm_idx = at;
        st.qm_rows = deque_size(lists);
        st.qm_hash = rec_hash(r);
        st.qm_press = LP_TOUCH ? 0 : *(unsigned long long *)((char *)key + INPUT_KEY_TIME);
        drop_input();
        return 1;
    }
#endif
