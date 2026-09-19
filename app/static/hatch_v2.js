(function(){
window.DROP1_PREMIUM_HATCH=true;
const EGG="/static/assets/primal-egg.png";
const EGG_FALLBACK="/static/assets/primal-egg.png";
const IS_IOS=/iPad|iPhone|iPod/.test(navigator.userAgent)||((navigator.platform==='MacIntel')&&navigator.maxTouchPoints>1);
const css=`
.capsuleScene .capsule{
 width:188px!important;height:224px!important;border:0!important;border-radius:0!important;
 background:url("${EGG}") center/contain no-repeat!important;
 box-shadow:none!important;overflow:visible!important;
 animation:premiumEggFloat 3.2s ease-in-out infinite!important;
 filter:drop-shadow(0 20px 24px #000a) drop-shadow(0 0 18px #42dfff66) drop-shadow(0 0 42px #754cff4d)
}
.capsuleScene .capsule:before,.capsuleScene .capsule:after,.capsuleScene .core{display:none!important}
@keyframes premiumEggFloat{0%,100%{transform:translateY(0) rotate(-1deg) scale(1)}50%{transform:translateY(-9px) rotate(1deg) scale(1.018)}}

.reveal.primalV6{position:fixed!important;inset:0!important;overflow:hidden!important;padding:0!important;background:#02040a!important;display:flex!important;align-items:stretch!important;justify-content:center!important;--accent:#58e7ff;--accent2:#744dff}
.reveal.primalV6.hatch-common{--accent:#dff7ff;--accent2:#6987a3}.reveal.primalV6.hatch-rare{--accent:#55e6ff;--accent2:#6857ff}.reveal.primalV6.hatch-epic{--accent:#e168ff;--accent2:#7047ff}.reveal.primalV6.hatch-legendary{--accent:#ffe16d;--accent2:#ff861d}.reveal.primalV6.hatch-mythic{--accent:#84ffff;--accent2:#ff55dd}
.reveal.primalV6 .revealBox{position:absolute!important;z-index:30!important;left:16px!important;right:16px!important;bottom:calc(16px + env(safe-area-inset-bottom))!important;max-width:none!important;width:auto!important;opacity:0;transform:translateY(24px)}
.reveal.primalV6 .revealEyebrow,.reveal.primalV6 .revealCard,.reveal.primalV6 #revealName,.reveal.primalV6 #revealSerial{display:none!important}
.reveal.primalV6 .revealBtns{display:grid!important;grid-template-columns:1.15fr 1fr!important;gap:9px!important;margin:0!important}
.reveal.primalV6 .revealBtns .btn{padding:14px 10px!important;border-radius:16px!important;font-size:13px!important}
.reveal.primalV6 #revealAgain{background:linear-gradient(180deg,#f8fdff,#dcebff)!important;color:#07101c!important;border:1px solid var(--accent)!important;box-shadow:0 0 24px color-mix(in srgb,var(--accent) 35%,transparent)!important}
.reveal.primalV6 #revealClose{background:#09111ee8!important;color:#dceaff!important;border:1px solid #2e405a!important}

.p6Scene{position:absolute;inset:0;z-index:10;overflow:hidden;background:radial-gradient(circle at 50% 33%,color-mix(in srgb,var(--accent2) 28%,#0b1321) 0,#07101b 37%,#02040a 74%);perspective:900px}
.p6Scene:before{content:"";position:absolute;inset:0;z-index:1;background:linear-gradient(180deg,#02040ac7 0,transparent 18%,transparent 67%,#02040af2 100%),radial-gradient(circle at 50% 38%,transparent 0 42%,#0009 82%);pointer-events:none}
.p6Grid{position:absolute;left:-15%;right:-15%;bottom:-8%;height:38%;z-index:0;opacity:.17;transform:perspective(520px) rotateX(64deg);background-image:linear-gradient(#58e7ff20 1px,transparent 1px),linear-gradient(90deg,#58e7ff20 1px,transparent 1px);background-size:34px 34px;mask-image:linear-gradient(180deg,transparent,#000 25%,#000)}
.p6Top{position:absolute;z-index:12;left:20px;right:20px;top:calc(26px + env(safe-area-inset-top));display:flex;align-items:center;justify-content:space-between;gap:12px;opacity:0}
.p6Kicker{font-size:9px;font-weight:950;letter-spacing:.25em;color:#aabbd0}.p6Signal{font-size:9px;font-weight:950;letter-spacing:.14em;color:var(--accent);border:1px solid color-mix(in srgb,var(--accent) 50%,#26394f);background:#06101bd9;border-radius:999px;padding:7px 9px;box-shadow:0 0 18px color-mix(in srgb,var(--accent) 20%,transparent)}
.p6Chamber{position:absolute;left:50%;top:45%;z-index:5;width:min(92vw,430px);height:min(63vh,560px);transform:translate(-50%,-50%);border-radius:34px;overflow:hidden;border:1px solid #334b6a;background:radial-gradient(circle at 50% 35%,#17365c,#07101a 70%);box-shadow:0 35px 90px #000c,inset 0 0 55px #5aa7ff0d}
.p6Chamber:before,.p6Chamber:after{content:"";position:absolute;z-index:9;left:12%;right:12%;height:2px;background:linear-gradient(90deg,transparent,var(--accent),transparent);box-shadow:0 0 16px var(--accent);opacity:.34}.p6Chamber:before{top:8%}.p6Chamber:after{bottom:8%}
.p6Creature{position:absolute;inset:0;z-index:4;overflow:hidden;opacity:.08;filter:brightness(.2) saturate(.45) blur(5px);transform:scale(.9)}
.p6Creature img{position:absolute;left:0;top:-2%;width:100%;height:110%;object-fit:contain;object-position:50% 50%;display:block}
.p6Creature model-viewer{position:absolute;inset:0;width:100%;height:100%;background:transparent;--poster-color:transparent;touch-action:none}
.p6Creature .p6Poster{position:absolute;inset:0;width:100%;height:100%;object-fit:contain;object-position:center;display:block;opacity:1;transition:opacity .22s ease}
.p6Scan{position:absolute;z-index:8;left:7%;right:7%;top:16%;height:2px;background:linear-gradient(90deg,transparent,var(--accent),#fff,var(--accent),transparent);box-shadow:0 0 18px var(--accent),0 0 38px var(--accent);opacity:0}
.p6EggWrap{position:absolute;z-index:11;left:50%;top:47%;width:220px;height:270px;transform:translate(-50%,-50%) scale(.9);display:grid;place-items:center;will-change:transform,filter,opacity}
.p6EggVisual{position:absolute;inset:0;background:url("${EGG}") center/contain no-repeat;filter:drop-shadow(0 22px 26px #000c) drop-shadow(0 0 20px color-mix(in srgb,var(--accent) 38%,transparent)) drop-shadow(0 0 52px color-mix(in srgb,var(--accent2) 30%,transparent));transform:translateZ(0);-webkit-transform:translateZ(0);backface-visibility:hidden;-webkit-backface-visibility:hidden}.p6EggCssFallback{position:absolute;width:168px;height:214px;border-radius:50% 50% 47% 53%/58% 58% 42% 42%;background:radial-gradient(circle at 36% 23%,#eaffff 0,#91efff 10%,#5f76d8 36%,#2b214e 70%,#090d18 100%);border:2px solid #77eaff;box-shadow:0 0 22px #5ee5ff88,0 0 58px #704dff55,inset -18px -24px 32px #0b102b88;opacity:.42;z-index:-1}
.p6EggAura{position:absolute;inset:12%;border-radius:50%;z-index:-1;background:radial-gradient(circle,color-mix(in srgb,var(--accent) 18%,transparent),transparent 68%);filter:blur(16px);opacity:.65}
.p6Cracks{position:absolute;inset:0;pointer-events:none;opacity:0;filter:drop-shadow(0 0 7px var(--accent)) drop-shadow(0 0 18px var(--accent))}
.p6Cracks:before,.p6Cracks:after{content:"";position:absolute;background:#f4ffff;transform-origin:top center;clip-path:polygon(42% 0,100% 0,54% 19%,92% 21%,26% 48%,72% 50%,0 100%,27% 62%,2% 63%,55% 32%,14% 31%)}
.p6Cracks:before{width:6px;height:128px;left:51%;top:21%;transform:rotate(10deg) scaleY(.05)}.p6Cracks:after{width:5px;height:91px;left:35%;top:38%;transform:rotate(-36deg) scaleY(.05)}
.p6Flash{position:absolute;z-index:10;left:50%;top:47%;width:24px;height:24px;border-radius:50%;transform:translate(-50%,-50%) scale(.1);opacity:0;background:#fff;box-shadow:0 0 30px 20px var(--accent),0 0 110px 72px var(--accent2)}
.p6Meta{position:absolute;z-index:14;left:22px;right:22px;bottom:calc(99px + env(safe-area-inset-bottom));text-align:center;opacity:0;transform:translateY(18px)}
.p6Rarity{display:inline-flex;align-items:center;gap:6px;border:1px solid color-mix(in srgb,var(--accent) 65%,#36485c);background:#06101bd9;color:var(--accent);border-radius:999px;padding:7px 10px;font-size:9px;font-weight:950;letter-spacing:.18em;box-shadow:0 0 20px color-mix(in srgb,var(--accent) 25%,transparent)}
.p6Name{font-size:34px;font-weight:950;line-height:1;margin-top:10px;letter-spacing:-.035em;text-shadow:0 10px 32px #000}.p6Serial{font-size:11px;color:#9eb0c7;margin-top:8px;letter-spacing:.07em}
.p6Status{position:absolute;z-index:13;left:0;right:0;bottom:13%;text-align:center;font-size:9px;font-weight:950;letter-spacing:.28em;color:#dffbff;text-shadow:0 0 12px var(--accent);opacity:.75}
.p6Dust{position:absolute;inset:0;z-index:11;pointer-events:none}.p6Dust i{position:absolute;width:3px;height:3px;border-radius:50%;background:var(--accent);box-shadow:0 0 10px var(--accent);opacity:0}

/* Essential hatch motion uses CSS keyframes for Telegram iOS WebView reliability. */
@keyframes p6TopIn{from{opacity:0;transform:translateY(-7px)}to{opacity:1;transform:translateY(0)}}
@keyframes p6ChamberIn{from{transform:translate(-50%,-50%) scale(.96)}to{transform:translate(-50%,-50%) scale(1)}}
@keyframes p6EggArrive{0%{transform:translate(-50%,-50%) scale(.82);opacity:.15;filter:brightness(.55)}65%{transform:translate(-50%,-50%) scale(.94);opacity:1;filter:brightness(1.08)}100%{transform:translate(-50%,-50%) scale(.9);opacity:1;filter:brightness(1)}}
@keyframes p6ScanSweep{0%{opacity:0;transform:translateY(0)}12%{opacity:.9}82%{opacity:.8;transform:translateY(330px)}100%{opacity:0;transform:translateY(360px)}}
@keyframes p6EggShake{0%,100%{transform:translate(-50%,-50%) scale(.92) rotate(0)}16%{transform:translate(-50%,-50%) scale(.93) rotate(-2deg)}34%{transform:translate(-50%,-50%) scale(.94) rotate(3deg)}54%{transform:translate(-50%,-50%) scale(.94) rotate(-3.4deg)}74%{transform:translate(-50%,-50%) scale(.95) rotate(2deg)}}
@keyframes p6CrackOn{0%{opacity:0;filter:brightness(.8)}35%{opacity:1;filter:brightness(2)}100%{opacity:1;filter:brightness(1.15)}}
@keyframes p6FlashBurst{0%{opacity:0;transform:translate(-50%,-50%) scale(.1)}24%{opacity:1;transform:translate(-50%,-50%) scale(1)}100%{opacity:0;transform:translate(-50%,-50%) scale(7.5)}}
@keyframes p6EggVanish{0%{opacity:1;transform:translate(-50%,-50%) scale(.95);filter:brightness(1)}48%{opacity:.95;transform:translate(-50%,-50%) scale(1.05);filter:brightness(1.8)}100%{opacity:0;transform:translate(-50%,-50%) scale(1.24);filter:brightness(2.5) blur(8px)}}
@keyframes p6CreatureWake{0%{opacity:.08;filter:brightness(.2) saturate(.45) blur(5px);transform:scale(.9)}62%{opacity:.88;filter:brightness(1.2) saturate(1.22) blur(0);transform:scale(1.045)}100%{opacity:1;filter:brightness(1) saturate(1.06) blur(0);transform:scale(1)}}
@keyframes p6MetaIn{0%{opacity:0;transform:translateY(18px)}70%{opacity:1;transform:translateY(-4px)}100%{opacity:1;transform:translateY(0)}}
@keyframes p6BtnsIn{from{opacity:0;transform:translateY(24px)}to{opacity:1;transform:translateY(0)}}
.p6Scene.p6Run .p6Top{animation:p6TopIn .42s ease-out forwards;-webkit-animation:p6TopIn .42s ease-out forwards}
.p6Scene.p6Run .p6Chamber{animation:p6ChamberIn .65s ease-out forwards;-webkit-animation:p6ChamberIn .65s ease-out forwards}
.p6Scene.p6Run .p6EggWrap{animation:p6EggArrive .7s cubic-bezier(.2,.75,.2,1) forwards;-webkit-animation:p6EggArrive .7s cubic-bezier(.2,.75,.2,1) forwards}
.p6Scene.p6Run .p6Scan{animation:p6ScanSweep .93s ease-in-out forwards;-webkit-animation:p6ScanSweep .93s ease-in-out forwards}
.p6Scene.p6Fracture .p6EggWrap{animation:p6EggShake .72s ease-in-out forwards;-webkit-animation:p6EggShake .72s ease-in-out forwards}
.p6Scene.p6Fracture .p6Cracks{animation:p6CrackOn .36s ease-out forwards;-webkit-animation:p6CrackOn .36s ease-out forwards}
.p6Scene.p6Awaken .p6Flash{animation:p6FlashBurst .76s ease-out forwards;-webkit-animation:p6FlashBurst .76s ease-out forwards}
.p6Scene.p6Awaken .p6EggWrap{animation:p6EggVanish .66s cubic-bezier(.15,.75,.18,1) forwards;-webkit-animation:p6EggVanish .66s cubic-bezier(.15,.75,.18,1) forwards}
.p6Scene.p6Awaken .p6Creature{animation:p6CreatureWake 1.08s cubic-bezier(.12,.9,.18,1.05) forwards;-webkit-animation:p6CreatureWake 1.08s cubic-bezier(.12,.9,.18,1.05) forwards}
.p6Scene.p6Confirmed .p6Meta{animation:p6MetaIn .62s cubic-bezier(.2,.8,.2,1) forwards;-webkit-animation:p6MetaIn .62s cubic-bezier(.2,.8,.2,1) forwards}
`;
const st=document.createElement('style');st.textContent=css;document.head.appendChild(st);
const preload=new Image();preload.src=EGG;

let ac=null;
function unlockAudio(){try{const A=window.AudioContext||window.webkitAudioContext;if(!A)return;if(!ac)ac=new A();if(ac.state==='suspended')ac.resume()}catch(e){}}
function noise(t,d=.06,v=.2,cut=900){if(!ac||ac.state!=='running')return;const sr=ac.sampleRate,b=ac.createBuffer(1,Math.max(1,Math.floor(sr*d)),sr),a=b.getChannelData(0);for(let i=0;i<a.length;i++)a[i]=(Math.random()*2-1)*(1-i/a.length);const s=ac.createBufferSource(),f=ac.createBiquadFilter(),g=ac.createGain();s.buffer=b;f.type='highpass';f.frequency.value=cut;g.gain.setValueAtTime(v,t);g.gain.exponentialRampToValueAtTime(.001,t+d);s.connect(f);f.connect(g);g.connect(ac.destination);s.start(t)}
function hatchSound(){try{unlockAudio();if(!ac||ac.state!=='running')return;const n=ac.currentTime+.02;const low=ac.createOscillator(),lg=ac.createGain();low.type='sine';low.frequency.setValueAtTime(48,n);low.frequency.exponentialRampToValueAtTime(112,n+1.55);lg.gain.setValueAtTime(.001,n);lg.gain.exponentialRampToValueAtTime(.075,n+.16);lg.gain.exponentialRampToValueAtTime(.001,n+1.62);low.connect(lg);lg.connect(ac.destination);low.start(n);low.stop(n+1.65);noise(n+.66,.055,.18,1250);noise(n+.94,.07,.30,950);noise(n+1.22,.12,.48,720);const w=ac.createOscillator(),wg=ac.createGain();w.type='triangle';w.frequency.setValueAtTime(190,n+1.12);w.frequency.exponentialRampToValueAtTime(900,n+1.72);wg.gain.setValueAtTime(.001,n+1.08);wg.gain.exponentialRampToValueAtTime(.07,n+1.22);wg.gain.exponentialRampToValueAtTime(.001,n+1.88);w.connect(wg);wg.connect(ac.destination);w.start(n+1.08);w.stop(n+1.9)}catch(e){}}
function haptics(){try{const h=window.Telegram?.WebApp?.HapticFeedback;h?.impactOccurred?.('light');setTimeout(()=>h?.impactOccurred?.('medium'),720);setTimeout(()=>h?.impactOccurred?.('heavy'),1230);setTimeout(()=>h?.notificationOccurred?.('success'),2080)}catch(e){}}
function rarity(i){return String(i?.rarity||'common').toLowerCase()}
function artUrl(i){return window.DROP1_ART?.[i?.id||i?.character_id]||''}
function modelUrl(i){return window.DROP1_MODEL?.[i?.id||i?.character_id]||''}
function addDust(root){if(IS_IOS)return;for(let i=0;i<26;i++){const p=document.createElement('i');p.style.left=(38+Math.random()*24)+'%';p.style.top=(39+Math.random()*18)+'%';root.appendChild(p);setTimeout(()=>{try{p.animate?.([{opacity:0,transform:'translate(0,0) scale(.2)'},{opacity:.9,transform:`translate(${(Math.random()-.5)*130}px,${-30-Math.random()*100}px) scale(1)`},{opacity:0,transform:`translate(${(Math.random()-.5)*220}px,${-100-Math.random()*170}px) scale(.2)`}],{duration:1000+Math.random()*700,easing:'ease-out',fill:'forwards'})}catch(e){}},1120+Math.random()*220)}}

function clamp01(v){return Math.max(0,Math.min(1,v))}
function easeOutCubic(t){t=clamp01(t);return 1-Math.pow(1-t,3)}
function easeInOut(t){t=clamp01(t);return t<.5?2*t*t:1-Math.pow(-2*t+2,2)/2}
function iosShake(t){
  // deterministic damped shake: visible on iPhone but settles before reveal
  const amp=(1-clamp01(t))*5.2;
  return Math.sin(t*42)*amp + Math.sin(t*71)*amp*.38;
}
function runIOSHatch(scene,refs,box,r){
  const {top,ch,creature,scan,egg,cracks,flash,status,meta}=refs;
  const started=performance.now();
  const duration=3150;
  // Reset every property we drive so a cached prior reveal cannot leak state.
  top.style.opacity='0'; ch.style.transform='translate(-50%,-50%) scale(.96)';
  egg.style.opacity='1'; egg.style.transform='translate(-50%,-50%) scale(.82)';
  egg.style.filter='brightness(.72)';
  cracks.style.opacity='0'; scan.style.opacity='0'; flash.style.opacity='0';
  creature.style.opacity='.08'; creature.style.transform='scale(.9)';
  creature.style.filter='brightness(.25) saturate(.55)';
  meta.style.opacity='0';
  if(box){box.style.opacity='0';box.style.transform='translateY(24px)';box.style.animation='none';box.style.webkitAnimation='none'}

  function frame(now){
    const ms=now-started;

    // intro 0-680ms
    const intro=easeOutCubic(ms/680);
    top.style.opacity=String(intro);
    ch.style.transform='translate(-50%,-50%) scale('+(0.96+0.04*intro).toFixed(4)+')';
    const eggScale=.82+.10*intro;
    egg.style.transform='translate(-50%,-50%) scale('+eggScale.toFixed(4)+')';
    egg.style.filter='brightness('+(0.72+.28*intro).toFixed(3)+')';

    // scanner 110-950ms
    const sp=clamp01((ms-110)/840);
    if(sp>0&&sp<1){
      scan.style.opacity=String(Math.sin(Math.PI*sp)*.9);
      scan.style.transform='translateY('+(350*sp).toFixed(1)+'px)';
    }else if(sp>=1){scan.style.opacity='0'}

    // fracture 690-1420ms
    const fp=clamp01((ms-690)/730);
    if(fp>0){
      status.textContent='SHELL FRACTURE';
      cracks.style.opacity=String(Math.min(1,fp*3));
      cracks.style.filter='brightness('+(1+Math.sin(fp*Math.PI)*1.15).toFixed(2)+') drop-shadow(0 0 12px var(--accent))';
      const rot=iosShake(fp);
      const sc=.92+.035*Math.sin(Math.PI*fp);
      egg.style.transform='translate(-50%,-50%) scale('+sc.toFixed(4)+') rotate('+rot.toFixed(2)+'deg)';
    }

    // awakening 1320-2150ms
    const ap=clamp01((ms-1320)/830);
    if(ap>0){
      status.textContent='SPECIMEN AWAKENING';
      const burst=Math.sin(Math.PI*clamp01(ap*1.35));
      flash.style.opacity=String(Math.max(0,burst));
      flash.style.transform='translate(-50%,-50%) scale('+(0.2+7.0*easeOutCubic(ap)).toFixed(3)+')';
      egg.style.opacity=String(1-easeOutCubic(ap));
      egg.style.transform='translate(-50%,-50%) scale('+(0.95+.30*easeOutCubic(ap)).toFixed(3)+')';
      egg.style.filter='brightness('+(1+1.7*ap).toFixed(2)+')';
      const cp=easeOutCubic(clamp01((ms-1450)/760));
      creature.style.opacity=String(.08+.92*cp);
      creature.style.transform='scale('+(0.90+.10*cp+.035*Math.sin(cp*Math.PI)).toFixed(3)+')';
      creature.style.filter='brightness('+(0.25+.78*cp).toFixed(2)+') saturate('+(0.55+.5*cp).toFixed(2)+')';
    }

    // confirm 2250+
    const mp=easeOutCubic((ms-2250)/520);
    if(mp>0){
      status.textContent='SPECIMEN CONFIRMED';
      status.style.opacity=String(1-mp);
      meta.style.opacity=String(mp);
      meta.style.transform='translateY('+(18*(1-mp)).toFixed(1)+'px)';
      if(box){box.style.opacity=String(mp);box.style.transform='translateY('+(24*(1-mp)).toFixed(1)+'px)'}
    }

    if(ms<duration && r.dataset.hatching==='1') requestAnimationFrame(frame);
    else {
      r.dataset.hatching='0';
      egg.style.opacity='0';
      creature.style.opacity='1';
      creature.style.transform='scale(1)';
      creature.style.filter='brightness(1) saturate(1.05)';
      meta.style.opacity='1';
      meta.style.transform='translateY(0)';
      if(box){box.style.opacity='1';box.style.transform='translateY(0)'}
    }
  }
  requestAnimationFrame(frame);
}

function showRevealV6(item){
 if(!item)return;const r=document.getElementById('reveal');if(!r)return;
 r.querySelector('.p6Scene')?.remove();r.querySelector('.phScene')?.remove();
 r.className='reveal primalV6 hatch-'+rarity(item);r.style.display='flex';r.dataset.hatching='1';
 const rr=document.getElementById('revealRarity'),ra=document.getElementById('revealArt'),rn=document.getElementById('revealName'),rs=document.getElementById('revealSerial'),box=r.querySelector('.revealBox');
 if(rr)rr.textContent='';if(ra)ra.innerHTML='';if(rn)rn.textContent='';if(rs)rs.textContent='';if(box){box.style.opacity='0';box.style.transform='translateY(24px)'}
 const url=artUrl(item),model=modelUrl(item),scene=document.createElement('div');scene.className='p6Scene';
 const creatureMarkup=(model&&!IS_IOS)
   ? `<div class="p6Creature"><img class="p6Poster" src="${url}" alt=""><model-viewer src="${model}" poster="${url}" alt="${item.name||'Creature'} 3D" auto-rotate auto-rotate-delay="0" rotation-per-second="14deg" interaction-prompt="none" shadow-intensity="1.25" shadow-softness=".8" exposure="1.08" environment-image="neutral" camera-orbit="20deg 75deg auto" camera-controls="false" loading="eager" reveal="auto"></model-viewer></div>`
   : `<div class="p6Creature">${url?`<img src="${url}" alt="${item.name||'Creature'}">`:'<div style="font-size:130px;display:grid;place-items:center;height:100%">🦖</div>'}</div>`;
 scene.innerHTML=`<div class="p6Grid"></div><div class="p6Top"><div class="p6Kicker">DROP1 // PRIMAL HATCH</div><div class="p6Signal">LIFE SIGNAL</div></div><div class="p6Chamber">${creatureMarkup}<div class="p6Scan"></div><div class="p6Flash"></div><div class="p6EggWrap"><div class="p6EggAura"></div><div class="p6EggCssFallback"></div><div class="p6EggVisual" role="img" aria-label="Primal egg"></div><div class="p6Cracks"></div></div></div><div class="p6Dust"></div><div class="p6Status">INCUBATION LOCKED</div><div class="p6Meta"><div class="p6Rarity">◆ ${String(item.rarity||'common').toUpperCase()}</div><div class="p6Name">${item.name||'Creature'}</div><div class="p6Serial">#${String(item.serial_no||0).padStart(6,'0')} · PWR ${item.power||0} · LCK ${item.luck||0}</div></div>`;
 r.insertBefore(scene,r.firstChild);
 const mv=scene.querySelector('model-viewer'),poster=scene.querySelector('.p6Poster');
 if(mv){
   mv.addEventListener('load',()=>{if(poster)poster.style.opacity='0'},{once:true});
   mv.addEventListener('error',()=>{mv.remove();if(poster)poster.style.opacity='1'},{once:true});
 }
 const top=scene.querySelector('.p6Top'),ch=scene.querySelector('.p6Chamber'),creature=scene.querySelector('.p6Creature'),scan=scene.querySelector('.p6Scan'),egg=scene.querySelector('.p6EggWrap'),cracks=scene.querySelector('.p6Cracks'),flash=scene.querySelector('.p6Flash'),status=scene.querySelector('.p6Status'),meta=scene.querySelector('.p6Meta'),dust=scene.querySelector('.p6Dust');
 hatchSound();haptics();addDust(dust);
 if(IS_IOS){
   runIOSHatch(scene,{top,ch,creature,scan,egg,cracks,flash,status,meta},box,r);
 }else{
   requestAnimationFrame(()=>requestAnimationFrame(()=>scene.classList.add('p6Run')));
   setTimeout(()=>{status.textContent='SHELL FRACTURE';scene.classList.add('p6Fracture')},690);
   setTimeout(()=>{status.textContent='SPECIMEN AWAKENING';scene.classList.add('p6Awaken')},1320);
   setTimeout(()=>{
     status.textContent='SPECIMEN CONFIRMED';
     scene.classList.add('p6Confirmed');
     status.style.opacity='0';
     if(box){
       box.style.opacity='1';
       box.style.transform='translateY(0)';
       box.style.animation='p6BtnsIn .52s ease-out forwards';
       box.style.webkitAnimation='p6BtnsIn .52s ease-out forwards';
     }
   },2280);
   setTimeout(()=>{r.dataset.hatching='0'},3050);
 }
}
document.addEventListener('pointerdown',unlockAudio,{capture:true,passive:true});document.addEventListener('touchstart',unlockAudio,{capture:true,passive:true});window.showReveal=showRevealV6;
})();