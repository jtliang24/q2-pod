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
    # boot resume to Home (ipod-ui 4.5)
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
    'b5883083a6.25': 'Q2 wheel keys and Key Tone (ipod-ui 4.8, Q2 only)',  # patch.py:12698 w=m.find(scroll_view,chooser); m.paint(w,gap=0)
    'b5883083a6.26': 'Q2 wheel keys and Key Tone (ipod-ui 4.8, Q2 only)',  # patch.py:12702 assert m.call(gap=100)==11 and m.selected(w)==3; m.paint(w,gap=0)
    'b5883083a6.24': 'Q2 wheel keys and Key Tone (ipod-ui 4.8, Q2 only)',  # patch.py:15601 m.paint(w,gap=0)
    'b5883083a6.22': 'Q2 wheel keys and Key Tone (ipod-ui 4.8, Q2 only)',  # patch.py:15596 m.paint(w,gap=0)
    'b5883083a6.23': 'Q2 wheel keys and Key Tone (ipod-ui 4.8, Q2 only)',  # patch.py:15600 m.paint(w,gap=0)
    '62d41f4b6b.2': 'Q2 wheel keys and Key Tone (ipod-ui 4.8, Q2 only)',  # patch.py:16847 m.call(address=inp,args=(m.wm,m.event,0,0),event_type=O[EVT_KEY_DOWN],gap=0); 
    '2b29282a16': 'Q2 wheel keys and Key Tone (ipod-ui 4.8, Q2 only)',  # patch.py:16848 m.word(payload_syms[wheel_frame_at],m.now); m.call(address=inp,args=(m.wm,m.ev
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
    'fce0c3c949': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:11155 for _ in range(5):
    'f57ff05657.3': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:11157 assert m.selected(w)==3
    '432a1afb1d': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:11158 assert m.call(gap=100)==11 and m.selected(w)==3; m.paint(w,gap=0)
    '89ccf3788a.2': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:11159 assert m.call(gap=O[EDGE_PAUSE_MS])==11 and m.selected(w)==0; m.paint(w,gap=0)
    '5ee9fdb957.2': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:11160 assert m.call(PREV,gap=100)==11 and m.selected(w)==0; m.paint(w,gap=0)
    'a2857f87e2': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:11161 assert m.call(PREV,gap=O[EDGE_PAUSE_MS])==11 and m.selected(w)==3; m.paint(w,gap=0
    '60d2c2805f': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:15612 paint() [dependent]
    '60d2c2805f.2': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:15624 paint() [dependent]
    '60d2c2805f.3': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:15627 paint() [dependent]
    '60d2c2805f.4': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:15639 paint() [dependent]
    '60d2c2805f.5': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:15642 paint() [dependent]
    '60d2c2805f.6': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:15646 paint() [dependent]
    '60d2c2805f.7': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:15655 paint() [dependent]
    '60d2c2805f.8': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:15660 paint() [dependent]
    '60d2c2805f.9': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:15668 paint() [dependent]
    '60d2c2805f.10': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:15677 paint() [dependent]
    '60d2c2805f.11': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:15683 paint() [dependent]
    '60d2c2805f.12': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:15688 paint() [dependent]
    '60d2c2805f.13': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:15699 paint() [dependent]
    'e8477b34a9': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:15709 for _ in range(10): m.call(O['KEY_CENTER'],gap=100,count=2_000_000) [dependent]
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
    # Q2 Return key and window-manager ABI (Phase 5)
    'dfe4cdaacb': 'Q2 Return key and window-manager ABI (Phase 5)',  # patch.py:3181 for existing in (False,True):
    '06388513e1': 'Q2 Return key and window-manager ABI (Phase 5)',  # patch.py:3204 assert m.call(170,gap=0)==11
    # Q2 pointer dispatch ABI (Phase 5)
    'c2221ae651': 'Q2 pointer dispatch ABI (Phase 5)',  # patch.py:3383 assert [c[1] for c in m.dispatched()]==[w,es[0]] and not m.clicks
    '225d0d79d5': 'Q2 pointer dispatch ABI (Phase 5)',  # PullDispatchMachine uses Q2 vtable and emitter fixtures; V2.1 needs its own fixture
    # Cases that run V1.32 stock code or read a Q2 build file: config_playmode, the hscroll tick at 0x5e8914,
    # and the Q2 build's default.ttf
    'ee43bd3ea1': "V1.32's own code and assets run by the case (config_playmode, the hscroll tick, default.ttf)",  # patch.py:4595 assert [c[1:3] for c in m.calls if c[0]==config_playmode]==[(2,1)]; passed()
    '1b7552ad52': "V1.32's own code and assets run by the case (config_playmode, the hscroll tick, default.ttf)",  # patch.py:6078 for only_focus,want,stepped in ((1,7,False),(0,None,True)):
    'f118915b4f': "V1.32's own code and assets run by the case (config_playmode, the hscroll tick, default.ttf)",  # patch.py:6086 font=TTFont(B/default.ttf); advance=lambda s: sum(font[hmtx][font.getBestCma
    '49669592bd': "V1.32's own code and assets run by the case (config_playmode, the hscroll tick, default.ttf)",  # patch.py:6087 assert all(advance(s)<=271 for s in (Artist View: Cover Flow,Refresh Cover Fl
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
    '0804d29cca': 'Playlists, Podcasts and Audiobooks as Shortcuts (1.6.7; unported)',  # patch.py:10062 assert [(d.text(c[1]),c[2]) for c in d.calls if c[0]==navigator_to_with_context
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
