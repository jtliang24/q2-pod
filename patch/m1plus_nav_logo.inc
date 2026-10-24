/* M1 Plus: logo_sync's checks of a 320x480 card logo. patch/navigation.c includes this where it stood (docs/m1plus-roadmap.md U1c). */
#if M1PLUS
    const char *err = "Boot logo must be a 320x480 JPEG";
    (void)unused;
    if (access(LOGO_SRC, 0))
        unlink(LOGO_DST), err = 0;
    else
        b = read_all(LOGO_SRC, LOGO_MAX, &n);
    if (b && jpeg_size(b, n) == (320u << 16 | 480)) {
#endif
