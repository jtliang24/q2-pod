/* M1 Plus: the album rows' art keys on V2.1's album_page. patch/navigation.c includes this where it stood (docs/m1plus-roadmap.md U1c). */
#if M1PLUS
static const char *page_key(char *buf, void *list, unsigned i) {
    const char *k = artist_key(buf, list, i);
    return k ? k : split_key(buf, list, i);
}
/* album_page's albumcoverinfo_init calls (0x524720, 0x524760, 0x5248d0), an artist's albums too. */
int ringnav_albumcovers(void *list) { return rename_covers(list, page_key); }
#endif
