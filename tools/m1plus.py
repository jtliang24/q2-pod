#!/usr/bin/env python3
"""The M1 Plus target: its V2.1 tables and its own build pipeline, beside upstream's tools/build.py.

build.py keeps upstream's Q2 code; its build() hands an M1 Plus input to build() here
(docs/m1plus-roadmap.md U1). The pipeline reuses build.py's helpers and tables where V2.1 matches V1.32,
and every V2.1 address here was found in V2.1's own code."""
import hashlib, io, json, re, shlex, struct, subprocess, tarfile, zipfile
from build import (ROOT, EXTRA_TIMEZONES, VERSION, VERSIONS, BASE, SCRATCH, RING_STEP, FLAGS, FUNCTIONS, GLOBALS, CONTEXT_DATA, HELPER,
                   HELPER_LIKE, HELPER_LIBS, BOOT, REMOTE, S90PLAY, ROCKBOX_FLAG, BOOT_HOOK, S11LOGO, LOGO_HOOK,
                   REMOTE_HOOK, BLUEALSA, BLUEALSA2, BT_KEEPALIVE, SCROBBLE_CA, WATCHDOG, WATCHDOG_SLEEP, RTC_WRITE, LOCK_CLOCK_12H, ICONS,
                   STOCK_EQ, OBSOLETE, TAG_C, append_payload, check, dev_tag, fileoff, jpeg_size, patch_bluealsa,
                   run, segments, sha, source_sha256, symbols)

MODEL = 'Shanling M1 Plus'
M1PLUS_BIN_SHA = '1ccb4667e3e9bdf9a35be4dc58d09b898ca53c5fd58396b7667fb91fe895f925'
M1PLUS_ZIP_SHA = 'db7bdbc42ffe6d5c1e3fdca9363edb78a01898b9a725c34793394cf6abfa33c0'
M1PLUS_DEMO_SHA = '29e23119bc2a0f153f3ea0ba942a39754d1aab0879c1040fae2269df8bd9b3f1'
M1PLUS_GP = 0xa03ed0
INPUTS = {M1PLUS_ZIP_SHA: ('M1 Plus Firmware V2.1/update.bin', M1PLUS_BIN_SHA), M1PLUS_BIN_SHA: (None, M1PLUS_BIN_SHA)}
# Stock routines only the M1 Plus payload calls, beside build.py's FUNCTIONS (compile_common merges them).
M1PLUS_FUNCTIONS = {
 'view_create': ('void *', 'void *, int, int, int, int'),  # the Home card's page and card views
 'label_set_line_wrap': ('int', 'void *, int'),
 'slide_indicator_set_max': ('int', 'void *, unsigned'),
 # (widget, index, animate): Knob: Navigation slides Home to the focused card's page (m1plus_nav_home.c)
 'slide_view_set_active_ex': ('int', 'void *, unsigned, int'),
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
}
WM_PAINT_LEAF_M1PLUS = ('window_manager_paint', 0x677b44, 'ringnav_wm_paint', (0x10800009, 0, 0x8c820088))
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
        # parse_albumcovertask_thd's jalr toolsGetAlbumCover calls: Ogg pictures through ffmpeg.
        'GRID_COVER': ((0x4edf1c, 0x0320f809, 'coverflow_album_cover'), (0x4ef018, 0x0320f809, 'coverflow_grid_cover'),
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
    },
    # V2.1's routines are V1.32's, moved: each site is its Q2 counterpart's word in V2.1's copy.
    'm1plus': {
        # mclNextSong's bal to the shuffle pick (0x5d03b0).
        'SHUFFLE_CALL': ((0x5d5a28, 0x0411ea61, 'ringnav_shuffle'),),
        # check_cpumem's "open failed, skip the write" beq: 1.2.2's form. Upstream 1.2.9 returns from the
        # Q2's thread at once instead (roadmap U3's batch).
        'DROP_CACHES': ((0x50b868, 0x12220006, 0x10000006),),
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
        # before its toolsGetExternCover, then Folder view's two (40 px).
        'GRID_COVER': ((0x4dd6a8, 0x0320f809, 'coverflow_album_cover'), (0x4de8a4, 0x0320f809, 'coverflow_grid_cover'),
                       (0x4de960, 0x0320f809, 'coverflow_grid_cover')),
        # parseplaycover_thd's toolsGetExternCover after a local track's embedded art failed (0x4df1e8),
        # under parse_cover_mutex: m1plus_player_cover drops it for ffmpeg (patch/m1plus_player_cover.c).
        'PLAYER_COVER': ((0x4df218, 0x8f99b880, None), (0x4df228, 0x0320f809, 'm1plus_player_cover')),
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
# a roadmap U4 row. IPOD_HOOKS are Q2 only as a group (roadmap section 5). A sync adds a row for each
# new upstream hook or site it doesn't port, and the report fails until it has one.
M1PLUS_PORTS = {
    # Hooks
    'on_wm_keydown_before_fun': ('q2only', "Key Tone's click on the wheel's press; V2.1 has no buzzer command (progress 15)"),
    'buzzeer_switch': ('q2only', 'Key Tone; V2.1 has no buzzer command (progress 15)'),
    'localmusic_page_init': ('ported', "the Library's rows are the Q2 Pod page's Library page (progress 17)"),
    'load_localartist_list': ('ported', "V2.1 has no such function: an artist's albums are loadLocalClassList(0xff01), "
                              'hooked as ringnav_localclass (progress 12)'),
    'screensaver_rows': ('ported', "V2.1 has no rows hook: the Lock screen page's rows are lockscreen_page's (progress 28)"),
    'stream_page_init': ('ported', 'V2.1 has no Streaming page: Spotify, Internet Radio and AirPlay are Q2 Pod page rows '
                         '(progress 22)'),
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
    'localmusic_playlistsmore_page_init': ('unported', "a playlist's More page: editing, song search, a row hold "
                                           "(1.3.8); V2.1 has no playlistsmore_page"),
    'systemset_fwupdate_page_init': ('unported', "Network Update (1.3.8) fetches DiamondBond's Q2 update.tar; off "
                                     "until it points at the M1 releases. fwupdate_tf is M1PLUS_UNRESOLVED"),
    'usbmode_page_init': ('unported', "card apps end before USB storage unmounts the card (1.4.2); the card app "
                          'host (addon.c) waits for U4, with Apps'),
    # Call sites
    'ARTIST_ALBUMS': ('native', "V2.1's artist page lists the artist's albums (roadmap 4)"),
    'BOOT_MODE_CALL': ('native', 'V2.1 saves ARTISTTYPE and reads it in config_init (roadmap 4)'),
    'CLASS_ICON': ('native', 'V2.1 draws its own artist icon (roadmap 4)'),
    'ARTIST_COVER_ROW': ('native', "V2.1 has no artist page of 160 px rows: an artist's albums are an album list, "
                         'whose covers COVER_PAUSE and ALBUM_ART cover (progress 12, 30)'),
    'HOLD_RETURN': ('q2only', 'long Return; the M1 has no Return key'),
    'STANDBY_WAKE': ('q2only', "Standby resume staying dark goes with the Q2's Centre-key Wake; V2.1 has Double wake"),
    'WHEEL_TS_READ': ('q2only', 'the touch wheel'),
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
}
# V2.1 globals V1.32 lacks, read as GLOBALS are. Bluetooth keeps its own level, [PLAYSET] BTVOLUME:
# the volume dialog (on_volume_tsup_fun), status bar and set_devicevolume use it while headset_output
# is 2, and `volume` stays the jacks'. on_wm_keyup_fun swaps Previous and Next, and the volume keys,
# while rotate_mode is 1 (the rotated screen, 0x4cd9f8).
M1PLUS_GLOBALS = ['g_btvolume', 'g_rotate_mode']
# V2.1 data V1.32 lacks, read as CONTEXT_DATA is (sizes checked). pdeq_choicemenu: the Home menu's
# chosen cards, a deque of ids that home_page_init's grid builder (0x534064) lays out six to a page.
M1PLUS_CONTEXT_DATA = {'pdeq_choicemenu': 4}
# Renamed in V2.1; each has the size of its V1.32 counterpart (checked in m1plus_symbols).
M1PLUS_CONTEXT_ALIASES = {
    'g_folder_path': 'folder_path',
    'g_dacoff_time': 'dacoff_time',
    'g_power_capacity': 'power_capacity',
    'g_screensaver_picture': 'screensaver_picture',
    'g_memory_info': 'meminfo_save',
    'g_class_type': 'cur_classtype',
    'g_local_classinfo_save': 'classinfo_save',
    'p_deque_showlist': 'pdeq_showlist',
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
}
# V1.32 routines V2.1 has no twin of yet, called only from a Q2 hook the M1 leaves unported: declared
# with no address, so the page compiles and --gc-sections drops it. The link fails if live code
# reaches one. Each goes with its hook's U4 row.
M1PLUS_UNRESOLVED = {
    'fwupdate_tf': 'Network Update (netupdate.c): stock\'s TF card update, systemset_fwupdate_page_init unported',
}
M1PLUS_FUNCTION_ALIASES = {
    'device_set_volume': 'set_devicevolume',
    'config_outputchannel': 'set_outputchannel',
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
    # The batch record (pvec_selectrecord): n rows unselected, then one row's selection toggled
    'batch_init_selectrecord': 'select_recordinit',
    'batch_set_selectitem': 'set_selectindex',
    # delete_playqueue_file calls it where V1.32's calls player_start_queue (0x4e4a80): the queue row's play
    'player_start_queue': 'start_playqueue',
    # folder_back calls it where V1.32's calls folder_reset_variable (0x4dbf0c): a fresh Folder visit.
    # V2.1's clears one enter-history deque where V1.32's clears two, and its flags are words.
    'folder_reset_variable': 'clear_foldervariate',
}
M1PLUS_HOOKS = {
    'widget_on_paint_border': (0x668810, 'ringnav_paint', 'paint'),
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
    'kugou_obtainlyric': (0x509ee4, 'ringnav_lyric_search', 'kugou'),
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
    'eq_rate_gates': ((0x42ce34, 0x10400098, 0),
                      (0x42e6fc, 0x10400015, 0)),
    'seek_slot': 0x89f76c,
    'stock_seek': 0x48cc6c,
    'id3_calls': (0x48ee74, 0x492028, 0x492ab4),
    'stock_id3': 0x48b760,
    'written_audio_pts': 0x4300f4,
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
        from build import HOOKS, IPOD_HOOKS
        resumed = {n: x for n, (_, _, x) in M1PLUS_HOOKS.items() if x and n not in HOOKS | IPOD_HOOKS}
        for name, (ret, args) in (FUNCTIONS | M1PLUS_FUNCTIONS).items():
            if name in resumed:
                header += [f'extern {ret} stock_{resumed[name]}_trampoline({args});',
                           f'#define {name} stock_{resumed[name]}_trampoline']
            elif name in syms and syms[name]:
                header.append(f'#define {name} (({ret} (*)({args}))0x{syms[name]:x}u)')
            elif name in M1PLUS_UNRESOLVED:
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
    flags = [*FLAGS, '-fno-math-errno', '-ffunction-sections', '-fdata-sections', '-DIPOD=0', '-DM1PLUS=1']
    if player: flags += ['-mnan=2008', '-DPEQ_PLAYER=1']
    objects = []
    for name in ['peq.c', 'peq_player.c'] if player else ['peq.c', 'peq_ui.c', 'coverflow.c', 'scrobble.c', 'photos.c', 'books.c', 'games.c', 'visualizer.c', 'playback.c', 'upnext.c', 'spotify.c', 'addon.c', 'radio.c', 'tidal.c', 'netupdate.c', 'onlinematch.c', 'crossfade.c', 'headset.c', 'lockscreen.c', 'chapters.c']:
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
    patch_word(data, prof['seek_slot'], prof['stock_seek'], ps['mp3_seek'], 'Audio demuxer seek slot')
    for address in prof['id3_calls']:
        patch_word(data, address, jal(prof['stock_id3']), jal(ps['id3_gain']), 'MP3 ReplayGain')
    append_payload(data, payload, PLAYER_BASE, max(len(payload), ps['__end']-PLAYER_BASE), 'player')
    (out/'hciplayer').write_bytes(data)
    return dict(stock_sha256=raw_sha, sha256=sha(data), payload_sha256=sha(payload))

def compile_payload(out):
    """Compile and link the payload."""
    extra = compile_common(out, out/'stock-demo')  # also writes the libc/libcstl imports navigation.c uses
    flags = [*FLAGS, '-DIPOD=0', '-DM1PLUS=1']
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
    from build import HOOKS, IPOD_HOOKS
    for x in dict.fromkeys(x for _, _, x in (HOOKS | IPOD_HOOKS).values() if x):
        if x not in resume:
            asm += [f'.globl stock_{x}_trampoline', f'stock_{x}_trampoline:', 'jr $ra', 'move $v0, $zero']
    (out/'trampoline.S').write_text('\n'.join(asm)+'\n')
    run('clang',*flags,'-c',out/'trampoline.S','-o',out/'trampoline.o')
    leaf_paint = WM_PAINT_LEAF_M1PLUS
    undefined = [f'--undefined={name}' for _, name, _ in active_hooks.values()]
    undefined += [f'--undefined={leaf_paint[2]}', '--undefined=ringnav_audio_extension', '--undefined=ringnav_bootmode', '--undefined=playback_set']
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
    """Whether path is an audited M1 Plus input (build.py's build() hands it here)."""
    return hashlib.sha256(path.read_bytes()).hexdigest() in INPUTS

def build(target_path, out, logo, ipod=False, dev=False, m1_release=None):
    """m1_release: an M1 Plus release's (name, tag), from tools/release_m1.py: the tag instead of
    VERSIONS', and the name in About and the manifest."""
    check(not ipod, 'M1 Plus has no iPod build yet')
    variant = 'stock'
    version = VERSIONS[variant]
    out.mkdir(parents=True, exist_ok=True)
    dev_count = 0
    if dev:  # the next number in the untracked .build-number
        counter = ROOT/'.build-number'
        dev = int(counter.read_text()) + 1 if counter.exists() else 1
        counter.write_text(f'{dev}\n')
        version = dev_tag(dev, version[-1])
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
    from ipod import SETTINGS_ICONS, imagemagick, patch_word, sized_art
    m1plus_names(sq, out)  # every V2.1 name the payload uses is in V2.1's rootfs
    demo = out/'stock-demo'; demo.write_bytes(raw_demo)
    symbol_table = run('readelf', '-Ws', demo)
    syms = symbols(demo, symbol_table)
    header = [f'#define RING_STEP {RING_STEP}']
    # navigation.c's ringnav_timezone names them; its hook, select_timezone, is unported (M1PLUS_PORTS)
    header.append('#define EXTRA_TIMEZONE_NAMES {' + ','.join(json.dumps(zone) for _, zone in EXTRA_TIMEZONES) + '}')
    syms, stubs = m1plus_symbols(syms, symbol_table)
    stubbed = dict(stubs)
    for name in [*CONTEXT_DATA, *M1PLUS_CONTEXT_DATA]:
        if name in stubbed:
            header += [f'extern unsigned char {M1PLUS_STUB}{name}[{stubbed[name]}];',
                       f'#define {name} ((const unsigned char *){M1PLUS_STUB}{name})']
        else:
            header.append(f'#define {name} ((const unsigned char *)0x{syms[name]:x}u)')
    # iPod's image hook leaves the settings icons' category colours alone (navigation.c settings_icon).
    names = ''.join(n.removesuffix('.png') + '\\0' for n in SETTINGS_ICONS)
    header.append(f'#define SETTINGS_ICON_NAMES "{names}"')
    header.append(f'#define ROCKBOX_FLAG "{ROCKBOX_FLAG}"')  # Home's Rockbox row, for S90play
    # About: the stock firmware's version on its own row, and this build's on the CFW. Version row.
    release = m1_release[0] if m1_release else VERSION
    header += [f'#define STOCK_VERSION "{stock_version}"', f'#define Q2POD_VERSION "{release}{f" dev {dev_count}" if dev else ""}"',
               f'#define Q2POD_TAG "{"" if dev else release}"',  # netupdate.c (unported on M1): the release tag, none when --dev
               f'#define Q2POD_UA "Q2Pod/{release} (https://github.com/jtliang24/q2-pod)"']  # onlinematch.c, as MusicBrainz asks
    (out/'stock.h').write_text('\n'.join(header)+'\n')
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
    for name, address, replacement, words in [WM_PAINT_LEAF_M1PLUS]:
        off = fileoff(patched, address)
        check(syms[name] == address and struct.unpack_from('<III', patched, off) == words, f'{name}: unexpected code')
        jump(off, replacement)
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
    # Single shared version literal: V2.1's updater refuses an equal firmware_v20.info version (update_firmware,
    # 0x4e0e34; docs/m1plus.md), so it carries the build tag and stock V2.1 can be flashed back. About's FW.
    # Version row reads it too; ringnav_about shows STOCK_VERSION there instead.
    check(patched.count(b'V2.1\0') == 1, 'Version literal is not unique')
    off = patched.find(b'V2.1\0')
    patched[off:off+len(version)+1] = version.encode() + b'\0'
    for rtc in [RTC_WRITE, RTC_READ_M1PLUS]:
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
    # New inodes, each with its stock image's metadata, as build.py adds them: the Coverflow icons, the Q2 Pod
    # page's and Streaming rows' icons (drawn in assets/icons/, or a copy of the V2.1 image named), the Home
    # card's art, and the helpers.
    xx = 'release/assets/default/raw/images/xx/'
    mapping = dict(
        shuffle='pset_playmode.png', scrobble='drop_wifi.png', podcasts='dlna.png',
        audiobooks='playset_foldercover.png', photos='pset_covermode.png', books='system_language.png',
        videos='sset_display.png', longsongs='system_time.png')
    icons = {n: ('system_language.png', (ROOT/'assets/icons'/n).read_bytes()) for n in ICONS}
    drawn = ('podcasts', 'audiobooks', 'books', 'videos')
    icons.update({f'local_{n}.png': (like, (ROOT/'assets/icons'/f'local_{n}.png').read_bytes() if n in drawn
                                     else cat(xx+like)) for n, like in mapping.items()})
    for n in ('spotify', 'radio'):  # Streaming's Spotify and Internet Radio rows
        icons[f'stream_{n}.png'] = ('tidal.png', (ROOT/'assets/icons'/f'stream_{n}.png').read_bytes())
        # the Q2 Pod page's rows at V2.1's 40 px (list_row_core); the radio's Now Playing art keeps stream_radio's 52
        icons[f'row_{n}.png'] = ('tidal.png', sized_art((ROOT/'assets/icons'/f'stream_{n}.png').read_bytes(), 40))
    # V2.1's rows draw a 40 px icon (list_row_core) where V1.32's drew 52: the drawn ones at its size,
    # and the Q2 Pod page's Coverflow row from the Coverflow card's art. The Home card's pair is V2.1's
    # 66 px card art (mymusic.png's).
    for n in drawn:
        like, data = icons[f'local_{n}.png']
        icons[f'local_{n}.png'] = (like, sized_art(data, 40))
    icons['local_coverflow.png'] = ('pset_playmode.png', sized_art((ROOT/'assets/icons/menu_coverflow.png').read_bytes(), 40))
    # V1.32's Local Music icons Ratings and Most Played name, which V2.1 lacks: its Favourites and
    # Frequent cards' art at the rows' size.
    icons['local_fav.png'] = ('pset_playmode.png', sized_art(cat(xx+'fav.png'), 40))
    icons['local_frequentplay.png'] = ('pset_playmode.png', sized_art(cat(xx+'many.png'), 40))
    for n in ('home_q2pod', 'home_q2pod_down'):
        icons[f'{n}.png'] = ('mymusic.png', (ROOT/'assets/icons'/f'{n}.png').read_bytes())
    icons['stream_airplay.png'] = ('airplay.png', cat(xx+'airplay.png'))
    added = []
    helper_items = {
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
        version=version, **({'release': m1_release[0]} if m1_release else {}), variant=variant, dev=dev, **({'dev_count': dev_count} if dev else {}), peq=audio, bluealsa_sha256=sha(bluealsa), q2video_sha256=sha((out/'q2video').read_bytes()), q2boot_sha256=sha((out/'q2boot').read_bytes()), **({'q2remote_sha256': sha((out/'q2remote').read_bytes())} if dev else {}), compact_code=[], changed_assets=changed_assets, logo_sha256=sha(logo_data), logo_source=logo_source,
        patch_symbols={n:hex(v) for n,v in ps.items() if n.startswith('stock_')},
        tools={t:run(t,'--version').splitlines()[0] for t in ['clang','ld.lld','llvm-objcopy']} |
              {'imagemagick': imagemagick('-version', data=b'').decode().splitlines()[0]})
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps({k:manifest[k] for k in ['update_sha256','patch_bytes','version']},indent=2))
