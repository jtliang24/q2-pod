/* M1 Plus: Add to Playlist and Add to My Fav for an artist, genre, album or folder row (2.9). V2.1's batch_add_file
 * (0x4da7dc) expands the row and commits one song at a time, each its own journaled SQLite write to the card, on
 * the UI thread: the watchdog's long count covers it, as it does an import's (navigation.c ringnav_wdt_long). Every
 * caller reaches it here: the stock pages' Add, the playlist page's row, and the payload's own adds, which
 * tools/m1plus.py keeps at V2.1's address. The Q2's V1.32 batch_add_file (0x4f4be8) has the same gap. */
extern void ringnav_wdt_long(void);
extern int stock_batchadd_trampoline(int cls, int dest, void *list, void *select, int arg);
int ringnav_batch_add(int cls, int dest, void *list, void *select, int arg);

int ringnav_batch_add(int cls, int dest, void *list, void *select, int arg) {
    ringnav_wdt_long();
    return stock_batchadd_trampoline(cls, dest, list, select, arg);
}
