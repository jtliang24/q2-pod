"""The patch.py checks the M1 Plus fails until the iPod UI item that ports them lands (gaprun.py).

Each is a top-level statement of patch.py, keyed by a hash of its source and its number among identical ones, and
listed under the docs/m1plus-ipod-ui.md item that makes it pass; that item's commit drops its entries (a listed
check that passes fails the run). After an edit to patch.py, GAPS_DUMP=gaps.json python3 test/m1plus/patch.py BUILD
writes every failing check, to rekey the list."""
GAPS = {
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
    'cda4a65073': 'status bar scenarios on the V2.1 bar (Phase 5)',  # patch.py:1248 t,label,show,page=title_machine(TIMETITLE=0,THEME=MODERN); assert show(page(A
    'b8f4f6235c': 'status bar scenarios on the V2.1 bar (Phase 5)',  # patch.py:1249 assert show(page(None))==6:14 PM and t.nodes[label][style:normal:font_name]=
    'ec806f3360.5': 'status bar scenarios on the V2.1 bar (Phase 5)',  # patch.py:6409 m.advance(0) [dependent]
    'e8b2f8b250': 'status bar scenarios on the V2.1 bar (Phase 5)',  # patch.py:6427 assert m.call(address=HOOKS['systembar_showface'][0],args=(bar,0,0,0),gap=0)==0 [dependent]
    # The Q2 Display page's Home rows (its Corners and Q2 rows around them): the M1's Home layouts and rows are
    # m1_home_modes and the M1 Display test (ipod-ui 4.5); the fixture itself is Phase 5's
    '466012b4b4': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8866 home_bounds(False); carousel(False)
    '8f720362a9': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8868 home_bounds(True); carousel(False)
    '84b943d9a0': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8870 writes=click(1); assert [(w[0],m.text(w[2])) for w in writes]==[(2,HOME)] and te
    '927dc434cc.2': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8870 writes=click(1); assert [(w[0],m.text(w[2])) for w in writes]==[(2,HOME)] and te
    '4fc57e7f8e': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8871 carousel(True); assert not [c for c in m.calls if c[0]==image_manager_unload_all
    '35d85e600e': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8872 click(1); assert texts()[1]==Home: Split; home_bounds(False); carousel(False); p
    '466012b4b4.2': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8872 click(1); assert texts()[1]==Home: Split; home_bounds(False); carousel(False); p
    '715ae6bcff': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8872 click(1); assert texts()[1]==Home: Split; home_bounds(False); carousel(False); p
    '4fc57e7f8e.2': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8908 click(1); assert texts()[1]==Home: Full; home_bounds(True,True); click(1); carou
    '715ae6bcff.2': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8908 click(1); assert texts()[1]==Home: Full; home_bounds(True,True); click(1); carou
    '715ae6bcff.3': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8908 click(1); assert texts()[1]==Home: Full; home_bounds(True,True); click(1); carou
    'c0c3106d02': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8908 click(1); assert texts()[1]==Home: Full; home_bounds(True,True); click(1); carou
    'fd1c55d76c': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8908 click(1); assert texts()[1]==Home: Full; home_bounds(True,True); click(1); carou
    '715ae6bcff.4': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8909 click(1); home_bounds(False,True); carousel(False); passed()
    'baa6580069.2': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8909 click(1); home_bounds(False,True); carousel(False); passed()
    # The Q2's Display page after 1.6.4's restack (Smart Awake and Night Shift on it, Controls on System): the M1 keeps
    # its own (m1plus_nav_display.c)
    '84cc193a06': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:9197 assert m.icons_set==[system_display,switch_off,display_backlight,list_into,syste
    '8acf0e7dcb': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:9198 f,ctx=m.handler(m.nodes[kids[5]][children][0],O[EVT_CLICK]); m.calls=[]
    # Display and settings scenarios on V2.1's rows (Phase 5)
    'a85f9167be': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:2165 for row,image,fills in ((2,select,3),(0,unselect,0),(2,more,4),(0,more,0)):
    '4c768d5151': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:9182 one_label=m.nodes[m.nodes[scrub_one][children][0]][child
    '2402551706': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:9182 one_label=m.nodes[m.nodes[scrub_one][children][0]][child
    'cf1bf26734': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:9183 f,ctx=m.handler(m.nodes[scrub_one][children][0],O[EVT_CL
    '066151a889': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:9185 assert [(c[1],m.text(c[2]),m.text(c[3])) for c in m.call
    '377ee02e26': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:9213 assert [m.text(c[1]) for c in m.calls if c[0]==opendir@G
    'e8cb08926c': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8762 assert m.call(address=f,args=(ctx,m.event,0,0),gap=0)==0 and m.opened[-1]==(syst
    'f6375d0298': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8766 assert m.icons_set==[playset_covermode,playset_covermode,system_update]
    'dcddcb57a6': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8770 view=display_page(m,1); rows=setting_rows(m,view)
    '944032aee2': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8772 assert kids==[rows[3],light,rows[0],corners,rows[1],rows[2],centred] and m.nodes
    '10c62dfae3': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8772 kids=m.nodes[view]['children']; light,corners,centred=kids[1],kids[3],kids[6]
    'c9c6fdc8c1': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8773 assert m.icons_set==[system_display,system_display,system_display,system_display
    '0ac48111d4': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8774 buttons=[m.nodes[r][children][0] for r in rows]; labels=[m.nodes[b][children][1]
    '0e824e3e4f': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8774 buttons=[m.nodes[r][children][0] for r in rows]; labels=[m.nodes[b][children][1]
    '549cb92260': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8775 for b,l in zip(buttons,labels):
    '2ab19091a5': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8782 keep_label=m.nodes[m.nodes[keep_lit][children][0]][children][1]; assert m.nodes[
    '70bf24c794': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8782 keep_label=m.nodes[m.nodes[keep_lit][children][0]][children][1]; assert m.nodes[
    '4d56f7c40c': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8783 f,ctx=m.handler(m.nodes[keep_lit][children][0],O[EVT_CLICK]); m.calls=[]
    '86b4e73d17': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8784 assert m.call(address=f,args=(ctx,m.event,0,0),gap=0)==0 and not did(m,image_man
    '1bbb79bed9': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8785 assert [(c[1],m.text(c[2]),m.text(c[3])) for c in m.calls if c[0]==write_int_con
    '8271bfe8ff.10': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8786 m.call(address=f,args=(ctx,m.event,0,0),gap=0)
    '86b4e73d17.2': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8790 assert m.call(address=f,args=(ctx,m.event,0,0),gap=0)==0 and not did(m,image_man
    '8271bfe8ff.11': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8792 m.call(address=f,args=(ctx,m.event,0,0),gap=0)
    '341ae680b0': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8795 centred_label=m.nodes[m.nodes[centred][children][0]][children][1]; assert m.node
    'cb11270062': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8795 centred_label=m.nodes[m.nodes[centred][children][0]][children][1]; assert m.node
    '41b6025c64': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8796 f,ctx=m.handler(m.nodes[centred][children][0],O[EVT_CLICK]); m.calls=[]
    '86b4e73d17.3': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8797 assert m.call(address=f,args=(ctx,m.event,0,0),gap=0)==0 and not did(m,image_man
    '36ad551169': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8798 assert [(c[1],m.text(c[2]),m.text(c[3])) for c in m.calls if c[0]==write_int_con
    '3a615939a6': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8803 assert loaded(playing_page)==[playing_page_stock] and loaded(home_page)==[home_p
    '8271bfe8ff.12': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8804 m.call(address=f,args=(ctx,m.event,0,0),gap=0); assert loaded(playing_page)==[pl
    'a153bcc628': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8806 cf_label=m.nodes[m.nodes[cf][children][0]][children][1]; assert m.nodes[cf_label
    'd3ef113228': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8807 f,ctx=m.handler(m.nodes[cf][children][0],O[EVT_CLICK]); m.calls=[]
    '2a4b480d6f': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8809 assert [(c[1],m.text(c[2]),m.text(c[3])) for c in m.calls if c[0]==write_int_con
    '8271bfe8ff.13': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8810 m.call(address=f,args=(ctx,m.event,0,0),gap=0); assert m.nodes[cf_label][text]==
    '8271bfe8ff.14': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8811 m.call(address=f,args=(ctx,m.event,0,0),gap=0); assert m.nodes[cf_label][text]==
    '5350877c9a': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8814 sort_label,refresh_label=(m.nodes[m.nodes[r][children][0]][children][1] for r in
    'acc55bb4b8': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8816 f,ctx=m.handler(m.nodes[cf_refresh][children][0],O[EVT_CLICK]); m.mock(opendir@G
    '1cdc7d997d': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8827 assert texts()==[Accent: Ivory,Home: Split,Battery: Icon,Theme: Minimal]; passed
    '84fb5c2e21': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8861 shortcut_button=m.nodes[shortcut][children][0]
    '5622a7e908': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8862 sf,sc=m.handler(shortcut_button,O[EVT_CLICK])
    '927dc434cc': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8867 writes=click(1); assert [(w[0],m.text(w[2])) for w in writes]==[(1,HOME)] and te
    'a0f267beae': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8867 writes=click(1); assert [(w[0],m.text(w[2])) for w in writes]==[(1,HOME)] and te
    '0c075ea462': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8876 corners_label=m.nodes[m.nodes[corners][children][0]][children][1]; assert m.node
    '3fd3d27d9c': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8876 corners_label=m.nodes[m.nodes[corners][children][0]][children][1]; assert m.node
    '88774fb87c': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8878 assert corners_switch()==[switch_off]
    '66dc56914a': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8879 f,ctx=m.handler(m.nodes[corners][children][0],O[EVT_CLICK]); m.calls=[]
    '191084d657': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8880 assert m.call(address=f,args=(ctx,m.event,0,0),gap=0)==0 and corners_switch()==[
    '445cf125f8': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8881 assert [(c[1],m.text(c[3])) for c in m.calls if c[0]==write_int_config]==[(1,ROU
    '8329427fda': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8883 light_label=m.nodes[m.nodes[light][children][0]][children][1]; assert m.nodes[li
    'a206a7a356': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8883 light_label=m.nodes[m.nodes[light][children][0]][children][1]; assert m.nodes[li
    '7553168288': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8884 f,ctx=f_light,ctx_light=m.handler(m.nodes[light][children][0],O[EVT_CLICK])
    '91dc641367': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8885 for value,text in ((1,On),(2,Auto),(0,Off)):
    'd54d44a9a7': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8901 assert corners_switch()==[switch_off] and m.nodes[light_label][text]==Light Mode
    'c181110dc5': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8902 assert (image_manager_unload_all,0x1000500) in [c[:2] for c in m.calls] and (wid
    'baa6580069': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8905 assert texts()==[Accent: Cobalt,Home: Split,Battery: Icon,Theme: Classic]; home_
    'bb0f2639c0': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8911 for _ in range(2): m.call(address=f_light,args=(ctx_light,m.event,0,0),gap=0)
    'a206a7a356.2': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8912 assert m.nodes[light_label][text]==Light Mode: Off
    '231e4ded71': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8913 for value,name in ((5,Tangerine),(6,Plum),(8,Green),(0,Graphite),(1,Crimson),(2,
    '26a9fde919': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8922 assert texts()[3]==Theme: Minimal and corners_switch()==[switch_on] and m.nodes[
    '466012b4b4.3': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8926 home_bounds(False)
    '6c1776f92b': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8927 m.paint(view); assert not m.bands and m.rounded[0][color]==color_t(ACCENTS[0][0]
    'a573372f36': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8929 m.call(address=f_light,args=(ctx_light,m.event,0,0),gap=0); m.call(address=f_lig
    'a573372f36.2': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8929 m.call(address=f_light,args=(ctx_light,m.event,0,0),gap=0); m.call(address=f_lig
    '9406000021': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8930 assert m.nodes[light_label][text]==Light Mode: Auto
    'a206a7a356.3': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8933 m.call(address=f_light,args=(ctx_light,m.event,0,0),gap=0); assert m.nodes[light
    'a573372f36.3': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8933 m.call(address=f_light,args=(ctx_light,m.event,0,0),gap=0); assert m.nodes[light
    '472cbcd7f9': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8935 for value,name in ((1,Crimson),(2,Tidal),(3,Champagne),(4,Cobalt),(5,Tangerine),
    '63150259f5': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8941 for value,name in ((1,Percent),(2,Icon + Percent),(3,Percent Inside),(0,Icon)):
    '47417148e4': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8945 m,view,rows=display({ACCENT:2,HOME:1,BATTERY:2,SHORTCUT:1}); got=[m.nodes[
    'e44a70fe75': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8945 m,view,rows=display({ACCENT:2,HOME:1,BATTERY:2,SHORTCUT:1}); got=[m.nodes[
    'f529705857': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8945 m,view,rows=display({ACCENT:2,HOME:1,BATTERY:2,SHORTCUT:1}); got=[m.nodes[
    'b43f0ec9d3': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8946 m,view,rows=display({BATTERY:3}); assert m.nodes[m.nodes[m.nodes[rows[2]][childr
    'e8b43de32c': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8946 m,view,rows=display({BATTERY:3}); assert m.nodes[m.nodes[m.nodes[rows[2]][childr
    '3d40ff6b9b': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8981 assert m.selected(view)==3 and m.confirm()==11 and m.dispatched()[0][1]==m.nodes
    'b32ce1e463': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8985 assert at(0x613ee8,4)==bytes.fromhex(1cc7a524) and at(0x77c71c,5)==bdone\0; pass
    '01f9e7d40a': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:9083 CONFIG.clear(); m,view=settings(display,sub=1); items=m.nodes[view][children]; t
    'd83a7b5843': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:9107 m,view=settings(0x4cbcc4,default=72); before=tree(m,view); lay(m,view); after=tr
    '6f053ba547': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:9110 m,view=settings(0x4cbcc4); odd=m.node(list_item); other=m.node(button)
    '6f053ba547.2': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:9117 m,view=settings(0x4cbcc4); lay(m,view); items=m.nodes[view][children]
    '330e6086e6.2': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:9125 assert m.confirm()==11 and m.dispatched()[0][1]==buttons[-1]; passed()
    '638c1bd20c': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:9126 m.click(buttons[2]); assert m.selected(view)==2; passed()
    'ecbccc89c2': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:9126 m.click(buttons[2]); assert m.selected(view)==2; passed()
    'f9bab94df3': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:9130 m,view,rows=display({ACCENT:2}); m.paint(view)
    '8fe2090d8d': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:9131 assert not m.bands and m.rounded[-1][color]==color_t(0xeeeeec); passed()
    '8271bfe8ff.15': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:9134 f,ctx=m.handler(m.nodes[rows[0]][children][0],O[EVT_CLICK]); m.call(address=f,ar
    '91e3bc677a': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:9134 f,ctx=m.handler(m.nodes[rows[0]][children][0],O[EVT_CLICK]); m.call(address=f,ar
    '205e8cce17': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:9669 assert len(kids)==7 and [row_text(r) for r in kids[2:4]+kids[5:]]==[Smart Awake
    '9c9c68e54a': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:9678 ctl=display_page(m,3); wheel,hold,scrub_one,tone,hp,lock,wake,guard=m.nodes[ctl]
    'c248660b8f': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:9679 assert [row_text(r) for r in (hold,scrub_one)]==[Hold Return: Recent,Single P
    '721ce726ec': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:9698 title_label=m.nodes[m.nodes[time_title][children][0]][children][1]; assert m
    'c0543776ff': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:9698 title_label=m.nodes[m.nodes[time_title][children][0]][children][1]; assert m
    'c09c1d2d13': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:9699 f,ctx=m.handler(m.nodes[time_title][children][0],O[EVT_CLICK]); m.calls=[]
    '04ee26c974': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:9701 assert [(c[1],m.text(c[2]),m.text(c[3])) for c in m.calls if c[0]==write_int_co
    '86b4e73d17.4': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:9713 assert m.call(address=f,args=(ctx,m.event,0,0),gap=0)==0 and not did(m,image_ma
    '783dcdd2d8': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:10035 cf_label=m.nodes[m.nodes[cf][children][0]][children][1]; assert m.nodes[cf_l
    '5f8160d10d': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:10037 assert m.call(address=f,args=(ctx,m.event,0,0),gap=0)==0 and m.nodes[cf_label][
    'd35d8969d4': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:10039 m.call(address=f,args=(ctx,m.event,0,0),gap=0); assert m.nodes[cf_label][text]
    '783dcdd2d8.2': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:10040 m.call(address=f,args=(ctx,m.event,0,0),gap=0); assert m.nodes[cf_label][text]
    '292652f99c': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:10045 assert m.nodes[sort_label][text]==Cover Flow Sort: Album and m.nodes[refresh
    'fe25421f4e': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:12326 assert m.call(address=f,args=(ctx,m.event,0,0),gap=0)==0 and m.toasts[-1][3]=='C
    'ed2956df57': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:10049 assert did(m,image_manager_unload_all) and m.nodes[refresh_label][text]==Re
    'e13a30a3e2': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:10141 assert kids==[rows[3],light,rows[0],corners,rows[1],shortcut,rows[2],time_title,
    '9c302e240e': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:10142 assert texts()==[Accent: Cobalt,Home: Split,Battery: Icon,Theme: Modern]
    '3eaa96bb9c.11': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:10144 m.paint(view); assert m.selected(view)==0 and [m.bands[i][4] for i in (0,1,47)]=
    'd97107e594': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:10144 m.paint(view); assert m.selected(view)==0 and [m.bands[i][4] for i in (0,1,47)]=
    '40067dec30': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:10158 writes=pick_theme(0); assert [(w[0],m.text(w[2])) for w in writes]==[(0,THEME)
    'f4010c9d31': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:10158 writes=pick_theme(0); assert [(w[0],m.text(w[2])) for w in writes]==[(0,THEME)
    '3eaa96bb9c.12': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:10160 m.paint(view); assert m.selected(view)==0
    '6ca09aa218': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:10162 assert kids==[rows[3],light,rows[0],corners,rows[1],shortcut,rows[2],time_title,
    '3eaa96bb9c.13': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:10164 m.paint(view); assert not m.bands and m.rounded[0][color]==color_t(ACCENTS[0][
    'd08cf6e780': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:10168 for t in (2,0):
    'd652ea7b25.3': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:10422 m.paint(view); assert m.selected(view)==0
    '8d1e687c98': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:10437 m,view,rows=display({CLASSIC_LIGHT_ACCENT:2},setup=classic_light); m.paint(v
    '1bd50aaf3a': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:10438 assert CL_SEL(2) in [b[4] for b in m.bands]; passed()
    '8e9b60476e': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:10439 accent_row=m.nodes[view][children][2]; f,ctx=m.handler(m.nodes[accent_row][ch
    '4a5cac4138': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:10439 accent_row=m.nodes[view][children][2]; f,ctx=m.handler(m.nodes[accent_row][ch
    '8271bfe8ff.16': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:10439 accent_row=m.nodes[view][children][2]; f,ctx=m.handler(m.nodes[accent_row][ch
    '16f1862d89': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:10440 m.paint(view); assert CL_SEL(3) in [b[4] for b in m.bands] and CL_SEL(2) not in 
    '36b49d8f56': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:11948 cfv=display_page(m,2) [dependent]
    '5db2661012': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:11948 cf,cf_sort,cf_refresh=m.nodes[cfv]['children'] [fixture extension]
    '66249771a8': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:11950 ctl=display_page(m,3) [dependent]
    'f92a41034a': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:11952 view=display_page(m,1) [dependent]
    'c497c56eab': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:11992 assert loaded('playing_page')==['playing_page'] [dependent]
    'a7f54dea42': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:12353 m.call(address=HOOKS['home_page_init'][0],args=(home,0,0,0),gap=0) [dependent]
    '272249ba26': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:12384 carousel(False) [fixture extension]
    '272249ba26.2': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:12386 carousel(False) [fixture extension]
    '272249ba26.3': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:12390 carousel(False) [fixture extension]
    '272249ba26.4': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:12425 carousel(False) [fixture extension]
    'd652ea7b25.2': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:12439 assert m.selected(view)==0 [fixture extension]
    '4aadbcc5de': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:14516 swap_values(m,120,0) [fixture extension]
    'd7f4dc6863.3': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:14516 m=classic_light_home() [fixture extension]
    # Classic (1.6.7): its own geometry set boots V1.32 immediates (theme_boot), and its bar, rows, fonts, pane and
    # Library on Home with it; the M1 builds Minimal and Modern only (tools/m1plus.py m1_themes)
    'a08dbf9b32': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:9275 for config,preset in (({},0),({**C,K:1},1),({**C,K:2},2),({**C,K:3,HOME:
    'a361fff5ed': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:9296 for preset in range(4):
    'ff7a03c4ac': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:9344 assert m.config_reads==[(/mnt/data/config.ini,IPOD,key,0) for key in (ACC
    '162a1d4cea': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:9363 assert gradient({CLASSIC_LIGHT_ACCENT:1,THEME:1},[red,grey])[1]==[red,gr
    'ddf72f93ef': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:9432 for config,name,fmt in (({CLASSIC_LIGHT_ACCENT:1,THEME:1},switch_on,3)
    '7359ed486d': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:9439 for t in (1,2):
    '911eb3e3c1': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:9492 for preset,config in [(p,c) for p in CLASSIC for c in ({CLASSIC_LIGHT_ACCENT:s
    '9491397d36': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:9516 for preset,config in [(p,c) for p in CLASSIC for c in ({CLASSIC_LIGHT_ACCENT:s
    'c50f817f2a': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:9744 assert m.syscalls==[(4125,p,PAGE,7) for p in pages]+[s for p in pages for s in (
    '0fb5dd04ce': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:9745 assert {a:m.get(a) for a in IMM_SITES}=={a:(w&0xffff0000|28 if IMM_SITES[a]==pi
    'f90c48e783': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:9747 m.call(address=load,args=(m.string(system_bar),0,0,0),gap=0); assert len(m.sys
    'c1e3daff3e': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:9750 assert gm.syscalls==[(4125,pages[0],PAGE,7),(4125,pages[1],PAGE,7),(4125,pages[0
    'e36d3abbbe': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:9758 assert [s[3] for s in gm.syscalls]==[7] and {a:gm.get(a) for a in IMM_SITES}==gb
    '74510bd7ad': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:9763 assert gloaded(home_page,2)==[home_page] and gloaded(home_page,1)==[ipod_
    '868eec3662': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:9767 redirect(system_bar); assert loaded(system_bar)==[ipod_system_bar] and loa
    '72e7c5a2a3': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:9770 nm=Machine(); assert classic_light_boot(nm)==[classic-light_system_bar]
    '468b1add84': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:9771 assert {nm.get(a)&0xffff for a,v in IMM_SITES.items() if v==pitch}=={32}; pass
    '8349b5b269': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:9773 nm=Machine(); tried=[]; assert classic_light_boot(nm,rowart=0,fail=lambda page
    '13a7b1caa4': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:9779 for fail,want in ((lambda page:True,290),(lambda page:False,294)):
    '134029dd4e': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:9787 assert [(nm.text(c[1]),0x70000000<=c[1]<0x70010000) for c in nm.calls if c[0]==
    'ae5456ca42': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:9809 assert [r[:4] for r in grows]==[(0,j,375,1) for j in range(25)]+[(0,24,375,1),(0
    '954fb6a8eb': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:9810 assert (grows[0][4],grows[24][4],grows[25][4],grows[26][4])==(color_t(0xffffff),
    '690d609ad7': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:9811 assert all(a>=b for j in range(24) for a,b in zip(channels(grows[j][4]),channels
    '399668fdec': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:9817 assert [r[:4] for r in gdrows]==[(0,j,375,1) for j in range(26)]
    '5094ee33a1': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:9818 assert (gdrows[0][4],gdrows[24][4],gdrows[25][4])==(color_t(0x1c1c1c),color_t(0x
    'd665719d07': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:9819 assert all(a>=b for j in range(24) for a,b in zip(channels(gdrows[j][4]),channel
    '3bca7fc3d0': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:9847 assert ps_bar(pshome,0)==(Q2 Pod,1,0,0)
    '5bcd40e0a9': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:9848 assert ps_bar(pshome,2)==(Q2 Pod,0,0,classic_light_play_l) and ps_bar(pshome
    '91884605fc': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:9849 assert ps_bar(pssongs,2)==(Songs,1,classic_light_play_l,0) and ps_bar(pssong
    '3bca7fc3d0.2': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:9850 assert ps_bar(pshome,0)==(Q2 Pod,1,0,0); passed()
    'aaa9e52573': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:12140 for bt_text,bt_face in (('Навстречу Ветру','bold'),('日本語','default'),('Songs','c
    'f0827065aa': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:12183 assert bm.get(bw_['view_battery']+O['W_W'])==29 and bm.get(bw_['view_battery']+O
    'cd74de1736': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:9907 assert bm.get(bw_[img_bt]+O[W_Y])==1 and bm.get(bw_[img_wifi]+O[W_Y])&0x
    'c587d0e468': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:9908 assert bands[:LEVEL]==outline
    '5e224e0d47': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:12187 assert bands[LEVEL:]==[(BX,y+1+j,12,1,color_t(c)) for j,c in enumerate(ROWS)]+SH
    'db88085c12': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:12190 assert dark==body_bands(LINE)+bands[LEVEL:-2]
    '3a10c52250': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:9915 assert bands[LEVEL:]==[(BX,y+1+j,BW,1,color_t(c)) for j,c in enumerate(ROWS)]+SH
    'f491898ac7': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:12194 assert [b[:4] for b in bands[LEVEL:LEVEL+11]]==[(BX,y+1+j,BW,1) for j in range(1
    '8c187dcc88': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:12195 assert bm.image_draws==[((0,0,BW,11),(BX,y+1,BW,11))],bm.image_draws
    'e1f8cc9c29': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:12199 assert bands[LEVEL:LEVEL+11]==[(BX,y+1+j,BW,1,color_t(c)) for j,c in enumerate(R
    '8c187dcc88.2': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:12200 assert bm.image_draws==[((0,0,BW,11),(BX,y+1,BW,11))],bm.image_draws
    'c26e1c0a08': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:9927 bm,bw_,bands=classic_light_battery_bar(3,bar_battery,100%,state=2,cable=1); 
    '06036b048f': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:12208 assert bands[LEVEL:]==[(BX,y+1,3,11,color_t(0xd9402e))]+SHADE+EMBOSS
    '11e2298ce9': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:12209 for mode in (1,2,3):  # Percent Inside (digits in the body), and the stored valu
    'f911c3fe3d': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:12215 for lt,past in (('1',0xffffff),('0',0xffffff)):
    'b3506986e1': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:12224 for status,eq,eq_on in ((0,0,0),(2,0,0),(0,1,1),(2,1,0)):
    '927c293b21': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:9954 for lt,mark in ((1,l),(0,d)):
    '5e5ca7e295': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:9958 assert image({},classic_light_play_l,prep=classic_light)==[same,same] and imag
    'd1c0c66090': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:9964 assert image({LIGHT:1},classic_light_sort_bars,prep=classic_light,px=bars)
    '03883fc6e3': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:9966 assert image({LIGHT:1},classic_light_chevron,prep=classic_light,px=bars)==
    'cf5477b737': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:9969 assert image({},bar_aac,prep=classic_light)==[ink,ink] and image({THEME:1}
    'd6f59b9947': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:9971 assert image({LIGHT:0},bar_aac,prep=classic_light)==[white,white]; passed(
    '0f7a2571c2': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:9977 assert cm.icons==[(317+25,24,(0,0,240,96))] and classic_light_chevron in [cm.t
    '6f5f05d622': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:9978 cm.call(); cm.paint(cw); assert cm.icons==[(317+25,72-cm.get(cw+O[SCROLL_Y]),(
    'f457523035': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:9979 cm.touch(); cm.paint(cw); assert not cm.icons; passed()  # no selection, no chev
    '7ef8be6118': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:9980 assert image({},list_into,prep=classic_light)==[bytes(8)+b\xee*4]*2; passed(
    'a3819af6db': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:9993 for into_half in (1,0):  # Classic, both halves: the chevron alone, its box 
    'd105e65638': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10014 assert [title_value(r) for r in dm.nodes[dv][children]]==[(Theme,Classic),
    '5dceccafd2': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10019 assert (Single Press Scrub,Off) in [title_value(r) for r in dm.nodes[dv][ch
    '87219f38f4': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10025 assert [b[:5] for b in rm.bands]==ntick
    'd108428531': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10027 assert image({},select,prep=classic_light)==image({},unselect,prep=classic_l
    '78d0895ece': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10033 assert len(hm.icons)==1 and hm.icons[0][0]==168+25 and classic_light_chevron i
    '832e4ebbc0': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10137 writes=pick_theme(2); assert [(w[0],m.text(w[1]),m.text(w[2])) for w in writes]=
    'a98a01e63c': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10137 writes=pick_theme(2); assert [(w[0],m.text(w[1]),m.text(w[2])) for w in writes]=
    '2cd52126b1': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:12811 assert [m.nodes[i]['image'] for i in marks]==['unselect','select','unselect'] an
    '7b5178656d': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10307 assert {geometry(m,i) for i in marks}=={(375-SET[EDGE]-50,0,50,32)},[geometry(
    'fa9fefaafc': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:12812 assert m.selected(view)==1,m.selected(view)
    'fa9fefaafc.2': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:12814 assert m.selected(view)==1,m.selected(view)
    '52a9a2d092': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10314 m.paint(w); assert m.selected(w)==2,m.selected(w)
    '025f755abe': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:12792 assert [m.nodes[i]['image'] for i in marks]==['unselect','unselect','select'] an
    '0071a2ce54': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:12794 assert m.paint(view)==0 and m.selected(view)==2,m.selected(view)
    '0071a2ce54.2': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:12798 assert m.paint(view)==0 and m.selected(view)==2,m.selected(view)
    '83ea910eb4': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10340 m,view=settings(0x4c0f6c,default=32,boot=classic_light_on); item,title,detail=st
    'fd58aa37a3': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10342 assert hs[1]==64 and set(hs[:1]+hs[2:])=={32},hs
    '3222280cdb': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10346 m,view=settings(0x4c0f6c); item,*_=stacked_row(m,view); assert lay(m,view)==0 an
    '29a2d59a7e': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10346 m,view=settings(0x4c0f6c); item,*_=stacked_row(m,view); assert lay(m,view)==0 an
    '83ea910eb4.2': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10349 m,view=settings(0x4c0f6c,default=32,boot=classic_light_on); item,title,detail=st
    '707c4c2140': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10355 assert not m.nodes[lead][visible] and m.nodes[trail][visible] and geometry(m
    'ab58e79e1b': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10356 assert geometry(m,title)[0]==geometry(m,detail)[0]==SET[TEXT_X],(geometry(m,ti
    'e8786266c1': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10357 for classic in (0,2):  # Minimals and Moderns; Classics below (classic_light_
    'd292e0301f': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10378 for classic in (0,2,0,2,0,2):  # each a Theme pick, from Minimal: no restart
    'a8a58009af': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10400 for builder in (0x4c43e4, 0x4cbcc4, display):  # language, System settings, Di
    'a49e14f46f': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10410 CONFIG.clear(); m,view=settings(0x4cbcc4,boot=classic_light_boot); before=tree(m
    '804241dd89': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10443 m,view,rows=display({THEME:1,CLASSIC_LIGHT_ACCENT:7})
    'ca6e8e9699': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10444 assert [row_text(r) for r in m.nodes[view][children]][:3]==[Theme: Classic,
    '004086f705': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10445 m,view,rows=display({THEME:MODERN,ACCENT:7})
    'acc08bec35': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10446 assert [row_text(r) for r in m.nodes[view][children]]==[Theme: Modern,Light
    '5383884ab9': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10447 m,view,rows=display({THEME:3})
    '45de4bc6cd': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10448 assert [row_text(r) for r in m.nodes[view][children]]==[Theme: Minimal,Ligh
    '0db6723159': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10467 assert [sk_rows[j] for j in range(52)]==[color_t(NB_TOP),color_t(0x27ade5)]+[col
    'ce5ad76def': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10485 assert boxof(al)==(20,0,280,32) and boxof(ap)==(0,0,300,32) and boxof(asort)==(3
    'eaae8489ea': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10486 assert am.nodes[asort][image]==classic_light_sort_bars and am.nodes[al][sty
    'ab6d76a5ba': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10488 am.word(al+O[W_H],50); am.call(address=HOOKS[widget_on_paint_background][0],
    '0a22584090': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10490 assert boxof(al)==(20,0,280,32) and boxof(ap)==(0,0,300,32); passed()  # Recentl
    'bf79b36ffa': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10509 for light in (1,0):
    '4ae1592f52': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10518 assert not sep_bands(song_list(classic_light_on,address=0x4a4ae8)[0]),Albums
    'fef6c44c4a': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10519 assert not sep_bands(song_list(lambda k:k.config.update(THEME=1))[0]),Classic
    '6beaa47377': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10520 for light in (1,0):
    '33569def72': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10529 for lthm,ly,lend in ((1,0,672-256),(1,32,672-224),(0,0,672-294),(2,0,672
    '78935ec4bb': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10574 for status in (0,2,0):
    'da9394c1d9': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10601 for fname in (list_folder,list_song):
    '5d56b6c1f4': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10618 for theme_,square in ((1,1),(0,0),(2,0)):
    'd1b1a703fe': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10631 assert style_color(sk,0xffaaaaaa)[1]==0xffffffff and style_color(sk,0x80000000)[
    '89d47d90f8': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10635 for mlight,mwant in ((1,0xff6b6d6b),(0,0xff949294)):
    '3c057dbc04': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10658 assert {(b[0],b[2]) for b in nk.bands}=={(0,nk.get(nw+O[W_W]))} and np_loaded(
    '4af680388a': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10660 assert lit(nl)==1 and half_of(nl)!=half_of(nk)
    'ed7c67984f': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10661 assert style_color(nl,0xff000000,bg_color)[1]==0xffffffff and style_color(nl,0
    '379ba3118e': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10663 assert light_image({LIGHT:1},scover_wait0,False,prep=classic_light)[:4]==b
    'a3a2b32171': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10678 assert lit(au)==1 and style_color(au,0xff000000,bg_color)[1]==0xffffffff
    '8be7e3e5e2': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10681 assert lit(au)==0 and half_of(au)!=day and style_color(au,0xff000000,bg_color)
    'cb53aa2336': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10691 m,view,rows=display({THEME:1},setup=classic_light)
    'cfc813ab00': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10692 assert [row_text(r) for r in m.nodes[view][children]]==[Theme: Classic,Ligh
    'e0cfd27827': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10696 for stored,name in ((None,Classic Blue),(7,Classic Blue),(12,Classic Bl
    'a46a4d9b12': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10699 m,view,rows=display({},setup=classic_light); f,ctx=m.handler(m.nodes[rows[0]][c
    '9183036f78': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10700 for value,name in ((0,Graphite),(1,Crimson),(2,Tidal),(3,Champagne),(4,
    'a46a4d9b12.2': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10710 m,view,rows=display({},setup=classic_light); art=m.nodes[view][children][9]
    'ffe66125a4': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10710 m,view,rows=display({},setup=classic_light); art=m.nodes[view][children][9]
    'cfc813ab00.2': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10711 assert [row_text(r) for r in m.nodes[view][children]]==[Theme: Classic,Ligh
    '8867c30f55': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10712 assert m.config_reads[13:17]==[(/mnt/data/config.ini,IPOD,k,v) for k,v in ((
    '3bf16d8289': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10715 assert art_boot({})==art_boot({ROWART:1})==art_boot({ROWART:2})==[class
    '11022741e6': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10716 assert art_boot({ROWART:0})==[classic-light-text_system_bar]
    '536aa048e3': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10721 m,view,_=display({},setup=classic_light); row=m.nodes[view][children][5]; f,ct
    '16d6896c80': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10721 m,view,_=display({},setup=classic_light); row=m.nodes[view][children][5]; f,ct
    '3ed161bb74': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10721 m,view,_=display({},setup=classic_light); row=m.nodes[view][children][5]; f,ct
    '8e3f18c4a7': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10722 assert row_text(row)==Battery: Icon
    '83fd4aea14': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10723 for value,name in ((3,Percent Inside),(0,Icon),(3,Percent Inside)):
    '9d20fb56c8': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10734 b=m.nodes[row][children][0]; title=m.nodes[b][children][1]; val=next(k for k
    '8a711ccc68': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10734 b=m.nodes[row][children][0]; title=m.nodes[b][children][1]; val=next(k for k
    'f2795e87d8': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10734 b=m.nodes[row][children][0]; title=m.nodes[b][children][1]; val=next(k for k
    '9ed1dc1a70': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10735 vx,vw,bx=(m.get(val+O[W_X]),m.get(val+O[W_W]),m.get(b+O[W_X]))
    '24894284d8': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10736 assert row_w(Percent Inside)<=vw-4 and bx+vx+vw==356
    'fc92543ba5': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10737 assert m.get(title+O[W_X])+m.get(title+O[W_W])==vx-8; passed()
    '0d39090727': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10738 for stored in (1,2):
    'e4ba6522f9': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10745 for t in (0,2):  # Minimal and Modern: every value is its own (Classics Per
    '94f7a277a9': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10760 m,view,rows=display({THEME:1}); f,ctx=m.handler(m.nodes[rows[3]][children]
    'a477f3c544': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10760 m,view,rows=display({THEME:1}); f,ctx=m.handler(m.nodes[rows[3]][children]
    'db09a5833f': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10761 assert m.call(address=f,args=(ctx,m.event,0,0),gap=0)==0 and m.opened[-1]==(sys
    'c6f97c6bab': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:13256 assert [row_text(r) for r in m.nodes[view]['children']]==['Minimal','Modern','Cl
    '7857848972': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10766 m,view,rows=display({}); pview=display_page(m,4); m.calls=[]
    '832e4ebbc0.2': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10768 writes=pick_theme(2); assert [(w[0],m.text(w[2])) for w in writes][:1]==[(2,THE
    'b5632ce2c1': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10768 writes=pick_theme(2); assert [(w[0],m.text(w[2])) for w in writes][:1]==[(2,THE
    'c7b928e81e': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:13262 assert [m.nodes[m.nodes[m.nodes[r]['children'][0]]['children'][0]]['image'] for 
    '0d38a23f5d': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10774 for answer,light,want in ((0,0,[]),(10,0,[(1,THEME),(1,LIGHT),(9,CLASSI
    'a990dd0434': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10791 assert m.prompts==[Restart to apply?] and not [c for c in m.calls if c[0]==wr
    '2620d504a8': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10792 for answer,want in ((0,[]),(10,[(0,ROWART)])):
    'f07af0d011': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10801 m,view,_=display({ROUNDED:1},sub=4,cls=RestartMachine,setup=classic_light); 
    '183101a79b': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10803 assert m.call(address=payload_syms[theme_pick],args=(2,0,0,0),gap=0)==0 and m.
    '53d65c4641': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10805 assert writes==[(2,THEME),(4,ACCENT),(0,ROUNDED),(0,TIMETITLE)],writes
    '707b0cc6a9': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10806 assert [c[0] for c in m.calls if c[0]==stock_reboot]==[stock_reboot]
    'b1c3af4879': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10807 t=m.call(address=payload_syms[theme],args=(0,0,0,0),gap=0)&0xffffffff
    'd70a21d01d': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10808 assert m.text(m.get(t))==Classic
    '251720a9ab': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10810 for i,key,label in ((7,HOMELIB,Library on Home),(8,ROWPREVIEW,Row Preview
    'bcf5bd4d2d': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10819 for art,want in ((0,1),(1,0)):
    '1ca0b126aa': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10822 k=Machine(); assert [k.call(address=payload_syms[theme_restart],args=(t,0,0,0)
    '857a54b6a5': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10852 fk,fb,ft=font_row(classic_light,Title)
    'bf12794819': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10853 assert [fk.nodes[ft][fstyle:{s}:font_name] for s in STATES]==[classic-light]
    'b3b088370c': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10854 fk.calls=[]; native_row_layout(fk,fb); assert not [c for c in fk.calls if c[0]==
    'fd26aa9608': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10854 fk.calls=[]; native_row_layout(fk,fb); assert not [c for c in fk.calls if c[0]==
    'aa4cf517c8': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10854 fk.calls=[]; native_row_layout(fk,fb); assert not [c for c in fk.calls if c[0]==
    'd85722930f': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10855 fk,fb,ft=font_row(classic_light,Навстречу ветру); assert fk.nodes[ft][style:n
    '892db71293': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:13349 assert fk.nodes[ft]['style:normal:font_name']=='bold' and fk.nodes[ft]['style:no
    '8026238042': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10856 fk,fb,ft=font_row(classic_light,日本語 Title); assert fk.nodes[ft][style:normal:
    '49366170bb': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10856 fk,fb,ft=font_row(classic_light,日本語 Title); assert fk.nodes[ft][style:normal:
    '22458ab634': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10857 for setup in (None,lambda k: k.config.update(THEME=MODERN)):  # Minimal and Mode
    'e339bdb653': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:13395 for setup,face in ((lambda k: k.config.update(THEME=MODERN),'default'),(classic_
    'ac97b6086a': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10866 for setup,face in ((classic_light,classic-light),(lambda k: None,default),(l
    '0b91f21f03': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:10887 for config,listw,roww,shown in (({HOME:1},375,O[HOME_FULL_ROW],0),({},O[H
    'd7f4dc6863': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:11461 m=classic_light_home(); lib=named(m,m.top,list_view_homelib); lview=named(m,m.
    'a8633bce4f': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:11462 sets=named(m,m.top,list_view_homeset); assert not m.nodes[lib][visible] and 
    '4520f6257d': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:11466 assert ltitled()==Q2 Pod
    '77196ff0dd': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:11471 m.nodes[lview][children]=lrows
    'c0c3caab46': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:11472 f,ctx=m.handler(named(m,m.top,img_library),O[EVT_CLICK]); assert f==payload_
    '26e79705af': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:11472 f,ctx=m.handler(named(m,m.top,img_library),O[EVT_CLICK]); assert f==payload_
    'b0fbf8b8e1': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:11474 assert next(c for c in m.calls if c[0]==stock_localmusic)[1]==lib and next(c f
    '0dc95f049f': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:11475 assert next(c for c in m.calls if c[0]==widget_off_by_ctx)[1:3]==(lib,lib) and
    'c28d07b691': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:11476 assert m.nodes[lib][visible] and m.nodes[lib][sensitive]==1 and not m.nodes[
    'bd78e0856e': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:11477 for r in m.nodes[lview][children]:
    'e1c61429f0': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:11480 assert ltitled()==Library; passed()
    '1de9e6b89f': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:11481 m.calls=[]; assert m.call(O[KEY_RETURN])==11 and m.nodes[lst][visible] and n
    '75bca0d582': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:11482 f,ctx=m.handler(named(m,m.top,img_settings),O[EVT_CLICK]); m.call(address=f,
    'b65f951f58': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:11482 f,ctx=m.handler(named(m,m.top,img_settings),O[EVT_CLICK]); m.call(address=f,
    '4520f6257d.2': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:11483 m.call(O[KEY_RETURN]); assert ltitled()==Q2 Pod
    '79715657c2': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:11485 lbefore=list(m.nodes[lview][children]); m.calls=[]; f,ctx=m.handler(named(m,m.
    'c0c3caab46.2': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:11485 lbefore=list(m.nodes[lview][children]); m.calls=[]; f,ctx=m.handler(named(m,m.
    '00f3ee7e11': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:14061 assert m.nodes[lview]['children']==lbefore and len(lbefore)==18 and any(c[0]=='s
    '3a79e008f0': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:11487 assert m.nodes[lib][visible] and ltitled()==Library
    '0855bac06c': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:11488 for r in lbefore:
    '26fd422363': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:11490 m.call(O[KEY_RETURN]); assert m.nodes[lst][visible] and ltitled()==Q2 Pod;
    'b0d39d12bd': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:11491 for mode in (1,2):
    'd7f4dc6863.2': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:11496 CONFIG[HOMELIB]=0; m=classic_light_home(); del CONFIG[HOMELIB]
    'c0c3caab46.3': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:11497 f,ctx=m.handler(named(m,m.top,img_library),O[EVT_CLICK]); m.calls=[]; m.call
    '6d3ab55b06': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:11498 assert any(c[0]==on_home_music_onclick for c in m.calls) and not any(c[0]==st
    'b1027c6057': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:11579 pane_cases()
    'ca67f3f477': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:11741 set_value(m,SITES[0x524820],60); set_value(m,SITES[0x524944],6)
    'cc80da2e90': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:11741 set_value(m,SITES[0x524820],60); set_value(m,SITES[0x524944],6)
    '43aa56c88a': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:11744 assert m.call(address=HOOKS[localmusic_page_init][0],args=(m.top,5,0,0),gap=0)
    '2eebf6b01d': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:11745 button=m.nodes[m.nodes[view][children][0]][children][0]; icon=m.nodes[button
    'ffa43be08a': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:11745 button=m.nodes[m.nodes[view][children][0]][children][0]; icon=m.nodes[button
    '3215d688bc': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:11746 assert m.get(button+O[W_H])==60 and m.get(icon+O[W_X])==6; passed()
    '3439f03873': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:11750 for lra,lalbum in ((0,32),(1,52)):
    '34ac4855fc': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:11775 for lra in (0,1):
    'aee48b21c0': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:11785 for lra in (1,0):
    'bf774ca8a2': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:11792 assert lm.call(address=HOOKS[localmusic_page_init][0],args=(lm.top,5,0,0),gap=
    '4544463931': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:11701 for config,name,square in (({'THEME':'1'},'play_defaultcover',1),({'THEME':'2'}, [fixture extension]
    '3091791a7f': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:12040 assert loaded('dialog/volume_dialog')==['dialog/ipod_volume_dialog'] [dependent]
    '1dde9bbfa5': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:12068 assert style_color(pm,0xff000000,'bg_color')[1]==0xffffffff [fixture extension]
    'ecc63f3117': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:12243 for v in ('lo','hi'): [fixture extension]
    '7f5dffa791': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:12837 assert lay(m,view)==0 and geometry(m,item)[3]==64 and not m.nodes[lead]['visible [fixture extension]
    '63d018b330': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:12838 assert geometry(m,title)[0]==SET['TEXT_X'] [fixture extension]
    '83ea910eb4.3': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:12841 m,view=settings(0x4c0f6c,default=32,boot=classic_light_on) [fixture extension]
    'dd1a58efdc': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:13257 assert m.icons_set==['unselect','select','unselect'] [fixture extension]
    '1517353f27': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:13348 assert [(fk.nodes[ft][f'style:{s}:font_name'],fk.nodes[ft][f'style:{s}:font_size [fixture extension]
    '7bc1f1ab60': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:13349 fk,fb,ft=font_row(classic_light,'Moscow Москва') [fixture extension]
    '9585f2ca3d': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:13429 for light,paper in (('1',0xffffffff),('0',0xff000000)): [fixture extension]
    '6b1afb0859': 'Classic and the theme engine on its own geometry set (1.6.7; Classic unported)',  # patch.py:14390 for pt_ in ('0',): [fixture extension]
    # 1.6.7's new Shortcuts: the M1's are Favorites, Shuffle, Rated Albums, Artists and Albums (shortcut())
    'ddca64781d': 'Playlists, Podcasts and Audiobooks as Shortcuts (1.6.7; unported)',  # patch.py:10060 assert d.text(d.call(address=payload_syms[ipod_home_shortcut],args=(0,0,0,0),g
    '700de58828': 'Playlists, Podcasts and Audiobooks as Shortcuts (1.6.7; unported)',  # patch.py:12517 assert [(d.text(c[1]),c[2]) for c in d.calls if c[0]==navigator_to_with_context
    'c67b0e573f': 'Playlists, Podcasts and Audiobooks as Shortcuts (1.6.7; unported)',  # patch.py:10102 for label in (Favorites,Shuffle,Rated Albums,Playlists,Artists,Albums
    '4a2be76ac0': 'Playlists, Podcasts and Audiobooks as Shortcuts (1.6.7; unported)',  # patch.py:12156 assert m.text(m.call(address=payload_syms[ipod_home_shortcut],args=(0,0,0,0),g
    'eb604de254': 'Playlists, Podcasts and Audiobooks as Shortcuts (1.6.7; unported)',  # patch.py:12157 m.calls=[]; assert m.call(address=payload_syms[home_shortcut_open],args=(0,m.e
    'b36537fa89': 'Playlists, Podcasts and Audiobooks as Shortcuts (1.6.7; unported)',  # patch.py:12158 assert [m.text(c[1]) for c in m.calls if c[0]==navigator_to]==[folder_page]
    '68add6ecdb': 'Playlists, Podcasts and Audiobooks as Shortcuts (1.6.7; unported)',  # patch.py:12160 assert m.text(syms[g_folder_path])==/mnt/mmc/Podcasts and m.u.mem_read(syms[
    'c2403b1456': 'Playlists, Podcasts and Audiobooks as Shortcuts (1.6.7; unported)',  # patch.py:12162 assert m.text(m.call(address=payload_syms[ipod_home_shortcut],args=(0,0,0,0),g
    'eb604de254.2': 'Playlists, Podcasts and Audiobooks as Shortcuts (1.6.7; unported)',  # patch.py:12163 m.calls=[]; assert m.call(address=payload_syms[home_shortcut_open],args=(0,m.e
    'dd982fb5ef': 'Playlists, Podcasts and Audiobooks as Shortcuts (1.6.7; unported)',  # patch.py:12164 assert not [c for c in m.calls if c[0]==navigator_to] and m.toasts[-1][3]==No
    '27d4e91422.3': 'Playlists, Podcasts and Audiobooks as Shortcuts (1.6.7; unported)',  # patch.py:15022 assert m.call(address=HOOKS['folder_page_init'][0],args=(win,0,0,0),gap=0)==0 [dependent]
}
