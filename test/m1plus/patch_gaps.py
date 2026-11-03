"""The patch.py checks the M1 Plus fails until the iPod UI item that ports them lands (gaprun.py).

Each is a top-level statement of patch.py, keyed by a hash of its source and its number among identical ones, and
listed under the docs/m1plus-ipod-ui.md item that makes it pass; that item's commit drops its entries (a listed
check that passes fails the run). After an edit to patch.py, GAPS_DUMP=gaps.json python3 test/m1plus/patch.py BUILD
writes every failing check, to rekey the list."""
GAPS = {
    # iPod UI assets (ipod-ui 3)
    'ff3de6c4e5': 'iPod UI assets (ipod-ui 3)',  # patch.py:1398 m=Machine(); root=asset_node(m,decode((B/'ui/localmusic/album_page.bin
    '2212dfddf4': 'iPod UI assets (ipod-ui 3)',  # patch.py:1398 m=Machine(); root=asset_node(m,decode((B/'ui/localmusic/album_page.bin
    '200658faae': 'iPod UI assets (ipod-ui 3)',  # patch.py:2106 node=next(n for n in ui_walk(decode((B/'ui/playing_page.bin').read_byt
    '5965b040da': 'iPod UI assets (ipod-ui 3)',  # patch.py:2107 for x in (22,187,353):
    '460388395f': 'iPod UI assets (ipod-ui 3)',  # patch.py:5454 bar=asset_tree(m,STATUS_BAR); m.word(bar+O['W_W'],375)
    '141b466846': 'iPod UI assets (ipod-ui 3)',  # patch.py:5454 bar=asset_tree(m,STATUS_BAR); m.word(bar+O['W_W'],375)
    '432f651209': 'iPod UI assets (ipod-ui 3)',  # patch.py:5455 views=[named(m,bar,n) for n in ('view_left','view_right')]
    '78b0d2089b': 'iPod UI assets (ipod-ui 3)',  # patch.py:5456 for v in views:
    '8217be2fad': 'iPod UI assets (ipod-ui 3)',  # patch.py:5465 cells=laid_out()
    '6faac8d410': 'iPod UI assets (ipod-ui 3)',  # patch.py:5467 assert all(h==30 and inset<=x and x+w<=375-inset for x,w,h in cells), 
    '9675b0c872': 'iPod UI assets (ipod-ui 3)',  # patch.py:5468 title=named(m,bar,'label_clock'); x,w=m.get(title+O['W_X']),m.get(titl
    '83f4a0efd5': 'iPod UI assets (ipod-ui 3)',  # patch.py:5469 left,right=(cells[len(m.nodes[views[0]]['children'])-1],cells[len(m.no
    '953d4e8e49': 'iPod UI assets (ipod-ui 3)',  # patch.py:5470 assert left[0]+left[1]<=x and x+w<=right[0] and x+w/2==375/2, (left,ri
    'f45fdac0a1': 'iPod UI assets (ipod-ui 3)',  # patch.py:5475 batt=[named(m,bar,n) for n in ('img_battery','label_battery','view_bat
    '4f4969742f': 'iPod UI assets (ipod-ui 3)',  # patch.py:5476 for mode,want in enumerate((10,O['BATT_PCT_W'],O['BATT_BODY_W']+O['BAT
    '7df3ec1854.2': 'iPod UI assets (ipod-ui 3)',  # patch.py:5488 m.word(bar+O['W_PARENT'],m.wm); m.word(syms['system_bar'],bar)
    '2fb8e24f61.2': 'iPod UI assets (ipod-ui 3)',  # patch.py:5488 m.word(bar+O['W_PARENT'],m.wm); m.word(syms['system_bar'],bar)
    'b51c376171': 'iPod UI assets (ipod-ui 3)',  # patch.py:5489 m.nodes[named(m,bar,'img_bt')]['visible']=0
    'f73bf2a48c': 'iPod UI assets (ipod-ui 3)',  # patch.py:5490 m.nodes[named(m,bar,'img_wifi')]['visible']=0
    'cf244ba904': 'iPod UI assets (ipod-ui 3)',  # patch.py:5491 slot=named(m,bar,'view_battery')
    '019eb47519': 'iPod UI assets (ipod-ui 3)',  # patch.py:5492 m.nodes[named(m,bar,'label_battery')]['text']='50%'
    'd4e2e98ab7': 'iPod UI assets (ipod-ui 3)',  # patch.py:5495 paint_live_bar()
    '5592f0f40d': 'iPod UI assets (ipod-ui 3)',  # patch.py:5496 idle=named(m,bar,'label_idle'); state=named(m,bar,'img_state'); eq=nam
    '2be6a9ce5b': 'iPod UI assets (ipod-ui 3)',  # patch.py:5496 idle=named(m,bar,'label_idle'); state=named(m,bar,'img_state'); eq=nam
    'dd695657d5': 'iPod UI assets (ipod-ui 3)',  # patch.py:5496 idle=named(m,bar,'label_idle'); state=named(m,bar,'img_state'); eq=nam
    '54bedb9c88': 'iPod UI assets (ipod-ui 3)',  # patch.py:5497 assert m.get(eq+O['W_W'])==28
    'ee4849c484': 'iPod UI assets (ipod-ui 3)',  # patch.py:5498 assert all(m.nodes[eq]['asset'][f'style:{s}:font_size']=='16' for s in
    'd4333c8df2': 'iPod UI assets (ipod-ui 3)',  # patch.py:5502 m.advance(0); shown=(m.nodes[state]['visible'],m.nodes[state].get('ima
    '406773bfbe': 'iPod UI assets (ipod-ui 3)',  # patch.py:5503 for status,equalizer,icon in ((0,0,''),(2,0,'bar_play'),(3,0,'bar_paus
    '2120c2ed3c': 'iPod UI assets (ipod-ui 3)',  # patch.py:5519 m.word(0xa3beac,2); m.nodes[eq]['visible']=1; m.nodes[state]['visible'
    '2bfc5141c1': 'iPod UI assets (ipod-ui 3)',  # patch.py:5519 m.word(0xa3beac,2); m.nodes[eq]['visible']=1; m.nodes[state]['visible'
    'c0c216337f': 'iPod UI assets (ipod-ui 3)',  # patch.py:5519 m.word(0xa3beac,2); m.nodes[eq]['visible']=1; m.nodes[state]['visible'
    '4cb62ca34f': 'iPod UI assets (ipod-ui 3)',  # patch.py:5521 assert ('stock_showface',bar) in [c[:2] for c in m.calls] and m.nodes[
    '0a9fe5785b': 'iPod UI assets (ipod-ui 3)',  # patch.py:5523 for mode in (1,2,3,0,1,2,3,0):
    'cd20baf1b9': 'iPod UI assets (ipod-ui 3)',  # patch.py:11154 assert texts(info)==['Spotify','Song','A, B','LP','0:10','-3:10']
    '35b96a16c8': 'iPod UI assets (ipod-ui 3)',  # patch.py:11161 m.advance(2500); assert texts(info)[4:]==['0:12','-3:08'] and len(m.th
    '338b3ce9bb': 'iPod UI assets (ipod-ui 3)',  # patch.py:11210 m.advance(250); assert texts(info)[4]=='1:05' and 'on_wm_keyup_fun' no
    '30331ad68c': 'iPod UI assets (ipod-ui 3)',  # patch.py:11365 m.advance(3000); assert m.labels(np)==['Internet Radio','Three','Some 
    # selection bar and paint backbone (ipod-ui 4.1)
    'cab93246cd': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:980 if is_m1plus:  # Stock's outline over V2.1's opaque rows until 4.1 (m1
    'c519fad1b2': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:1042 for classic in (0,1):
    'ff45bb6b2a': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:1937 assert not m.strokes and [(r['rect'],r['radius'],r['color']) for r in 
    'ecd194be6f': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:1941 assert not m.strokes and [r['rect'] for r in m.rounded if r['kind']=='
    'a81c9fd1c3': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:1960 assert tuple(m.get(prompt+O[k]) for k in ('W_X','W_Y','W_W','W_H'))==(
    '646f1a6906': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:1961 assert m.nodes[prompt]['style:normal:font_size']==O['CONFIRM_PROMPT_PX
    '1e6a4e4689': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:1962 assert m.nodes[prompt]['style:normal:text_align_h']=='center' and m.no
    'a85f9167be': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:2180 for row,image,fills in ((2,'select',3),(0,'unselect',0),(2,'more',4),(
    '2584fa5400': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:2673 for band_y in range(10,20):
    'c56a83002f': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:2678 assert [(c[2],c[3]) for c in m.calls if c[0]==sink]==want
    '4f7dbcae47': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:5386 m=Machine(); view,imgs=home_list(m); click_target(m,imgs[2])
    'f43abcdfc1': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:5386 m=Machine(); view,imgs=home_list(m); click_target(m,imgs[2])
    '3eaa96bb9c': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:5387 m.paint(view)
    'd652ea7b25': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:5388 assert m.selected(view)==0
    '47ba5647cc': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:5389 for i in range(1,7): assert m.call()==11 and m.selected(view)==i and m
    '3eaa96bb9c.2': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:5390 m.paint(view); assert m.rounded[0]['rect']==(25,6*HOME_ROW+HOME_ROW//2
    '3c4013c003': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:5390 m.paint(view); assert m.rounded[0]['rect']==(25,6*HOME_ROW+HOME_ROW//2
    'c48d53e9b2': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:5391 assert m.call(gap=50)==11 and m.selected(view)==6   # bumped
    '7f02d59ef4': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:5392 assert m.call(gap=O['EDGE_PAUSE_MS'])==11 and m.selected(view)==0
    '6585eb09c4': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:5393 assert m.call(O['KEY_PREV'],gap=50)==11 and m.selected(view)==0   # bu
    '328966b976': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:5394 assert m.call(O['KEY_PREV'],gap=O['EDGE_PAUSE_MS'])==11 and m.selected
    '093f54b391': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:5395 for i in range(5,2,-1): assert m.call(O['KEY_PREV'])==11 and m.selecte
    '11e3b719f5': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:5396 assert m.call(O['KEY_RETURN'])==11 and m.selected(view)==0 and not des
    '2fbfc74242': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:5397 for i in (1,2): assert m.call(gap=1000)==11 and m.selected(view)==i
    '707d9c9fa3': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:5398 assert not m.slides and m.confirm()==11 and m.dispatched()[0][1]==imgs
    '4f7dbcae47.2': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:5402 m=Machine(); view,imgs=home_list(m); bar=m.node('window','system_bar')
    '3eaa96bb9c.3': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:5404 m.byte(syms['g_backlight_status'],0); m.paint(view); assert m.selected
    '56298f1c9a': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:5404 m.byte(syms['g_backlight_status'],0); m.paint(view); assert m.selected
    '6eaf9d30ac': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:5405 paint_bar(); assert ('widget_invalidate_force',view) not in [c[:2] for
    '27669fc1eb': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:5407 paint_bar(); assert ('widget_invalidate_force',view) in [c[:2] for c i
    '3eaa96bb9c.4': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:5408 m.paint(view); assert m.selected(view)==0 and m.rounded[0]['rect']==(2
    'f92f34df2f': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:5408 m.paint(view); assert m.selected(view)==0 and m.rounded[0]['rect']==(2
    '6eaf9d30ac.2': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:5409 paint_bar(); assert ('widget_invalidate_force',view) not in [c[:2] for
    '4f7dbcae47.3': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:5418 m=Machine(); view,imgs=home_list(m); click_target(m,imgs[2]); m.clip=(
    'f43abcdfc1.2': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:5418 m=Machine(); view,imgs=home_list(m); click_target(m,imgs[2]); m.clip=(
    '3eaa96bb9c.5': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:5419 m.paint(view)
    '1a714b6666': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:5422 assert m.rounded[0]['rect']==(25,HOME_ROW//2-3,6,6) and m.icons==bar()
    '3eaa96bb9c.6': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:5424 m.call(); m.paint(view); assert m.selected(view)==1 and m.rounded[0]['
    '06323174d4': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:5424 m.call(); m.paint(view); assert m.selected(view)==1 and m.rounded[0]['
    '3eaa96bb9c.7': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:5427 m.touch(); m.paint(view); assert m.icons==bar() and m.selected(view)==
    '2f7883a1cf': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:5427 m.touch(); m.paint(view); assert m.icons==bar() and m.selected(view)==
    '3eaa96bb9c.8': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:5428 m.byte(syms['g_navbar_status'],1); m.paint(view); assert not m.icons a
    '4f7dbcae47.4': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:5430 m=Machine(); m.config['THEME']='1'; view,imgs=home_list(m); click_targ
    'f43abcdfc1.3': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:5430 m=Machine(); m.config['THEME']='1'; view,imgs=home_list(m); click_targ
    '3eaa96bb9c.9': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:5431 m.paint(view)
    'd9bf25c26c': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:5433 assert m.sel()==(0,0,HOME_LIST_W,HOME_ROW) and m.icons==cbar() and not
    '1801d15492': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:5434 assert m.bands[1][4]==color_t(ACCENTS[0][0]) and loaded(m)==['list_int
    '3eaa96bb9c.10': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:5435 m.call(); m.paint(view); assert m.selected(view)==1 and m.sel()[1]>0 a
    '9089197301': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:5435 m.call(); m.paint(view); assert m.selected(view)==1 and m.sel()[1]>0 a
    'a3a33155a8': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:5552 for virtual in (False,True):
    'f519682145': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6045 for theme in ('0','1'):
    '1903a0a4b3': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6098 assert not [t for t in m.timers.values() if t[1]==payload_syms['home_d
    'd30af9692f': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6099 assert [signed(m.get(m.art+O[k])) for k in ('W_X','W_Y','W_W','W_H')]=
    'ed2910cddb': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6117 assert shown()==['2 of 3','Album 1','-2:05']; passed()
    'afd9cd9841': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6119 m.nodes[slider]['value']=101; assert repaint()==['label_ipod_remain'] 
    '92fb5f57fe': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6130 for mx,v,want in ((3725,0,'-1:02:05'),(3600,0,'-1:00:00'),(3599,0,'-59
    '185fc82d53': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6219 m.nodes[title]['text']='T'*30; assert vis_paint()==['T'*30]
    'a38d0b0245': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6220 m.nodes[title]['text']='T'*40; assert vis_paint()==['T'*33+'\u2026']; 
    '0e46124c66': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6225 assert struct.unpack_from('<I',demo,fileoff(demo,big))[0]==j(payload_s
    '21c8ee7740': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6233 b,bw,alpha=bigcover()
    '14f1bff163': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6234 b.advance(O['BC_MS']-1); assert alpha()==[255,255] and len(b.timers)==
    'fc61cf3cfb': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6236 for _ in range(O['BC_STEPS']):
    '1ebe8d95b1': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6238 n=O['BC_STEPS']; assert steps==[255*(n-k)//n for k in range(1,n+1)] an
    '49afffcc86': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6242 tick(); assert alpha()==[0,0] and not b.timers
    '14f1bff163.2': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6243 b.word(O['MCL_POS'],2); tick(); assert alpha()==[255,255] and len(b.ti
    '14f1bff163.3': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6244 b.advance(O['BC_MS']-1); tick(); assert alpha()==[255,255] and len(b.t
    '21c8ee7740.2': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6245 b,bw,alpha=bigcover(); b.advance(O['BC_MS']+O['BC_STEP_MS'])
    '6047532c93': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6246 f,ctx=b.handler(bw,O['EVT_DESTROY']); b.call(address=f,args=(ctx,b.eve
    '21c8ee7740.3': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6255 b,bw,alpha=bigcover(); shade,title=b.nodes[bw]['children']; b.word(bw+
    'a136c8b8e0': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6255 b,bw,alpha=bigcover(); shade,title=b.nodes[bw]['children']; b.word(bw+
    '0c991e6002': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6255 b,bw,alpha=bigcover(); shade,title=b.nodes[bw]['children']; b.word(bw+
    '951b0913b8': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6256 img=b.node('image','img_bigcover'); b.nodes[bw]['children'].append(img
    '4dfee25352': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6256 img=b.node('image','img_bigcover'); b.nodes[bw]['children'].append(img
    '6c6e19108a': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6262 put(img,*sq); put(shade,sq[0],sq[1]+BC_ART-60,BC_ART,60); put(title,sq
    'b960b73fdc': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6269 assert fit()==[] and geo(img)==sq  # the last track's cover file
    'ce0ce86558': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6270 b.u.mem_write(syms['g_lastcover_url'],bc_track(1)); assert fit()==bc_d
    '06de30b402': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6270 b.u.mem_write(syms['g_lastcover_url'],bc_track(1)); assert fit()==bc_d
    '6e8aa6e345': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6271 x,y,w,h=geo(img); assert w>BC_ART and h==w*900//1600 and x==(375-w)//2
    'cfa65ef6b1': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6272 assert geo(shade)==[x,y+h-60,w,60] and geo(title)==[x+12,y+h-45,w-24,3
    '57475acdcd': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6273 assert fit()==[]
    '04ca846cfd': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6274 put(img,*sq); assert fit()==bc_mv and geo(img)==[x,y,w,h]
    '14633f4497': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6275 b.word(O['MCL_POS'],2); assert fit()==[] and geo(img)==[x,y,w,h]  # a 
    'd12242c8b0': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6277 b.u.mem_write(syms['g_lastcover_url'],bc_track(2)); assert fit()==bc_m
    '74fa668bc8': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6277 b.u.mem_write(syms['g_lastcover_url'],bc_track(2)); assert fit()==bc_m
    '06de30b402.2': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6278 b.image_size=(900,1600); b.byte(syms['g_playcover_type'],2); assert fi
    '1b2b96b553': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6279 x,y,w,h=geo(img); assert h>BC_ART and w==h*900//1600 and x==(375-w)//2
    '74fa668bc8.2': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6281 assert fit()==bc_mv and geo(img)==sq  # Tidal
    'd12242c8b0.2': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6282 b.u.mem_write(syms['g_lastcover_url'],bc_track(2)); b.nodes[img]['imag
    '5ed1bec45f': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6282 b.u.mem_write(syms['g_lastcover_url'],bc_track(2)); b.nodes[img]['imag
    '74fa668bc8.3': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6283 b.nodes[img]['image']='default_bigcover'; assert fit()==bc_mv and geo(
    '55202c380d': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6360 m.call(address=big,args=(bigwin,7,0,0),gap=0)  # ringnav_bigcover keep
    '85fba7fef6': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6367 assert any(0<a<255 for a in pixels.values())
    'c040749ebb': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6401 assert step(m)==11 and m.nodes[m.slider]['value']==105 and m.nodes[m.e
    '5bb8daf98f': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6402 assert m.nodes[m.remain]['text']=='-2:00'
    '1aa8589c73': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6403 assert step(m,gap=1500)==11 and m.nodes[m.slider]['value']==110 and m.
    '262157c160': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6404 assert m.nodes[m.remain]['text']=='-1:55'
    '196370eaa5': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6405 step(m,O['SCRUB_MS']-100,wait=True); assert m.seeks==[] and m.nodes[m.
    '765c8ca948': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6407 for _ in range(12): assert step(m,gap=20)==11
    '984bdeb087': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6408 assert m.nodes[m.slider]['value']-110>12*O['SCRUB_STEP'] and m.seeks==
    '379418464e': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6410 for key,end in ((O['KEY_NEXT'],225),(O['KEY_PREV'],0)):
    'eb38459dd6': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6413 assert step(m,gap=300)==11 and m.nodes[m.slider]['value']==5 and m.see
    '9a89e63f61': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6415 centre(m,50); step(m,O['SCRUB_MS'],wait=True); ended(m,[5]); passed()
    '8101c7dd73': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6423 assert did(m,'mclSetSeek')==[135] and not m.seeks and not did(m,'mclSe
    '74311a4217': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6424 step(m,O['SCRUB_MS']+5000,wait=True); assert not m.seeks and not m.sta
    'e8a1a98ba1': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6427 assert not m.starts and m.nodes[m.slider]['value']==105 and m.timers
    '208a92803b': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6428 m.word(PLAY_STATUS,2); step(m,1000,wait=True); assert not m.starts
    'bf0954d4e1': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6429 step(m,1500,wait=True); assert m.starts==[m.win] and not m.timers; pas
    '838749eac8': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6437 centre(m); step(m); centre(m,50); assert did(m,'mclSetSeek')==[105]
    '83309cf382': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6438 reopen(m); assert m.nodes[m.slider]['value']==105 and m.nodes[m.elapse
    'a216310d6b': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6439 assert did(m,'playing_timer_clear')==[m.win]; step(m,5000,wait=True); 
    '4d6ae59f1b': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6440 centre(m); step(m); assert m.nodes[m.slider]['value']==110; passed()
    '1ec8a51eee': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6445 step(m,O['SCRUB_MS']-1,wait=True); assert m.seeks==[] and not m.starts
    '1acfe38d73': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6446 step(m,1,wait=True); assert m.seeks==[105] and not m.starts  # settle_
    'd93b3914e6': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6447 step(m,O['SCRUB_MS'],wait=True); ended(m,[105]); assert m.nodes[m.slid
    '5d550e5acc': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6447 step(m,O['SCRUB_MS'],wait=True); ended(m,[105]); assert m.nodes[m.slid
    '5d550e5acc.2': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6450 assert m.nodes[m.slider]['value']==105; centre(m,50); step(m,O['SCRUB_
    'd93b3914e6.2': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6450 assert m.nodes[m.slider]['value']==105; centre(m,50); step(m,O['SCRUB_
    'd9b211abf8': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6452 for end in ('centre','timeout','bound'):
    'ee34a125f0': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6459 for end in ('centre','return','touch'):
    'bfd6e55727': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6474 for presses in (1,2):
    '1acfe38d73.2': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6483 m.top=m.node('window','home_page'); step(m); assert m.seeks==[105] and
    'dc662aa100': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6484 step(m,O['SCRUB_MS'],wait=True); assert m.seeks==[105] and m.starts==[
    'b45a784858': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6487 assert m.seeks==[] and not m.starts and not m.timers; passed()
    '1dc9436f15': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6490 for end in ('tick','timeout','return'):
    'e2c6cec663': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6532 for kw in ({'page':0},{'size':0},{'lines':0}):
    '14b0be8b0c': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6542 m=lyric_page(); assert loop(m)==0 and raw(m)==1; m.calls=[]
    'b2cb33d0d6': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6542 m=lyric_page(); assert loop(m)==0 and raw(m)==1; m.calls=[]
    '33e411d7d7': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6543 loop(m,-28); assert settle(m)[-1]==O['BUMP_PX'] and follow(m,0)==O['BU
    '2d450a38f0': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6543 loop(m,-28); assert settle(m)[-1]==O['BUMP_PX'] and follow(m,0)==O['BU
    'ef4b16c7af': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6544 assert ('reset_poweroptions_timer',1,1,1) in [c[:4] for c in m.calls] 
    'b6af0e1f46': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6545 m.word(payload_syms['wheel_held'],0); assert settle(m)[-1]==0; m.word(
    '5810214f81': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6546 follow(m,20); assert settle(m)[-1]==20; m.advance(O['LYRIC_PUSH_MS'])
    'b5e3f6b84f': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6546 follow(m,20); assert settle(m)[-1]==20; m.advance(O['LYRIC_PUSH_MS'])
    '790d5863b0': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6547 loop(m,28); assert settle(m)[-1]==20-O['BUMP_PX'] and follow(m,20)==20
    'ff1b9fa985': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6547 loop(m,28); assert settle(m)[-1]==20-O['BUMP_PX'] and follow(m,20)==20
    '14b0be8b0c.2': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6549 m=lyric_page(); loop(m); loop(m,-28); m.advance(500); loop(m,-28)
    'b1c92aab98': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6549 m=lyric_page(); loop(m); loop(m,-28); m.advance(500); loop(m,-28)
    '33e411d7d7.2': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6549 m=lyric_page(); loop(m); loop(m,-28); m.advance(500); loop(m,-28)
    '33e411d7d7.3': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6549 m=lyric_page(); loop(m); loop(m,-28); m.advance(500); loop(m,-28)
    '66b2f4c87c': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6550 assert settle(m)[-1]==26; m.word(payload_syms['wheel_held'],0); assert
    '8d912b0fb3': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6550 assert settle(m)[-1]==26; m.word(payload_syms['wheel_held'],0); assert
    '14b0be8b0c.3': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6552 m=lyric_page(); assert loop(m)==0 and raw(m)==1; hold(m); m.calls=[]
    'b2cb33d0d6.2': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6552 m=lyric_page(); assert loop(m)==0 and raw(m)==1; hold(m); m.calls=[]
    'bb6c2c76d0': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6552 m=lyric_page(); assert loop(m)==0 and raw(m)==1; hold(m); m.calls=[]
    '09e0ba0cc6': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6553 ys=[loop(m,-28)]+settle(m); steps=[b-a for a,b in zip([0]+ys,ys)]
    '3e40276733': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6553 ys=[loop(m,-28)]+settle(m); steps=[b-a for a,b in zip([0]+ys,ys)]
    '8e7decd10c': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6554 assert ys[-1]==20 and 0<ys[0]<5 and all(0<=s<=4 for s in steps) and st
    'ef4b16c7af.2': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6555 assert ('reset_poweroptions_timer',1,1,1) in [c[:4] for c in m.calls] 
    '46a1858c69': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6556 assert not did(m,'playing_timer_clear') and not did(m,'sleep_ms'); pas
    'ab60e9f310': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6558 for _ in range(3): loop(m,-1)
    '2df204679d': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6559 settle(m); assert y(m)==22; passed()
    'f805f3f1b6': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6559 settle(m); assert y(m)==22; passed()
    '0ca817ce8c': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6561 for _ in range(60): loop(m,-12)
    '84f07b87cf': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6562 assert settle(m)[-1]==110 and m.get(m.lrc+O['VIEW_CONTENT_H'])==288; p
    '866c26dd74': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6564 for _ in range(60): loop(m,12)
    'b6af0e1f46.2': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6565 assert settle(m)[-1]==0; passed()
    '6d4970ef6a': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6567 m=lyric_page(config={'WHEELSENSITIVITY':'100'}); loop(m); hold(m); loo
    'b1c92aab98.2': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6567 m=lyric_page(config={'WHEELSENSITIVITY':'100'}); loop(m); hold(m); loo
    'bb6c2c76d0.2': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6567 m=lyric_page(config={'WHEELSENSITIVITY':'100'}); loop(m); hold(m); loo
    '34c306a7cb': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6567 m=lyric_page(config={'WHEELSENSITIVITY':'100'}); loop(m); hold(m); loo
    'b5e3f6b84f.2': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6567 m=lyric_page(config={'WHEELSENSITIVITY':'100'}); loop(m); hold(m); loo
    '14b0be8b0c.4': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6569 m=lyric_page(); loop(m); loop(m,-56); settle(m); assert y(m)==40
    'b1c92aab98.3': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6569 m=lyric_page(); loop(m); loop(m,-56); settle(m); assert y(m)==40
    '31c2c2ba32': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6569 m=lyric_page(); loop(m); loop(m,-56); settle(m); assert y(m)==40
    '2df204679d.2': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6569 m=lyric_page(); loop(m); loop(m,-56); settle(m); assert y(m)==40
    '8dc2f66aa4': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6569 m=lyric_page(); loop(m); loop(m,-56); settle(m); assert y(m)==40
    '6a61f1355f': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6570 assert follow(m,0)==40; m.advance(O['SCRUB_MS']+1000); assert settle(m
    '8bb44b59c8': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6570 assert follow(m,0)==40; m.advance(O['SCRUB_MS']+1000); assert settle(m
    '40bead0886': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6571 assert not did(m,'playing_timer_clear') and not m.starts; passed()
    '53fab8b81b': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6574 m.nodes[m.slide]['value']=0; loop(m); assert raw(m)==0 and follow(m,70
    'b1c92aab98.4': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6574 m.nodes[m.slide]['value']=0; loop(m); assert raw(m)==0 and follow(m,70
    '76bd6c6315': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6574 m.nodes[m.slide]['value']=0; loop(m); assert raw(m)==0 and follow(m,70
    'f19fc2ec4d': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6575 m.nodes[m.slide]['value']=1; loop(m); assert raw(m)==1 and follow(m,90
    'b1c92aab98.5': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6575 m.nodes[m.slide]['value']=1; loop(m); assert raw(m)==1 and follow(m,90
    '968ad0041e': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6575 m.nodes[m.slide]['value']=1; loop(m); assert raw(m)==1 and follow(m,90
    '29670a53c2': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6576 ys=settle(m); assert ys[-1]==90 and ys[0]<90,ys; passed()
    'a8b1d4e2b0': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6576 ys=settle(m); assert ys[-1]==90 and ys[0]<90,ys; passed()
    '9341c2472a': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6578 for off in (0,1):
    '14b0be8b0c.5': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6584 m=lyric_page(); loop(m); loop(m,-56); settle(m); m.word(O['MCL_POS'],1
    'b1c92aab98.6': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6584 m=lyric_page(); loop(m); loop(m,-56); settle(m); m.word(O['MCL_POS'],1
    '31c2c2ba32.2': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6584 m=lyric_page(); loop(m); loop(m,-56); settle(m); m.word(O['MCL_POS'],1
    '2df204679d.3': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6584 m=lyric_page(); loop(m); loop(m,-56); settle(m); m.word(O['MCL_POS'],1
    '2eadecd1b7': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6584 m=lyric_page(); loop(m); loop(m,-56); settle(m); m.word(O['MCL_POS'],1
    '14b0be8b0c.6': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6588 m=lyric_page(); m.handlers[0x529f0c]='stock_lyric_rows'; loop(m); loop
    'b1c92aab98.7': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6588 m=lyric_page(); m.handlers[0x529f0c]='stock_lyric_rows'; loop(m); loop
    '31c2c2ba32.3': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6588 m=lyric_page(); m.handlers[0x529f0c]='stock_lyric_rows'; loop(m); loop
    '2df204679d.4': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6588 m=lyric_page(); m.handlers[0x529f0c]='stock_lyric_rows'; loop(m); loop
    '801f4c1661': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6589 assert rows(m)==40 and follow(m,0)==40; passed()
    '20a2be18af': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6590 m.word(O['MCL_POS'],2); m.word(m.lrc+O['SCROLL_Y'],60); assert rows(m)
    '037f338d97': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6590 m.word(O['MCL_POS'],2); m.word(m.lrc+O['SCROLL_Y'],60); assert rows(m)
    '5810214f81.2': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6591 follow(m,20); assert settle(m)[-1]==20; passed()  # the follow is back
    'b5e3f6b84f.3': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6591 follow(m,20); assert settle(m)[-1]==20; passed()  # the follow is back
    '39fd93c268': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6594 m=lyric_page(page=0); loop(m); m.pressed=1; loop(m); m.nodes[m.slide][
    'b1c92aab98.8': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6594 m=lyric_page(page=0); loop(m); m.pressed=1; loop(m); m.nodes[m.slide][
    'b1c92aab98.9': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6594 m=lyric_page(page=0); loop(m); m.pressed=1; loop(m); m.nodes[m.slide][
    'f19fc2ec4d.2': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6594 m=lyric_page(page=0); loop(m); m.pressed=1; loop(m); m.nodes[m.slide][
    'b1c92aab98.10': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6594 m=lyric_page(page=0); loop(m); m.pressed=1; loop(m); m.nodes[m.slide][
    '20a2be18af.2': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6595 m.word(m.lrc+O['SCROLL_Y'],60); loop(m); m.pressed=0; loop(m); follow(
    'b1c92aab98.11': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6595 m.word(m.lrc+O['SCROLL_Y'],60); loop(m); m.pressed=0; loop(m); follow(
    'b1c92aab98.12': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6595 m.word(m.lrc+O['SCROLL_Y'],60); loop(m); m.pressed=0; loop(m); follow(
    'a8da2bfe8f': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6595 m.word(m.lrc+O['SCROLL_Y'],60); loop(m); m.pressed=0; loop(m); follow(
    'b6af0e1f46.3': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6595 m.word(m.lrc+O['SCROLL_Y'],60); loop(m); m.pressed=0; loop(m); follow(
    '14b0be8b0c.7': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6596 m=lyric_page(); loop(m); a=m.alloc(0x80); m.word(m.lrc+O['VIEW_ANIMATO
    'b1c92aab98.13': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6596 m=lyric_page(); loop(m); a=m.alloc(0x80); m.word(m.lrc+O['VIEW_ANIMATO
    '0e9008d0c7': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6596 m=lyric_page(); loop(m); a=m.alloc(0x80); m.word(m.lrc+O['VIEW_ANIMATO
    'b1c92aab98.14': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6596 m=lyric_page(); loop(m); a=m.alloc(0x80); m.word(m.lrc+O['VIEW_ANIMATO
    'bc3398d579': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6597 assert m.get(m.lrc+O['VIEW_ANIMATOR'])==0 and ('widget_animator_destro
    '14b0be8b0c.8': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6599 m=lyric_page(); m.handlers[0x529f0c]='stock_lyric_rows'; loop(m); loop
    'b1c92aab98.15': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6599 m=lyric_page(); m.handlers[0x529f0c]='stock_lyric_rows'; loop(m); loop
    '31c2c2ba32.4': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6599 m=lyric_page(); m.handlers[0x529f0c]='stock_lyric_rows'; loop(m); loop
    '2df204679d.5': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6599 m=lyric_page(); m.handlers[0x529f0c]='stock_lyric_rows'; loop(m); loop
    '53fab8b81b.2': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6600 m.nodes[m.slide]['value']=0; loop(m); assert follow(m,20)==20  # off t
    'b1c92aab98.16': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6600 m.nodes[m.slide]['value']=0; loop(m); assert follow(m,20)==20  # off t
    '69eb271416': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6600 m.nodes[m.slide]['value']=0; loop(m); assert follow(m,20)==20  # off t
    'b1c92aab98.17': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6601 m.byte(syms['g_backlight_status'],0); loop(m); m.word(O['MCL_POS'],2);
    '504ef5d85c': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6601 m.byte(syms['g_backlight_status'],0); loop(m); m.word(O['MCL_POS'],2);
    '20a2be18af.3': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6602 m.word(m.lrc+O['SCROLL_Y'],60); assert rows(m)==0  # a stale follow, t
    'b750c0fe2e': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6602 m.word(m.lrc+O['SCROLL_Y'],60); assert rows(m)==0  # a stale follow, t
    'b1c92aab98.18': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6603 m.byte(syms['g_backlight_status'],1); loop(m); m.pressed=1; loop(m); m
    'b1c92aab98.19': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6603 m.byte(syms['g_backlight_status'],1); loop(m); m.pressed=1; loop(m); m
    'f19fc2ec4d.3': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6603 m.byte(syms['g_backlight_status'],1); loop(m); m.pressed=1; loop(m); m
    'b1c92aab98.20': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6603 m.byte(syms['g_backlight_status'],1); loop(m); m.pressed=1; loop(m); m
    'fba181f823': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6604 m.word(m.lrc+O['SCROLL_Y'],20); loop(m); m.pressed=0; loop(m)
    'b1c92aab98.21': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6604 m.word(m.lrc+O['SCROLL_Y'],20); loop(m); m.pressed=0; loop(m)
    'b1c92aab98.22': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6604 m.word(m.lrc+O['SCROLL_Y'],20); loop(m); m.pressed=0; loop(m)
    'a8da2bfe8f.2': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6605 follow(m,0); assert settle(m)[-1]==0; passed()
    'b6af0e1f46.4': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6605 follow(m,0); assert settle(m)[-1]==0; passed()
    '14b0be8b0c.9': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6607 m=lyric_page(); loop(m); hold(m); loop(m,-36); assert settle(m,200)[-1
    'b1c92aab98.23': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6607 m=lyric_page(); loop(m); hold(m); loop(m,-36); assert settle(m,200)[-1
    'bb6c2c76d0.3': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6607 m=lyric_page(); loop(m); hold(m); loop(m,-36); assert settle(m,200)[-1
    'ad03b1ffac': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6607 m=lyric_page(); loop(m); hold(m); loop(m,-36); assert settle(m,200)[-1
    'cacd8b8fb7': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6607 m=lyric_page(); loop(m); hold(m); loop(m,-36); assert settle(m,200)[-1
    '29670a53c2.2': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6608 m.word(payload_syms['wheel_held'],0); ys=settle(m); assert ys[-1]==20 
    'dcd71d1411': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6608 m.word(payload_syms['wheel_held'],0); ys=settle(m); assert ys[-1]==20 
    '14f083728c': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6609 m.word(payload_syms['wheel_held'],1); loop(m,-50); assert settle(m)[-1
    'b8286a7454': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6609 m.word(payload_syms['wheel_held'],1); loop(m,-50); assert settle(m)[-1
    'e94ad641c3': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6610 m.word(payload_syms['wheel_held'],0); assert settle(m)[-1]==70 and fol
    '14b0be8b0c.10': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6612 m=lyric_page(); loop(m); hold(m); loop(m,-36); m.word(payload_syms['wh
    'b1c92aab98.24': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6612 m=lyric_page(); loop(m); hold(m); loop(m,-36); m.word(payload_syms['wh
    'bb6c2c76d0.4': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6612 m=lyric_page(); loop(m); hold(m); loop(m,-36); m.word(payload_syms['wh
    'ad03b1ffac.2': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6612 m=lyric_page(); loop(m); hold(m); loop(m,-36); m.word(payload_syms['wh
    'b5e3f6b84f.4': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6612 m=lyric_page(); loop(m); hold(m); loop(m,-36); m.word(payload_syms['wh
    '187abcda7f': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6613 m.word(payload_syms['wheel_held'],1); m.word(m.lrc+O['SCROLL_Y'],30); 
    'b1c92aab98.25': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6613 m.word(payload_syms['wheel_held'],1); m.word(m.lrc+O['SCROLL_Y'],30); 
    '3470cf7a54': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6614 assert settle(m)[-1]==30; passed()  # not the wheel's doing: no snap
    '35111b43eb': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6622 for off,on in ((other,back),(dark,lambda m: dark(m,1)),(touch,lambda m
    '14b0be8b0c.11': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6629 m=lyric_page(); loop(m); m.pressed=1; loop(m); m.word(m.lrc+O['SCROLL_
    'b1c92aab98.26': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6629 m=lyric_page(); loop(m); m.pressed=1; loop(m); m.word(m.lrc+O['SCROLL_
    'b1c92aab98.27': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6629 m=lyric_page(); loop(m); m.pressed=1; loop(m); m.word(m.lrc+O['SCROLL_
    '4178cb65af': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6629 m=lyric_page(); loop(m); m.pressed=1; loop(m); m.word(m.lrc+O['SCROLL_
    '6a61f1355f.2': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6630 assert follow(m,0)==40; m.pressed=0; loop(m); assert follow(m,0)==40 a
    'b1c92aab98.28': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6630 assert follow(m,0)==40; m.pressed=0; loop(m); assert follow(m,0)==40 a
    '78cc369f84': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6630 assert follow(m,0)==40; m.pressed=0; loop(m); assert follow(m,0)==40 a
    '14b0be8b0c.12': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6631 m=lyric_page(); loop(m); m.pressed=1; loop(m); m.pressed=0; loop(m); f
    'b1c92aab98.29': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6631 m=lyric_page(); loop(m); m.pressed=1; loop(m); m.pressed=0; loop(m); f
    'b1c92aab98.30': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6631 m=lyric_page(); loop(m); m.pressed=1; loop(m); m.pressed=0; loop(m); f
    'b1c92aab98.31': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6631 m=lyric_page(); loop(m); m.pressed=1; loop(m); m.pressed=0; loop(m); f
    '5810214f81.3': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6631 m=lyric_page(); loop(m); m.pressed=1; loop(m); m.pressed=0; loop(m); f
    'b5e3f6b84f.5': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6631 m=lyric_page(); loop(m); m.pressed=1; loop(m); m.pressed=0; loop(m); f
    '14b0be8b0c.13': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6632 m=lyric_page(); loop(m); m.top=m.node('window','home_page'); m.pressed
    'b1c92aab98.32': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6632 m=lyric_page(); loop(m); m.top=m.node('window','home_page'); m.pressed
    'b1c92aab98.33': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6632 m=lyric_page(); loop(m); m.top=m.node('window','home_page'); m.pressed
    '4178cb65af.2': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6632 m=lyric_page(); loop(m); m.top=m.node('window','home_page'); m.pressed
    'b1c92aab98.34': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6633 m.pressed=0; loop(m); m.top=m.win; loop(m); follow(m,0); assert settle
    'b1c92aab98.35': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6633 m.pressed=0; loop(m); m.top=m.win; loop(m); follow(m,0); assert settle
    'a8da2bfe8f.3': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6633 m.pressed=0; loop(m); m.top=m.win; loop(m); follow(m,0); assert settle
    'b6af0e1f46.5': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6633 m.pressed=0; loop(m); m.top=m.win; loop(m); follow(m,0); assert settle
    '14b0be8b0c.14': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6636 m=lyric_page()
    '94795f3766': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6637 assert step(m)==11 and y(m)==0 and settle(m)[-1]==20
    'b033261e7d': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6639 for _ in range(5): assert step(m,gap=200)==11; ys.append(settle(m)[-1]
    'cdd63e7186': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6640 assert ys==[70,90,110,110,110],ys
    '8d288139c4': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6641 for _ in range(3): assert step(m,O['KEY_PREV'],gap=200)==11
    '84149054c2': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6642 assert settle(m)[-1]==20 and not did(m,'playing_timer_clear') and not 
    '14b0be8b0c.15': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6645 m=lyric_page(); centre(m); m.nodes[m.slide]['value']=0; step(m); m.nod
    '53fab8b81b.3': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6645 m=lyric_page(); centre(m); m.nodes[m.slide]['value']=0; step(m); m.nod
    'f19fc2ec4d.4': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6645 m=lyric_page(); centre(m); m.nodes[m.slide]['value']=0; step(m); m.nod
    'f2206cb84d': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6646 assert step(m)==11 and m.seeks==[105] and settle(m)[-1]==20
    'bf0954d4e1.2': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6647 step(m,O['SCRUB_MS'],wait=True); assert m.starts==[m.win] and not m.ti
    '14b0be8b0c.16': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6650 m=lyric_page(); loop(m); hold(m); loop(m,-28); settle(m)
    'b1c92aab98.36': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6650 m=lyric_page(); loop(m); hold(m); loop(m,-28); settle(m)
    'bb6c2c76d0.5': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6650 m=lyric_page(); loop(m); hold(m); loop(m,-28); settle(m)
    '33e411d7d7.4': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6650 m=lyric_page(); loop(m); hold(m); loop(m,-28); settle(m)
    '2df204679d.6': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6650 m=lyric_page(); loop(m); hold(m); loop(m,-28); settle(m)
    '87cd1c1941': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6652 assert follow(m,0)==20 and not m.starts and not m.timers; passed()
    'b1c92aab98.37': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6654 loop(m); assert raw(m)==0 and not m.starts and not m.timers; passed()
    'f670786de6': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6654 loop(m); assert raw(m)==0 and not m.starts and not m.timers; passed()
    '4bf024fbb1': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8330 m.art_size=(319,319); m.pixels.clear(); paint_home(); c=tex_of(319,319
    '9dbe947d5c': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8331 assert m.nodes[m.art]['image']=='' and [signed(m.get(m.art+O[k])) for 
    'f55ac103ea': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8332 assert (c['u0'],c['v0'],c['rx'],c['ry'])==((290-PW)//2,0,29,29) and no
    '8cef526eea': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8333 assert drawn()==framed(c,0) and ('bitmap_lock_buffer_for_write',) in [
    '214b860d29': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8334 assert drawn()==framed(c,0) and ('bitmap_lock_buffer_for_write',) not 
    'd78c984174': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8335 paint_home(); m.advance(0); assert len(drifts())==1  # it arms on the 
    '4bf4c098d9': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8336 m.calls.clear(); m.advance(TICK); assert set(invalidated())=={(m.home,
    'fb9e654bc7': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8337 assert drawn()==framed(c,TICK)!=framed(c,0)  # a tick moves it by a fr
    '1b40e39f5c': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8338 m.advance(1000-TICK); assert drawn()==framed(c,1000) and len(drifts())
    '7684b0f340': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8339 m.advance(TICK); instructions[0]=0; assert drawn()==framed(c,1000+TICK
    '8fc3352f1c': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8341 tid=next(t for t,v in m.timers.items() if v[1]==payload_syms['home_dri
    '41e7830027': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8341 tid=next(t for t,v in m.timers.items() if v[1]==payload_syms['home_dri
    '20aa5be228': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8342 m.advance(5000); t=1000+TICK+O['DRIFT_MAX_STEP_MS']; assert drawn()==f
    '8856eca524': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8345 for cover_up in (lambda: setattr(m,'top',np),lambda: m.byte(syms['g_ba
    '20aa5be228.2': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8358 paint_home(); assert drawn()==framed(c,t); paint_home(); assert len(dr
    'd78c984174.2': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8358 paint_home(); assert drawn()==framed(c,t); paint_home(); assert len(dr
    'bb392fd3a1': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8360 instructions[0]=0; paint_home(); filter_cost=instructions[0]; c=tex_of
    '0dbb8cdbd9': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8361 assert drawn()==framed(c,t) and len(drifts())==1
    'b04fddfbd0': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8363 instructions[0]=0; paint_home(); big_cost=instructions[0]; m.u.hook_de
    '20aa5be228.3': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8363 instructions[0]=0; paint_home(); big_cost=instructions[0]; m.u.hook_de
    'e71e90c7e3': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8367 assert not drifts() and m.nodes[m.art]['image'].endswith('externpic.jp
    '4f7dbcae47.5': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8469 m=Machine(); view,imgs=home_list(m); begin(m,view)
    'a1af47494f': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8470 labels=[m.nodes[m.get(img+O['W_PARENT'])]['children'][0] for img in im
    '3d53ed3386': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8472 end(m,labels[0]); begin(m,labels[1]); assert style_color(m,0xffffffff)
    '6593826291': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8514 for name,column in (('text_color',3),('bg_color',2)):
    '9e5dd4854f': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8735 for name in ('local_album','local_photos','list_folder','list_tidal','
    '1068b5c50c': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8772 m,main,_=display({},sub=0)
    'c6052dee0d': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8773 kids=m.nodes[main]['children']
    '487c8eb5c1': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8774 assert len(kids)==6 and [row_text(r) for r in kids[3:]]==['Appearance'
    '2dff49cb69': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8775 assert m.icons_set==['system_display','list_into','playset_covermode',
    'c99a4ebc97': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8776 f,ctx=m.handler(m.nodes[kids[4]]['children'][0],O['EVT_CLICK']); m.cal
    'e8cb08926c': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8777 assert m.call(address=f,args=(ctx,m.event,0,0),gap=0)==0 and m.opened[
    '36b49d8f56': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8780 cfv=display_page(m,2); cf,cf_sort,cf_refresh=m.nodes[cfv]['children']
    '5db2661012': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8780 cfv=display_page(m,2); cf,cf_sort,cf_refresh=m.nodes[cfv]['children']
    'f6375d0298': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8781 assert m.icons_set==['playset_covermode','playset_covermode','system_u
    '15567d5dec': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8784 assert [row_text(r) for r in (shortcut,hold,qs)]==['Shortcut: Rockbox'
    'f92a41034a': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8785 view=display_page(m,1); rows=setting_rows(m,view)
    'dcddcb57a6': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8785 view=display_page(m,1); rows=setting_rows(m,view)
    '85172db86c': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8786 kids=m.nodes[view]['children']; light,corners,centred=kids[1],kids[3],
    '944032aee2': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8787 assert kids==[rows[3],light,rows[0],corners,rows[1],rows[2],centred] a
    'c9c6fdc8c1': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8788 assert m.icons_set==['system_display','system_display','system_display
    '0ac48111d4': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8789 buttons=[m.nodes[r]['children'][0] for r in rows]; labels=[m.nodes[b][
    '0e824e3e4f': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8789 buttons=[m.nodes[r]['children'][0] for r in rows]; labels=[m.nodes[b][
    '549cb92260': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8790 for b,l in zip(buttons,labels):
    '2ab19091a5': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8797 keep_label=m.nodes[m.nodes[keep_lit]['children'][0]]['children'][1]; a
    '70bf24c794': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8797 keep_label=m.nodes[m.nodes[keep_lit]['children'][0]]['children'][1]; a
    '4d56f7c40c': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8798 f,ctx=m.handler(m.nodes[keep_lit]['children'][0],O['EVT_CLICK']); m.ca
    '86b4e73d17': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8799 assert m.call(address=f,args=(ctx,m.event,0,0),gap=0)==0 and not did(m
    '1bbb79bed9': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8800 assert [(c[1],m.text(c[2]),m.text(c[3])) for c in m.calls if c[0]=='wr
    '8271bfe8ff.10': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8801 m.call(address=f,args=(ctx,m.event,0,0),gap=0)
    '86b4e73d17.2': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8805 assert m.call(address=f,args=(ctx,m.event,0,0),gap=0)==0 and not did(m
    '49995443e1': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8806 assert [(c[1],m.text(c[2]),m.text(c[3])) for c in m.calls if c[0]=='wr
    '8271bfe8ff.11': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8807 m.call(address=f,args=(ctx,m.event,0,0),gap=0)
    '341ae680b0': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8810 centred_label=m.nodes[m.nodes[centred]['children'][0]]['children'][1];
    'cb11270062': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8810 centred_label=m.nodes[m.nodes[centred]['children'][0]]['children'][1];
    '41b6025c64': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8811 f,ctx=m.handler(m.nodes[centred]['children'][0],O['EVT_CLICK']); m.cal
    '86b4e73d17.3': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8812 assert m.call(address=f,args=(ctx,m.event,0,0),gap=0)==0 and not did(m
    '36ad551169': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8813 assert [(c[1],m.text(c[2]),m.text(c[3])) for c in m.calls if c[0]=='wr
    '3a615939a6': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8818 assert loaded('playing_page')==['playing_page_stock'] and loaded('home
    '8271bfe8ff.12': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8819 m.call(address=f,args=(ctx,m.event,0,0),gap=0); assert loaded('playing
    'a153bcc628': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8821 cf_label=m.nodes[m.nodes[cf]['children'][0]]['children'][1]; assert m.
    '6ab6271070': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8821 cf_label=m.nodes[m.nodes[cf]['children'][0]]['children'][1]; assert m.
    'd3ef113228': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8822 f,ctx=m.handler(m.nodes[cf]['children'][0],O['EVT_CLICK']); m.calls=[]
    'cd883ae115': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8823 assert m.call(address=f,args=(ctx,m.event,0,0),gap=0)==0 and m.nodes[c
    '2a4b480d6f': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8824 assert [(c[1],m.text(c[2]),m.text(c[3])) for c in m.calls if c[0]=='wr
    '8271bfe8ff.13': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8825 m.call(address=f,args=(ctx,m.event,0,0),gap=0); assert m.nodes[cf_labe
    '115a769ae0': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8825 m.call(address=f,args=(ctx,m.event,0,0),gap=0); assert m.nodes[cf_labe
    '8271bfe8ff.14': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8826 m.call(address=f,args=(ctx,m.event,0,0),gap=0); assert m.nodes[cf_labe
    '6ab6271070.2': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8826 m.call(address=f,args=(ctx,m.event,0,0),gap=0); assert m.nodes[cf_labe
    '5350877c9a': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8829 sort_label,refresh_label=(m.nodes[m.nodes[r]['children'][0]]['children
    '1f952a4891': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8830 assert m.nodes[sort_label]['text']=='Coverflow Sort: Album' and m.node
    'acc55bb4b8': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8831 f,ctx=m.handler(m.nodes[cf_refresh]['children'][0],O['EVT_CLICK']); m.
    'd9ba565d32': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8832 assert m.call(address=f,args=(ctx,m.event,0,0),gap=0)==0 and m.toasts[
    '26bda3c14e': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8833 assert [m.text(c[1]) for c in m.calls if c[0]=='opendir@GLIBC_2.0']==[
    '1cdc7d997d': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8842 assert texts()==['Accent: Ivory','Home: Split','Battery: Icon','Theme:
    '198848f550': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8848 home=asset_tree(m,HOME_PAGE)
    'a7f54dea42': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8850 m.call(address=HOOKS['home_page_init'][0],args=(home,0,0,0),gap=0)
    'd3cec3151b': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8851 art=named(m,home,'img_homeart')
    '84fb5c2e21': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8876 shortcut_button=m.nodes[shortcut]['children'][0]
    '5622a7e908': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8877 sf,sc=m.handler(shortcut_button,O['EVT_CLICK'])
    'e5e97b6d36': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8878 for label in ('Favorites','Shuffle','Rated Albums','Artists','Albums',
    '927dc434cc': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8882 writes=click(1); assert [(w[0],m.text(w[2])) for w in writes]==[(1,'HO
    'a0f267beae': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8882 writes=click(1); assert [(w[0],m.text(w[2])) for w in writes]==[(1,'HO
    '3fd3d27d9c': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8891 corners_label=m.nodes[m.nodes[corners]['children'][0]]['children'][1];
    '0c075ea462': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8891 corners_label=m.nodes[m.nodes[corners]['children'][0]]['children'][1];
    '88774fb87c': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8893 assert corners_switch()==['switch_off']
    '66dc56914a': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8894 f,ctx=m.handler(m.nodes[corners]['children'][0],O['EVT_CLICK']); m.cal
    '191084d657': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8895 assert m.call(address=f,args=(ctx,m.event,0,0),gap=0)==0 and corners_s
    '445cf125f8': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8896 assert [(c[1],m.text(c[3])) for c in m.calls if c[0]=='write_int_confi
    '8329427fda': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8898 light_label=m.nodes[m.nodes[light]['children'][0]]['children'][1]; ass
    'a206a7a356': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8898 light_label=m.nodes[m.nodes[light]['children'][0]]['children'][1]; ass
    '7553168288': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8899 f,ctx=f_light,ctx_light=m.handler(m.nodes[light]['children'][0],O['EVT
    '91dc641367': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8900 for value,text in ((1,'On'),(2,'Auto'),(0,'Off')):
    'f1eae9f6ce': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8915 writes=click(3); assert [(w[0],m.text(w[1]),m.text(w[2])) for w in wri
    'fd2f07fc93': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8915 writes=click(3); assert [(w[0],m.text(w[1]),m.text(w[2])) for w in wri
    'd54d44a9a7': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8916 assert corners_switch()==['switch_off'] and m.nodes[light_label]['text
    'c181110dc5': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8917 assert ('image_manager_unload_all',0x1000500) in [c[:2] for c in m.cal
    '85172db86c.2': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8918 kids=m.nodes[view]['children']
    '944032aee2.2': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8919 assert kids==[rows[3],light,rows[0],corners,rows[1],rows[2],centred] a
    '044cdebfbf': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8920 assert texts()==['Accent: Cobalt','Home: Split','Battery: Icon','Theme
    'baa6580069': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8920 assert texts()==['Accent: Cobalt','Home: Split','Battery: Icon','Theme
    'd652ea7b25.2': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8922 m.paint(view); assert m.selected(view)==0; passed()
    'bb0f2639c0': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8926 for _ in range(2): m.call(address=f_light,args=(ctx_light,m.event,0,0)
    'a206a7a356.2': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8927 assert m.nodes[light_label]['text']=='Light Mode: Off'
    '231e4ded71': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8928 for value,name in ((5,'Tangerine'),(6,'Plum'),(8,'Green'),(0,'Graphite
    'f1eae9f6ce.2': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8936 writes=click(3); assert [(w[0],m.text(w[2])) for w in writes]==[(0,'TH
    '304a770053': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8936 writes=click(3); assert [(w[0],m.text(w[2])) for w in writes]==[(0,'TH
    '26a9fde919': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8937 assert texts()[3]=='Theme: Minimal' and corners_switch()==['switch_on'
    'd652ea7b25.3': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8938 m.paint(view); assert m.selected(view)==0
    '85172db86c.3': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8939 kids=m.nodes[view]['children']
    '78b2a6d980': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8940 assert kids==[rows[3],light,rows[0],corners,rows[1],rows[2],centred] a
    '466012b4b4.3': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8941 home_bounds(False)
    '6c1776f92b': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8942 m.paint(view); assert not m.bands and m.rounded[0]['color']==color_t(A
    'a573372f36': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8944 m.call(address=f_light,args=(ctx_light,m.event,0,0),gap=0); m.call(add
    'a573372f36.2': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8944 m.call(address=f_light,args=(ctx_light,m.event,0,0),gap=0); m.call(add
    '9406000021': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8945 assert m.nodes[light_label]['text']=='Light Mode: Auto'
    'f49ec85af4': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8946 for theme in ('Classic','Minimal'):
    'a573372f36.3': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8948 m.call(address=f_light,args=(ctx_light,m.event,0,0),gap=0); assert m.n
    'a206a7a356.3': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8948 m.call(address=f_light,args=(ctx_light,m.event,0,0),gap=0); assert m.n
    '472cbcd7f9': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8950 for value,name in ((1,'Crimson'),(2,'Tidal'),(3,'Champagne'),(4,'Cobal
    '3264b12e96': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8954 click(3); home_bounds(False,True); click(3); home_bounds(False); passe
    'baa6580069.3': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8954 click(3); home_bounds(False,True); click(3); home_bounds(False); passe
    '3264b12e96.2': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8954 click(3); home_bounds(False,True); click(3); home_bounds(False); passe
    '466012b4b4.4': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8954 click(3); home_bounds(False,True); click(3); home_bounds(False); passe
    '63150259f5': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8956 for value,name in ((1,'Percent'),(2,'Icon + Percent'),(3,'Percent Insi
    'f529705857': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8960 m,view,rows=display({'ACCENT':'2','HOME':'1','BATTERY':'2','SHORTCUT':
    '47417148e4': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8960 m,view,rows=display({'ACCENT':'2','HOME':'1','BATTERY':'2','SHORTCUT':
    'e44a70fe75': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8960 m,view,rows=display({'ACCENT':'2','HOME':'1','BATTERY':'2','SHORTCUT':
    'e8b43de32c': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8961 m,view,rows=display({'BATTERY':'3'}); assert m.nodes[m.nodes[m.nodes[r
    'b43f0ec9d3': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8961 m,view,rows=display({'BATTERY':'3'}); assert m.nodes[m.nodes[m.nodes[r
    'e684a09ad2': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8962 m,view,rows=display({'ACCENT':'2','HOME':'1','THEME':'1'}); got=[m.nod
    '47417148e4.2': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8962 m,view,rows=display({'ACCENT':'2','HOME':'1','THEME':'1'}); got=[m.nod
    '49c403d473': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8963 assert got==['Accent: Tidal','Home: Full','Battery: Icon','Theme: Clas
    'b5c738c80f': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8993 m,view,_=display({},sub=0)
    '3d40ff6b9b': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8996 assert m.selected(view)==3 and m.confirm()==11 and m.dispatched()[0][1
    'b32ce1e463': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9000 assert at(0x613ee8,4)==bytes.fromhex('1cc7a524') and at(0x77c71c,5)==b
    'dca5c4a74d': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9083 for classic in (0,1):
    '4a05eb9365': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9098 CONFIG.clear(); m,view=settings('display',sub=1); items=m.nodes[view][
    'a993d66116': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9098 CONFIG.clear(); m,view=settings('display',sub=1); items=m.nodes[view][
    '01f9e7d40a': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9098 CONFIG.clear(); m,view=settings('display',sub=1); items=m.nodes[view][
    'e0a4fa8337': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9103 previous=m.node('window','sysset_page',[cached,library]); m.nodes[m.wm
    'e1e8ddc1d0': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9104 for classic in (1,0,1,0,1):  # each a click on Theme, from Minimal
    'd83a7b5843': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9122 m,view=settings(0x4cbcc4,default=72); before=tree(m,view); lay(m,view)
    '9aec68f85c': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9122 m,view=settings(0x4cbcc4,default=72); before=tree(m,view); lay(m,view)
    '075f869521': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9122 m,view=settings(0x4cbcc4,default=72); before=tree(m,view); lay(m,view)
    'db4762b8ba': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9122 m,view=settings(0x4cbcc4,default=72); before=tree(m,view); lay(m,view)
    'ba217aad41': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9123 assert [r[1] for r in after]==[r[1] for r in before] and all(r[0][3]==
    '6f053ba547': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9125 m,view=settings(0x4cbcc4); odd=m.node('list_item'); other=m.node('butt
    'f8aa851a1b': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9128 m.nodes[view]['children'].append(odd); lay(m,view)
    '075f869521.2': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9128 m.nodes[view]['children'].append(odd); lay(m,view)
    '6f053ba547.2': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9132 m,view=settings(0x4cbcc4); lay(m,view); items=m.nodes[view]['children'
    '075f869521.3': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9132 m,view=settings(0x4cbcc4); lay(m,view); items=m.nodes[view]['children'
    'a993d66116.2': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9132 m,view=settings(0x4cbcc4); lay(m,view); items=m.nodes[view]['children'
    '375301fb60': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9133 buttons=[m.nodes[i]['children'][0] for i in items]
    'd652ea7b25.4': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9134 m.paint(view); assert m.selected(view)==0
    '588932ae9b': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9135 for k in range(1,len(items)):
    '330e6086e6.2': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9140 assert m.confirm()==11 and m.dispatched()[0][1]==buttons[-1]; passed()
    '638c1bd20c': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9141 m.click(buttons[2]); assert m.selected(view)==2; passed()
    'ecbccc89c2': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9141 m.click(buttons[2]); assert m.selected(view)==2; passed()
    'f9bab94df3': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9145 m,view,rows=display({'ACCENT':'2'}); m.paint(view)
    '8fe2090d8d': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9146 assert not m.bands and m.rounded[-1]['color']==color_t(0xeeeeec); pass
    '5ffc96853b': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9147 m,view,rows=display({'ACCENT':'2','THEME':'1'}); m.paint(view)
    'fe173a1c41': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9148 assert [m.bands[i][4] for i in (0,1,47)]==[color_t(ACCENTS[2][i]) for 
    '91e3bc677a': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9149 f,ctx=m.handler(m.nodes[rows[0]]['children'][0],O['EVT_CLICK']); m.cal
    '8271bfe8ff.15': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9149 f,ctx=m.handler(m.nodes[rows[0]]['children'][0],O['EVT_CLICK']); m.cal
    'b42e571763': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9150 m.paint(view); assert [m.bands[i][4] for i in (0,1,47)]==[color_t(ACCE
    'c547892cd4.2': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9158 assert m.nodes[m.slider][FG]==-1; centre(m,50); assert m.nodes[m.slide
    'f1671ac043': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9163 for config,listw,roww,shown in (({'HOME':'1'},375,O['HOME_FULL_ROW'],0
    '34e658d714': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9242 def turn(m,w,gaps,key=NEXT):
    '18b998b1ce': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9248 for table in (False,True):
    '4f7dbcae47.6': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9258 m=Machine(); view,imgs=home_list(m); click_target(m,imgs[2]); m.paint(
    'f43abcdfc1.4': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9258 m=Machine(); view,imgs=home_list(m); click_target(m,imgs[2]); m.paint(
    '5bd5ab63dd': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9259 assert turn(m,view,(1000,100,100,1000,100,100,100,400))==[1,2,3,4,5,6,
    'f3c2c3d56a': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9260 assert m.get(view+O['SCROLL_Y'])==0 and turn(m,view,(1000,400,100,100)
    '99f82b57ad': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9261 assert m.confirm()==11 and m.dispatched()[0][1]==imgs[4]; passed()
    'a4f0a31c20': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9277 m,w,es=ring()
    '65fe61354e': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9278 for gap in (100,100,200,200,O['EDGE_PAUSE_MS']-1):
    '1b4ec485e2.2': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9281 assert m.call(gap=O['EDGE_PAUSE_MS'])==11 and m.selected(w)==0 and m.g
    '13f330a7eb.4': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9282 m.paint(w,gap=0); assert m.sel()==(0,0,240,48)
    'ffae34869d': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9283 assert turn(m,w,(100,100,100))==[1,2,3] and turn(m,w,(100,100,100),PRE
    '5ee9fdb957': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9284 assert m.call(PREV,gap=100)==11 and m.selected(w)==0
    '2425d1664c.2': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9285 m.paint(w,gap=0); assert m.sel()==(0,6,240,48)   # bumped down at the 
    '6d8ba8f135': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9286 assert m.call(PREV,gap=O['EDGE_PAUSE_MS'])==11 and m.selected(w)==5; p
    '967f2416f4': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9288 m,w,es=ring('display_page')
    '472f32aa51': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9289 for gap in (100,O['EDGE_PAUSE_MS'],1000):
    '09bc2f5c69': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9302 m,view=home_machine(); got=[]
    '1e0231bb5a': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9303 for gap in (1000,100,100,1000):
    'adb643c360': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9306 assert got==[(1,1),(1,2),(1,3),(1,4)],got; passed()
    '09bc2f5c69.2': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9309 m,view=home_machine()
    '704d00c0fb': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9310 assert [tick(m) for _ in range(6)]==[1]*6 and m.selected(view)==6
    '324aa1f5c5': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9311 assert [tick(m,gap=gap) for gap in (1000,50,400,100)]==[0,0,1,1] and m
    '09bc2f5c69.3': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9316 m,view=home_machine(); seen=[]
    '314f710b6d': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9317 m.u.hook_add(UC_HOOK_CODE,lambda u,a,size,x: seen.append(u.mem_read(TO
    'b76d3b1aa8': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9318 assert tick(m)==1 and seen==[0,1] and tick(m,gap=100)==1 and seen==[0,
    '7548179734': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9322 assert [tick(m,gap=100) for _ in range(16)]==[1]*16 and m.selected(w)=
    'c2b318887d': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9325 assert sum(tick(m) for _ in range(5))==5 and m.selected(w)==5
    'd7e731a709': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9326 assert [tick(m,gap=gap) for gap in (100,200,200,O['EDGE_PAUSE_MS']-1)]
    '73a22f538a': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9327 assert tick(m,gap=O['EDGE_PAUSE_MS'])==1 and m.selected(w)==0
    'e6289a625f': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9328 assert tick(m,gap=100)==1 and m.selected(w)==1; passed()
    '4b6b6e58a9': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9333 for field in ('pressed','animating'):
    '54cd6b0199': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9335 m.advance(O['HOLD_POLL_MS']); assert m.selected(w)==1 and not m.timers
    '6a2bf94683': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9336 assert press(m,RETURN)==1 and lift(m,RETURN)==0 and m.ret==0 and m.u.m
    '3aed5d6ed8': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9337 assert tick(m)==0 and m.ret==11 and m.selected(w)==1
    '02b19578f8': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9338 debounced(m); assert tick(m)==1 and m.selected(w)==2; passed()
    'be34ff1914': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9338 debounced(m); assert tick(m)==1 and m.selected(w)==2; passed()
    '7d9597fb67': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9341 assert [tick(m) for _ in range(6)]==[1]*6 and m.selected(w)==6
    '19e6f5cf3b': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9343 assert m.selected(w2)==6 and not buzzes(m); passed()
    '4e6d8c3707': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9346 assert press(m,CENTER)==1 and lift(m,CENTER)==0 and m.ret==11
    '9b7bc98d6f': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9347 m.advance(O['DOUBLE_CLICK_MS']); assert m.clicks==[es[0]] and not buzz
    '0ea534a834': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9352 m,view=home_machine(tone=0)
    '843be0645f': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9353 assert [tick(m) for _ in range(4)]==[0,0,0,0] and m.selected(view)==4 
    '09bc2f5c69.4': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9354 m,view=home_machine()
    'd728f0276e': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9355 assert press(m)==0; m.byte(TONE,0); assert lift(m)==0 and m.selected(v
    'e7acacb513': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9355 assert press(m)==0; m.byte(TONE,0); assert lift(m)==0 and m.selected(v
    'd728f0276e.2': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9356 assert press(m)==0; m.byte(TONE,1); assert lift(m)==1 and m.selected(v
    '68d8609819': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9356 assert press(m)==0; m.byte(TONE,1); assert lift(m)==1 and m.selected(v
    '4cc7114bfc': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9357 m.byte(TONE,0x5a); assert tick(m)==1 and m.u.mem_read(TONE,1)==b'\x5a'
    '0edabec405': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9369 assert [tick(m,key) for key in (NEXT,PREV,NEXT)]==stock((NEXT,PREV,NEX
    '02b19578f8.2': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9370 m=audible(scrub_page()); centre(m); debounced(m)  # the double press's
    '1ca2b5f7e2': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9371 assert [tick(m,gap=100) for _ in range(3)]==stock((NEXT,)*3)==[1,1,1] 
    '7c13a365d9': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9373 assert [tick(m,gap=20) for _ in range(2)]==[1,1] and slide(m,m.slide)[
    '173e341947': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9375 assert tick(m)==1 and [c[0] for c in m.moved()]==['slide_menu_scroll_t
    '2fead0dd90': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9377 assert [tick(m,gap=100) for _ in range(3)]==[1,1,1] and m.get(w+O['TAB
    'a2f7c4efae': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9378 keys=(CENTER,RETURN,O['KEY_PLAY'],222,223)
    'a6b2a5d1a6': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9380 assert [tick(m,key) for key in keys]==stock(keys)==[1]*5 and m.selecte
    '1259956533': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9382 for kw in ({'po':1},{'bal':1},{'way':1}):
    '1b3c3df4b3': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9388 m,w,es=long_list(8,routed(audible(Machine()),status=2))
    'e975a93454': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9389 assert tick(m)==1 and m.selected(w)==1 and [tick(m,key) for key in key
    '8545dac447': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9392 assert [press(m,RETURN),press(m,RETURN,gap=500)]==[1,0]; long_return(m
    'da312d9a7f': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9392 assert [press(m,RETURN),press(m,RETURN,gap=500)]==[1,0]; long_return(m
    '25abf919f0': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9393 assert len(destinations(m))==0 and press(m,RETURN)==1; passed()
    'f34bc407f0': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9395 assert press(m,CENTER)==1 and m.release()==11 and press(m,CENTER,gap=1
    '0c1461d0f7': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9396 for flags in (dict(g_backlight_status=0),dict(g_backlight_status=0,g_k
    'd728f0276e.3': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9407 assert press(m)==0; m.page('playing_page'); assert lift(m)==0 and m.re
    'f92846c058': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9407 assert press(m)==0; m.page('playing_page'); assert lift(m)==0 and m.re
    '09d009e8a7': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9408 assert tick(m)==1 and m.ret==0
    'aaabec2de3': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9409 assert press(m)==1; m.top=lst; assert lift(m)==0 and m.ret==11 and m.s
    'eee466f316': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9409 assert press(m)==1; m.top=lst; assert lift(m)==0 and m.ret==11 and m.s
    'be34ff1914.2': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9410 assert tick(m)==1 and m.selected(w)==2; passed()
    'd728f0276e.4': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9414 assert press(m)==0; w2,es2=m.page_list(8,extent=8*48,name='allmusic_pa
    'aad0e62a15': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9415 assert lift(m)==1 and m.selected(w2)==1 and m.selected(w)==0
    'f6b449b7e7': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9416 wiped(m,w2); m.paint(w2,gap=0); assert m.selected(w2)==1 and tick(m)==
    '48c077d550': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9423 assert press(m)==0 and tick(m)==1 and m.selected(w)==1
    'd728f0276e.5': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9424 assert press(m)==0; m.page('playing_page'); assert [tick(m),tick(m)]==
    'ec76034544': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9424 assert press(m)==0; m.page('playing_page'); assert [tick(m),tick(m)]==
    '80b8704b8b': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9425 m.top=lst; assert lift(m)==0 and m.ret==11 and m.selected(w)==2
    'abfefd53ec': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9426 assert press(m)==0 and press(m,RETURN)==0 and lift(m)==0 and m.ret==11
    '4c862414ba': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9427 assert lift(m,RETURN)==0 and press(m,RETURN)==1 and lift(m,RETURN)==0
    '02b19578f8.3': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9428 debounced(m); assert tick(m)==1 and m.selected(w)==3
    'fd4b0317ce': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9428 debounced(m); assert tick(m)==1 and m.selected(w)==3
    '9bacd6a492': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:10457 border(tiles[0]); assert m.bands[-1][:5]==((O['PH_TILE_W']-O['PH_THUMB
    'edbce3467b': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:10468 border(tiles[2]); assert m.bands[-1][4]==O['PH_GREY']
    # style, image and loader hooks (ipod-ui 4.1)
    'a44d2b3708': 'style, image and loader hooks (ipod-ui 4.1)',  # patch.py:5718 if 'localmusic_playlistsmore_page_init' in HOOKS or is_m1plus:  # M1 P
    '068a8e2bb8': 'style, image and loader hooks (ipod-ui 4.1)',  # patch.py:9859 assert m.nodes[title]['style']==m.nodes[detail]['style'] and m.nodes[t
    # Lock screen battery (ipod-ui 4.2)
    'a30d14f512': 'Lock screen battery (ipod-ui 4.2)',  # patch.py:14152 for mode in range(4):
    # status bar (ipod-ui 4.2)
    'e8b2f8b250': 'status bar (ipod-ui 4.2)',  # patch.py:5520 assert m.call(address=HOOKS['systembar_showface'][0],args=(bar,0,0,0),
    # Display settings pages (ipod-ui 4.3)
    '66249771a8': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8782 ctl=display_page(m,3); shortcut,keep_lit,click_hp,hold,qs,wheel=m.node
    'b6f44251eb': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8782 ctl=display_page(m,3); shortcut,keep_lit,click_hp,hold,qs,wheel=m.node
    'ccb736163c': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8783 assert m.icons_set==['playset_covermode','system_display','switch_off'
    'cda4c9d091': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8803 hp_label=m.nodes[m.nodes[click_hp]['children'][0]]['children'][1]; ass
    '0f4a736089': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8803 hp_label=m.nodes[m.nodes[click_hp]['children'][0]]['children'][1]; ass
    '4de8cb5d25': 'Display settings pages (ipod-ui 4.3)',  # patch.py:8804 f,ctx=m.handler(m.nodes[click_hp]['children'][0],O['EVT_CLICK']); m.ca
    # Library rows (ipod-ui 4.4)
    '90bd3c3315': 'Library rows (ipod-ui 4.4)',  # patch.py:10119 assert m.call(address=LIBRARY_INIT,args=(m.top,5,0,0),gap=0)==0 and le
    '1735956559': 'Library rows (ipod-ui 4.4)',  # patch.py:10122 assert m.call(address=LIBRARY_INIT,args=(m.top,5,0,0),gap=0)==0 and le
    '1735956559.2': 'Library rows (ipod-ui 4.4)',  # patch.py:10145 assert m.call(address=LIBRARY_INIT,args=(m.top,5,0,0),gap=0)==0 and le
    'c9436c1725': 'Library rows (ipod-ui 4.4)',  # patch.py:10147 assert m.nodes[icon]['image']=='local_podcasts' and m.nodes[label]['te
    'e426449b2e': 'Library rows (ipod-ui 4.4)',  # patch.py:10149 assert m.call(address=f,args=(ctx,m.event,0,0),gap=0)==0 and [m.text(c
    'aff13a2aa5': 'Library rows (ipod-ui 4.4)',  # patch.py:10152 assert m.text(syms['g_folder_path'])=='/mnt/mmc/PODCASTS' and m.u.mem_
    '6904e6d290': 'Library rows (ipod-ui 4.4)',  # patch.py:10153 assert [c[0] for c in m.calls]==(['stock_folder','folder_reset_variabl
    'e2bf44dcdb': 'Library rows (ipod-ui 4.4)',  # patch.py:10171 assert m.text(syms['g_folder_path'])=='/mnt/mmc/Audiobooks' and m.u.me
    '4cf040f0ac.2': 'Library rows (ipod-ui 4.4)',  # patch.py:10177 assert m.u.mem_read(syms['g_folder_layer'],1)[0]==1; passed()
    'e1488a9b2c': 'Library rows (ipod-ui 4.4)',  # patch.py:10434 assert m.nodes[icon]['image']=='local_photos' and m.nodes[label]['text
    'f70dc558f2': 'Library rows (ipod-ui 4.4)',  # patch.py:10436 page=m.top; assert m.nodes[page]['name']=='photos_page' and m.nodes[pa
    'f137392a59': 'Library rows (ipod-ui 4.4)',  # patch.py:10437 albums,grid,viewer=m.nodes[page]['children']; assert not m.nodes[grid]
    '0bbb08dfbf': 'Library rows (ipod-ui 4.4)',  # patch.py:10437 albums,grid,viewer=m.nodes[page]['children']; assert not m.nodes[grid]
    '98bd21d7ec': 'Library rows (ipod-ui 4.4)',  # patch.py:10442 assert labels(albums)==['Photos','All Photos','Trip']; passed()
    'ef0fa3e1ea': 'Library rows (ipod-ui 4.4)',  # patch.py:10445 rows=m.find('scroll_view',albums); first=m.nodes[rows]['children'][0]
    'e684ea0e3b': 'Library rows (ipod-ui 4.4)',  # patch.py:10445 rows=m.find('scroll_view',albums); first=m.nodes[rows]['children'][0]
    '7a16728ff5': 'Library rows (ipod-ui 4.4)',  # patch.py:10446 f,ctx=m.handler(first,O['EVT_CLICK']); m.call(address=f,args=(ctx,m.ev
    '1fd75a2d47': 'Library rows (ipod-ui 4.4)',  # patch.py:10447 assert not m.nodes[albums]['visible'] and m.nodes[grid]['visible'] and
    'f527a66865': 'Library rows (ipod-ui 4.4)',  # patch.py:10448 tiles_view=m.find('scroll_view',grid); tiles=m.nodes[tiles_view]['chil
    'f35ed69ec8': 'Library rows (ipod-ui 4.4)',  # patch.py:10448 tiles_view=m.find('scroll_view',grid); tiles=m.nodes[tiles_view]['chil
    'f2dcd8f006': 'Library rows (ipod-ui 4.4)',  # patch.py:10449 assert m.nodes[tiles_view].get('yslidable')==1 and m.nodes[tiles_view]
    'ca5bcbf4b7': 'Library rows (ipod-ui 4.4)',  # patch.py:10450 assert [cf_geometry(m,t) for t in tiles]==[(O['PH_GRID_X']+(i%O['PH_CO
    '014c02e5ef': 'Library rows (ipod-ui 4.4)',  # patch.py:10451 assert all(m.nodes[t]['style']==S('s_listitem_black') for t in tiles) 
    '5e9c3519c5.5': 'Library rows (ipod-ui 4.4)',  # patch.py:10458 worker,arg=m.threads[0]; assert m.call(address=worker,args=(arg,0,0,0)
    '05e51b9735': 'Library rows (ipod-ui 4.4)',  # patch.py:10460 assert m.thumbs==[(paths[0],cache(0,'.tmp'),SW,SH),(cache(0,'.jpg'),ca
    'c8bc727799': 'Library rows (ipod-ui 4.4)',  # patch.py:10464 assert m.forks==1 and m.bad=={cache(2,'.bad')} and cache(2,'.jpg') not
    '35102b9315': 'Library rows (ipod-ui 4.4)',  # patch.py:10465 m.advance(250); assert m.joins==[77]; passed()
    '9798366090': 'Library rows (ipod-ui 4.4)',  # patch.py:10467 border(tiles[1]); assert m.draws[-1]==((0,0,54,72),((O['PH_TILE_W']-54
    '3f8d3b67be': 'Library rows (ipod-ui 4.4)',  # patch.py:10471 f,ctx=m.handler(tiles[1],O['EVT_CLICK']); m.call(address=f,args=(ctx,m
    '689b5f7f65': 'Library rows (ipod-ui 4.4)',  # patch.py:10472 s=m.find('slide_menu',viewer); m.slide=s
    '803c670638': 'Library rows (ipod-ui 4.4)',  # patch.py:10473 assert m.nodes[viewer]['visible'] and not m.nodes[grid]['visible'] and
    '445325f05f': 'Library rows (ipod-ui 4.4)',  # patch.py:10476 assert stride==(O['PH_SHOT_H'] if is_m1plus else O['UI_W']), stride
    'd3dd7d93fb': 'Library rows (ipod-ui 4.4)',  # patch.py:10477 assert m.get(s+O['SLIDE_INDEX'])==1
    'f14b2a65e7': 'Library rows (ipod-ui 4.4)',  # patch.py:10480 assert m.draws==want_draws and m.loads==['file://'+cache(1,'.jpg'),'fi
    '9a0ce9d7d0': 'Library rows (ipod-ui 4.4)',  # patch.py:10484 (_,a),(_,b)=m.draws
    '9c02c75b54': 'Library rows (ipod-ui 4.4)',  # patch.py:10487 assert len(m.draws)==2 and a[0]-rest_x==b[0]+O['UI_W'] and a[0]-rest_x
    'd869882dfa': 'Library rows (ipod-ui 4.4)',  # patch.py:10489 if is_m1plus:
    'eb14fc1851': 'Library rows (ipod-ui 4.4)',  # patch.py:10507 info=[x for x in m.nodes[viewer]['children'] if m.nodes[x]['type']=='h
    '375ba953ac': 'Library rows (ipod-ui 4.4)',  # patch.py:10509 assert len([x for x in m.nodes[viewer]['children'] if m.nodes[x].get('
    'b1e491e365': 'Library rows (ipod-ui 4.4)',  # patch.py:10511 assert not m.nodes[info]['visible'] and inset<=x and x+bw<=O['UI_W']-i
    '04d4486489': 'Library rows (ipod-ui 4.4)',  # patch.py:10512 f,ctx=m.handler(m.nodes[s]['children'][1],O['EVT_CLICK']); m.call(addr
    'd3326d5c6b': 'Library rows (ipod-ui 4.4)',  # patch.py:10513 assert m.nodes[info]['visible'] and m.nodes[info]['text']=='2 of 4  b.
    '77da0b2628': 'Library rows (ipod-ui 4.4)',  # patch.py:10514 m.call(address=f,args=(ctx,m.event,0,0),gap=0); assert not m.nodes[inf
    '2e373d3697': 'Library rows (ipod-ui 4.4)',  # patch.py:10515 m.word(s+O['SLIDE_INDEX'],2); f,ctx=m.handler(s,O['EVT_VALUE_CHANGED']
    'c7fddc062c': 'Library rows (ipod-ui 4.4)',  # patch.py:10516 assert m.nodes[info]['visible'] and m.nodes[info]['text']=="Can't open
    '807736ab70': 'Library rows (ipod-ui 4.4)',  # patch.py:10518 m.top=page; assert m.call()==11 and signed(m.get(m.get(s+O['SLIDE_ANIM
    '756d505e56': 'Library rows (ipod-ui 4.4)',  # patch.py:10520 m.page=page; assert m.key()==11 and m.nodes[grid]['visible'] and not m
    '45e71bc88a': 'Library rows (ipod-ui 4.4)',  # patch.py:10521 assert m.nodes[tiles_view]['_ringnav_index']==2 and m.nodes[tiles_view
    '3e0937e7bd': 'Library rows (ipod-ui 4.4)',  # patch.py:10522 assert m.key()==11 and m.nodes[albums]['visible'] and not m.nodes[grid
    'c41f2aab67': 'Library rows (ipod-ui 4.4)',  # patch.py:10524 m.close(); assert sorted(m.destroyed)==sorted(m.frames) and m.frames; 
    'cbacef2660': 'Library rows (ipod-ui 4.4)',  # patch.py:10644 assert m.nodes[icon]['image']=='local_books' and m.nodes[label]['text'
    'b358ca1c9e': 'Library rows (ipod-ui 4.4)',  # patch.py:10647 page=m.page=m.top; assert m.nodes[page]['name']=='books_page' and m.no
    '733a834669': 'Library rows (ipod-ui 4.4)',  # patch.py:10650 assert [m.nodes[b]['style'] for b in back]==(['navbar_btnreturn_style'
    'c46dab838d': 'Library rows (ipod-ui 4.4)',  # patch.py:10651 assert not m.nodes[reader]['visible'] and labels(books)==['Books','A T
    '9f67208a44': 'Library rows (ipod-ui 4.4)',  # patch.py:10654 rows=m.nodes[m.find('scroll_view',books)]['children']
    '3cc8ca65d6': 'Library rows (ipod-ui 4.4)',  # patch.py:10660 open_book(1); assert m.nodes[reader]['visible'] and not m.nodes[books]
    '4da64fc55e': 'Library rows (ipod-ui 4.4)',  # patch.py:10660 open_book(1); assert m.nodes[reader]['visible'] and not m.nodes[books]
    'b1fcbcb769': 'Library rows (ipod-ui 4.4)',  # patch.py:10662 assert len(first)==O['BOOK_ROWS'] and all(c==0xffffffff and font==('de
    '498022484e': 'Library rows (ipod-ui 4.4)',  # patch.py:10663 assert ' '.join(t for t,*_ in first if t).split()==words[:len(' '.join
    '4d543f31ef': 'Library rows (ipod-ui 4.4)',  # patch.py:10667 assert [y for _,_,y,*_ in first]==[6+26*i for i in range(O['BOOK_ROWS'
    '50336d44f7': 'Library rows (ipod-ui 4.4)',  # patch.py:10670 seen=' '.join(t for t,*_ in first+second).split(); assert seen==words[
    '6f3fb08151': 'Library rows (ipod-ui 4.4)',  # patch.py:10674 assert m.call(O['KEY_CENTER'])==11 and m.nodes[info]['visible'] and re
    '9ed8cbf09a': 'Library rows (ipod-ui 4.4)',  # patch.py:10676 assert m.key()==11 and m.nodes[books]['visible'] and '/mnt/data/ringna
    '1122a9c94c': 'Library rows (ipod-ui 4.4)',  # patch.py:10677 assert m.nodes[m.find('scroll_view',books)]['_ringnav_index']==1
    '3cc8ca65d6.2': 'Library rows (ipod-ui 4.4)',  # patch.py:10678 open_book(1); assert page_lines()==third; passed()
    '89ccc96807': 'Library rows (ipod-ui 4.4)',  # patch.py:10681 m.key(); open_book(0); assert m.nodes[info]['visible'] and m.nodes[inf
    '7a7393e41f': 'Library rows (ipod-ui 4.4)',  # patch.py:10681 m.key(); open_book(0); assert m.nodes[info]['visible'] and m.nodes[inf
    '5e9c3519c5.6': 'Library rows (ipod-ui 4.4)',  # patch.py:10682 worker,arg=m.threads[0]; assert m.call(address=worker,args=(arg,0,0,0)
    'ff8f3c9395': 'Library rows (ipod-ui 4.4)',  # patch.py:10684 assert bytes(m.files[cache])=='Chapter 1\n\nCafé & tea.\f\nChapter 2'.
    'a02c341028': 'Library rows (ipod-ui 4.4)',  # patch.py:10685 assert [t for t,*_ in page_lines()]==['Chapter 1','','Café & tea.'] an
    '9f1e9af975': 'Library rows (ipod-ui 4.4)',  # patch.py:10688 m.key(); m.files[R+'/Series/A Tale.EPUB']=bytearray(b'PK junk'); m.fil
    '89ccc96807.2': 'Library rows (ipod-ui 4.4)',  # patch.py:10688 m.key(); m.files[R+'/Series/A Tale.EPUB']=bytearray(b'PK junk'); m.fil
    '66ca87bd79': 'Library rows (ipod-ui 4.4)',  # patch.py:10689 worker,arg=m.threads[-1]; m.call(address=worker,args=(arg,0,0,0),gap=0
    'e0231eb762': 'Library rows (ipod-ui 4.4)',  # patch.py:10690 assert m.nodes[info]['visible'] and m.nodes[info]['text']=="Can't open
    'e39fa9664a': 'Library rows (ipod-ui 4.4)',  # patch.py:10712 sheet,chooser=games_open(); G=m.get(payload_syms['g'])
    '213d438955': 'Library rows (ipod-ui 4.4)',  # patch.py:10713 assert labels(chooser)==['Games','Sudoku','Vortex','Solitaire','Snake'
    '7fe72d327e': 'Library rows (ipod-ui 4.4)',  # patch.py:10714 rows=m.nodes[m.find('scroll_view',chooser)]['children']
    '1a3e33b7bc': 'Library rows (ipod-ui 4.4)',  # patch.py:10723 pick(0); assert m.nodes[sheet]['visible'] and not m.nodes[chooser]['vi
    '55475613b4': 'Library rows (ipod-ui 4.4)',  # patch.py:10723 pick(0); assert m.nodes[sheet]['visible'] and not m.nodes[chooser]['vi
    'f0312e5d82': 'Library rows (ipod-ui 4.4)',  # patch.py:10724 key(O['KEY_NEXT']); assert byte(G_CUR)==1
    'b20a386471': 'Library rows (ipod-ui 4.4)',  # patch.py:10724 key(O['KEY_NEXT']); assert byte(G_CUR)==1
    'b5cb0ea5ea': 'Library rows (ipod-ui 4.4)',  # patch.py:10725 key(O['KEY_PREV']); key(O['KEY_PREV']); assert byte(G_CUR)==80
    'b5cb0ea5ea.2': 'Library rows (ipod-ui 4.4)',  # patch.py:10725 key(O['KEY_PREV']); key(O['KEY_PREV']); assert byte(G_CUR)==80
    'f954819afe': 'Library rows (ipod-ui 4.4)',  # patch.py:10725 key(O['KEY_PREV']); key(O['KEY_PREV']); assert byte(G_CUR)==80
    '8ab44fbf2b': 'Library rows (ipod-ui 4.4)',  # patch.py:10726 key(O['KEY_FWD_BTN']); assert byte(G_CUR)==8
    'd32ce63cd7': 'Library rows (ipod-ui 4.4)',  # patch.py:10726 key(O['KEY_FWD_BTN']); assert byte(G_CUR)==8
    '27066724e2': 'Library rows (ipod-ui 4.4)',  # patch.py:10727 key(O['KEY_BACK_BTN']); assert byte(G_CUR)==80; passed()
    'f954819afe.2': 'Library rows (ipod-ui 4.4)',  # patch.py:10727 key(O['KEY_BACK_BTN']); assert byte(G_CUR)==80; passed()
    '762bfec88c': 'Library rows (ipod-ui 4.4)',  # patch.py:10731 blank=cells().index(0); clue=next(i for i,c in enumerate(cells()) if c
    '6097ea4c6d': 'Library rows (ipod-ui 4.4)',  # patch.py:10731 blank=cells().index(0); clue=next(i for i,c in enumerate(cells()) if c
    '66068ea3ba': 'Library rows (ipod-ui 4.4)',  # patch.py:10732 m.byte(G+G_CUR,clue); key(O['KEY_CENTER']); assert not word(G_PICKING)
    '89af2aa3aa': 'Library rows (ipod-ui 4.4)',  # patch.py:10732 m.byte(G+G_CUR,clue); key(O['KEY_CENTER']); assert not word(G_PICKING)
    'de88260b50': 'Library rows (ipod-ui 4.4)',  # patch.py:10732 m.byte(G+G_CUR,clue); key(O['KEY_CENTER']); assert not word(G_PICKING)
    'dce369e8ed': 'Library rows (ipod-ui 4.4)',  # patch.py:10733 m.byte(G+G_CUR,blank); key(O['KEY_CENTER']); assert word(G_PICKING)
    '89af2aa3aa.2': 'Library rows (ipod-ui 4.4)',  # patch.py:10733 m.byte(G+G_CUR,blank); key(O['KEY_CENTER']); assert word(G_PICKING)
    '04c950dde2': 'Library rows (ipod-ui 4.4)',  # patch.py:10733 m.byte(G+G_CUR,blank); key(O['KEY_CENTER']); assert word(G_PICKING)
    'f31d93643d': 'Library rows (ipod-ui 4.4)',  # patch.py:10734 for _ in range(3): key(O['KEY_NEXT'])
    '89af2aa3aa.3': 'Library rows (ipod-ui 4.4)',  # patch.py:10735 paint(); key(O['KEY_CENTER']); assert cells()[blank]==3 and not word(G
    '610b9df287': 'Library rows (ipod-ui 4.4)',  # patch.py:10735 paint(); key(O['KEY_CENTER']); assert cells()[blank]==3 and not word(G
    '0c96352e42': 'Library rows (ipod-ui 4.4)',  # patch.py:10736 m.advance(2000); saved=bytes(m.files['/mnt/data/ringnav-sudoku']); ass
    '623961eddf': 'Library rows (ipod-ui 4.4)',  # patch.py:10736 m.advance(2000); saved=bytes(m.files['/mnt/data/ringnav-sudoku']); ass
    '89af2aa3aa.4': 'Library rows (ipod-ui 4.4)',  # patch.py:10737 key(O['KEY_CENTER']); key(O['KEY_NEXT']); key(O['KEY_RETURN']); assert
    'f0312e5d82.2': 'Library rows (ipod-ui 4.4)',  # patch.py:10737 key(O['KEY_CENTER']); key(O['KEY_NEXT']); key(O['KEY_RETURN']); assert
    '4df64b387d': 'Library rows (ipod-ui 4.4)',  # patch.py:10737 key(O['KEY_CENTER']); key(O['KEY_NEXT']); key(O['KEY_RETURN']); assert
    '076a4e0505': 'Library rows (ipod-ui 4.4)',  # patch.py:10737 key(O['KEY_CENTER']); key(O['KEY_NEXT']); key(O['KEY_RETURN']); assert
    '585fa21b17': 'Library rows (ipod-ui 4.4)',  # patch.py:10738 before=cells(); key(O['KEY_PLAY']); assert cells()==before and word(52
    'a63f5492f4': 'Library rows (ipod-ui 4.4)',  # patch.py:10738 before=cells(); key(O['KEY_PLAY']); assert cells()==before and word(52
    '17b18e8bc2': 'Library rows (ipod-ui 4.4)',  # patch.py:10738 before=cells(); key(O['KEY_PLAY']); assert cells()==before and word(52
    '4df64b387d.2': 'Library rows (ipod-ui 4.4)',  # patch.py:10739 key(O['KEY_RETURN']); assert cells()==before and not word(52)
    '2682c91d39': 'Library rows (ipod-ui 4.4)',  # patch.py:10739 key(O['KEY_RETURN']); assert cells()==before and not word(52)
    '4df64b387d.3': 'Library rows (ipod-ui 4.4)',  # patch.py:10740 key(O['KEY_RETURN']); m.advance(0); assert word(G_SCREEN)==0 and m.nod
    '66735bf663': 'Library rows (ipod-ui 4.4)',  # patch.py:10740 key(O['KEY_RETURN']); m.advance(0); assert word(G_SCREEN)==0 and m.nod
    '7b597aa195.2': 'Library rows (ipod-ui 4.4)',  # patch.py:10741 assert m.key()==11; passed()
    'c54ae6e308': 'Library rows (ipod-ui 4.4)',  # patch.py:10743 m.page=m.top; pick(1); assert word(G_SCREEN)==2 and len(frames())==1 a
    'fd81feb488': 'Library rows (ipod-ui 4.4)',  # patch.py:10743 m.page=m.top; pick(1); assert word(G_SCREEN)==2 and len(frames())==1 a
    '39b8a3eb58': 'Library rows (ipod-ui 4.4)',  # patch.py:10744 m.word(payload_syms['wheel_travel'],-50&0xffffffff); m.advance(34); as
    'b65e55e61d': 'Library rows (ipod-ui 4.4)',  # patch.py:10746 assert made('reset_poweroptions_timer') and made('widget_invalidate_fo
    '89af2aa3aa.5': 'Library rows (ipod-ui 4.4)',  # patch.py:10750 key(O['KEY_CENTER']); m.advance(500); assert word(G_VX)==1 and made('w
    '909fcc2b6a': 'Library rows (ipod-ui 4.4)',  # patch.py:10750 key(O['KEY_CENTER']); m.advance(500); assert word(G_VX)==1 and made('w
    '8ab44fbf2b.2': 'Library rows (ipod-ui 4.4)',  # patch.py:10751 key(O['KEY_FWD_BTN']); assert not made('widget_invalidate_force')
    'a63f5492f4.2': 'Library rows (ipod-ui 4.4)',  # patch.py:10752 key(O['KEY_PLAY']); assert word(G_PAUSED)==1 and not frames() and m.ge
    'ab6bd7a3ab': 'Library rows (ipod-ui 4.4)',  # patch.py:10752 key(O['KEY_PLAY']); assert word(G_PAUSED)==1 and not frames() and m.ge
    '0dfa876a9e': 'Library rows (ipod-ui 4.4)',  # patch.py:10753 x=word(G_VX+20),word(G_VX+24); m.advance(500); assert (word(G_VX+20),w
    '4cf142ac31': 'Library rows (ipod-ui 4.4)',  # patch.py:10753 x=word(G_VX+20),word(G_VX+24); m.advance(500); assert (word(G_VX+20),w
    'a63f5492f4.3': 'Library rows (ipod-ui 4.4)',  # patch.py:10754 key(O['KEY_PLAY']); assert word(G_PAUSED)==0 and len(frames())==1 and 
    'e8f2d84a5f': 'Library rows (ipod-ui 4.4)',  # patch.py:10754 key(O['KEY_PLAY']); assert word(G_PAUSED)==0 and len(frames())==1 and 
    'ab6bd7a3ab.2': 'Library rows (ipod-ui 4.4)',  # patch.py:10756 assert word(G_PAUSED)==1 and not frames() and m.get(payload_syms['whee
    '4df64b387d.4': 'Library rows (ipod-ui 4.4)',  # patch.py:10757 key(O['KEY_RETURN']); assert word(G_PAUSED)==2; key(O['KEY_NEXT']); pa
    'ff742ca8d6': 'Library rows (ipod-ui 4.4)',  # patch.py:10757 key(O['KEY_RETURN']); assert word(G_PAUSED)==2; key(O['KEY_NEXT']); pa
    'f0312e5d82.3': 'Library rows (ipod-ui 4.4)',  # patch.py:10757 key(O['KEY_RETURN']); assert word(G_PAUSED)==2; key(O['KEY_NEXT']); pa
    '89af2aa3aa.6': 'Library rows (ipod-ui 4.4)',  # patch.py:10757 key(O['KEY_RETURN']); assert word(G_PAUSED)==2; key(O['KEY_NEXT']); pa
    '6e49df19e4': 'Library rows (ipod-ui 4.4)',  # patch.py:10766 m.page=m.top; pick(2); assert word(G_SCREEN)==3 and cur()==0 and [n(p)
    'fe2edce464': 'Library rows (ipod-ui 4.4)',  # patch.py:10766 m.page=m.top; pick(2); assert word(G_SCREEN)==3 and cur()==0 and [n(p)
    '60d2c2805f.7': 'Library rows (ipod-ui 4.4)',  # patch.py:10766 m.page=m.top; pick(2); assert word(G_SCREEN)==3 and cur()==0 and [n(p)
    '89af2aa3aa.7': 'Library rows (ipod-ui 4.4)',  # patch.py:10767 key(O['KEY_CENTER']); m.advance(2000); assert (n(0),n(1))==(23,1) and 
    '09e347b645': 'Library rows (ipod-ui 4.4)',  # patch.py:10767 key(O['KEY_CENTER']); m.advance(2000); assert (n(0),n(1))==(23,1) and 
    'f0312e5d82.4': 'Library rows (ipod-ui 4.4)',  # patch.py:10768 key(O['KEY_NEXT']); assert cur()==1; key(O['KEY_FWD_BTN']); assert cur
    '5a8ea34ce4': 'Library rows (ipod-ui 4.4)',  # patch.py:10768 key(O['KEY_NEXT']); assert cur()==1; key(O['KEY_FWD_BTN']); assert cur
    '8ab44fbf2b.3': 'Library rows (ipod-ui 4.4)',  # patch.py:10768 key(O['KEY_NEXT']); assert cur()==1; key(O['KEY_FWD_BTN']); assert cur
    '5393abcfc6': 'Library rows (ipod-ui 4.4)',  # patch.py:10768 key(O['KEY_NEXT']); assert cur()==1; key(O['KEY_FWD_BTN']); assert cur
    '27066724e2.2': 'Library rows (ipod-ui 4.4)',  # patch.py:10768 key(O['KEY_NEXT']); assert cur()==1; key(O['KEY_FWD_BTN']); assert cur
    '5a8ea34ce4.2': 'Library rows (ipod-ui 4.4)',  # patch.py:10768 key(O['KEY_NEXT']); assert cur()==1; key(O['KEY_FWD_BTN']); assert cur
    'b5cb0ea5ea.3': 'Library rows (ipod-ui 4.4)',  # patch.py:10769 key(O['KEY_PREV']); key(O['KEY_PREV']); assert cur()==12; key(O['KEY_B
    'b5cb0ea5ea.4': 'Library rows (ipod-ui 4.4)',  # patch.py:10769 key(O['KEY_PREV']); key(O['KEY_PREV']); assert cur()==12; key(O['KEY_B
    'b77931b1d9': 'Library rows (ipod-ui 4.4)',  # patch.py:10769 key(O['KEY_PREV']); key(O['KEY_PREV']); assert cur()==12; key(O['KEY_B
    '27066724e2.3': 'Library rows (ipod-ui 4.4)',  # patch.py:10769 key(O['KEY_PREV']); key(O['KEY_PREV']); assert cur()==12; key(O['KEY_B
    'faca4081c1': 'Library rows (ipod-ui 4.4)',  # patch.py:10769 key(O['KEY_PREV']); key(O['KEY_PREV']); assert cur()==12; key(O['KEY_B
    'b06052aade': 'Library rows (ipod-ui 4.4)',  # patch.py:10770 put(6,[64|13+11]); put(7,[3,64|10]); m.byte(G+G_SOL+329,7)  # Q of hea
    '8829606b74': 'Library rows (ipod-ui 4.4)',  # patch.py:10770 put(6,[64|13+11]); put(7,[3,64|10]); m.byte(G+G_SOL+329,7)  # Q of hea
    '2fba74c885': 'Library rows (ipod-ui 4.4)',  # patch.py:10770 put(6,[64|13+11]); put(7,[3,64|10]); m.byte(G+G_SOL+329,7)  # Q of hea
    '89af2aa3aa.8': 'Library rows (ipod-ui 4.4)',  # patch.py:10771 key(O['KEY_CENTER']); assert word(G_PICKING) and word(48)==7; paint()
    '3adb6b93ae': 'Library rows (ipod-ui 4.4)',  # patch.py:10771 key(O['KEY_CENTER']); assert word(G_PICKING) and word(48)==7; paint()
    '60d2c2805f.8': 'Library rows (ipod-ui 4.4)',  # patch.py:10771 key(O['KEY_CENTER']); assert word(G_PICKING) and word(48)==7; paint()
    '8ab44fbf2b.4': 'Library rows (ipod-ui 4.4)',  # patch.py:10772 key(O['KEY_FWD_BTN']); key(O['KEY_CENTER']); assert word(G_PICKING)  #
    '89af2aa3aa.9': 'Library rows (ipod-ui 4.4)',  # patch.py:10772 key(O['KEY_FWD_BTN']); key(O['KEY_CENTER']); assert word(G_PICKING)  #
    '04c950dde2.2': 'Library rows (ipod-ui 4.4)',  # patch.py:10772 key(O['KEY_FWD_BTN']); key(O['KEY_CENTER']); assert word(G_PICKING)  #
    '8ab44fbf2b.5': 'Library rows (ipod-ui 4.4)',  # patch.py:10773 key(O['KEY_FWD_BTN']); key(O['KEY_PREV']); key(O['KEY_CENTER']); asser
    'b5cb0ea5ea.5': 'Library rows (ipod-ui 4.4)',  # patch.py:10773 key(O['KEY_FWD_BTN']); key(O['KEY_PREV']); key(O['KEY_CENTER']); asser
    '89af2aa3aa.10': 'Library rows (ipod-ui 4.4)',  # patch.py:10773 key(O['KEY_FWD_BTN']); key(O['KEY_PREV']); key(O['KEY_CENTER']); asser
    'de88260b50.2': 'Library rows (ipod-ui 4.4)',  # patch.py:10773 key(O['KEY_FWD_BTN']); key(O['KEY_PREV']); key(O['KEY_CENTER']); asser
    'e122849745': 'Library rows (ipod-ui 4.4)',  # patch.py:10774 assert (n(6),n(7),byte(G_SOL+4+24*6+1),byte(G_SOL+4+24*7))==(2,1,64|10
    'bb7cea08b8': 'Library rows (ipod-ui 4.4)',  # patch.py:10775 put(1,[64|26]); m.byte(G+G_SOL+329,1); key(O['KEY_CENTER']); key(O['KE
    '2d1aafdcf1': 'Library rows (ipod-ui 4.4)',  # patch.py:10775 put(1,[64|26]); m.byte(G+G_SOL+329,1); key(O['KEY_CENTER']); key(O['KE
    '89af2aa3aa.11': 'Library rows (ipod-ui 4.4)',  # patch.py:10775 put(1,[64|26]); m.byte(G+G_SOL+329,1); key(O['KEY_CENTER']); key(O['KE
    '89af2aa3aa.12': 'Library rows (ipod-ui 4.4)',  # patch.py:10775 put(1,[64|26]); m.byte(G+G_SOL+329,1); key(O['KEY_CENTER']); key(O['KE
    '66fc1b822e': 'Library rows (ipod-ui 4.4)',  # patch.py:10776 assert not word(G_PICKING) and n(1)==0 and n(2)==1 and byte(G_SOL+4+48
    'f24d40e6a6': 'Library rows (ipod-ui 4.4)',  # patch.py:10777 m.byte(G+G_SOL+329,6); key(O['KEY_CENTER']); key(O['KEY_CENTER']); ass
    '89af2aa3aa.13': 'Library rows (ipod-ui 4.4)',  # patch.py:10777 m.byte(G+G_SOL+329,6); key(O['KEY_CENTER']); key(O['KEY_CENTER']); ass
    '89af2aa3aa.14': 'Library rows (ipod-ui 4.4)',  # patch.py:10777 m.byte(G+G_SOL+329,6); key(O['KEY_CENTER']); key(O['KEY_CENTER']); ass
    '6f97b4218f': 'Library rows (ipod-ui 4.4)',  # patch.py:10777 m.byte(G+G_SOL+329,6); key(O['KEY_CENTER']); key(O['KEY_CENTER']); ass
    '89af2aa3aa.15': 'Library rows (ipod-ui 4.4)',  # patch.py:10778 key(O['KEY_CENTER']); key(O['KEY_RETURN']); assert not word(G_PICKING)
    '4df64b387d.5': 'Library rows (ipod-ui 4.4)',  # patch.py:10778 key(O['KEY_CENTER']); key(O['KEY_RETURN']); assert not word(G_PICKING)
    'fc8f50ca54': 'Library rows (ipod-ui 4.4)',  # patch.py:10778 key(O['KEY_CENTER']); key(O['KEY_RETURN']); assert not word(G_PICKING)
    '3b5bfd9a87': 'Library rows (ipod-ui 4.4)',  # patch.py:10779 before_sol=sol(); key(O['KEY_PLAY']); assert word(52); paint(); key(O[
    'a63f5492f4.4': 'Library rows (ipod-ui 4.4)',  # patch.py:10779 before_sol=sol(); key(O['KEY_PLAY']); assert word(52); paint(); key(O[
    '48117aadd2': 'Library rows (ipod-ui 4.4)',  # patch.py:10779 before_sol=sol(); key(O['KEY_PLAY']); assert word(52); paint(); key(O[
    '60d2c2805f.9': 'Library rows (ipod-ui 4.4)',  # patch.py:10779 before_sol=sol(); key(O['KEY_PLAY']); assert word(52); paint(); key(O[
    '4df64b387d.6': 'Library rows (ipod-ui 4.4)',  # patch.py:10779 before_sol=sol(); key(O['KEY_PLAY']); assert word(52); paint(); key(O[
    '2074d0cbd8': 'Library rows (ipod-ui 4.4)',  # patch.py:10779 before_sol=sol(); key(O['KEY_PLAY']); assert word(52); paint(); key(O[
    '4df64b387d.7': 'Library rows (ipod-ui 4.4)',  # patch.py:10780 key(O['KEY_RETURN']); m.advance(0); assert word(G_SCREEN)==0 and m.nod
    '0265a33ba6': 'Library rows (ipod-ui 4.4)',  # patch.py:10780 key(O['KEY_RETURN']); m.advance(0); assert word(G_SCREEN)==0 and m.nod
    'a8b1b2cfa3': 'Library rows (ipod-ui 4.4)',  # patch.py:10787 m.page=m.top; pick(3); assert word(G_SCREEN)==4 and len(frames())==1 a
    'eff446ceed': 'Library rows (ipod-ui 4.4)',  # patch.py:10787 m.page=m.top; pick(3); assert word(G_SCREEN)==4 and len(frames())==1 a
    '78000abffe': 'Library rows (ipod-ui 4.4)',  # patch.py:10788 assert body()==[207,208,209] and sdir()==1 and sstate()==1; paint()
    '60d2c2805f.10': 'Library rows (ipod-ui 4.4)',  # patch.py:10788 assert body()==[207,208,209] and sdir()==1 and sstate()==1; paint()
    'f8114faee2': 'Library rows (ipod-ui 4.4)',  # patch.py:10789 snake_before=bytes(m.u.mem_read(G+G_SN,820))
    '144777dfab': 'Library rows (ipod-ui 4.4)',  # patch.py:10790 skey(O['KEY_NEXT']); skey(O['KEY_PREV']); assert bytes(m.u.mem_read(G+
    '8287c7e95e': 'Library rows (ipod-ui 4.4)',  # patch.py:10790 skey(O['KEY_NEXT']); skey(O['KEY_PREV']); assert bytes(m.u.mem_read(G+
    '4d62a8962b': 'Library rows (ipod-ui 4.4)',  # patch.py:10790 skey(O['KEY_NEXT']); skey(O['KEY_PREV']); assert bytes(m.u.mem_read(G+
    '2fa25e9f4c': 'Library rows (ipod-ui 4.4)',  # patch.py:10791 skey(O['KEY_FWD_BTN']); skey(O['KEY_FWD_BTN']); assert sdir()==2
    '2fa25e9f4c.2': 'Library rows (ipod-ui 4.4)',  # patch.py:10791 skey(O['KEY_FWD_BTN']); skey(O['KEY_FWD_BTN']); assert sdir()==2
    '96332b49eb': 'Library rows (ipod-ui 4.4)',  # patch.py:10791 skey(O['KEY_FWD_BTN']); skey(O['KEY_FWD_BTN']); assert sdir()==2
    '0a7bec6f95': 'Library rows (ipod-ui 4.4)',  # patch.py:10792 m.advance(170); assert body()[-1]==229 and sdir()==3 and made('widget_
    '00dddc04a1': 'Library rows (ipod-ui 4.4)',  # patch.py:10793 skey(O['KEY_BACK_BTN']); assert sdir()==3  # waits for the next step
    '96b5b20b52': 'Library rows (ipod-ui 4.4)',  # patch.py:10793 skey(O['KEY_BACK_BTN']); assert sdir()==3  # waits for the next step
    'c37b29e226': 'Library rows (ipod-ui 4.4)',  # patch.py:10794 skey(O['KEY_PLAY']); assert word(G_PAUSED)==1 and not frames(); was=bo
    'e18733dc4c': 'Library rows (ipod-ui 4.4)',  # patch.py:10794 skey(O['KEY_PLAY']); assert word(G_PAUSED)==1 and not frames(); was=bo
    '8e41ef36eb': 'Library rows (ipod-ui 4.4)',  # patch.py:10794 skey(O['KEY_PLAY']); assert word(G_PAUSED)==1 and not frames(); was=bo
    'af9a1fb5b9': 'Library rows (ipod-ui 4.4)',  # patch.py:10794 skey(O['KEY_PLAY']); assert word(G_PAUSED)==1 and not frames(); was=bo
    '60d2c2805f.11': 'Library rows (ipod-ui 4.4)',  # patch.py:10794 skey(O['KEY_PLAY']); assert word(G_PAUSED)==1 and not frames(); was=bo
    '144777dfab.2': 'Library rows (ipod-ui 4.4)',  # patch.py:10795 skey(O['KEY_NEXT']); assert sdir()==3  # no turning while paused
    '96b5b20b52.2': 'Library rows (ipod-ui 4.4)',  # patch.py:10795 skey(O['KEY_NEXT']); assert sdir()==3  # no turning while paused
    'c37b29e226.2': 'Library rows (ipod-ui 4.4)',  # patch.py:10796 skey(O['KEY_PLAY']); assert word(G_PAUSED)==0 and len(frames())==1
    '8aa1970242': 'Library rows (ipod-ui 4.4)',  # patch.py:10796 skey(O['KEY_PLAY']); assert word(G_PAUSED)==0 and len(frames())==1
    'eeb61f1ab8': 'Library rows (ipod-ui 4.4)',  # patch.py:10797 m.word(G+G_SN+812,5); m.advance(170*12); assert sstate()==2 and not fr
    'e3f0e327aa': 'Library rows (ipod-ui 4.4)',  # patch.py:10797 m.word(G+G_SN+812,5); m.advance(170*12); assert sstate()==2 and not fr
    '33e712f7ef': 'Library rows (ipod-ui 4.4)',  # patch.py:10798 best=bytes(m.files['/mnt/data/ringnav-snake']); assert len(best)==12 a
    '25f19f306a': 'Library rows (ipod-ui 4.4)',  # patch.py:10798 best=bytes(m.files['/mnt/data/ringnav-snake']); assert len(best)==12 a
    '60d2c2805f.12': 'Library rows (ipod-ui 4.4)',  # patch.py:10799 paint(); skey(O['KEY_CENTER']); assert sstate()==1 and body()==[207,20
    '7e0adf5d24': 'Library rows (ipod-ui 4.4)',  # patch.py:10799 paint(); skey(O['KEY_CENTER']); assert sstate()==1 and body()==[207,20
    'e040fa48bd': 'Library rows (ipod-ui 4.4)',  # patch.py:10799 paint(); skey(O['KEY_CENTER']); assert sstate()==1 and body()==[207,20
    '00dddc04a1.2': 'Library rows (ipod-ui 4.4)',  # patch.py:10800 skey(O['KEY_BACK_BTN']); assert sdir()==0  # side Previous turns left,
    '00827aff47': 'Library rows (ipod-ui 4.4)',  # patch.py:10800 skey(O['KEY_BACK_BTN']); assert sdir()==0  # side Previous turns left,
    '60e611da01': 'Library rows (ipod-ui 4.4)',  # patch.py:10801 m.advance(170); assert body()[-1]==189
    '2fa25e9f4c.3': 'Library rows (ipod-ui 4.4)',  # patch.py:10802 skey(O['KEY_FWD_BTN']); assert sdir()==1  # side Next turns right
    'b274b92071': 'Library rows (ipod-ui 4.4)',  # patch.py:10802 skey(O['KEY_FWD_BTN']); assert sdir()==1  # side Next turns right
    'c37b29e226.3': 'Library rows (ipod-ui 4.4)',  # patch.py:10803 skey(O['KEY_PLAY']); skey(O['KEY_BACK_BTN']); skey(O['KEY_FWD_BTN']); 
    '00dddc04a1.3': 'Library rows (ipod-ui 4.4)',  # patch.py:10803 skey(O['KEY_PLAY']); skey(O['KEY_BACK_BTN']); skey(O['KEY_FWD_BTN']); 
    '2fa25e9f4c.4': 'Library rows (ipod-ui 4.4)',  # patch.py:10803 skey(O['KEY_PLAY']); skey(O['KEY_BACK_BTN']); skey(O['KEY_FWD_BTN']); 
    'b274b92071.2': 'Library rows (ipod-ui 4.4)',  # patch.py:10803 skey(O['KEY_PLAY']); skey(O['KEY_BACK_BTN']); skey(O['KEY_FWD_BTN']); 
    'c37b29e226.4': 'Library rows (ipod-ui 4.4)',  # patch.py:10804 skey(O['KEY_PLAY'])
    'd303e06d4c': 'Library rows (ipod-ui 4.4)',  # patch.py:10805 skey(O['KEY_RETURN']); assert word(G_PAUSED)==2 and word(60)==0
    'faf9c369f1': 'Library rows (ipod-ui 4.4)',  # patch.py:10805 skey(O['KEY_RETURN']); assert word(G_PAUSED)==2 and word(60)==0
    '144777dfab.3': 'Library rows (ipod-ui 4.4)',  # patch.py:10806 skey(O['KEY_NEXT']); assert word(60)==1  # the wheel picks in the menu
    'ace70b2003': 'Library rows (ipod-ui 4.4)',  # patch.py:10806 skey(O['KEY_NEXT']); assert word(60)==1  # the wheel picks in the menu
    '8287c7e95e.2': 'Library rows (ipod-ui 4.4)',  # patch.py:10807 skey(O['KEY_PREV']); assert word(60)==0
    '2dc4376a5f': 'Library rows (ipod-ui 4.4)',  # patch.py:10807 skey(O['KEY_PREV']); assert word(60)==0
    '00dddc04a1.4': 'Library rows (ipod-ui 4.4)',  # patch.py:10808 skey(O['KEY_BACK_BTN']); assert word(60)==1
    'ace70b2003.2': 'Library rows (ipod-ui 4.4)',  # patch.py:10808 skey(O['KEY_BACK_BTN']); assert word(60)==1
    '2fa25e9f4c.5': 'Library rows (ipod-ui 4.4)',  # patch.py:10809 skey(O['KEY_FWD_BTN']); assert word(60)==0
    '2dc4376a5f.2': 'Library rows (ipod-ui 4.4)',  # patch.py:10809 skey(O['KEY_FWD_BTN']); assert word(60)==0
    '2fa25e9f4c.6': 'Library rows (ipod-ui 4.4)',  # patch.py:10810 skey(O['KEY_FWD_BTN']); paint(); skey(O['KEY_CENTER']); m.advance(0)
    '60d2c2805f.13': 'Library rows (ipod-ui 4.4)',  # patch.py:10810 skey(O['KEY_FWD_BTN']); paint(); skey(O['KEY_CENTER']); m.advance(0)
    '7e0adf5d24.2': 'Library rows (ipod-ui 4.4)',  # patch.py:10810 skey(O['KEY_FWD_BTN']); paint(); skey(O['KEY_CENTER']); m.advance(0)
    '6c7b308867': 'Library rows (ipod-ui 4.4)',  # patch.py:10811 assert word(G_SCREEN)==0 and not frames(); passed()
    '7e86233542.18': 'Library rows (ipod-ui 4.4)',  # patch.py:10813 m.close(); assert m.get(payload_syms['g'])==0 and not frames()
    'e39fa9664a.2': 'Library rows (ipod-ui 4.4)',  # patch.py:10814 sheet,chooser=games_open(); G=m.get(payload_syms['g']); rows=m.nodes[m
    '7fe72d327e.2': 'Library rows (ipod-ui 4.4)',  # patch.py:10814 sheet,chooser=games_open(); G=m.get(payload_syms['g']); rows=m.nodes[m
    '1a3e33b7bc.2': 'Library rows (ipod-ui 4.4)',  # patch.py:10815 pick(0); assert cells()==before
    '98152372b9': 'Library rows (ipod-ui 4.4)',  # patch.py:10815 pick(0); assert cells()==before
    '4df64b387d.8': 'Library rows (ipod-ui 4.4)',  # patch.py:10816 key(O['KEY_RETURN']); m.advance(0); pick(2); assert sol()[:-4]==before
    '6e49df19e4.2': 'Library rows (ipod-ui 4.4)',  # patch.py:10816 key(O['KEY_RETURN']); m.advance(0); pick(2); assert sol()[:-4]==before
    '74841e0c17': 'Library rows (ipod-ui 4.4)',  # patch.py:10816 key(O['KEY_RETURN']); m.advance(0); pick(2); assert sol()[:-4]==before
    'd1de3ca1f1': 'Library rows (ipod-ui 4.4)',  # patch.py:10819 m.byte(G+G_SOL+329,0)
    '9332ab3ede': 'Library rows (ipod-ui 4.4)',  # patch.py:10821 assert not saves; m.advance(2000); assert len(saves)==1 and bytes(m.fi
    '4df64b387d.9': 'Library rows (ipod-ui 4.4)',  # patch.py:10822 key(O['KEY_RETURN']); m.advance(0); pick(0); key(O['KEY_RETURN']); m.a
    '1a3e33b7bc.3': 'Library rows (ipod-ui 4.4)',  # patch.py:10822 key(O['KEY_RETURN']); m.advance(0); pick(0); key(O['KEY_RETURN']); m.a
    '4df64b387d.10': 'Library rows (ipod-ui 4.4)',  # patch.py:10822 key(O['KEY_RETURN']); m.advance(0); pick(0); key(O['KEY_RETURN']); m.a
    '71bc7633bd': 'Library rows (ipod-ui 4.4)',  # patch.py:10822 key(O['KEY_RETURN']); m.advance(0); pick(0); key(O['KEY_RETURN']); m.a
    '6e49df19e4.3': 'Library rows (ipod-ui 4.4)',  # patch.py:10822 key(O['KEY_RETURN']); m.advance(0); pick(0); key(O['KEY_RETURN']); m.a
    '4df64b387d.11': 'Library rows (ipod-ui 4.4)',  # patch.py:10823 key(O['KEY_RETURN']); m.advance(0); pick(1); assert len(frames())==1
    'c54ae6e308.2': 'Library rows (ipod-ui 4.4)',  # patch.py:10823 key(O['KEY_RETURN']); m.advance(0); pick(1); assert len(frames())==1
    '012e45a329': 'Library rows (ipod-ui 4.4)',  # patch.py:10823 key(O['KEY_RETURN']); m.advance(0); pick(1); assert len(frames())==1
    '7e86233542.19': 'Library rows (ipod-ui 4.4)',  # patch.py:10824 m.close(); assert m.get(payload_syms['g'])==0 and not frames() and m.g
    'e087294d76': 'Library rows (ipod-ui 4.4)',  # patch.py:10835 assert m.nodes[icon]['image']=='local_videos' and m.nodes[label]['text
    'e426449b2e.2': 'Library rows (ipod-ui 4.4)',  # patch.py:10837 assert m.call(address=f,args=(ctx,m.event,0,0),gap=0)==0 and [m.text(c
    '4cc80260b6': 'Library rows (ipod-ui 4.4)',  # patch.py:14820 if is_m1plus:
    # hold Return to Now Playing (ipod-ui 4.4)
    'dfe4cdaacb': 'hold Return to Now Playing (ipod-ui 4.4)',  # patch.py:3196 for existing in (False,True):
    '06388513e1': 'hold Return to Now Playing (ipod-ui 4.4)',  # patch.py:3219 assert m.call(170,gap=0)==11
    # pull to search on iPod lists (ipod-ui 4.4)
    'b8767f31f8': 'pull to search on iPod lists (ipod-ui 4.4)',  # patch.py:3288 for page_name in ('folder_page','localmusic_page','allmusic_page','rad
    '22ec0013d1': 'pull to search on iPod lists (ipod-ui 4.4)',  # patch.py:3330 assert len(m.searches())==1 and m.get(w+O['TABLE_ROWS'])==count and m.
    '3791f9c29f': 'pull to search on iPod lists (ipod-ui 4.4)',  # patch.py:3335 for cancel in ('below','horizontal','upward','midlist','outside','edge
    'd1d94c7d11': 'pull to search on iPod lists (ipod-ui 4.4)',  # patch.py:3381 for distance in (7,48):
    'c2221ae651': 'pull to search on iPod lists (ipod-ui 4.4)',  # patch.py:3398 assert [c[1] for c in m.dispatched()]==[w,es[0]] and not m.clicks
    '830fe27fdf': 'pull to search on iPod lists (ipod-ui 4.4)',  # patch.py:3411 m=SearchNavigationMachine();w,es=m.page_list(6,height=240,name='localm
    '909058c712.2': 'pull to search on iPod lists (ipod-ui 4.4)',  # patch.py:3412 m.order=[page];m.sync_order()
    'cdc3f66699': 'pull to search on iPod lists (ipod-ui 4.4)',  # patch.py:3415 assert m.nodes[m.top]['name']=='dialog/search_dialog' and m.order[0]==
    '909058c712.3': 'pull to search on iPod lists (ipod-ui 4.4)',  # patch.py:3419 m.order.remove(m.top);m.sync_order()
    # Home and the Q2 Pod page (ipod-ui 4.5)
    '466012b4b4': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:8881 home_bounds(False); carousel(False)
    '272249ba26': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:8881 home_bounds(False); carousel(False)
    '8f720362a9': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:8883 home_bounds(True); carousel(False)
    '272249ba26.2': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:8883 home_bounds(True); carousel(False)
    '927dc434cc.2': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:8885 writes=click(1); assert [(w[0],m.text(w[2])) for w in writes]==[(2,'HO
    '84b943d9a0': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:8885 writes=click(1); assert [(w[0],m.text(w[2])) for w in writes]==[(2,'HO
    '4fc57e7f8e': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:8886 carousel(True); assert not [c for c in m.calls if c[0]=='image_manager
    '715ae6bcff': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:8887 click(1); assert texts()[1]=='Home: Split'; home_bounds(False); carous
    '35d85e600e': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:8887 click(1); assert texts()[1]=='Home: Split'; home_bounds(False); carous
    '466012b4b4.2': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:8887 click(1); assert texts()[1]=='Home: Split'; home_bounds(False); carous
    '272249ba26.3': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:8887 click(1); assert texts()[1]=='Home: Split'; home_bounds(False); carous
    '715ae6bcff.2': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:8923 click(1); assert texts()[1]=='Home: Full'; home_bounds(True,True); cli
    'fd1c55d76c': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:8923 click(1); assert texts()[1]=='Home: Full'; home_bounds(True,True); cli
    'c0c3106d02': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:8923 click(1); assert texts()[1]=='Home: Full'; home_bounds(True,True); cli
    '715ae6bcff.3': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:8923 click(1); assert texts()[1]=='Home: Full'; home_bounds(True,True); cli
    '4fc57e7f8e.2': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:8923 click(1); assert texts()[1]=='Home: Full'; home_bounds(True,True); cli
    '715ae6bcff.4': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:8924 click(1); home_bounds(False,True); carousel(False); passed()
    'baa6580069.2': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:8924 click(1); home_bounds(False,True); carousel(False); passed()
    '272249ba26.4': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:8924 click(1); home_bounds(False,True); carousel(False); passed()
    'f08e7ea68f': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:9636 if is_m1plus: q2pod_page()  # its own names: the Library's machine (m,
    '0f3397c13c': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:9731 if is_m1plus: q2pod_real_grid()
    'ff99c8ed8a': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:9834 home_carousel()
    '6557576207': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:9835 for full in (0,1):
    # boot resume to Home (ipod-ui 4.5)
    '6bd274c37f': 'boot resume to Home (ipod-ui 4.5)',  # patch.py:4672 assert struct.unpack_from('<I',demo,fileoff(demo,0x523de0))[0]==jal(bo
    'ca3db14059': 'boot resume to Home (ipod-ui 4.5)',  # patch.py:4673 for car,cls,want in ((0,1,[(0x5550,4,1,3)]),(0,0xff,[]),(1,0xf003,[]))
    # Now Playing (ipod-ui 4.6)
    '64d0da19d1': 'Now Playing (ipod-ui 4.6)',  # patch.py:6155 cover_is(b'/p/C',2); assert art_pass()==(reload,'file:///tmp/externpic
    'e3949fc4b3': 'Now Playing (ipod-ui 4.6)',  # patch.py:6156 m.word(O['MCL_POS'],1); cover_is(b'/p/B',1); assert art_pass()==(reloa
    '88ba9daedb': 'Now Playing (ipod-ui 4.6)',  # patch.py:6157 m.word(O['MCL_POS'],2); cover_is(b'/p/C',3); assert art_pass()==(reloa
    'e31731b50f': 'Now Playing (ipod-ui 4.6)',  # patch.py:6159 m.byte(syms['g_backlight_status'],1); assert art_pass()==(reload,'file
    '828d5aab4e': 'Now Playing (ipod-ui 4.6)',  # patch.py:6659 if 'mclLoadExLyric' in HOOKS:
    # big cover page (ipod-ui 4.6)
    '9d2b5f1ad7': 'big cover page (ipod-ui 4.6)',  # patch.py:6537 for page,left in ((1,O['BC_IDLE_FULL']),(0,3)):
    # Games (ipod-ui 4.8, Q2 only)
    '59bdeea4c9': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10758 assert word(G_SCREEN)==0 and not frames() and m.get(payload_syms['whee
    '7b597aa195.3': 'Games (ipod-ui 4.8, Q2 only)',  # patch.py:10759 assert m.key()==11; passed()  # Return in the chooser after Vortex goe
}
