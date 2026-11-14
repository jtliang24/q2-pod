"""The patch.py checks the M1 Plus fails until the iPod UI item that ports them lands (gaprun.py).

Each is a top-level statement of patch.py, keyed by a hash of its source and its number among identical ones, and
listed under the docs/m1plus-ipod-ui.md item that makes it pass; that item's commit drops its entries (a listed
check that passes fails the run). After an edit to patch.py, GAPS_DUMP=gaps.json python3 test/m1plus/patch.py BUILD
writes every failing check, to rekey the list."""
GAPS = {
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
    '4a2be76ac0': 'Playlists, Podcasts and Audiobooks as Shortcuts (1.6.7; unported)',  # patch.py:12156 assert m.text(m.call(address=payload_syms[ipod_home_shortcut],args=(0,0,0,0),g
    'eb604de254': 'Playlists, Podcasts and Audiobooks as Shortcuts (1.6.7; unported)',  # patch.py:12157 m.calls=[]; assert m.call(address=payload_syms[home_shortcut_open],args=(0,m.e
    'b36537fa89': 'Playlists, Podcasts and Audiobooks as Shortcuts (1.6.7; unported)',  # patch.py:12158 assert [m.text(c[1]) for c in m.calls if c[0]==navigator_to]==[folder_page]
    '68add6ecdb': 'Playlists, Podcasts and Audiobooks as Shortcuts (1.6.7; unported)',  # patch.py:12160 assert m.text(syms[g_folder_path])==/mnt/mmc/Podcasts and m.u.mem_read(syms[
    'c2403b1456': 'Playlists, Podcasts and Audiobooks as Shortcuts (1.6.7; unported)',  # patch.py:12162 assert m.text(m.call(address=payload_syms[ipod_home_shortcut],args=(0,0,0,0),g
    'eb604de254.2': 'Playlists, Podcasts and Audiobooks as Shortcuts (1.6.7; unported)',  # patch.py:12163 m.calls=[]; assert m.call(address=payload_syms[home_shortcut_open],args=(0,m.e
    'dd982fb5ef': 'Playlists, Podcasts and Audiobooks as Shortcuts (1.6.7; unported)',  # patch.py:12164 assert not [c for c in m.calls if c[0]==navigator_to] and m.toasts[-1][3]==No
    '27d4e91422.3': 'Playlists, Podcasts and Audiobooks as Shortcuts (1.6.7; unported)',  # patch.py:15022 assert m.call(address=HOOKS['folder_page_init'][0],args=(win,0,0,0),gap=0)==0 [dependent]
}
