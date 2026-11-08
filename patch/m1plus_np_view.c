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

/* The accent's light tone (Minimal's own accent: MINIMAL_FILL) fills the progress bar; a white fill (Minimal: a thicker line,
 * its fill near white already) marks the scrub. The line stays centred in its widget. 32-bit to 57 h. */
np_bar_t np_bar_fill(unsigned pos_ms, unsigned dur_ms, int scrubbing, int w, int h) {
    int line = scrubbing ? NP_BAR_CLASSIC : np_bar_h(), x = (int)((pos_ms >> 4) * (unsigned)w / ((dur_ms >> 4) | 1));
    return (np_bar_t){ .x = x && x < line ? line : x,
                       .y = (h - line) / 2,
                       .h = line,
                       .radius = np_bar_h() / 2,
                       .fill = scrubbing ? 0xffffffffu : RGBA(accent_tone(TONE_LIGHT)),
                       .track = RGBA(TRACK_COLOR) };
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

/* np_sync writes in a paint, and AWTK drops what a paint invalidates. V2.1's own writes leave the top row out of the frame
 * when the cover stays, so a Next within an album kept the old count on screen until something repainted the row. Once,
 * after the frame. Spotify's page writes from its timer, which needs none of this. */
static int np_repaint(const void *info) {
    st.np_repaint = 0;
    if (st.np_pos) widget_invalidate_force(st.np_pos, (void *)0);
    if (st.np_album) widget_invalidate_force(st.np_album, (void *)0);
    return 0; /* RET_REMOVE */
}

static void np_sync(void *top) {
    if (!top || top != st.np_win) return;
    np_view_t v = np_view_local();
    np_src_t s = np_src_local();
    np_write(&v, &s);
    if (v.hash != st.np_hash) rearm(&st.np_repaint, np_repaint, 0);
    st.np_hash = v.hash;
    st.np_bold = v.bold;
}

/* The scrub, one for both pages: its state is st's, in the page's seconds, and st.scrub_page is whose it is while it runs and
 * settles. Elsewhere it is the local page's, which chapter_pick and ringnav_playing's held seek start directly.
 *
 * The local page follows stock's own key seek (0x52c754; docs/internals.md#scrub-ipod): its 250 ms timer stops, the slider and
 * label_playtime preview the target, player_seek_time commits it once on exit in track seconds (it adds a CUE track's start),
 * and the timer restarts. Spotify's page reads the target through np_scrub_shown, and seeks by its socket. */
static void np_local_read(np_src_t *s) { *s = np_src_local(); }
static void *np_local_bar(void) { return st.np_slider; }
static int np_local_second(void) {
    int sec = -1, total;
    player_playtime_and_length(&sec, &total);
    return sec;
}
static int np_local_status(void) { return mclGetPlayStatus(); }
static void np_local_seek(unsigned ms) { st.held_sec = seek_position((int)(ms / 1000)); }
static void np_local_hold(int on) {
    if (on)
        playing_timer_clear(st.np_win);
    else
        playing_timer_start(st.np_win);
}
static void np_local_preview(int sec) {
    widget_set_prop_int(st.np_slider, "value", sec);
    clock_text(st.np_elapsed, 0, sec);
    np_sync(st.np_win);
}
static const np_page_t np_local = { np_local_read, np_local_bar, np_track, np_local_second, np_local_status,
                                    np_local_seek, np_local_hold, np_fill, np_local_preview };

#define SCRUB_PAGE (st.scrub_page ? (const np_page_t *)st.scrub_page : &np_local)

/* The page on top, if it is a Now Playing with a bar to scrub. */
static const np_page_t *np_page_on(void *top) {
    return top && top == st.np_win ? &np_local : spot_np_page(top);
}

int np_scrubbing(const np_page_t *p) { return st.scrub && SCRUB_PAGE == p; }

/* What the page shows of a player at ms: the target, while the scrub runs or settles. */
unsigned np_scrub_shown(const np_page_t *p, unsigned ms) {
    return SCRUB_PAGE == p && (st.scrub || st.settle_timer) ? (unsigned)st.scrub_to * 1000 : ms;
}

/* Paused, the seek waits for Play (np_scrub_end) and the player's second stands still until then,
 * and the page's timer would put the bar back on it. The bar keeps the
 * target until the player reports it, the track changes or stops, or SETTLE_PLAY_MS of playing
 * pass without it; then the page's timer comes back. */
#define SETTLE_MS 250
#define SETTLE_PLAY_MS 2000
static int settle_poll(const void *info) {
    const np_page_t *p = SCRUB_PAGE;
    int sec = p->second(), status = p->status();
    if (status == 2) st.settle_played += SETTLE_MS;
    if (p->bar() && p->track() == st.scrub_track &&
        (sec < st.scrub_to - 1 || sec > st.scrub_to + 1) &&
        (status == 3 || (status == 2 && st.settle_played < SETTLE_PLAY_MS)))
        return 8; /* RET_REPEAT: paused, or not there yet */
    st.settle_timer = 0;
    st.scrub_page = (void *)0;
    if (p->bar()) p->hold(0);
    return 0;
}

/* Commits a target the wheel moved, unless the playing track changed since the scrub began; the
 * fill comes back, and the page's timer once the player is there (settle_poll), unless the page is
 * gone. */
void np_scrub_end(void) {
    if (!st.scrub) return;
    const np_page_t *p = SCRUB_PAGE;
    st.scrub = 0;
    stop_timer(&st.scrub_timer);
    int seek = st.scrub_moved && p->track() == st.scrub_track;
    if (seek) p->seek((unsigned)st.scrub_to * 1000);
    st.scrub_moved = 0;
    if (!p->bar()) {
        st.scrub_page = (void *)0;
        return;
    }
    st.settle_played = 0;
    if (seek) rearm(&st.settle_timer, settle_poll, SETTLE_MS); /* before the fill, which a page may read through it */
    p->fill(0);
    if (seek) return;
    st.scrub_page = (void *)0;
    p->hold(0);
}
#define scrub_end np_scrub_end

static int scrub_expire(const void *info) {
    st.scrub_timer = 0;
    scrub_end();
    return 0;
}

/* Starts a scrub on the page's bar: the target is where the bar is, the page's timer stops so it
 * cannot pull the fill back, and the fill goes to the scrub colour. */
void np_scrub_start(const np_page_t *p) {
    if (!p->bar()) return;
    np_src_t s;
    p->read(&s);
    st.scrub_page = p;
    st.scrub = 1;
    st.scrub_moved = 0;
    st.scrub_to = (int)(s.pos_ms / 1000);
    st.scrub_track = p->track();
    stop_timer(&st.settle_timer);
    p->hold(1);
    p->fill(1);
    rearm(&st.scrub_timer, scrub_expire, SCRUB_MS);
}

/* A finger on the page's bar: the target it holds, previewed as a scrub is, and seeking on its release. */
void np_scrub_drag(const np_page_t *p, int sec, int done) {
    if (!np_scrubbing(p)) np_scrub_start(p);
    st.scrub_to = sec;
    st.scrub_moved = 1;
    if (done) {
        np_scrub_end();
        return;
    }
    p->preview(sec);
    rearm(&st.scrub_timer, scrub_expire, SCRUB_MS);
}

static void np_cancel(void) {
    unsigned settle = st.settle_timer; /* an earlier scrub's wait; the one scrub_end arms stays */
    const np_page_t *p = SCRUB_PAGE;
    stop_timer(&st.np_press);
    scrub_end();
    if (!settle) return;
    stop_timer(&st.settle_timer);
    st.scrub_page = (void *)0;
    if (p->bar()) p->hold(0);
}

/* A page closing: its target is dropped, no seek, as np_gone's. */
void np_scrub_gone(const np_page_t *p) {
    if (SCRUB_PAGE != p) return;
    st.scrub_moved = 0;
    np_cancel();
}

/* A single centre press, DOUBLE_CLICK_MS on, never while scrubbing: it replays the release to stock
 * on_wm_keyup_fun, which turns the screen off (it reads only the event's key). */
static int np_single(const void *info) {
    static const unsigned release[EVENT_KEY / 4 + 1] = { [EVENT_KEY / 4] = WM_KEY_SLEEP };
    st.np_press = 0;
    if (g_backlight_status) on_wm_keyup_fun((void *)0, (void *)release);
    return 0;
}

/* Centre and, while scrubbing, the wheel on the top Now Playing page. A centre press waits
 * DOUBLE_CLICK_MS: a second one starts scrub, else it turns the screen off as anywhere else; while
 * scrubbing one press ends it at once (center_press). The wheel moves the target SCRUB_STEP
 * seconds times the WHEEL_RAMP_MS ramp, within the track, and only previews it: the seek waits
 * for the scrub to end. Neither the volume nor its dialog sees the wheel. */
static int np_key(void *top, unsigned key) {
    unsigned now = (unsigned)time_now_ms();
    const np_page_t *p = np_page_on(top);
    if (key == KEY_CENTER) {
        int press = center_press(&st.np_press, &st.np_press_at, np_single, st.scrub);
        if (press != 2) return press ? STOP : 0;
        if (st.scrub) /* one press ends a scrub, a double press starts one */
            scrub_end();
        else
            np_scrub_start(p);
        return STOP;
    }
    if (p->track() != st.scrub_track) { /* a new track: scrub_end drops the last one's target */
        scrub_end();
        return STOP;
    }
    int dir = key == KEY_NEXT ? 1 : -1;
    /* the step grows while the wheel spins: every tick counts, on the ramp lists had before */
    int step = SCRUB_STEP * ramp(top, p->bar(), 0, -1, dir, now, WHEEL_RAMP_MS, WHEEL_RAMP_MS);
    np_src_t s;
    p->read(&s);
    int to = clamp_step(st.scrub_to, (int)(s.dur_ms / 1000), dir * step);
    if (to != st.scrub_to) st.scrub_moved = 1;
    st.scrub_to = to;
    p->preview(to);
    rearm(&st.scrub_timer, scrub_expire, SCRUB_MS);
    return STOP;
}
#endif
