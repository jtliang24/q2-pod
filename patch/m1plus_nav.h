/* M1 Plus: navigation.c's declarations of the M1's own routines, and V2.1 stand-ins for V1.32 ones.
 * patch/navigation.c includes this after its headers (docs/m1plus-roadmap.md U1c). */
#if M1PLUS
/* V2.1 has only the per-corner form (V1.32's wrapper calls it so) */
#define canvas_stroke_rounded_rect(c, rect, s, color, radius, width)                              \
    canvas_stroke_rounded_rect_ex(c, rect, s, color, radius, radius, radius, radius, width, 0xffff)
extern int coverflow_centre(int x, int y); /* coverflow.c */
extern void video_touch(void *e);          /* books.c */
#endif
