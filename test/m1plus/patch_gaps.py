"""The patch.py checks the M1 Plus fails until the iPod UI item that ports them lands (gaprun.py).

Each is a top-level statement of patch.py, keyed by a hash of its source and its number among identical ones, and
listed under the docs/m1plus-ipod-ui.md item that makes it pass; that item's commit drops its entries (a listed
check that passes fails the run). After an edit to patch.py, GAPS_DUMP=gaps.json python3 test/m1plus/patch.py BUILD
writes every failing check, to rekey the list."""
GAPS = {
    # iPod UI assets (ipod-ui 3)
    '2212dfddf4': 'iPod UI assets (ipod-ui 3)',  # patch.py:1383 m=Machine(); root=asset_node(m,decode((B/ui/localmusic/album_page.bin).read_byte
    'ff3de6c4e5': 'iPod UI assets (ipod-ui 3)',  # patch.py:1383 m=Machine(); root=asset_node(m,decode((B/ui/localmusic/album_page.bin).read_byte
    '5965b040da': 'iPod UI assets (ipod-ui 3)',  # patch.py:2092 for x in (22,187,353):
    '30331ad68c': 'iPod UI assets (ipod-ui 3)',  # patch.py:11349 m.advance(3000); assert m.labels(np)==[Internet Radio,Three,Some Artist,A Song,M
    '9e5dd4854f': 'iPod UI assets (ipod-ui 3)',  # patch.py:8720 for name in (local_album,local_photos,list_folder,list_tidal,player_playlist,
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
    '428f0ff844': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:9195 assert len(kids)==7 and [row_text(r) for r in kids[2:4]+kids[5:]]==[Smart Awake,
    '84cc193a06': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:9197 assert m.icons_set==[system_display,switch_off,display_backlight,list_into,syste
    '8acf0e7dcb': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:9198 f,ctx=m.handler(m.nodes[kids[5]][children][0],O[EVT_CLICK]); m.calls=[]
    '8bf3015b29': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:9204 ctl=display_page(m,3); wheel,qs,hold,scrub_one,tone,hp,lock,wake,guard=m.nodes[c
    '0368ea4be4': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:9205 assert [row_text(r) for r in (hold,qs,scrub_one)]==[Hold Return: Recent,Wheel QS
    '0058106308': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:9342 assert kids==[rows[3],light,rows[0],corners,rows[1],shortcut,rows[2],centred] an
    '56a6bfb023': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:9363 assert kids==[rows[3],light,rows[0],corners,rows[1],shortcut,rows[2],centred] an
    # boot resume to Home (ipod-ui 4.5)
    # Quick Settings and dialogs (ipod-ui 4.7)
    'a81c9fd1c3': 'Quick Settings and dialogs (ipod-ui 4.7)',  # patch.py:1945 assert tuple(m.get(prompt+O[k]) for k in (W_X,W_Y,W_W,W_H))==(0,0,375,O[CONFIRM_
    '646f1a6906': 'Quick Settings and dialogs (ipod-ui 4.7)',  # patch.py:1946 assert m.nodes[prompt][style:normal:font_size]==O[CONFIRM_PROMPT_PX]
    '1e6a4e4689': 'Quick Settings and dialogs (ipod-ui 4.7)',  # patch.py:1947 assert m.nodes[prompt][style:normal:text_align_h]==center and m.nodes[prompt][st
    '7943387180': 'Quick Settings and dialogs (ipod-ui 4.7)',  # patch.py:2022 assert tuple(m.get(prompt+O[k]) for k in (W_X,W_Y,W_W,W_H))==(0,0,375,1
    '646f1a6906.2': 'Quick Settings and dialogs (ipod-ui 4.7)',  # patch.py:2023 assert m.nodes[prompt][style:normal:font_size]==O[CONFIRM_PROMPT_PX]
    # Home's Centre after the Q2 wheel's timed turns (100 ms gaps): the M1's knob and Centre on Home are m1_home_modes
    '99f82b57ad': 'Q2 wheel keys and Key Tone (ipod-ui 4.8, Q2 only)',  # patch.py:9246 assert m.confirm()==11 and m.dispatched()[0][1]==imgs[4]; passed()
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
    'e39fa9664a': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10697 sheet,chooser=games_open(); G=m.get(payload_syms[g])
    '213d438955': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10698 assert labels(chooser)==[Games,Sudoku,Vortex,Solitaire,Snake] and not m.nodes[sh
    '7fe72d327e': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10699 rows=m.nodes[m.find(scroll_view,chooser)][children]
    '1a3e33b7bc': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10708 pick(0); assert m.nodes[sheet][visible] and not m.nodes[chooser][visible] and wo
    '55475613b4': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10708 pick(0); assert m.nodes[sheet][visible] and not m.nodes[chooser][visible] and wo
    'b20a386471': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10709 key(O[KEY_NEXT]); assert byte(G_CUR)==1
    'f0312e5d82': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10709 key(O[KEY_NEXT]); assert byte(G_CUR)==1
    'b5cb0ea5ea': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10710 key(O[KEY_PREV]); key(O[KEY_PREV]); assert byte(G_CUR)==80
    'b5cb0ea5ea.2': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10710 key(O[KEY_PREV]); key(O[KEY_PREV]); assert byte(G_CUR)==80
    'f954819afe': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10710 key(O[KEY_PREV]); key(O[KEY_PREV]); assert byte(G_CUR)==80
    '8ab44fbf2b': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10711 key(O[KEY_FWD_BTN]); assert byte(G_CUR)==8
    'd32ce63cd7': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10711 key(O[KEY_FWD_BTN]); assert byte(G_CUR)==8
    '27066724e2': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10712 key(O[KEY_BACK_BTN]); assert byte(G_CUR)==80; passed()
    'f954819afe.2': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10712 key(O[KEY_BACK_BTN]); assert byte(G_CUR)==80; passed()
    '6097ea4c6d': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10716 blank=cells().index(0); clue=next(i for i,c in enumerate(cells()) if c&16)
    '762bfec88c': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10716 blank=cells().index(0); clue=next(i for i,c in enumerate(cells()) if c&16)
    '66068ea3ba': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10717 m.byte(G+G_CUR,clue); key(O[KEY_CENTER]); assert not word(G_PICKING)
    '89af2aa3aa': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10717 m.byte(G+G_CUR,clue); key(O[KEY_CENTER]); assert not word(G_PICKING)
    'de88260b50': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10717 m.byte(G+G_CUR,clue); key(O[KEY_CENTER]); assert not word(G_PICKING)
    '04c950dde2': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10718 m.byte(G+G_CUR,blank); key(O[KEY_CENTER]); assert word(G_PICKING)
    '89af2aa3aa.2': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10718 m.byte(G+G_CUR,blank); key(O[KEY_CENTER]); assert word(G_PICKING)
    'dce369e8ed': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10718 m.byte(G+G_CUR,blank); key(O[KEY_CENTER]); assert word(G_PICKING)
    'f31d93643d': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10719 for _ in range(3): key(O[KEY_NEXT])
    '610b9df287': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10720 paint(); key(O[KEY_CENTER]); assert cells()[blank]==3 and not word(G_PICKING)
    '89af2aa3aa.3': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10720 paint(); key(O[KEY_CENTER]); assert cells()[blank]==3 and not word(G_PICKING)
    '0c96352e42': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10721 m.advance(2000); saved=bytes(m.files[/mnt/data/ringnav-sudoku]); assert len(save
    '623961eddf': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10721 m.advance(2000); saved=bytes(m.files[/mnt/data/ringnav-sudoku]); assert len(save
    '076a4e0505': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10722 key(O[KEY_CENTER]); key(O[KEY_NEXT]); key(O[KEY_RETURN]); assert cells()[blank]=
    '4df64b387d': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10722 key(O[KEY_CENTER]); key(O[KEY_NEXT]); key(O[KEY_RETURN]); assert cells()[blank]=
    '89af2aa3aa.4': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10722 key(O[KEY_CENTER]); key(O[KEY_NEXT]); key(O[KEY_RETURN]); assert cells()[blank]=
    'f0312e5d82.2': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10722 key(O[KEY_CENTER]); key(O[KEY_NEXT]); key(O[KEY_RETURN]); assert cells()[blank]=
    '17b18e8bc2': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10723 before=cells(); key(O[KEY_PLAY]); assert cells()==before and word(52); paint()
    '585fa21b17': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10723 before=cells(); key(O[KEY_PLAY]); assert cells()==before and word(52); paint()
    'a63f5492f4': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10723 before=cells(); key(O[KEY_PLAY]); assert cells()==before and word(52); paint()
    '2682c91d39': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10724 key(O[KEY_RETURN]); assert cells()==before and not word(52)
    '4df64b387d.2': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10724 key(O[KEY_RETURN]); assert cells()==before and not word(52)
    '4df64b387d.3': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10725 key(O[KEY_RETURN]); m.advance(0); assert word(G_SCREEN)==0 and m.nodes[chooser][
    '66735bf663': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10725 key(O[KEY_RETURN]); m.advance(0); assert word(G_SCREEN)==0 and m.nodes[chooser][
    '7b597aa195.2': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10726 assert m.key()==11; passed()
    'c54ae6e308': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10728 m.page=m.top; pick(1); assert word(G_SCREEN)==2 and len(frames())==1 and m.get(p
    'fd81feb488': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10728 m.page=m.top; pick(1); assert word(G_SCREEN)==2 and len(frames())==1 and m.get(p
    '39b8a3eb58': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10729 m.word(payload_syms[wheel_travel],-50&0xffffffff); m.advance(34); assert word(G_
    'b65e55e61d': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10731 assert made(reset_poweroptions_timer) and made(widget_invalidate_force)
    '89af2aa3aa.5': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10735 key(O[KEY_CENTER]); m.advance(500); assert word(G_VX)==1 and made(widget_invalid
    '909fcc2b6a': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10735 key(O[KEY_CENTER]); m.advance(500); assert word(G_VX)==1 and made(widget_invalid
    '8ab44fbf2b.2': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10736 key(O[KEY_FWD_BTN]); assert not made(widget_invalidate_force)
    'a63f5492f4.2': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10737 key(O[KEY_PLAY]); assert word(G_PAUSED)==1 and not frames() and m.get(payload_sy
    'ab6bd7a3ab': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10737 key(O[KEY_PLAY]); assert word(G_PAUSED)==1 and not frames() and m.get(payload_sy
    '0dfa876a9e': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10738 x=word(G_VX+20),word(G_VX+24); m.advance(500); assert (word(G_VX+20),word(G_VX+2
    '4cf142ac31': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10738 x=word(G_VX+20),word(G_VX+24); m.advance(500); assert (word(G_VX+20),word(G_VX+2
    'a63f5492f4.3': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10739 key(O[KEY_PLAY]); assert word(G_PAUSED)==0 and len(frames())==1 and m.get(payloa
    'e8f2d84a5f': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10739 key(O[KEY_PLAY]); assert word(G_PAUSED)==0 and len(frames())==1 and m.get(payloa
    'ab6bd7a3ab.2': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10741 assert word(G_PAUSED)==1 and not frames() and m.get(payload_syms[wheel_raw])==0
    '4df64b387d.4': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10742 key(O[KEY_RETURN]); assert word(G_PAUSED)==2; key(O[KEY_NEXT]); paint(); key(O[K
    '89af2aa3aa.6': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10742 key(O[KEY_RETURN]); assert word(G_PAUSED)==2; key(O[KEY_NEXT]); paint(); key(O[K
    'f0312e5d82.3': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10742 key(O[KEY_RETURN]); assert word(G_PAUSED)==2; key(O[KEY_NEXT]); paint(); key(O[K
    'ff742ca8d6': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10742 key(O[KEY_RETURN]); assert word(G_PAUSED)==2; key(O[KEY_NEXT]); paint(); key(O[K
    '6e49df19e4': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10751 m.page=m.top; pick(2); assert word(G_SCREEN)==3 and cur()==0 and [n(p) for p in
    'fe2edce464': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10751 m.page=m.top; pick(2); assert word(G_SCREEN)==3 and cur()==0 and [n(p) for p in
    '09e347b645': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10752 key(O[KEY_CENTER]); m.advance(2000); assert (n(0),n(1))==(23,1) and bytes(m.file
    '89af2aa3aa.7': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10752 key(O[KEY_CENTER]); m.advance(2000); assert (n(0),n(1))==(23,1) and bytes(m.file
    '27066724e2.2': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10753 key(O[KEY_NEXT]); assert cur()==1; key(O[KEY_FWD_BTN]); assert cur()==7; key(O[K
    '5393abcfc6': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10753 key(O[KEY_NEXT]); assert cur()==1; key(O[KEY_FWD_BTN]); assert cur()==7; key(O[K
    '5a8ea34ce4': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10753 key(O[KEY_NEXT]); assert cur()==1; key(O[KEY_FWD_BTN]); assert cur()==7; key(O[K
    '5a8ea34ce4.2': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10753 key(O[KEY_NEXT]); assert cur()==1; key(O[KEY_FWD_BTN]); assert cur()==7; key(O[K
    '8ab44fbf2b.3': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10753 key(O[KEY_NEXT]); assert cur()==1; key(O[KEY_FWD_BTN]); assert cur()==7; key(O[K
    'f0312e5d82.4': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10753 key(O[KEY_NEXT]); assert cur()==1; key(O[KEY_FWD_BTN]); assert cur()==7; key(O[K
    '27066724e2.3': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10754 key(O[KEY_PREV]); key(O[KEY_PREV]); assert cur()==12; key(O[KEY_BACK_BTN]); asse
    'b5cb0ea5ea.3': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10754 key(O[KEY_PREV]); key(O[KEY_PREV]); assert cur()==12; key(O[KEY_BACK_BTN]); asse
    'b5cb0ea5ea.4': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10754 key(O[KEY_PREV]); key(O[KEY_PREV]); assert cur()==12; key(O[KEY_BACK_BTN]); asse
    'b77931b1d9': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10754 key(O[KEY_PREV]); key(O[KEY_PREV]); assert cur()==12; key(O[KEY_BACK_BTN]); asse
    'faca4081c1': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10754 key(O[KEY_PREV]); key(O[KEY_PREV]); assert cur()==12; key(O[KEY_BACK_BTN]); asse
    '2fba74c885': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10755 put(6,[64|13+11]); put(7,[3,64|10]); m.byte(G+G_SOL+329,7)  # Q of hearts; a fac
    '8829606b74': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10755 put(6,[64|13+11]); put(7,[3,64|10]); m.byte(G+G_SOL+329,7)  # Q of hearts; a fac
    'b06052aade': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10755 put(6,[64|13+11]); put(7,[3,64|10]); m.byte(G+G_SOL+329,7)  # Q of hearts; a fac
    '3adb6b93ae': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10756 key(O[KEY_CENTER]); assert word(G_PICKING) and word(48)==7; paint()
    '89af2aa3aa.8': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10756 key(O[KEY_CENTER]); assert word(G_PICKING) and word(48)==7; paint()
    '04c950dde2.2': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10757 key(O[KEY_FWD_BTN]); key(O[KEY_CENTER]); assert word(G_PICKING)  # not onto the
    '89af2aa3aa.9': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10757 key(O[KEY_FWD_BTN]); key(O[KEY_CENTER]); assert word(G_PICKING)  # not onto the
    '8ab44fbf2b.4': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10757 key(O[KEY_FWD_BTN]); key(O[KEY_CENTER]); assert word(G_PICKING)  # not onto the
    '89af2aa3aa.10': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10758 key(O[KEY_FWD_BTN]); key(O[KEY_PREV]); key(O[KEY_CENTER]); assert not word(G_PIC
    '8ab44fbf2b.5': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10758 key(O[KEY_FWD_BTN]); key(O[KEY_PREV]); key(O[KEY_CENTER]); assert not word(G_PIC
    'b5cb0ea5ea.5': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10758 key(O[KEY_FWD_BTN]); key(O[KEY_PREV]); key(O[KEY_CENTER]); assert not word(G_PIC
    'de88260b50.2': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10758 key(O[KEY_FWD_BTN]); key(O[KEY_PREV]); key(O[KEY_CENTER]); assert not word(G_PIC
    'e122849745': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10759 assert (n(6),n(7),byte(G_SOL+4+24*6+1),byte(G_SOL+4+24*7))==(2,1,64|10,64|3) and
    '2d1aafdcf1': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10760 put(1,[64|26]); m.byte(G+G_SOL+329,1); key(O[KEY_CENTER]); key(O[KEY_CENTER])  #
    '89af2aa3aa.11': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10760 put(1,[64|26]); m.byte(G+G_SOL+329,1); key(O[KEY_CENTER]); key(O[KEY_CENTER])  #
    '89af2aa3aa.12': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10760 put(1,[64|26]); m.byte(G+G_SOL+329,1); key(O[KEY_CENTER]); key(O[KEY_CENTER])  #
    'bb7cea08b8': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10760 put(1,[64|26]); m.byte(G+G_SOL+329,1); key(O[KEY_CENTER]); key(O[KEY_CENTER])  #
    '66fc1b822e': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10761 assert not word(G_PICKING) and n(1)==0 and n(2)==1 and byte(G_SOL+4+48)==64|26
    '6f97b4218f': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10762 m.byte(G+G_SOL+329,6); key(O[KEY_CENTER]); key(O[KEY_CENTER]); assert not word(G
    '89af2aa3aa.13': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10762 m.byte(G+G_SOL+329,6); key(O[KEY_CENTER]); key(O[KEY_CENTER]); assert not word(G
    '89af2aa3aa.14': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10762 m.byte(G+G_SOL+329,6); key(O[KEY_CENTER]); key(O[KEY_CENTER]); assert not word(G
    'f24d40e6a6': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10762 m.byte(G+G_SOL+329,6); key(O[KEY_CENTER]); key(O[KEY_CENTER]); assert not word(G
    '4df64b387d.5': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10763 key(O[KEY_CENTER]); key(O[KEY_RETURN]); assert not word(G_PICKING) and word(G_SC
    '89af2aa3aa.15': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10763 key(O[KEY_CENTER]); key(O[KEY_RETURN]); assert not word(G_PICKING) and word(G_SC
    'fc8f50ca54': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10763 key(O[KEY_CENTER]); key(O[KEY_RETURN]); assert not word(G_PICKING) and word(G_SC
    '2074d0cbd8': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10764 before_sol=sol(); key(O[KEY_PLAY]); assert word(52); paint(); key(O[KEY_RETURN])
    '3b5bfd9a87': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10764 before_sol=sol(); key(O[KEY_PLAY]); assert word(52); paint(); key(O[KEY_RETURN])
    '48117aadd2': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10764 before_sol=sol(); key(O[KEY_PLAY]); assert word(52); paint(); key(O[KEY_RETURN])
    '4df64b387d.6': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10764 before_sol=sol(); key(O[KEY_PLAY]); assert word(52); paint(); key(O[KEY_RETURN])
    'a63f5492f4.4': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10764 before_sol=sol(); key(O[KEY_PLAY]); assert word(52); paint(); key(O[KEY_RETURN])
    '0265a33ba6': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10765 key(O[KEY_RETURN]); m.advance(0); assert word(G_SCREEN)==0 and m.nodes[chooser][
    '4df64b387d.7': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10765 key(O[KEY_RETURN]); m.advance(0); assert word(G_SCREEN)==0 and m.nodes[chooser][
    'a8b1b2cfa3': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10772 m.page=m.top; pick(3); assert word(G_SCREEN)==4 and len(frames())==1 and m.get(p
    'eff446ceed': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10772 m.page=m.top; pick(3); assert word(G_SCREEN)==4 and len(frames())==1 and m.get(p
    '78000abffe': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10773 assert body()==[207,208,209] and sdir()==1 and sstate()==1; paint()
    'f8114faee2': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10774 snake_before=bytes(m.u.mem_read(G+G_SN,820))
    '144777dfab': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10775 skey(O[KEY_NEXT]); skey(O[KEY_PREV]); assert bytes(m.u.mem_read(G+G_SN,820))==sn
    '4d62a8962b': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10775 skey(O[KEY_NEXT]); skey(O[KEY_PREV]); assert bytes(m.u.mem_read(G+G_SN,820))==sn
    '8287c7e95e': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10775 skey(O[KEY_NEXT]); skey(O[KEY_PREV]); assert bytes(m.u.mem_read(G+G_SN,820))==sn
    '2fa25e9f4c': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10776 skey(O[KEY_FWD_BTN]); skey(O[KEY_FWD_BTN]); assert sdir()==2
    '2fa25e9f4c.2': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10776 skey(O[KEY_FWD_BTN]); skey(O[KEY_FWD_BTN]); assert sdir()==2
    '96332b49eb': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10776 skey(O[KEY_FWD_BTN]); skey(O[KEY_FWD_BTN]); assert sdir()==2
    '0a7bec6f95': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10777 m.advance(170); assert body()[-1]==229 and sdir()==3 and made(widget_invalidate_
    '00dddc04a1': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10778 skey(O[KEY_BACK_BTN]); assert sdir()==3  # waits for the next step
    '96b5b20b52': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10778 skey(O[KEY_BACK_BTN]); assert sdir()==3  # waits for the next step
    '8e41ef36eb': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10779 skey(O[KEY_PLAY]); assert word(G_PAUSED)==1 and not frames(); was=body(); m.adva
    'af9a1fb5b9': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10779 skey(O[KEY_PLAY]); assert word(G_PAUSED)==1 and not frames(); was=body(); m.adva
    'c37b29e226': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10779 skey(O[KEY_PLAY]); assert word(G_PAUSED)==1 and not frames(); was=body(); m.adva
    'e18733dc4c': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10779 skey(O[KEY_PLAY]); assert word(G_PAUSED)==1 and not frames(); was=body(); m.adva
    '144777dfab.2': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10780 skey(O[KEY_NEXT]); assert sdir()==3  # no turning while paused
    '96b5b20b52.2': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10780 skey(O[KEY_NEXT]); assert sdir()==3  # no turning while paused
    '8aa1970242': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10781 skey(O[KEY_PLAY]); assert word(G_PAUSED)==0 and len(frames())==1
    'c37b29e226.2': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10781 skey(O[KEY_PLAY]); assert word(G_PAUSED)==0 and len(frames())==1
    'e3f0e327aa': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10782 m.word(G+G_SN+812,5); m.advance(170*12); assert sstate()==2 and not frames() and
    'eeb61f1ab8': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10782 m.word(G+G_SN+812,5); m.advance(170*12); assert sstate()==2 and not frames() and
    '25f19f306a': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10783 best=bytes(m.files[/mnt/data/ringnav-snake]); assert len(best)==12 and best[:8]=
    '33e712f7ef': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10783 best=bytes(m.files[/mnt/data/ringnav-snake]); assert len(best)==12 and best[:8]=
    '7e0adf5d24': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10784 paint(); skey(O[KEY_CENTER]); assert sstate()==1 and body()==[207,208,209] and l
    'e040fa48bd': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10784 paint(); skey(O[KEY_CENTER]); assert sstate()==1 and body()==[207,208,209] and l
    '00827aff47': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10785 skey(O[KEY_BACK_BTN]); assert sdir()==0  # side Previous turns left, without the
    '00dddc04a1.2': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10785 skey(O[KEY_BACK_BTN]); assert sdir()==0  # side Previous turns left, without the
    '60e611da01': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10786 m.advance(170); assert body()[-1]==189
    '2fa25e9f4c.3': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10787 skey(O[KEY_FWD_BTN]); assert sdir()==1  # side Next turns right
    'b274b92071': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10787 skey(O[KEY_FWD_BTN]); assert sdir()==1  # side Next turns right
    '00dddc04a1.3': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10788 skey(O[KEY_PLAY]); skey(O[KEY_BACK_BTN]); skey(O[KEY_FWD_BTN]); assert sdir()==1
    '2fa25e9f4c.4': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10788 skey(O[KEY_PLAY]); skey(O[KEY_BACK_BTN]); skey(O[KEY_FWD_BTN]); assert sdir()==1
    'b274b92071.2': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10788 skey(O[KEY_PLAY]); skey(O[KEY_BACK_BTN]); skey(O[KEY_FWD_BTN]); assert sdir()==1
    'c37b29e226.3': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10788 skey(O[KEY_PLAY]); skey(O[KEY_BACK_BTN]); skey(O[KEY_FWD_BTN]); assert sdir()==1
    'c37b29e226.4': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10789 skey(O[KEY_PLAY])
    'd303e06d4c': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10790 skey(O[KEY_RETURN]); assert word(G_PAUSED)==2 and word(60)==0
    'faf9c369f1': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10790 skey(O[KEY_RETURN]); assert word(G_PAUSED)==2 and word(60)==0
    '144777dfab.3': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10791 skey(O[KEY_NEXT]); assert word(60)==1  # the wheel picks in the menu
    'ace70b2003': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10791 skey(O[KEY_NEXT]); assert word(60)==1  # the wheel picks in the menu
    '2dc4376a5f': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10792 skey(O[KEY_PREV]); assert word(60)==0
    '8287c7e95e.2': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10792 skey(O[KEY_PREV]); assert word(60)==0
    '00dddc04a1.4': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10793 skey(O[KEY_BACK_BTN]); assert word(60)==1
    'ace70b2003.2': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10793 skey(O[KEY_BACK_BTN]); assert word(60)==1
    '2dc4376a5f.2': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10794 skey(O[KEY_FWD_BTN]); assert word(60)==0
    '2fa25e9f4c.5': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10794 skey(O[KEY_FWD_BTN]); assert word(60)==0
    '2fa25e9f4c.6': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10795 skey(O[KEY_FWD_BTN]); paint(); skey(O[KEY_CENTER]); m.advance(0)
    '7e0adf5d24.2': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10795 skey(O[KEY_FWD_BTN]); paint(); skey(O[KEY_CENTER]); m.advance(0)
    '6c7b308867': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10796 assert word(G_SCREEN)==0 and not frames(); passed()
    '7e86233542.18': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10798 m.close(); assert m.get(payload_syms[g])==0 and not frames()
    '7fe72d327e.2': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10799 sheet,chooser=games_open(); G=m.get(payload_syms[g]); rows=m.nodes[m.find(scroll
    'e39fa9664a.2': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10799 sheet,chooser=games_open(); G=m.get(payload_syms[g]); rows=m.nodes[m.find(scroll
    '1a3e33b7bc.2': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10800 pick(0); assert cells()==before
    '98152372b9': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10800 pick(0); assert cells()==before
    '4df64b387d.8': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10801 key(O[KEY_RETURN]); m.advance(0); pick(2); assert sol()[:-4]==before_sol[:-4]  #
    '6e49df19e4.2': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10801 key(O[KEY_RETURN]); m.advance(0); pick(2); assert sol()[:-4]==before_sol[:-4]  #
    '74841e0c17': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10801 key(O[KEY_RETURN]); m.advance(0); pick(2); assert sol()[:-4]==before_sol[:-4]  #
    'd1de3ca1f1': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10804 m.byte(G+G_SOL+329,0)
    '9332ab3ede': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10806 assert not saves; m.advance(2000); assert len(saves)==1 and bytes(m.files[/mnt/d
    '1a3e33b7bc.3': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10807 key(O[KEY_RETURN]); m.advance(0); pick(0); key(O[KEY_RETURN]); m.advance(0); ass
    '4df64b387d.10': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10807 key(O[KEY_RETURN]); m.advance(0); pick(0); key(O[KEY_RETURN]); m.advance(0); ass
    '4df64b387d.9': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10807 key(O[KEY_RETURN]); m.advance(0); pick(0); key(O[KEY_RETURN]); m.advance(0); ass
    '6e49df19e4.3': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10807 key(O[KEY_RETURN]); m.advance(0); pick(0); key(O[KEY_RETURN]); m.advance(0); ass
    '71bc7633bd': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10807 key(O[KEY_RETURN]); m.advance(0); pick(0); key(O[KEY_RETURN]); m.advance(0); ass
    '012e45a329': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10808 key(O[KEY_RETURN]); m.advance(0); pick(1); assert len(frames())==1
    '4df64b387d.11': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10808 key(O[KEY_RETURN]); m.advance(0); pick(1); assert len(frames())==1
    'c54ae6e308.2': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10808 key(O[KEY_RETURN]); m.advance(0); pick(1); assert len(frames())==1
    '7e86233542.17': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10809 m.close(); assert m.get(payload_syms[g])==0 and not frames() and m.get(payload_s
    '59bdeea4c9': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10743 assert word(G_SCREEN)==0 and not frames() and m.get(payload_syms[wheel_raw])==0
    '7b597aa195.3': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10744 assert m.key()==11; passed()  # Return in the chooser after Vortex goes back to
    'eb4ebda625': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:11154 w=m.find(scroll_view,chooser); m.paint(w,gap=0)
    'b5883083a6.20': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:11154 w=m.find(scroll_view,chooser); m.paint(w,gap=0)
    'fce0c3c949': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:11155 for _ in range(5):
    'f57ff05657.3': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:11157 assert m.selected(w)==3
    '432a1afb1d': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:11158 assert m.call(gap=100)==11 and m.selected(w)==3; m.paint(w,gap=0)
    'b5883083a6.21': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:11158 assert m.call(gap=100)==11 and m.selected(w)==3; m.paint(w,gap=0)
    '89ccf3788a.2': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:11159 assert m.call(gap=O[EDGE_PAUSE_MS])==11 and m.selected(w)==0; m.paint(w,gap=0)
    'b5883083a6.22': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:11159 assert m.call(gap=O[EDGE_PAUSE_MS])==11 and m.selected(w)==0; m.paint(w,gap=0)
    '5ee9fdb957.2': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:11160 assert m.call(PREV,gap=100)==11 and m.selected(w)==0; m.paint(w,gap=0)
    'b5883083a6.23': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:11160 assert m.call(PREV,gap=100)==11 and m.selected(w)==0; m.paint(w,gap=0)
    'a2857f87e2': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:11161 assert m.call(PREV,gap=O[EDGE_PAUSE_MS])==11 and m.selected(w)==3; m.paint(w,gap=0
    'b5883083a6.24': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:11161 assert m.call(PREV,gap=O[EDGE_PAUSE_MS])==11 and m.selected(w)==3; m.paint(w,ga
    # Display and settings scenarios on V2.1's rows (Phase 5)
    'a85f9167be': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:2165 for row,image,fills in ((2,select,3),(0,unselect,0),(2,more,4),(0,more,0)):
    '4c768d5151': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:9182 one_label=m.nodes[m.nodes[scrub_one][children][0]][child
    '2402551706': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:9182 one_label=m.nodes[m.nodes[scrub_one][children][0]][child
    'cf1bf26734': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:9183 f,ctx=m.handler(m.nodes[scrub_one][children][0],O[EVT_CL
    '066151a889': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:9185 assert [(c[1],m.text(c[2]),m.text(c[3])) for c in m.call
    '377ee02e26': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:9213 assert [m.text(c[1]) for c in m.calls if c[0]==opendir@G
    '859ce41177': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:9214 assert did(m,image_manager_unload_all) and m.nodes[refre
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
    '6ab6271070': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8806 cf_label=m.nodes[m.nodes[cf][children][0]][children][1]; assert m.nodes[cf_label
    'a153bcc628': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8806 cf_label=m.nodes[m.nodes[cf][children][0]][children][1]; assert m.nodes[cf_label
    'd3ef113228': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8807 f,ctx=m.handler(m.nodes[cf][children][0],O[EVT_CLICK]); m.calls=[]
    'cd883ae115': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8808 assert m.call(address=f,args=(ctx,m.event,0,0),gap=0)==0 and m.nodes[cf_label][t
    '2a4b480d6f': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8809 assert [(c[1],m.text(c[2]),m.text(c[3])) for c in m.calls if c[0]==write_int_con
    '115a769ae0': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8810 m.call(address=f,args=(ctx,m.event,0,0),gap=0); assert m.nodes[cf_label][text]==
    '8271bfe8ff.13': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8810 m.call(address=f,args=(ctx,m.event,0,0),gap=0); assert m.nodes[cf_label][text]==
    '6ab6271070.2': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8811 m.call(address=f,args=(ctx,m.event,0,0),gap=0); assert m.nodes[cf_label][text]==
    '8271bfe8ff.14': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8811 m.call(address=f,args=(ctx,m.event,0,0),gap=0); assert m.nodes[cf_label][text]==
    '5350877c9a': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8814 sort_label,refresh_label=(m.nodes[m.nodes[r][children][0]][children][1] for r in
    '1f952a4891': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8815 assert m.nodes[sort_label][text]==Coverflow Sort: Album and m.nodes[refresh_labe
    'acc55bb4b8': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8816 f,ctx=m.handler(m.nodes[cf_refresh][children][0],O[EVT_CLICK]); m.mock(opendir@G
    'd9ba565d32': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8817 assert m.call(address=f,args=(ctx,m.event,0,0),gap=0)==0 and m.toasts[-1][3]==Co
    '1cdc7d997d': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8827 assert texts()==[Accent: Ivory,Home: Split,Battery: Icon,Theme: Minimal]; passed
    '84fb5c2e21': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8861 shortcut_button=m.nodes[shortcut][children][0]
    '5622a7e908': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8862 sf,sc=m.handler(shortcut_button,O[EVT_CLICK])
    'e5e97b6d36': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8863 for label in (Favorites,Shuffle,Rated Albums,Artists,Albums,Games,Rockbox):
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
    'f1eae9f6ce': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8900 writes=click(3); assert [(w[0],m.text(w[1]),m.text(w[2])) for w in writes]==[(1,
    'fd2f07fc93': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8900 writes=click(3); assert [(w[0],m.text(w[1]),m.text(w[2])) for w in writes]==[(1,
    'd54d44a9a7': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8901 assert corners_switch()==[switch_off] and m.nodes[light_label][text]==Light Mode
    'c181110dc5': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8902 assert (image_manager_unload_all,0x1000500) in [c[:2] for c in m.calls] and (wid
    '044cdebfbf': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8905 assert texts()==[Accent: Cobalt,Home: Split,Battery: Icon,Theme: Classic]; home_
    'baa6580069': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8905 assert texts()==[Accent: Cobalt,Home: Split,Battery: Icon,Theme: Classic]; home_
    'bb0f2639c0': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8911 for _ in range(2): m.call(address=f_light,args=(ctx_light,m.event,0,0),gap=0)
    'a206a7a356.2': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8912 assert m.nodes[light_label][text]==Light Mode: Off
    '231e4ded71': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8913 for value,name in ((5,Tangerine),(6,Plum),(8,Green),(0,Graphite),(1,Crimson),(2,
    '304a770053': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8921 writes=click(3); assert [(w[0],m.text(w[2])) for w in writes]==[(0,THEME),(0,MIN
    'f1eae9f6ce.2': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8921 writes=click(3); assert [(w[0],m.text(w[2])) for w in writes]==[(0,THEME),(0,MIN
    '26a9fde919': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8922 assert texts()[3]==Theme: Minimal and corners_switch()==[switch_on] and m.nodes[
    '466012b4b4.3': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8926 home_bounds(False)
    '6c1776f92b': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8927 m.paint(view); assert not m.bands and m.rounded[0][color]==color_t(ACCENTS[0][0]
    'a573372f36': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8929 m.call(address=f_light,args=(ctx_light,m.event,0,0),gap=0); m.call(address=f_lig
    'a573372f36.2': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8929 m.call(address=f_light,args=(ctx_light,m.event,0,0),gap=0); m.call(address=f_lig
    '9406000021': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8930 assert m.nodes[light_label][text]==Light Mode: Auto
    'f49ec85af4': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8931 for theme in (Classic,Minimal):
    'a206a7a356.3': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8933 m.call(address=f_light,args=(ctx_light,m.event,0,0),gap=0); assert m.nodes[light
    'a573372f36.3': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8933 m.call(address=f_light,args=(ctx_light,m.event,0,0),gap=0); assert m.nodes[light
    '472cbcd7f9': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8935 for value,name in ((1,Crimson),(2,Tidal),(3,Champagne),(4,Cobalt),(5,Tangerine),
    '3264b12e96': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8939 click(3); home_bounds(False,True); click(3); home_bounds(False); passed()
    '3264b12e96.2': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8939 click(3); home_bounds(False,True); click(3); home_bounds(False); passed()
    '466012b4b4.4': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8939 click(3); home_bounds(False,True); click(3); home_bounds(False); passed()
    'baa6580069.3': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8939 click(3); home_bounds(False,True); click(3); home_bounds(False); passed()
    '63150259f5': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8941 for value,name in ((1,Percent),(2,Icon + Percent),(3,Percent Inside),(0,Icon)):
    '47417148e4': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8945 m,view,rows=display({ACCENT:2,HOME:1,BATTERY:2,SHORTCUT:1}); got=[m.nodes[
    'e44a70fe75': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8945 m,view,rows=display({ACCENT:2,HOME:1,BATTERY:2,SHORTCUT:1}); got=[m.nodes[
    'f529705857': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8945 m,view,rows=display({ACCENT:2,HOME:1,BATTERY:2,SHORTCUT:1}); got=[m.nodes[
    'b43f0ec9d3': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8946 m,view,rows=display({BATTERY:3}); assert m.nodes[m.nodes[m.nodes[rows[2]][childr
    'e8b43de32c': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8946 m,view,rows=display({BATTERY:3}); assert m.nodes[m.nodes[m.nodes[rows[2]][childr
    '47417148e4.2': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8947 m,view,rows=display({ACCENT:2,HOME:1,THEME:1}); got=[m.nodes[m.nodes[m.nodes[r
    'e684a09ad2': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8947 m,view,rows=display({ACCENT:2,HOME:1,THEME:1}); got=[m.nodes[m.nodes[m.nodes[r
    '49c403d473': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8948 assert got==[Accent: Tidal,Home: Full,Battery: Icon,Theme: Classic] and m.nodes[
    '3d40ff6b9b': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8981 assert m.selected(view)==3 and m.confirm()==11 and m.dispatched()[0][1]==m.nodes
    'b32ce1e463': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:8985 assert at(0x613ee8,4)==bytes.fromhex(1cc7a524) and at(0x77c71c,5)==bdone\0; pass
    'dca5c4a74d': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:9068 for classic in (0,1):
    '01f9e7d40a': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:9083 CONFIG.clear(); m,view=settings(display,sub=1); items=m.nodes[view][children]; t
    'e1e8ddc1d0': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:9089 for classic in (1,0,1,0,1):  # each a click on Theme, from Minimal
    'd83a7b5843': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:9107 m,view=settings(0x4cbcc4,default=72); before=tree(m,view); lay(m,view); after=tr
    '6f053ba547': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:9110 m,view=settings(0x4cbcc4); odd=m.node(list_item); other=m.node(button)
    '6f053ba547.2': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:9117 m,view=settings(0x4cbcc4); lay(m,view); items=m.nodes[view][children]
    'd652ea7b25.4': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:9119 m.paint(view); assert m.selected(view)==0
    '330e6086e6.2': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:9125 assert m.confirm()==11 and m.dispatched()[0][1]==buttons[-1]; passed()
    '638c1bd20c': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:9126 m.click(buttons[2]); assert m.selected(view)==2; passed()
    'ecbccc89c2': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:9126 m.click(buttons[2]); assert m.selected(view)==2; passed()
    'f9bab94df3': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:9130 m,view,rows=display({ACCENT:2}); m.paint(view)
    '8fe2090d8d': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:9131 assert not m.bands and m.rounded[-1][color]==color_t(0xeeeeec); passed()
    '5ffc96853b': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:9132 m,view,rows=display({ACCENT:2,THEME:1}); m.paint(view)
    'fe173a1c41': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:9133 assert [m.bands[i][4] for i in (0,1,47)]==[color_t(ACCENTS[2][i]) for i in (4,0,
    '8271bfe8ff.15': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:9134 f,ctx=m.handler(m.nodes[rows[0]][children][0],O[EVT_CLICK]); m.call(address=f,ar
    '91e3bc677a': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:9134 f,ctx=m.handler(m.nodes[rows[0]][children][0],O[EVT_CLICK]); m.call(address=f,ar
    'b42e571763': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:9135 m.paint(view); assert [m.bands[i][4] for i in (0,1,47)]==[color_t(ACCENTS[3][i])
    'f1671ac043': "Display and settings scenarios on V2.1's rows (Phase 5)",  # patch.py:9148 for config,listw,roww,shown in (({HOME:1},375,O[HOME_FULL_ROW],0),({},O[HOME_SPL
    # Q2 Return key and window-manager ABI (Phase 5)
    'dfe4cdaacb': 'Q2 Return key and window-manager ABI (Phase 5)',  # patch.py:3181 for existing in (False,True):
    '06388513e1': 'Q2 Return key and window-manager ABI (Phase 5)',  # patch.py:3204 assert m.call(170,gap=0)==11
    # Q2 pointer dispatch ABI (Phase 5)
    'c2221ae651': 'Q2 pointer dispatch ABI (Phase 5)',  # patch.py:3383 assert [c[1] for c in m.dispatched()]==[w,es[0]] and not m.clicks
    '4fbeccd763': 'Q2 pointer dispatch ABI (Phase 5)',  # PullDispatchMachine uses Q2 vtable and emitter fixtures; V2.1 needs its own fixture
}
