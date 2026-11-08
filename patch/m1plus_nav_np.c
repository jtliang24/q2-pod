/* M1 Plus: Knob: Navigation's press and turns on Now Playing. patch/m1plus_nav_back.c includes this (docs/m1plus-ipod-ui.md 4.6). */
#if M1PLUS
/* Now Playing keeps the knob's volume (knob_nav_active), so its press stays V2.1's power key, which
 * turns the screen off. Here a single press starts the scrub instead and a double press turns the
 * screen off, as a double Centre does on every list; the Q2's is the other way round (np_key). While
 * scrubbing, a press seeks to the target and ends it, and the turns move the target: clockwise
 * (volume up) forward in time, whichever way Knob Up sorts a list. Neither the volume nor its dialog
 * sees them. Keys that are not the knob's end the scrub and go on to V2.1. */

/* A single press, DOUBLE_CLICK_MS on with no second: the scrub, if Now Playing still waits for it. */
static int np_knob_single(const void *info) {
    (void)info;
    st.np_press = 0;
    void *top = window_manager_get_top_window(window_manager());
    if ((top == st.np_win || spot_knob_on(top)) && g_backlight_status && usable() && !st.scrub &&
        !window_manager_is_animating(window_manager()) &&
        !window_manager_get_pointer_pressed(window_manager())) {
        if (top == st.np_win)
            scrub_start();
        else
            spot_scrub_start();
    }
    return 0;
}

/* Returns whether it took the key. Spotify's page (ipod-ui 4.6, spot_knob_on) takes the press and the turns as this page does. */
static int np_knob_key(void *top, unsigned key, int boot_guard) {
    pod_settings();
    int spot = spot_knob_on(top);
    if (!st.knob_mode || (top != st.np_win && !spot) || !g_backlight_status || !usable() || bt__recv_pageflag ||
        window_manager_is_animating(window_manager()) ||
        window_manager_get_pointer_pressed(window_manager()))
        return 0;
    if (spot) {
        if (key == KEY_POWER && !boot_guard) {
            int press = center_press(&st.np_press, &st.np_press_at, np_knob_single, spot_scrubbing());
            if (press == 2 && !spot_scrubbing()) return 0;
            if (press != 1) spot_scrub_end();
            return 1;
        }
        if (!spot_scrubbing()) return 0;
        if (key == KEY_VOLUMEUP || key == KEY_VOLUMEDOWN) return spot_key(top, key == KEY_VOLUMEUP ? KEY_NEXT : KEY_PREV);
        spot_scrub_end();
        return 0;
    }
    if (key == KEY_POWER && !boot_guard) {
        int press = center_press(&st.np_press, &st.np_press_at, np_knob_single, st.scrub);
        if (press == 2 && !st.scrub) return 0; /* a double press: V2.1's, the screen off */
        if (press != 1) scrub_end(); /* a scrubbing press, or an overdue first's single ends at once */
        return 1;
    }
    if (!st.scrub) return 0;
    if (key == KEY_VOLUMEUP || key == KEY_VOLUMEDOWN)
        return np_key(top, key == KEY_VOLUMEUP ? KEY_NEXT : KEY_PREV);
    scrub_end();
    return 0;
}
#endif
