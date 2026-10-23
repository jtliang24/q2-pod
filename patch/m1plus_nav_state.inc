/* M1 Plus: the M1's fields of scratch_t. patch/navigation.c includes this where it stood (docs/m1plus-roadmap.md U1c). */
#if M1PLUS
    /* A touch long-press (lp_input): its timer, the page and point pressed, set while qm_hold
     * takes the row under that point (lp_touch), and the press's click to swallow. */
    unsigned lp_timer;
    void *lp_top;
    int lp_x, lp_y, lp_touch, lp_swallow;
    /* A finger on a carousel (slide_swipe): its slide_menu, px to an item, the press's x and
     * time, the offset then, and whether it has moved far enough to drag. */
    void *sw_slide;
    unsigned sw_at;
    int sw_px, sw_x, sw_live, sw_drag;
    int qm_opening; /* qm_open's navigator_to is running: its sortselect_dialog is the menu */
    void *lib_page; /* the Q2 Pod Home card's page (library_open) */
#endif
