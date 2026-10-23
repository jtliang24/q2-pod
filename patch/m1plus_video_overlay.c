/* M1 Plus: the position bar on the upright panel. patch/video.c includes this where it stood (docs/m1plus-roadmap.md U1c). */
#if M1PLUS
#define M1_BAR_X 20
void overlay(unsigned char *f, unsigned line, int n, int total) {
    int end = H - M1_BAR_X;
    if (total <= 0) return;
    n = n < 0 ? 0 : n > total ? total : n;
    int fill = M1_BAR_X + (end - M1_BAR_X) * n / total; /* total: seconds, far below overflow */
    for (int y = H - BAR_Y - BAR_H; y < H - BAR_Y; ++y)
        for (int x = M1_BAR_X; x < end; ++x) memset(f + y * line + x * 4, x < fill ? 0xff : 0, 4);
}
#endif
