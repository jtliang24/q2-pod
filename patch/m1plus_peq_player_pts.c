/* M1 Plus: decoded() and LENGTH at V2.1's hciplayer addresses (tools/m1plus.py PLAYER_PROFILE passes them).
 * patch/peq_player.c includes this where upstream's stand (docs/m1plus-roadmap.md U1c). */
#if M1PLUS
/* written_audio_pts: seconds decoded so far, NOPTS (-2^63) without a stream;
 * the length is {media-info}'s whole seconds (demo's mclGetPlayTime). */
static double decoded(void) {
    char *mp = MPCTX, *sh = mp ? *(char **)(mp + 0x2c) : 0, *ds = mp ? *(char **)(mp + 0x34) : 0;
    return sh && ds ? ((double (*)(void *, void *))WRITTEN_AUDIO_PTS)(sh, ds) : -1;
}
#define LENGTH (*(volatile int *)LENGTH_ADDR)
#endif
