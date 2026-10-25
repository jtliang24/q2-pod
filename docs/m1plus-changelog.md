# M1 Plus changelog

Releases of Q2 Pod for the Shanling M1 Plus, newest first. Each is named after the upstream release it
carries and an M1 revision, `<version>-m1.<n>`. `tools/release_m1.py` takes the top entry's name and
turns its text into the release notes, as `tools/release.py` does with [changelog.md](changelog.md).
Upstream's changes are in that file.

- **1.4.2-m1.1**:
  - Q2 Pod 1.4.2 on the M1 Plus's stock firmware V2.1, in V2.1's own look: the first published M1 Plus release. A Q2 Pod card on Home opens its page: Shuffle, Ratings, Most Played, Long Songs, Podcasts, Audiobooks, Photos, Books, Videos, Coverflow, Spotify, Internet Radio and AirPlay.
  - Upstream's changes since 1.2.2 that run on the M1 Plus, among them EQ Advanced's Auto preamp for each sample rate, Audio and System settings wrapping at their ends, the MQA switch, and Mono Audio and Swap L/R. Q2 Pod's own changelog has the rest.
  - Lyrics from a track's tags, and lyrics and covers found online (LRCLIB, then MusicBrainz and iTunes, before Kugou and NetEase). Chapters for M4B audiobooks. Standby Limit powers the player off after a long Standby.
  - A built-in lock screen wallpaper now survives a reboot, and picks from View Queue keep a shuffle's order.
  - Display's **Knob: Navigation** now moves through Home's cards (the press opens one) and V2.1's own settings pages, Date and time among them, and pickers open on their current option.
  - A tap outside the hold menu or the rating picker closes it. The Q2 Pod pages' lists use V2.1's rows, and Now Playing's info page reads more cleanly.
  - Not on the M1 Plus yet: the iPod UI, the Q2's touch wheel settings, the card apps and System settings' Apps, Network Update, games, and the extra time zones.
  - Known issues: the hold menu's Go to Artist does nothing, and its Go to Album opens the playing song's album.
- **1.2.2-m1.1**:
  - Q2 Pod 1.2.2 on the M1 Plus's stock firmware V2.1, in V2.1's own look. A Q2 Pod card on Home opens its page: Coverflow, Shuffle, Ratings, Most Played, Long Songs, Books, Photos, Videos, Spotify, Internet Radio and AirPlay.
  - Every Q2 Pod page has V2.1's title-bar back button. A touch long-press opens the hold menu, where the Q2 holds Play/Pause.
  - Display's **Knob** setting can turn the volume knob into list navigation, with Previous as Back.
  - From Q2 Pod: the 30-band PEQ, Crossfade, ReplayGain, gapless Shuffle Albums and Folders, LDAC HQ at 990 kbps, Resume on Connect, a queue that survives a reboot, the Lock screen's clock and pictures, and the Rockbox dual boot.
  - Not on the M1 Plus: the iPod UI, and the Q2's touch wheel settings.
