/* M1 Plus: Now Playing's folder-image call (PLAYER_COVER). patch/coverflow.c includes this after
 * coverflow_player_cover, whose fallbacks these are. */
#if M1PLUS
/* V2.1's parseplaycover_thd makes the call under parse_cover_mutex, which the album grids' worker
 * and Coverflow's hold too (V2.1 has no player cover lock), so the folder images and ffmpeg run
 * with it dropped, as grid_cover's ffmpeg does: the paths are the thread's own. */
int m1plus_player_cover(const char *track, const char *dst, int w, int h) {
    if (toolsGetExternCover(track, dst, w, h) == 1) return 1;
    pthread_mutex_unlock((void *)parse_cover_mutex);
    int ok = beside_art(track, dst, w, h, 0, ff_thumb) || (!marked_empty(track) && ff_thumb(track, dst, w, h));
    pthread_mutex_lock((void *)parse_cover_mutex);
    return ok;
}
#endif
