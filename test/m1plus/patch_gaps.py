"""The patch.py checks the M1 Plus fails until the iPod UI item that ports them lands (gaprun.py).

Each is a top-level statement of patch.py, keyed by a hash of its source and its number among identical ones, and
listed under the docs/m1plus-ipod-ui.md item that makes it pass; that item's commit drops its entries (a listed
check that passes fails the run). After an edit to patch.py, GAPS_DUMP=gaps.json python3 test/m1plus/patch.py BUILD
writes every failing check, to rekey the list."""
GAPS = {
    # Coverflow glass insets (ipod-ui 4.5)
    '4fd466fd66': 'Coverflow glass insets (ipod-ui 4.5)',  # patch.py:7736 if variant=='ipod':
    # Home and the Q2 Pod page (ipod-ui 4.5)
    'f08e7ea68f': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:9519 if is_m1plus: q2pod_page()  # its own names: the Library's machine (m,
    '0f3397c13c': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:9614 if is_m1plus: q2pod_real_grid()
    '6c3a7c13cc': 'Home and the Q2 Pod page (ipod-ui 4.5)',  # patch.py:9696 if variant=='ipod':
    # Library rows (ipod-ui 4.4)
    'b8d56fdeb9': 'Library rows (ipod-ui 4.4)',  # patch.py:9374 assert [kids[i] for i in (*range(1,5),6,8,9,10,12,13,15)]==[stock[i] f
    '90bd3c3315': 'Library rows (ipod-ui 4.4)',  # patch.py:9981 assert m.call(address=LIBRARY_INIT,args=(m.top,5,0,0),gap=0)==0 and le
    '1735956559': 'Library rows (ipod-ui 4.4)',  # patch.py:9984 assert m.call(address=LIBRARY_INIT,args=(m.top,5,0,0),gap=0)==0 and le
    '1735956559.2': 'Library rows (ipod-ui 4.4)',  # patch.py:10007 assert m.call(address=LIBRARY_INIT,args=(m.top,5,0,0),gap=0)==0 and le
    'c9436c1725': 'Library rows (ipod-ui 4.4)',  # patch.py:10009 assert m.nodes[icon]['image']=='local_podcasts' and m.nodes[label]['te
    'e426449b2e': 'Library rows (ipod-ui 4.4)',  # patch.py:10011 assert m.call(address=f,args=(ctx,m.event,0,0),gap=0)==0 and [m.text(c
    'aff13a2aa5': 'Library rows (ipod-ui 4.4)',  # patch.py:10014 assert m.text(syms['g_folder_path'])=='/mnt/mmc/PODCASTS' and m.u.mem_
    '6904e6d290': 'Library rows (ipod-ui 4.4)',  # patch.py:10015 assert [c[0] for c in m.calls]==(['stock_folder','folder_reset_variabl
    'e2bf44dcdb': 'Library rows (ipod-ui 4.4)',  # patch.py:10033 assert m.text(syms['g_folder_path'])=='/mnt/mmc/Audiobooks' and m.u.me
    '4cf040f0ac.2': 'Library rows (ipod-ui 4.4)',  # patch.py:10039 assert m.u.mem_read(syms['g_folder_layer'],1)[0]==1; passed()
    'e1488a9b2c': 'Library rows (ipod-ui 4.4)',  # patch.py:10296 assert m.nodes[icon]['image']=='local_photos' and m.nodes[label]['text
    'f70dc558f2': 'Library rows (ipod-ui 4.4)',  # patch.py:10298 page=m.top; assert m.nodes[page]['name']=='photos_page' and m.nodes[pa
    'f137392a59': 'Library rows (ipod-ui 4.4)',  # patch.py:10299 albums,grid,viewer=m.nodes[page]['children']; assert not m.nodes[grid]
    '0bbb08dfbf': 'Library rows (ipod-ui 4.4)',  # patch.py:10299 albums,grid,viewer=m.nodes[page]['children']; assert not m.nodes[grid]
    '98bd21d7ec': 'Library rows (ipod-ui 4.4)',  # patch.py:10304 assert labels(albums)==['Photos','All Photos','Trip']; passed()
    'ef0fa3e1ea': 'Library rows (ipod-ui 4.4)',  # patch.py:10307 rows=m.find('scroll_view',albums); first=m.nodes[rows]['children'][0]
    'e684ea0e3b': 'Library rows (ipod-ui 4.4)',  # patch.py:10307 rows=m.find('scroll_view',albums); first=m.nodes[rows]['children'][0]
    '7a16728ff5': 'Library rows (ipod-ui 4.4)',  # patch.py:10308 f,ctx=m.handler(first,O['EVT_CLICK']); m.call(address=f,args=(ctx,m.ev
    '1fd75a2d47': 'Library rows (ipod-ui 4.4)',  # patch.py:10309 assert not m.nodes[albums]['visible'] and m.nodes[grid]['visible'] and
    'f527a66865': 'Library rows (ipod-ui 4.4)',  # patch.py:10310 tiles_view=m.find('scroll_view',grid); tiles=m.nodes[tiles_view]['chil
    'f35ed69ec8': 'Library rows (ipod-ui 4.4)',  # patch.py:10310 tiles_view=m.find('scroll_view',grid); tiles=m.nodes[tiles_view]['chil
    'f2dcd8f006': 'Library rows (ipod-ui 4.4)',  # patch.py:10311 assert m.nodes[tiles_view].get('yslidable')==1 and m.nodes[tiles_view]
    'ca5bcbf4b7': 'Library rows (ipod-ui 4.4)',  # patch.py:10312 assert [cf_geometry(m,t) for t in tiles]==[(O['PH_GRID_X']+(i%O['PH_CO
    '014c02e5ef': 'Library rows (ipod-ui 4.4)',  # patch.py:10313 assert all(m.nodes[t]['style']==S('s_listitem_black') for t in tiles) 
    '5e9c3519c5.5': 'Library rows (ipod-ui 4.4)',  # patch.py:10320 worker,arg=m.threads[0]; assert m.call(address=worker,args=(arg,0,0,0)
    '05e51b9735': 'Library rows (ipod-ui 4.4)',  # patch.py:10322 assert m.thumbs==[(paths[0],cache(0,'.tmp'),SW,SH),(cache(0,'.jpg'),ca
    'c8bc727799': 'Library rows (ipod-ui 4.4)',  # patch.py:10326 assert m.forks==1 and m.bad=={cache(2,'.bad')} and cache(2,'.jpg') not
    '35102b9315': 'Library rows (ipod-ui 4.4)',  # patch.py:10327 m.advance(250); assert m.joins==[77]; passed()
    '15d1ce3908': 'Library rows (ipod-ui 4.4)',  # patch.py:10329 border(tiles[1]); assert m.draws[-1]==((0,0,54,72),((O['PH_TILE_W']-54
    '9798366090': 'Library rows (ipod-ui 4.4)',  # patch.py:10329 border(tiles[1]); assert m.draws[-1]==((0,0,54,72),((O['PH_TILE_W']-54
    '3f8d3b67be': 'Library rows (ipod-ui 4.4)',  # patch.py:10333 f,ctx=m.handler(tiles[1],O['EVT_CLICK']); m.call(address=f,args=(ctx,m
    '689b5f7f65': 'Library rows (ipod-ui 4.4)',  # patch.py:10334 s=m.find('slide_menu',viewer); m.slide=s
    '803c670638': 'Library rows (ipod-ui 4.4)',  # patch.py:10335 assert m.nodes[viewer]['visible'] and not m.nodes[grid]['visible'] and
    '445325f05f': 'Library rows (ipod-ui 4.4)',  # patch.py:10338 assert stride==(O['PH_SHOT_H'] if is_m1plus else O['UI_W']), stride
    'd3dd7d93fb': 'Library rows (ipod-ui 4.4)',  # patch.py:10339 assert m.get(s+O['SLIDE_INDEX'])==1
    'f14b2a65e7': 'Library rows (ipod-ui 4.4)',  # patch.py:10342 assert m.draws==want_draws and m.loads==['file://'+cache(1,'.jpg'),'fi
    '9a0ce9d7d0': 'Library rows (ipod-ui 4.4)',  # patch.py:10346 (_,a),(_,b)=m.draws
    '9c02c75b54': 'Library rows (ipod-ui 4.4)',  # patch.py:10349 assert len(m.draws)==2 and a[0]-rest_x==b[0]+O['UI_W'] and a[0]-rest_x
    'd869882dfa': 'Library rows (ipod-ui 4.4)',  # patch.py:10351 if is_m1plus:
    'eb14fc1851': 'Library rows (ipod-ui 4.4)',  # patch.py:10369 info=[x for x in m.nodes[viewer]['children'] if m.nodes[x]['type']=='h
    '375ba953ac': 'Library rows (ipod-ui 4.4)',  # patch.py:10371 assert len([x for x in m.nodes[viewer]['children'] if m.nodes[x].get('
    'b1e491e365': 'Library rows (ipod-ui 4.4)',  # patch.py:10373 assert not m.nodes[info]['visible'] and inset<=x and x+bw<=O['UI_W']-i
    '04d4486489': 'Library rows (ipod-ui 4.4)',  # patch.py:10374 f,ctx=m.handler(m.nodes[s]['children'][1],O['EVT_CLICK']); m.call(addr
    'd3326d5c6b': 'Library rows (ipod-ui 4.4)',  # patch.py:10375 assert m.nodes[info]['visible'] and m.nodes[info]['text']=='2 of 4  b.
    '77da0b2628': 'Library rows (ipod-ui 4.4)',  # patch.py:10376 m.call(address=f,args=(ctx,m.event,0,0),gap=0); assert not m.nodes[inf
    '2e373d3697': 'Library rows (ipod-ui 4.4)',  # patch.py:10377 m.word(s+O['SLIDE_INDEX'],2); f,ctx=m.handler(s,O['EVT_VALUE_CHANGED']
    'c7fddc062c': 'Library rows (ipod-ui 4.4)',  # patch.py:10378 assert m.nodes[info]['visible'] and m.nodes[info]['text']=="Can't open
    '807736ab70': 'Library rows (ipod-ui 4.4)',  # patch.py:10380 m.top=page; assert m.call()==11 and signed(m.get(m.get(s+O['SLIDE_ANIM
    '756d505e56': 'Library rows (ipod-ui 4.4)',  # patch.py:10382 m.page=page; assert m.key()==11 and m.nodes[grid]['visible'] and not m
    '45e71bc88a': 'Library rows (ipod-ui 4.4)',  # patch.py:10383 assert m.nodes[tiles_view]['_ringnav_index']==2 and m.nodes[tiles_view
    '3e0937e7bd': 'Library rows (ipod-ui 4.4)',  # patch.py:10384 assert m.key()==11 and m.nodes[albums]['visible'] and not m.nodes[grid
    'c41f2aab67': 'Library rows (ipod-ui 4.4)',  # patch.py:10386 m.close(); assert sorted(m.destroyed)==sorted(m.frames) and m.frames; 
    'cbacef2660': 'Library rows (ipod-ui 4.4)',  # patch.py:10498 assert m.nodes[icon]['image']=='local_books' and m.nodes[label]['text'
    'b358ca1c9e': 'Library rows (ipod-ui 4.4)',  # patch.py:10501 page=m.page=m.top; assert m.nodes[page]['name']=='books_page' and m.no
    '733a834669': 'Library rows (ipod-ui 4.4)',  # patch.py:10504 assert [m.nodes[b]['style'] for b in back]==(['navbar_btnreturn_style'
    'c46dab838d': 'Library rows (ipod-ui 4.4)',  # patch.py:10505 assert not m.nodes[reader]['visible'] and labels(books)==['Books','A T
    '9f67208a44': 'Library rows (ipod-ui 4.4)',  # patch.py:10508 rows=m.nodes[m.find('scroll_view',books)]['children']
    '3cc8ca65d6': 'Library rows (ipod-ui 4.4)',  # patch.py:10514 open_book(1); assert m.nodes[reader]['visible'] and not m.nodes[books]
    '4da64fc55e': 'Library rows (ipod-ui 4.4)',  # patch.py:10514 open_book(1); assert m.nodes[reader]['visible'] and not m.nodes[books]
    'b1fcbcb769': 'Library rows (ipod-ui 4.4)',  # patch.py:10516 assert len(first)==O['BOOK_ROWS'] and all(c==0xffffffff and font==('de
    '498022484e': 'Library rows (ipod-ui 4.4)',  # patch.py:10517 assert ' '.join(t for t,*_ in first if t).split()==words[:len(' '.join
    '4d543f31ef': 'Library rows (ipod-ui 4.4)',  # patch.py:10521 assert [y for _,_,y,*_ in first]==[6+26*i for i in range(O['BOOK_ROWS'
    '50336d44f7': 'Library rows (ipod-ui 4.4)',  # patch.py:10524 seen=' '.join(t for t,*_ in first+second).split(); assert seen==words[
    '6f3fb08151': 'Library rows (ipod-ui 4.4)',  # patch.py:10528 assert m.call(O['KEY_CENTER'])==11 and m.nodes[info]['visible'] and re
    '9ed8cbf09a': 'Library rows (ipod-ui 4.4)',  # patch.py:10530 assert m.key()==11 and m.nodes[books]['visible'] and '/mnt/data/ringna
    '1122a9c94c': 'Library rows (ipod-ui 4.4)',  # patch.py:10531 assert m.nodes[m.find('scroll_view',books)]['_ringnav_index']==1
    '3cc8ca65d6.2': 'Library rows (ipod-ui 4.4)',  # patch.py:10532 open_book(1); assert page_lines()==third; passed()
    '89ccc96807': 'Library rows (ipod-ui 4.4)',  # patch.py:10535 m.key(); open_book(0); assert m.nodes[info]['visible'] and m.nodes[inf
    '7a7393e41f': 'Library rows (ipod-ui 4.4)',  # patch.py:10535 m.key(); open_book(0); assert m.nodes[info]['visible'] and m.nodes[inf
    '5e9c3519c5.6': 'Library rows (ipod-ui 4.4)',  # patch.py:10536 worker,arg=m.threads[0]; assert m.call(address=worker,args=(arg,0,0,0)
    'ff8f3c9395': 'Library rows (ipod-ui 4.4)',  # patch.py:10538 assert bytes(m.files[cache])=='Chapter 1\\n\\nCafé & tea.\\f\\nChapter
    'a02c341028': 'Library rows (ipod-ui 4.4)',  # patch.py:10539 assert [t for t,*_ in page_lines()]==['Chapter 1','','Café & tea.'] an
    '9f1e9af975': 'Library rows (ipod-ui 4.4)',  # patch.py:10542 m.key(); m.files[R+'/Series/A Tale.EPUB']=bytearray(b'PK junk'); m.fil
    '89ccc96807.2': 'Library rows (ipod-ui 4.4)',  # patch.py:10542 m.key(); m.files[R+'/Series/A Tale.EPUB']=bytearray(b'PK junk'); m.fil
    '66ca87bd79': 'Library rows (ipod-ui 4.4)',  # patch.py:10543 worker,arg=m.threads[-1]; m.call(address=worker,args=(arg,0,0,0),gap=0
    'e0231eb762': 'Library rows (ipod-ui 4.4)',  # patch.py:10544 assert m.nodes[info]['visible'] and m.nodes[info]['text']=="Can't open
    '6ca9dc2835': 'Library rows (ipod-ui 4.4)',  # patch.py:10551 if variant=='ipod':
    'e087294d76': 'Library rows (ipod-ui 4.4)',  # patch.py:10689 assert m.nodes[icon]['image']=='local_videos' and m.nodes[label]['text
    'e426449b2e.2': 'Library rows (ipod-ui 4.4)',  # patch.py:10691 assert m.call(address=f,args=(ctx,m.event,0,0),gap=0)==0 and [m.text(c
    # Lock screen battery (ipod-ui 4.2)
    '23bc91cc59': 'Lock screen battery (ipod-ui 4.2)',  # patch.py:13503 for mode in range(4 if variant=='ipod' else 0):
    # Now Playing (ipod-ui 4.6)
    '1e55f3d783': 'Now Playing (ipod-ui 4.6)',  # patch.py:6640 if 'mclLoadExLyric' in HOOKS:
    'e6222b03cf': 'Now Playing (ipod-ui 4.6)',  # patch.py:11008 assert texts(info)==['Spotify','Song','A, B','LP',mmss('0:10'),mmss('-
    'a690fb4c40': 'Now Playing (ipod-ui 4.6)',  # patch.py:11015 m.advance(2500); assert texts(info)[4:]==[mmss('0:12'),mmss('-3:08')] 
    '17041ede1c': 'Now Playing (ipod-ui 4.6)',  # patch.py:11064 m.advance(250); assert texts(info)[4]==mmss('1:05') and 'on_wm_keyup_f
    '181347b08e': 'Now Playing (ipod-ui 4.6)',  # patch.py:11220 m.advance(3000); assert m.labels(np)==['Internet Radio','Three','Some 
    # big cover page (ipod-ui 4.6)
    '4cc80260b6': 'big cover page (ipod-ui 4.6)',  # patch.py:14155 if is_m1plus:
    # boot resume to Home (ipod-ui 4.5)
    '3c83ec917c': 'boot resume to Home (ipod-ui 4.5)',  # patch.py:4686 if variant=='ipod':
    # hold Return to Now Playing (ipod-ui 4.4)
    'cf8bb85991': 'hold Return to Now Playing (ipod-ui 4.4)',  # patch.py:3214 if variant=='ipod':
    # iPod UI assets (ipod-ui 3)
    '99e8e70cf6': 'iPod UI assets (ipod-ui 3)',  # patch.py:1364 if variant=='ipod':
    'e23268faa4': 'iPod UI assets (ipod-ui 3)',  # patch.py:2082 if variant=='ipod':
    'a56ebc2ec9': 'iPod UI assets (ipod-ui 3)',  # patch.py:5466 if variant=='ipod':
    # pull to search on iPod lists (ipod-ui 4.4)
    '4090933652': 'pull to search on iPod lists (ipod-ui 4.4)',  # patch.py:3307 for page_name in ('folder_page','localmusic_page','allmusic_page','rad
    'f4af82f22a': 'pull to search on iPod lists (ipod-ui 4.4)',  # patch.py:3345 if variant=='ipod':
    '8b360424d9': 'pull to search on iPod lists (ipod-ui 4.4)',  # patch.py:3401 if variant=='ipod':
    # selection bar and paint backbone (ipod-ui 4.1)
    '962e0dd3d7': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:860 for i in range(4):
    '330e6086e6': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:865 assert m.confirm()==11 and m.dispatched()[0][1]==buttons[-1]; passed()
    'b7adabc3be': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:957 if variant=='stock':
    '4cad3e05ef': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:1633 assert m.sel()==(0,36,240,48)
    '821cd87161': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:1910 if variant=='ipod':
    'e5e267496d': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:2160 if variant=='ipod':
    '8b1b861018': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:2653 if variant=='stock':
    'db74ccf0f2': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:2686 assert m.selected(w)==0 and m.sel()==(0,0,240,140)
    '13f330a7eb': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:2768 m.paint(a); assert m.sel()==(0,0,240,48); passed()
    '32b45b605a': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:3024 assert m.sel()==(0,42,240,48)   # bumped up against the end
    '13f330a7eb.2': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:3027 m.paint(w,gap=0); assert m.sel()==(0,0,240,48)
    '2425d1664c': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:3029 m.paint(w,gap=0); assert m.sel()==(0,6,240,48)   # bumped down at the 
    '3d56c36ba4': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:3032 m.paint(w,gap=0); assert m.sel()==(0,48,240,48)
    '32b45b605a.2': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:3042 m.paint(w,gap=0); assert m.sel()==(0,42,240,48)
    'fc0c657fe8': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:3073 for name in ('display_page','playerqueue_page'):
    '13f330a7eb.3': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:3088 m.paint(w,gap=0); assert m.sel()==(0,0,240,48)
    '3d56c36ba4.2': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:3155 m.paint(w,gap=0); assert m.sel()==(0,48,240,48)
    'be6e09ac30': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:5379 if variant=='ipod':
    '725f2c48f2': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:5570 for virtual in (False,True):
    'ffddda8787': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:6046 if variant=='ipod':
    '78ffafb9bb': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8186 if variant=='ipod':
    '604e6e6774': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:8275 if variant=='ipod':
    'b71684326d': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:9120 if variant=='ipod':
    '5cac0445a1': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:10319 border(tiles[0]); assert m.bands[-1][:5]==((O['PH_TILE_W']-O['PH_THUMB
    '9bacd6a492': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:10319 border(tiles[0]); assert m.bands[-1][:5]==((O['PH_TILE_W']-O['PH_THUMB
    '877fe46ba6': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:10330 border(tiles[2]); assert m.bands[-1][4]==O['PH_GREY']
    'edbce3467b': 'selection bar and paint backbone (ipod-ui 4.1)',  # patch.py:10330 border(tiles[2]); assert m.bands[-1][4]==O['PH_GREY']
    # style, image and loader hooks (ipod-ui 4.1)
    'd6557c9a9e': 'style, image and loader hooks (ipod-ui 4.1)',  # patch.py:5736 if 'localmusic_playlistsmore_page_init' in HOOKS or is_m1plus:  # M1 P
    'aaaff6d03e': 'style, image and loader hooks (ipod-ui 4.1)',  # patch.py:9721 assert m.nodes[title]['style']==m.nodes[detail]['style'] and (variant!
}
