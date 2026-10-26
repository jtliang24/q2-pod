/* M1 Plus: a hold's row on an album's tracks. patch/navigation.c includes this in qm_hold, in place of
 * the Q2's showlist check (docs/m1plus-roadmap.md U4). */
#if M1PLUS
    /* V2.1's albuminfo_page heads its tracks with the album's cover and Play All, a tap target of its
     * own, so its entries are the showlist's rows after those: a hold on them holds nothing. */
    unsigned head = list && !tk_strcmp(name, "albuminfo_page") && (unsigned)g_menu.rows > deque_size(list)
                        ? (unsigned)g_menu.rows - deque_size(list)
                        : 0;
    if (!list || head > 2 || deque_size(list) + head != (unsigned)g_menu.rows || (unsigned)g_menu.id[cur] < head)
        return 0;
    void *r = deque_at(list, g_menu.id[cur] - head);
#endif
