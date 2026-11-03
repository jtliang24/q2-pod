/* M1 Plus: the two backends of spotify.c's page, included by it. Spotify (librespot, .spotify) and Soloify
 * (the q2-soloify relay, .soloify) share the page, the /tmp names and the Q2SPOT/1 contract; this table
 * is what differs: the card folder and its launcher, the texts that name the service, and the rows
 * Soloify has no use for (downloads, sign-out). Streaming's rows pass the index as spot_open's ctx. Only
 * one runs at a time: opening the other backend stops the first (spot_open). The Q2 keeps spotify.c's
 * literals, so its payload is unchanged. */
struct spot_backend {
    const char *label, *bin, *run, *log;
    const char *missing_note, *missing_sub; /* its folder is not on the card */
    const char *pair_note, *pair_sub;       /* Now Playing, before the phone chose Q2 */
    const char *pair_row, *pair_row_sub;    /* the page's prompt */
    const char *old_note, *old_sub, *old_row_sub; /* an add-on without the browse socket */
    const char *wait_sub, *idle_sub;
    const char *signout, *tips, *no_sock, *no_answer;
    int downloads; /* the Downloads hub, Download Playlist and Sign Out are offered */
};
static const struct spot_backend spot_backends[2] = {
    { "Spotify", SPOT_DIR "/librespot", "/bin/sh " SPOT_DIR "/run", SPOT_DIR "/spot.log",
      "Spotify isn't on the card", "See the Q2 Pod guide to add it",
      "Open Spotify on your phone", "and choose Q2",
      "Open Spotify on your phone and choose Q2", "Both on the same Wi-Fi",
      "Update Spotify on the card", "See the Q2 Pod guide", "to browse on the Q2",
      "Waiting for Spotify", "Choose music in Spotify",
      "Sign Out of Spotify?", "Search Spotify", "Spotify isn't running", "Spotify didn't answer", 1 },
    { "Soloify", SOLOIFY_DIR "/q2-soloify", "/bin/sh " SOLOIFY_DIR "/run", SOLOIFY_DIR "/spot.log",
      "Soloify isn't on the card", "Install it from Apps",
      "Pair Soloify on its server", "Open Spotify near it, choose Q2",
      "Pair Soloify on its server", "Open Spotify near the server and choose Q2",
      "Update Soloify on the card", "Install the latest from Apps", "to browse here",
      "Waiting for Soloify", "Choose music in Soloify",
      "Sign Out of Soloify?", "Search Soloify", "Soloify isn't running", "Soloify didn't answer", 0 },
};
/* The backend in use: 0 Spotify, 1 Soloify. Outside sp, which spot_stop clears. */
static int spot_be __attribute__((section(".scratch")));
#define SB(field) (spot_backends[spot_be].field)
#define SPOT_BIN SB(bin)
#define SPOT_RUN SB(run)
#define SPOT_LOG SB(log)
#define SPOT_T_LABEL SB(label)
#define SPOT_T_MISSING_NOTE SB(missing_note)
#define SPOT_T_MISSING_SUB SB(missing_sub)
#define SPOT_T_PAIR_NOTE SB(pair_note)
#define SPOT_T_PAIR_SUB SB(pair_sub)
#define SPOT_T_PAIR_ROW SB(pair_row)
#define SPOT_T_PAIR_ROW_SUB SB(pair_row_sub)
#define SPOT_T_OLD_NOTE SB(old_note)
#define SPOT_T_OLD_SUB SB(old_sub)
#define SPOT_T_OLD_ROW_SUB SB(old_row_sub)
#define SPOT_T_WAIT_SUB SB(wait_sub)
#define SPOT_T_IDLE_SUB SB(idle_sub)
#define SPOT_T_SIGNOUT SB(signout)
#define SPOT_T_TIPS SB(tips)
#define SPOT_T_NO_SOCK SB(no_sock)
#define SPOT_T_NO_ANSWER SB(no_answer)
#define SPOT_DOWNLOADS SB(downloads)
