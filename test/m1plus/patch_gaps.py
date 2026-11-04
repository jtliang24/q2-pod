"""The patch.py checks the M1 Plus fails until the iPod UI item that ports them lands (gaprun.py).

Each is a top-level statement of patch.py, keyed by a hash of its source and its number among identical ones, and
listed under the docs/m1plus-ipod-ui.md item that makes it pass; that item's commit drops its entries (a listed
check that passes fails the run). After an edit to patch.py, GAPS_DUMP=gaps.json python3 test/m1plus/patch.py BUILD
writes every failing check, to rekey the list."""
GAPS = {
    # iPod UI assets (ipod-ui 3)
    '2212dfddf4': 'iPod UI assets (ipod-ui 3)',  # patch.py:1383 m=Machine(); root=asset_node(m,decode((B/ui/localmusic/album_page.bin).read_byte
    'ff3de6c4e5': 'iPod UI assets (ipod-ui 3)',  # patch.py:1383 m=Machine(); root=asset_node(m,decode((B/ui/localmusic/album_page.bin).read_byte
    '200658faae': 'iPod UI assets (ipod-ui 3)',  # patch.py:2091 node=next(n for n in ui_walk(decode((B/ui/playing_page.bin).read_bytes())) if n[
    '5965b040da': 'iPod UI assets (ipod-ui 3)',  # patch.py:2092 for x in (22,187,353):
    'cd20baf1b9': 'iPod UI assets (ipod-ui 3)',  # patch.py:11138 assert texts(info)==[Spotify,Song,A, B,LP,0:10,-3:10]
    '35b96a16c8': 'iPod UI assets (ipod-ui 3)',  # patch.py:11145 m.advance(2500); assert texts(info)[4:]==[0:12,-3:08] and len(m.thumbs)==1
    '338b3ce9bb': 'iPod UI assets (ipod-ui 3)',  # patch.py:11194 m.advance(250); assert texts(info)[4]==1:05 and on_wm_keyup_fun not in [c[0] for
    '30331ad68c': 'iPod UI assets (ipod-ui 3)',  # patch.py:11349 m.advance(3000); assert m.labels(np)==[Internet Radio,Three,Some Artist,A Song,M
    # status bar scenarios on the V2.1 bar (Phase 5)
    '78b0d2089b': 'status bar scenarios on the V2.1 bar (Phase 5)',  # patch.py:5441 for v in views:
    '8217be2fad': 'status bar scenarios on the V2.1 bar (Phase 5)',  # patch.py:5450 cells=laid_out()
    '6faac8d410': 'status bar scenarios on the V2.1 bar (Phase 5)',  # patch.py:5452 assert all(h==30 and inset<=x and x+w<=375-inset for x,w,h in cells), (inset,cel
    '4a0bdf3e2a': 'status bar scenarios on the V2.1 bar (Phase 5)',  # patch.py:5453 title=named(m,bar,label_clock); x,w=m.get(title+O[W_X]),m.get(title+O[W_W])
    '83f4a0efd5': 'status bar scenarios on the V2.1 bar (Phase 5)',  # patch.py:5454 left,right=(cells[len(m.nodes[views[0]][children])-1],cells[len(m.nodes[views[0]
    '953d4e8e49': 'status bar scenarios on the V2.1 bar (Phase 5)',  # patch.py:5455 assert left[0]+left[1]<=x and x+w<=right[0] and x+w/2==375/2, (left,right,x,w); 
    '4f4969742f': 'status bar scenarios on the V2.1 bar (Phase 5)',  # patch.py:5461 for mode,want in enumerate((10,O[BATT_PCT_W],O[BATT_BODY_W]+O[BATT_NUB_W]+O[BATT
    'b51c376171': 'status bar scenarios on the V2.1 bar (Phase 5)',  # patch.py:5474 m.nodes[named(m,bar,img_bt)][visible]=0
    '019eb47519': 'status bar scenarios on the V2.1 bar (Phase 5)',  # patch.py:5477 m.nodes[named(m,bar,label_battery)][text]=50%
    'd4e2e98ab7': 'status bar scenarios on the V2.1 bar (Phase 5)',  # patch.py:5480 paint_live_bar()
    '54bedb9c88': 'status bar scenarios on the V2.1 bar (Phase 5)',  # patch.py:5482 assert m.get(eq+O[W_W])==28
    'ee4849c484': 'status bar scenarios on the V2.1 bar (Phase 5)',  # patch.py:5483 assert all(m.nodes[eq][asset][fstyle:{s}:font_size]==16 for s in (normal,disable
    '8fc0d6b69c': 'status bar scenarios on the V2.1 bar (Phase 5)',  # patch.py:5484 clock_box=tuple(m.get(title+O[k]) for k in (W_X,W_Y,W_W,W_H))
    'd4333c8df2': 'status bar scenarios on the V2.1 bar (Phase 5)',  # patch.py:5487 m.advance(0); shown=(m.nodes[state][visible],m.nodes[state].get(image))
    '406773bfbe': 'status bar scenarios on the V2.1 bar (Phase 5)',  # patch.py:5488 for status,equalizer,icon in ((0,0,),(2,0,bar_play),(3,0,bar_pause),(3,0,bar_pau
    '2120c2ed3c': 'status bar scenarios on the V2.1 bar (Phase 5)',  # patch.py:5504 m.word(0xa3beac,2); m.nodes[eq][visible]=1; m.nodes[state][visible]=0
    '2bfc5141c1': 'status bar scenarios on the V2.1 bar (Phase 5)',  # patch.py:5504 m.word(0xa3beac,2); m.nodes[eq][visible]=1; m.nodes[state][visible]=0
    'c0c216337f': 'status bar scenarios on the V2.1 bar (Phase 5)',  # patch.py:5504 m.word(0xa3beac,2); m.nodes[eq][visible]=1; m.nodes[state][visible]=0
    '4cb62ca34f': 'status bar scenarios on the V2.1 bar (Phase 5)',  # patch.py:5506 assert (stock_showface,bar) in [c[:2] for c in m.calls] and m.nodes[state][visib
    '0a9fe5785b': 'status bar scenarios on the V2.1 bar (Phase 5)',  # patch.py:5508 for mode in (1,2,3,0,1,2,3,0):
    # Display settings pages (ipod-ui 4.3)
    'a85f9167be': 'Display settings pages (ipod-ui 4.3)',  # patch.py:2165 for row,image,fills in ((2,select,3),(0,unselect,0),(2,more,4),(0,more,0)):
    '9e5dd4854f': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8720 for name in (local_album,local_photos,list_folder,list_tidal,player_playlist,
    '1068b5c50c': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8757 m,main,_=display({},sub=0)
    'c6052dee0d': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8758 kids=m.nodes[main][children]
    '487c8eb5c1': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8759 assert len(kids)==6 and [row_text(r) for r in kids[3:]]==[Appearance,Coverflow,C
    '2dff49cb69': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8760 assert m.icons_set==[system_display,list_into,playset_covermode,list_into,playse
    'c99a4ebc97': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8761 f,ctx=m.handler(m.nodes[kids[4]][children][0],O[EVT_CLICK]); m.calls=[]
    'e8cb08926c': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8762 assert m.call(address=f,args=(ctx,m.event,0,0),gap=0)==0 and m.opened[-1]==(syst
    '36b49d8f56': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8765 cfv=display_page(m,2); cf,cf_sort,cf_refresh=m.nodes[cfv][children]
    '5db2661012': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8765 cfv=display_page(m,2); cf,cf_sort,cf_refresh=m.nodes[cfv][children]
    'f6375d0298': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8766 assert m.icons_set==[playset_covermode,playset_covermode,system_update]
    '66249771a8': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8767 ctl=display_page(m,3); shortcut,keep_lit,click_hp,hold,qs,wheel=m.nodes[ctl][chi
    'b6f44251eb': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8767 ctl=display_page(m,3); shortcut,keep_lit,click_hp,hold,qs,wheel=m.nodes[ctl][chi
    'ccb736163c': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8768 assert m.icons_set==[playset_covermode,system_display,switch_off,system_display,
    '15567d5dec': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8769 assert [row_text(r) for r in (shortcut,hold,qs)]==[Shortcut: Rockbox,Hold Return
    'dcddcb57a6': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8770 view=display_page(m,1); rows=setting_rows(m,view)
    'f92a41034a': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8770 view=display_page(m,1); rows=setting_rows(m,view)
    '85172db86c': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8771 kids=m.nodes[view][children]; light,corners,centred=kids[1],kids[3],kids[6]
    '944032aee2': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8772 assert kids==[rows[3],light,rows[0],corners,rows[1],rows[2],centred] and m.nodes
    'c9c6fdc8c1': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8773 assert m.icons_set==[system_display,system_display,system_display,system_display
    '0ac48111d4': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8774 buttons=[m.nodes[r][children][0] for r in rows]; labels=[m.nodes[b][children][1]
    '0e824e3e4f': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8774 buttons=[m.nodes[r][children][0] for r in rows]; labels=[m.nodes[b][children][1]
    '549cb92260': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8775 for b,l in zip(buttons,labels):
    '2ab19091a5': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8782 keep_label=m.nodes[m.nodes[keep_lit][children][0]][children][1]; assert m.nodes[
    '70bf24c794': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8782 keep_label=m.nodes[m.nodes[keep_lit][children][0]][children][1]; assert m.nodes[
    '4d56f7c40c': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8783 f,ctx=m.handler(m.nodes[keep_lit][children][0],O[EVT_CLICK]); m.calls=[]
    '86b4e73d17': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8784 assert m.call(address=f,args=(ctx,m.event,0,0),gap=0)==0 and not did(m,image_man
    '1bbb79bed9': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8785 assert [(c[1],m.text(c[2]),m.text(c[3])) for c in m.calls if c[0]==write_int_con
    '8271bfe8ff.10': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8786 m.call(address=f,args=(ctx,m.event,0,0),gap=0)
    '0f4a736089': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8788 hp_label=m.nodes[m.nodes[click_hp][children][0]][children][1]; assert m.nodes[hp
    'cda4c9d091': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8788 hp_label=m.nodes[m.nodes[click_hp][children][0]][children][1]; assert m.nodes[hp
    '4de8cb5d25': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8789 f,ctx=m.handler(m.nodes[click_hp][children][0],O[EVT_CLICK]); m.calls=[]
    '86b4e73d17.2': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8790 assert m.call(address=f,args=(ctx,m.event,0,0),gap=0)==0 and not did(m,image_man
    '49995443e1': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8791 assert [(c[1],m.text(c[2]),m.text(c[3])) for c in m.calls if c[0]==write_int_con
    '8271bfe8ff.11': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8792 m.call(address=f,args=(ctx,m.event,0,0),gap=0)
    '341ae680b0': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8795 centred_label=m.nodes[m.nodes[centred][children][0]][children][1]; assert m.node
    'cb11270062': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8795 centred_label=m.nodes[m.nodes[centred][children][0]][children][1]; assert m.node
    '41b6025c64': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8796 f,ctx=m.handler(m.nodes[centred][children][0],O[EVT_CLICK]); m.calls=[]
    '86b4e73d17.3': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8797 assert m.call(address=f,args=(ctx,m.event,0,0),gap=0)==0 and not did(m,image_man
    '36ad551169': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8798 assert [(c[1],m.text(c[2]),m.text(c[3])) for c in m.calls if c[0]==write_int_con
    '3a615939a6': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8803 assert loaded(playing_page)==[playing_page_stock] and loaded(home_page)==[home_p
    '8271bfe8ff.12': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8804 m.call(address=f,args=(ctx,m.event,0,0),gap=0); assert loaded(playing_page)==[pl
    '6ab6271070': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8806 cf_label=m.nodes[m.nodes[cf][children][0]][children][1]; assert m.nodes[cf_label
    'a153bcc628': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8806 cf_label=m.nodes[m.nodes[cf][children][0]][children][1]; assert m.nodes[cf_label
    'd3ef113228': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8807 f,ctx=m.handler(m.nodes[cf][children][0],O[EVT_CLICK]); m.calls=[]
    'cd883ae115': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8808 assert m.call(address=f,args=(ctx,m.event,0,0),gap=0)==0 and m.nodes[cf_label][t
    '2a4b480d6f': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8809 assert [(c[1],m.text(c[2]),m.text(c[3])) for c in m.calls if c[0]==write_int_con
    '115a769ae0': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8810 m.call(address=f,args=(ctx,m.event,0,0),gap=0); assert m.nodes[cf_label][text]==
    '8271bfe8ff.13': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8810 m.call(address=f,args=(ctx,m.event,0,0),gap=0); assert m.nodes[cf_label][text]==
    '6ab6271070.2': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8811 m.call(address=f,args=(ctx,m.event,0,0),gap=0); assert m.nodes[cf_label][text]==
    '8271bfe8ff.14': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8811 m.call(address=f,args=(ctx,m.event,0,0),gap=0); assert m.nodes[cf_label][text]==
    '5350877c9a': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8814 sort_label,refresh_label=(m.nodes[m.nodes[r][children][0]][children][1] for r in
    '1f952a4891': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8815 assert m.nodes[sort_label][text]==Coverflow Sort: Album and m.nodes[refresh_labe
    'acc55bb4b8': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8816 f,ctx=m.handler(m.nodes[cf_refresh][children][0],O[EVT_CLICK]); m.mock(opendir@G
    'd9ba565d32': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8817 assert m.call(address=f,args=(ctx,m.event,0,0),gap=0)==0 and m.toasts[-1][3]==Co
    '26bda3c14e': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8818 assert [m.text(c[1]) for c in m.calls if c[0]==opendir@GLIBC_2.0]==[/mnt/mmc/.co
    '1cdc7d997d': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8827 assert texts()==[Accent: Ivory,Home: Split,Battery: Icon,Theme: Minimal]; passed
    'a7f54dea42': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8835 m.call(address=HOOKS[home_page_init][0],args=(home,0,0,0),gap=0)
    'd3cec3151b': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8836 art=named(m,home,img_homeart)
    '84fb5c2e21': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8861 shortcut_button=m.nodes[shortcut][children][0]
    '5622a7e908': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8862 sf,sc=m.handler(shortcut_button,O[EVT_CLICK])
    'e5e97b6d36': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8863 for label in (Favorites,Shuffle,Rated Albums,Artists,Albums,Games,Rockbox):
    '927dc434cc': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8867 writes=click(1); assert [(w[0],m.text(w[2])) for w in writes]==[(1,HOME)] and te
    'a0f267beae': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8867 writes=click(1); assert [(w[0],m.text(w[2])) for w in writes]==[(1,HOME)] and te
    '0c075ea462': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8876 corners_label=m.nodes[m.nodes[corners][children][0]][children][1]; assert m.node
    '3fd3d27d9c': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8876 corners_label=m.nodes[m.nodes[corners][children][0]][children][1]; assert m.node
    '88774fb87c': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8878 assert corners_switch()==[switch_off]
    '66dc56914a': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8879 f,ctx=m.handler(m.nodes[corners][children][0],O[EVT_CLICK]); m.calls=[]
    '191084d657': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8880 assert m.call(address=f,args=(ctx,m.event,0,0),gap=0)==0 and corners_switch()==[
    '445cf125f8': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8881 assert [(c[1],m.text(c[3])) for c in m.calls if c[0]==write_int_config]==[(1,ROU
    '8329427fda': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8883 light_label=m.nodes[m.nodes[light][children][0]][children][1]; assert m.nodes[li
    'a206a7a356': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8883 light_label=m.nodes[m.nodes[light][children][0]][children][1]; assert m.nodes[li
    '7553168288': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8884 f,ctx=f_light,ctx_light=m.handler(m.nodes[light][children][0],O[EVT_CLICK])
    '91dc641367': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8885 for value,text in ((1,On),(2,Auto),(0,Off)):
    'f1eae9f6ce': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8900 writes=click(3); assert [(w[0],m.text(w[1]),m.text(w[2])) for w in writes]==[(1,
    'fd2f07fc93': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8900 writes=click(3); assert [(w[0],m.text(w[1]),m.text(w[2])) for w in writes]==[(1,
    'd54d44a9a7': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8901 assert corners_switch()==[switch_off] and m.nodes[light_label][text]==Light Mode
    'c181110dc5': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8902 assert (image_manager_unload_all,0x1000500) in [c[:2] for c in m.calls] and (wid
    '85172db86c.2': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8903 kids=m.nodes[view][children]
    '944032aee2.2': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8904 assert kids==[rows[3],light,rows[0],corners,rows[1],rows[2],centred] and m.nodes
    '044cdebfbf': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8905 assert texts()==[Accent: Cobalt,Home: Split,Battery: Icon,Theme: Classic]; home_
    'baa6580069': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8905 assert texts()==[Accent: Cobalt,Home: Split,Battery: Icon,Theme: Classic]; home_
    'd652ea7b25.2': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8907 m.paint(view); assert m.selected(view)==0; passed()
    'bb0f2639c0': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8911 for _ in range(2): m.call(address=f_light,args=(ctx_light,m.event,0,0),gap=0)
    'a206a7a356.2': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8912 assert m.nodes[light_label][text]==Light Mode: Off
    '231e4ded71': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8913 for value,name in ((5,Tangerine),(6,Plum),(8,Green),(0,Graphite),(1,Crimson),(2,
    '304a770053': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8921 writes=click(3); assert [(w[0],m.text(w[2])) for w in writes]==[(0,THEME),(0,MIN
    'f1eae9f6ce.2': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8921 writes=click(3); assert [(w[0],m.text(w[2])) for w in writes]==[(0,THEME),(0,MIN
    '26a9fde919': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8922 assert texts()[3]==Theme: Minimal and corners_switch()==[switch_on] and m.nodes[
    'd652ea7b25.3': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8923 m.paint(view); assert m.selected(view)==0
    '85172db86c.3': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8924 kids=m.nodes[view][children]
    '78b2a6d980': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8925 assert kids==[rows[3],light,rows[0],corners,rows[1],rows[2],centred] and texts()
    '466012b4b4.3': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8926 home_bounds(False)
    '6c1776f92b': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8927 m.paint(view); assert not m.bands and m.rounded[0][color]==color_t(ACCENTS[0][0]
    'a573372f36': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8929 m.call(address=f_light,args=(ctx_light,m.event,0,0),gap=0); m.call(address=f_lig
    'a573372f36.2': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8929 m.call(address=f_light,args=(ctx_light,m.event,0,0),gap=0); m.call(address=f_lig
    '9406000021': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8930 assert m.nodes[light_label][text]==Light Mode: Auto
    'f49ec85af4': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8931 for theme in (Classic,Minimal):
    'a206a7a356.3': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8933 m.call(address=f_light,args=(ctx_light,m.event,0,0),gap=0); assert m.nodes[light
    'a573372f36.3': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8933 m.call(address=f_light,args=(ctx_light,m.event,0,0),gap=0); assert m.nodes[light
    '472cbcd7f9': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8935 for value,name in ((1,Crimson),(2,Tidal),(3,Champagne),(4,Cobalt),(5,Tangerine),
    '3264b12e96': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8939 click(3); home_bounds(False,True); click(3); home_bounds(False); passed()
    '3264b12e96.2': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8939 click(3); home_bounds(False,True); click(3); home_bounds(False); passed()
    '466012b4b4.4': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8939 click(3); home_bounds(False,True); click(3); home_bounds(False); passed()
    'baa6580069.3': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8939 click(3); home_bounds(False,True); click(3); home_bounds(False); passed()
    '63150259f5': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8941 for value,name in ((1,Percent),(2,Icon + Percent),(3,Percent Inside),(0,Icon)):
    '47417148e4': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8945 m,view,rows=display({ACCENT:2,HOME:1,BATTERY:2,SHORTCUT:1}); got=[m.nodes[
    'e44a70fe75': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8945 m,view,rows=display({ACCENT:2,HOME:1,BATTERY:2,SHORTCUT:1}); got=[m.nodes[
    'f529705857': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8945 m,view,rows=display({ACCENT:2,HOME:1,BATTERY:2,SHORTCUT:1}); got=[m.nodes[
    'b43f0ec9d3': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8946 m,view,rows=display({BATTERY:3}); assert m.nodes[m.nodes[m.nodes[rows[2]][childr
    'e8b43de32c': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8946 m,view,rows=display({BATTERY:3}); assert m.nodes[m.nodes[m.nodes[rows[2]][childr
    '47417148e4.2': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8947 m,view,rows=display({ACCENT:2,HOME:1,THEME:1}); got=[m.nodes[m.nodes[m.nodes[r
    'e684a09ad2': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8947 m,view,rows=display({ACCENT:2,HOME:1,THEME:1}); got=[m.nodes[m.nodes[m.nodes[r
    '49c403d473': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8948 assert got==[Accent: Tidal,Home: Full,Battery: Icon,Theme: Classic] and m.nodes[
    'b5c738c80f': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8978 m,view,_=display({},sub=0)
    '3d40ff6b9b': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8981 assert m.selected(view)==3 and m.confirm()==11 and m.dispatched()[0][1]==m.nodes
    'b32ce1e463': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8985 assert at(0x613ee8,4)==bytes.fromhex(1cc7a524) and at(0x77c71c,5)==bdone\0; pass
    'dca5c4a74d': 'Display settings pages (ipod-ui 4.3)',  # patch.py:9068 for classic in (0,1):
    '01f9e7d40a': 'Display settings pages (ipod-ui 4.3)',  # patch.py:9083 CONFIG.clear(); m,view=settings(display,sub=1); items=m.nodes[view][children]; t
    '4a05eb9365': 'Display settings pages (ipod-ui 4.3)',  # patch.py:9083 CONFIG.clear(); m,view=settings(display,sub=1); items=m.nodes[view][children]; t
    'a993d66116': 'Display settings pages (ipod-ui 4.3)',  # patch.py:9083 CONFIG.clear(); m,view=settings(display,sub=1); items=m.nodes[view][children]; t
    'e0a4fa8337': 'Display settings pages (ipod-ui 4.3)',  # patch.py:9088 previous=m.node(window,sysset_page,[cached,library]); m.nodes[m.wm][children].in
    'e1e8ddc1d0': 'Display settings pages (ipod-ui 4.3)',  # patch.py:9089 for classic in (1,0,1,0,1):  # each a click on Theme, from Minimal
    '075f869521': 'Display settings pages (ipod-ui 4.3)',  # patch.py:9107 m,view=settings(0x4cbcc4,default=72); before=tree(m,view); lay(m,view); after=tr
    '9aec68f85c': 'Display settings pages (ipod-ui 4.3)',  # patch.py:9107 m,view=settings(0x4cbcc4,default=72); before=tree(m,view); lay(m,view); after=tr
    'd83a7b5843': 'Display settings pages (ipod-ui 4.3)',  # patch.py:9107 m,view=settings(0x4cbcc4,default=72); before=tree(m,view); lay(m,view); after=tr
    'db4762b8ba': 'Display settings pages (ipod-ui 4.3)',  # patch.py:9107 m,view=settings(0x4cbcc4,default=72); before=tree(m,view); lay(m,view); after=tr
    'ba217aad41': 'Display settings pages (ipod-ui 4.3)',  # patch.py:9108 assert [r[1] for r in after]==[r[1] for r in before] and all(r[0][3]==72 for r i
    '6f053ba547': 'Display settings pages (ipod-ui 4.3)',  # patch.py:9110 m,view=settings(0x4cbcc4); odd=m.node(list_item); other=m.node(button)
    '075f869521.2': 'Display settings pages (ipod-ui 4.3)',  # patch.py:9113 m.nodes[view][children].append(odd); lay(m,view)
    'f8aa851a1b': 'Display settings pages (ipod-ui 4.3)',  # patch.py:9113 m.nodes[view][children].append(odd); lay(m,view)
    '075f869521.3': 'Display settings pages (ipod-ui 4.3)',  # patch.py:9117 m,view=settings(0x4cbcc4); lay(m,view); items=m.nodes[view][children]
    '6f053ba547.2': 'Display settings pages (ipod-ui 4.3)',  # patch.py:9117 m,view=settings(0x4cbcc4); lay(m,view); items=m.nodes[view][children]
    'a993d66116.2': 'Display settings pages (ipod-ui 4.3)',  # patch.py:9117 m,view=settings(0x4cbcc4); lay(m,view); items=m.nodes[view][children]
    '375301fb60': 'Display settings pages (ipod-ui 4.3)',  # patch.py:9118 buttons=[m.nodes[i][children][0] for i in items]
    'd652ea7b25.4': 'Display settings pages (ipod-ui 4.3)',  # patch.py:9119 m.paint(view); assert m.selected(view)==0
    '588932ae9b': 'Display settings pages (ipod-ui 4.3)',  # patch.py:9120 for k in range(1,len(items)):
    '330e6086e6.2': 'Display settings pages (ipod-ui 4.3)',  # patch.py:9125 assert m.confirm()==11 and m.dispatched()[0][1]==buttons[-1]; passed()
    '638c1bd20c': 'Display settings pages (ipod-ui 4.3)',  # patch.py:9126 m.click(buttons[2]); assert m.selected(view)==2; passed()
    'ecbccc89c2': 'Display settings pages (ipod-ui 4.3)',  # patch.py:9126 m.click(buttons[2]); assert m.selected(view)==2; passed()
    'f9bab94df3': 'Display settings pages (ipod-ui 4.3)',  # patch.py:9130 m,view,rows=display({ACCENT:2}); m.paint(view)
    '8fe2090d8d': 'Display settings pages (ipod-ui 4.3)',  # patch.py:9131 assert not m.bands and m.rounded[-1][color]==color_t(0xeeeeec); passed()
    '5ffc96853b': 'Display settings pages (ipod-ui 4.3)',  # patch.py:9132 m,view,rows=display({ACCENT:2,THEME:1}); m.paint(view)
    'fe173a1c41': 'Display settings pages (ipod-ui 4.3)',  # patch.py:9133 assert [m.bands[i][4] for i in (0,1,47)]==[color_t(ACCENTS[2][i]) for i in (4,0,
    '8271bfe8ff.15': 'Display settings pages (ipod-ui 4.3)',  # patch.py:9134 f,ctx=m.handler(m.nodes[rows[0]][children][0],O[EVT_CLICK]); m.call(address=f,ar
    '91e3bc677a': 'Display settings pages (ipod-ui 4.3)',  # patch.py:9134 f,ctx=m.handler(m.nodes[rows[0]][children][0],O[EVT_CLICK]); m.call(address=f,ar
    'b42e571763': 'Display settings pages (ipod-ui 4.3)',  # patch.py:9135 m.paint(view); assert [m.bands[i][4] for i in (0,1,47)]==[color_t(ACCENTS[3][i])
    'c547892cd4.2': 'Display settings pages (ipod-ui 4.3)',  # patch.py:9143 assert m.nodes[m.slider][FG]==-1; centre(m,50); assert m.nodes[m.slider][FG]==si
    'f1671ac043': 'Display settings pages (ipod-ui 4.3)',  # patch.py:9148 for config,listw,roww,shown in (({HOME:1},375,O[HOME_FULL_ROW],0),({},O[HOME_SPL
    # Library rows (ipod-ui 4.4)
    'a44d2b3708': 'Library rows (ipod-ui 4.4)',  # patch.py:5703 if localmusic_playlistsmore_page_init in HOOKS or is_m1plus:  # M1 Plus: no play
    '068a8e2bb8': 'Library rows (ipod-ui 4.4)',  # patch.py:9844 assert m.nodes[title][style]==m.nodes[detail][style] and m.nodes[title][style]==
    '90bd3c3315': 'Library rows (ipod-ui 4.4)',  # patch.py:10104 assert m.call(address=LIBRARY_INIT,args=(m.top,5,0,0),gap=0)==0 and len(m.nodes[
    '1735956559': 'Library rows (ipod-ui 4.4)',  # patch.py:10107 assert m.call(address=LIBRARY_INIT,args=(m.top,5,0,0),gap=0)==0 and len(m.nodes[
    '1735956559.2': 'Library rows (ipod-ui 4.4)',  # patch.py:10130 assert m.call(address=LIBRARY_INIT,args=(m.top,5,0,0),gap=0)==0 and len(m.nodes[
    'c9436c1725': 'Library rows (ipod-ui 4.4)',  # patch.py:10132 assert m.nodes[icon][image]==local_podcasts and m.nodes[label][text]==Podcasts a
    'e426449b2e': 'Library rows (ipod-ui 4.4)',  # patch.py:10134 assert m.call(address=f,args=(ctx,m.event,0,0),gap=0)==0 and [m.text(c[1]) for c
    'aff13a2aa5': 'Library rows (ipod-ui 4.4)',  # patch.py:10137 assert m.text(syms[g_folder_path])==/mnt/mmc/PODCASTS and m.u.mem_read(syms[g_fo
    '6904e6d290': 'Library rows (ipod-ui 4.4)',  # patch.py:10138 assert [c[0] for c in m.calls]==([stock_folder,folder_reset_variable,strlen@GLIB
    'e2bf44dcdb': 'Library rows (ipod-ui 4.4)',  # patch.py:10156 assert m.text(syms[g_folder_path])==/mnt/mmc/Audiobooks and m.u.mem_read(syms[g_
    '4cf040f0ac.2': 'Library rows (ipod-ui 4.4)',  # patch.py:10162 assert m.u.mem_read(syms[g_folder_layer],1)[0]==1; passed()
    'e1488a9b2c': 'Library rows (ipod-ui 4.4)',  # patch.py:10419 assert m.nodes[icon][image]==local_photos and m.nodes[label][text]==Photos and l
    'f70dc558f2': 'Library rows (ipod-ui 4.4)',  # patch.py:10421 page=m.top; assert m.nodes[page][name]==photos_page and m.nodes[page][style:norm
    '0bbb08dfbf': 'Library rows (ipod-ui 4.4)',  # patch.py:10422 albums,grid,viewer=m.nodes[page][children]; assert not m.nodes[grid][visible] an
    'f137392a59': 'Library rows (ipod-ui 4.4)',  # patch.py:10422 albums,grid,viewer=m.nodes[page][children]; assert not m.nodes[grid][visible] an
    '98bd21d7ec': 'Library rows (ipod-ui 4.4)',  # patch.py:10427 assert labels(albums)==[Photos,All Photos,Trip]; passed()
    'e684ea0e3b': 'Library rows (ipod-ui 4.4)',  # patch.py:10430 rows=m.find(scroll_view,albums); first=m.nodes[rows][children][0]
    'ef0fa3e1ea': 'Library rows (ipod-ui 4.4)',  # patch.py:10430 rows=m.find(scroll_view,albums); first=m.nodes[rows][children][0]
    '7a16728ff5': 'Library rows (ipod-ui 4.4)',  # patch.py:10431 f,ctx=m.handler(first,O[EVT_CLICK]); m.call(address=f,args=(ctx,m.event,0,0),gap
    '1fd75a2d47': 'Library rows (ipod-ui 4.4)',  # patch.py:10432 assert not m.nodes[albums][visible] and m.nodes[grid][visible] and labels(grid)=
    'f35ed69ec8': 'Library rows (ipod-ui 4.4)',  # patch.py:10433 tiles_view=m.find(scroll_view,grid); tiles=m.nodes[tiles_view][children]
    'f527a66865': 'Library rows (ipod-ui 4.4)',  # patch.py:10433 tiles_view=m.find(scroll_view,grid); tiles=m.nodes[tiles_view][children]
    'f2dcd8f006': 'Library rows (ipod-ui 4.4)',  # patch.py:10434 assert m.nodes[tiles_view].get(yslidable)==1 and m.nodes[tiles_view].get(virtual
    'ca5bcbf4b7': 'Library rows (ipod-ui 4.4)',  # patch.py:10435 assert [cf_geometry(m,t) for t in tiles]==[(O[PH_GRID_X]+(i%O[PH_COLS])*O[PH_TIL
    '014c02e5ef': 'Library rows (ipod-ui 4.4)',  # patch.py:10436 assert all(m.nodes[t][style]==S(s_listitem_black) for t in tiles) and len(m.thre
    '5e9c3519c5.5': 'Library rows (ipod-ui 4.4)',  # patch.py:10443 worker,arg=m.threads[0]; assert m.call(address=worker,args=(arg,0,0,0),gap=0,cou
    '05e51b9735': 'Library rows (ipod-ui 4.4)',  # patch.py:10445 assert m.thumbs==[(paths[0],cache(0,.tmp),SW,SH),(cache(0,.jpg),cache(0,.tmp),TW
    'c8bc727799': 'Library rows (ipod-ui 4.4)',  # patch.py:10449 assert m.forks==1 and m.bad=={cache(2,.bad)} and cache(2,.jpg) not in m.cache
    '35102b9315': 'Library rows (ipod-ui 4.4)',  # patch.py:10450 m.advance(250); assert m.joins==[77]; passed()
    '9798366090': 'Library rows (ipod-ui 4.4)',  # patch.py:10452 border(tiles[1]); assert m.draws[-1]==((0,0,54,72),((O[PH_TILE_W]-54)//2,(O[PH_T
    '3f8d3b67be': 'Library rows (ipod-ui 4.4)',  # patch.py:10456 f,ctx=m.handler(tiles[1],O[EVT_CLICK]); m.call(address=f,args=(ctx,m.event,0,0),
    '689b5f7f65': 'Library rows (ipod-ui 4.4)',  # patch.py:10457 s=m.find(slide_menu,viewer); m.slide=s
    '803c670638': 'Library rows (ipod-ui 4.4)',  # patch.py:10458 assert m.nodes[viewer][visible] and not m.nodes[grid][visible] and len(m.nodes[s
    '445325f05f': 'Library rows (ipod-ui 4.4)',  # patch.py:10461 assert stride==(O[PH_SHOT_H] if is_m1plus else O[UI_W]), stride
    'd3dd7d93fb': 'Library rows (ipod-ui 4.4)',  # patch.py:10462 assert m.get(s+O[SLIDE_INDEX])==1
    'f14b2a65e7': 'Library rows (ipod-ui 4.4)',  # patch.py:10465 assert m.draws==want_draws and m.loads==[file://+cache(1,.jpg),file://+cache(0,.
    '9a0ce9d7d0': 'Library rows (ipod-ui 4.4)',  # patch.py:10469 (_,a),(_,b)=m.draws
    '9c02c75b54': 'Library rows (ipod-ui 4.4)',  # patch.py:10472 assert len(m.draws)==2 and a[0]-rest_x==b[0]+O[UI_W] and a[0]-rest_x==O[UI_W]//4
    'd869882dfa': 'Library rows (ipod-ui 4.4)',  # patch.py:10474 if is_m1plus:
    'eb14fc1851': 'Library rows (ipod-ui 4.4)',  # patch.py:10492 info=[x for x in m.nodes[viewer][children] if m.nodes[x][type]==hscroll_label][0
    '375ba953ac': 'Library rows (ipod-ui 4.4)',  # patch.py:10494 assert len([x for x in m.nodes[viewer][children] if m.nodes[x].get(style)==navba
    'b1e491e365': 'Library rows (ipod-ui 4.4)',  # patch.py:10496 assert not m.nodes[info][visible] and inset<=x and x+bw<=O[UI_W]-inset  # the wh
    '04d4486489': 'Library rows (ipod-ui 4.4)',  # patch.py:10497 f,ctx=m.handler(m.nodes[s][children][1],O[EVT_CLICK]); m.call(address=f,args=(ct
    'd3326d5c6b': 'Library rows (ipod-ui 4.4)',  # patch.py:10498 assert m.nodes[info][visible] and m.nodes[info][text]==2 of 4  b.jpg and m.nodes
    '77da0b2628': 'Library rows (ipod-ui 4.4)',  # patch.py:10499 m.call(address=f,args=(ctx,m.event,0,0),gap=0); assert not m.nodes[info][visible
    '2e373d3697': 'Library rows (ipod-ui 4.4)',  # patch.py:10500 m.word(s+O[SLIDE_INDEX],2); f,ctx=m.handler(s,O[EVT_VALUE_CHANGED]); m.call(addr
    'c7fddc062c': 'Library rows (ipod-ui 4.4)',  # patch.py:10501 assert m.nodes[info][visible] and m.nodes[info][text]=="Cant open this photo"; p
    '807736ab70': 'Library rows (ipod-ui 4.4)',  # patch.py:10503 m.top=page; assert m.call()==11 and signed(m.get(m.get(s+O[SLIDE_ANIMATOR])+O[AN
    '756d505e56': 'Library rows (ipod-ui 4.4)',  # patch.py:10505 m.page=page; assert m.key()==11 and m.nodes[grid][visible] and not m.nodes[viewe
    '45e71bc88a': 'Library rows (ipod-ui 4.4)',  # patch.py:10506 assert m.nodes[tiles_view][_ringnav_index]==2 and m.nodes[tiles_view][_ringnav_c
    '3e0937e7bd': 'Library rows (ipod-ui 4.4)',  # patch.py:10507 assert m.key()==11 and m.nodes[albums][visible] and not m.nodes[grid][visible]
    'c41f2aab67': 'Library rows (ipod-ui 4.4)',  # patch.py:10509 m.close(); assert sorted(m.destroyed)==sorted(m.frames) and m.frames; passed()
    'cbacef2660': 'Library rows (ipod-ui 4.4)',  # patch.py:10629 assert m.nodes[icon][image]==local_books and m.nodes[label][text]==Books and len
    'b358ca1c9e': 'Library rows (ipod-ui 4.4)',  # patch.py:10632 page=m.page=m.top; assert m.nodes[page][name]==books_page and m.nodes[page][styl
    '733a834669': 'Library rows (ipod-ui 4.4)',  # patch.py:10635 assert [m.nodes[b][style] for b in back]==([navbar_btnreturn_style] if is_m1plus
    'c46dab838d': 'Library rows (ipod-ui 4.4)',  # patch.py:10636 assert not m.nodes[reader][visible] and labels(books)==[Books,A Tale,Zed]; passe
    '9f67208a44': 'Library rows (ipod-ui 4.4)',  # patch.py:10639 rows=m.nodes[m.find(scroll_view,books)][children]
    '3cc8ca65d6': 'Library rows (ipod-ui 4.4)',  # patch.py:10645 open_book(1); assert m.nodes[reader][visible] and not m.nodes[books][visible] an
    '4da64fc55e': 'Library rows (ipod-ui 4.4)',  # patch.py:10645 open_book(1); assert m.nodes[reader][visible] and not m.nodes[books][visible] an
    'b1fcbcb769': 'Library rows (ipod-ui 4.4)',  # patch.py:10647 assert len(first)==O[BOOK_ROWS] and all(c==0xffffffff and font==(default,20) for
    '498022484e': 'Library rows (ipod-ui 4.4)',  # patch.py:10648 assert  .join(t for t,*_ in first if t).split()==words[:len( .join(t for t,*_ in
    '4d543f31ef': 'Library rows (ipod-ui 4.4)',  # patch.py:10652 assert [y for _,_,y,*_ in first]==[6+26*i for i in range(O[BOOK_ROWS])] and len(
    '50336d44f7': 'Library rows (ipod-ui 4.4)',  # patch.py:10655 seen= .join(t for t,*_ in first+second).split(); assert seen==words[:len(seen)] 
    '6f3fb08151': 'Library rows (ipod-ui 4.4)',  # patch.py:10659 assert m.call(O[KEY_CENTER])==11 and m.nodes[info][visible] and re.fullmatch(r\d
    '9ed8cbf09a': 'Library rows (ipod-ui 4.4)',  # patch.py:10661 assert m.key()==11 and m.nodes[books][visible] and /mnt/data/ringnav-books in m.
    '1122a9c94c': 'Library rows (ipod-ui 4.4)',  # patch.py:10662 assert m.nodes[m.find(scroll_view,books)][_ringnav_index]==1
    '3cc8ca65d6.2': 'Library rows (ipod-ui 4.4)',  # patch.py:10663 open_book(1); assert page_lines()==third; passed()
    '7a7393e41f': 'Library rows (ipod-ui 4.4)',  # patch.py:10666 m.key(); open_book(0); assert m.nodes[info][visible] and m.nodes[info][text]==Pr
    '89ccc96807': 'Library rows (ipod-ui 4.4)',  # patch.py:10666 m.key(); open_book(0); assert m.nodes[info][visible] and m.nodes[info][text]==Pr
    '5e9c3519c5.6': 'Library rows (ipod-ui 4.4)',  # patch.py:10667 worker,arg=m.threads[0]; assert m.call(address=worker,args=(arg,0,0,0),gap=0,cou
    'ff8f3c9395': 'Library rows (ipod-ui 4.4)',  # patch.py:10669 assert bytes(m.files[cache])==Chapter 1\n\nCafé & tea.\f\nChapter 2.encode() and
    'a02c341028': 'Library rows (ipod-ui 4.4)',  # patch.py:10670 assert [t for t,*_ in page_lines()]==[Chapter 1,,Café & tea.] and m.call()==11 a
    '89ccc96807.2': 'Library rows (ipod-ui 4.4)',  # patch.py:10673 m.key(); m.files[R+/Series/A Tale.EPUB]=bytearray(bPK junk); m.files.pop(cache);
    '9f1e9af975': 'Library rows (ipod-ui 4.4)',  # patch.py:10673 m.key(); m.files[R+/Series/A Tale.EPUB]=bytearray(bPK junk); m.files.pop(cache);
    '66ca87bd79': 'Library rows (ipod-ui 4.4)',  # patch.py:10674 worker,arg=m.threads[-1]; m.call(address=worker,args=(arg,0,0,0),gap=0,count=50_
    'e0231eb762': 'Library rows (ipod-ui 4.4)',  # patch.py:10675 assert m.nodes[info][visible] and m.nodes[info][text]=="Cant open this book" and
    'e39fa9664a': 'Library rows (ipod-ui 4.4)',  # patch.py:10697 sheet,chooser=games_open(); G=m.get(payload_syms[g])
    '213d438955': 'Library rows (ipod-ui 4.4)',  # patch.py:10698 assert labels(chooser)==[Games,Sudoku,Vortex,Solitaire,Snake] and not m.nodes[sh
    '7fe72d327e': 'Library rows (ipod-ui 4.4)',  # patch.py:10699 rows=m.nodes[m.find(scroll_view,chooser)][children]
    '1a3e33b7bc': 'Library rows (ipod-ui 4.4)',  # patch.py:10708 pick(0); assert m.nodes[sheet][visible] and not m.nodes[chooser][visible] and wo
    '55475613b4': 'Library rows (ipod-ui 4.4)',  # patch.py:10708 pick(0); assert m.nodes[sheet][visible] and not m.nodes[chooser][visible] and wo
    'b20a386471': 'Library rows (ipod-ui 4.4)',  # patch.py:10709 key(O[KEY_NEXT]); assert byte(G_CUR)==1
    'f0312e5d82': 'Library rows (ipod-ui 4.4)',  # patch.py:10709 key(O[KEY_NEXT]); assert byte(G_CUR)==1
    'b5cb0ea5ea': 'Library rows (ipod-ui 4.4)',  # patch.py:10710 key(O[KEY_PREV]); key(O[KEY_PREV]); assert byte(G_CUR)==80
    'b5cb0ea5ea.2': 'Library rows (ipod-ui 4.4)',  # patch.py:10710 key(O[KEY_PREV]); key(O[KEY_PREV]); assert byte(G_CUR)==80
    'f954819afe': 'Library rows (ipod-ui 4.4)',  # patch.py:10710 key(O[KEY_PREV]); key(O[KEY_PREV]); assert byte(G_CUR)==80
    '8ab44fbf2b': 'Library rows (ipod-ui 4.4)',  # patch.py:10711 key(O[KEY_FWD_BTN]); assert byte(G_CUR)==8
    'd32ce63cd7': 'Library rows (ipod-ui 4.4)',  # patch.py:10711 key(O[KEY_FWD_BTN]); assert byte(G_CUR)==8
    '27066724e2': 'Library rows (ipod-ui 4.4)',  # patch.py:10712 key(O[KEY_BACK_BTN]); assert byte(G_CUR)==80; passed()
    'f954819afe.2': 'Library rows (ipod-ui 4.4)',  # patch.py:10712 key(O[KEY_BACK_BTN]); assert byte(G_CUR)==80; passed()
    '6097ea4c6d': 'Library rows (ipod-ui 4.4)',  # patch.py:10716 blank=cells().index(0); clue=next(i for i,c in enumerate(cells()) if c&16)
    '762bfec88c': 'Library rows (ipod-ui 4.4)',  # patch.py:10716 blank=cells().index(0); clue=next(i for i,c in enumerate(cells()) if c&16)
    '66068ea3ba': 'Library rows (ipod-ui 4.4)',  # patch.py:10717 m.byte(G+G_CUR,clue); key(O[KEY_CENTER]); assert not word(G_PICKING)
    '89af2aa3aa': 'Library rows (ipod-ui 4.4)',  # patch.py:10717 m.byte(G+G_CUR,clue); key(O[KEY_CENTER]); assert not word(G_PICKING)
    'de88260b50': 'Library rows (ipod-ui 4.4)',  # patch.py:10717 m.byte(G+G_CUR,clue); key(O[KEY_CENTER]); assert not word(G_PICKING)
    '04c950dde2': 'Library rows (ipod-ui 4.4)',  # patch.py:10718 m.byte(G+G_CUR,blank); key(O[KEY_CENTER]); assert word(G_PICKING)
    '89af2aa3aa.2': 'Library rows (ipod-ui 4.4)',  # patch.py:10718 m.byte(G+G_CUR,blank); key(O[KEY_CENTER]); assert word(G_PICKING)
    'dce369e8ed': 'Library rows (ipod-ui 4.4)',  # patch.py:10718 m.byte(G+G_CUR,blank); key(O[KEY_CENTER]); assert word(G_PICKING)
    'f31d93643d': 'Library rows (ipod-ui 4.4)',  # patch.py:10719 for _ in range(3): key(O[KEY_NEXT])
    '610b9df287': 'Library rows (ipod-ui 4.4)',  # patch.py:10720 paint(); key(O[KEY_CENTER]); assert cells()[blank]==3 and not word(G_PICKING)
    '89af2aa3aa.3': 'Library rows (ipod-ui 4.4)',  # patch.py:10720 paint(); key(O[KEY_CENTER]); assert cells()[blank]==3 and not word(G_PICKING)
    '0c96352e42': 'Library rows (ipod-ui 4.4)',  # patch.py:10721 m.advance(2000); saved=bytes(m.files[/mnt/data/ringnav-sudoku]); assert len(save
    '623961eddf': 'Library rows (ipod-ui 4.4)',  # patch.py:10721 m.advance(2000); saved=bytes(m.files[/mnt/data/ringnav-sudoku]); assert len(save
    '076a4e0505': 'Library rows (ipod-ui 4.4)',  # patch.py:10722 key(O[KEY_CENTER]); key(O[KEY_NEXT]); key(O[KEY_RETURN]); assert cells()[blank]=
    '4df64b387d': 'Library rows (ipod-ui 4.4)',  # patch.py:10722 key(O[KEY_CENTER]); key(O[KEY_NEXT]); key(O[KEY_RETURN]); assert cells()[blank]=
    '89af2aa3aa.4': 'Library rows (ipod-ui 4.4)',  # patch.py:10722 key(O[KEY_CENTER]); key(O[KEY_NEXT]); key(O[KEY_RETURN]); assert cells()[blank]=
    'f0312e5d82.2': 'Library rows (ipod-ui 4.4)',  # patch.py:10722 key(O[KEY_CENTER]); key(O[KEY_NEXT]); key(O[KEY_RETURN]); assert cells()[blank]=
    '17b18e8bc2': 'Library rows (ipod-ui 4.4)',  # patch.py:10723 before=cells(); key(O[KEY_PLAY]); assert cells()==before and word(52); paint()
    '585fa21b17': 'Library rows (ipod-ui 4.4)',  # patch.py:10723 before=cells(); key(O[KEY_PLAY]); assert cells()==before and word(52); paint()
    'a63f5492f4': 'Library rows (ipod-ui 4.4)',  # patch.py:10723 before=cells(); key(O[KEY_PLAY]); assert cells()==before and word(52); paint()
    '2682c91d39': 'Library rows (ipod-ui 4.4)',  # patch.py:10724 key(O[KEY_RETURN]); assert cells()==before and not word(52)
    '4df64b387d.2': 'Library rows (ipod-ui 4.4)',  # patch.py:10724 key(O[KEY_RETURN]); assert cells()==before and not word(52)
    '4df64b387d.3': 'Library rows (ipod-ui 4.4)',  # patch.py:10725 key(O[KEY_RETURN]); m.advance(0); assert word(G_SCREEN)==0 and m.nodes[chooser][
    '66735bf663': 'Library rows (ipod-ui 4.4)',  # patch.py:10725 key(O[KEY_RETURN]); m.advance(0); assert word(G_SCREEN)==0 and m.nodes[chooser][
    '7b597aa195.2': 'Library rows (ipod-ui 4.4)',  # patch.py:10726 assert m.key()==11; passed()
    'c54ae6e308': 'Library rows (ipod-ui 4.4)',  # patch.py:10728 m.page=m.top; pick(1); assert word(G_SCREEN)==2 and len(frames())==1 and m.get(p
    'fd81feb488': 'Library rows (ipod-ui 4.4)',  # patch.py:10728 m.page=m.top; pick(1); assert word(G_SCREEN)==2 and len(frames())==1 and m.get(p
    '39b8a3eb58': 'Library rows (ipod-ui 4.4)',  # patch.py:10729 m.word(payload_syms[wheel_travel],-50&0xffffffff); m.advance(34); assert word(G_
    'b65e55e61d': 'Library rows (ipod-ui 4.4)',  # patch.py:10731 assert made(reset_poweroptions_timer) and made(widget_invalidate_force)
    '89af2aa3aa.5': 'Library rows (ipod-ui 4.4)',  # patch.py:10735 key(O[KEY_CENTER]); m.advance(500); assert word(G_VX)==1 and made(widget_invalid
    '909fcc2b6a': 'Library rows (ipod-ui 4.4)',  # patch.py:10735 key(O[KEY_CENTER]); m.advance(500); assert word(G_VX)==1 and made(widget_invalid
    '8ab44fbf2b.2': 'Library rows (ipod-ui 4.4)',  # patch.py:10736 key(O[KEY_FWD_BTN]); assert not made(widget_invalidate_force)
    'a63f5492f4.2': 'Library rows (ipod-ui 4.4)',  # patch.py:10737 key(O[KEY_PLAY]); assert word(G_PAUSED)==1 and not frames() and m.get(payload_sy
    'ab6bd7a3ab': 'Library rows (ipod-ui 4.4)',  # patch.py:10737 key(O[KEY_PLAY]); assert word(G_PAUSED)==1 and not frames() and m.get(payload_sy
    '0dfa876a9e': 'Library rows (ipod-ui 4.4)',  # patch.py:10738 x=word(G_VX+20),word(G_VX+24); m.advance(500); assert (word(G_VX+20),word(G_VX+2
    '4cf142ac31': 'Library rows (ipod-ui 4.4)',  # patch.py:10738 x=word(G_VX+20),word(G_VX+24); m.advance(500); assert (word(G_VX+20),word(G_VX+2
    'a63f5492f4.3': 'Library rows (ipod-ui 4.4)',  # patch.py:10739 key(O[KEY_PLAY]); assert word(G_PAUSED)==0 and len(frames())==1 and m.get(payloa
    'e8f2d84a5f': 'Library rows (ipod-ui 4.4)',  # patch.py:10739 key(O[KEY_PLAY]); assert word(G_PAUSED)==0 and len(frames())==1 and m.get(payloa
    'ab6bd7a3ab.2': 'Library rows (ipod-ui 4.4)',  # patch.py:10741 assert word(G_PAUSED)==1 and not frames() and m.get(payload_syms[wheel_raw])==0
    '4df64b387d.4': 'Library rows (ipod-ui 4.4)',  # patch.py:10742 key(O[KEY_RETURN]); assert word(G_PAUSED)==2; key(O[KEY_NEXT]); paint(); key(O[K
    '89af2aa3aa.6': 'Library rows (ipod-ui 4.4)',  # patch.py:10742 key(O[KEY_RETURN]); assert word(G_PAUSED)==2; key(O[KEY_NEXT]); paint(); key(O[K
    'f0312e5d82.3': 'Library rows (ipod-ui 4.4)',  # patch.py:10742 key(O[KEY_RETURN]); assert word(G_PAUSED)==2; key(O[KEY_NEXT]); paint(); key(O[K
    'ff742ca8d6': 'Library rows (ipod-ui 4.4)',  # patch.py:10742 key(O[KEY_RETURN]); assert word(G_PAUSED)==2; key(O[KEY_NEXT]); paint(); key(O[K
    '6e49df19e4': 'Library rows (ipod-ui 4.4)',  # patch.py:10751 m.page=m.top; pick(2); assert word(G_SCREEN)==3 and cur()==0 and [n(p) for p in 
    'fe2edce464': 'Library rows (ipod-ui 4.4)',  # patch.py:10751 m.page=m.top; pick(2); assert word(G_SCREEN)==3 and cur()==0 and [n(p) for p in 
    '09e347b645': 'Library rows (ipod-ui 4.4)',  # patch.py:10752 key(O[KEY_CENTER]); m.advance(2000); assert (n(0),n(1))==(23,1) and bytes(m.file
    '89af2aa3aa.7': 'Library rows (ipod-ui 4.4)',  # patch.py:10752 key(O[KEY_CENTER]); m.advance(2000); assert (n(0),n(1))==(23,1) and bytes(m.file
    '27066724e2.2': 'Library rows (ipod-ui 4.4)',  # patch.py:10753 key(O[KEY_NEXT]); assert cur()==1; key(O[KEY_FWD_BTN]); assert cur()==7; key(O[K
    '5393abcfc6': 'Library rows (ipod-ui 4.4)',  # patch.py:10753 key(O[KEY_NEXT]); assert cur()==1; key(O[KEY_FWD_BTN]); assert cur()==7; key(O[K
    '5a8ea34ce4': 'Library rows (ipod-ui 4.4)',  # patch.py:10753 key(O[KEY_NEXT]); assert cur()==1; key(O[KEY_FWD_BTN]); assert cur()==7; key(O[K
    '5a8ea34ce4.2': 'Library rows (ipod-ui 4.4)',  # patch.py:10753 key(O[KEY_NEXT]); assert cur()==1; key(O[KEY_FWD_BTN]); assert cur()==7; key(O[K
    '8ab44fbf2b.3': 'Library rows (ipod-ui 4.4)',  # patch.py:10753 key(O[KEY_NEXT]); assert cur()==1; key(O[KEY_FWD_BTN]); assert cur()==7; key(O[K
    'f0312e5d82.4': 'Library rows (ipod-ui 4.4)',  # patch.py:10753 key(O[KEY_NEXT]); assert cur()==1; key(O[KEY_FWD_BTN]); assert cur()==7; key(O[K
    '27066724e2.3': 'Library rows (ipod-ui 4.4)',  # patch.py:10754 key(O[KEY_PREV]); key(O[KEY_PREV]); assert cur()==12; key(O[KEY_BACK_BTN]); asse
    'b5cb0ea5ea.3': 'Library rows (ipod-ui 4.4)',  # patch.py:10754 key(O[KEY_PREV]); key(O[KEY_PREV]); assert cur()==12; key(O[KEY_BACK_BTN]); asse
    'b5cb0ea5ea.4': 'Library rows (ipod-ui 4.4)',  # patch.py:10754 key(O[KEY_PREV]); key(O[KEY_PREV]); assert cur()==12; key(O[KEY_BACK_BTN]); asse
    'b77931b1d9': 'Library rows (ipod-ui 4.4)',  # patch.py:10754 key(O[KEY_PREV]); key(O[KEY_PREV]); assert cur()==12; key(O[KEY_BACK_BTN]); asse
    'faca4081c1': 'Library rows (ipod-ui 4.4)',  # patch.py:10754 key(O[KEY_PREV]); key(O[KEY_PREV]); assert cur()==12; key(O[KEY_BACK_BTN]); asse
    '2fba74c885': 'Library rows (ipod-ui 4.4)',  # patch.py:10755 put(6,[64|13+11]); put(7,[3,64|10]); m.byte(G+G_SOL+329,7)  # Q of hearts; a fac
    '8829606b74': 'Library rows (ipod-ui 4.4)',  # patch.py:10755 put(6,[64|13+11]); put(7,[3,64|10]); m.byte(G+G_SOL+329,7)  # Q of hearts; a fac
    'b06052aade': 'Library rows (ipod-ui 4.4)',  # patch.py:10755 put(6,[64|13+11]); put(7,[3,64|10]); m.byte(G+G_SOL+329,7)  # Q of hearts; a fac
    '3adb6b93ae': 'Library rows (ipod-ui 4.4)',  # patch.py:10756 key(O[KEY_CENTER]); assert word(G_PICKING) and word(48)==7; paint()
    '60d2c2805f.8': 'Library rows (ipod-ui 4.4)',  # patch.py:10756 key(O[KEY_CENTER]); assert word(G_PICKING) and word(48)==7; paint()
    '89af2aa3aa.8': 'Library rows (ipod-ui 4.4)',  # patch.py:10756 key(O[KEY_CENTER]); assert word(G_PICKING) and word(48)==7; paint()
    '04c950dde2.2': 'Library rows (ipod-ui 4.4)',  # patch.py:10757 key(O[KEY_FWD_BTN]); key(O[KEY_CENTER]); assert word(G_PICKING)  # not onto the 
    '89af2aa3aa.9': 'Library rows (ipod-ui 4.4)',  # patch.py:10757 key(O[KEY_FWD_BTN]); key(O[KEY_CENTER]); assert word(G_PICKING)  # not onto the 
    '8ab44fbf2b.4': 'Library rows (ipod-ui 4.4)',  # patch.py:10757 key(O[KEY_FWD_BTN]); key(O[KEY_CENTER]); assert word(G_PICKING)  # not onto the 
    '89af2aa3aa.10': 'Library rows (ipod-ui 4.4)',  # patch.py:10758 key(O[KEY_FWD_BTN]); key(O[KEY_PREV]); key(O[KEY_CENTER]); assert not word(G_PIC
    '8ab44fbf2b.5': 'Library rows (ipod-ui 4.4)',  # patch.py:10758 key(O[KEY_FWD_BTN]); key(O[KEY_PREV]); key(O[KEY_CENTER]); assert not word(G_PIC
    'b5cb0ea5ea.5': 'Library rows (ipod-ui 4.4)',  # patch.py:10758 key(O[KEY_FWD_BTN]); key(O[KEY_PREV]); key(O[KEY_CENTER]); assert not word(G_PIC
    'de88260b50.2': 'Library rows (ipod-ui 4.4)',  # patch.py:10758 key(O[KEY_FWD_BTN]); key(O[KEY_PREV]); key(O[KEY_CENTER]); assert not word(G_PIC
    'e122849745': 'Library rows (ipod-ui 4.4)',  # patch.py:10759 assert (n(6),n(7),byte(G_SOL+4+24*6+1),byte(G_SOL+4+24*7))==(2,1,64|10,64|3) and
    '2d1aafdcf1': 'Library rows (ipod-ui 4.4)',  # patch.py:10760 put(1,[64|26]); m.byte(G+G_SOL+329,1); key(O[KEY_CENTER]); key(O[KEY_CENTER])  #
    '89af2aa3aa.11': 'Library rows (ipod-ui 4.4)',  # patch.py:10760 put(1,[64|26]); m.byte(G+G_SOL+329,1); key(O[KEY_CENTER]); key(O[KEY_CENTER])  #
    '89af2aa3aa.12': 'Library rows (ipod-ui 4.4)',  # patch.py:10760 put(1,[64|26]); m.byte(G+G_SOL+329,1); key(O[KEY_CENTER]); key(O[KEY_CENTER])  #
    'bb7cea08b8': 'Library rows (ipod-ui 4.4)',  # patch.py:10760 put(1,[64|26]); m.byte(G+G_SOL+329,1); key(O[KEY_CENTER]); key(O[KEY_CENTER])  #
    '66fc1b822e': 'Library rows (ipod-ui 4.4)',  # patch.py:10761 assert not word(G_PICKING) and n(1)==0 and n(2)==1 and byte(G_SOL+4+48)==64|26
    '6f97b4218f': 'Library rows (ipod-ui 4.4)',  # patch.py:10762 m.byte(G+G_SOL+329,6); key(O[KEY_CENTER]); key(O[KEY_CENTER]); assert not word(G
    '89af2aa3aa.13': 'Library rows (ipod-ui 4.4)',  # patch.py:10762 m.byte(G+G_SOL+329,6); key(O[KEY_CENTER]); key(O[KEY_CENTER]); assert not word(G
    '89af2aa3aa.14': 'Library rows (ipod-ui 4.4)',  # patch.py:10762 m.byte(G+G_SOL+329,6); key(O[KEY_CENTER]); key(O[KEY_CENTER]); assert not word(G
    'f24d40e6a6': 'Library rows (ipod-ui 4.4)',  # patch.py:10762 m.byte(G+G_SOL+329,6); key(O[KEY_CENTER]); key(O[KEY_CENTER]); assert not word(G
    '4df64b387d.5': 'Library rows (ipod-ui 4.4)',  # patch.py:10763 key(O[KEY_CENTER]); key(O[KEY_RETURN]); assert not word(G_PICKING) and word(G_SC
    '89af2aa3aa.15': 'Library rows (ipod-ui 4.4)',  # patch.py:10763 key(O[KEY_CENTER]); key(O[KEY_RETURN]); assert not word(G_PICKING) and word(G_SC
    'fc8f50ca54': 'Library rows (ipod-ui 4.4)',  # patch.py:10763 key(O[KEY_CENTER]); key(O[KEY_RETURN]); assert not word(G_PICKING) and word(G_SC
    '2074d0cbd8': 'Library rows (ipod-ui 4.4)',  # patch.py:10764 before_sol=sol(); key(O[KEY_PLAY]); assert word(52); paint(); key(O[KEY_RETURN])
    '3b5bfd9a87': 'Library rows (ipod-ui 4.4)',  # patch.py:10764 before_sol=sol(); key(O[KEY_PLAY]); assert word(52); paint(); key(O[KEY_RETURN])
    '48117aadd2': 'Library rows (ipod-ui 4.4)',  # patch.py:10764 before_sol=sol(); key(O[KEY_PLAY]); assert word(52); paint(); key(O[KEY_RETURN])
    '4df64b387d.6': 'Library rows (ipod-ui 4.4)',  # patch.py:10764 before_sol=sol(); key(O[KEY_PLAY]); assert word(52); paint(); key(O[KEY_RETURN])
    '60d2c2805f.9': 'Library rows (ipod-ui 4.4)',  # patch.py:10764 before_sol=sol(); key(O[KEY_PLAY]); assert word(52); paint(); key(O[KEY_RETURN])
    'a63f5492f4.4': 'Library rows (ipod-ui 4.4)',  # patch.py:10764 before_sol=sol(); key(O[KEY_PLAY]); assert word(52); paint(); key(O[KEY_RETURN])
    '0265a33ba6': 'Library rows (ipod-ui 4.4)',  # patch.py:10765 key(O[KEY_RETURN]); m.advance(0); assert word(G_SCREEN)==0 and m.nodes[chooser][
    '4df64b387d.7': 'Library rows (ipod-ui 4.4)',  # patch.py:10765 key(O[KEY_RETURN]); m.advance(0); assert word(G_SCREEN)==0 and m.nodes[chooser][
    'a8b1b2cfa3': 'Library rows (ipod-ui 4.4)',  # patch.py:10772 m.page=m.top; pick(3); assert word(G_SCREEN)==4 and len(frames())==1 and m.get(p
    'eff446ceed': 'Library rows (ipod-ui 4.4)',  # patch.py:10772 m.page=m.top; pick(3); assert word(G_SCREEN)==4 and len(frames())==1 and m.get(p
    '60d2c2805f.10': 'Library rows (ipod-ui 4.4)',  # patch.py:10773 assert body()==[207,208,209] and sdir()==1 and sstate()==1; paint()
    '78000abffe': 'Library rows (ipod-ui 4.4)',  # patch.py:10773 assert body()==[207,208,209] and sdir()==1 and sstate()==1; paint()
    'f8114faee2': 'Library rows (ipod-ui 4.4)',  # patch.py:10774 snake_before=bytes(m.u.mem_read(G+G_SN,820))
    '144777dfab': 'Library rows (ipod-ui 4.4)',  # patch.py:10775 skey(O[KEY_NEXT]); skey(O[KEY_PREV]); assert bytes(m.u.mem_read(G+G_SN,820))==sn
    '4d62a8962b': 'Library rows (ipod-ui 4.4)',  # patch.py:10775 skey(O[KEY_NEXT]); skey(O[KEY_PREV]); assert bytes(m.u.mem_read(G+G_SN,820))==sn
    '8287c7e95e': 'Library rows (ipod-ui 4.4)',  # patch.py:10775 skey(O[KEY_NEXT]); skey(O[KEY_PREV]); assert bytes(m.u.mem_read(G+G_SN,820))==sn
    '2fa25e9f4c': 'Library rows (ipod-ui 4.4)',  # patch.py:10776 skey(O[KEY_FWD_BTN]); skey(O[KEY_FWD_BTN]); assert sdir()==2
    '2fa25e9f4c.2': 'Library rows (ipod-ui 4.4)',  # patch.py:10776 skey(O[KEY_FWD_BTN]); skey(O[KEY_FWD_BTN]); assert sdir()==2
    '96332b49eb': 'Library rows (ipod-ui 4.4)',  # patch.py:10776 skey(O[KEY_FWD_BTN]); skey(O[KEY_FWD_BTN]); assert sdir()==2
    '0a7bec6f95': 'Library rows (ipod-ui 4.4)',  # patch.py:10777 m.advance(170); assert body()[-1]==229 and sdir()==3 and made(widget_invalidate_
    '00dddc04a1': 'Library rows (ipod-ui 4.4)',  # patch.py:10778 skey(O[KEY_BACK_BTN]); assert sdir()==3  # waits for the next step
    '96b5b20b52': 'Library rows (ipod-ui 4.4)',  # patch.py:10778 skey(O[KEY_BACK_BTN]); assert sdir()==3  # waits for the next step
    '60d2c2805f.11': 'Library rows (ipod-ui 4.4)',  # patch.py:10779 skey(O[KEY_PLAY]); assert word(G_PAUSED)==1 and not frames(); was=body(); m.adva
    '8e41ef36eb': 'Library rows (ipod-ui 4.4)',  # patch.py:10779 skey(O[KEY_PLAY]); assert word(G_PAUSED)==1 and not frames(); was=body(); m.adva
    'af9a1fb5b9': 'Library rows (ipod-ui 4.4)',  # patch.py:10779 skey(O[KEY_PLAY]); assert word(G_PAUSED)==1 and not frames(); was=body(); m.adva
    'c37b29e226': 'Library rows (ipod-ui 4.4)',  # patch.py:10779 skey(O[KEY_PLAY]); assert word(G_PAUSED)==1 and not frames(); was=body(); m.adva
    'e18733dc4c': 'Library rows (ipod-ui 4.4)',  # patch.py:10779 skey(O[KEY_PLAY]); assert word(G_PAUSED)==1 and not frames(); was=body(); m.adva
    '144777dfab.2': 'Library rows (ipod-ui 4.4)',  # patch.py:10780 skey(O[KEY_NEXT]); assert sdir()==3  # no turning while paused
    '96b5b20b52.2': 'Library rows (ipod-ui 4.4)',  # patch.py:10780 skey(O[KEY_NEXT]); assert sdir()==3  # no turning while paused
    '8aa1970242': 'Library rows (ipod-ui 4.4)',  # patch.py:10781 skey(O[KEY_PLAY]); assert word(G_PAUSED)==0 and len(frames())==1
    'c37b29e226.2': 'Library rows (ipod-ui 4.4)',  # patch.py:10781 skey(O[KEY_PLAY]); assert word(G_PAUSED)==0 and len(frames())==1
    'e3f0e327aa': 'Library rows (ipod-ui 4.4)',  # patch.py:10782 m.word(G+G_SN+812,5); m.advance(170*12); assert sstate()==2 and not frames() and
    'eeb61f1ab8': 'Library rows (ipod-ui 4.4)',  # patch.py:10782 m.word(G+G_SN+812,5); m.advance(170*12); assert sstate()==2 and not frames() and
    '25f19f306a': 'Library rows (ipod-ui 4.4)',  # patch.py:10783 best=bytes(m.files[/mnt/data/ringnav-snake]); assert len(best)==12 and best[:8]=
    '33e712f7ef': 'Library rows (ipod-ui 4.4)',  # patch.py:10783 best=bytes(m.files[/mnt/data/ringnav-snake]); assert len(best)==12 and best[:8]=
    '60d2c2805f.12': 'Library rows (ipod-ui 4.4)',  # patch.py:10784 paint(); skey(O[KEY_CENTER]); assert sstate()==1 and body()==[207,208,209] and l
    '7e0adf5d24': 'Library rows (ipod-ui 4.4)',  # patch.py:10784 paint(); skey(O[KEY_CENTER]); assert sstate()==1 and body()==[207,208,209] and l
    'e040fa48bd': 'Library rows (ipod-ui 4.4)',  # patch.py:10784 paint(); skey(O[KEY_CENTER]); assert sstate()==1 and body()==[207,208,209] and l
    '00827aff47': 'Library rows (ipod-ui 4.4)',  # patch.py:10785 skey(O[KEY_BACK_BTN]); assert sdir()==0  # side Previous turns left, without the
    '00dddc04a1.2': 'Library rows (ipod-ui 4.4)',  # patch.py:10785 skey(O[KEY_BACK_BTN]); assert sdir()==0  # side Previous turns left, without the
    '60e611da01': 'Library rows (ipod-ui 4.4)',  # patch.py:10786 m.advance(170); assert body()[-1]==189
    '2fa25e9f4c.3': 'Library rows (ipod-ui 4.4)',  # patch.py:10787 skey(O[KEY_FWD_BTN]); assert sdir()==1  # side Next turns right
    'b274b92071': 'Library rows (ipod-ui 4.4)',  # patch.py:10787 skey(O[KEY_FWD_BTN]); assert sdir()==1  # side Next turns right
    '00dddc04a1.3': 'Library rows (ipod-ui 4.4)',  # patch.py:10788 skey(O[KEY_PLAY]); skey(O[KEY_BACK_BTN]); skey(O[KEY_FWD_BTN]); assert sdir()==1
    '2fa25e9f4c.4': 'Library rows (ipod-ui 4.4)',  # patch.py:10788 skey(O[KEY_PLAY]); skey(O[KEY_BACK_BTN]); skey(O[KEY_FWD_BTN]); assert sdir()==1
    'b274b92071.2': 'Library rows (ipod-ui 4.4)',  # patch.py:10788 skey(O[KEY_PLAY]); skey(O[KEY_BACK_BTN]); skey(O[KEY_FWD_BTN]); assert sdir()==1
    'c37b29e226.3': 'Library rows (ipod-ui 4.4)',  # patch.py:10788 skey(O[KEY_PLAY]); skey(O[KEY_BACK_BTN]); skey(O[KEY_FWD_BTN]); assert sdir()==1
    'c37b29e226.4': 'Library rows (ipod-ui 4.4)',  # patch.py:10789 skey(O[KEY_PLAY])
    'd303e06d4c': 'Library rows (ipod-ui 4.4)',  # patch.py:10790 skey(O[KEY_RETURN]); assert word(G_PAUSED)==2 and word(60)==0
    'faf9c369f1': 'Library rows (ipod-ui 4.4)',  # patch.py:10790 skey(O[KEY_RETURN]); assert word(G_PAUSED)==2 and word(60)==0
    '144777dfab.3': 'Library rows (ipod-ui 4.4)',  # patch.py:10791 skey(O[KEY_NEXT]); assert word(60)==1  # the wheel picks in the menu
    'ace70b2003': 'Library rows (ipod-ui 4.4)',  # patch.py:10791 skey(O[KEY_NEXT]); assert word(60)==1  # the wheel picks in the menu
    '2dc4376a5f': 'Library rows (ipod-ui 4.4)',  # patch.py:10792 skey(O[KEY_PREV]); assert word(60)==0
    '8287c7e95e.2': 'Library rows (ipod-ui 4.4)',  # patch.py:10792 skey(O[KEY_PREV]); assert word(60)==0
    '00dddc04a1.4': 'Library rows (ipod-ui 4.4)',  # patch.py:10793 skey(O[KEY_BACK_BTN]); assert word(60)==1
    'ace70b2003.2': 'Library rows (ipod-ui 4.4)',  # patch.py:10793 skey(O[KEY_BACK_BTN]); assert word(60)==1
    '2dc4376a5f.2': 'Library rows (ipod-ui 4.4)',  # patch.py:10794 skey(O[KEY_FWD_BTN]); assert word(60)==0
    '2fa25e9f4c.5': 'Library rows (ipod-ui 4.4)',  # patch.py:10794 skey(O[KEY_FWD_BTN]); assert word(60)==0
    '2fa25e9f4c.6': 'Library rows (ipod-ui 4.4)',  # patch.py:10795 skey(O[KEY_FWD_BTN]); paint(); skey(O[KEY_CENTER]); m.advance(0)
    '60d2c2805f.13': 'Library rows (ipod-ui 4.4)',  # patch.py:10795 skey(O[KEY_FWD_BTN]); paint(); skey(O[KEY_CENTER]); m.advance(0)
    '7e0adf5d24.2': 'Library rows (ipod-ui 4.4)',  # patch.py:10795 skey(O[KEY_FWD_BTN]); paint(); skey(O[KEY_CENTER]); m.advance(0)
    '6c7b308867': 'Library rows (ipod-ui 4.4)',  # patch.py:10796 assert word(G_SCREEN)==0 and not frames(); passed()
    '7e86233542.18': 'Library rows (ipod-ui 4.4)',  # patch.py:10798 m.close(); assert m.get(payload_syms[g])==0 and not frames()
    '7fe72d327e.2': 'Library rows (ipod-ui 4.4)',  # patch.py:10799 sheet,chooser=games_open(); G=m.get(payload_syms[g]); rows=m.nodes[m.find(scroll
    'e39fa9664a.2': 'Library rows (ipod-ui 4.4)',  # patch.py:10799 sheet,chooser=games_open(); G=m.get(payload_syms[g]); rows=m.nodes[m.find(scroll
    '1a3e33b7bc.2': 'Library rows (ipod-ui 4.4)',  # patch.py:10800 pick(0); assert cells()==before
    '98152372b9': 'Library rows (ipod-ui 4.4)',  # patch.py:10800 pick(0); assert cells()==before
    '4df64b387d.8': 'Library rows (ipod-ui 4.4)',  # patch.py:10801 key(O[KEY_RETURN]); m.advance(0); pick(2); assert sol()[:-4]==before_sol[:-4]  #
    '6e49df19e4.2': 'Library rows (ipod-ui 4.4)',  # patch.py:10801 key(O[KEY_RETURN]); m.advance(0); pick(2); assert sol()[:-4]==before_sol[:-4]  #
    '74841e0c17': 'Library rows (ipod-ui 4.4)',  # patch.py:10801 key(O[KEY_RETURN]); m.advance(0); pick(2); assert sol()[:-4]==before_sol[:-4]  #
    'd1de3ca1f1': 'Library rows (ipod-ui 4.4)',  # patch.py:10804 m.byte(G+G_SOL+329,0)
    '9332ab3ede': 'Library rows (ipod-ui 4.4)',  # patch.py:10806 assert not saves; m.advance(2000); assert len(saves)==1 and bytes(m.files[/mnt/d
    '1a3e33b7bc.3': 'Library rows (ipod-ui 4.4)',  # patch.py:10807 key(O[KEY_RETURN]); m.advance(0); pick(0); key(O[KEY_RETURN]); m.advance(0); ass
    '4df64b387d.10': 'Library rows (ipod-ui 4.4)',  # patch.py:10807 key(O[KEY_RETURN]); m.advance(0); pick(0); key(O[KEY_RETURN]); m.advance(0); ass
    '4df64b387d.9': 'Library rows (ipod-ui 4.4)',  # patch.py:10807 key(O[KEY_RETURN]); m.advance(0); pick(0); key(O[KEY_RETURN]); m.advance(0); ass
    '6e49df19e4.3': 'Library rows (ipod-ui 4.4)',  # patch.py:10807 key(O[KEY_RETURN]); m.advance(0); pick(0); key(O[KEY_RETURN]); m.advance(0); ass
    '71bc7633bd': 'Library rows (ipod-ui 4.4)',  # patch.py:10807 key(O[KEY_RETURN]); m.advance(0); pick(0); key(O[KEY_RETURN]); m.advance(0); ass
    '012e45a329': 'Library rows (ipod-ui 4.4)',  # patch.py:10808 key(O[KEY_RETURN]); m.advance(0); pick(1); assert len(frames())==1
    '4df64b387d.11': 'Library rows (ipod-ui 4.4)',  # patch.py:10808 key(O[KEY_RETURN]); m.advance(0); pick(1); assert len(frames())==1
    'c54ae6e308.2': 'Library rows (ipod-ui 4.4)',  # patch.py:10808 key(O[KEY_RETURN]); m.advance(0); pick(1); assert len(frames())==1
    '7e86233542.19': 'Library rows (ipod-ui 4.4)',  # patch.py:10809 m.close(); assert m.get(payload_syms[g])==0 and not frames() and m.get(payload_s
    'e087294d76': 'Library rows (ipod-ui 4.4)',  # patch.py:10820 assert m.nodes[icon][image]==local_videos and m.nodes[label][text]==Videos and l
    'e426449b2e.2': 'Library rows (ipod-ui 4.4)',  # patch.py:10822 assert m.call(address=f,args=(ctx,m.event,0,0),gap=0)==0 and [m.text(c[1]) for c
    # hold Return to Now Playing (ipod-ui 4.4)
    'dfe4cdaacb': 'hold Return to Now Playing (ipod-ui 4.4)',  # patch.py:3181 for existing in (False,True):
    '06388513e1': 'hold Return to Now Playing (ipod-ui 4.4)',  # patch.py:3204 assert m.call(170,gap=0)==11
    # pull to search on iPod lists (ipod-ui 4.4)
    'b8767f31f8': 'pull to search on iPod lists (ipod-ui 4.4)',  # patch.py:3273 for page_name in (folder_page,localmusic_page,allmusic_page,radio_page):
    '22ec0013d1': 'pull to search on iPod lists (ipod-ui 4.4)',  # patch.py:3315 assert len(m.searches())==1 and m.get(w+O[TABLE_ROWS])==count and m.get(w+O[TABL
    '3791f9c29f': 'pull to search on iPod lists (ipod-ui 4.4)',  # patch.py:3320 for cancel in (below,horizontal,upward,midlist,outside,edge0,edge30,edge31
    'd1d94c7d11': 'pull to search on iPod lists (ipod-ui 4.4)',  # patch.py:3366 for distance in (7,48):
    'c2221ae651': 'pull to search on iPod lists (ipod-ui 4.4)',  # patch.py:3383 assert [c[1] for c in m.dispatched()]==[w,es[0]] and not m.clicks
    '830fe27fdf': 'pull to search on iPod lists (ipod-ui 4.4)',  # patch.py:3396 m=SearchNavigationMachine();w,es=m.page_list(6,height=240,name=localmusic_page);
    '909058c712.2': 'pull to search on iPod lists (ipod-ui 4.4)',  # patch.py:3397 m.order=[page];m.sync_order()
    'cdc3f66699': 'pull to search on iPod lists (ipod-ui 4.4)',  # patch.py:3400 assert m.nodes[m.top][name]==dialog/search_dialog and m.order[0]==page
    '909058c712.3': 'pull to search on iPod lists (ipod-ui 4.4)',  # patch.py:3404 m.order.remove(m.top);m.sync_order()
    # Home and the Q2 Pod page (ipod-ui 4.5)
    '4f7dbcae47': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:5371 m=Machine(); view,imgs=home_list(m); click_target(m,imgs[2])
    'f43abcdfc1': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:5371 m=Machine(); view,imgs=home_list(m); click_target(m,imgs[2])
    '3eaa96bb9c': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:5372 m.paint(view)
    'd652ea7b25': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:5373 assert m.selected(view)==0
    '47ba5647cc': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:5374 for i in range(1,7): assert m.call()==11 and m.selected(view)==i and m.get(view+
    '3c4013c003': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:5375 m.paint(view); assert m.rounded[0][rect]==(25,6*HOME_ROW+HOME_ROW//2-3,6,6)
    '3eaa96bb9c.2': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:5375 m.paint(view); assert m.rounded[0][rect]==(25,6*HOME_ROW+HOME_ROW//2-3,6,6)
    'c48d53e9b2': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:5376 assert m.call(gap=50)==11 and m.selected(view)==6   # bumped
    '7f02d59ef4': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:5377 assert m.call(gap=O[EDGE_PAUSE_MS])==11 and m.selected(view)==0
    '6585eb09c4': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:5378 assert m.call(O[KEY_PREV],gap=50)==11 and m.selected(view)==0   # bumped
    '328966b976': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:5379 assert m.call(O[KEY_PREV],gap=O[EDGE_PAUSE_MS])==11 and m.selected(view)==6
    '093f54b391': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:5380 for i in range(5,2,-1): assert m.call(O[KEY_PREV])==11 and m.selected(view)==i
    '11e3b719f5': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:5381 assert m.call(O[KEY_RETURN])==11 and m.selected(view)==0 and not destinations(m)
    '2fbfc74242': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:5382 for i in (1,2): assert m.call(gap=1000)==11 and m.selected(view)==i
    '707d9c9fa3': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:5383 assert not m.slides and m.confirm()==11 and m.dispatched()[0][1]==imgs[2]; passe
    '4f7dbcae47.2': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:5387 m=Machine(); view,imgs=home_list(m); bar=m.node(window,system_bar); m.word(syms[
    '3eaa96bb9c.3': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:5389 m.byte(syms[g_backlight_status],0); m.paint(view); assert m.selected(view)==-1 a
    '56298f1c9a': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:5389 m.byte(syms[g_backlight_status],0); m.paint(view); assert m.selected(view)==-1 a
    '6eaf9d30ac': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:5390 paint_bar(); assert (widget_invalidate_force,view) not in [c[:2] for c in m.call
    '27669fc1eb': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:5392 paint_bar(); assert (widget_invalidate_force,view) in [c[:2] for c in m.calls]
    '3eaa96bb9c.4': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:5393 m.paint(view); assert m.selected(view)==0 and m.rounded[0][rect]==(25,HOME_ROW//
    'f92f34df2f': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:5393 m.paint(view); assert m.selected(view)==0 and m.rounded[0][rect]==(25,HOME_ROW//
    '6eaf9d30ac.2': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:5394 paint_bar(); assert (widget_invalidate_force,view) not in [c[:2] for c in m.call
    '4f7dbcae47.3': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:5403 m=Machine(); view,imgs=home_list(m); click_target(m,imgs[2]); m.clip=(0,0,375,32
    'f43abcdfc1.2': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:5403 m=Machine(); view,imgs=home_list(m); click_target(m,imgs[2]); m.clip=(0,0,375,32
    '3eaa96bb9c.5': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:5404 m.paint(view)
    '1a714b6666': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:5407 assert m.rounded[0][rect]==(25,HOME_ROW//2-3,6,6) and m.icons==bar()
    '06323174d4': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:5409 m.call(); m.paint(view); assert m.selected(view)==1 and m.rounded[0][rect][1]>0 
    '3eaa96bb9c.6': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:5409 m.call(); m.paint(view); assert m.selected(view)==1 and m.rounded[0][rect][1]>0 
    '2f7883a1cf': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:5412 m.touch(); m.paint(view); assert m.icons==bar() and m.selected(view)==1; passed(
    '3eaa96bb9c.7': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:5412 m.touch(); m.paint(view); assert m.icons==bar() and m.selected(view)==1; passed(
    '3eaa96bb9c.8': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:5413 m.byte(syms[g_navbar_status],1); m.paint(view); assert not m.icons and not loade
    '4f7dbcae47.4': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:5415 m=Machine(); m.config[THEME]=1; view,imgs=home_list(m); click_target(m,imgs[2]);
    'f43abcdfc1.3': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:5415 m=Machine(); m.config[THEME]=1; view,imgs=home_list(m); click_target(m,imgs[2]);
    '3eaa96bb9c.9': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:5416 m.paint(view)
    'd9bf25c26c': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:5418 assert m.sel()==(0,0,HOME_LIST_W,HOME_ROW) and m.icons==cbar() and not m.rounded
    '1801d15492': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:5419 assert m.bands[1][4]==color_t(ACCENTS[0][0]) and loaded(m)==[list_into] and m.cl
    '3eaa96bb9c.10': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:5420 m.call(); m.paint(view); assert m.selected(view)==1 and m.sel()[1]>0 and m.icons
    '9089197301': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:5420 m.call(); m.paint(view); assert m.selected(view)==1 and m.sel()[1]>0 and m.icons
    'f519682145': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:6030 for theme in (0,1):
    '1903a0a4b3': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:6083 assert not [t for t in m.timers.values() if t[1]==payload_syms[home_drift]] and 
    'd30af9692f': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:6084 assert [signed(m.get(m.art+O[k])) for k in (W_X,W_Y,W_W,W_H)]==[SPLIT,0,PW,290];
    '4bf024fbb1': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:8315 m.art_size=(319,319); m.pixels.clear(); paint_home(); c=tex_of(319,319)
    '9dbe947d5c': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:8316 assert m.nodes[m.art][image]== and [signed(m.get(m.art+O[k])) for k in (W_X,W_Y,
    'f55ac103ea': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:8317 assert (c[u0],c[v0],c[rx],c[ry])==((290-PW)//2,0,29,29) and not drifts()
    '8cef526eea': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:8318 assert drawn()==framed(c,0) and (bitmap_lock_buffer_for_write,) in [x[:1] for x 
    '214b860d29': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:8319 assert drawn()==framed(c,0) and (bitmap_lock_buffer_for_write,) not in [x[:1] fo
    'd78c984174': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:8320 paint_home(); m.advance(0); assert len(drifts())==1  # it arms on the next paint
    '4bf4c098d9': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:8321 m.calls.clear(); m.advance(TICK); assert set(invalidated())=={(m.home,(SPLIT,0,P
    'fb9e654bc7': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:8322 assert drawn()==framed(c,TICK)!=framed(c,0)  # a tick moves it by a fraction of 
    '1b40e39f5c': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:8323 m.advance(1000-TICK); assert drawn()==framed(c,1000) and len(drifts())==1; passe
    '7684b0f340': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:8324 m.advance(TICK); instructions[0]=0; assert drawn()==framed(c,1000+TICK); frame_c
    '41e7830027': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:8326 tid=next(t for t,v in m.timers.items() if v[1]==payload_syms[home_drift]); m.tim
    '8fc3352f1c': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:8326 tid=next(t for t,v in m.timers.items() if v[1]==payload_syms[home_drift]); m.tim
    '20aa5be228': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:8327 m.advance(5000); t=1000+TICK+O[DRIFT_MAX_STEP_MS]; assert drawn()==framed(c,t); 
    '8856eca524': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:8330 for cover_up in (lambda: setattr(m,top,np),lambda: m.byte(syms[g_backlight_statu
    '20aa5be228.2': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:8343 paint_home(); assert drawn()==framed(c,t); paint_home(); assert len(drifts())==1
    'd78c984174.2': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:8343 paint_home(); assert drawn()==framed(c,t); paint_home(); assert len(drifts())==1
    'bb392fd3a1': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:8345 instructions[0]=0; paint_home(); filter_cost=instructions[0]; c=tex_of(638,638)
    '0dbb8cdbd9': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:8346 assert drawn()==framed(c,t) and len(drifts())==1
    '20aa5be228.3': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:8348 instructions[0]=0; paint_home(); big_cost=instructions[0]; m.u.hook_del(pan_coun
    'b04fddfbd0': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:8348 instructions[0]=0; paint_home(); big_cost=instructions[0]; m.u.hook_del(pan_coun
    'e71e90c7e3': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:8352 assert not drifts() and m.nodes[m.art][image].endswith(externpic.jpg) and m.get(
    '4f7dbcae47.5': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:8454 m=Machine(); view,imgs=home_list(m); begin(m,view)
    'a1af47494f': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:8455 labels=[m.nodes[m.get(img+O[W_PARENT])][children][0] for img in imgs]
    '3d53ed3386': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:8457 end(m,labels[0]); begin(m,labels[1]); assert style_color(m,0xffffffff)[1]==0xffa
    '198848f550': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:8833 home=asset_tree(m,HOME_PAGE)
    '272249ba26': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:8866 home_bounds(False); carousel(False)
    '466012b4b4': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:8866 home_bounds(False); carousel(False)
    '272249ba26.2': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:8868 home_bounds(True); carousel(False)
    '8f720362a9': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:8868 home_bounds(True); carousel(False)
    '84b943d9a0': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:8870 writes=click(1); assert [(w[0],m.text(w[2])) for w in writes]==[(2,HOME)] and te
    '927dc434cc.2': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:8870 writes=click(1); assert [(w[0],m.text(w[2])) for w in writes]==[(2,HOME)] and te
    '4fc57e7f8e': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:8871 carousel(True); assert not [c for c in m.calls if c[0]==image_manager_unload_all
    '272249ba26.3': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:8872 click(1); assert texts()[1]==Home: Split; home_bounds(False); carousel(False); p
    '35d85e600e': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:8872 click(1); assert texts()[1]==Home: Split; home_bounds(False); carousel(False); p
    '466012b4b4.2': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:8872 click(1); assert texts()[1]==Home: Split; home_bounds(False); carousel(False); p
    '715ae6bcff': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:8872 click(1); assert texts()[1]==Home: Split; home_bounds(False); carousel(False); p
    '4fc57e7f8e.2': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:8908 click(1); assert texts()[1]==Home: Full; home_bounds(True,True); click(1); carou
    '715ae6bcff.2': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:8908 click(1); assert texts()[1]==Home: Full; home_bounds(True,True); click(1); carou
    '715ae6bcff.3': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:8908 click(1); assert texts()[1]==Home: Full; home_bounds(True,True); click(1); carou
    'c0c3106d02': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:8908 click(1); assert texts()[1]==Home: Full; home_bounds(True,True); click(1); carou
    'fd1c55d76c': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:8908 click(1); assert texts()[1]==Home: Full; home_bounds(True,True); click(1); carou
    '272249ba26.4': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:8909 click(1); home_bounds(False,True); carousel(False); passed()
    '715ae6bcff.4': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:8909 click(1); home_bounds(False,True); carousel(False); passed()
    'baa6580069.2': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:8909 click(1); home_bounds(False,True); carousel(False); passed()
    '4f7dbcae47.6': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:9243 m=Machine(); view,imgs=home_list(m); click_target(m,imgs[2]); m.paint(view)
    'f43abcdfc1.4': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:9243 m=Machine(); view,imgs=home_list(m); click_target(m,imgs[2]); m.paint(view)
    '99f82b57ad': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:9246 assert m.confirm()==11 and m.dispatched()[0][1]==imgs[4]; passed()
    '09bc2f5c69': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:9287 m,view=home_machine(); got=[]
    '09bc2f5c69.2': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:9294 m,view=home_machine()
    '09bc2f5c69.3': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:9301 m,view=home_machine(); seen=[]
    '0ea534a834': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:9337 m,view=home_machine(tone=0)
    '09bc2f5c69.4': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:9339 m,view=home_machine()
    'f08e7ea68f': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:9621 if is_m1plus: q2pod_page()  # its own names: the Librarys machine (m, top) is us
    '0f3397c13c': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:9716 if is_m1plus: q2pod_real_grid()
    'ff99c8ed8a': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:9819 home_carousel()
    '6557576207': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:9820 for full in (0,1):
    '9bacd6a492': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:10442 border(tiles[0]); assert m.bands[-1][:5]==((O[PH_TILE_W]-O[PH_THUMB_W])//2,(O[PH
    'edbce3467b': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:10453 border(tiles[2]); assert m.bands[-1][4]==O[PH_GREY]
    # boot resume to Home (ipod-ui 4.5)
    '6bd274c37f': 'boot resume to Home (ipod-ui 4.5)',  # patch.py:4657 assert struct.unpack_from(<I,demo,fileoff(demo,0x523de0))[0]==jal(boot)
    'ca3db14059': 'boot resume to Home (ipod-ui 4.5)',  # patch.py:4658 for car,cls,want in ((0,1,[(0x5550,4,1,3)]),(0,0xff,[]),(1,0xf003,[])):
    # Now Playing (ipod-ui 4.6)
    'ed2910cddb': 'Now Playing (ipod-ui 4.6)',  # patch.py:6102 assert shown()==[2 of 3,Album 1,-2:05]; passed()
    'afd9cd9841': 'Now Playing (ipod-ui 4.6)',  # patch.py:6104 m.nodes[slider][value]=101; assert repaint()==[label_ipod_remain] and shown()[2]
    '92fb5f57fe': 'Now Playing (ipod-ui 4.6)',  # patch.py:6115 for mx,v,want in ((3725,0,-1:02:05),(3600,0,-1:00:00),(3599,0,-59:59),(90,90,-0:
    '64d0da19d1': 'Now Playing (ipod-ui 4.6)',  # patch.py:6140 cover_is(b/p/C,2); assert art_pass()==(reload,file:///tmp/externpic.jpg) and art
    'e3949fc4b3': 'Now Playing (ipod-ui 4.6)',  # patch.py:6141 m.word(O[MCL_POS],1); cover_is(b/p/B,1); assert art_pass()==(reload,file:///tmp/
    '88ba9daedb': 'Now Playing (ipod-ui 4.6)',  # patch.py:6142 m.word(O[MCL_POS],2); cover_is(b/p/C,3); assert art_pass()==(reload,play_default
    'e31731b50f': 'Now Playing (ipod-ui 4.6)',  # patch.py:6144 m.byte(syms[g_backlight_status],1); assert art_pass()==(reload,file:///tmp/exter
    'c040749ebb': 'Now Playing (ipod-ui 4.6)',  # patch.py:6386 assert step(m)==11 and m.nodes[m.slider][value]==105 and m.nodes[m.elapsed][text
    '5bb8daf98f': 'Now Playing (ipod-ui 4.6)',  # patch.py:6387 assert m.nodes[m.remain][text]==-2:00
    '1aa8589c73': 'Now Playing (ipod-ui 4.6)',  # patch.py:6388 assert step(m,gap=1500)==11 and m.nodes[m.slider][value]==110 and m.nodes[m.elap
    '262157c160': 'Now Playing (ipod-ui 4.6)',  # patch.py:6389 assert m.nodes[m.remain][text]==-1:55
    '196370eaa5': 'Now Playing (ipod-ui 4.6)',  # patch.py:6390 step(m,O[SCRUB_MS]-100,wait=True); assert m.seeks==[] and m.nodes[m.slider][valu
    '765c8ca948': 'Now Playing (ipod-ui 4.6)',  # patch.py:6392 for _ in range(12): assert step(m,gap=20)==11
    '984bdeb087': 'Now Playing (ipod-ui 4.6)',  # patch.py:6393 assert m.nodes[m.slider][value]-110>12*O[SCRUB_STEP] and m.seeks==[]; passed()
    '379418464e': 'Now Playing (ipod-ui 4.6)',  # patch.py:6395 for key,end in ((O[KEY_NEXT],225),(O[KEY_PREV],0)):
    'eb38459dd6': 'Now Playing (ipod-ui 4.6)',  # patch.py:6398 assert step(m,gap=300)==11 and m.nodes[m.slider][value]==5 and m.seeks==[]; pass
    '9a89e63f61': 'Now Playing (ipod-ui 4.6)',  # patch.py:6400 centre(m,50); step(m,O[SCRUB_MS],wait=True); ended(m,[5]); passed()
    '8101c7dd73': 'Now Playing (ipod-ui 4.6)',  # patch.py:6408 assert did(m,mclSetSeek)==[135] and not m.seeks and not did(m,mclSetResume)
    '74311a4217': 'Now Playing (ipod-ui 4.6)',  # patch.py:6409 step(m,O[SCRUB_MS]+5000,wait=True); assert not m.seeks and not m.starts and m.no
    'e8a1a98ba1': 'Now Playing (ipod-ui 4.6)',  # patch.py:6412 assert not m.starts and m.nodes[m.slider][value]==105 and m.timers
    '208a92803b': 'Now Playing (ipod-ui 4.6)',  # patch.py:6413 m.word(PLAY_STATUS,2); step(m,1000,wait=True); assert not m.starts
    'bf0954d4e1': 'Now Playing (ipod-ui 4.6)',  # patch.py:6414 step(m,1500,wait=True); assert m.starts==[m.win] and not m.timers; passed()
    '838749eac8': 'Now Playing (ipod-ui 4.6)',  # patch.py:6422 centre(m); step(m); centre(m,50); assert did(m,mclSetSeek)==[105]
    '83309cf382': 'Now Playing (ipod-ui 4.6)',  # patch.py:6423 reopen(m); assert m.nodes[m.slider][value]==105 and m.nodes[m.elapsed][text]==1:
    'a216310d6b': 'Now Playing (ipod-ui 4.6)',  # patch.py:6424 assert did(m,playing_timer_clear)==[m.win]; step(m,5000,wait=True); assert not m
    '4d6ae59f1b': 'Now Playing (ipod-ui 4.6)',  # patch.py:6425 centre(m); step(m); assert m.nodes[m.slider][value]==110; passed()
    '1ec8a51eee': 'Now Playing (ipod-ui 4.6)',  # patch.py:6430 step(m,O[SCRUB_MS]-1,wait=True); assert m.seeks==[] and not m.starts
    '1acfe38d73': 'Now Playing (ipod-ui 4.6)',  # patch.py:6431 step(m,1,wait=True); assert m.seeks==[105] and not m.starts  # settle_poll resta
    '5d550e5acc': 'Now Playing (ipod-ui 4.6)',  # patch.py:6432 step(m,O[SCRUB_MS],wait=True); ended(m,[105]); assert m.nodes[m.slider][value]==
    'd93b3914e6': 'Now Playing (ipod-ui 4.6)',  # patch.py:6432 step(m,O[SCRUB_MS],wait=True); ended(m,[105]); assert m.nodes[m.slider][value]==
    '5d550e5acc.2': 'Now Playing (ipod-ui 4.6)',  # patch.py:6435 assert m.nodes[m.slider][value]==105; centre(m,50); step(m,O[SCRUB_MS],wait=True
    'd93b3914e6.2': 'Now Playing (ipod-ui 4.6)',  # patch.py:6435 assert m.nodes[m.slider][value]==105; centre(m,50); step(m,O[SCRUB_MS],wait=True
    'd9b211abf8': 'Now Playing (ipod-ui 4.6)',  # patch.py:6437 for end in (centre,timeout,bound):
    'ee34a125f0': 'Now Playing (ipod-ui 4.6)',  # patch.py:6444 for end in (centre,return,touch):
    'bfd6e55727': 'Now Playing (ipod-ui 4.6)',  # patch.py:6459 for presses in (1,2):
    '1acfe38d73.2': 'Now Playing (ipod-ui 4.6)',  # patch.py:6468 m.top=m.node(window,home_page); step(m); assert m.seeks==[105] and not m.starts
    'dc662aa100': 'Now Playing (ipod-ui 4.6)',  # patch.py:6469 step(m,O[SCRUB_MS],wait=True); assert m.seeks==[105] and m.starts==[m.win] and n
    'b45a784858': 'Now Playing (ipod-ui 4.6)',  # patch.py:6472 assert m.seeks==[] and not m.starts and not m.timers; passed()
    '1dc9436f15': 'Now Playing (ipod-ui 4.6)',  # patch.py:6475 for end in (tick,timeout,return):
    'e2c6cec663': 'Now Playing (ipod-ui 4.6)',  # patch.py:6517 for kw in ({page:0},{size:0},{lines:0}):
    '14b0be8b0c': 'Now Playing (ipod-ui 4.6)',  # patch.py:6527 m=lyric_page(); assert loop(m)==0 and raw(m)==1; m.calls=[]
    'b2cb33d0d6': 'Now Playing (ipod-ui 4.6)',  # patch.py:6527 m=lyric_page(); assert loop(m)==0 and raw(m)==1; m.calls=[]
    '2d450a38f0': 'Now Playing (ipod-ui 4.6)',  # patch.py:6528 loop(m,-28); assert settle(m)[-1]==O[BUMP_PX] and follow(m,0)==O[BUMP_PX]
    '33e411d7d7': 'Now Playing (ipod-ui 4.6)',  # patch.py:6528 loop(m,-28); assert settle(m)[-1]==O[BUMP_PX] and follow(m,0)==O[BUMP_PX]
    'ef4b16c7af': 'Now Playing (ipod-ui 4.6)',  # patch.py:6529 assert (reset_poweroptions_timer,1,1,1) in [c[:4] for c in m.calls]  # the scree
    'b6af0e1f46': 'Now Playing (ipod-ui 4.6)',  # patch.py:6530 m.word(payload_syms[wheel_held],0); assert settle(m)[-1]==0; m.word(payload_syms
    '5810214f81': 'Now Playing (ipod-ui 4.6)',  # patch.py:6531 follow(m,20); assert settle(m)[-1]==20; m.advance(O[LYRIC_PUSH_MS])
    'b5e3f6b84f': 'Now Playing (ipod-ui 4.6)',  # patch.py:6531 follow(m,20); assert settle(m)[-1]==20; m.advance(O[LYRIC_PUSH_MS])
    '790d5863b0': 'Now Playing (ipod-ui 4.6)',  # patch.py:6532 loop(m,28); assert settle(m)[-1]==20-O[BUMP_PX] and follow(m,20)==20-O[BUMP_PX];
    'ff1b9fa985': 'Now Playing (ipod-ui 4.6)',  # patch.py:6532 loop(m,28); assert settle(m)[-1]==20-O[BUMP_PX] and follow(m,20)==20-O[BUMP_PX];
    '14b0be8b0c.2': 'Now Playing (ipod-ui 4.6)',  # patch.py:6534 m=lyric_page(); loop(m); loop(m,-28); m.advance(500); loop(m,-28)
    '33e411d7d7.2': 'Now Playing (ipod-ui 4.6)',  # patch.py:6534 m=lyric_page(); loop(m); loop(m,-28); m.advance(500); loop(m,-28)
    '33e411d7d7.3': 'Now Playing (ipod-ui 4.6)',  # patch.py:6534 m=lyric_page(); loop(m); loop(m,-28); m.advance(500); loop(m,-28)
    'b1c92aab98': 'Now Playing (ipod-ui 4.6)',  # patch.py:6534 m=lyric_page(); loop(m); loop(m,-28); m.advance(500); loop(m,-28)
    '66b2f4c87c': 'Now Playing (ipod-ui 4.6)',  # patch.py:6535 assert settle(m)[-1]==26; m.word(payload_syms[wheel_held],0); assert settle(m)[-
    '8d912b0fb3': 'Now Playing (ipod-ui 4.6)',  # patch.py:6535 assert settle(m)[-1]==26; m.word(payload_syms[wheel_held],0); assert settle(m)[-
    '14b0be8b0c.3': 'Now Playing (ipod-ui 4.6)',  # patch.py:6537 m=lyric_page(); assert loop(m)==0 and raw(m)==1; hold(m); m.calls=[]
    'b2cb33d0d6.2': 'Now Playing (ipod-ui 4.6)',  # patch.py:6537 m=lyric_page(); assert loop(m)==0 and raw(m)==1; hold(m); m.calls=[]
    'bb6c2c76d0': 'Now Playing (ipod-ui 4.6)',  # patch.py:6537 m=lyric_page(); assert loop(m)==0 and raw(m)==1; hold(m); m.calls=[]
    '09e0ba0cc6': 'Now Playing (ipod-ui 4.6)',  # patch.py:6538 ys=[loop(m,-28)]+settle(m); steps=[b-a for a,b in zip([0]+ys,ys)]
    '3e40276733': 'Now Playing (ipod-ui 4.6)',  # patch.py:6538 ys=[loop(m,-28)]+settle(m); steps=[b-a for a,b in zip([0]+ys,ys)]
    '8e7decd10c': 'Now Playing (ipod-ui 4.6)',  # patch.py:6539 assert ys[-1]==20 and 0<ys[0]<5 and all(0<=s<=4 for s in steps) and steps[-1]==0
    'ef4b16c7af.2': 'Now Playing (ipod-ui 4.6)',  # patch.py:6540 assert (reset_poweroptions_timer,1,1,1) in [c[:4] for c in m.calls]  # the scree
    '46a1858c69': 'Now Playing (ipod-ui 4.6)',  # patch.py:6541 assert not did(m,playing_timer_clear) and not did(m,sleep_ms); passed()  # nor d
    'ab60e9f310': 'Now Playing (ipod-ui 4.6)',  # patch.py:6543 for _ in range(3): loop(m,-1)
    '2df204679d': 'Now Playing (ipod-ui 4.6)',  # patch.py:6544 settle(m); assert y(m)==22; passed()
    'f805f3f1b6': 'Now Playing (ipod-ui 4.6)',  # patch.py:6544 settle(m); assert y(m)==22; passed()
    '0ca817ce8c': 'Now Playing (ipod-ui 4.6)',  # patch.py:6546 for _ in range(60): loop(m,-12)
    '84f07b87cf': 'Now Playing (ipod-ui 4.6)',  # patch.py:6547 assert settle(m)[-1]==110 and m.get(m.lrc+O[VIEW_CONTENT_H])==288; passed()
    '866c26dd74': 'Now Playing (ipod-ui 4.6)',  # patch.py:6549 for _ in range(60): loop(m,12)
    'b6af0e1f46.2': 'Now Playing (ipod-ui 4.6)',  # patch.py:6550 assert settle(m)[-1]==0; passed()
    '34c306a7cb': 'Now Playing (ipod-ui 4.6)',  # patch.py:6552 m=lyric_page(config={WHEELSENSITIVITY:100}); loop(m); hold(m); loop(m,-14); asse
    '6d4970ef6a': 'Now Playing (ipod-ui 4.6)',  # patch.py:6552 m=lyric_page(config={WHEELSENSITIVITY:100}); loop(m); hold(m); loop(m,-14); asse
    'b1c92aab98.2': 'Now Playing (ipod-ui 4.6)',  # patch.py:6552 m=lyric_page(config={WHEELSENSITIVITY:100}); loop(m); hold(m); loop(m,-14); asse
    'b5e3f6b84f.2': 'Now Playing (ipod-ui 4.6)',  # patch.py:6552 m=lyric_page(config={WHEELSENSITIVITY:100}); loop(m); hold(m); loop(m,-14); asse
    'bb6c2c76d0.2': 'Now Playing (ipod-ui 4.6)',  # patch.py:6552 m=lyric_page(config={WHEELSENSITIVITY:100}); loop(m); hold(m); loop(m,-14); asse
    '14b0be8b0c.4': 'Now Playing (ipod-ui 4.6)',  # patch.py:6554 m=lyric_page(); loop(m); loop(m,-56); settle(m); assert y(m)==40
    '2df204679d.2': 'Now Playing (ipod-ui 4.6)',  # patch.py:6554 m=lyric_page(); loop(m); loop(m,-56); settle(m); assert y(m)==40
    '31c2c2ba32': 'Now Playing (ipod-ui 4.6)',  # patch.py:6554 m=lyric_page(); loop(m); loop(m,-56); settle(m); assert y(m)==40
    '8dc2f66aa4': 'Now Playing (ipod-ui 4.6)',  # patch.py:6554 m=lyric_page(); loop(m); loop(m,-56); settle(m); assert y(m)==40
    'b1c92aab98.3': 'Now Playing (ipod-ui 4.6)',  # patch.py:6554 m=lyric_page(); loop(m); loop(m,-56); settle(m); assert y(m)==40
    '6a61f1355f': 'Now Playing (ipod-ui 4.6)',  # patch.py:6555 assert follow(m,0)==40; m.advance(O[SCRUB_MS]+1000); assert settle(m)[-1]==40 an
    '8bb44b59c8': 'Now Playing (ipod-ui 4.6)',  # patch.py:6555 assert follow(m,0)==40; m.advance(O[SCRUB_MS]+1000); assert settle(m)[-1]==40 an
    '40bead0886': 'Now Playing (ipod-ui 4.6)',  # patch.py:6556 assert not did(m,playing_timer_clear) and not m.starts; passed()
    '53fab8b81b': 'Now Playing (ipod-ui 4.6)',  # patch.py:6559 m.nodes[m.slide][value]=0; loop(m); assert raw(m)==0 and follow(m,70)==70
    '76bd6c6315': 'Now Playing (ipod-ui 4.6)',  # patch.py:6559 m.nodes[m.slide][value]=0; loop(m); assert raw(m)==0 and follow(m,70)==70
    'b1c92aab98.4': 'Now Playing (ipod-ui 4.6)',  # patch.py:6559 m.nodes[m.slide][value]=0; loop(m); assert raw(m)==0 and follow(m,70)==70
    '968ad0041e': 'Now Playing (ipod-ui 4.6)',  # patch.py:6560 m.nodes[m.slide][value]=1; loop(m); assert raw(m)==1 and follow(m,90)==70
    'b1c92aab98.5': 'Now Playing (ipod-ui 4.6)',  # patch.py:6560 m.nodes[m.slide][value]=1; loop(m); assert raw(m)==1 and follow(m,90)==70
    'f19fc2ec4d': 'Now Playing (ipod-ui 4.6)',  # patch.py:6560 m.nodes[m.slide][value]=1; loop(m); assert raw(m)==1 and follow(m,90)==70
    '29670a53c2': 'Now Playing (ipod-ui 4.6)',  # patch.py:6561 ys=settle(m); assert ys[-1]==90 and ys[0]<90,ys; passed()
    'a8b1d4e2b0': 'Now Playing (ipod-ui 4.6)',  # patch.py:6561 ys=settle(m); assert ys[-1]==90 and ys[0]<90,ys; passed()
    '9341c2472a': 'Now Playing (ipod-ui 4.6)',  # patch.py:6563 for off in (0,1):
    '14b0be8b0c.5': 'Now Playing (ipod-ui 4.6)',  # patch.py:6569 m=lyric_page(); loop(m); loop(m,-56); settle(m); m.word(O[MCL_POS],1); assert lo
    '2df204679d.3': 'Now Playing (ipod-ui 4.6)',  # patch.py:6569 m=lyric_page(); loop(m); loop(m,-56); settle(m); m.word(O[MCL_POS],1); assert lo
    '2eadecd1b7': 'Now Playing (ipod-ui 4.6)',  # patch.py:6569 m=lyric_page(); loop(m); loop(m,-56); settle(m); m.word(O[MCL_POS],1); assert lo
    '31c2c2ba32.2': 'Now Playing (ipod-ui 4.6)',  # patch.py:6569 m=lyric_page(); loop(m); loop(m,-56); settle(m); m.word(O[MCL_POS],1); assert lo
    'b1c92aab98.6': 'Now Playing (ipod-ui 4.6)',  # patch.py:6569 m=lyric_page(); loop(m); loop(m,-56); settle(m); m.word(O[MCL_POS],1); assert lo
    '14b0be8b0c.6': 'Now Playing (ipod-ui 4.6)',  # patch.py:6573 m=lyric_page(); m.handlers[0x529f0c]=stock_lyric_rows; loop(m); loop(m,-56); set
    '2df204679d.4': 'Now Playing (ipod-ui 4.6)',  # patch.py:6573 m=lyric_page(); m.handlers[0x529f0c]=stock_lyric_rows; loop(m); loop(m,-56); set
    '31c2c2ba32.3': 'Now Playing (ipod-ui 4.6)',  # patch.py:6573 m=lyric_page(); m.handlers[0x529f0c]=stock_lyric_rows; loop(m); loop(m,-56); set
    'b1c92aab98.7': 'Now Playing (ipod-ui 4.6)',  # patch.py:6573 m=lyric_page(); m.handlers[0x529f0c]=stock_lyric_rows; loop(m); loop(m,-56); set
    '801f4c1661': 'Now Playing (ipod-ui 4.6)',  # patch.py:6574 assert rows(m)==40 and follow(m,0)==40; passed()
    '037f338d97': 'Now Playing (ipod-ui 4.6)',  # patch.py:6575 m.word(O[MCL_POS],2); m.word(m.lrc+O[SCROLL_Y],60); assert rows(m)==0 and loop(m
    '20a2be18af': 'Now Playing (ipod-ui 4.6)',  # patch.py:6575 m.word(O[MCL_POS],2); m.word(m.lrc+O[SCROLL_Y],60); assert rows(m)==0 and loop(m
    '5810214f81.2': 'Now Playing (ipod-ui 4.6)',  # patch.py:6576 follow(m,20); assert settle(m)[-1]==20; passed()  # the follow is back
    'b5e3f6b84f.3': 'Now Playing (ipod-ui 4.6)',  # patch.py:6576 follow(m,20); assert settle(m)[-1]==20; passed()  # the follow is back
    '39fd93c268': 'Now Playing (ipod-ui 4.6)',  # patch.py:6579 m=lyric_page(page=0); loop(m); m.pressed=1; loop(m); m.nodes[m.slide][value]=1; 
    'b1c92aab98.10': 'Now Playing (ipod-ui 4.6)',  # patch.py:6579 m=lyric_page(page=0); loop(m); m.pressed=1; loop(m); m.nodes[m.slide][value]=1; 
    'b1c92aab98.8': 'Now Playing (ipod-ui 4.6)',  # patch.py:6579 m=lyric_page(page=0); loop(m); m.pressed=1; loop(m); m.nodes[m.slide][value]=1; 
    'b1c92aab98.9': 'Now Playing (ipod-ui 4.6)',  # patch.py:6579 m=lyric_page(page=0); loop(m); m.pressed=1; loop(m); m.nodes[m.slide][value]=1; 
    'f19fc2ec4d.2': 'Now Playing (ipod-ui 4.6)',  # patch.py:6579 m=lyric_page(page=0); loop(m); m.pressed=1; loop(m); m.nodes[m.slide][value]=1; 
    '20a2be18af.2': 'Now Playing (ipod-ui 4.6)',  # patch.py:6580 m.word(m.lrc+O[SCROLL_Y],60); loop(m); m.pressed=0; loop(m); follow(m,0); assert
    'a8da2bfe8f': 'Now Playing (ipod-ui 4.6)',  # patch.py:6580 m.word(m.lrc+O[SCROLL_Y],60); loop(m); m.pressed=0; loop(m); follow(m,0); assert
    'b1c92aab98.11': 'Now Playing (ipod-ui 4.6)',  # patch.py:6580 m.word(m.lrc+O[SCROLL_Y],60); loop(m); m.pressed=0; loop(m); follow(m,0); assert
    'b1c92aab98.12': 'Now Playing (ipod-ui 4.6)',  # patch.py:6580 m.word(m.lrc+O[SCROLL_Y],60); loop(m); m.pressed=0; loop(m); follow(m,0); assert
    'b6af0e1f46.3': 'Now Playing (ipod-ui 4.6)',  # patch.py:6580 m.word(m.lrc+O[SCROLL_Y],60); loop(m); m.pressed=0; loop(m); follow(m,0); assert
    '0e9008d0c7': 'Now Playing (ipod-ui 4.6)',  # patch.py:6581 m=lyric_page(); loop(m); a=m.alloc(0x80); m.word(m.lrc+O[VIEW_ANIMATOR],a); m.pr
    '14b0be8b0c.7': 'Now Playing (ipod-ui 4.6)',  # patch.py:6581 m=lyric_page(); loop(m); a=m.alloc(0x80); m.word(m.lrc+O[VIEW_ANIMATOR],a); m.pr
    'b1c92aab98.13': 'Now Playing (ipod-ui 4.6)',  # patch.py:6581 m=lyric_page(); loop(m); a=m.alloc(0x80); m.word(m.lrc+O[VIEW_ANIMATOR],a); m.pr
    'b1c92aab98.14': 'Now Playing (ipod-ui 4.6)',  # patch.py:6581 m=lyric_page(); loop(m); a=m.alloc(0x80); m.word(m.lrc+O[VIEW_ANIMATOR],a); m.pr
    'bc3398d579': 'Now Playing (ipod-ui 4.6)',  # patch.py:6582 assert m.get(m.lrc+O[VIEW_ANIMATOR])==0 and (widget_animator_destroy,a) in [c[:2
    '14b0be8b0c.8': 'Now Playing (ipod-ui 4.6)',  # patch.py:6584 m=lyric_page(); m.handlers[0x529f0c]=stock_lyric_rows; loop(m); loop(m,-56); set
    '2df204679d.5': 'Now Playing (ipod-ui 4.6)',  # patch.py:6584 m=lyric_page(); m.handlers[0x529f0c]=stock_lyric_rows; loop(m); loop(m,-56); set
    '31c2c2ba32.4': 'Now Playing (ipod-ui 4.6)',  # patch.py:6584 m=lyric_page(); m.handlers[0x529f0c]=stock_lyric_rows; loop(m); loop(m,-56); set
    'b1c92aab98.15': 'Now Playing (ipod-ui 4.6)',  # patch.py:6584 m=lyric_page(); m.handlers[0x529f0c]=stock_lyric_rows; loop(m); loop(m,-56); set
    '53fab8b81b.2': 'Now Playing (ipod-ui 4.6)',  # patch.py:6585 m.nodes[m.slide][value]=0; loop(m); assert follow(m,20)==20  # off the page: sto
    '69eb271416': 'Now Playing (ipod-ui 4.6)',  # patch.py:6585 m.nodes[m.slide][value]=0; loop(m); assert follow(m,20)==20  # off the page: sto
    'b1c92aab98.16': 'Now Playing (ipod-ui 4.6)',  # patch.py:6585 m.nodes[m.slide][value]=0; loop(m); assert follow(m,20)==20  # off the page: sto
    '504ef5d85c': 'Now Playing (ipod-ui 4.6)',  # patch.py:6586 m.byte(syms[g_backlight_status],0); loop(m); m.word(O[MCL_POS],2); assert loop(m
    'b1c92aab98.17': 'Now Playing (ipod-ui 4.6)',  # patch.py:6586 m.byte(syms[g_backlight_status],0); loop(m); m.word(O[MCL_POS],2); assert loop(m
    '20a2be18af.3': 'Now Playing (ipod-ui 4.6)',  # patch.py:6587 m.word(m.lrc+O[SCROLL_Y],60); assert rows(m)==0  # a stale follow, then the new 
    'b750c0fe2e': 'Now Playing (ipod-ui 4.6)',  # patch.py:6587 m.word(m.lrc+O[SCROLL_Y],60); assert rows(m)==0  # a stale follow, then the new 
    'b1c92aab98.18': 'Now Playing (ipod-ui 4.6)',  # patch.py:6588 m.byte(syms[g_backlight_status],1); loop(m); m.pressed=1; loop(m); m.nodes[m.sli
    'b1c92aab98.19': 'Now Playing (ipod-ui 4.6)',  # patch.py:6588 m.byte(syms[g_backlight_status],1); loop(m); m.pressed=1; loop(m); m.nodes[m.sli
    'b1c92aab98.20': 'Now Playing (ipod-ui 4.6)',  # patch.py:6588 m.byte(syms[g_backlight_status],1); loop(m); m.pressed=1; loop(m); m.nodes[m.sli
    'f19fc2ec4d.3': 'Now Playing (ipod-ui 4.6)',  # patch.py:6588 m.byte(syms[g_backlight_status],1); loop(m); m.pressed=1; loop(m); m.nodes[m.sli
    'b1c92aab98.21': 'Now Playing (ipod-ui 4.6)',  # patch.py:6589 m.word(m.lrc+O[SCROLL_Y],20); loop(m); m.pressed=0; loop(m)
    'b1c92aab98.22': 'Now Playing (ipod-ui 4.6)',  # patch.py:6589 m.word(m.lrc+O[SCROLL_Y],20); loop(m); m.pressed=0; loop(m)
    'fba181f823': 'Now Playing (ipod-ui 4.6)',  # patch.py:6589 m.word(m.lrc+O[SCROLL_Y],20); loop(m); m.pressed=0; loop(m)
    'a8da2bfe8f.2': 'Now Playing (ipod-ui 4.6)',  # patch.py:6590 follow(m,0); assert settle(m)[-1]==0; passed()
    'b6af0e1f46.4': 'Now Playing (ipod-ui 4.6)',  # patch.py:6590 follow(m,0); assert settle(m)[-1]==0; passed()
    '14b0be8b0c.9': 'Now Playing (ipod-ui 4.6)',  # patch.py:6592 m=lyric_page(); loop(m); hold(m); loop(m,-36); assert settle(m,200)[-1]==26  # t
    'ad03b1ffac': 'Now Playing (ipod-ui 4.6)',  # patch.py:6592 m=lyric_page(); loop(m); hold(m); loop(m,-36); assert settle(m,200)[-1]==26  # t
    'b1c92aab98.23': 'Now Playing (ipod-ui 4.6)',  # patch.py:6592 m=lyric_page(); loop(m); hold(m); loop(m,-36); assert settle(m,200)[-1]==26  # t
    'bb6c2c76d0.3': 'Now Playing (ipod-ui 4.6)',  # patch.py:6592 m=lyric_page(); loop(m); hold(m); loop(m,-36); assert settle(m,200)[-1]==26  # t
    'cacd8b8fb7': 'Now Playing (ipod-ui 4.6)',  # patch.py:6592 m=lyric_page(); loop(m); hold(m); loop(m,-36); assert settle(m,200)[-1]==26  # t
    '29670a53c2.2': 'Now Playing (ipod-ui 4.6)',  # patch.py:6593 m.word(payload_syms[wheel_held],0); ys=settle(m); assert ys[-1]==20 and ys[0]>20
    'dcd71d1411': 'Now Playing (ipod-ui 4.6)',  # patch.py:6593 m.word(payload_syms[wheel_held],0); ys=settle(m); assert ys[-1]==20 and ys[0]>20
    '14f083728c': 'Now Playing (ipod-ui 4.6)',  # patch.py:6594 m.word(payload_syms[wheel_held],1); loop(m,-50); assert settle(m)[-1]==56  # nea
    'b8286a7454': 'Now Playing (ipod-ui 4.6)',  # patch.py:6594 m.word(payload_syms[wheel_held],1); loop(m,-50); assert settle(m)[-1]==56  # nea
    'e94ad641c3': 'Now Playing (ipod-ui 4.6)',  # patch.py:6595 m.word(payload_syms[wheel_held],0); assert settle(m)[-1]==70 and follow(m,0)==70
    '14b0be8b0c.10': 'Now Playing (ipod-ui 4.6)',  # patch.py:6597 m=lyric_page(); loop(m); hold(m); loop(m,-36); m.word(payload_syms[wheel_held],0
    'ad03b1ffac.2': 'Now Playing (ipod-ui 4.6)',  # patch.py:6597 m=lyric_page(); loop(m); hold(m); loop(m,-36); m.word(payload_syms[wheel_held],0
    'b1c92aab98.24': 'Now Playing (ipod-ui 4.6)',  # patch.py:6597 m=lyric_page(); loop(m); hold(m); loop(m,-36); m.word(payload_syms[wheel_held],0
    'b5e3f6b84f.4': 'Now Playing (ipod-ui 4.6)',  # patch.py:6597 m=lyric_page(); loop(m); hold(m); loop(m,-36); m.word(payload_syms[wheel_held],0
    'bb6c2c76d0.4': 'Now Playing (ipod-ui 4.6)',  # patch.py:6597 m=lyric_page(); loop(m); hold(m); loop(m,-36); m.word(payload_syms[wheel_held],0
    '187abcda7f': 'Now Playing (ipod-ui 4.6)',  # patch.py:6598 m.word(payload_syms[wheel_held],1); m.word(m.lrc+O[SCROLL_Y],30); loop(m); m.wor
    'b1c92aab98.25': 'Now Playing (ipod-ui 4.6)',  # patch.py:6598 m.word(payload_syms[wheel_held],1); m.word(m.lrc+O[SCROLL_Y],30); loop(m); m.wor
    '3470cf7a54': 'Now Playing (ipod-ui 4.6)',  # patch.py:6599 assert settle(m)[-1]==30; passed()  # not the wheels doing: no snap
    '35111b43eb': 'Now Playing (ipod-ui 4.6)',  # patch.py:6607 for off,on in ((other,back),(dark,lambda m: dark(m,1)),(touch,lambda m: touch(m,
    '14b0be8b0c.11': 'Now Playing (ipod-ui 4.6)',  # patch.py:6614 m=lyric_page(); loop(m); m.pressed=1; loop(m); m.word(m.lrc+O[SCROLL_Y],40)
    '4178cb65af': 'Now Playing (ipod-ui 4.6)',  # patch.py:6614 m=lyric_page(); loop(m); m.pressed=1; loop(m); m.word(m.lrc+O[SCROLL_Y],40)
    'b1c92aab98.26': 'Now Playing (ipod-ui 4.6)',  # patch.py:6614 m=lyric_page(); loop(m); m.pressed=1; loop(m); m.word(m.lrc+O[SCROLL_Y],40)
    'b1c92aab98.27': 'Now Playing (ipod-ui 4.6)',  # patch.py:6614 m=lyric_page(); loop(m); m.pressed=1; loop(m); m.word(m.lrc+O[SCROLL_Y],40)
    '6a61f1355f.2': 'Now Playing (ipod-ui 4.6)',  # patch.py:6615 assert follow(m,0)==40; m.pressed=0; loop(m); assert follow(m,0)==40 and settle(
    '78cc369f84': 'Now Playing (ipod-ui 4.6)',  # patch.py:6615 assert follow(m,0)==40; m.pressed=0; loop(m); assert follow(m,0)==40 and settle(
    'b1c92aab98.28': 'Now Playing (ipod-ui 4.6)',  # patch.py:6615 assert follow(m,0)==40; m.pressed=0; loop(m); assert follow(m,0)==40 and settle(
    '14b0be8b0c.12': 'Now Playing (ipod-ui 4.6)',  # patch.py:6616 m=lyric_page(); loop(m); m.pressed=1; loop(m); m.pressed=0; loop(m); follow(m,20
    '5810214f81.3': 'Now Playing (ipod-ui 4.6)',  # patch.py:6616 m=lyric_page(); loop(m); m.pressed=1; loop(m); m.pressed=0; loop(m); follow(m,20
    'b1c92aab98.29': 'Now Playing (ipod-ui 4.6)',  # patch.py:6616 m=lyric_page(); loop(m); m.pressed=1; loop(m); m.pressed=0; loop(m); follow(m,20
    'b1c92aab98.30': 'Now Playing (ipod-ui 4.6)',  # patch.py:6616 m=lyric_page(); loop(m); m.pressed=1; loop(m); m.pressed=0; loop(m); follow(m,20
    'b1c92aab98.31': 'Now Playing (ipod-ui 4.6)',  # patch.py:6616 m=lyric_page(); loop(m); m.pressed=1; loop(m); m.pressed=0; loop(m); follow(m,20
    'b5e3f6b84f.5': 'Now Playing (ipod-ui 4.6)',  # patch.py:6616 m=lyric_page(); loop(m); m.pressed=1; loop(m); m.pressed=0; loop(m); follow(m,20
    '14b0be8b0c.13': 'Now Playing (ipod-ui 4.6)',  # patch.py:6617 m=lyric_page(); loop(m); m.top=m.node(window,home_page); m.pressed=1; loop(m); m
    '4178cb65af.2': 'Now Playing (ipod-ui 4.6)',  # patch.py:6617 m=lyric_page(); loop(m); m.top=m.node(window,home_page); m.pressed=1; loop(m); m
    'b1c92aab98.32': 'Now Playing (ipod-ui 4.6)',  # patch.py:6617 m=lyric_page(); loop(m); m.top=m.node(window,home_page); m.pressed=1; loop(m); m
    'b1c92aab98.33': 'Now Playing (ipod-ui 4.6)',  # patch.py:6617 m=lyric_page(); loop(m); m.top=m.node(window,home_page); m.pressed=1; loop(m); m
    'a8da2bfe8f.3': 'Now Playing (ipod-ui 4.6)',  # patch.py:6618 m.pressed=0; loop(m); m.top=m.win; loop(m); follow(m,0); assert settle(m)[-1]==0
    'b1c92aab98.34': 'Now Playing (ipod-ui 4.6)',  # patch.py:6618 m.pressed=0; loop(m); m.top=m.win; loop(m); follow(m,0); assert settle(m)[-1]==0
    'b1c92aab98.35': 'Now Playing (ipod-ui 4.6)',  # patch.py:6618 m.pressed=0; loop(m); m.top=m.win; loop(m); follow(m,0); assert settle(m)[-1]==0
    'b6af0e1f46.5': 'Now Playing (ipod-ui 4.6)',  # patch.py:6618 m.pressed=0; loop(m); m.top=m.win; loop(m); follow(m,0); assert settle(m)[-1]==0
    '14b0be8b0c.14': 'Now Playing (ipod-ui 4.6)',  # patch.py:6621 m=lyric_page()
    '94795f3766': 'Now Playing (ipod-ui 4.6)',  # patch.py:6622 assert step(m)==11 and y(m)==0 and settle(m)[-1]==20
    'b033261e7d': 'Now Playing (ipod-ui 4.6)',  # patch.py:6624 for _ in range(5): assert step(m,gap=200)==11; ys.append(settle(m)[-1])
    'cdd63e7186': 'Now Playing (ipod-ui 4.6)',  # patch.py:6625 assert ys==[70,90,110,110,110],ys
    '8d288139c4': 'Now Playing (ipod-ui 4.6)',  # patch.py:6626 for _ in range(3): assert step(m,O[KEY_PREV],gap=200)==11
    '84149054c2': 'Now Playing (ipod-ui 4.6)',  # patch.py:6627 assert settle(m)[-1]==20 and not did(m,playing_timer_clear) and not m.starts and
    '14b0be8b0c.15': 'Now Playing (ipod-ui 4.6)',  # patch.py:6630 m=lyric_page(); centre(m); m.nodes[m.slide][value]=0; step(m); m.nodes[m.slide][
    '53fab8b81b.3': 'Now Playing (ipod-ui 4.6)',  # patch.py:6630 m=lyric_page(); centre(m); m.nodes[m.slide][value]=0; step(m); m.nodes[m.slide][
    'f19fc2ec4d.4': 'Now Playing (ipod-ui 4.6)',  # patch.py:6630 m=lyric_page(); centre(m); m.nodes[m.slide][value]=0; step(m); m.nodes[m.slide][
    'f2206cb84d': 'Now Playing (ipod-ui 4.6)',  # patch.py:6631 assert step(m)==11 and m.seeks==[105] and settle(m)[-1]==20
    'bf0954d4e1.2': 'Now Playing (ipod-ui 4.6)',  # patch.py:6632 step(m,O[SCRUB_MS],wait=True); assert m.starts==[m.win] and not m.timers; passed
    '14b0be8b0c.16': 'Now Playing (ipod-ui 4.6)',  # patch.py:6635 m=lyric_page(); loop(m); hold(m); loop(m,-28); settle(m)
    '2df204679d.6': 'Now Playing (ipod-ui 4.6)',  # patch.py:6635 m=lyric_page(); loop(m); hold(m); loop(m,-28); settle(m)
    '33e411d7d7.4': 'Now Playing (ipod-ui 4.6)',  # patch.py:6635 m=lyric_page(); loop(m); hold(m); loop(m,-28); settle(m)
    'b1c92aab98.36': 'Now Playing (ipod-ui 4.6)',  # patch.py:6635 m=lyric_page(); loop(m); hold(m); loop(m,-28); settle(m)
    'bb6c2c76d0.5': 'Now Playing (ipod-ui 4.6)',  # patch.py:6635 m=lyric_page(); loop(m); hold(m); loop(m,-28); settle(m)
    '87cd1c1941': 'Now Playing (ipod-ui 4.6)',  # patch.py:6637 assert follow(m,0)==20 and not m.starts and not m.timers; passed()
    'b1c92aab98.37': 'Now Playing (ipod-ui 4.6)',  # patch.py:6639 loop(m); assert raw(m)==0 and not m.starts and not m.timers; passed()
    'f670786de6': 'Now Playing (ipod-ui 4.6)',  # patch.py:6639 loop(m); assert raw(m)==0 and not m.starts and not m.timers; passed()
    '828d5aab4e': 'Now Playing (ipod-ui 4.6)',  # patch.py:6644 if mclLoadExLyric in HOOKS:
    # big cover page (ipod-ui 4.6)
    '185fc82d53': 'big cover page (ipod-ui 4.6)',  # patch.py:6204 m.nodes[title][text]=T*30; assert vis_paint()==[T*30]
    'a38d0b0245': 'big cover page (ipod-ui 4.6)',  # patch.py:6205 m.nodes[title][text]=T*40; assert vis_paint()==[T*33+\u2026]; passed()
    '0e46124c66': 'big cover page (ipod-ui 4.6)',  # patch.py:6210 assert struct.unpack_from(<I,demo,fileoff(demo,big))[0]==j(payload_syms[ringnav_
    '21c8ee7740': 'big cover page (ipod-ui 4.6)',  # patch.py:6218 b,bw,alpha=bigcover()
    '14f1bff163': 'big cover page (ipod-ui 4.6)',  # patch.py:6219 b.advance(O[BC_MS]-1); assert alpha()==[255,255] and len(b.timers)==1
    'a44c732f02': 'big cover page (ipod-ui 4.6)',  # patch.py:6219 b.advance(O[BC_MS]-1); assert alpha()==[255,255] and len(b.timers)==1
    'fc61cf3cfb': 'big cover page (ipod-ui 4.6)',  # patch.py:6221 for _ in range(O[BC_STEPS]):
    '1ebe8d95b1': 'big cover page (ipod-ui 4.6)',  # patch.py:6223 n=O[BC_STEPS]; assert steps==[255*(n-k)//n for k in range(1,n+1)] and not b.time
    '1b10f1d81b': 'big cover page (ipod-ui 4.6)',  # patch.py:6225 b.handlers[HOOKS[main_loop_sleep_default][0]+12]=stock_sleep
    '49afffcc86': 'big cover page (ipod-ui 4.6)',  # patch.py:6227 tick(); assert alpha()==[0,0] and not b.timers
    'ea5610f7ed': 'big cover page (ipod-ui 4.6)',  # patch.py:6227 tick(); assert alpha()==[0,0] and not b.timers
    '14f1bff163.2': 'big cover page (ipod-ui 4.6)',  # patch.py:6228 b.word(O[MCL_POS],2); tick(); assert alpha()==[255,255] and len(b.timers)==1
    '5347fbe965': 'big cover page (ipod-ui 4.6)',  # patch.py:6228 b.word(O[MCL_POS],2); tick(); assert alpha()==[255,255] and len(b.timers)==1
    'ea5610f7ed.2': 'big cover page (ipod-ui 4.6)',  # patch.py:6228 b.word(O[MCL_POS],2); tick(); assert alpha()==[255,255] and len(b.timers)==1
    '14f1bff163.3': 'big cover page (ipod-ui 4.6)',  # patch.py:6229 b.advance(O[BC_MS]-1); tick(); assert alpha()==[255,255] and len(b.timers)==1; p
    'a44c732f02.2': 'big cover page (ipod-ui 4.6)',  # patch.py:6229 b.advance(O[BC_MS]-1); tick(); assert alpha()==[255,255] and len(b.timers)==1; p
    'ea5610f7ed.3': 'big cover page (ipod-ui 4.6)',  # patch.py:6229 b.advance(O[BC_MS]-1); tick(); assert alpha()==[255,255] and len(b.timers)==1; p
    '21c8ee7740.2': 'big cover page (ipod-ui 4.6)',  # patch.py:6230 b,bw,alpha=bigcover(); b.advance(O[BC_MS]+O[BC_STEP_MS])
    'e1c8b3cea9': 'big cover page (ipod-ui 4.6)',  # patch.py:6230 b,bw,alpha=bigcover(); b.advance(O[BC_MS]+O[BC_STEP_MS])
    '6047532c93': 'big cover page (ipod-ui 4.6)',  # patch.py:6231 f,ctx=b.handler(bw,O[EVT_DESTROY]); b.call(address=f,args=(ctx,b.event,0,0),gap=
    '73765184a7': 'big cover page (ipod-ui 4.6)',  # patch.py:6231 f,ctx=b.handler(bw,O[EVT_DESTROY]); b.call(address=f,args=(ctx,b.event,0,0),gap=
    '7089b04b7b': 'big cover page (ipod-ui 4.6)',  # patch.py:6232 assert not b.timers; passed()
    '0c991e6002': 'big cover page (ipod-ui 4.6)',  # patch.py:6240 b,bw,alpha=bigcover(); shade,title=b.nodes[bw][children]; b.word(bw+O[W_PARENT],
    '21c8ee7740.3': 'big cover page (ipod-ui 4.6)',  # patch.py:6240 b,bw,alpha=bigcover(); shade,title=b.nodes[bw][children]; b.word(bw+O[W_PARENT],
    'a136c8b8e0': 'big cover page (ipod-ui 4.6)',  # patch.py:6240 b,bw,alpha=bigcover(); shade,title=b.nodes[bw][children]; b.word(bw+O[W_PARENT],
    '4dfee25352': 'big cover page (ipod-ui 4.6)',  # patch.py:6241 img=b.node(image,img_bigcover); b.nodes[bw][children].append(img); b.word(img+O[
    '951b0913b8': 'big cover page (ipod-ui 4.6)',  # patch.py:6241 img=b.node(image,img_bigcover); b.nodes[bw][children].append(img); b.word(img+O[
    'fb5e21c22d': 'big cover page (ipod-ui 4.6)',  # patch.py:6241 img=b.node(image,img_bigcover); b.nodes[bw][children].append(img); b.word(img+O[
    '42812995cc': 'big cover page (ipod-ui 4.6)',  # patch.py:6247 put(img,*sq); put(shade,sq[0],sq[1]+BC_ART-60,BC_ART,60); put(title,sq[0]+12,sq[
    '6c6e19108a': 'big cover page (ipod-ui 4.6)',  # patch.py:6247 put(img,*sq); put(shade,sq[0],sq[1]+BC_ART-60,BC_ART,60); put(title,sq[0]+12,sq[
    'bf7c4f0afa': 'big cover page (ipod-ui 4.6)',  # patch.py:6247 put(img,*sq); put(shade,sq[0],sq[1]+BC_ART-60,BC_ART,60); put(title,sq[0]+12,sq[
    '1998828138': 'big cover page (ipod-ui 4.6)',  # patch.py:6248 b.nodes[img][image]=file:///tmp/coverpic.jpg; b.image_size=(1600,900)
    '4dfd481eb2': 'big cover page (ipod-ui 4.6)',  # patch.py:6248 b.nodes[img][image]=file:///tmp/coverpic.jpg; b.image_size=(1600,900)
    '23d4050e04': 'big cover page (ipod-ui 4.6)',  # patch.py:6253 b.byte(syms[g_playcover_type],1); b.u.mem_write(syms[g_lastcover_url],b/p/other\
    '7022507e88': 'big cover page (ipod-ui 4.6)',  # patch.py:6253 b.byte(syms[g_playcover_type],1); b.u.mem_write(syms[g_lastcover_url],b/p/other\
    'b960b73fdc': 'big cover page (ipod-ui 4.6)',  # patch.py:6254 assert fit()==[] and geo(img)==sq  # the last tracks cover file
    '06de30b402': 'big cover page (ipod-ui 4.6)',  # patch.py:6255 b.u.mem_write(syms[g_lastcover_url],bc_track(1)); assert fit()==bc_dec+bc_mv
    'ce0ce86558': 'big cover page (ipod-ui 4.6)',  # patch.py:6255 b.u.mem_write(syms[g_lastcover_url],bc_track(1)); assert fit()==bc_dec+bc_mv
    '6e8aa6e345': 'big cover page (ipod-ui 4.6)',  # patch.py:6256 x,y,w,h=geo(img); assert w>BC_ART and h==w*900//1600 and x==(375-w)//2 and y==(3
    '89466224fd': 'big cover page (ipod-ui 4.6)',  # patch.py:6256 x,y,w,h=geo(img); assert w>BC_ART and h==w*900//1600 and x==(375-w)//2 and y==(3
    'cfa65ef6b1': 'big cover page (ipod-ui 4.6)',  # patch.py:6257 assert geo(shade)==[x,y+h-60,w,60] and geo(title)==[x+12,y+h-45,w-24,30] and len
    '57475acdcd': 'big cover page (ipod-ui 4.6)',  # patch.py:6258 assert fit()==[]
    '04ca846cfd': 'big cover page (ipod-ui 4.6)',  # patch.py:6259 put(img,*sq); assert fit()==bc_mv and geo(img)==[x,y,w,h]
    'bf7c4f0afa.2': 'big cover page (ipod-ui 4.6)',  # patch.py:6259 put(img,*sq); assert fit()==bc_mv and geo(img)==[x,y,w,h]
    '14633f4497': 'big cover page (ipod-ui 4.6)',  # patch.py:6260 b.word(O[MCL_POS],2); assert fit()==[] and geo(img)==[x,y,w,h]  # a skip: still 
    '5347fbe965.2': 'big cover page (ipod-ui 4.6)',  # patch.py:6260 b.word(O[MCL_POS],2); assert fit()==[] and geo(img)==[x,y,w,h]  # a skip: still 
    '3568f7fe3d': 'big cover page (ipod-ui 4.6)',  # patch.py:6261 b.byte(syms[g_playcover_type],1); b.nodes[img][image]=file:///tmp/externpic.jpg
    '7022507e88.2': 'big cover page (ipod-ui 4.6)',  # patch.py:6261 b.byte(syms[g_playcover_type],1); b.nodes[img][image]=file:///tmp/externpic.jpg
    '74fa668bc8': 'big cover page (ipod-ui 4.6)',  # patch.py:6262 b.u.mem_write(syms[g_lastcover_url],bc_track(2)); assert fit()==bc_mv and geo(im
    'd12242c8b0': 'big cover page (ipod-ui 4.6)',  # patch.py:6262 b.u.mem_write(syms[g_lastcover_url],bc_track(2)); assert fit()==bc_mv and geo(im
    '06de30b402.2': 'big cover page (ipod-ui 4.6)',  # patch.py:6263 b.image_size=(900,1600); b.byte(syms[g_playcover_type],2); assert fit()==bc_dec+
    '1db6c7812c': 'big cover page (ipod-ui 4.6)',  # patch.py:6263 b.image_size=(900,1600); b.byte(syms[g_playcover_type],2); assert fit()==bc_dec+
    '84d5947e0e': 'big cover page (ipod-ui 4.6)',  # patch.py:6263 b.image_size=(900,1600); b.byte(syms[g_playcover_type],2); assert fit()==bc_dec+
    '1b2b96b553': 'big cover page (ipod-ui 4.6)',  # patch.py:6264 x,y,w,h=geo(img); assert h>BC_ART and w==h*900//1600 and x==(375-w)//2,geo(img)
    '89466224fd.2': 'big cover page (ipod-ui 4.6)',  # patch.py:6264 x,y,w,h=geo(img); assert h>BC_ART and w==h*900//1600 and x==(375-w)//2,geo(img)
    '169b9b0fb3': 'big cover page (ipod-ui 4.6)',  # patch.py:6265 b.nodes[img][image]=file:///tmp/album_tidal.jpg; b.u.mem_write(syms[g_lastcover_
    '7b8d8262f6': 'big cover page (ipod-ui 4.6)',  # patch.py:6265 b.nodes[img][image]=file:///tmp/album_tidal.jpg; b.u.mem_write(syms[g_lastcover_
    '74fa668bc8.2': 'big cover page (ipod-ui 4.6)',  # patch.py:6266 assert fit()==bc_mv and geo(img)==sq  # Tidal
    '3568f7fe3d.2': 'big cover page (ipod-ui 4.6)',  # patch.py:6267 b.u.mem_write(syms[g_lastcover_url],bc_track(2)); b.nodes[img][image]=file:///tm
    '5ed1bec45f': 'big cover page (ipod-ui 4.6)',  # patch.py:6267 b.u.mem_write(syms[g_lastcover_url],bc_track(2)); b.nodes[img][image]=file:///tm
    'd12242c8b0.2': 'big cover page (ipod-ui 4.6)',  # patch.py:6267 b.u.mem_write(syms[g_lastcover_url],bc_track(2)); b.nodes[img][image]=file:///tm
    '74fa668bc8.3': 'big cover page (ipod-ui 4.6)',  # patch.py:6268 b.nodes[img][image]=default_bigcover; assert fit()==bc_mv and geo(img)==sq; pass
    'c573122d1f': 'big cover page (ipod-ui 4.6)',  # patch.py:6268 b.nodes[img][image]=default_bigcover; assert fit()==bc_mv and geo(img)==sq; pass
    '55202c380d': 'big cover page (ipod-ui 4.6)',  # patch.py:6345 m.call(address=big,args=(bigwin,7,0,0),gap=0)  # ringnav_bigcover keeps the wind
    '85fba7fef6': 'big cover page (ipod-ui 4.6)',  # patch.py:6352 assert any(0<a<255 for a in pixels.values())
    '9d2b5f1ad7': 'big cover page (ipod-ui 4.6)',  # patch.py:6522 for page,left in ((1,O[BC_IDLE_FULL]),(0,3)):
    # Quick Settings and dialogs (ipod-ui 4.7)
    'a81c9fd1c3': 'Quick Settings and dialogs (ipod-ui 4.7)',  # patch.py:1945 assert tuple(m.get(prompt+O[k]) for k in (W_X,W_Y,W_W,W_H))==(0,0,375,O[CONFIRM_
    '646f1a6906': 'Quick Settings and dialogs (ipod-ui 4.7)',  # patch.py:1946 assert m.nodes[prompt][style:normal:font_size]==O[CONFIRM_PROMPT_PX]
    '1e6a4e4689': 'Quick Settings and dialogs (ipod-ui 4.7)',  # patch.py:1947 assert m.nodes[prompt][style:normal:text_align_h]==center and m.nodes[prompt][st
    # Q2 wheel keys and Key Tone (ipod-ui 4.8, Q2 only)
    '34e658d714': 'Q2 wheel keys and Key Tone (ipod-ui 4.8, Q2 only)',  # patch.py:9227 def turn(m,w,gaps,key=NEXT):
    '18b998b1ce': 'Q2 wheel keys and Key Tone (ipod-ui 4.8, Q2 only)',  # patch.py:9233 for table in (False,True):
    '5bd5ab63dd': 'Q2 wheel keys and Key Tone (ipod-ui 4.8, Q2 only)',  # patch.py:9244 assert turn(m,view,(1000,100,100,1000,100,100,100,400))==[1,2,3,4,5,6,6,0]
    'f3c2c3d56a': 'Q2 wheel keys and Key Tone (ipod-ui 4.8, Q2 only)',  # patch.py:9245 assert m.get(view+O[SCROLL_Y])==0 and turn(m,view,(1000,400,100,100),PREV)==[0,6
    'a4f0a31c20': 'Q2 wheel keys and Key Tone (ipod-ui 4.8, Q2 only)',  # patch.py:9262 m,w,es=ring()
    '65fe61354e': 'Q2 wheel keys and Key Tone (ipod-ui 4.8, Q2 only)',  # patch.py:9263 for gap in (100,100,200,200,O[EDGE_PAUSE_MS]-1):
    '1b4ec485e2.2': 'Q2 wheel keys and Key Tone (ipod-ui 4.8, Q2 only)',  # patch.py:9266 assert m.call(gap=O[EDGE_PAUSE_MS])==11 and m.selected(w)==0 and m.get(w+O[SCROL
    '13f330a7eb.4': 'Q2 wheel keys and Key Tone (ipod-ui 4.8, Q2 only)',  # patch.py:9267 m.paint(w,gap=0); assert m.sel()==(0,0,240,48)
    'ffae34869d': 'Q2 wheel keys and Key Tone (ipod-ui 4.8, Q2 only)',  # patch.py:9268 assert turn(m,w,(100,100,100))==[1,2,3] and turn(m,w,(100,100,100),PREV)==[2,1,0
    '5ee9fdb957': 'Q2 wheel keys and Key Tone (ipod-ui 4.8, Q2 only)',  # patch.py:9269 assert m.call(PREV,gap=100)==11 and m.selected(w)==0
    '2425d1664c.2': 'Q2 wheel keys and Key Tone (ipod-ui 4.8, Q2 only)',  # patch.py:9270 m.paint(w,gap=0); assert m.sel()==(0,6,240,48)   # bumped down at the top, on th
    '6d8ba8f135': 'Q2 wheel keys and Key Tone (ipod-ui 4.8, Q2 only)',  # patch.py:9271 assert m.call(PREV,gap=O[EDGE_PAUSE_MS])==11 and m.selected(w)==5; passed()
    '967f2416f4': 'Q2 wheel keys and Key Tone (ipod-ui 4.8, Q2 only)',  # patch.py:9273 m,w,es=ring(display_page)
    '472f32aa51': 'Q2 wheel keys and Key Tone (ipod-ui 4.8, Q2 only)',  # patch.py:9274 for gap in (100,O[EDGE_PAUSE_MS],1000):
    '1e0231bb5a': 'Q2 wheel keys and Key Tone (ipod-ui 4.8, Q2 only)',  # patch.py:9288 for gap in (1000,100,100,1000):
    'adb643c360': 'Q2 wheel keys and Key Tone (ipod-ui 4.8, Q2 only)',  # patch.py:9291 assert got==[(1,1),(1,2),(1,3),(1,4)],got; passed()
    '704d00c0fb': 'Q2 wheel keys and Key Tone (ipod-ui 4.8, Q2 only)',  # patch.py:9295 assert [tick(m) for _ in range(6)]==[1]*6 and m.selected(view)==6
    '324aa1f5c5': 'Q2 wheel keys and Key Tone (ipod-ui 4.8, Q2 only)',  # patch.py:9296 assert [tick(m,gap=gap) for gap in (1000,50,400,100)]==[0,0,1,1] and m.selected(
    '314f710b6d': 'Q2 wheel keys and Key Tone (ipod-ui 4.8, Q2 only)',  # patch.py:9302 m.u.hook_add(UC_HOOK_CODE,lambda u,a,size,x: seen.append(u.mem_read(TONE,1)[0]),
    'b76d3b1aa8': 'Q2 wheel keys and Key Tone (ipod-ui 4.8, Q2 only)',  # patch.py:9303 assert tick(m)==1 and seen==[0,1] and tick(m,gap=100)==1 and seen==[0,1,0,1]; pa
    '7548179734': 'Q2 wheel keys and Key Tone (ipod-ui 4.8, Q2 only)',  # patch.py:9307 assert [tick(m,gap=100) for _ in range(16)]==[1]*16 and m.selected(w)==65; passe
    'c2b318887d': 'Q2 wheel keys and Key Tone (ipod-ui 4.8, Q2 only)',  # patch.py:9310 assert sum(tick(m) for _ in range(5))==5 and m.selected(w)==5
    'd7e731a709': 'Q2 wheel keys and Key Tone (ipod-ui 4.8, Q2 only)',  # patch.py:9311 assert [tick(m,gap=gap) for gap in (100,200,200,O[EDGE_PAUSE_MS]-1)]==[0,0,0,0] 
    '73a22f538a': 'Q2 wheel keys and Key Tone (ipod-ui 4.8, Q2 only)',  # patch.py:9312 assert tick(m,gap=O[EDGE_PAUSE_MS])==1 and m.selected(w)==0
    'e6289a625f': 'Q2 wheel keys and Key Tone (ipod-ui 4.8, Q2 only)',  # patch.py:9313 assert tick(m,gap=100)==1 and m.selected(w)==1; passed()
    '4b6b6e58a9': 'Q2 wheel keys and Key Tone (ipod-ui 4.8, Q2 only)',  # patch.py:9318 for field in (pressed,animating):
    '54cd6b0199': 'Q2 wheel keys and Key Tone (ipod-ui 4.8, Q2 only)',  # patch.py:9320 m.advance(O[HOLD_POLL_MS]); assert m.selected(w)==1 and not m.timers  # the slid
    '6a2bf94683': 'Q2 wheel keys and Key Tone (ipod-ui 4.8, Q2 only)',  # patch.py:9321 assert press(m,RETURN)==1 and lift(m,RETURN)==0 and m.ret==0 and m.u.mem_read(KE
    '3aed5d6ed8': 'Q2 wheel keys and Key Tone (ipod-ui 4.8, Q2 only)',  # patch.py:9322 assert tick(m)==0 and m.ret==11 and m.selected(w)==1
    '02b19578f8': 'Q2 wheel keys and Key Tone (ipod-ui 4.8, Q2 only)',  # patch.py:9323 debounced(m); assert tick(m)==1 and m.selected(w)==2; passed()
    'be34ff1914': 'Q2 wheel keys and Key Tone (ipod-ui 4.8, Q2 only)',  # patch.py:9323 debounced(m); assert tick(m)==1 and m.selected(w)==2; passed()
    '7d9597fb67': 'Q2 wheel keys and Key Tone (ipod-ui 4.8, Q2 only)',  # patch.py:9326 assert [tick(m) for _ in range(6)]==[1]*6 and m.selected(w)==6
    '19e6f5cf3b': 'Q2 wheel keys and Key Tone (ipod-ui 4.8, Q2 only)',  # patch.py:9328 assert m.selected(w2)==6 and not buzzes(m); passed()
    '4e6d8c3707': 'Q2 wheel keys and Key Tone (ipod-ui 4.8, Q2 only)',  # patch.py:9331 assert press(m,CENTER)==1 and lift(m,CENTER)==0 and m.ret==11
    '9b7bc98d6f': 'Q2 wheel keys and Key Tone (ipod-ui 4.8, Q2 only)',  # patch.py:9332 m.advance(O[DOUBLE_CLICK_MS]); assert m.clicks==[es[0]] and not buzzes(m); passe
    '843be0645f': 'Q2 wheel keys and Key Tone (ipod-ui 4.8, Q2 only)',  # patch.py:9338 assert [tick(m) for _ in range(4)]==[0,0,0,0] and m.selected(view)==4 and m.u.me
    'd728f0276e': 'Q2 wheel keys and Key Tone (ipod-ui 4.8, Q2 only)',  # patch.py:9340 assert press(m)==0; m.byte(TONE,0); assert lift(m)==0 and m.selected(view)==1   
    'e7acacb513': 'Q2 wheel keys and Key Tone (ipod-ui 4.8, Q2 only)',  # patch.py:9340 assert press(m)==0; m.byte(TONE,0); assert lift(m)==0 and m.selected(view)==1   
    '68d8609819': 'Q2 wheel keys and Key Tone (ipod-ui 4.8, Q2 only)',  # patch.py:9341 assert press(m)==0; m.byte(TONE,1); assert lift(m)==1 and m.selected(view)==2   
    'd728f0276e.2': 'Q2 wheel keys and Key Tone (ipod-ui 4.8, Q2 only)',  # patch.py:9341 assert press(m)==0; m.byte(TONE,1); assert lift(m)==1 and m.selected(view)==2   
    '4cc7114bfc': 'Q2 wheel keys and Key Tone (ipod-ui 4.8, Q2 only)',  # patch.py:9342 m.byte(TONE,0x5a); assert tick(m)==1 and m.u.mem_read(TONE,1)==b\x5a; passed()
    '0edabec405': 'Q2 wheel keys and Key Tone (ipod-ui 4.8, Q2 only)',  # patch.py:9354 assert [tick(m,key) for key in (NEXT,PREV,NEXT)]==stock((NEXT,PREV,NEXT))==[1,1,
    '02b19578f8.2': 'Q2 wheel keys and Key Tone (ipod-ui 4.8, Q2 only)',  # patch.py:9355 m=audible(scrub_page()); centre(m); debounced(m)  # the double presss stock whee
    '1ca2b5f7e2': 'Q2 wheel keys and Key Tone (ipod-ui 4.8, Q2 only)',  # patch.py:9356 assert [tick(m,gap=100) for _ in range(3)]==stock((NEXT,)*3)==[1,1,1] and m.node
    '7c13a365d9': 'Q2 wheel keys and Key Tone (ipod-ui 4.8, Q2 only)',  # patch.py:9358 assert [tick(m,gap=20) for _ in range(2)]==[1,1] and slide(m,m.slide)[3]==120; p
    '173e341947': 'Q2 wheel keys and Key Tone (ipod-ui 4.8, Q2 only)',  # patch.py:9360 assert tick(m)==1 and [c[0] for c in m.moved()]==[slide_menu_scroll_to_next]; pa
    '2fead0dd90': 'Q2 wheel keys and Key Tone (ipod-ui 4.8, Q2 only)',  # patch.py:9362 assert [tick(m,gap=100) for _ in range(3)]==[1,1,1] and m.get(w+O[TABLE_TOP])==2
    'a2f7c4efae': 'Q2 wheel keys and Key Tone (ipod-ui 4.8, Q2 only)',  # patch.py:9363 keys=(CENTER,RETURN,O[KEY_PLAY],222,223)
    'a6b2a5d1a6': 'Q2 wheel keys and Key Tone (ipod-ui 4.8, Q2 only)',  # patch.py:9365 assert [tick(m,key) for key in keys]==stock(keys)==[1]*5 and m.selected(w)==0; p
    '1259956533': 'Q2 wheel keys and Key Tone (ipod-ui 4.8, Q2 only)',  # patch.py:9367 for kw in ({po:1},{bal:1},{way:1}):
    '1b3c3df4b3': 'Q2 wheel keys and Key Tone (ipod-ui 4.8, Q2 only)',  # patch.py:9373 m,w,es=long_list(8,routed(audible(Machine()),status=2))
    'e975a93454': 'Q2 wheel keys and Key Tone (ipod-ui 4.8, Q2 only)',  # patch.py:9374 assert tick(m)==1 and m.selected(w)==1 and [tick(m,key) for key in keys]==[1]*5;
    '8545dac447': 'Q2 wheel keys and Key Tone (ipod-ui 4.8, Q2 only)',  # patch.py:9377 assert [press(m,RETURN),press(m,RETURN,gap=500)]==[1,0]; long_return(m); assert 
    'da312d9a7f': 'Q2 wheel keys and Key Tone (ipod-ui 4.8, Q2 only)',  # patch.py:9377 assert [press(m,RETURN),press(m,RETURN,gap=500)]==[1,0]; long_return(m); assert 
    '25abf919f0': 'Q2 wheel keys and Key Tone (ipod-ui 4.8, Q2 only)',  # patch.py:9378 assert len(destinations(m))==0 and press(m,RETURN)==1; passed()
    'f34bc407f0': 'Q2 wheel keys and Key Tone (ipod-ui 4.8, Q2 only)',  # patch.py:9380 assert press(m,CENTER)==1 and m.release()==11 and press(m,CENTER,gap=100)==1 and
    '0c1461d0f7': 'Q2 wheel keys and Key Tone (ipod-ui 4.8, Q2 only)',  # patch.py:9381 for flags in (dict(g_backlight_status=0),dict(g_backlight_status=0,g_keylock_fla
    'd728f0276e.3': 'Q2 wheel keys and Key Tone (ipod-ui 4.8, Q2 only)',  # patch.py:9392 assert press(m)==0; m.page(playing_page); assert lift(m)==0 and m.ret==0 and m.s
    'f92846c058': 'Q2 wheel keys and Key Tone (ipod-ui 4.8, Q2 only)',  # patch.py:9392 assert press(m)==0; m.page(playing_page); assert lift(m)==0 and m.ret==0 and m.s
    '09d009e8a7': 'Q2 wheel keys and Key Tone (ipod-ui 4.8, Q2 only)',  # patch.py:9393 assert tick(m)==1 and m.ret==0
    'aaabec2de3': 'Q2 wheel keys and Key Tone (ipod-ui 4.8, Q2 only)',  # patch.py:9394 assert press(m)==1; m.top=lst; assert lift(m)==0 and m.ret==11 and m.selected(w)
    'eee466f316': 'Q2 wheel keys and Key Tone (ipod-ui 4.8, Q2 only)',  # patch.py:9394 assert press(m)==1; m.top=lst; assert lift(m)==0 and m.ret==11 and m.selected(w)
    'be34ff1914.2': 'Q2 wheel keys and Key Tone (ipod-ui 4.8, Q2 only)',  # patch.py:9395 assert tick(m)==1 and m.selected(w)==2; passed()
    'd728f0276e.4': 'Q2 wheel keys and Key Tone (ipod-ui 4.8, Q2 only)',  # patch.py:9399 assert press(m)==0; w2,es2=m.page_list(8,extent=8*48,name=allmusic_page); m.pain
    'aad0e62a15': 'Q2 wheel keys and Key Tone (ipod-ui 4.8, Q2 only)',  # patch.py:9400 assert lift(m)==1 and m.selected(w2)==1 and m.selected(w)==0
    'f6b449b7e7': 'Q2 wheel keys and Key Tone (ipod-ui 4.8, Q2 only)',  # patch.py:9401 wiped(m,w2); m.paint(w2,gap=0); assert m.selected(w2)==1 and tick(m)==1 and m.se
    '48c077d550': 'Q2 wheel keys and Key Tone (ipod-ui 4.8, Q2 only)',  # patch.py:9408 assert press(m)==0 and tick(m)==1 and m.selected(w)==1
    'd728f0276e.5': 'Q2 wheel keys and Key Tone (ipod-ui 4.8, Q2 only)',  # patch.py:9409 assert press(m)==0; m.page(playing_page); assert [tick(m),tick(m)]==[0,1] and m.
    'ec76034544': 'Q2 wheel keys and Key Tone (ipod-ui 4.8, Q2 only)',  # patch.py:9409 assert press(m)==0; m.page(playing_page); assert [tick(m),tick(m)]==[0,1] and m.
    '80b8704b8b': 'Q2 wheel keys and Key Tone (ipod-ui 4.8, Q2 only)',  # patch.py:9410 m.top=lst; assert lift(m)==0 and m.ret==11 and m.selected(w)==2
    'abfefd53ec': 'Q2 wheel keys and Key Tone (ipod-ui 4.8, Q2 only)',  # patch.py:9411 assert press(m)==0 and press(m,RETURN)==0 and lift(m)==0 and m.ret==11 and m.sel
    '4c862414ba': 'Q2 wheel keys and Key Tone (ipod-ui 4.8, Q2 only)',  # patch.py:9412 assert lift(m,RETURN)==0 and press(m,RETURN)==1 and lift(m,RETURN)==0
    '02b19578f8.3': 'Q2 wheel keys and Key Tone (ipod-ui 4.8, Q2 only)',  # patch.py:9413 debounced(m); assert tick(m)==1 and m.selected(w)==3
    'fd4b0317ce': 'Q2 wheel keys and Key Tone (ipod-ui 4.8, Q2 only)',  # patch.py:9413 debounced(m); assert tick(m)==1 and m.selected(w)==3
    # Games (ipod-ui 4.8, Q2 only)
    '59bdeea4c9': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10743 assert word(G_SCREEN)==0 and not frames() and m.get(payload_syms[wheel_raw])==0
    '7b597aa195.3': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10744 assert m.key()==11; passed()  # Return in the chooser after Vortex goes back to 
}
