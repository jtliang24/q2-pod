/* M1 Plus: mp3_seek's stock routine and flag at V2.1's hciplayer addresses (tools/m1plus.py PLAYER_PROFILE).
 * patch/peq_player.c includes this after upstream's (docs/m1plus-roadmap.md U1c). */
#if M1PLUS
#undef STOCK_SEEK
#undef HR_MP3_SEEK
#define STOCK_SEEK ((void (*)(void *, float, float, int))STOCK_SEEK_ADDR)
#define HR_MP3_SEEK (*(volatile int *)HR_MP3_SEEK_ADDR)
/* 1.5.5's MP3 delay/padding trim needs V2.1's decoder sites before it can run.
 * Keep the shared seek notification inert until that port (m1plus-unported.md). */
void mp3_gapless_seek(void *demuxer, int at_start) {
    (void)demuxer, (void)at_start;
}
#endif
