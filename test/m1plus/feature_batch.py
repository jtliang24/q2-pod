"""Extra V2.1 scenarios, executed in patch.py's MIPS harness namespace."""
# Configuration changes the Q2 Pod page beneath it, using persistent service ids. Tidal's Home
# card and unavailable Downloads have no switches; Configuration itself always remains visible.
m=AppMachine(); card_app(m,'deezer','name=Deezer\n')
rows=streaming(m); lib=m.top
m.click(rows['Configuration']); m.page=m.top
assert m.labels()==['Configuration','Tidal Cache: 2 GB','Spotify Cache: 2 GB','Stop Streaming Services',
                    'Spotify','Deezer','Soulseek','Internet Radio','AirPlay'],m.labels()
gap=m.rows()[3]
assert m.nodes[gap]['style']==NAMES['ROW_STYLE'] and m.nodes[gap]['style:normal:bg_color']==-16777216
for index,key,label in ((4,'SPOTIFY','Spotify'),(5,'deezer','Deezer'),(7,'RADIO','Internet Radio'),(8,'AIRPLAY','AirPlay')):
    m.row(index)
    assert key in m.config['STREAMHIDE'].split(',') and not m.nodes[rows[label]]['visible'], (key,m.config,m.nodes[rows[label]])
    switch=m.nodes[m.rows()[index]]['children'][-1]
    assert m.nodes[switch]['image']==NAMES['ICON_SWITCH_OFF']
assert m.nodes[rows['Configuration']]['visible']
saved=dict(m.config); m.close(); m.top=lib; m.click(rows['Configuration']); m.page=m.top
assert m.config==saved and m.nodes[m.nodes[m.rows()[4]]['children'][-1]]['image']==NAMES['ICON_SWITCH_OFF']; passed()
# A fresh payload instance models reboot; adding another app cannot shift the hidden app's key.
n=AppMachine(); card_app(n,'deezer','name=Deezer\n'); card_app(n,'aaa','name=AAA\n'); n.config.update(saved)
rows2=streaming(n)
assert all(not n.nodes[rows2[label]]['visible'] for label in ('Spotify','Deezer','Internet Radio','AirPlay'))
assert n.nodes[rows2['AAA']]['visible'] and n.nodes[rows2['Configuration']]['visible']; passed()
m.row(4); assert m.nodes[rows['Spotify']]['visible'] and 'SPOTIFY' not in m.config['STREAMHIDE'].split(','); passed()
# Native empty-default semantics: a missing STREAMHIDE key does not write the output buffer.
# Poison the stack first so zero-initialized emulator memory cannot conceal an uninitialized read.
class MissingStreamHide(AppMachine):
    def hook(self,u,address,size,unused):
        if self.handlers.get(address)=='toolsReadConfig' and self.text(u.reg_read(REGS[2]))=='STREAMHIDE' and 'STREAMHIDE' not in self.config:
            return self.returns(0,clobber=True)
        return super().hook(u,address,size,unused)
m=MissingStreamHide(); m.u.mem_write(0x70000000,b'\xa5'*0x10000)
rows=streaming(m); assert m.nodes[rows['Spotify']]['visible']
m.click(rows['Configuration']); m.page=m.top; m.row(4)
assert m.config['STREAMHIDE']=='SPOTIFY' and not m.nodes[rows['Spotify']]['visible']; passed()

# Memory housekeeping has no job beyond dropping caches: the patched native entry returns
# before opening any file or scheduling a periodic wake.
m=Machine(); assert m.call(address=0x50b810,args=(0,0,0,0),gap=0)==0 and not m.calls; passed()
# The status poll stretches only while dark and quiet. Cover workers stretch whenever dark;
# waking restores their original pace, and already-long waits stay long.
for quiet,lit in ((0,1),(0,0),(1,0),(1,1)):
    m=Machine(); m.mock('usleep@GLIBC_2.0'); m.word(payload_syms['dark_quiet'],quiet); m.byte(syms['g_backlight_status'],lit)
    for name,on in (('ringnav_dark_usleep',quiet),('ringnav_dark_cover_usleep',not lit)):
        for delay in (50000,200000,2000000):
            m.call(address=payload_syms[name],args=(delay,0,0,0),gap=0)
            assert [c[1] for c in m.calls if c[0].startswith('usleep')]==[max(delay,O['DARK_POLL_US']) if on else delay]
    passed()
# V2.1's Tidal launcher creates a worker on demand. There is no idle boot worker needing a
# semaphore post. Execute the real launcher with only network/thread endpoints mocked.
class NativeTidal(QueueMachine):
    def __init__(self,online):
        super().__init__(); self.online=online; self.lifecycle=[]
        for name in ('networkGetConnectStatus','mclGetPlayPos','tidal_playurl','pthread_cancel@GLIBC_2.0',
                     'pthread_join@GLIBC_2.0','pthread_create@GLIBC_2.2','pthread_detach@GLIBC_2.0'):
            self.handlers[syms[name]]='nt:'+name
    def hook(self,u,address,size,unused):
        name=self.handlers.get(address,'')
        if not name.startswith('nt:'): return super().hook(u,address,size,unused)
        name=name[3:]; a,b,c,d=[u.reg_read(r) for r in REGS]; ret=0
        if name=='networkGetConnectStatus': ret=self.online
        elif name=='mclGetPlayPos': ret=0
        elif name.startswith('pthread_create'):
            assert c==0x51c288 and d==self.items(self.get(syms['mcl_pdeqplaylist']))[0]
            self.word(a,77); self.lifecycle.append('create')
        elif name.startswith('pthread_detach'): assert a==77; self.lifecycle.append('detach')
        elif name.startswith('pthread_cancel'): self.lifecycle.append('cancel')
        elif name.startswith('pthread_join'): self.lifecycle.append('join')
        self.returns(ret,clobber=True)
m=NativeTidal(0); m.call(address=syms['get_tidal_trackurl'],args=(0,0,0,0),gap=0); assert not m.lifecycle; passed()
m=NativeTidal(1); m.call(address=syms['get_tidal_trackurl'],args=(0,0,0,0),gap=0)
assert m.lifecycle==['create','detach']; m.lifecycle=[]
m.call(address=syms['get_tidal_trackurl'],args=(0,0,0,0),gap=0)
assert m.lifecycle==['cancel','join','create','detach']; passed()
# Execute V2.1's complete CUE parser with byte-oriented stdio mocks. Its eighth conversion
# is a shared jalr (the seven direct calls alone miss Windows-1252 track titles).
class CueNative(TagTextMachine):
    def __init__(self,data):
        super().__init__(); self.data=data; self.at=0; self.records=[]; self.ptrs=[]; self.conversions=[]
        for name in ('fopen','fread','fclose','fgets','feof','ferror','ftell','fseek'):
            self.handlers[syms[name+('@GLIBC_2.2' if name in ('fopen','fclose') else '@GLIBC_2.0')]]='cf:'+name
        self.handlers[syms['_deque_push_back']]='cf:push'; self.handlers[syms['deque_size']]='cf:size'; self.handlers[syms['deque_at']]='cf:at'
        self.mock('toolsFreeStSongInfo','strstr@GLIBC_2.0','strchr@GLIBC_2.0','strcat@GLIBC_2.0','sprintf@GLIBC_2.0')
    def hook(self,u,address,size,unused):
        name=self.handlers.get(address,''); a,b,c,d=[u.reg_read(r) for r in REGS]; ret=0
        if name=='strcat@GLIBC_2.0':
            u.mem_write(a,self.raw(a)+self.raw(b)+bytes([0])); return self.returns(a,clobber=True)
        if name=='strchr@GLIBC_2.0':
            at=self.raw(a).find(bytes([b&255])); return self.returns(a+at if at>=0 else 0,clobber=True)
        if name=='strstr@GLIBC_2.0':
            at=self.raw(a).find(self.raw(b)); return self.returns(a+at if at>=0 else 0,clobber=True)
        if name=='snprintf@GLIBC_2.0' and self.raw(c)==b'%s':
            data=self.raw(d); u.mem_write(a,data[:b-1]+bytes([0])); return self.returns(len(data),clobber=True)
        if name=='t:iconv': self.conversions.append((self.raw(a),self.text(b),self.text(c)))
        if not name.startswith('cf:'): return super().hook(u,address,size,unused)
        name=name[3:]
        if name=='fopen': self.at=0; ret=0x1170000
        elif name=='fread':
            data=self.data[self.at:self.at+b*c]; self.at+=len(data); u.mem_write(a,data); ret=len(data)//b
        elif name=='fgets':
            if self.at<len(self.data):
                end=min(self.data.find(b'\n',self.at)+1 or len(self.data),self.at+b-1)
                data=self.data[self.at:end]; self.at=end; u.mem_write(a,data+b'\0'); ret=a
        elif name=='feof': ret=int(self.at>=len(self.data))
        elif name=='ftell': ret=self.at
        elif name=='fseek': self.at=(0 if c==0 else self.at if c==1 else len(self.data))+signed(b)
        elif name=='size': ret=len(self.records)
        elif name=='at': ret=self.ptrs[b] if b<len(self.ptrs) else 0
        elif name=='push':
            ptr=self.alloc(0x58); u.mem_write(ptr,bytes(u.mem_read(b,0x58))); self.ptrs.append(ptr)
            self.records.append({k:self.raw(self.get(b+O[k])) for k in ('REC_NAME','REC_TITLE','REC_ARTIST','REC_ALBUM') if self.get(b+O[k])})
        self.returns(ret,clobber=True)

def native_cue(title,artist,album,encoding,old_indirect=False):
    data=(f'PERFORMER "{artist}"\nTITLE "{album}"\nFILE "04 Cue.flac" WAVE\n  TRACK 01 AUDIO\n    TITLE "{title}"\n    INDEX 01 00:00:00\n').encode(encoding)
    m=CueNative(data)
    if old_indirect: m.word(0x5e7de4,0x0320f809)
    assert m.call(address=0x5e6f00,args=(m.string('/mnt/mmc/test'),m.string('/mnt/mmc/test/04 Cue.cue'),m.string('04 Cue.flac'),0),gap=0,count=5000000)==1
    assert len(m.records)==1
    return m
for title,artist,album,encoding in [('Canção','Beyoncé’s','Café “Hi” €','cp1252'),('Ñandú','Artist','Álbum','utf-8'),('晴天','周杰伦','叶惠美','gbk')]:
    m=native_cue(title,artist,album,encoding)
    assert m.records[0]['REC_TITLE'].decode()==title,m.records
    assert m.records[0]['REC_ARTIST'].decode().strip()==artist,m.records
    assert m.records[0]['REC_ALBUM'].decode().strip()==album,m.records
    passed()
m=native_cue('Canção','Artist','Album','cp1252',True)
assert m.records[0]['REC_TITLE'].decode()=='Can玢o' and m.conversions; passed()  # old site reproduces the device fault
