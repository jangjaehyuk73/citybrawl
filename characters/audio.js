/* 도시명물 대전 — 절차적 사운드 (Web Audio, 외부 파일 없음)
   window.SND.init()  최초 유저 제스처에서 호출(오토플레이 정책) → BGM 시작
   window.SND.play('punch' 등)  효과음
   window.SND.toggleMute()      음소거 토글
*/
window.SND = (function(){
  let AC=null, master=null, muted=false;
  let bgmOn=false, step=0, nextT=0, bgmTimer=null;
  const BGMVOL=0.6;

  function init(){
    if(AC){ if(AC.state==='suspended') AC.resume(); return; }
    AC = new (window.AudioContext||window.webkitAudioContext)();
    master = AC.createGain(); master.gain.value = muted?0:0.5; master.connect(AC.destination);
    startBGM();
  }
  const now = ()=> AC.currentTime;

  // ── 신스 헬퍼 ──
  function tone(freq,dur,type,gain,t,opt){ opt=opt||{}; t=(t||0)+now();
    const o=AC.createOscillator(), g=AC.createGain();
    o.type=type||'square'; o.frequency.setValueAtTime(freq,t);
    if(opt.slideTo) o.frequency.exponentialRampToValueAtTime(Math.max(1,opt.slideTo),t+dur);
    const a=opt.attack||0.004;
    g.gain.setValueAtTime(0.0001,t); g.gain.exponentialRampToValueAtTime(gain,t+a);
    g.gain.exponentialRampToValueAtTime(0.0001,t+dur);
    o.connect(g); g.connect(opt.dest||master); o.start(t); o.stop(t+dur+0.03);
  }
  function noise(dur,gain,t,filt,ftype){ t=(t||0)+now();
    const n=AC.createBufferSource(), buf=AC.createBuffer(1,Math.max(1,AC.sampleRate*dur),AC.sampleRate);
    const d=buf.getChannelData(0); for(let i=0;i<d.length;i++) d[i]=Math.random()*2-1; n.buffer=buf;
    const g=AC.createGain(); g.gain.setValueAtTime(gain,t); g.gain.exponentialRampToValueAtTime(0.0001,t+dur);
    let node=n;
    if(filt){ const f=AC.createBiquadFilter(); f.type=ftype||'bandpass'; f.frequency.value=filt; f.Q.value=0.9; n.connect(f); node=f; }
    node.connect(g); g.connect(master); n.start(t); n.stop(t+dur+0.03);
  }

  // ── 효과음 ──
  const SFX = {
    hover(){ tone(680,0.06,'square',0.10,0,{slideTo:920}); },
    swoosh(){ noise(0.26,0.16,0,650,'bandpass'); },
    select(){ tone(523,0.08,'square',0.22); tone(784,0.14,'square',0.22,0.08); },
    appear(){ tone(150,0.30,'sine',0.55,0,{slideTo:55}); noise(0.16,0.30,0,320,'lowpass'); },
    vs(){ tone(196,0.20,'sawtooth',0.32); tone(247,0.24,'sawtooth',0.28,0.12); },
    fight(){ noise(0.28,0.18,0,1400,'bandpass'); tone(330,0.10,'square',0.25,0.02,{slideTo:660}); tone(660,0.26,'square',0.3,0.14); },
    punch(){ noise(0.08,0.34,0,1800,'bandpass'); tone(165,0.12,'sine',0.42,0,{slideTo:70}); },
    kick(){ noise(0.13,0.40,0,900,'bandpass'); tone(110,0.18,'sine',0.5,0,{slideTo:44}); },
    special(){ tone(900,0.42,'sawtooth',0.3,0,{slideTo:120}); noise(0.42,0.24,0,1600,'bandpass'); },
    guard(){ tone(1250,0.11,'square',0.24,0,{slideTo:880}); tone(1560,0.09,'square',0.16,0.01); noise(0.05,0.14,0,3200,'highpass'); },
    hit(){ noise(0.12,0.34,0,700,'lowpass'); tone(125,0.14,'sine',0.34,0,{slideTo:58}); },
    jump(){ tone(300,0.17,'sine',0.24,0,{slideTo:760}); },
    ko(){ tone(300,0.55,'sawtooth',0.42,0,{slideTo:66}); noise(0.4,0.24,0,480,'lowpass'); },
    win(){ [523,659,784,1047].forEach((f,i)=>tone(f,0.26,'square',0.28,i*0.11)); },
  };
  function play(name){ if(!AC||muted) return; try{ (SFX[name]||function(){})(); }catch(e){} }

  // ── BGM: 스텝 시퀀서(익사이팅 비트) ──
  const BPM=150, STEP=(60/BPM)/2;            // 8분음표
  const ROOTS=[110.00,87.31,130.81,98.00];   // Am F C G (마디별 베이스 루트)
  const ARP=[440,523,587,659,784];           // A C D E G (리드 아르페지오)
  function startBGM(){ if(bgmOn) return; bgmOn=true; step=0; nextT=now()+0.15; schedule(); }
  function schedule(){
    if(!AC) return;
    while(nextT < now()+0.2){
      const t=nextT - now(), s=step%16, bar=Math.floor(step/16)%4;
      if(s%4===0) tone(120,0.16,'sine',0.55*BGMVOL,t,{slideTo:44});       // 킥(4-on-floor)
      if(s%8===4){ noise(0.11,0.28*BGMVOL,t,2200,'highpass'); noise(0.09,0.18*BGMVOL,t,1600,'bandpass'); } // 스네어
      if(s%2===1) noise(0.03,0.11*BGMVOL,t,7000,'highpass');              // 하이햇(오프비트)
      if(s%2===0) tone(ROOTS[bar],0.19,'sawtooth',0.16*BGMVOL,t);         // 베이스
      if(s%2===0) tone(ARP[step%ARP.length],0.13,'square',0.09*BGMVOL,t); // 리드
      nextT += STEP; step++;
    }
    bgmTimer=setTimeout(schedule,60);
  }
  function toggleMute(){ muted=!muted; if(master) master.gain.value = muted?0:0.5; return muted; }

  return { init, play, toggleMute, get muted(){ return muted; } };
})();
