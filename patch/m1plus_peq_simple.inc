/* M1 Plus keeps its two-button Simple EQ layout and wheel order.
 * The new Presets shortcut (1.5.8) is deferred; presets remain in Advanced. */
enum { E3_TABS, E3_SWITCH, E3_LOW, E3_HIGH = 4, E3_RESET, E3_PRESETS };
#define E3_LAST E3_RESET
#define E3_BUTTON_COUNT 2
#define E3_BUTTON_FOCUS(i) ((i) ? E3_RESET : E3_SWITCH)
#define E3_BUTTON_NAME(i) ((i) ? "Reset" : names[0])
static const short e3_button[2][2] = { { 12, E3_BUTTON }, { E3_RIGHT, E3_BUTTON } };
