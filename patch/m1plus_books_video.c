/* M1 Plus: quitting a video with a tap on q2video's back chevron. patch/books.c includes this where it stood (docs/m1plus-roadmap.md U1c). */
#if M1PLUS
/* ringnav_input's touches while q2video plays. M1 Plus has no Return key: q2video draws a back
 * chevron at the top left (video.c back_glyph), and a tap pressed and lifted in its VIDEO_BACK_PX
 * square there quits, as Return does. Any other touch does nothing. */
#define VIDEO_BACK_PX 64 /* video.c BACK_PX */
void video_touch(void *e) {
    unsigned type = (unsigned)I(e, EVENT_TYPE);
    int in = I(e, EVENT_X) < VIDEO_BACK_PX && I(e, EVENT_Y) < VIDEO_BACK_PX;
    if (type == EVT_INPUT_POINTER_DOWN)
        vid.back = in;
    else if (type == EVT_INPUT_POINTER_MOVE)
        vid.back &= in;
    else if (type == EVT_POINTER_UP) {
        if (vid.back && in) video_key(KEY_RETURN);
        vid.back = 0;
    }
}
#endif
