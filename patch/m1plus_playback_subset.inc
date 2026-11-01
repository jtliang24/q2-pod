/* M1 Plus: a library subset's queue across a power-off (docs/m1plus.md). patch/playback.c includes this
 * before stock_memory, which calls subset_only, and ringnav_savequeue subset_save. */
#if M1PLUS
#define SUBSET_FILE "/mnt/data/ringnav-subset"
/* Without advanced play, an all-songs class queue (0xf001) built from some of the library (an era's
 * Play All, Most Played, Ratings, Long Songs) came back as the whole library: stock's resume rebuilds
 * the class. Power-off keeps its tracks in order here, as {checksum, n, size} and each track's
 * identity and path, as the snapshot's; the restore narrows stock's rebuild back to them. */
static void subset_save(void) {
    void *q = queue();
    unsigned n = q ? deque_size(q) : 0, size = 12;
    for (unsigned i = 0; i < n && size; ++i) {
        const char *path = P(deque_at(q, i), REC_PATH);
        unsigned len = path ? strlen(path) : 0;
        size = len && len < 1024 ? size + 12 + len + 1 : 0;
    }
    unsigned char *buf = !s.active && M(MCL_TYPE) == 0xf001 && n && n <= SAVE_LIMIT && size ? calloc(size, 1) : 0;
    if (!buf) {
        unlink(SUBSET_FILE);
        return;
    }
    unsigned char *p = buf + 12;
    for (unsigned i = 0; i < n; ++i) {
        void *r = deque_at(q, i);
        const char *path = P(r, REC_PATH);
        unsigned identity[] = { strlen(path) + 1, (unsigned)I(r, REC_CUE_START), (unsigned)I(r, REC_CUE_END) };
        memcpy(p, identity, sizeof identity);
        memcpy(p + sizeof identity, path, identity[0]);
        p += sizeof identity + identity[0];
    }
    unsigned head[3] = { 0, n, size };
    memcpy(buf, head, sizeof head);
    head[0] = hash_bytes(FNV_SEED, buf, size);
    memcpy(buf, head, 4);
    if (!blob_io(SUBSET_FILE, SUBSET_FILE ".tmp", buf, size, 1)) unlink(SUBSET_FILE);
    free(buf);
}
/* out, stock's whole-library rebuild resumed at at: the saved tracks found in it, in their order,
 * when stock's track is one of them; else as stock built it. */
static int subset_only(void *out, int at) {
    void *f = fopen(SUBSET_FILE, "rb");
    unsigned head[3] = { 0 }, n = deque_size(out);
    int ok = f && fread(head, 12, 1, f) == 1 && head[1] && head[1] <= SAVE_LIMIT &&
             head[2] >= 12 + head[1] * 14 && head[2] <= 12 + head[1] * 1036;
    unsigned char *buf = ok ? calloc(head[2], 1) : 0, extra;
    ok = buf && fread(buf + 12, head[2] - 12, 1, f) == 1 && !fread(&extra, 1, 1, f);
    if (f) fclose(f);
    if (ok) {
        memcpy(buf, head, 12);
        memset(buf, 0, 4);
        ok = hash_bytes(FNV_SEED, buf, head[2]) == head[0];
    }
    resume_row *lookup = ok && n ? calloc(n, sizeof *lookup) : 0;
    void *q = 0, *mine = deque_at(out, (unsigned)at);
    int pos = -1;
    if (lookup) {
        for (unsigned i = 0; i < n; ++i) lookup[i] = (resume_row){ deque_at(out, i), i };
        qsort(lookup, n, sizeof *lookup, resume_before);
        q = _create_deque("stSongInfo");
        deque_init(q);
        unsigned char *p = buf + 12, *end = buf + head[2];
        for (unsigned i = 0; i < head[1]; ++i) {
            unsigned id[3];
            if (end - p < 12) break;
            memcpy(id, p, 12);
            p += 12;
            if (id[0] < 2 || id[0] > (unsigned)(end - p) || p[id[0] - 1]) break;
            const char *path = (const char *)p;
            p += id[0];
            unsigned lo = 0, hi = n;
            while (lo < hi) {
                unsigned mid = lo + (hi - lo) / 2;
                if (resume_cmp(lookup[mid].record, path, id[1], id[2]) < 0)
                    lo = mid + 1;
                else
                    hi = mid;
            }
            if (lo == n || resume_cmp(lookup[lo].record, path, id[1], id[2])) continue;
            if (pos < 0 && !resume_cmp(mine, path, id[1], id[2])) pos = (int)deque_size(q);
            _deque_push_back(q, lookup[lo].record);
        }
        if (pos >= 0) deque_assign(out, q);
        deque_destroy(q);
    }
    free(lookup);
    free(buf);
    return pos >= 0 ? pos : at;
}
#endif
