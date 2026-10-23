/* M1 Plus: MP3 ReplayGain through V2.1's ID3v2 walker, whose arguments are swapped. patch/peq_player.c includes this where it stood (docs/m1plus-roadmap.md U1c). */
#if M1PLUS
int id3_gain(int version, void *s) {
    long long at = AT(s, 0x30, long long) + AT(s, 0x28, int) - AT(s, 0x2c, int) - 10; /* stream_tell */
    int ret = STOCK_ID3(version, s);
    int fd = AT(s, 0x14, int);
    long long back = lseek64(fd, 0, 1);
    unsigned char h[10], f[256];
    char t[256];
    void *dict = 0;
    if (back >= 0 && lseek64(fd, at, 0) == at && read(fd, h, 10) == 10 && !memcmp(h, "ID3", 3) &&
        (h[3] == 3 || h[3] == 4)) {
        int v4 = h[3] == 4;
        long long end = at + 10 + id3_int(h + 6, 1);
        at += 10;
        if (h[5] & 0x40 && read(fd, h, 4) == 4) at += v4 ? id3_int(h, 1) : 4 + id3_int(h, 0); /* extended header */
        while (at + 10 <= end && lseek64(fd, at, 0) == at && read(fd, h, 10) == 10 && h[0]) {
            unsigned n = id3_int(h + 4, v4), k, key;
            if (!memcmp(h, "TXXX", 4) && n <= sizeof f && read(fd, f, n) == (int)n &&
                (k = id3_txxx(f, n, t, sizeof t)) > (key = strlen(t)) + 1)
                AV_DICT_SET(&dict, t, t + key + 1, 0);
            at += 10 + n;
        }
        RG_EXPORT(0, dict);
        AV_DICT_FREE(&dict);
    }
    if (back >= 0) lseek64(fd, back, 0);
    return ret;
}
#endif
