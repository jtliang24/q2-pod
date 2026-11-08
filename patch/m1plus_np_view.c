/* M1 Plus: Now Playing's one set of painters, for the local page and Spotify's (m1plus_np_view.h). patch/navigation.c
 * includes this where the Q2 has its np_sync and np_theme. */
#if M1PLUS
/* "-" first when negative is 1, as clock_text, written only when it changed. */
static void np_clock(void *label, int negative, unsigned t) {
    char s[16] = "-";
    toolsTimeItoa(s + negative, (int)t);
    if (text_differs(label, s)) widget_set_text_utf8(label, s);
}

static void np_text(void *label, const char *s) {
    if (!label || !s || !text_differs(label, s)) return;
    widget_set_text_utf8(label, s);
    widget_set_prop_int(label, "xoffset", 0);
}

/* The page from its player. Labels are written only when their source changes; a new text or position restarts Minimal's
 * album marquee from its start (paint_caps). */
void np_write(np_view_t *v, const np_src_t *s) {
    const char *album = s->album ? s->album : "";
    unsigned pos[2] = { s->index, s->count };
    unsigned h = hash_bytes(fnv(FNV_SEED, (const unsigned char *)album), (const unsigned char *)pos, sizeof pos);
    if (s->title) h = fnv(h, (const unsigned char *)s->title);
    if (s->artist) h = fnv(h, (const unsigned char *)s->artist);
    if (h != v->hash) {
        char c[24] = "";
        v->hash = h;
        if (s->count) tk_snprintf(c, sizeof c, "%d of %d", s->index + 1, s->count);
        if (v->counter) widget_set_text_utf8(v->counter, c);
        np_text(v->title, s->title);
        np_text(v->artist, s->artist);
        np_text(v->album, album);
        st.np_off = 0;
        stop_timer(&st.np_marquee); /* the next paint restarts it if the album overflows */
    }
    v->bold = bold_label(v->title, v->bold); /* the title, as it changes */
    unsigned sec = s->pos_ms / 1000, total = s->dur_ms / 1000;
    if (v->elapsed) np_clock(v->elapsed, 0, sec);
    if (v->remain) np_clock(v->remain, 1, sec < total ? total - sec : 0);
    if (v->play && v->shown != (unsigned)s->playing + 1) {
        v->shown = (unsigned)s->playing + 1;
        widget_use_style(v->play, s->playing ? "btn_imgpause_style" : "btn_imgplay_style");
    }
}

/* The Theme, on a page's labels: stock's play-state glyph where it has one, which Minimal hides, and the album, which in
 * Minimal is paint_caps' capitals over its transparent label. */
void np_view_theme(const np_view_t *v) {
    void *glyph = v->win ? widget_lookup(v->win, "img_playstate", 1) : (void *)0;
    if (glyph) widget_set_opacity(glyph, ipod_classic() ? 255 : 0);
    if (v->album) widget_set_opacity(v->album, ipod_classic() ? 255 : 0);
}

/* The local page, by the names ringnav_playing looked up. */
static np_view_t np_view_local(void) {
    return (np_view_t){ .win = st.np_win, .title = st.np_title, .album = st.np_album, .remain = st.np_remain,
                        .counter = st.np_pos, .hash = st.np_hash, .bold = st.np_bold };
}

/* Local music: the queue's album and position, and the bar's second and length (stock's seconds, slider max less value, so
 * a drag or scrub previews the remaining time). */
static np_src_t np_src_local(void) {
    unsigned at, n;
    void *r = queue_now(&at, &n);
    return (np_src_t){ .album = now_tag(r, REC_ALBUM),
                       .pos_ms = (unsigned)widget_get_prop_int(st.np_slider, "value", 0) * 1000,
                       .dur_ms = (unsigned)widget_get_prop_int(st.np_slider, "max", 0) * 1000,
                       .index = at,
                       .count = r ? n : 0,
                       .playing = mclGetPlayStatus() == 2 };
}

static void np_sync(void *top) {
    if (!top || top != st.np_win) return;
    np_view_t v = np_view_local();
    np_src_t s = np_src_local();
    np_write(&v, &s);
    st.np_hash = v.hash;
    st.np_bold = v.bold;
}
#endif
