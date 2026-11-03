/* V2.1 Streaming Configuration, included by navigation.c. */
static const char *const sc_dirs[] = { TIDAL_DIR, SPOT_DIR };
extern int spot_soloify_running(void); /* spotify.c */
/* Soloify's card settings, read by its relay when it connects (docs/wire.md): .delay (ms, none for
 * Auto) and .quality (kbit/s, none for the bridge's 160). */
#define SOLOIFY_DELAY SOLOIFY_DIR "/.delay"
#define SOLOIFY_QUALITY SOLOIFY_DIR "/.quality"
static int svc_soloify __attribute__((section(".scratch"))); /* its row is on Streaming, so on Configuration */
static void *sc_soloify[2] __attribute__((section(".scratch"))); /* its Delay and Quality rows */
static int soloify_installed(void) { return !access(SOLOIFY_DIR "/q2-soloify", 0); }

/* The choice i, the cap being 512 << i MB: 2 (2 GB) when the file is missing or holds another. */
int stream_cache(int spotify) {
    char path[48], s[12];
    tk_snprintf(path, sizeof path, "%s/.cache-size", sc_dirs[spotify]);
    state_read(path, s, sizeof s);
    unsigned mb = (unsigned)atoi(s + 1);
    for (int i = 0; i < 5; ++i)
        if (mb == 512u << i) return i;
    return 2;
}

/* Row i's caption: a cache row's size, or Erase Spotify Data's state. */
static void sc_text(int i) {
    static const char *const sizes[] = { "512 MB", "1 GB", "2 GB", "4 GB", "8 GB" };
    char s[40];
    if (i < 2)
        tk_snprintf(s, sizeof s, "%s Cache: %s", i ? "Spotify" : "Tidal", sizes[stream_cache(i)]);
    widget_set_text_utf8(widget_get_child(st.sc_row[i], 0),
                         i < 2            ? s
                         : shelf_erase(0) ? "Erasing…"
                         : st.sc_armed    ? "Press again to erase the login and cache"
                                          : "Erase Spotify Data");
}

/* netupdate.c's erase ended: .cache-size went with it, so Spotify's row reads 2 GB again. */
void stream_erased(void) {
    if (st.sc_page) sc_text(1), sc_text(2);
}

static const unsigned sc_delays[] = { 0, 1000, 2000, 4000, 8000 }; /* ms; 0 is Auto: 1 s on the LAN, 4 s beyond */
static const unsigned sc_rates[] = { 96, 128, 160 };

/* The choice in a Soloify setting's file: its index in values, the file missing or holding another
 * giving fallback. */
static int sc_soloify_choice(const char *path, const unsigned *values, int n, int fallback) {
    char s[12];
    state_read(path, s, sizeof s);
    unsigned v = (unsigned)atoi(s + 1);
    for (int i = 0; i < n; ++i)
        if (v == values[i]) return i;
    return fallback;
}

static void sc_soloify_text(int i) {
    char s[40];
    if (i == 0) {
        int d = sc_soloify_choice(SOLOIFY_DELAY, sc_delays, 5, 0);
        if (d) tk_snprintf(s, sizeof s, "Soloify Delay: %u s", sc_delays[d] / 1000);
        else tk_snprintf(s, sizeof s, "Soloify Delay: Auto");
    } else
        tk_snprintf(s, sizeof s, "Soloify Quality: %u kbit/s", sc_rates[sc_soloify_choice(SOLOIFY_QUALITY, sc_rates, 3, 2)]);
    widget_set_text_utf8(widget_get_child(sc_soloify[i], 0), s);
}

/* Soloify's relay reads these when it connects, so a change stops a running Soloify: the next open
 * starts it with the new value. */
static void sc_soloify_click(int i) {
    char s[12], tmp[40];
    const char *path = i ? SOLOIFY_QUALITY : SOLOIFY_DELAY;
    int n, next = i ? (sc_soloify_choice(path, sc_rates, 3, 2) + 1) % 3 : (sc_soloify_choice(path, sc_delays, 5, 0) + 1) % 5;
    unsigned v = i ? sc_rates[next] : sc_delays[next];
    if (!v) { /* Auto: no file */
        unlink(path);
    } else {
        n = tk_snprintf(s, sizeof s, "%u", v);
        tk_snprintf(tmp, sizeof tmp, "%s.tmp", path);
        if (!blob_io(path, tmp, s, (unsigned)n, 1)) toast("Could not save setting");
    }
    sc_soloify_text(i);
    if (spot_soloify_running()) {
        spot_stop();
        toast("Soloify stopped to apply it");
    }
}

/* M1's Q2 Pod services: Spotify, Soloify if installed, installed card apps, Internet Radio, AirPlay. Native
 * Tidal stays on Home and has no switch; Tidal Downloads is unavailable. Keys and cache files
 * remain upstream's, so a card and its settings survive model changes. */
static const char *const svc_fixed[][2] = { { "SPOTIFY", "Spotify" },
    { "RADIO", "Internet Radio" }, { "AIRPLAY", "AirPlay" } };
/* Service i's key (label 0) or row label (1), as Streaming last listed them. */
static const char *svc(int i, int label) {
    if (i == 1 && svc_soloify) return label ? "Soloify" : "SOLOIFY";
    if (i >= 1 && i < 1 + st.svc_n) return label ? addon_name(i - 1 - svc_soloify) : addon_id(i - 1 - svc_soloify);
    return svc_fixed[i < 1 ? i : i - st.svc_n][label];
}
static void svc_hidden(char *s) {
    /* V2.1 leaves the destination untouched for a missing key and an empty default. */
    s[0] = 0;
    toolsReadConfig("/mnt/data/config.ini", "Q2POD", "STREAMHIDE", s, "");
}
static char *svc_find(char *hide, int i) {
    const char *key = svc(i, 0);
    return key ? csv_find(hide, key) : 0;
}
/* A switch row's Centre: the service hidden, or shown again, and saved; its switch and its row on
 * Streaming (the page under this one) follow at once. ponytail: an uninstalled app's key stays
 * in STREAMHIDE (hidden again if it comes back); a list full of them (ROOT_MAX) refuses more. */
static int svc_toggle(int i) {
    char hide[SVC_HIDE];
    const char *key = svc(i, 0);
    if (!key) return 0;
    svc_hidden(hide);
    /* ROOT_MAX, not sizeof hide: stock's config line (a 257-byte sprintf, a 255-byte fgets) */
    int hidden = csv_toggle(hide, ROOT_MAX, key);
    if (hidden < 0) {
        toast("Could not save setting");
        return 0;
    }
    toolsWriteConfig("/mnt/data/config.ini", "Q2POD", "STREAMHIDE", hide);
    list_toggle(st.sc_check[i], svc(i, 1), !hidden);
    void *view = st.lib_page ? widget_lookup(st.lib_page, "scroll_view", 1) : 0;
    for (unsigned c = 0, rows = view ? widget_count_children(view) : 0; c < rows; ++c)
        if (widget_get_prop_int(widget_get_child(view, c), SVC_PROP, 0) == i + 1)
            widget_set_visible(widget_get_child(view, c), !hidden, 0);
    if (view) widget_layout(view);
    return 0;
}

/* A cache row steps to the next size and saves it: Tidal's applies at the next download's trim,
 * Spotify's when librespot next starts. Erase Spotify Data wants a second press in a row, as the
 * App Store's Remove: any other row's press or leaving the page drops the first. Stop Streaming
 * Services ends librespot and its restart loop, a radio station, the card apps (addon.c) and a
 * stock stream (Tidal's) queue, so the keys and the output are local music's again; local music
 * already stopped is left as it is. */
static int sc_click(void *ctx, void *event) {
    int i = (int)(long)ctx, x = svc_soloify ? 2 : 0; /* x: Soloify's two rows after Erase */
    st.sc_armed = i == 2 && !st.sc_armed && !shelf_erase(0); /* erasing: says to wait */
    if (i == 2 && !st.sc_armed) shelf_erase(1);
    sc_text(2);
    if (i > 4 + x) return svc_toggle(i - 5 - x);
    if (i == 2) return 0;
    if (x && (i == 3 || i == 4)) return sc_soloify_click(i - 3), 0;
    if (i == 3 + x) {
        unsigned type = (unsigned)MCL(MCL_TYPE);
        spot_stop();
        radio_stop();
        addon_stop();
        if (type != 1 && (type & 0xf000) != 0xf000 && mclGetPlayStatus() != 1) player_stop();
        toast("Streaming stopped");
        return 0;
    }
    if (i == 1 && shelf_erase(0)) return toast("Wait for the one in progress"), 0; /* it rm -rfs */
    char path[48], tmp[52], s[8];
    int n = tk_snprintf(s, sizeof s, "%uM", 512u << (stream_cache(i) + 1) % 5);
    tk_snprintf(path, sizeof path, "%s/.cache-size", sc_dirs[i]);
    tk_snprintf(tmp, sizeof tmp, "%s.tmp", path);
    mkdir(sc_dirs[i], 0755);
    if (!blob_io(path, tmp, s, (unsigned)n, 1)) toast("Could not save setting");
    sc_text(i);
    return 0;
}

static int stream_config(void *ctx, void *event) {
    if (st.sc_page || !(st.sc_page = page_open("streamconf_page", page_closed, page_keyup)))
        return 0;
    int n = 3 + st.svc_n, x = svc_soloify ? 2 : 0;
    void *view = page_list(st.sc_page, st.sc_page, 0, "Configuration", 5 + n + x, PAGE_ROW_H);
    for (int i = 0; i < 3; ++i)
        st.sc_row[i] = page_row_detail(view, i, "", 0, sc_click), sc_text(i);
    for (int i = 0; i < x; ++i) /* Soloify's Delay and Quality, while it is on the card */
        sc_soloify[i] = page_row_detail(view, 3 + i, "", 0, sc_click), sc_soloify_text(i);
    page_row_detail(view, 3 + x, "Stop Streaming Services", 0, sc_click);
    void *gap = list_item_create(view, 0, (4 + x) * PAGE_ROW_H, UI_W, PAGE_ROW_H); /* a gap before the toggles */
    widget_use_style(gap, ROW_STYLE);
    widget_set_prop_int(gap, "style:normal:bg_color", (int)0xff000000u);
    char hide[SVC_HIDE];
    svc_hidden(hide);
    for (int i = 0; i < n; ++i) {
        st.sc_check[i] = widget_get_child(page_row_detail(view, 5 + x + i, "", 0, sc_click), 0);
        list_toggle(st.sc_check[i], svc(i, 1), !svc_find(hide, i));
    }
    return 0;
}

