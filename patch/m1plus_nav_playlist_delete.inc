/* M1 Plus: Delete on Library -> Playlists' multi-select. patch/navigation.c includes this where the Q2's
 * ringnav_playlist_delete stands (docs/m1plus-unported.md, "Playlist allocation and deletion"). */
#if M1PLUS
/* V2.1 has no playlistsmore_page: playlist_page's Delete button (its click, 0x53dbcc) deletes the rows ticked in
 * pvec_selectrecord. Stock's batch_delete_file (0x4e1408) deletes each header, then its entries, every statement
 * its own write with its result ignored, and always says msg_delplaylistsuccess. Here every ticked playlist goes
 * in one BEGIN IMMEDIATE transaction, each header checked by changes(), and success is said only after the commit;
 * a failure rolls back, keeps every playlist and says so. Stock's empty-selection message and confirm stay. */
int ringnav_playlist_delete(void *ctx, void *event) {
    void *list = P(p_deque_playlist, 0), *chosen = P(p_vector_select_record, 0), *db = 0;
    struct {
        int kind, ms;
        char text[0x400];
    } info = { 1, 2000, { 0 } };
    if (!list || !chosen || select_recordempty()) {
        getFormatString("msg_delplaylistfailed", info.text, 0x200);
        navigator_to_with_context("dialog/msginfo_dialog", &info);
        return 0;
    }
    info.ms = 0;
    getFormatString("msg_delplaylist", info.text, 0x200);
    if (confirm_over(&info, "Delete") != 10) return 0;
    unsigned n = vector_size(chosen), rows = deque_size(list);
    int ok = 0;
    char sql[256];
    if (sqlite3_open("/mnt/data/database.db", &db)) goto done;
    if (sqlite3_exec(db, "begin immediate", 0, 0, 0)) goto done;
    for (unsigned i = 0; i < n && i < rows; ++i) {
        if (!*(int *)vector_at(chosen, i)) continue;
        int id = I(deque_at(list, i), REC_ID);
        tk_snprintf(sql, sizeof sql,
                    "delete from playlist where id=%d;select changes();"
                    "delete from playlist where id>100 and cd_num=%d",
                    id, id);
        if (id < 0 || id >= 100 || sqlite3_exec(db, sql, ple_changed, 0, 0)) goto rollback;
    }
    if (sqlite3_exec(db, "commit", 0, 0, 0)) goto rollback;
    ok = 1;
    goto done;
rollback:
    sqlite3_exec(db, "rollback", 0, 0, 0);
done:
    if (db) sqlite3_close(db);
    if (ok) {
        g_delete_flag = 1;
        info.ms = 2000;
        getFormatString("msg_delplaylistsuccess", info.text, 0x200);
        navigator_to_with_context("dialog/msginfo_dialog", &info);
    } else
        toast("Could not delete playlist");
    return 0;
}
#endif
