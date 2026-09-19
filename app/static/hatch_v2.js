(function(){
window.DROP1_PREMIUM_HATCH=true;
const EGG="/static/assets/primal-egg.webp";
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
.p6Creature img{position:absolute;left:0;top:-7%;width:100%;height:126%;object-fit:cover;object-position:50% 18%;display:block}
.p6Scan{position:absolute;z-index:8;left:7%;right:7%;top:16%;height:2px;background:linear-gradient(90deg,transparent,var(--accent),#fff,var(--accent),transparent);box-shadow:0 0 18px var(--accent),0 0 38px var(--accent);opacity:0}
.p6EggWrap{position:absolute;z-index:11;left:50%;top:47%;width:220px;height:270px;transform:translate(-50%,-50%) scale(.9);display:grid;place-items:center;will-change:transform,filter,opacity}
.p6EggImg{width:100%;height:100%;object-fit:contain;display:block;filter:drop-shadow(0 22px 26px #000c) drop-shadow(0 0 20px color-mix(in srgb,var(--accent) 38%,transparent)) drop-shadow(0 0 52px color-mix(in srgb,var(--accent2) 30%,transparent));user-select:none;-webkit-user-drag:none}
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
function addDust(root){for(let i=0;i<26;i++){const p=document.createElement('i');p.style.left=(38+Math.random()*24)+'%';p.style.top=(39+Math.random()*18)+'%';root.appendChild(p);setTimeout(()=>p.animate([{opacity:0,transform:'translate(0,0) scale(.2)'},{opacity:.9,transform:`translate(${(Math.random()-.5)*130}px,${-30-Math.random()*100}px) scale(1)`},{opacity:0,transform:`translate(${(Math.random()-.5)*220}px,${-100-Math.random()*170}px) scale(.2)`}],{duration:1000+Math.random()*700,easing:'ease-out',fill:'forwards'}),1120+Math.random()*220)}}
function showRevealV6(item){
 if(!item)return;const r=document.getElementById('reveal');if(!r)return;
 r.querySelector('.p6Scene')?.remove();r.querySelector('.phScene')?.remove();
 r.className='reveal primalV6 hatch-'+rarity(item);r.style.display='flex';r.dataset.hatching='1';
 const rr=document.getElementById('revealRarity'),ra=document.getElementById('revealArt'),rn=document.getElementById('revealName'),rs=document.getElementById('revealSerial'),box=r.querySelector('.revealBox');
 if(rr)rr.textContent='';if(ra)ra.innerHTML='';if(rn)rn.textContent='';if(rs)rs.textContent='';if(box){box.style.opacity='0';box.style.transform='translateY(24px)'}
 const url=artUrl(item),scene=document.createElement('div');scene.className='p6Scene';
 scene.innerHTML=`<div class="p6Grid"></div><div class="p6Top"><div class="p6Kicker">DROP1 // PRIMAL HATCH</div><div class="p6Signal">LIFE SIGNAL</div></div><div class="p6Chamber"><div class="p6Creature">${url?`<img src="${url}" alt="${item.name||'Creature'}">`:'<div style="font-size:130px;display:grid;place-items:center;height:100%">🦖</div>'}</div><div class="p6Scan"></div><div class="p6Flash"></div><div class="p6EggWrap"><div class="p6EggAura"></div><img class="p6EggImg" src="${EGG}" alt="Primal egg"><div class="p6Cracks"></div></div></div><div class="p6Dust"></div><div class="p6Status">INCUBATION LOCKED</div><div class="p6Meta"><div class="p6Rarity">◆ ${String(item.rarity||'common').toUpperCase()}</div><div class="p6Name">${item.name||'Creature'}</div><div class="p6Serial">#${String(item.serial_no||0).padStart(6,'0')} · PWR ${item.power||0} · LCK ${item.luck||0}</div></div>`;
 r.insertBefore(scene,r.firstChild);
 const top=scene.querySelector('.p6Top'),ch=scene.querySelector('.p6Chamber'),creature=scene.querySelector('.p6Creature'),scan=scene.querySelector('.p6Scan'),egg=scene.querySelector('.p6EggWrap'),cracks=scene.querySelector('.p6Cracks'),flash=scene.querySelector('.p6Flash'),status=scene.querySelector('.p6Status'),meta=scene.querySelector('.p6Meta'),dust=scene.querySelector('.p6Dust');
 hatchSound();haptics();addDust(dust);
 top.animate([{opacity:0,transform:'translateY(-7px)'},{opacity:1,transform:'translateY(0)'}],{duration:420,fill:'forwards'});
 ch.animate([{transform:'translate(-50%,-50%) scale(.96)'},{transform:'translate(-50%,-50%) scale(1)'}],{duration:650,easing:'ease-out',fill:'forwards'});
 egg.animate([{transform:'translate(-50%,-50%) scale(.84)',opacity:.2,filter:'brightness(.55)'},{transform:'translate(-50%,-50%) scale(.92)',opacity:1,filter:'brightness(1)'},{transform:'translate(-50%,-50%) scale(.9)',opacity:1,filter:'brightness(1)'}],{duration:700,easing:'cubic-bezier(.2,.75,.2,1)',fill:'forwards'});
 scan.animate([{opacity:0,transform:'translateY(0)'},{opacity:.9,transform:'translateY(0)'},{opacity:.8,transform:'translateY(330px)'},{opacity:0,transform:'translateY(360px)'}],{duration:930,easing:'ease-in-out',fill:'forwards'});
 setTimeout(()=>{status.textContent='SHELL FRACTURE';cracks.animate([{opacity:0},{opacity:1}],{duration:240,fill:'forwards'});cracks.querySelectorAll(':scope:before,:scope:after');egg.animate([{transform:'translate(-50%,-50%) scale(.9) rotate(0)'},{transform:'translate(-50%,-50%) scale(.91) rotate(-1.6deg)'},{transform:'translate(-50%,-50%) scale(.92) rotate(2.4deg)'},{transform:'translate(-50%,-50%) scale(.92) rotate(-2.8deg)'},{transform:'translate(-50%,-50%) scale(.93) rotate(1.4deg)'},{transform:'translate(-50%,-50%) scale(.93) rotate(0)'}],{duration:720,easing:'ease-in-out',fill:'forwards'});scene.querySelector('.p6Cracks').animate([{filter:'brightness(1)'},{filter:'brightness(1.8)'},{filter:'brightness(1.1)'}],{duration:680,fill:'forwards'})},690);
 setTimeout(()=>{status.textContent='SPECIMEN AWAKENING';flash.animate([{opacity:0,transform:'translate(-50%,-50%) scale(.1)'},{opacity:1,transform:'translate(-50%,-50%) scale(1)'},{opacity:0,transform:'translate(-50%,-50%) scale(7.5)'}],{duration:760,easing:'ease-out',fill:'forwards'});egg.animate([{opacity:1,transform:'translate(-50%,-50%) scale(.93)',filter:'brightness(1)'},{opacity:.85,transform:'translate(-50%,-50%) scale(1.02)',filter:'brightness(1.8)'},{opacity:0,transform:'translate(-50%,-50%) scale(1.22)',filter:'brightness(2.5) blur(8px)'}],{duration:660,easing:'cubic-bezier(.15,.75,.18,1)',fill:'forwards'});creature.animate([{opacity:.08,filter:'brightness(.2) saturate(.45) blur(5px)',transform:'scale(.9)'},{opacity:.82,filter:'brightness(1.18) saturate(1.2) blur(0)',transform:'scale(1.04)'},{opacity:1,filter:'brightness(1) saturate(1.06) blur(0)',transform:'scale(1)'}],{duration:1080,easing:'cubic-bezier(.12,.9,.18,1.05)',fill:'forwards'})},1320);
 setTimeout(()=>{status.textContent='SPECIMEN CONFIRMED';status.animate([{opacity:.78},{opacity:0}],{duration:480,fill:'forwards'});meta.animate([{opacity:0,transform:'translateY(18px)'},{opacity:1,transform:'translateY(-4px)'},{opacity:1,transform:'translateY(0)'}],{duration:620,easing:'cubic-bezier(.2,.8,.2,1)',fill:'forwards'});if(box)box.animate([{opacity:0,transform:'translateY(24px)'},{opacity:1,transform:'translateY(0)'}],{duration:520,easing:'ease-out',fill:'forwards'})},2280);
 setTimeout(()=>{r.dataset.hatching='0'},3050)
}
document.addEventListener('pointerdown',unlockAudio,{capture:true,passive:true});document.addEventListener('touchstart',unlockAudio,{capture:true,passive:true});window.showReveal=showRevealV6;
})();