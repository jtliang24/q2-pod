/* M1 Plus: ringnav's knob: in Knob: Navigation the turns move the list and Previous goes back. patch/navigation.c includes this where it stood (docs/m1plus-roadmap.md U1c). */
#if M1PLUS
    int boot_guard = g_power_longkey || g_ingore_bootkey_flag || *(volatile unsigned char *)BOOT_KEY_GUARD;
    if (knob_nav_active()) {
        /* Knob Up: List Up, the default, takes the volume-up turn toward the list's top */
        unsigned up = st.knob_reverse ? KEY_NEXT : KEY_PREV, down = st.knob_reverse ? KEY_PREV : KEY_NEXT;
        if (key == KEY_VOLUMEUP) key = up, I(event, EVENT_KEY) = up;
        else if (key == KEY_VOLUMEDOWN) key = down, I(event, EVENT_KEY) = down;
        else if (key == KEY_POWER && !boot_guard) key = KEY_CENTER, I(event, EVENT_KEY) = KEY_CENTER;
        /* Previous is Back: the page's back button, pressed (Home has nothing to go back to: there
         * it stays Previous track). It is the button stock takes as Previous: V2.1 swaps the two
         * on a rotated screen (on_wm_keyup_fun, rotate_mode 1). knob_nav_active() already leaves a
         * dark screen and the key lock to stock. */
        else if (key == (g_rotate_mode == 1 ? KEY_FWD_BTN : KEY_BACK_BTN) &&
                 !home_menu(window_manager_get_top_window(window_manager()))) {
            timer_add(previous_back, 0, 0);
            return STOP;
        }
    }
#endif
