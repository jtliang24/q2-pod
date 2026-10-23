/* M1 Plus: tk_strcmp, which V2.1 lacks. patch/peq.h includes this where it stood (docs/m1plus-roadmap.md U1c). */
#if M1PLUS
/* V2.1 has no tk_strcmp. AWTK's, which the Q2 calls, takes NULL, and the payload relies on it: V2.1's
 * widget_get_prop_str returns NULL, not the default, for a value that is unset or empty (a label
 * with no text yet, an image with none), and Internet Radio's first station crashed demo there. */
static inline int tk_strcmp_m1(const char *a, const char *b) {
    return a == b ? 0 : !a ? -1 : !b ? 1 : strcmp(a, b);
}
#define tk_strcmp tk_strcmp_m1
#endif
