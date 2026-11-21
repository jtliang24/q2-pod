# M1 Plus changelog

Releases of Q2 Pod for the Shanling M1 Plus, newest first. Each is named after the upstream release it
carries and an M1 revision, `<version>-m1.<n>`. `tools/release_m1.py` takes the top entry's name and
turns its text into the release notes, as `tools/release.py` does with [changelog.md](changelog.md).
Upstream's changes are in that file.

- **1.7.6-m1.1**:
  - Q2 Pod 1.7.6 on the M1 Plus's stock firmware V2.1. Upstream's changes since 1.7.0 that run on the M1 Plus are below; Q2 Pod's own changelog has the rest.
  - Playback: the player catches up with the Q2's. MP3, AAC, Opus and Vorbis albums play gapless with no click between tracks, a change of sample rate lets the last track finish before it switches, and Pause, Play, Next and Previous answer sooner. A stream that stops for a while, as when Wi-Fi drops out, carries on from where it stopped.
  - Playback: Crossfade, the visualizer and the EQ read each track's length right. They read the wrong value before.
  - Playback: a FLAC cut short, a broken DSD, ISO, AAC or WMA file, a genre tag over 128 characters or a status check between tracks no longer stalls or stops the player, and the song before a broken file plays to its end. **Play Next** on a long queue no longer risks a restart.
  - System: if the M1 Plus freezes, a watchdog restarts it and `q2-crash.log` on the card says what it was doing. The card keeps the two logs before the newest as `q2-crash.log.1` and `q2-crash.log.2`. A restart or a card update saves the queue first.
  - Battery: the status bar, **Percent** and the lock screen show the battery's real charge. On the cable they used to follow the charging animation. Percent stays one colour when charging ends.
  - Library: Songs and the other lists no longer hold on to more memory each time they open. On a big library, opening an album, **Go to Album** and **Recently Added** are faster after the next **Update Local Music**, which no longer sometimes skips the update without a word. **Frequent** is gone: **Most Played** lists your most played songs.
  - Library: adding an album to your favourites, or rating it five hearts, makes its songs favourites too.
  - Playlists: a new or imported playlist never takes another's place, and deleting several ticked playlists at once deletes them all.
  - Lyrics: tap the lyrics to fill the screen in every layout; a hold there keeps them full screen. The last lines stay in the middle, with no stray earlier line under them, and lyrics you scrolled stay where you left them. An .lrc with emoji or Korean text reads right.
  - Internet Radio: iHeart stations, such as KIIS FM, show the artist and song instead of raw text.
  - App Store: **Check for Updates** is the first row and says how many apps can be updated. The list holds up to 32 apps, so Soloify still fits beside upstream's.
  - Cover Flow: a large PNG or progressive JPEG cover no longer risks a restart while Cover Flow builds its covers.
  - EQ: a long preset name stays on the right, cut short with an ellipsis. The PEQ's messages break between words and keep clear of the screen's edges.
  - Bluetooth: the buttons of a headset whose name is longer than 55 characters work.
  - Known issues: a tap on View Queue's playing row starts the song again, and a **Play Next** while the next song is ready keeps that song's file open until the player restarts.

- **1.7.0-m1.1**:
  - Q2 Pod 1.7.0 on the M1 Plus's stock firmware V2.1, now with Q2 Pod's iPod UI as its only UI, laid out for the portrait screen and the knob. Upstream's changes since 1.5.8 that run on the M1 Plus are below; Q2 Pod's own changelog has the rest.
  - Home: **Split** shows the playing album's whole cover across the top, over a blurred copy of it, with the menu below; **Full** is the menu alone and **Carousel** a row of cards. Display → Appearance → Home chooses.
  - Every page has a status bar with the clock, a back chevron at the top left, and Bluetooth, play/pause, Wi-Fi and the battery on the right. Tap the chevron to go back, or hold it to return to Now Playing or Home. **Knob: Navigation** is the default: the knob moves through the rows, its press opens one, and Previous goes back.
  - Settings, the Library and their lists use the iPod's rows. Display's **Appearance**, **Cover Flow** and **Controls** hold Theme, Light Mode, Accent, Home, Shortcut, Battery and the knob's settings.
  - Now Playing: the iPod's layout with V2.1's transport buttons and a large Back at the top. **Centred Now Playing** in Appearance opens V2.1's own page instead. Spotify's page takes the same layout.
  - Quick Settings is V2.1's pull-down from the top of the screen, laid out as the iPod's. Confirm prompts are a sheet across the top with Cancel and OK as rows.
  - Themes: **Minimal** and **Modern**, each in Light Mode or dark, with your accent. Choosing one applies its look at once.
  - Spotify: **Soloify** plays a Spotify account through Soloist. Install it from **System settings → Apps**; it gets its own Streaming row.
  - EQ: **EQ per Output** keeps a separate EQ for the 3.5 mm and 4.4 mm jacks, USB and each Bluetooth device.
  - Library: **Recently Added** goes by the date the card created each file, and Cover Flow's rows have new names, among them **Artist View**.
  - Not on the M1 Plus yet: **Theme: Classic**, Night Shift, the extra time zones, Network Update, Playlists, Podcasts and Audiobooks as Shortcuts, Games (they need the wheel), and the rest of the port report (docs/m1plus-unported.md).

- **1.5.8-m1.1**:
  - Q2 Pod 1.5.8 on the M1 Plus's stock firmware V2.1. Upstream's changes since 1.4.2 that run on the M1 Plus are below; Q2 Pod's own changelog has the rest.
  - Library: **Era**, after Genre, lists each decade with dated albums. A decade has **Play All**, **Shuffle** and its albums by year.
  - Library: titles, artists and albums with accented letters (Café, Canção) show as tagged instead of as Chinese characters, in tags and in CUE sheets. **Update Local Music** skips hidden folders, such as apps' caches.
  - Streaming: **Configuration** lists the services, each with a tick. Untick the ones you don't use to hide them from Streaming.
  - Lyrics: **Download Album Lyrics** saves synced lyrics from LRCLIB beside every song of the playing album. **Download Cover & Lyrics** saves the lyrics you accept in the song's own folder, and blank lines in lyrics no longer show as gaps.
  - EQ: with the EQ on, FLAC plays again, and the EQ also applies to hi-res tracks. Gapless albums no longer click between tracks with the EQ or PEQ on.
  - Crossfade goes up to 15 s. Skipping a track over Bluetooth no longer crackles.
  - Spotify: when Spotify refuses to unlock your account's tracks, the player says so within a second instead of "Loading…".
  - Battery: the player and the cover loaders wait longer between checks while paused or with the screen off, and a memory-cleaning thread that woke every few seconds is gone.
  - View Queue: holding Play/Pause on a row moves it to play next instead of pausing, and Now Playing follows a tapped row at once.
  - A queue started from Era, Most Played, Ratings or Long Songs comes back after a power-off as that queue, at the same song, instead of the whole library.
  - Known issue: View Queue opens only while a shuffle is on.
  - Not on the M1 Plus yet: the iPod UI, Network Update, the extra time zones, `database.ignore` folders, automatic scrobble uploads, Simple EQ's Presets button, Coverflow's flick gestures and games.

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
