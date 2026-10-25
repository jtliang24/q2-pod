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
  - A tap outside the hold menu or the rating picker closes it. The Q2 Pod pages' lists use V2.1's rows, Coverflow's track titles among them, and Now Playing's info page reads more cleanly.
  - **System settings → Apps**, before System Update, installs, updates and removes Spotify, Deezer, Soulseek and File Browser from their GitHub releases. The card apps get rows on the Q2 Pod page, after Spotify, and end before USB storage takes the card.
  - **Edit Playlist**: hold a playlist's row to add songs (with a search), move them and remove them.
  - The hold menu's Go to Album and Go to Artist open the held song's album and artist, a hold on an album's tracks opens the track's menu, and a play from Folder replaces the open Now Playing.
  - Knob: Navigation moves through View Queue's dialog, the Home editor, Recent and Frequent, search and CD Ripper.
  - Folder names with `%` no longer crash Folder's rows. A folder scan refreshes tags that changed. A CUE track without sheet tags takes its file's. Ogg and Opus covers show in the album grids and Folder, and Now Playing gets the art stock's decoder refuses. A FLAC's ALBUM ARTIST is read.
  - Lyrics: the top row is never cut, and Play/Pause no longer flicks them to the top.
  - Bluetooth: earbuds that connect while the player reconnects the last device are kept, and a pause you make isn't undone by the earbuds' automatic resume.
  - Not on the M1 Plus yet: the iPod UI, the Q2's touch wheel settings, Network Update, Streaming's Configuration, games, and the extra time zones.
- **1.2.2-m1.1**:
  - Q2 Pod 1.2.2 on the M1 Plus's stock firmware V2.1, in V2.1's own look. A Q2 Pod card on Home opens its page: Coverflow, Shuffle, Ratings, Most Played, Long Songs, Books, Photos, Videos, Spotify, Internet Radio and AirPlay.
  - Every Q2 Pod page has V2.1's title-bar back button. A touch long-press opens the hold menu, where the Q2 holds Play/Pause.
  - Display's **Knob** setting can turn the volume knob into list navigation, with Previous as Back.
  - From Q2 Pod: the 30-band PEQ, Crossfade, ReplayGain, gapless Shuffle Albums and Folders, LDAC HQ at 990 kbps, Resume on Connect, a queue that survives a reboot, the Lock screen's clock and pictures, and the Rockbox dual boot.
  - Not on the M1 Plus: the iPod UI, and the Q2's touch wheel settings.
