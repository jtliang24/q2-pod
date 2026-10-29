/* V2.1 Streaming Configuration, included by navigation.c. */
static const char *const sc_dirs[] = { TIDAL_DIR, SPOT_DIR };

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

static void sc_text(int i) {
    static const char *const sizes[] = { "512 MB", "1 GB", "2 GB", "4 GB", "8 GB" };
    char s[40];
    tk_snprintf(s, sizeof s, "%s Cache: %s", i ? "Spotify" : "Tidal", sizes[stream_cache(i)]);
    widget_set_text_utf8(widget_get_child(st.sc_row[i], 0), s);
}

/* M1's Q2 Pod services: Spotify, installed card apps, Internet Radio, AirPlay. Native
 * Tidal stays on Home and has no switch; Tidal Downloads is unavailable. Keys and cache files
 * remain upstream's, so a card and its settings survive model changes. */
static const char *const svc_fixed[][2] = { { "SPOTIFY", "Spotify" },
    { "RADIO", "Internet Radio" }, { "AIRPLAY", "AirPlay" } };
/* Service i's key (label 0) or row label (1), as Streaming last listed them. */
static const char *svc(int i, int label) {
    if (i >= 1 && i < 1 + st.svc_n) return label ? addon_name(i - 1) : addon_id(i - 1);
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
 * Spotify's when librespot next starts. Stop Streaming Services ends librespot and its restart
 * loop, a radio station, the card apps (addon.c) and a stock stream (Tidal's) queue, so the keys
 * and the output are local music's again; local music already stopped is left as it is. */
static int sc_click(void *ctx, void *event) {
    int i = (int)(long)ctx;
    if (i > 3) return svc_toggle(i - 4);
    if (i == 2) {
        unsigned type = (unsigned)MCL(MCL_TYPE);
        spot_stop();
        radio_stop();
        addon_stop();
        if (type != 1 && (type & 0xf000) != 0xf000 && mclGetPlayStatus() != 1) player_stop();
        toast("Streaming stopped");
        return 0;
    }
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
    int n = 3 + st.svc_n;
    void *view = page_list(st.sc_page, st.sc_page, 0, "Configuration", 4 + n, PAGE_ROW_H);
    for (int i = 0; i < 2; ++i)
        st.sc_row[i] = page_row_detail(view, i, "", 0, sc_click), sc_text(i);
    page_row_detail(view, 2, "Stop Streaming Services", 0, sc_click);
    void *gap = list_item_create(view, 0, 3 * PAGE_ROW_H, UI_W, PAGE_ROW_H); /* a gap before the toggles */
    widget_use_style(gap, ROW_STYLE);
    widget_set_prop_int(gap, "style:normal:bg_color", (int)0xff000000u);
    char hide[SVC_HIDE];
    svc_hidden(hide);
    for (int i = 0; i < n; ++i) {
        st.sc_check[i] = widget_get_child(page_row_detail(view, 4 + i, "", 0, sc_click), 0);
        list_toggle(st.sc_check[i], svc(i, 1), !svc_find(hide, i));
    }
    return 0;
}

