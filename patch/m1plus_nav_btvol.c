/* M1 Plus: Bluetooth's own volume level, which V2.1 keeps apart. patch/navigation.c includes this where it stood (docs/m1plus-roadmap.md U1c). */
#if M1PLUS
/* V2.1 keeps Bluetooth's level apart, [PLAYSET] BTVOLUME: its volume dialog, status bar and
 * set_devicevolume use it while the output is Bluetooth, and g_volume stays the jacks'. */
#define BT_VOLUME g_btvolume
#define BT_VOLUME_KEY "BTVOLUME"
int headset_gain(void) {
    if (!bt_audio_ready()) return g_volume;
    return btvol.ready && BT_VOLUME ? 100 : BT_VOLUME;
}
#endif
