/* M1 Plus: the hold menu's dialog, opened non-modal as on the Q2. patch/navigation.c includes this where it stood (docs/m1plus-roadmap.md U1c). */
#if M1PLUS
int stock_sortselect_trampoline(void *, void *);
/* dialog_sortselect_dialog_init. V2.1's navigator runs a dialog modally (dialog_modal, its own
 * event loop until the dialog closes) when to_modal is set after its init, and V2.1's sortselect
 * leaves it at the default, set: navigator_to would return only once the menu had gone, and the
 * menu would show V2.1's sort rows. The hold menu's own open clears it, as V1.32's init does; a
 * sort dialog V2.1 opens itself stays modal. */
int qm_sortselect_init(void *win, void *ctx) {
    int result = stock_sortselect_trampoline(win, ctx);
    if (st.qm_opening && win) widget_set_prop_int(win, "to_modal", 0);
    return result;
}
#endif
