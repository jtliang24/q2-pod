#!/usr/bin/env python3
"""The M1 Plus target: its V2.1 tables and its own build pipeline, beside upstream's tools/build.py.

build.py keeps upstream's Q2 code; its build() hands an M1 Plus input to build() here
(docs/m1plus-roadmap.md U1). The pipeline reuses build.py's helpers and tables where V2.1 matches V1.32,
and every V2.1 address here was found in V2.1's own code."""
import hashlib, io, json, re, shlex, struct, subprocess, tarfile, zipfile
from build import (ROOT, TIMEZONES, TIMEZONE_ORDER, VERSION, TAG, BASE, SCRATCH, RING_STEP, FLAGS, FUNCTIONS, GLOBALS, CONTEXT_DATA, HELPER,
                   HELPER_LIKE, HELPER_LIBS, BOOT, REMOTE, S90PLAY, ROCKBOX_FLAG, BOOT_HOOK, S11LOGO, LOGO_HOOK,
                   REMOTE_HOOK, BLUEALSA, BLUEALSA2, BT_KEEPALIVE, SCROBBLE_CA, WATCHDOG, WATCHDOG_SLEEP, RTC_WRITE, LOCK_CLOCK_12H, WIFI_LPS, ICONS,
                   STOCK_EQ, OBSOLETE, TAG_C, append_payload, check, dev_tag, fileoff, jpeg_size, patch_bluealsa,
                   run, segments, sha, source_sha256, symbols)

MODEL = 'Shanling M1 Plus'
M1PLUS_BIN_SHA = '1ccb4667e3e9bdf9a35be4dc58d09b898ca53c5fd58396b7667fb91fe895f925'
M1PLUS_ZIP_SHA = 'db7bdbc42ffe6d5c1e3fdca9363edb78a01898b9a725c34793394cf6abfa33c0'
M1PLUS_DEMO_SHA = '29e23119bc2a0f153f3ea0ba942a39754d1aab0879c1040fae2269df8bd9b3f1'
M1PLUS_GP = 0xa03ed0
# The M1's edition letter in the tag where the Q2's is I (build.py TAG, V159I): V159M, and dev builds
# end in m (V02Gm), so no M1 tag equals a Q2 one.
M1_TAG = TAG[:-1] + 'M'

def m1_dev_tag(number):
    return dev_tag(number)[:-1] + 'm'

INPUTS = {M1PLUS_ZIP_SHA: ('M1 Plus Firmware V2.1/update.bin', M1PLUS_BIN_SHA), M1PLUS_BIN_SHA: (None, M1PLUS_BIN_SHA)}
# Stock routines only the M1 Plus payload calls, beside build.py's FUNCTIONS (compile_common merges them).
M1PLUS_FUNCTIONS = {
 'm1_home_click': ('int', 'void *, void *'),
 'toolsThumbSpecCover': ('int', 'const char *, const char *, int, int'),
 'set_hscroll_label_attribute': ('void', 'void *'),
 'label_set_line_wrap': ('int', 'void *, int'),
 # Home's art (ipod-ui 4.5): image_manager_unload_bitmap_by_name (patch/m1plus_nav.h) is V2.1's lookup by name, which
 # copies the cached bitmap_t, then its unload of that bitmap's entries
 'image_manager_lookup': ('int', 'void *, const char *, void *'),
 'image_manager_unload_bitmap': ('int', 'void *, void *'),
 # its four corner radii, the width and the edges (0xffff all), as V1.32's wrapper (0x63d034) passes them
 'canvas_stroke_rounded_rect_ex': ('int', 'void *, const void *, const void *, const void *, unsigned, unsigned, unsigned, unsigned, unsigned, unsigned'),
 # Shanling's real signature, (name, readAudioProperties): the M1 Plus passes 1 (V2.1's scanner passes 0)
 'taglib_file_open': ('void *', 'const char *, int'),
 'widget_add_child': ('int', 'void *, void *'),
 'widget_remove_child': ('int', 'void *, void *'),  # out of its parent, not destroyed
 'widget_get_window': ('void *', 'void *'),
 # V2.1's Lock screen page: its pick of picture index (lockscreen.c lockscreen_page)
 'saver_pick': ('int', 'void *, int'),
 # V2.1's Play mode page's other two calls (0x49fc88): the M1 Plus's config_playmode (patch/peq.h)
 'notifyPlayMode': ('int', 'void'),
 'dmrSendPlayMode': ('int', 'int'),
 'volume_refresh': ('void', 'void *'),  # the volume dialog shows the output's level
 'text_edit_set_select': ('int', 'void *, unsigned, unsigned'),  # the M1 Plus's edit_set_select (patch/m1plus_peq.h)
 'navigator_replace': ('int', 'const char *'),  # Tidal's login in its main page's place (m1_tidal_login)
}
WM_PAINT_LEAF_M1PLUS = ('window_manager_paint', 0x677b44, 'ringnav_wm_paint', (0x10800009, 0, 0x8c820088))
# style_get_gradient (docs/m1plus-ipod-ui.md 4.1) is the Q2's leaf again: beqz a0; nop; lw v0, 0(a0), then the
# style vtable's get_gradient (+0x18) tail-called. style_get_color's own bal to it returns to
# STYLE_COLOR_GRADIENT_RET (offsets.inc), which the payload's leaf tells apart.
GRADIENT_LEAF_M1PLUS = ('style_get_gradient', 0x659f9c, 'ringnav_style_gradient', (0x10800009, 0, 0x8c820000))
BLUEALSA_SHA = '0a4ffb7cc8207a46a3568440c5f31022b7125befd164e2f1af52537340a9892a'  # the same binary in Q2 V1.32 and M1 Plus V2.1
# V2.1 also reads the RTC back each time demo starts (platform_init's toolsGetRtcTime), local time
# too: it reads UTC as well, or every start would shift the clock by the zone's offset.
RTC_READ_M1PLUS = (b'hwclock -s\0\0', b'hwclock -su\0')
# Call-site patches: stock calls and words the payload replaces, per model, each found in that model's
# own demo (docs/m1plus-roadmap.md section 4). Each entry is (address, original word, replacement): a str
# replacement is a jal to that payload symbol, None pins the word unchanged. A model without an entry
# leaves that behaviour stock. build.py applies the Q2's with upstream's own code; build() here applies
# the M1's; test/m1plus/build.py and test/m1plus/patch.py read both.
CALL_SITES = {
    'q2': {
        # config_init's bal config_playmode becomes jal ringnav_bootmode, which keeps the saved queue
        # while it applies the boot play mode, and reads Artists.
        'BOOT_MODE_CALL': ((0x4f999c, 0x0411e992, 'ringnav_bootmode'),),
        # Stock init builds the Songs view (0x4adcbc); it calls the stock Albums tab click handler
        # (0x4ac7ec) instead, which sets the tab state, queries the artist's albums and builds them.
        'ARTIST_ALBUMS': ((0x4aebd0, 0x2739dcbc, 0x2739c7ec), (0x4aebd4, 0x0411fc39, 0x0411f705)),
        # mclNextSong's bal mcl_shuffle_pick; the payload calls the stock pick, then applies a pending
        # Play next. Its delay slot (a0=1) stays.
        'SHUFFLE_CALL': ((0x5addf0, 0x0411e8cb, 'ringnav_shuffle'),),
        # Hold Return: only on_wm_keylong_fun's final Home call (bal) changes; all stock gates and its
        # release guard precede it (docs/ipod.md#hold-return).
        'HOLD_RETURN': ((0x4e8924, 0x04110fdf, 'compact_now_playing'),),
        # device_standby's bal awake_screen after the resume from Standby becomes li $v0, 1: the screen
        # stays dark, so the resuming key acts as it does dark (Play plays, centre wakes).
        'STANDBY_WAKE': ((0x4f7d24, 0x0411ff26, 0x24020001),),
        # checkBluetoothStatus' jalr player_save_start once a headset's A2DP comes up (a0 0: the queue
        # restarts unpaused, whatever it was doing) (docs/internals.md#resume-on-connect).
        'BT_CONNECT_START': ((0x4f358c, 0x0320f809, 'ringnav_bt_connect_start'),),
        # toolsLoadAllFile stops a scan at 20,000 songs: lw $2,count; slti $2,$2,0x4e20 before each
        # entry. 65,000 overflows slti's signed immediate, so the lw becomes jal ringnav_scan_room and the
        # slti loads the count into a0 in its delay slot (lw $2/$4, -0x3cac($fp)); the bnez after it, and
        # its delay slot's stop-flag load, stay.
        'SCAN_LIMIT': ((0x5c977c, 0x8fc2c354, 'ringnav_scan_room'), (0x5c9780, 0x28424e20, 0x8fc4c354)),
        # check_mem_thd (platform_init's detached thread) returns at once: it never opens drop_caches,
        # writes 3 to it or wakes each second. lui/addiu $gp -> jr $ra; move $v0,$zero.
        'DROP_CACHES': ((0x512050, 0x3c1c0051, 0x03e00008), (0x512054, 0x279c4c70, 0x00001025)),
        # player_parsecover_thd's jalr toolsGetExternCover (Now Playing's folder art, after its embedded
        # art failed) becomes jal coverflow_player_cover, which gives ffmpeg what stock's decoder refuses.
        'PLAYER_COVER': ((0x51301c, 0x0320f809, 'coverflow_player_cover'),),
        # platform_init's control thread start: install callbacks before it discovers boot connections,
        # and config_bt_init's reset moves before it too (1.3.8, in place of 1.2.9's BT_POWER).
        'BT_INIT': ((0x512598, 0x0320f809, 'headset_bt_init'),),
        'BT_PARAMS': ((0x4f3ab4, 0x0411f5ef, 0),),
        # openBluetooth's jalr btctl_device_status_callback registers headset_bt_status instead, and
        # autoLinkBluetooth's bal checkPairDev also skips while the link list holds a connected link.
        'BT_STATUS': ((0x4effe0, 0x0320f809, 'headset_status_register'),),
        'BT_AUTOLINK': ((0x4f17fc, 0x0411fd04, 'headset_bt_autolink'),),
        # toolsLoadAllFile's existing-song check, folder scans only.
        'SCAN_REFRESH': ((0x5c981c, 0x0411fd88, 'ringnav_scan_refresh'),),
        # Folder row names are text, not printf formats ("99% Invisible" crashes stock's formatter):
        # tk_snprintf becomes tk_strncpy of record->name, 511 bytes and the terminator.
        'FOLDER_NAME': ((0x522384, 0x24050200, 0x240601ff), (0x522390, 0x8f99a7c8, 0x8f99b200),
                        (0x522398, 0x8e260008, 0x8e250008)),
        # player_get_id3info's jalr strcpy of the parsed path: a CUE track without sheet tags takes its file's.
        'ID3_PATH': ((0x5148e8, 0x0320f809, 'ringnav_id3_path'),),
        # The Now Playing timer's jalr scroll_view_scroll_to, its lyric follow: whole rows at the top.
        'LYRIC_FOLLOW': ((0x52bed0, 0x0320f809, 'ringnav_lyric_follow'),),
        # The page refresh's bal to the lyric row builder: the lyrics keep their place on a refresh.
        'LYRIC_ROWS': ((0x52b8f8, 0x0411f984, 'ringnav_lyric_rows'),),
        # Stock's .lrc loader's jalr fopen: a copy that ringnav_lyric reads again, as a tag's.
        'LYRIC_OPEN': ((0x5a9c5c, 0x0320f809, 'ringnav_lrc_open'),),
        # parse_albumcovertask_thd's jalr toolsGetAlbumCover calls: Ogg pictures through ffmpeg.
        'GRID_COVER': ((0x4edf1c, 0x0320f809, 'coverflow_album_cover'), (0x4ef018, 0x0320f809, 'coverflow_folder_cover'),
                       (0x4ef0d4, 0x0320f809, 'coverflow_grid_cover')),
        # Now Playing's info page: its one fill (bal 0x52a508) goes through ringnav_np_info, which tidies
        # the lines.
        'NP_INFO_CALL': ((0x52baf4, 0x0411fa84, 'ringnav_np_info'),),
        # switchBtPriority sends LDAC quality 0x16 (SQ, 660 kbps) for both HQ (row 0) and Standard (row
        # 1). The dispatch keeps 0x15 + row in its free 0x14($sp) slot, so HQ sends 0x15 (990 kbps); see
        # docs/internals.md.
        'LDAC_HQ': ((0x4f033c, 0x00042080, 0x00041880),   # sll $3,$4,2
                    (0x4f0340, 0x2442f030, 0x00431021),   # addu $2,$2,$3
                    (0x4f0344, 0x00442021, 0x8c42f030),   # lw $2,-0xfd0($2)
                    (0x4f0348, 0x8c820000, 0x24840015),   # addiu $4,$4,0x15
                    (0x4f0354, 0x00000000, 0xafa40014),   # sw $4,0x14($sp), jr's delay slot
                    (0x4f0360, 0x24040016, 0x8fa40014)),  # lw $4,0x14($sp), was li $4,0x16
        # The encoder thread's ts_read call (jalr $t9) becomes jal ringnav_ts_read, which makes the
        # wheel's ticks from the samples (playback.c wheel_sample).
        'WHEEL_TS_READ': ((0x625b6c, 0x0320f809, 'ringnav_ts_read'),),
        # The extension checks' jalr strstr (its lw $t9 two words before) in toolsLoadDirectory and the
        # recursive scan also accept M4B (manifest audio_extension_calls).
        'AUDIO_EXTENSION_CALLS': ((0x5c204c, 0x8f99f950, None), (0x5c2054, 0x0320f809, 'ringnav_audio_extension'),
                                  (0x5c3d9c, 0x8f99f950, None), (0x5c3da4, 0x0320f809, 'ringnav_audio_extension')),
        # The bal toolsTrimLeft on each name copy in the two library name comparators (0x5b9d40, 0x5ba658,
        # the Chinese and other-language sorts) becomes jal ringnav_sort_key, which also drops a leading
        # article.
        'SORT_TRIMS': ((0x5b9e38, 0x0411ff86, 'ringnav_sort_key'), (0x5b9ea4, 0x0411ff6b, 'ringnav_sort_key'),
                       (0x5ba750, 0x0411fd40, 'ringnav_sort_key'), (0x5ba7bc, 0x0411fd25, 'ringnav_sort_key')),
        # Library Albums' cover cache names (navigation.c art_key): the row renderer's snprintf of the
        # name, with a2 the row (addiu a2,"%s" becomes move a2,s3), the Albums page's
        # albumcoverinfo_init calls and the album page's big cover snprintf become jal to the payload;
        # so do an artist page's albums renderer (its row in s2) and albumcoverinfo_init calls on tab
        # entry, return and init.
        'ALBUM_ART': ((0x4a388c, 0x0320f809, 'ringnav_art_name'), (0x4a3890, 0x24c66c04, 0x02603025),
                      (0x4a421c, 0x0320f809, 'ringnav_albumcovers'), (0x4a42c0, 0x0320f809, 'ringnav_albumcovers'),
                      (0x4a5718, 0x0320f809, 'ringnav_albumcovers'), (0x4a72a4, 0x0320f809, 'ringnav_art_header'),
                      (0x4ab804, 0x0320f809, 'ringnav_artist_art_name'), (0x4ab808, 0x24c66c04, 0x02403025),
                      (0x4ac840, 0x0320f809, 'ringnav_artist_covers'), (0x4ae860, 0x0320f809, 'ringnav_artist_covers'),
                      (0x4ae968, 0x0320f809, 'ringnav_artist_covers'), (0x4aebc0, 0x0320f809, 'ringnav_artist_covers')),
        # Library Artists rows: the row bind's bal to class_icon becomes jal ringnav_class_icon, which
        # hides the head.
        'CLASS_ICON': ((0x4b0cec, 0x0411fbc9, 'ringnav_class_icon'),),
        # Album grids' and Songs' scroll start no longer pauses the cover worker (sw $3,0($2) -> nop); see
        # docs/internals.md.
        'COVER_PAUSE': ((0x4aab60, 0xac430000, 0), (0x4a22d0, 0xac430000, 0), (0x4a7bb0, 0xac430000, 0)),
        # An artist's albums scroll end divides yoffset by its 160 px rows, not 256; see docs/internals.md.
        'ARTIST_COVER_ROW': ((0x4ad878, 0x244400ff, 0x240400a0),   # addiu $4,$2,0xff -> li $4,160
                             (0x4ad880, 0x28430000, 0x0044001a),   # slti $3,$2,0 -> div $zero,$2,$4
                             (0x4ad884, 0x0043200a, 0),            # movz $4,$2,$3 -> nop
                             (0x4ad88c, 0x00042203, 0x00002012)),  # sra $4,$4,8 -> mflo $4
        # Local art completion passes the worker's copied key (sp + 0x1688) and the payload validates the
        # row under aclist_mutex; the folder-cover path, which branched past the key (b 0x4edda0), enters
        # at the key as the others do.
        'COVER_DONE': ((0x4edd9c, 0x8f99b6d4, 0x27a61688), (0x4edda0, 0x0411ff44, 'ringnav_cover_done'),
                       (0x4eeddc, 0x1000fbf0, 0x1000fbef)),
        # input_device_status' timer and threshold lookup: Play/Pause and Return hold at 700 ms.
        'HOLD_KEYS': ((0x6a0088, 0x8f99b1a4, 0x02603825),
                      (0x6a0098, 0x0320f809, 'ringnav_hold_timer'),
                      (0x6a03e8, 0x0411ffa4, 'ringnav_hold_info')),
        # on_wm_idle_status' player_mainscheduling call, paced by the payload.
        'MAINSCHEDULING_CALL': ((0x4e9d28, 0x0320f809, 'ringnav_mainscheduling'),),
        # toolsFixId3ErrorCode's jalr strcmp of the GBK round trip: GBK only when the bytes read as GBK.
        'TAG_TEXT': ((0x5c5e7c, 0x0320f809, 'ringnav_gbk_tag'),),
        # The CUE sheet parser's seven bal toolsIconvConvert: UTF-8, GBK or Windows-1252.
        'CUE_TEXT': ((0x5c06d0, 0x0411f176, 'ringnav_cue_text'), (0x5c0794, 0x0411f145, 'ringnav_cue_text'),
                     (0x5c084c, 0x0411f117, 'ringnav_cue_text'), (0x5c0908, 0x0411f0e8, 'ringnav_cue_text'),
                     (0x5c0bc8, 0x0411f038, 'ringnav_cue_text'), (0x5c0f84, 0x0411ef49, 'ringnav_cue_text'),
                     (0x5c130c, 0x0411ee67, 'ringnav_cue_text')),
        # The library scan's folder walk: its first strcmp (jalr, "." in its delay slot, pinned) skips
        # every hidden folder.
        'SCAN_DIRS': ((0x5c3c0c, 0x0320f809, 'ringnav_scan_dir'), (0x5c3c10, 0x24a55110, None)),
        # Baidu Pan's and Tidal's start-flag polls' jalr usleep: their threads park (tidal.c).
        'STREAM_POLL_CALLS': ((0x47f824, 0x0320f809, 'ringnav_baidu_poll'), (0x486404, 0x0320f809, 'ringnav_tidal_poll')),
        # mclSyncPlayerStatus' jalr usleep: at least DARK_POLL_US while the Q2 is dark and quiet;
        # parse_albumcovertask_thd's and player_parsecover_thd's whenever it is dark.
        'DARK_POLLS': ((0x5a958c, 0x0320f809, 'ringnav_dark_usleep'), (0x4edbe0, 0x0320f809, 'ringnav_dark_cover_usleep'),
                       (0x512fac, 0x0320f809, 'ringnav_dark_cover_usleep')),
        # Download Cover & Lyrics' accept: its jalr snprintf of the cp command, its format's addiu pinned.
        'LYRIC_SAVE': ((0x525484, 0x0320f809, 'ringnav_lyric_save'), (0x525480, 0x24c62630, None)),
        # Tidal's playlist, album and favourite-tracks threads' done store: sb $3,0($2) -> nop.
        'TIDAL_PAGE_DONE': ((0x48b57c, 0xa0430000, 0), (0x48b70c, 0xa0430000, 0), (0x488434, 0xa0430000, 0)),
        # importPlayList's jalr toolsGetDirectoryM3u8, its lw $t9 pinned: a card app's own playlists only.
        'M3U_DIR_CALL': ((0x50dab8, 0x0320f809, 'addon_m3u_dir'), (0x50dab4, 0x8f99bad4, None)),
        # mclWaitAccept's jalr accept: the saved MQA mode reaches each new player connection (1.6.3; build()
        # patches it by its address, with no site constant).
        'MQA_ACCEPT': ((0x5a7da0, 0x0320f809, 'mqa_accept'),),
    },
    # V2.1's routines are V1.32's, moved: each site is its Q2 counterpart's word in V2.1's copy.
    'm1plus': {
        # V2.1's mclWaitAccept's jalr accept (its lw $t9 accept@GLIBC at 0x5d0020); the delay slot's store of the
        # address length stays, and a positive descriptor is published at MCL_FD after it, as V1.32's.
        'MQA_ACCEPT': ((0x5d0030, 0x0320f809, 'mqa_accept'),),
        # V2.1 toolsFixId3ErrorCode's round-trip strcmp, with the Latin-1 source in a1.
        'TAG_TEXT': ((0x5ec5e4, 0x0320f809, 'ringnav_gbk_tag'),),
        # V2.1's CUE parser has seven bal conversions plus a shared jalr for track titles.
        # The jalr can call toolsIconvConvert or toolsIconvConvertNew (UTF-8 <- GBK).
        'CUE_TEXT': ((0x5e72dc, 0x0411f1b4, 'ringnav_cue_text'),
                     (0x5e73a0, 0x0411f183, 'ringnav_cue_text'),
                     (0x5e7458, 0x0411f155, 'ringnav_cue_text'),
                     (0x5e7514, 0x0411f126, 'ringnav_cue_text'),
                     (0x5e77d4, 0x0411f076, 'ringnav_cue_text'),
                     (0x5e7b90, 0x0411ef87, 'ringnav_cue_text'),
                     (0x5e7de4, 0x0320f809, 'ringnav_cue_text'),
                     (0x5e7f18, 0x0411eea5, 'ringnav_cue_text')),
        # toolsLoadAllFile's recursive directory walk (0x5ea364), first directory strcmp, ".".
        'SCAN_DIRS': ((0x5ea6a8, 0x0320f809, 'ringnav_scan_dir'), (0x5ea6ac, 0x24a53ed4, None)),
        # mclLoadExLyric's private loader: fopen of the final (possibly converted) .lrc.
        'LYRIC_OPEN': ((0x5d3bdc, 0x0320f809, 'ringnav_lrc_open'),),
        # onlinesearch's accept: snprintf(cp -rf tmp, .downpic/name), after both access checks.
        'LYRIC_SAVE': ((0x537ca0, 0x0320f809, 'ringnav_lyric_save'), (0x537c9c, 0x24c61b90, None)),
        # Cover accept: preserve its native thumbnail and also save the JPEG beside the song.
        'COVER_SAVE': ((0x537b10, 0x0320f809, 'm1plus_cover_save'),),
        # mclNextSong's bal to the shuffle pick (0x5d03b0).
        'SHUFFLE_CALL': ((0x5d5a28, 0x0411ea61, 'ringnav_shuffle'),),
        # V2.1's check_cpumem is the complete detached memory thread: open drop_caches,
        # write "3" every five one-second sleeps, forever; no other work. Return NULL at entry.
        'DROP_CACHES': ((0x50b810, 0x3c1c0050, 0x03e00008), (0x50b814, 0x279c86c0, 0x00001025)),
        # mclSyncPlayerStatus's outer 200 ms wait, and both cover workers' idle waits.
        # Its inner 10 ms playback/seek settling wait stays native.
        'DARK_POLLS': ((0x5d1814, 0x0320f809, 'ringnav_dark_usleep'),
                       (0x4dd4b4, 0x0320f809, 'ringnav_dark_cover_usleep'),
                       (0x4deef0, 0x0320f809, 'ringnav_dark_cover_usleep')),
        # toolsLoadAllFile's count check, the count at -0x4f7c($fp).
        'SCAN_LIMIT': ((0x5efeb4, 0x8fc2b084, 'ringnav_scan_room'), (0x5efeb8, 0x28424e20, 0x8fc4b084)),
        # toolsLoadDirectory's and the recursive scan's (0x5ea364) extension checks.
        'AUDIO_EXTENSION_CALLS': ((0x5e8ae8, 0x8f99f694, None), (0x5e8af0, 0x0320f809, 'ringnav_audio_extension'),
                                  (0x5ea838, 0x8f99f694, None), (0x5ea840, 0x0320f809, 'ringnav_audio_extension')),
        # The two name comparators, 0x5e0dac and 0x5e16c4.
        'SORT_TRIMS': ((0x5e0ea4, 0x0411ff86, 'ringnav_sort_key'), (0x5e0f10, 0x0411ff6b, 'ringnav_sort_key'),
                       (0x5e17bc, 0x0411fd40, 'ringnav_sort_key'), (0x5e1828, 0x0411fd25, 'ringnav_sort_key')),
        # album_page, which lists the library's albums and an artist's: its row renderer's snprintf of the
        # name (the row in s2), its three albumcoverinfo_init calls, and the album page's big cover's.
        'ALBUM_ART': ((0x523a34, 0x0320f809, 'ringnav_art_name'), (0x523a38, 0x24c61158, 0x02403025),
                      (0x524720, 0x0320f809, 'ringnav_albumcovers'), (0x524760, 0x0320f809, 'ringnav_albumcovers'),
                      (0x5248d0, 0x0320f809, 'ringnav_albumcovers'), (0x525b84, 0x0320f809, 'ringnav_art_header')),
        # The Albums list's (album_page) scroll start (0x522870); V2.1's Songs and artist page don't pause.
        'COVER_PAUSE': ((0x522890, 0xac430000, 0),),
        # parse_albumcovertask_thd's local completion and its folder path's branch to it (0x4de660).
        'COVER_DONE': ((0x4dd630, 0x8f99b86c, 0x27a61688), (0x4dd634, 0x0411fde3, 'ringnav_cover_done'),
                       (0x4de660, 0x1000fbf4, 0x1000fbf3)),
        # checkBluetoothStatus' bal save_start_player once a headset's A2DP comes up (a0 0).
        'BT_CONNECT_START': ((0x4d6320, 0x04113031, 'ringnav_bt_connect_start'),),
        # switchBtPriority's dispatch, its jump table at -0x5b50 from its GOT page: HQ and Standard (rows 0
        # and 1, btquality_page's btcode_ldachq and btcode_ldacst) share the li $4,0x16.
        'LDAC_HQ': ((0x4d304c, 0x00042080, 0x00041880),   # sll $3,$4,2
                    (0x4d3050, 0x2442a4b0, 0x00431021),   # addu $2,$2,$3
                    (0x4d3054, 0x00442021, 0x8c42a4b0),   # lw $2,-0x5b50($2)
                    (0x4d3058, 0x8c820000, 0x24840015),   # addiu $4,$4,0x15
                    (0x4d3064, 0x00000000, 0xafa40014),   # sw $4,0x14($sp), jr's delay slot
                    (0x4d3070, 0x24040016, 0x8fa40014)),  # lw $4,0x14($sp), was li $4,0x16
        # The lock screen picture's access checks, config_init's (0x4e5030) and get_screensaver_image's
        # (0x4d7524), access from -0x834($gp): a built-in wallpaper isn't a file. The Q2's build()
        # patches its two with upstream's code, as LOCKSCREEN_ACCESS's words.
        'LOCKSCREEN_ACCESS': ((0x4e6218, 0x0320f809, 'lockscreen_access'), (0x4d75b0, 0x0320f809, 'lockscreen_access')),
        # online_lyricthd (0x50a048) runs the hooked kugou_obtainlyric (LRCLIB, then Kugou), then NetEase's
        # com163_obtainlyric if it found nothing, as V1.32's does, but then NetEase again in every case
        # (0x50a1e4), which overwrote a found lyric. A find now branches past both (bnez $v0, 0x50a1ec).
        'LYRIC_SOURCES': ((0x50a1c0, 0x14400006, 0x1440000a),),
        # Now Playing's info page: show_player_face's bal to its fill (np_info, 0x539c40; $t9 is set
        # before it), as the Q2's one call.
        'NP_INFO_CALL': ((0x53bebc, 0x0411f760, 'ringnav_np_info'),),
        # platform_init's jalr btctl_create_daemon_thread: the callbacks before the control thread, and
        # config_bt_init's bal initBluetoothParam moves before it too (headset_bt_init), as V1.32's.
        'BT_INIT': ((0x50be24, 0x8f99f2c0, None), (0x50be28, 0x0320f809, 'headset_bt_init')),
        'BT_PARAMS': ((0x4d6ae4, 0x0411f51d, 0),),
        # openBluetooth's btctl_device_status_callback(BT_STATUS_CB, 0) registers headset_bt_status, and
        # autoLinkBluetooth's bal checkPairDev also skips while the link list holds a connected link.
        'BT_STATUS': ((0x4d2cec, 0x8f99f888, None), (0x4d2cf0, 0x0320f809, 'headset_status_register'),
                      (0x4d2cf4, 0x24844738, None)),
        'BT_AUTOLINK': ((0x4d44e4, 0x0411fd04, 'headset_bt_autolink'),),
        # Now Playing's timer: scroll_view_scroll_to(scroll_lrc, 0, y, 10), its lyric follow, as V1.32's.
        'LYRIC_FOLLOW': ((0x53ad54, 0x8f99acfc, None), (0x53ad64, 0x0320f809, 'ringnav_lyric_follow')),
        # show_player_face's bal to the lyric row builder (LYRIC_ROW_BUILDER, $t9 set before it), after
        # NP_INFO_CALL's: the rebuild ends at offset 0.
        'LYRIC_ROWS': ((0x53bed0, 0x0411f8db, 'ringnav_lyric_rows'),),
        # The Folder file click's navigator_to_with_context("playing_page", ...) (0x531c38's), which doesn't
        # look for an open one as the album track click does: m1plus_play_page closes it first.
        'FOLDER_PLAY': ((0x531e7c, 0x8f99a980, None), (0x531e94, 0x0320f809, 'm1plus_play_page')),
        # toolsLoadAllFile's existing-song check (bal toolsCheckItemExist), folder scans only: V1.32's word.
        'SCAN_REFRESH': ((0x5eff54, 0x0411fd88, 'ringnav_scan_refresh'),),
        # The folder row's text (0x532e34, bal'd from 0x533124; V1.32's 0x522304): tk_snprintf(buf, 512,
        # name) becomes tk_strncpy(buf, name, 511), its GOT slot -0x3300.
        'FOLDER_NAME': ((0x532eb4, 0x24050200, 0x240601ff), (0x532ec0, 0x8f99a868, 0x8f99cd00),
                        (0x532ec8, 0x8e260008, 0x8e250008)),
        # get_id3info's strcpy(playsong_id3info, record->path), its lw $t9 pinned.
        'ID3_PATH': ((0x4dff40, 0x8f99f324, None), (0x4dff4c, 0x0320f809, 'ringnav_id3_path')),
        # parse_albumcovertask_thd's toolsGetAlbumCover calls, under parse_cover_mutex: the Albums grid's,
        # before its toolsGetExternCover, then Folder view's two (40 px): the folder row's (1.6.3: its folder's first
        # song by name first), then the track row's.
        'GRID_COVER': ((0x4dd6a8, 0x0320f809, 'coverflow_album_cover'), (0x4de8a4, 0x0320f809, 'coverflow_folder_cover'),
                       (0x4de960, 0x0320f809, 'coverflow_grid_cover')),
        # parseplaycover_thd's toolsGetExternCover after a local track's embedded art failed (0x4df1e8),
        # under parse_cover_mutex: m1plus_player_cover drops it for ffmpeg (patch/m1plus_player_cover.c).
        'PLAYER_COVER': ((0x4df218, 0x8f99b880, None), (0x4df228, 0x0320f809, 'm1plus_player_cover')),
        # Tidal's main page with no session opens its login page from its init (tidal_tidal_main_init, 0x4b9e44):
        # bal navigator_to("tidal/tidal_userlongin"), its lw $t9 pinned, becomes jal m1_tidal_login, which replaces
        # the page when it stays unbuilt under the login (no saved login), as HiFi Music's page replaces itself
        # with its login (0x487eec). Back from the login then unwinds to the page that opened Tidal.
        'TIDAL_LOGIN': ((0x4b9e94, 0x8f99a704, None), (0x4b9e98, 0x04115fb9, 'm1_tidal_login')),
        # The Tidal and HiFi Music login pages' back buttons (0x4c703c, 0x49aa54; HiFi's dialog_quit first, which
        # returns at once on a window) call navigator_back_to_home: they call navigator_back (GOT -0x5528)
        # instead. Tidal's is a bal with its $t9, HiFi's a jalr; login success and logout keep their Home.
        'LOGIN_BACK': ((0x4c704c, 0x8f99ade4, 0x8f99aad8), (0x4c7058, 0x04112c11, 0x04112c20),
                       (0x49aa7c, 0x8f99ade4, 0x8f99aad8)),
    },
}
CALL_SITE_PURPOSES = {
    'BOOT_MODE_CALL': 'config_init preserves the saved queue when applying the boot play mode',
    'ARTIST_ALBUMS': 'artist detail opens on Albums',
    'SHUFFLE_CALL': 'shuffle honours Play next',
    'HOLD_RETURN': 'long Return destination after stock input gates',
    'STANDBY_WAKE': 'Standby resume stays dark',
    'BT_CONNECT_START': 'Bluetooth: Resume on connect',
    'SCAN_LIMIT': 'scan up to 65,000 songs',
    'DROP_CACHES': 'keep the page cache',
    'PLAYER_COVER': 'Now Playing art through ffmpeg',
    'BT_INIT': 'Bluetooth callbacks before control thread',
    'BT_PARAMS': 'Bluetooth state initialized before control thread',
    'BT_STATUS': 'Bluetooth: incoming link during a connect',
    'BT_AUTOLINK': 'Bluetooth: auto-link keeps an incoming link',
    'SCAN_REFRESH': 'folder scan refreshes existing tags',
    'FOLDER_NAME': 'folder names are literal text',
    'ID3_PATH': "a CUE track's file tags",
    'LYRIC_FOLLOW': 'lyric rows whole at the top',
    'LYRIC_ROWS': 'lyrics keep their place on a refresh',
    'GRID_COVER': 'Ogg art in Albums and Folder view',
    'NP_INFO_CALL': "Now Playing's info lines",
    'LDAC_HQ': 'LDAC HQ sends 990 kbps',
    'WHEEL_TS_READ': 'wheel ticks',
    'AUDIO_EXTENSION_CALLS': 'recognize M4B alongside existing audio extensions',
    'SORT_TRIMS': 'sort without a leading article',
    'ALBUM_ART': 'same-named albums apart in art',
    'CLASS_ICON': 'Artists rows without the head picture',
    'COVER_PAUSE': 'album grids never pause the cover worker',
    'ARTIST_COVER_ROW': "an artist's albums request the covers in view",
    'COVER_DONE': 'discard stale cover completion',
    'LOCKSCREEN_ACCESS': 'a built-in wallpaper survives a reboot',
    'LYRIC_SOURCES': "a found lyric isn't overwritten by NetEase's",
    'FOLDER_PLAY': 'a Folder play replaces the open Now Playing',
    'HOLD_KEYS': 'Play/Pause and Return hold time',
    'MAINSCHEDULING_CALL': 'pace player scheduling',
    'TAG_TEXT': 'tag text GBK only when it reads as GBK',
    'CUE_TEXT': 'CUE text read as UTF-8, GBK or Windows-1252',
    'SCAN_DIRS': 'the library scan skips hidden folders',
    'STREAM_POLL_CALLS': 'stream threads park while idle',
    'DARK_POLLS': 'stock polls idle while dark',
    'LYRIC_OPEN': 'lyric files read as tags are',
    'LYRIC_SAVE': 'lyrics saved beside the song',
    'COVER_SAVE': 'covers saved beside the song',
    'TIDAL_PAGE_DONE': 'Tidal lists load every page',
    'M3U_DIR_CALL': 'card apps import only their own playlists',
    'TIDAL_LOGIN': "Tidal's login replaces its unbuilt main page",
    'LOGIN_BACK': 'Back from the Tidal and HiFi Music logins goes back, not Home',
    'MQA_ACCEPT': 'saved MQA mode on every player connection, including boot',
}
def call_sites(m1plus): return CALL_SITES['m1plus' if m1plus else 'q2']
def call_site_words(m1plus, ps):
    """Each of the model's call-site words as (name, address, original, replacement), the
    replacement resolved against the payload's symbols ps (a pin's is its original)."""
    return [(name, address, old, old if new is None else 0x0c000000 | ps[new] >> 2 if isinstance(new, str) else new)
            for name, words in call_sites(m1plus).items() for address, old, new in words]
# The port report (test/m1plus/ports.py): each Q2 hook and call site the M1 doesn't have by the same
# name, or for a hook the same payload symbol, as (status, why). ported: by another route; native: V2.1
# does it itself; q2only: by design (docs/m1plus-roadmap.md, "Already Q2-only by design"); unported:
# a roadmap U4 row. Each IPOD_HOOKS entry the M1 doesn't hook has its own unported row, naming the
# docs/m1plus-ipod-ui.md item that ports it. A sync adds a row for each
# new upstream hook or site it doesn't port, and the report fails until it has one.
M1PLUS_PORTS = {
    # Hooks
    'createPlayListItem': ('unported', 'playlist ID allocation (1.5.5); V2.1 allocator not yet pinned'),
    'playlist_delete_click': ('unported', 'transactional playlist deletion (1.5.5); V2.1 delete callback not yet pinned'),
    'on_wm_keydown_before_fun': ('q2only', "Key Tone's click on the wheel's press; V2.1 has no buzzer command (progress 15)"),
    'buzzeer_switch': ('q2only', 'Key Tone; V2.1 has no buzzer command (progress 15)'),
    'localmusic_page_init': ('ported', "the Library's rows are the Q2 Pod page's Library page (progress 17)"),
    'load_localartist_list': ('ported', "V2.1 has no such function: an artist's albums are loadLocalClassList(0xff01), "
                              'hooked as ringnav_localclass (progress 12)'),
    'screensaver_rows': ('ported', "V2.1 has no rows hook: the Lock screen page's rows are lockscreen_page's (progress 28)"),
    'stream_page_init': ('ported', 'V2.1 has no native Streaming page: streaming_open provides native Tidal, Spotify, '
                         'optional backends and apps, Internet Radio, AirPlay and Configuration'),
    'keylock_rows': ('native', "V2.1's Buttons lock has a switch and Volume, Keys and All modes (roadmap 4)"),
    'quick_lock': ('native', "V2.1's Buttons lock (roadmap 4)"),
    'dialog_statusbar_dialog_init': ('native', "quick settings' lock label, which goes with quick_lock (roadmap 4)"),
    'read_artistype_value': ('native', "V2.1's Artists page has its own Artist/Album Artist switch (roadmap 4)"),
    'saver_cover': ('native', "V2.1's image_base_set_image always invalidates (progress 29)"),
    'folder_load_top': ('unported', "Folder's roots list OTG without a drive; V2.1's folder roots aren't checked yet"),
    'select_timezone': ('unported', "the extra time zones (1.2.9); V2.1's select_timezone is 0x4d6b2c, but its 27 "
                        'labels are a pointer table (0x97c810) its row layout (0x4a21c8) copies to the stack, and '
                        "its counts are at 0x4a246c, 0x4a2604, 0x4e65dc and 0x4d6b68 (roadmap U4)"),
    'toolsQueryContentDbTable': ('unported', "an artist's albums tab's album-artist rewrite (1.2.9); V2.1 has no "
                                 'toolsQueryContentDbTable'),
    'write_int_config': ('native', "Bluetooth's own saved level (1.3.8); V2.1 keeps it apart, [PLAYSET] BTVOLUME, "
                         '(m1plus_nav_btvol.c)'),
    'mclSetOutputWay': ('native', "each output's own level on a switch (1.3.8); V2.1's set_devicevolume takes "
                        "btsource_volume while the output is Bluetooth"),
    'localmusic_playlistsmore_page_init': ('ported', "V2.1 has no playlistsmore_page: a playlist row's hold opens "
                                           "the hold menu's playlist rows, whose More… is its editor "
                                           '(m1plus_nav_playlist_hold.inc, ipod-ui 4.4)'),
    'systemset_fwupdate_page_init': ('unported', "Network Update (1.3.8) fetches DiamondBond's Q2 update.tar; off "
                                     "until it points at the M1 releases. fwupdate_tf is M1PLUS_UNRESOLVED"),
    # The iPod UI's hooks (docs/m1plus-ipod-ui.md Phase 4): the shared C compiles with IPOD=1, but each of these is
    # unhooked until its item ports it
    'list_get_img_pic': ('native', "song rows' format badge, which the iPod hides: V2.1 has no list_get_img_pic, and "
                         "its song rows draw no badge but img_mqa (music_create_tablerow) (ipod-ui 4.4)"),
    'playlist_rebuild': ('unported', "the playlist rebuild's iPod rows (ipod-ui 4.7)"),
    'mclIsUtf8WithoutBOM': ('unported', "an .lrc's UTF-8 test that reads 4-byte characters (1.5.9); V2.1's "
                            'mclIsUtf8WithoutBOM is 0x5d1824, not yet checked'),
    # Call sites
    'ARTIST_ALBUMS': ('native', "V2.1's artist page lists the artist's albums (roadmap 4)"),
    'BOOT_MODE_CALL': ('native', 'V2.1 saves ARTISTTYPE and reads it in config_init (roadmap 4)'),
    'CLASS_ICON': ('native', 'V2.1 draws its own artist icon (roadmap 4)'),
    'ARTIST_COVER_ROW': ('native', "V2.1 has no artist page of 160 px rows: an artist's albums are an album list, "
                         'whose covers COVER_PAUSE and ALBUM_ART cover (progress 12, 30)'),
    'HOLD_RETURN': ('ported', "long Return's Now Playing (compact_now_playing): on the M1, Previous's hold where it "
                    "is Back (ringnav_keylong's hold_previous, AWTK's 1000 ms key-long) and the chevron's (chevron_hold) "
                    '(ipod-ui 4.4)'),
    'STANDBY_WAKE': ('q2only', "Standby resume staying dark goes with the Q2's Centre-key Wake; V2.1 has Double wake"),
    'WHEEL_TS_READ': ('q2only', 'the touch wheel'),
    'MAINSCHEDULING_CALL': ('unported', 'paced player scheduling (1.5.5); V2.1 call site not yet pinned'),
    'HOLD_KEYS': ('unported', "Play/Pause's hold at 700 ms (1.4.5); V2.1's input_device_status is unnamed, and the "
                  'M1 opens the hold menu with a touch long-press too'),
    'STREAM_POLL_CALLS': ('native', "V2.1 creates a Tidal URL worker per request (get_tidal_trackurl, 0x512ed0); "
                          "no boot worker or idle start-flag poll, and no Baidu Pan"),
    'TIDAL_PAGE_DONE': ('unported', 'Tidal lists past 50 (1.5.0): goes with the Tidal list threads'),
    'M3U_DIR_CALL': ('unported', "a card app's library update imports only its own playlists (1.5.9); V2.1's "
                     'importPlayList is 0x4ef394, its listing call not yet found'),
    'timezone_row': ('unported', "the time zone rows' offsets in effect now (1.5.0): goes with select_timezone"),
    'folder_click': ('unported', "videos played from Folder view (1.5.0), where the Q2's Videos row now opens; "
                     "V2.1's folder row click is not yet found. The M1's Videos row keeps 1.4.5's list "
                     '(m1plus_books_video.c videos_open)'),
    'main_loop_post_key_event': ('unported', "SyncLink's keys past the Buttons lock (1.5.0); V2.1's is 0x693d9c, "
                                 'and its Buttons lock is its own (keylock_rows native): not yet checked'),
    'device_reboot': ('unported', "a reboot saves the queue first (1.5.0); V2.1's device_reboot is 0x4e743c, its "
                      'queue on a reboot not yet checked'),
    'dialog_checkfw_dialog_init': ('unported', "the firmware update's dialog saves the queue (1.5.0); V2.1 has no "
                                   'dialog_checkfw_dialog_init by name'),
    'get_tidal_trackurl': ('native', "V2.1 launches an on-demand URL worker instead of waking a polling worker"),
    'tidalPlaylistDetailThd': ('unported', "Tidal playlists past 50 (1.5.0); V2.1's is 0x516b9c, but V2.1 has no "
                               'tidal_albuminfo_thread_run, its done flag not yet found'),
    'tidalAlbumDetailThd': ('unported', "Tidal albums past 50 (1.5.0); V2.1's is 0x5178cc, its done flag not yet "
                            'found'),
    'tidalColTracksThd': ('unported', "Tidal favourite tracks past 50 (1.5.0); V2.1's is 0x51b2d4, but V2.1 has no "
                          'tidal_collection_thread_run, its done flag not yet found'),
}
PDR_M1PLUS = (0x5f388c, 0x65800)  # demo's .pdr, as build.py's PDR
M1PLUS_GLOBAL_ALIASES = {
    'g_playspeed_mode': 'playspeed_mode',
    'g_backlight_status': 'backlight_status',
    'g_lockscreen_pageflag': 'lockscreen_pageflag',
    'g_keylock_flag': 'keylock_flag',
    'g_keylock_mode': 'keylock_mode',
    'g_bluetoothflag': 'bluetoothflag',
    'g_usblink_status': 'usblink_status',
    'g_equalizer_flag': 'equalizer_flag',
    'g_playcover_type': 'playcover_type',
    'g_folder_layer': 'folder_layer',
    'g_otg_status': 'otg_status',
    'g_delete_flag': 'delete_flag',
    'g_volume': 'volume',
    'g_po_status': 'po_status',
    'g_bal_status': 'bal_status',
    'g_usbvol_mode': 'usbvol_mode',
    'g_usbdac_chargeflag': 'usbdac_chargeflag',
    'g_memory_play': 'memory_play',
    'g_headset_output': 'headset_output',
    'g_usbdet_value': 'usbdet_value',
    'g_time24h_flag': 'time24hflag',
    'bt__recv_pageflag': 'btrecv_pageflag',
    'g_maxvolume': 'max_volume',
    'g_carmode': 'car_mode',
    # Matched by their users in both firmwares (config_init's first-boot guide; folder_enter and
    # folder_back clear the navbar state).
    'g_guideflag': 'first_guideflag',
    'g_navbar_status': 'navigation_status',
    'g_btvolume': 'btsource_volume',
    'g_rotate_mode': 'rotate_mode',
    'g_time_zone': 'time_zone',
    # Songs' sort (navigation.c songs_sorted, 1.6.3): V2.1's getAllMusic takes no argument and reads it itself
    'g_sort_flag': 'sort_flag',
}
# V2.1 globals V1.32 lacks, read as GLOBALS are. Bluetooth keeps its own level, [PLAYSET] BTVOLUME:
# the volume dialog (on_volume_tsup_fun), status bar and set_devicevolume use it while headset_output
# is 2, and `volume` stays the jacks'. on_wm_keyup_fun swaps Previous and Next, and the volume keys,
# while rotate_mode is 1 (the rotated screen, 0x4cd9f8).
M1PLUS_GLOBALS = ['g_btvolume', 'g_rotate_mode']
# V2.1 data V1.32 lacks, read as CONTEXT_DATA is (sizes checked). The grid's cards (pdeq_choicemenu) left with the iPod
# Home (ipod-ui 4.5); Tidal's session holds the saved login m1_tidal_login reads (TIDAL_SAVED_LOGIN).
M1PLUS_CONTEXT_DATA = {'theTidal': 2628}
# Renamed in V2.1; each has the size of its V1.32 counterpart (checked in m1plus_symbols).
M1PLUS_CONTEXT_ALIASES = {
    # The track whose cover the player's files hold (ipod-ui 4.5, Home's art): parseplaycover_thd clears it while it
    # parses (0x4defec) and writes the track's path once its files are written (0x4df1a0), as V1.32's g_lastcover_url.
    'g_lastcover_url': 'savecover_path',
    'g_folder_path': 'folder_path',
    'g_dacoff_time': 'dacoff_time',
    'g_power_capacity': 'power_capacity',
    'g_screensaver_picture': 'screensaver_picture',
    'g_memory_info': 'meminfo_save',
    'g_class_type': 'cur_classtype',
    'g_local_classinfo_save': 'classinfo_save',
    'p_deque_showlist': 'pdeq_showlist',
    'p_deque_playlist': 'pdeq_playlist',  # the playlists getAllPlayList loads (loadLocalClassList, 0x4ee634)
    'p_vector_select_record': 'pvec_selectrecord',
    'g_play_id3_info': 'playsong_id3info',
    'p_deque_screensaverlist': 'pdeq_screensaverlist',
    'g_power_chargestate': 'pmucharge_status',  # get_battery_capacity keeps 0-2 in both
}
# V1.32's g_artist_type (load_localclass_list's flag) has no V2.1 twin: loadLocalClassList reads
# artist_type itself, which home_page_init saves, so the payload's flag keeps its own storage.
# A V1.32 global with no V2.1 counterpart gets zeroed storage of its own in the payload's .scratch
# (m1stub_<name>), never a guessed address. Every reader must treat zero as "off" or "none".
M1PLUS_STUB = 'm1stub_'
# V2.1 globals without a symbol. on_wm_keylong_fun sets this byte on a long power (knob) press
# (0x4cde14) and on_wm_keyup_fun drops that release and clears it (0x4cdc5c), as V1.32 does.
M1PLUS_RAW_GLOBALS = {'g_power_longkey': 0xa041b8}
# Local V2.1 routines, each checked to be a PIC entry with V2.1's GOT base.
M1PLUS_PRIVATE_FUNCTIONS = {
    'm1_home_click': 0x533b80,  # V2.1 Home destination dispatcher; widget name is the native menu id

    # The status bar's 1 s tick (docs/m1plus-ipod-ui.md 4.2): systembar_timer_start (0x5453c8) arms a 1000 ms timer on
    # 0x545394, which calls this with 0. It finds the bar's widgets by name from the system_bar global, as the Q2's
    # systembar_showface finds them from its argument, and sets their images and text but not their geometry.
    'systembar_showface': 0x544b48,
    'slide_menu_on_scroll_done': 0x6123f4,  # what slide_menu's scroll_to binds to its animator's end (0x612320)
    'folder_refresh': 0x5318ac,  # folder_page_init's (0x53354c): navbar and table from pdeq_showlist
    'album_row': 0x4e93c8,  # getAllAlbum's toolsQueryDbTable callback (0x4ea458): a record to tools_pdeq_directory
    'gif_image_create': 0x5fb69c,
    'mcl_shuffle_pick': 0x5d03b0,  # mclNextSong's and mclPrevSong's shuffle pick (SHUFFLE_CALL)
    # The Lock screen page's pick (systemset_screensaver_page_init's visit binds the first six
    # pictures' clicks to it): the picture's index into pdeq_screensaverlist, saved and checked
    'saver_pick': 0x4ab52c,
    'mcl_preload': 0x5d0ea4,  # the gapless pick and its open, hooked (M1PLUS_HOOKS) as on the Q2
    'mcl_open_preload': 0x5d0bd8,
    'btmenu_rows': 0x4a3734,  # the Bluetooth page's list: switch, name, quality, volume, search, devices
    # Now Playing's info page: its labels from the playing track, "Label:value" (show_player_face's bal, NP_INFO_CALL)
    'np_info': 0x539c40,
    'volume_refresh': 0x47d664,  # the volume dialog's label, bar and slider from the output's level (on_volume_tsup_fun)
    # The library title bar's Search button (0x5230a8 binds it, in search_style): navigator_to("search_page"), V2.1's
    # library search, which pull to search opens (ipod-ui 4.4; m1plus_ipod.json private_prologues).
    'stock_search': 0x523304,
}
# V1.32 routines V2.1 has no twin of yet, called only from a Q2 hook the M1 leaves unported: declared
# with no address, so the page compiles and --gc-sections drops it. The link fails if live code
# reaches one (not for navigation.c: M1PLUS_SHIMS). Each goes with its hook's U4 row.
M1PLUS_UNRESOLVED = {
    'fwupdate_tf': 'Network Update (netupdate.c): stock\'s TF card update, systemset_fwupdate_page_init unported',
}
# V1.32 routines V2.1 has no twin of that navigation.c names, which is one section (the tests call its unhooked
# routines, so --gc-sections cannot drop any): a stand-in in patch/m1plus_nav.h under the same name, as (status, why).
# The shipped payload drops the ones nothing calls. native: V2.1 does it itself; q2only: by design; unported: the
# docs/m1plus-ipod-ui.md item that ports it. test/m1plus/ports.py reports them.
M1PLUS_SHIMS = {
    'buzzeer_switch': ('q2only', 'Key Tone; V2.1 has no buzzer command (progress 15)'),
    'tk_str_end_with': ('ported', "its own C: V2.1's AWTK lacks it"),
    'image_manager_unload_bitmap_by_name': ('ported', "its own C on V2.1's image_manager_lookup and "
                                            'image_manager_unload_bitmap (ipod-ui 4.5)'),
}
M1PLUS_FUNCTION_ALIASES = {
    'device_set_volume': 'set_devicevolume',
    'config_outputchannel': 'set_outputchannel',
    # ringnav_boot's paused boot resume (ipod-ui 4.5): (queue, index, class, mode), as playing_page_init (0x53d28c) calls it
    'player_start': 'start_player',
    'player_stop': 'stop_player',  # mclStop with the mute, seek, play status and headset updates (V1.32 has both)
    'player_play_pause': 'play_pause_music',
    'player_prev_music': 'prev_music',
    'player_next_music': 'next_music',
    'player_save_start': 'save_start_player',
    'folder_reload_data': 'folder_reload',
    'player_playtime_and_length': 'get_playtimeandlength',
    'player_seek_time': 'seek_time',
    'switch_charge_enable': 'toolsSetChargeSwitch',
    'taglib_file_open': 'taglib_file_new',
    # Now Playing's position timer, which the scrub stops and restarts: V2.1's playing_page_init starts
    # player_timer_start (0x53c210) and player_timer_clear (0x53c758) ends it. V1.32's shape; the
    # interval is 500 ms where V1.32's is 250.
    'playing_timer_start': 'player_timer_start',
    'playing_timer_clear': 'player_timer_clear',
    # The batch record (pvec_selectrecord): n rows unselected, then one row's selection toggled
    'batch_init_selectrecord': 'select_recordinit',
    'batch_set_selectitem': 'set_selectindex',
    # delete_playqueue_file calls it where V1.32's calls player_start_queue (0x4e4a80): the queue row's play
    'player_start_queue': 'start_playqueue',
    # folder_back calls it where V1.32's calls folder_reset_variable (0x4dbf0c): a fresh Folder visit.
    # V2.1's clears one enter-history deque where V1.32's clears two, and its flags are words.
    'folder_reset_variable': 'clear_foldervariate',
    # Library -> Songs' load (navigation.c songs_load, 1.6.3): loadLocalClassList's default calls it with
    # 0xf001 after getAllMusic, where V1.32's load_localclass_list calls music_nagvation_title
    'music_nagvation_title': 'musicNagvationTitle',
}
M1PLUS_HOOKS = {
    'widget_on_paint_border': (0x668810, 'ringnav_paint', 'paint'),
    'systembar_showface': (0x544b48, 'ringnav_showface', 'showface'),  # V2.1's show_sysbar_face (ipod-ui 4.2)
    # The iPod UI's paint backbone (ipod-ui 4.1): the selection bar behind the rows, the accents and Light Mode on every
    # style colour and cached image, and each window's asset
    'widget_on_paint_background': (0x66b778, 'ringnav_paint_bg', 'paint_bg'),
    'style_get_color': (0x659fcc, 'ringnav_style_color', 'color'),
    'image_manager_add': (0x655638, 'ringnav_image_add', 'image'),
    'ui_loader_load_widget_with_parent': (0x663a74, 'ringnav_ui_load', 'ui_load'),
    'widget_dispatch': (0x66cec8, 'ringnav_dispatch', 'dispatch'),
    'on_wm_keylong_fun': (0x4cdd9c, 'ringnav_keylong', 'keylong'),
    'playset_equalizer_page_init': (0x49e358, 'peq_page_init', None),
    'set_equalizer_value': (0x4d851c, 'peq_stock_eq', 'eq'),
    'home_page_init': (0x534cd4, 'coverflow_home', 'home'),
    'toolsQueryDbTable': (0x5ee77c, 'ringnav_library_query', 'dbquery'),
    # Songs by filename and by format (sort_filename, sort_format); V2.1's title sort runs toolsQueryDbTable
    'toolsQueryDbTableAndSort': (0x5ee9ac, 'ringnav_sorted_query', 'sorted_query'),
    'scanAllMusicFile': (0x4e9df4, 'coverflow_scan_all', 'scan_all'),
    'scanSpecFolder': (0x4e9e90, 'coverflow_scan_folder', 'scan_folder'),
    'deleteMusicFromMusicDb': (0x4ede44, 'coverflow_delete_song', 'delete_song'),
    'main_loop_sleep_default': (0x658f70, 'ringnav_sleep', 'sleep'),
    'systemset_about_page_init': (0x4a170c, 'ringnav_about', 'about'),
    'folder_page_init': (0x53349c, 'ringnav_folder', 'folder'),
    'folder_back': (0x4dbecc, 'ringnav_folder_back', 'folder_back'),
    'window_manager_dispatch_input_event': (0x677b74, 'ringnav_input', 'input'),
    'systemset_sysset_page_init': (0x4ada78, 'ringnav_systemset', 'systemset'),
    'systemset_display_page_init': (0x4a5eb8, 'ringnav_display', 'display'),
    'get_screensaver_image': (0x4d7524, 'lockscreen_images', 'saverlist'),
    'save_memoryplay_info': (0x4e3340, 'ringnav_savequeue', 'savequeue'),
    'mclLoadPlayList': (0x5d1f28, 'ringnav_load', 'load'),
    'mclNextSong': (0x5d5800, 'ringnav_next', 'next'),
    'mclPrevSong': (0x5d56dc, 'ringnav_prev', 'prev'),
    'mclSetPlayMode': (0x5d278c, 'ringnav_mode', 'mode'),
    'mclSetPlaySpeed': (0x5d281c, 'ringnav_speed', 'speed'),
    # A queue row's pick (View Queue, stock's View Queue dialog, a queue delete) in a shuffle's play
    # order: V1.32's player_start_queue. The payload's player_start_queue calls reach it by alias.
    'start_playqueue': (0x4e47d0, 'ringnav_start_queue', 'start_queue'),
    # A track's LYRICS tag without a .lrc; stock's loader runs first, from every caller's GOT call
    'mclLoadExLyric': (0x5d41e4, 'ringnav_lyric', 'lyric'),
    # Online lyric and cover search: LRCLIB, then MusicBrainz and iTunes, before stock's Kugou. Both,
    # online_getkeyword_info and online_setkeyword_info are V1.32's but for their data addresses.
    'kugou_obtainlyric': (0x509ee4, 'ringnav_lyric_search', None),  # LRCLIB alone (1.5.0): no stock trampoline
    'kugou_obtaincover': (0x50aa78, 'ringnav_cover_search', 'kugoucover'),
    # The status bar's Wi-Fi signal from rtl8733bs's rx_signal, which keeps the radio's power save;
    # V2.1's asks the radio (SIOCGIWSTATS), as V1.32's does
    'networkGetWifiSignal': (0x5d76a8, 'ringnav_wifi_signal', None),
    # Standby Limit: into_standby's suspend to RAM (V1.32's device_standby's), V1.32's instruction for
    # instruction; the M1's rtc-ingenic has the same wakealarm
    'toolsIntoStandby': (0x5e5228, 'ringnav_standby', 'standby'),
    # Gapless: the next track's pick and its decoder's open, V1.32's moved
    'mcl_preload': (0x5d0ea4, 'ringnav_preload', 'preload'),
    'mcl_open_preload': (0x5d0bd8, 'ringnav_open_preload', 'open_preload'),
    # The Bluetooth page's list builder, rebuilt whole on every search and switch: Resume on Connect
    'btmenu_rows': (0x4a3734, 'ringnav_btrows', 'btrows'),
    'memeory_startplayer': (0x4e34dc, 'ringnav_memory', 'memory'),
    'systemset_powermanager_page_init': (0x4a9d18, 'ringnav_powermanager', 'power'),
    'playset_playset_page_init': (0x4a0c88, 'ringnav_audioset', 'audioset'),
    'mclStartPlayer': (0x5d5300, 'ringnav_start_player', 'start_player'),
    'mcl_tidalStartPlayer': (0x5d5184, 'tidal_start', 'tidal'),
    'playing_page_init': (0x53d1e4, 'ringnav_playing', 'playing'),
    'bigcover_page_init': (0x529a24, 'ringnav_bigcover', 'bigcover'),
    'on_wm_keyup_fun': (0x4cd9ac, 'ringnav', 'keyup'),
    'on_wm_before_tsdown_fun': (0x4cd608, 'ringnav_touch', 'touch'),
    'screensaver_page_init': (0x53fd44, 'lockscreen_init', 'saver'),
    # The Lock screen page: its picture grid, Time show and About; V2.1 has no rows hook
    'systemset_screensaver_page_init': (0x4abe04, 'lockscreen_page', 'saverpage'),
    'loadLocalClassList': (0x4ee504, 'ringnav_localclass', 'localclass'),
    'loadAlbumdetailList': (0x4eea98, 'ringnav_album_detail', 'detail'),
    'change_music': (0x4e3cec, 'ringnav_change', 'change'),
    # Bluetooth absolute volume: V2.1 merged V1.32's mclSetLocalVol and mclSetBtVol into mclSetVol
    'mclSetVol': (0x5d4cb0, 'ringnav_btvol', 'btvol'),
    # The hold menu: its sortselect_dialog opens non-modal, as V1.32's init leaves it
    'dialog_sortselect_dialog_init': (0x47d358, 'qm_sortselect_init', 'sortselect'),
    # A manual Play/Pause (V2.1's playpause_quick_click, DLNA, the payload's own) is marked, so a
    # headset's automatic resume doesn't undo it: V1.32's player_play_pause, (void) -> int as V2.1's
    'play_pause_music': (0x4e43b4, 'ringnav_play_pause', 'pause'),
    # A FLAC's ALBUM ARTIST when libtag finds no ALBUMARTIST; V2.1's (a, info, path), V1.32's
    # instruction for instruction, keeps the album artist at +0x580
    'toolsGetMusicInfo': (0x5ec6a8, 'ringnav_music_info', 'music_info'),
    # A song's added date: the card's creation stamp, not the access time (coverflow.c, 1.6.4). V2.1's is V1.32's
    # (access check, then stat), its three callers in the library scan's song records.
    'toolsGetFileCreateTime': (0x5e4ac8, 'ringnav_file_created', 'file_created'),
    # USB mode's page, as a cable to a computer opens it, before stock unmounts the card for USB
    # storage: the card apps end first (addon_card_away). V2.1's init binds its window as V1.32's.
    'dialog_playmore_dialog_init': (0x479cc4, 'ringnav_playermore', 'playermore'),
    'usbmode_page_init': (0x545dd8, 'ringnav_usbmode', 'usbmode'),
}

def m1plus_symbols(syms, symbol_table):
    """Resolve V1.32 names against the V2.1 demo: aliases (size-checked), then stubs.

    Returns syms with the aliases applied and the [(name, size)] that get m1stub_ storage. Private
    V1.32 routines are never merged: their addresses are V1.32 code."""
    syms = dict(syms)
    def size(name):
        found = re.search(rf'\b(\d+)\s+OBJECT\s+GLOBAL\s+DEFAULT\s+\d+\s+{re.escape(name)}$', symbol_table, re.M)
        return int(found.group(1)) if found else None
    for k, v in M1PLUS_FUNCTION_ALIASES.items():
        if v in syms: syms[k] = syms[v]
    syms.update(M1PLUS_PRIVATE_FUNCTIONS)
    stubs = []
    for name in GLOBALS + M1PLUS_GLOBALS:  # payload reads one byte: little-endian, a 4-byte flag's low byte
        alias = M1PLUS_GLOBAL_ALIASES.get(name, name)
        if name in M1PLUS_RAW_GLOBALS:
            syms[name] = M1PLUS_RAW_GLOBALS[name]
            continue
        check(name not in M1PLUS_GLOBALS or size(alias) is not None, f'{name}: no {alias} in V2.1')
        if size(alias) is None:
            stubs.append((name, 1))
            continue
        check(size(alias) in (1, 4), f'{name}: {alias} is not a byte or word global')
        syms[name] = syms[alias]
    for name, want in CONTEXT_DATA.items():
        alias = M1PLUS_CONTEXT_ALIASES.get(name, name)
        if size(alias) is None:
            stubs.append((name, want))
            continue
        check(size(alias) == want, f'{name}: {alias} context data size mismatch')
        syms[name] = syms[alias]
    for name, want in M1PLUS_CONTEXT_DATA.items():
        check(size(name) == want, f'{name}: no {want}-byte {name} in V2.1')
    return syms, stubs

def m1plus_names(sq, out):
    """Every stock widget, image and style the M1 Plus payload names (patch/offsets.inc VIEW_, ICON_,
    STYLE_, ROW_ and ABOUT_, as it compiles them) is in V2.1's rootfs: a V1.32 name there finds
    nothing, and a missing style draws AWTK's light default."""
    from ipod import decode, walk, style_props
    defines = dict(re.findall(r'^#define ((?:VIEW|ICON|STYLE|ROW|ABOUT)_\w+) "([^"]+)"$',
                              run('clang', '-E', '-dM', '-DM1PLUS=1', '-x', 'c', ROOT/'patch/offsets.inc'), re.M))
    check(defines, 'No M1 Plus asset names in patch/offsets.inc')
    tree = out/'v21-assets'
    run('unsquashfs', '-q', '-no-xattrs', '-f', '-d', tree, sq, 'release/assets/default/raw/ui',
        'release/assets/default/raw/styles/default.bin', 'release/assets/default/raw/styles/home_page.bin',
        'release/assets/default/raw/styles/playing_page.bin',
        'release/assets/default/raw/images/xx')
    raw = tree/'release/assets/default/raw'
    widgets = {n[2].get('name') for p in raw.glob('ui/**/*.bin') for n in walk(decode(p.read_bytes()))}
    # Home's cards and Now Playing's heart are styled from their pages' own files, which those pages'
    # widgets use.
    styles = {s for f in ('default', 'home_page', 'playing_page') for _, s, *_ in style_props((raw/f'styles/{f}.bin').read_bytes())}
    images = {p.stem for p in raw.glob('images/xx/*')}
    for key, value in sorted(defines.items()):
        kind = ('image', images) if key.startswith('ICON_') or key == 'ROW_CHEVRON' else \
               ('style', styles) if key.startswith('STYLE_') or key.endswith('_STYLE') else ('widget', widgets)
        check(value in kind[1], f'{key}: no {kind[0]} named {value!r} in V2.1')
    import shutil
    shutil.rmtree(tree)

def pic_gp(image, address):
    """The GOT base a PIC entry (lui $gp; addiu $gp; addu $gp, $t9) computes, else None."""
    lui, addiu, addu = struct.unpack_from('<III', image, fileoff(image, address))
    if lui >> 16 != 0x3c1c or addiu >> 16 != 0x279c or addu != 0x0399e021: return None
    low = addiu & 65535
    return ((lui & 65535) << 16) + (low if low < 32768 else low - 65536) + address

def m1plus_inc(name):
    """An integer #define of patch/offsets.inc as the M1 Plus payload compiles it."""
    found = re.search(rf'^#define {name} (0x[0-9a-f]+|\d+)$', run('clang', '-E', '-dM', '-DM1PLUS=1', '-x', 'c',
                                                              ROOT/'patch/offsets.inc'), re.M)
    check(found, f'{name}: not defined for M1 Plus')
    return int(found.group(1), 0)

def stub_asm(stubs):
    """Zeroed .scratch storage for the stubbed globals (link.ld maps .scratch R/W, zero-filled)."""
    asm = ['.section .scratch,"aw",@nobits', '.balign 8']
    for name, size in stubs:
        asm += [f'.globl {M1PLUS_STUB}{name}', f'{M1PLUS_STUB}{name}:', f'.space {(size + 7) & ~7}']
    return '\n'.join(asm) + '\n'

# hciplayer: the PEQ, ReplayGain and MP3 seek patch (tools/peq.py) at V2.1's addresses, each found in V2.1's
# binary; peq.py's constants are V1.32's.
M1PLUS_PLAYER_SHA = 'a64503746862af3e69b57f2e06167351b30cda28479348a845be5172e083a8c6'
PLAYER_PROFILE = {
    'desc': 0x893808,
    'desc_bytes': 'bc3789002c5e88004c358900b8c388000100000014fd4400',
    'open_slot': 0x89381c,
    'vbr_scan': 0x48f5fc,
    # mpctx's three loads fed only the gate and fault with no sh_audio (Q2 0x42cec0, docs/internals.md#music-info-between-songs)
    'eq_rate_gates': ((0x42ce24, 0x8c429e30, 0), (0x42ce28, 0x8c42002c, 0), (0x42ce2c, 0x8c42003c, 0),
                      (0x42ce34, 0x10400098, 0),
                      (0x42fa78, 0x14400052, 0x10000052)),  # bnez $v0 to the insert -> b
    # MPlayer pause loop: usec_sleep(20000) in its command/event loop, 50 ms as upstream.
    'pause_sleep': (0x42ff2c, 0x24044e20, 0x3404c350),
    'seek_slot': 0x89f76c,
    'stock_seek': 0x48cc6c,
    'id3_calls': (0x48ee74, 0x492028, 0x492ab4),
    'stock_id3': 0x48b760,
    'written_audio_pts': 0x44600c,
    'length_addr': 0xb10e5c,
    'av_dict_set': 0x6ea1a4,
    'av_dict_free': 0x6ea65c,
    'rg_export': 0x5381c4,
    'hr_mp3_seek': 0xb15298,
}
# libc/libcstl imports only the M1 payload uses, placed after peq.py's deque_pop_back.
M1PLUS_LIBC = {
    # V2.1 imports no deque_pop_back; navigation.c erases the last element through these
    'deque_begin': ('cstl_iter', 'const void *'), 'deque_end': ('cstl_iter', 'const void *'),
    'deque_erase': ('cstl_iter', 'void *, cstl_iter'), 'iterator_next': ('cstl_iter', 'cstl_iter'),
    'iterator_equal': ('int', 'cstl_iter, cstl_iter'),
}

def m1plus_libc(libc):
    """peq.py's LIBC with M1PLUS_LIBC after deque_pop_back: the import stubs' order is the payload's layout."""
    out = {}
    for name, value in libc.items():
        out[name] = value
        if name == 'deque_pop_back': out.update(M1PLUS_LIBC)
    return out

def compile_common(out, binary, player=False):
    """peq.compile_common for V2.1: its imports, V2.1's symbols, and the player's addresses."""
    from peq import LIBC
    got = {}
    for line in run('readelf', '-AW', binary).splitlines():
        words = line.split()
        if len(words) >= 6 and 'UND' in words and re.fullmatch('[0-9a-f]{8}', words[0]):
            got[words[-1].split('@')[0]] = int(words[0], 16)
    gp = 0xb16750 if player else M1PLUS_GP
    header = ['struct dirent { unsigned ino, off; unsigned short reclen; unsigned char d_type; char d_name[256]; };',
              'typedef struct { void *w[7]; } cstl_iter; /* libcstl 2.2 iterator_t, passed by value */']
    asm = ['.set noreorder', '.text']
    for name, (ret, args) in m1plus_libc(LIBC).items():
        # Unused I/O is removed by --gc-sections in the player payload.
        alias = {'fopen': 'fopen64', 'readdir': 'readdir64', 'pow': '__pow_finite'}.get(name, name) if player else name
        if name == 'localtime_r' and not player:
            libc = symbols(out/'libc-2.28.so')
            delta = libc['localtime_r@@GLIBC_2.0'] - libc['tzset@@GLIBC_2.0']
            check(delta == -7724, 'Unexpected libc localtime_r offset')
            header.append(f'extern {ret} peq_lib_{name}({args});')
            header.append(f'#define {name} peq_lib_{name}')
            address = got['tzset']
            asm += ['.section .scratch,"aw",@nobits', '.align 2',
                    'localtime_r_target: .space 4', f'.section .text.peq_lib_{name},"ax",@progbits',
                    f'.globl peq_lib_{name}', f'peq_lib_{name}:',
                    'lui $t8, %hi(localtime_r_target)', 'lw $t9, %lo(localtime_r_target)($t8)',
                    'bnez $t9, 1f', 'nop',
                    # Resolve tzset's lazy GOT entry once: unlike localtime, it writes no shared buffer.
                    'addiu $sp, $sp, -32', 'sw $ra, 28($sp)', 'sw $a0, 20($sp)', 'sw $a1, 24($sp)',
                    'jal peq_lib_tzset', 'nop', 'lw $ra, 28($sp)', 'lw $a0, 20($sp)',
                    'lw $a1, 24($sp)', 'addiu $sp, $sp, 32',
                    f'lui $t8, {address >> 16}', f'ori $t8, $t8, {address & 65535}',
                    'lw $t9, 0($t8)', f'addiu $t9, $t9, {delta}',
                    'lui $t8, %hi(localtime_r_target)', 'sw $t9, %lo(localtime_r_target)($t8)',
                    '1:', 'jr $t9', 'nop']
            continue
        if alias not in got:
            header.append(f'extern {ret} {name}({args});')
            continue
        address = got[alias]
        header += [f'extern {ret} peq_lib_{name}({args});', f'#define {name} peq_lib_{name}']
        asm += [f'.section .text.peq_lib_{name},"ax",@progbits', f'.globl peq_lib_{name}',
                f'peq_lib_{name}:', f'lui $gp, {gp >> 16}', f'ori $gp, $gp, {gp & 65535}',
                f'lui $t8, {address >> 16}', f'ori $t8, $t8, {address & 65535}',
                'lw $t9, 0($t8)', 'jr $t9', 'nop']
        if name in ('memcpy', 'memset', '__udivdi3'):
            asm += [f'.globl {name}', f'.set {name}, peq_lib_{name}']
    if player:  # peq_player.c's stock addresses, V1.32's by default
        header += [f'#define {macro} 0x{PLAYER_PROFILE[key]:x}u' for macro, key in (
            ('WRITTEN_AUDIO_PTS', 'written_audio_pts'), ('LENGTH_ADDR', 'length_addr'), ('STOCK_ID3_ADDR', 'stock_id3'),
            ('AV_DICT_SET_ADDR', 'av_dict_set'), ('AV_DICT_FREE_ADDR', 'av_dict_free'), ('RG_EXPORT_ADDR', 'rg_export'),
            ('STOCK_SEEK_ADDR', 'stock_seek'), ('HR_MP3_SEEK_ADDR', 'hr_mp3_seek'))]
    if not player:
        # V1.32's private routines are V1.32 code: never merged into V2.1's table
        syms, stubs = m1plus_symbols(symbols(binary), run('readelf', '-Ws', binary))
        # A routine V2.1 hooks where V1.32 does not (on_wm_keyup_fun, ringnav's): the payload's own
        # replays reach stock through its trampoline, not back into the hook.
        from build import HOOKS
        resumed = {n: x for n, (_, _, x) in M1PLUS_HOOKS.items() if x and n not in HOOKS}
        for name, (ret, args) in (FUNCTIONS | M1PLUS_FUNCTIONS).items():
            if name in resumed:
                header += [f'extern {ret} stock_{resumed[name]}_trampoline({args});',
                           f'#define {name} stock_{resumed[name]}_trampoline']
            elif name in syms and syms[name]:
                header.append(f'#define {name} (({ret} (*)({args}))0x{syms[name]:x}u)')
            elif name in M1PLUS_UNRESOLVED or name in M1PLUS_SHIMS:
                header.append(f'extern {ret} {name}({args});')
        # build.py has already checked each is a one-byte global (or, on V2.1, a byte or word).
        stubbed = dict(stubs)
        for name in GLOBALS + M1PLUS_GLOBALS:
            if name in stubbed:
                header += [f'extern volatile unsigned char {M1PLUS_STUB}{name};', f'#define {name} {M1PLUS_STUB}{name}']
            else:
                header.append(f'#define {name} (*(volatile unsigned char *)0x{syms[name]:x}u)')
    (out/'peq_platform.h').write_text('\n'.join(header)+'\n')
    (out/'peq_imports.S').write_text('\n'.join(asm)+'\n')
    flags = [*FLAGS, '-fno-math-errno', '-ffunction-sections', '-fdata-sections', '-DM1PLUS=1']
    if player: flags += ['-mnan=2008', '-DPEQ_PLAYER=1']
    objects = []
    for name in ['peq.c', 'peq_player.c'] if player else ['peq.c', 'peq_ui.c', 'coverflow.c', 'm1plus_library_scope.c', 'scrobble.c', 'photos.c', 'books.c', 'games.c', 'visualizer.c', 'playback.c', 'upnext.c', 'spotify.c', 'addon.c', 'addon_library.c', 'radio.c', 'tidal.c', 'netupdate.c', 'onlinematch.c', 'crossfade.c', 'nightshift.c', 'headset.c', 'lockscreen.c', 'chapters.c', 'lyrics.c']:
        obj = out/(name+'.o')
        run('clang', *flags, '-I', out, '-c', ROOT/'patch'/name, '-o', obj)
        objects.append(obj)
    obj = out/'peq_imports.o'
    run('clang', *flags, '-c', out/'peq_imports.S', '-o', obj)
    objects.append(obj)
    if not player:
        (out/'m1stubs.S').write_text(stub_asm(stubs))
        run('clang', *flags, '-c', out/'m1stubs.S', '-o', out/'m1stubs.o')
        objects.append(out/'m1stubs.o')
    return objects

def patch_player(raw, out):
    """peq.patch_player for V2.1's hciplayer, at PLAYER_PROFILE's addresses."""
    from ipod import jal, patch_word
    from peq import PLAYER_BASE
    out.mkdir(exist_ok=True)
    binary = out/'stock-hciplayer'
    binary.write_bytes(raw)
    raw_sha = sha(raw)
    check(raw_sha == M1PLUS_PLAYER_SHA, f'Unknown hciplayer sha256: {raw_sha}')
    prof = PLAYER_PROFILE
    check(raw[fileoff(raw, prof['desc']):fileoff(raw, prof['desc'])+24].hex() ==
          prof['desc_bytes'], 'EQ descriptor mismatch')
    objects = compile_common(out, binary, True)
    script = out/'link.ld'
    script.write_text('SECTIONS { . = 0xe10000; .text : { *(.text*) } .rodata : { *(.rodata*) } '
                      '.data : { *(.data*) *(.sdata*) } .bss : { *(.bss*) *(.sbss*) } '
                      '__end = .; /DISCARD/ : { *(.comment) *(.note*) *(.pdr) *(.mdebug*) '
                      '*(.MIPS.abiflags) *(.reginfo) } }')
    run('ld.lld', '-m', 'elf32ltsmip', '--gc-sections', '-T', script, '-e', 'peq_open', '--undefined=mp3_seek', '--undefined=id3_gain',
        *objects, '-o', out/'peq.elf')
    run('llvm-objcopy', '-O', 'binary', out/'peq.elf', out/'peq.bin')
    ps = symbols(out/'peq.elf')
    payload = (out/'peq.bin').read_bytes()
    data = bytearray(raw)
    off = fileoff(raw, prof['open_slot'])
    data[off:off+4] = struct.pack('<I', ps['peq_open'])
    patch_word(data, prof['vbr_scan'], 0x144008a8, 0, 'VBR scan')  # bnez $v0, ... -> nop
    for address, stock, patched in prof['eq_rate_gates']:
        patch_word(data, address, stock, patched, 'Equalizer rate gate')
    patch_word(data, *prof['pause_sleep'], 'pause loop sleep')
    patch_word(data, prof['seek_slot'], prof['stock_seek'], ps['mp3_seek'], 'Audio demuxer seek slot')
    for address in prof['id3_calls']:
        patch_word(data, address, jal(prof['stock_id3']), jal(ps['id3_gain']), 'MP3 ReplayGain')
    append_payload(data, payload, PLAYER_BASE, max(len(payload), ps['__end']-PLAYER_BASE), 'player')
    (out/'hciplayer').write_bytes(data)
    return dict(stock_sha256=raw_sha, sha256=sha(data), payload_sha256=sha(payload))

def m1_themes():
    """The built-in themes the M1 offers, and tools/theme.py loaded over the M1's screen (m1plus_ipod's copy of
    tools/ipod.py, so its SET0 is the M1's rows and bar). Only the themes on SET0 alone: Classic boots its own
    geometry set, whose row immediates are V1.32's (ipod.json), so it is unported (docs/m1plus-unported.md)."""
    import importlib.util, sys, m1plus_ipod
    saved = sys.modules.get('ipod')
    sys.modules['ipod'] = m1plus_ipod.ipod
    try:
        spec = importlib.util.spec_from_file_location('m1plus_theme', ROOT/'tools/theme.py')
        theme = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(theme)
    finally:
        if saved is None: sys.modules.pop('ipod', None)
        else: sys.modules['ipod'] = saved
    themes = [t for t in theme.builtins() if theme.geometry(t) == theme.SET0 and not any(o.get('sets') for o in t['opts'])]
    check([t['name'] for t in themes] == ['Minimal', 'Modern'], f'M1 themes: {[t["name"] for t in themes]}')
    return themes, theme


def m1_emit_themes(themes, theme, out):
    """out/'themes.inc' for the M1: tools/theme.py's, with no boot sites. theme_boot rewrites ipod.json's immediates,
    V1.32 code addresses, where a set differs from SET0; the M1 has one set, so nothing may differ, and with no sites
    nothing is touched even if it did."""
    theme.emit(themes, out)
    inc = (out/'themes.inc').read_text()
    check(len(theme.geometry_sets(themes)) == 1, 'M1 themes: one geometry set')
    sites = re.search(r'^#define BOOT_SITES (\d+)$', inc, re.M)
    table = re.search(r'^const boot_site_t boot_sites\[BOOT_SITES\] = \{.*\};$', inc, re.M)
    check(sites and table, 'themes.inc: no boot sites table')
    inc = inc[:table.start()] + 'const boot_site_t boot_sites[1] = {{0, 0}}; /* M1 Plus: none (BOOT_SITES 0) */' + inc[table.end():]
    inc = inc.replace(sites.group(0), '#define BOOT_SITES 0 /* M1 Plus: theme_boot writes no V1.32 site */')
    # The own options of the themes the M1 leaves out (Classic's OWN_HOMELIB, OWN_ROWPREVIEW): past theme_keys, so
    # theme_own finds no option for them and reads 0
    m1_keys = list(theme.theme_keys(themes))
    for k in theme.theme_keys(theme.builtins()):
        if k not in m1_keys: inc += f'#define OWN_{k} (THEME_KEYS + {len(m1_keys)}) /* M1 Plus: its theme is unported */\n'
    (out/'themes.inc').write_text(inc)


def compile_payload(out):
    """Compile and link the payload."""
    extra = compile_common(out, out/'stock-demo')  # also writes the libc/libcstl imports navigation.c uses
    # -Wno-unused-function: the Q2 pages M1 replaces (ringnav_display) are out, and their iPod helpers (setting_click) with no caller
    flags = [*FLAGS, '-DM1PLUS=1', '-Wno-unused-function']
    run('clang',*flags,'-I',out,'-c',ROOT/'patch/navigation.c','-o',out/'navigation.o')
    asm = ['.set noreorder', '.text']
    active_hooks = M1PLUS_HOOKS
    gp = M1PLUS_GP
    resume = {x: address for address, _, x in M1PLUS_HOOKS.values() if x}
    for x, address in resume.items():
        asm += [f'.globl stock_{x}_trampoline', f'stock_{x}_trampoline:', f'lui $gp, {gp >> 16}',
                f'ori $gp, $gp, {gp & 65535}', f'j 0x{address + 12:x}', 'nop']
    # A Q2 hook V2.1 lacks has no stock code to resume, so its trampoline returns 0. Every Q2 hook's
    # gets one, so a new upstream hook's payload links on M1 before it is ported (M1PLUS_PORTS).
    from build import HOOKS
    for x in dict.fromkeys(x for _, _, x in HOOKS.values() if x):
        if x not in resume:
            asm += [f'.globl stock_{x}_trampoline', f'stock_{x}_trampoline:', 'jr $ra', 'move $v0, $zero']
    (out/'trampoline.S').write_text('\n'.join(asm)+'\n')
    run('clang',*flags,'-c',out/'trampoline.S','-o',out/'trampoline.o')
    leaf_paint = WM_PAINT_LEAF_M1PLUS
    undefined = [f'--undefined={name}' for _, name, _ in active_hooks.values()]
    undefined += [f'--undefined={leaf_paint[2]}', f'--undefined={GRADIENT_LEAF_M1PLUS[2]}', '--undefined=ringnav_audio_extension', '--undefined=ringnav_bootmode', '--undefined=playback_set',
                  '--undefined=ringnav_boot']
    # every call site's payload routine: a jal from stock code is no reference the linker sees
    undefined += [f'--undefined={new}' for words in CALL_SITES['m1plus'].values() for _, _, new in words if isinstance(new, str)]
    run('ld.lld','-m','elf32ltsmip','--gc-sections','-T',ROOT/'patch/link.ld','-e','ringnav',
        *undefined, out/'navigation.o',out/'trampoline.o',*extra,'-o',out/'patch.elf')
    run('llvm-objcopy','-O','binary',out/'patch.elf',out/'patch.bin')
    return symbols(out/'patch.elf')

def compile_helper(out, cat, src, name, rels):
    """Link patch/src (and start.c) as name against the stock rootfs's libraries rels."""
    libs = []
    for rel in rels:
        libs.append(out/rel.rsplit('/', 1)[-1])
        libs[-1].write_bytes(cat(rel))
    objs = [out/f'{s}.o' for s in (src, 'start')]
    cflags = [f for f in FLAGS if f not in ('-mno-abicalls', '-G0')] + ['-mnan=2008', '-mabs=2008', '-mabicalls', '-DM1PLUS=1']
    for o in objs:
        run('clang', *cflags, '-c', ROOT/'patch'/f'{o.stem}.c', '-o', o)
    run('ld.lld', '-m', 'elf32ltsmip', '-e', '__start', '--dynamic-linker', '/lib/ld-linux-mipsn8.so.1',
        '--image-base=0x400000', '-z', 'noexecstack', '--gc-sections', '-s', '--hash-style=sysv', '--build-id=none',
        *objs, *libs, '-o', out/name)
    return (out/name).read_bytes()

TAG_C_SHA = '2541a577c124d62221c15d68a92ca72d7395b43ead3ed9968aa78c0f28e21dce'

def patch_m4b_cover(raw):
    """Extend the pinned TagLib cover dispatcher with its existing MP4 extractor."""
    from ipod import branch
    check(sha(raw) == TAG_C_SHA, 'Unexpected TagLib cover library')
    image = bytearray(raw)
    base, site, mp4, next_format, gp = 0x30000, 0x1255c, 0x12688, 0x12564, 0x32770
    # Keep M4A's successful comparison, then compare M4B before the original MP4 check.
    # GP-relative data and PC-relative branches work at any shared-library load address.
    words = [branch(0x10400000, base, mp4), 0,
             0x8f998170, 0x02002025, 0x27850000 | ((base + 44 - gp) & 0xffff),
             0x0320f809, 0,
             branch(0x10400000, base + 28, mp4), 0x8fbc0010,
             branch(0x10000000, base + 36, next_format), 0]
    payload = struct.pack('<11I', *words) + b'm4b\0'
    append_payload(image, payload, base, len(payload), 'TagLib cover')
    struct.pack_into('<I', image, segments(image)[-1][0] + 24, 5)  # immutable code/data
    check(struct.unpack_from('<I', raw, fileoff(raw, site))[0] == 0x1040004a,
          'Unexpected TagLib M4A cover branch')
    struct.pack_into('<I', image, fileoff(raw, site), branch(0x10000000, site, base))
    return bytes(image)


def takes(path):
    """Whether path is an audited M1 Plus input (build.py's build() hands it here). Anything else, a
    missing file too, goes on to build.py's own checks, as upstream's tests expect."""
    return path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest() in INPUTS

def build(target_path, out, logo, dev=False, m1_release=None):
    """m1_release: an M1 Plus release's (name, tag), from tools/release_m1.py: the tag instead of
    the build's own, and the name in About and the manifest."""
    version = M1_TAG
    out.mkdir(parents=True, exist_ok=True)
    dev_count = 0
    if dev:  # the next number in the untracked .build-number
        counter = ROOT/'.build-number'
        dev = int(counter.read_text()) + 1 if counter.exists() else 1
        counter.write_text(f'{dev}\n')
        version = m1_dev_tag(dev)
        # About's "dev N" counts from 1 for each upstream VERSION; the tag keeps the global number, so
        # the updater, which refuses the installed tag, still takes each dev build over any other.
        per = ROOT/'work/dev-count'
        last = per.read_text().split() if per.exists() else []
        dev_count = int(last[1]) + 1 if last[:1] == [VERSION] else 1
        per.parent.mkdir(exist_ok=True)
        per.write_text(f'{VERSION} {dev_count}\n')
    source = source_sha256()
    raw = target_path.read_bytes()
    input_sha = sha(raw)
    check(input_sha in INPUTS, 'Unsupported input: SHA-256 differs from every audited original')
    member, archive_sha = INPUTS[input_sha]
    if member:
        with zipfile.ZipFile(io.BytesIO(raw)) as z:
            tarbytes = z.read(member)
    else:
        tarbytes = raw
    check(sha(tarbytes) == archive_sha, 'Unsupported update archive: SHA-256 differs from audited original')
    with tarfile.open(fileobj=io.BytesIO(tarbytes)) as t:
        meta = t.getmembers()
        check([m.name for m in meta] == ['firmware_v20.info','recovery-update',
              'recovery-update/xImage','recovery-update/rootfs.squashfs'], 'Unexpected package members')
        blobs = {m.name:t.extractfile(m).read() for m in meta if m.isfile()}
    info = blobs['firmware_v20.info'].decode().splitlines()
    check(info[0] == MODEL, f'Unsupported model: {info[0]}')
    model = MODEL
    stock_version = info[1]
    check(stock_version == 'V2.1', f'Unsupported M1 Plus version: {stock_version}')
    archive_name = 'update.bin'
    expected_logo = (320, 480)
    if m1_release:  # tools/release_m1.py's (name, tag)
        check(not dev and len(m1_release[1]) == 5, 'An M1 release is no dev build, and its tag is 5 characters')
        version = m1_release[1]
    pdr_off, pdr_size = PDR_M1PLUS
    check(not (out/archive_name).exists(), 'Output already exists; use a fresh --out directory')
    sq = out/'stock.squashfs'; sq.write_bytes(blobs['recovery-update/rootfs.squashfs'])
    def cat(path): return subprocess.check_output(['unsquashfs', '-cat', str(sq), path])
    raw_demo = cat('release/bin/demo')
    (out/'libc-2.28.so').write_bytes(cat('lib/libc-2.28.so'))
    # peq.h tls_untimed writes OpenSSL 1.1.1f's SSL_CTX->param (0x100) and its ->flags (0xc) itself, as
    # build.py audits on the Q2: V2.1's rootfs has the same 1.1.1f, and these must still read those fields.
    for lib, fn, at, word in (('libssl.so.1.1', 'SSL_CTX_get0_param', 4, 0x8c820100),         # lw v0, 0x100(a0)
                              ('libcrypto.so.1.1', 'X509_VERIFY_PARAM_set_flags', 0, 0x8c86000c)):  # lw a2, 0xc(a0)
        data = cat('usr/lib/'+lib); (out/lib).write_bytes(data)
        address = symbols(out/lib)[fn+'@@OPENSSL_1_1_0']
        check(struct.unpack_from('<I', data, address + at)[0] == word, f'{lib}: {fn} layout changed')
    from ipod import imagemagick, patch_word, sized_art
    import m1plus_ipod
    m1plus_names(sq, out)  # every V2.1 name the payload uses is in V2.1's rootfs
    demo = out/'stock-demo'; demo.write_bytes(raw_demo)
    symbol_table = run('readelf', '-Ws', demo)
    syms = symbols(demo, symbol_table)
    header = [f'#define RING_STEP {RING_STEP}']
    # Classic's bold font (4.1) comes with the iPod assets: no range, so bold_label never picks it
    header.append('#define BOLD_RANGES {0, 0}')
    header.append('#define CLASSIC_LIGHT_RANGES {0, 0}')  # Classic's face (1.6.7): Classic is unported
    # navigation.c's ringnav_timezone and ringnav_timezone_row name them; their hooks, select_timezone and
    # timezone_row, are unported (M1PLUS_PORTS)
    header.append('#define TIMEZONE_NAMES {' + ','.join(json.dumps(zone) for _, zone in TIMEZONES) + '}')
    header.append('#define TIMEZONE_ORDER {' + ','.join(map(str, TIMEZONE_ORDER)) + '}')
    header.append('#define TIMEZONE_CITIES {' + ','.join(json.dumps(label.split(' ', 1)[1]) for label, _ in TIMEZONES) + '}')
    syms, stubs = m1plus_symbols(syms, symbol_table)
    stubbed = dict(stubs)
    for name in [*CONTEXT_DATA, *M1PLUS_CONTEXT_DATA]:
        if name in stubbed:
            header += [f'extern unsigned char {M1PLUS_STUB}{name}[{stubbed[name]}];',
                       f'#define {name} ((const unsigned char *){M1PLUS_STUB}{name})']
        else:
            header.append(f'#define {name} ((const unsigned char *)0x{syms[name]:x}u)')
    # iPod's image hook leaves the settings icons' category colours alone (navigation.c settings_icon): V2.1's own
    # (m1plus_ipod.json's settings_icons, ipod-ui 4.3), which its settings rows and the payload's draw.
    names = ''.join(n.removesuffix('.png') + '\\0' for n in m1plus_ipod.AUDIT['settings_icons'])
    header.append(f'#define SETTINGS_ICON_NAMES "{names}"')
    header.append(f'#define ROCKBOX_FLAG "{ROCKBOX_FLAG}"')  # Home's Rockbox row, for S90play
    # About: the stock firmware's version on its own row, and this build's on the CFW. Version row.
    release = m1_release[0] if m1_release else VERSION
    header += [f'#define STOCK_VERSION "{stock_version}"', f'#define Q2POD_VERSION "{release}{f" dev {dev_count}" if dev else ""}"',
               f'#define Q2POD_TAG "{"" if dev else release}"',  # netupdate.c (unported on M1): the release tag, none when --dev
               f'#define Q2POD_DEV {1 if dev else 0}',  # navigation.c stale_note (Q2 only: stale_heal is unported)
               '#define Q2POD_REPO "jtliang24/q2-pod"',  # netupdate.c (unported on M1): the repo of its releases
               f'#define Q2POD_UA "Q2Pod/{release} (https://github.com/jtliang24/q2-pod)"']  # onlinematch.c, as MusicBrainz asks
    themes, theme = m1_themes()
    header.append(f'#define THEME_N {len(themes)}')  # navigation.c setting_counts[]
    header.append(f'#define THEME_KEYS {len(theme.theme_keys(themes))}')  # navigation.c st.own[], themes.inc theme_keys[]
    (out/'stock.h').write_text('\n'.join(header)+'\n')
    m1_emit_themes(themes, theme, out)
    ps = compile_payload(out)
    payload = (out/'patch.bin').read_bytes()
    check(len(payload) < SCRATCH-BASE, 'Payload overlaps its scratch page')
    check(ps['__scratch_start'] == SCRATCH, 'Scratch state moved')
    # Map to the ELF's end, not __scratch_end: up to 1.3.8 link.ld placed only .scratch, and a static
    # outside it (coverflow.c's stock_rows, 1.3.8's headroom cache in peq.c) was an orphan .bss after it,
    # which put 1.3.8's on the heap's first page on M1. 1.3.9's link.ld takes .bss into .scratch, so the
    # two now agree; the ELF's end stays the bound if a section lands past it again.
    payload_end = max(v + m for _, (t, _, v, _, _, m, _, _) in segments((out/'patch.elf').read_bytes()) if t == 1)
    check(ps['__scratch_end'] <= payload_end <= SCRATCH + 0x20000, 'Scratch state exceeds its 128 KB')
    patched = bytearray(raw_demo)
    def jump(off, name): patched[off:off+8] = struct.pack('<II', 0x08000000 | (ps[name] >> 2), 0)
    for name, (address, replacement, _) in M1PLUS_HOOKS.items():
        check(syms[name] == address, f'{name}: callback address mismatch')
        check(pic_gp(patched, address) == M1PLUS_GP, f'{name}: unexpected PIC prologue or GOT base')
        jump(fileoff(patched, address), replacement)
    for name, address, replacement, words in [WM_PAINT_LEAF_M1PLUS, GRADIENT_LEAF_M1PLUS]:
        off = fileoff(patched, address)
        check(syms[name] == address and struct.unpack_from('<III', patched, off) == words, f'{name}: unexpected code')
        jump(off, replacement)
    # style_get_color's own bal style_get_gradient, returning to STYLE_COLOR_GRADIENT_RET, stays unmapped.
    from ipod import branch
    ret = m1plus_inc('STYLE_COLOR_GRADIENT_RET')
    check(struct.unpack_from('<I', patched, fileoff(patched, ret - 8))[0] ==
          branch(0x04110000, ret - 8, GRADIENT_LEAF_M1PLUS[1]), 'style_get_color: unexpected gradient call')
    for name, address in M1PLUS_PRIVATE_FUNCTIONS.items():
        check(pic_gp(raw_demo, address) == M1PLUS_GP, f'{name}: not a V2.1 PIC entry')
    # ringnav_speed and ringnav_mode tell config_mplayer's re-applying calls, and config_init's
    # boot one, from a choice by their return addresses: each a jalr $t9 after lw $t9, <callee's
    # GOT slot>($gp).
    for ret, callee in (('INITCONFIG_SPEED_RET', 'mclSetPlaySpeed'), ('INITCONFIG_MODE_RET', 'mclSetPlayMode'),
                        ('BOOT_MODE_RET', 'mclSetPlayMode')):
        ret = m1plus_inc(ret)
        words = struct.unpack_from('<5I', raw_demo, fileoff(raw_demo, ret - 24))
        load = next((w for w in reversed(words[:4]) if w >> 16 == 0x8f99), 0)
        slot = M1PLUS_GP + (load & 0xffff) - (0x10000 if load & 0x8000 else 0)
        check(load and words[4] == 0x0320f809 and
              struct.unpack_from('<I', raw_demo, fileoff(raw_demo, slot))[0] == syms[callee],
              f'config_mplayer: unexpected {callee} call')
    raw_player = cat('usr/bin/hciplayer')
    audio = patch_player(raw_player, out/'peq')
    check(sha(cat(BLUEALSA)) == BLUEALSA_SHA, 'Unexpected bluealsa')
    bluealsa = patch_bluealsa(cat(BLUEALSA))
    (out/'bluealsa').write_bytes(bluealsa)
    # A2DP's transport stays open 5 s between songs (1.3.8): V2.1's bluealsa2 starts the Q2's bluealsa
    bluealsa2 = cat(BLUEALSA2)
    check(bluealsa2.count(BT_KEEPALIVE[0]) == 1, 'Unexpected bluealsa2')
    (out/'bluealsa2').write_bytes(bluealsa2.replace(*BT_KEEPALIVE))
    (out/'watchdog').write_bytes(cat(WATCHDOG).replace(*WATCHDOG_SLEEP))
    for name, address, old, new in call_site_words(True, ps):
        patch_word(patched, address, old, new, CALL_SITE_PURPOSES[name])
    # The iPod UI's private entries and the event ids its code reads (m1plus_ipod.json), as V2.1 has them.
    for name, original in m1plus_ipod.AUDIT['private_prologues'].items():
        check(M1PLUS_PRIVATE_FUNCTIONS[name] == syms[name] and
              raw_demo[fileoff(raw_demo, syms[name]):][:12].hex() == original, f'{name}: unexpected stock entry')
    for address, original in m1plus_ipod.AUDIT['event_abi_words'].items():
        check(raw_demo[fileoff(raw_demo, int(address, 16)):][:4].hex() == original, f'{address}: unexpected event ABI instruction')
    compact_code = m1plus_ipod.patch_code(patched, ps)  # the iPod UI's audited code edits
    # Single shared version literal: V2.1's updater refuses an equal firmware_v20.info version (update_firmware,
    # 0x4e0e34; docs/m1plus.md), so it carries the build tag and stock V2.1 can be flashed back. About's FW.
    # Version row reads it too; ringnav_about shows STOCK_VERSION there instead.
    check(patched.count(b'V2.1\0') == 1, 'Version literal is not unique')
    off = patched.find(b'V2.1\0')
    patched[off:off+len(version)+1] = version.encode() + b'\0'
    for rtc in [RTC_WRITE, RTC_READ_M1PLUS, WIFI_LPS]:
        check(patched.count(rtc[0]) == 1, f'Unexpected RTC command {rtc[0]!r}')
        patched = patched.replace(*rtc)
    check(patched.count(LOCK_CLOCK_12H[0]) == 1, 'Unexpected lock clock formats')
    patched = patched.replace(*LOCK_CLOCK_12H)
    check(re.search(r'\.pdr +PROGBITS +0+ +0*%x +0*%x ' % (pdr_off, pdr_size), run('readelf', '-SW', demo)) and
          all(p[1]+p[4] <= pdr_off for _,p in segments(patched) if p[0] == 1), '.pdr: not the audited section')
    patched[pdr_off:pdr_off+pdr_size] = bytes(pdr_size)
    append_payload(patched, payload, BASE, payload_end-BASE, 'demo')
    (out/'demo').write_bytes(patched)
    # Pseudo-file round trip preserves every original inode's metadata and hardlinks.
    pseudo = out/'root.pseudo'
    run('unsquashfs','-pf',pseudo,sq)
    p = pseudo.read_bytes()
    # mksquashfs takes "/" from the source dir, not the pseudo file; carry stock values over.
    root = re.search(rb'^/ D (\d+) (\d+) (\d+) (\d+)$',p,re.M)
    check(root is not None, 'Missing root pseudo inode')
    t,mode,uid,gid = (x.decode() for x in root.groups())
    rootargs = ['-root-time',t,'-root-mode',mode,'-root-uid',uid,'-root-gid',gid]
    # Paths are passed through a shell by mksquashfs F entries; quote them explicitly.
    def inode(p, path): return re.search(rb'^'+re.escape(path)+rb' R (\d+) (\d+) (\d+) (\d+) .+$',p,re.M)
    def swap_inode(p, path, src):
        line = inode(p, path)
        check(line is not None, f'Missing {path.decode()} pseudo inode')
        return p[:line.start()]+path+b' F '+b' '.join(line.groups())+b' cat '+shlex.quote(str(src)).encode()+p[line.end():]
    s90play = cat(S90PLAY)
    check(s90play.count(BOOT_HOOK[0]) == 1 and s90play.count(REMOTE_HOOK[0]) == 1, 'Unexpected S90play')
    s90play = s90play.replace(*BOOT_HOOK)
    (out/'S90play').write_bytes(s90play.replace(*REMOTE_HOOK) if dev else s90play)
    s11logo = cat(S11LOGO)
    check(s11logo.count(LOGO_HOOK[0]) == 1, 'Unexpected S11logo_display_shell')
    (out/'S11logo').write_bytes(s11logo.replace(*LOGO_HOOK))
    # assets/boot-logo.jpg is 320x375: an M1 Plus build without --logo keeps V2.1's own splash.
    logo_source = 'stock' if logo == ROOT/'assets/boot-logo.jpg' else 'custom'
    if logo_source == 'stock':
        logo_data = cat('release/assets/default/raw/images/xx/logo.jpg')
    else:
        logo_data = logo.read_bytes()
    check(jpeg_size(logo_data) == expected_logo, f'Logo must be {expected_logo[0]}x{expected_logo[1]} like the stock splash')
    # Package exactly the validated bytes, even if the input is edited during compression.
    logo_target = out/'logo.jpg'
    logo_target.write_bytes(logo_data)
    for path, src in ((b'release/bin/demo', out/'demo'), (b'usr/bin/hciplayer', out/'peq/hciplayer'),
                      (BLUEALSA.encode(), out/'bluealsa'), (BLUEALSA2.encode(), out/'bluealsa2'),
                      (WATCHDOG.encode(), out/'watchdog'), (S90PLAY.encode(), out/'S90play'), (S11LOGO.encode(), out/'S11logo'),
                      (b'release/assets/default/raw/images/xx/logo.jpg', logo_target)):
        p = swap_inode(p, path, src)
    # New inodes, each with its stock image's metadata, as build.py adds them: the Coverflow icons, the Library's
    # and Streaming's rows' icons (drawn in assets/icons/, or a copy of the V2.1 image named), Home's card art, arrows
    # and placeholder, and the helpers.
    xx = 'release/assets/default/raw/images/xx/'
    mapping = dict(
        shuffle='pset_playmode.png', scrobble='drop_wifi.png', podcasts='dlna.png',
        audiobooks='playset_foldercover.png', photos='pset_covermode.png', books='system_language.png',
        videos='sset_display.png', longsongs='system_time.png', era='genre.png')
    icons = {n: ('system_language.png', (ROOT/'assets/icons'/n).read_bytes()) for n in ICONS}
    drawn = ('podcasts', 'audiobooks', 'books', 'videos')
    icons.update({f'local_{n}.png': (like, (ROOT/'assets/icons'/f'local_{n}.png').read_bytes() if n in drawn
                                     else cat(xx+like)) for n, like in mapping.items()})
    for n in ('spotify', 'radio'):  # Streaming's Spotify and Internet Radio rows
        icons[f'stream_{n}.png'] = ('tidal.png', (ROOT/'assets/icons'/f'stream_{n}.png').read_bytes())
        # the Q2 Pod page's rows at V2.1's 40 px (list_row_core); the radio's Now Playing art keeps stream_radio's 52
        icons[f'row_{n}.png'] = ('tidal.png', sized_art((ROOT/'assets/icons'/f'stream_{n}.png').read_bytes(), 40))
    # V2.1's rows draw a 40 px icon (list_row_core) where V1.32's drew 52: the drawn ones at its size.
    for n in drawn:
        like, data = icons[f'local_{n}.png']
        icons[f'local_{n}.png'] = (like, sized_art(data, 40))
    # V1.32's Local Music icons Ratings and Most Played name, which V2.1 lacks: its Favourites and
    # Frequent cards' art at the rows' size.
    icons['local_era.png'] = ('pset_playmode.png', sized_art(cat(xx+'genre.png'), 40))
    icons['local_fav.png'] = ('pset_playmode.png', sized_art(cat(xx+'fav.png'), 40))
    icons['local_frequentplay.png'] = ('pset_playmode.png', sized_art(cat(xx+'many.png'), 40))
    # The iPod Home (ipod-ui 4.5): each Carousel card's art, its role's V2.1 Home card art at 190 px, pressed too, and the
    # Shortcut card's own; the carousel's arrows; Split's placeholder at the panel's width (coverflow.c HOME_PLACEHOLDER).
    for row, art in m1plus_ipod.HOME_CARD_ART.items():
        for s in ('', '_down'):
            icons[f'home_card_{row}{s}.png'] = (f'{art}{s}.png', sized_art(cat(f'{xx}{art}{s}.png'), m1plus_ipod.CARD_ART))
    for s in ('', '_down'):
        icons[f'home_card_rockbox{s}.png'] = (f'fav{s}.png', m1plus_ipod.home_card_shortcut(down=bool(s)))
    for n in ('home_left', 'home_right'):
        icons[f'{n}.png'] = ('arrow_left_n.png', m1plus_ipod.home_arrow(n))
    icons['default_album_home.png'] = ('defaultcover.png', sized_art((ROOT/'assets/icons/default_album_home.png').read_bytes(),
                                                                      m1plus_ipod.ipod.UI_W))
    icons['row_stream_config.png'] = ('pset_playmode.png', sized_art(cat(xx+'sset_netservice.png'), 40))
    icons['bar_back.png'] = ('bar_play.png', m1plus_ipod.back_chevron())  # the status bar's back chevron (ipod-ui 4.2)
    icons['stream_airplay.png'] = ('airplay.png', cat(xx+'airplay.png'))
    # the card apps' rows on the Q2 Pod page (addon.c), at V2.1's 40 px as row_spotify
    icons['stream_app.png'] = ('tidal.png', sized_art((ROOT/'assets/icons/stream_app.png').read_bytes(), 40))
    added = []
    ui = 'release/assets/default/raw/ui/'
    helper_items = {
        ui+m1plus_ipod.PLAYING_STOCK: (ui+m1plus_ipod.PLAYING_PAGE, m1plus_ipod.playing_stock(cat(ui+m1plus_ipod.PLAYING_PAGE))),  # Centred Now Playing (ipod-ui 4.6)
        HELPER: (HELPER_LIKE, compile_helper(out, cat, 'video', 'q2video', HELPER_LIBS)),
        SCROBBLE_CA: ('etc/hosts', (ROOT/'assets/scrobble-ca.pem').read_bytes()),
        BOOT: (HELPER_LIKE, compile_helper(out, cat, 'boot', 'q2boot', HELPER_LIBS[:1])),
        **({REMOTE: (HELPER_LIKE, compile_helper(out, cat, 'remote', 'q2remote', HELPER_LIBS[:1]))} if dev else {})
    }
    for path, (like, data) in {**{xx+n: (xx+l, d) for n, (l, d) in icons.items()}, **helper_items}.items():
        stock = inode(p, like.encode())
        check(stock is not None, f'Missing stock inode for {path}')
        name = path.rsplit('/', 1)[-1]
        if path not in (HELPER, BOOT, REMOTE): (out/name).write_bytes(data)  # package the hashed bytes, as the logo
        path = path.encode()
        entry = path+b' F '+b' '.join(stock.groups())+b' cat '+shlex.quote(str(out/name)).encode()+b'\n'
        at = p.index(b'# START OF DATA')  # definitions precede the embedded data
        p = p[:at]+entry+p[at:]
        added.append([path, b'R', *stock.groups()])
    removed = []
    to_remove = STOCK_EQ + OBSOLETE
    for path in to_remove:
        line = re.search(rb'^'+re.escape(path.encode())+rb' R .+\n', p, re.M)
        if line is None and path in STOCK_EQ:
            continue
        check(line is not None, f'Missing stock inode {path}')
        removed.append(line.group().split()[:6])
        p = p[:line.start()]+p[line.end():]
    changed_assets = {}
    patch_list = [(TAG_C, patch_m4b_cover, 'libtag_c.so.2.0.1')]
    for path, fix, name in patch_list:
        original = cat(path)
        data = fix(original)
        (out/name).write_bytes(data)
        p = swap_inode(p, path.encode(), out/name)
        changed_assets[path] = dict(original_sha256=sha(original), sha256=sha(data))
    # The iPod UI's pages (docs/m1plus-ipod-ui.md Phase 3): only a page a rewrite changed is swapped in.
    for rel in m1plus_ipod.UI_ASSETS:
        path = 'release/assets/default/raw/ui/' + rel
        original = cat(path)
        data = m1plus_ipod.patch_asset(rel, original)
        if data == original:
            continue
        target = out/'ui'/rel; target.parent.mkdir(parents=True, exist_ok=True); target.write_bytes(data)
        p = swap_inode(p, path.encode(), target)
        changed_assets[path] = dict(original_sha256=sha(original), sha256=sha(data))
    # ... and its styles (4.1): the rows the selection bar shows through, and the press greys.
    for rel in m1plus_ipod.AUDIT['styles']:
        path = 'release/assets/default/raw/styles/' + rel
        original = cat(path)
        data = m1plus_ipod.patch_style(rel, original)
        check(data != original, f'{path}: the audited edits changed nothing')
        target = out/'styles'/rel; target.parent.mkdir(parents=True, exist_ok=True); target.write_bytes(data)
        p = swap_inode(p, path.encode(), target)
        changed_assets[path] = dict(original_sha256=sha(original), sha256=sha(data))
    # ... and its status bar's images (4.2): V2.1's play state, Bluetooth and Wi-Fi glyphs as the iPod's slim ones.
    for n in m1plus_ipod.AUDIT['status_icons']:
        path = 'release/assets/default/raw/images/xx/' + n
        original = cat(path)
        data = m1plus_ipod.status_icon(n, original)
        target = out/'status'/n; target.parent.mkdir(parents=True, exist_ok=True); target.write_bytes(data)
        p = swap_inode(p, path.encode(), target)
        changed_assets[path] = dict(original_sha256=sha(original), sha256=sha(data))
    # ... and Now Playing's controls (4.6): V2.1's heart, play mode, More and queue glyphs as the iPod's quiet ones.
    for n in m1plus_ipod.AUDIT['quiet_icons']:
        path = 'release/assets/default/raw/images/xx/' + n
        original = cat(path)
        data = m1plus_ipod.quiet_icon(n, original)
        target = out/'quiet'/n; target.parent.mkdir(parents=True, exist_ok=True); target.write_bytes(data)
        p = swap_inode(p, path.encode(), target)
        changed_assets[path] = dict(original_sha256=sha(original), sha256=sha(data))
    pseudo.write_bytes(p)
    (out/'empty').mkdir(exist_ok=True)
    newsq = out/'rootfs.squashfs'
    epoch = struct.unpack_from('<I',sq.read_bytes(),8)[0]
    run('mksquashfs',out/'empty',newsq,'-pf',pseudo,'-noappend','-comp','lzo',
        '-b','131072','-Xcompression-level','9','-tailends','-mkfs-time',epoch,*rootargs,'-processors','1','-no-progress')
    # All inodes, including demo and the logo, keep name/type/mtime/mode/uid/gid (sizes/offsets shift).
    def inodes(image):
        text = subprocess.check_output(['unsquashfs','-pf','-',str(image)]).split(b'\n# START OF DATA')[0]
        return sorted(l.split()[:6] for l in text.splitlines() if l and not l.startswith(b'#'))
    check(inodes(newsq) == sorted([i for i in inodes(sq) if i not in removed]+added),
          'Repacked rootfs metadata differs from stock')
    blobs['recovery-update/rootfs.squashfs'] = newsq.read_bytes()
    # Stock image proves this size fits; do not enlarge beyond its padded size.
    check(len(blobs['recovery-update/rootfs.squashfs']) <= sq.stat().st_size, 'Repacked rootfs exceeds stock size')
    blobs['firmware_v20.info'] = (f'{model}\n{version}\n'+''.join(
        hashlib.md5(blobs[n]).hexdigest()+'  '+n+'\n' for n in [
            'recovery-update/xImage','recovery-update/rootfs.squashfs'])).encode()
    out_archive = out/archive_name
    with tarfile.open(out_archive,'w',format=tarfile.GNU_FORMAT) as t:
        for m in meta:
            data = blobs.get(m.name)
            if data is not None: m.size=len(data)
            t.addfile(m,io.BytesIO(data) if data is not None else None)
    manifest = dict(model=model, input_sha256=input_sha, stock_demo_sha256=M1PLUS_DEMO_SHA,
        source_sha256=source, demo_sha256=sha(patched), patch_sha256=sha(payload),
        update_sha256=sha(out_archive.read_bytes()), rootfs_sha256=sha(newsq.read_bytes()),
        kernel_sha256=sha(blobs['recovery-update/xImage']), patch_bytes=len(payload), ring_step_pixels=RING_STEP,
        audio_extension_calls=[dict(address=hex(a), original=f'{o:#010x}', replacement=hex(n)) for name, a, o, n in call_site_words(True, ps) if name == 'AUDIO_EXTENSION_CALLS' and n != o],
        version=version, **({'release': m1_release[0]} if m1_release else {}), dev=dev, **({'dev_count': dev_count} if dev else {}), peq=audio, bluealsa_sha256=sha(bluealsa), q2video_sha256=sha((out/'q2video').read_bytes()), q2boot_sha256=sha((out/'q2boot').read_bytes()), **({'q2remote_sha256': sha((out/'q2remote').read_bytes())} if dev else {}), compact_code=compact_code, changed_assets=changed_assets, logo_sha256=sha(logo_data), logo_source=logo_source,
        patch_symbols={n:hex(v) for n,v in ps.items() if n.startswith('stock_')},
        tools={t:run(t,'--version').splitlines()[0] for t in ['clang','ld.lld','llvm-objcopy']} |
              {'imagemagick': imagemagick('-version', data=b'').decode().splitlines()[0]})
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps({k:manifest[k] for k in ['update_sha256','patch_bytes','version']},indent=2))
