/* M1 Plus: smart_wifi.c's stand-in, compiled in its place (tools/m1plus.py compile_payload). Smart Wi-Fi (1.7.3) is
 * unported (docs/m1plus-unported.md): Power has no Smart Wi-Fi row on the M1, so the radio stays as the user left it,
 * which is what smart_wifi.c does with the row off. Its hooks (systemset_wifi_page_init, stream_row, netservice_row,
 * playermore_online) aren't taken. */
#include "navigation.h"

void smart_wake(void) {}
int smart_config(const char *section, const char *key) { return 0; }
void smart_poll(void) {}
int smart_wifi_off(void) { return 0; }
int smart_wifi_wait(void) { return 0; }
int smart_hold(int (*fn)(void *, void *), void *ctx, const char *page) { return 0; }
/* smart_wifi.c's with no hold: fn goes on with the link up, else "Connect to Wi-Fi first" */
int need_link(int (*fn)(void *, void *), void *ctx) {
    if (get_wifisignal() > 0) return 1;
    toast("Connect to Wi-Fi first");
    return 0;
}
