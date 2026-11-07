/* M1 Plus: System Setting in the iPod's order. patch/navigation.c includes this before ringnav_systemset
 * (docs/m1plus-ipod-ui.md item 3). */
#if M1PLUS
/* Whether w, or a widget under it, draws the image named image (a V2.1 row's icon). */
static int draws_image(void *w, const char *image, int depth) {
    const char *name = w ? widget_get_prop_str(w, "image", (void *)0) : 0;
    if (name && !tk_strcmp(name, image)) return 1;
    for (unsigned i = 0, n = depth < 4 && w ? widget_count_children(w) : 0; i < n; ++i)
        if (draws_image(widget_get_child(w, i), image, depth + 1)) return 1;
    return 0;
}
/* view's last row: the one list_row or list_row_into has just added. */
static void *last_row(void *view) {
    unsigned n = view ? widget_count_children(view) : 0;
    return n ? widget_get_child(view, n - 1) : (void *)0;
}
/* The rows by role, as the Q2's sysset_order has them, then V2.1's extras, then maintenance, About last (the
 * user's order, Nov 6). V2.1's builder (systemset_sysset_page_init) makes a row per syssetMenu entry, its icon
 * get_systemset_showinfo's (two tables, which differ only in Double Tap's icon, by a GPIO), and its click reads
 * the row's name, which is its menu index, so restacking keeps each click. The payload's two rows are matched by
 * pointer: App Store draws system_update as Update does, Boot to sset_powermanager as Idle does. */
#define SYSSET_BOOT ((const char *)1)
#define SYSSET_APPS ((const char *)2)
#define SYSSET_OTHER ((const char *)3) /* a row matching no role (a later firmware's, or sset_prove) */
static const char *const sysset_roles[] = {
    "sset_wifiset",    "sset_netservice", "sset_display",      "sset_powermanager" /* Idle */,
    "sset_keylock" /* Buttons lock */,    "system_time",       "system_language",
    "sset_carmode" /* In-Vehicle */,      SYSSET_BOOT,         SYSSET_APPS,
    "sset_doublewake", "sset_tswake" /* Double Tap to Turn On */, "system_scrotate", "sset_theme",
    SYSSET_OTHER,      "system_update",   "system_reset",      "system_formatcard",
    "sset_about",
};
#define SYSSET_ROLES (sizeof sysset_roles / sizeof *sysset_roles)
static unsigned sysset_role(void *row, void *apps, void *boot) {
    const char *want = row == apps ? SYSSET_APPS : row == boot ? SYSSET_BOOT : 0;
    unsigned other = 0;
    for (unsigned k = 0; k < SYSSET_ROLES; ++k) {
        const char *role = sysset_roles[k];
        int named = role != SYSSET_BOOT && role != SYSSET_APPS && role != SYSSET_OTHER;
        if (role == SYSSET_OTHER) other = k;
        if (want ? role == want : named && draws_image(row, role, 0)) return k;
    }
    return other;
}
/* Restacks the rows once, after the payload's are added (apps, App Store, and boot, Boot to, or 0 without
 * Rockbox), each role in its place, rows of one role in V2.1's order. App Store opens a page, so it draws V2.1's
 * chevron, as page_row_into's rows do. */
static void sysset_ipod_order(void *view, void *apps, void *boot) {
    void *rows[32];
    unsigned char role[32];
    unsigned n = view ? widget_count_children(view) : 0;
    if (apps) image_base_set_image(image_create(apps, 295, 21, 13, 22), ROW_CHEVRON);
    if (n > sizeof rows / sizeof *rows) return;
    for (unsigned i = 0; i < n; ++i) {
        rows[i] = widget_get_child(view, i);
        role[i] = sysset_role(rows[i], apps, boot);
    }
    unsigned at = 0;
    for (unsigned k = 0; k < SYSSET_ROLES; ++k)
        for (unsigned i = 0; i < n; ++i)
            if (role[i] == k) widget_restack(rows[i], at++);
}
#endif
