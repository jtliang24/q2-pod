/* M1 Plus: directory markers (1.5.8) remain unported during this merge step.
 * MUSIC_WHERE keeps its existing spoken-word exclusions; new shared callers still
 * expand ordinary SQL and leave stored discovery lists alone, as before. */
#include "peq.h"
#include "library_scope.h"
char *library_scope_query(const char *sql) { return sql ? strdup(sql) : 0; }
int library_scope_hidden(const char *path) { (void)path; return 0; }
