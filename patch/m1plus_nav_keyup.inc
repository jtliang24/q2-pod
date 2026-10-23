/* M1 Plus: ringnav's media keys, taken before V2.1's on_wm_keyup_fun, which ringnav hooks. patch/navigation.c includes this where it stood (docs/m1plus-roadmap.md U1c). */
#if M1PLUS
    /* V2.1 has no key-up filter: this hooks on_wm_keyup_fun itself, which plays, skips and wakes
     * as it runs and returns 0. So the keys taken below are taken before it, and its key lock
     * (screen off, locked, mode other than 1: 0x4cda44) is kept. */
    int locked = !g_backlight_status && g_keylock_flag && g_keylock_mode != 1;
    if (key == KEY_PLAY && hold_released()) return STOP;
    if (!locked && media_owner() != 1 &&
        (key == KEY_PLAY || key == KEY_FWD_BTN || key == KEY_BACK_BTN)) {
        media_key(key);
        return STOP;
    }
    int result = stock_keyup_trampoline(ctx, event);
#endif
