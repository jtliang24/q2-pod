/* M1 Plus: V2.1's own pages ringnav navigates, beside contexts.inc's V1.32 ones. In Knob: Navigation
 * the knob turns the volume on a page not listed (knob_nav_active). patch/contexts.inc includes this
 * by a macro, so build.py's check of its quoted names against V1.32's windows doesn't read it; the
 * payload's library_page stays there, where upstream's test/patch.py looks for every runtime page. */
/* System Setting's pages that V2.1 names its own: Date and time's menu and its Automatic Time Set
 * (V1.32's datetime_page and autotime_page), Screen Rotation, Theme, and the DSD, USB, USB volume
 * and CD ripping settings; the pickers open on their checked option. */
{ "typedatetime_page", CTX_FIXED, 0 },
{ "autosynctime_page", CTX_FIXED, CHOICE },
{ "screenrotate_page", CTX_FIXED, CHOICE },
{ "theme_page", CTX_FIXED, CHOICE },
{ "dsdmode_page", CTX_FIXED, CHOICE },
{ "usbset_page", CTX_FIXED, CHOICE },
{ "usbvolmode_page", CTX_FIXED, CHOICE },
{ "rippingset_page", CTX_FIXED, 0 },
{ "system_page", CTX_FIXED, 0 },
/* V2.1's own lists outside System Setting: View Queue's dialog, the Home editor, Recent and
 * Frequent's guide page, search and online search, and CD Ripper's two pages (roadmap U4, from the
 * polish pass). The Tidal and HiFi store pages wait for an account to check them on. */
{ "playmore_dialog", CTX_DYNAMIC, 0 },
{ "homemenu_dialog", CTX_DYNAMIC, 0 },
{ "guide_page", CTX_DYNAMIC, 0 },
{ "search_page", CTX_DYNAMIC, 0 },
{ "onlinesearch_page", CTX_DYNAMIC, 0 },
{ "cdripper_page", CTX_DYNAMIC, 0 },
{ "searchcdripper_page", CTX_DYNAMIC, 0 },
/* Now Playing's queue (its queue button's playqueue_dialog), found on dev 8: the knob turned the volume there. */
{ "playqueue_dialog", CTX_DYNAMIC, 0 },
