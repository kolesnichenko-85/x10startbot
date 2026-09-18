(function(){
const css=`
.reveal.primalV5{position:fixed!important;inset:0!important;overflow:hidden!important;padding:0!important;background:#02040a!important;display:flex!important;align-items:stretch!important;justify-content:center!important;--accent:#58e7ff;--accent2:#744dff}
.reveal.primalV5.hatch-common{--accent:#dff7ff;--accent2:#6987a3}.reveal.primalV5.hatch-rare{--accent:#55e6ff;--accent2:#6857ff}.reveal.primalV5.hatch-epic{--accent:#e168ff;--accent2:#7047ff}.reveal.primalV5.hatch-legendary{--accent:#ffe16d;--accent2:#ff861d}.reveal.primalV5.hatch-mythic{--accent:#84ffff;--accent2:#ff55dd}
.reveal.primalV5 .revealBox{position:absolute!important;z-index:30!important;left:16px!important;right:16px!important;bottom:calc(16px + env(safe-area-inset-bottom))!important;max-width:none!important;width:auto!important;opacity:0;transform:translateY(24px)}
.reveal.primalV5 .revealEyebrow,.reveal.primalV5 .revealCard,.reveal.primalV5 #revealName,.reveal.primalV5 #revealSerial{display:none!important}
.reveal.primalV5 .revealBtns{display:grid!important;grid-template-columns:1.15fr 1fr!important;gap:9px!important;margin:0!important}
.reveal.primalV5 .revealBtns .btn{padding:14px 10px!important;border-radius:16px!important;font-size:13px!important}
.reveal.primalV5 #revealAgain{background:linear-gradient(180deg,#f8fdff,#dcebff)!important;color:#07101c!important;border:1px solid var(--accent)!important;box-shadow:0 0 24px color-mix(in srgb,var(--accent) 35%,transparent)!important}
.reveal.primalV5 #revealClose{background:#09111ee8!important;color:#dceaff!important;border:1px solid #2e405a!important}

.phScene{position:absolute;inset:0;z-index:10;overflow:hidden;background:
 radial-gradient(circle at 50% 34%,color-mix(in srgb,var(--accent2) 28%,#0b1321) 0,#07101b 35%,#02040a 72%);
 perspective:900px}
.phScene:before{content:"";position:absolute;inset:0;z-index:1;background:
 linear-gradient(180deg,#02040ac7 0,transparent 18%,transparent 67%,#02040af2 100%),
 radial-gradient(circle at 50% 38%,transparent 0 42%,#0008 82%);pointer-events:none}
.phGrid{position:absolute;left:-15%;right:-15%;bottom:-8%;height:38%;z-index:0;opacity:.22;transform:perspective(520px) rotateX(64deg);background-image:linear-gradient(#58e7ff20 1px,transparent 1px),linear-gradient(90deg,#58e7ff20 1px,transparent 1px);background-size:34px 34px;mask-image:linear-gradient(180deg,transparent,#000 25%,#000)}
.phTop{position:absolute;z-index:12;left:20px;right:20px;top:calc(26px + env(safe-area-inset-top));display:flex;align-items:center;justify-content:space-between;gap:12px;opacity:0}
.phKicker{font-size:9px;font-weight:950;letter-spacing:.25em;color:#aabbd0}.phSignal{font-size:9px;font-weight:950;letter-spacing:.14em;color:var(--accent);border:1px solid color-mix(in srgb,var(--accent) 50%,#26394f);background:#06101bd9;border-radius:999px;padding:7px 9px;box-shadow:0 0 18px color-mix(in srgb,var(--accent) 20%,transparent)}
.phChamber{position:absolute;left:50%;top:45%;z-index:5;width:min(92vw,430px);height:min(63vh,560px);transform:translate(-50%,-50%);border-radius:34px;overflow:hidden;border:1px solid #334b6a;background:radial-gradient(circle at 50% 35%,#17365c,#07101a 70%);box-shadow:0 35px 90px #000c,inset 0 0 55px #5aa7ff0d}
.phChamber:before,.phChamber:after{content:"";position:absolute;z-index:9;left:12%;right:12%;height:2px;background:linear-gradient(90deg,transparent,var(--accent),transparent);box-shadow:0 0 16px var(--accent);opacity:.45}
.phChamber:before{top:8%}.phChamber:after{bottom:8%}
.phCreature{position:absolute;inset:0;z-index:4;overflow:hidden;opacity:.13;filter:brightness(.35) saturate(.55) blur(3px);transform:scale(.9)}
.phCreature img{position:absolute;left:0;top:-7%;width:100%;height:126%;object-fit:cover;object-position:50% 18%;display:block}
.phScan{position:absolute;z-index:8;left:7%;right:7%;top:16%;height:2px;background:linear-gradient(90deg,transparent,var(--accent),#fff,var(--accent),transparent);box-shadow:0 0 18px var(--accent),0 0 38px var(--accent);opacity:0}
.phEgg{position:absolute;z-index:7;left:50%;top:47%;width:178px;height:232px;transform:translate(-50%,-50%);filter:drop-shadow(0 0 30px color-mix(in srgb,var(--accent) 50%,transparent));}
.phEggHalf{position:absolute;inset:0;border:1px solid color-mix(in srgb,var(--accent) 75%,#fff);background:
 radial-gradient(circle at 34% 20%,#fff8 0,transparent 12%),
 radial-gradient(circle at 44% 30%,color-mix(in srgb,var(--accent) 30%,transparent),transparent 45%),
 linear-gradient(145deg,#182944f0,#080d18f5 55%,#211841f4);
 box-shadow:inset -18px -26px 38px #0009,inset 10px 10px 18px #ffffff0c,0 0 22px color-mix(in srgb,var(--accent) 28%,transparent)}
.phEggTop{clip-path:polygon(0 0,100% 0,100% 52%,86% 49%,73% 57%,60% 49%,47% 58%,31% 48%,15% 56%,0 51%);border-radius:52% 48% 0 0/62% 62% 0 0}
.phEggBottom{clip-path:polygon(0 50%,15% 55%,31% 47%,47% 57%,60% 48%,73% 56%,86% 48%,100% 51%,100% 100%,0 100%);border-radius:0 0 47% 53%/0 0 39% 39%}
.phCrack{position:absolute;z-index:10;left:50%;top:27%;width:6px;height:112px;transform:translateX(-50%) rotate(8deg) scaleY(0);transform-origin:top;background:#fff;filter:drop-shadow(0 0 7px var(--accent)) drop-shadow(0 0 18px var(--accent));clip-path:polygon(40% 0,100% 0,58% 25%,100% 25%,23% 54%,72% 54%,0 100%,26% 65%,0 65%,55% 34%,17% 34%);opacity:0}
.phFlash{position:absolute;z-index:6;left:50%;top:47%;width:24px;height:24px;border-radius:50%;transform:translate(-50%,-50%) scale(.1);opacity:0;background:#fff;box-shadow:0 0 30px 20px var(--accent),0 0 110px 72px var(--accent2)}
.phMeta{position:absolute;z-index:14;left:22px;right:22px;bottom:calc(99px + env(safe-area-inset-bottom));text-align:center;opacity:0;transform:translateY(18px)}
.phRarity{display:inline-flex;align-items:center;gap:6px;border:1px solid color-mix(in srgb,var(--accent) 65%,#36485c);background:#06101bd9;color:var(--accent);border-radius:999px;padding:7px 10px;font-size:9px;font-weight:950;letter-spacing:.18em;box-shadow:0 0 20px color-mix(in srgb,var(--accent) 25%,transparent)}
.phName{font-size:34px;font-weight:950;line-height:1;margin-top:10px;letter-spacing:-.035em;text-shadow:0 10px 32px #000}
.phSerial{font-size:11px;color:#9eb0c7;margin-top:8px;letter-spacing:.07em}
.phStatus{position:absolute;z-index:13;left:0;right:0;bottom:13%;text-align:center;font-size:9px;font-weight:950;letter-spacing:.28em;color:#dffbff;text-shadow:0 0 12px var(--accent);opacity:.75}
.phDust{position:absolute;inset:0;z-index:11;pointer-events:none}.phDust i{position:absolute;width:3px;height:3px;border-radius:50%;background:var(--accent);box-shadow:0 0 10px var(--accent);opacity:0}
`;
const st=document.createElement('style');st.textContent=css;document.head.appendChild(st);

let ac=null;
function unlockAudio(){try{const A=window.AudioContext||window.webkitAudioContext;if(!A)return;if(!ac)ac=new A();if(ac.state==='suspended')ac.resume()}catch(e){}}
function noise(t,d=.06,v=.2,cut=900){if(!ac||ac.state!=='running')return;const sr=ac.sampleRate,b=ac.createBuffer(1,Math.max(1,Math.floor(sr*d)),sr),a=b.getChannelData(0);for(let i=0;i<a.length;i++)a[i]=(Math.random()*2-1)*(1-i/a.length);const s=ac.createBufferSource(),f=ac.createBiquadFilter(),g=ac.createGain();s.buffer=b;f.type='highpass';f.frequency.value=cut;g.gain.setValueAtTime(v,t);g.gain.exponentialRampToValueAtTime(.001,t+d);s.connect(f);f.connect(g);g.connect(ac.destination);s.start(t)}
function hatchSound(){try{unlockAudio();if(!ac||ac.state!=='running')return;const n=ac.currentTime+.02;const low=ac.createOscillator(),lg=ac.createGain();low.type='sine';low.frequency.setValueAtTime(52,n);low.frequency.exponentialRampToValueAtTime(118,n+1.5);lg.gain.setValueAtTime(.001,n);lg.gain.exponentialRampToValueAtTime(.08,n+.18);lg.gain.exponentialRampToValueAtTime(.001,n+1.55);low.connect(lg);lg.connect(ac.destination);low.start(n);low.stop(n+1.6);noise(n+.65,.055,.20,1200);noise(n+.92,.07,.32,980);noise(n+1.18,.11,.5,760);const w=ac.createOscillator(),wg=ac.createGain();w.type='triangle';w.frequency.setValueAtTime(210,n+1.12);w.frequency.exponentialRampToValueAtTime(880,n+1.65);wg.gain.setValueAtTime(.001,n+1.08);wg.gain.exponentialRampToValueAtTime(.08,n+1.22);wg.gain.exponentialRampToValueAtTime(.001,n+1.82);w.connect(wg);wg.connect(ac.destination);w.start(n+1.08);w.stop(n+1.85)}catch(e){}}
function haptics(){try{const h=window.Telegram?.WebApp?.HapticFeedback;h?.impactOccurred?.('light');setTimeout(()=>h?.impactOccurred?.('medium'),720);setTimeout(()=>h?.impactOccurred?.('heavy'),1160);setTimeout(()=>h?.notificationOccurred?.('success'),2060)}catch(e){}}
function rarity(i){return String(i?.rarity||'common').toLowerCase()}
function artUrl(i){return window.DROP1_ART?.[i?.id||i?.character_id]||''}
function addDust(root){for(let i=0;i<24;i++){const p=document.createElement('i');p.style.left=(38+Math.random()*24)+'%';p.style.top=(38+Math.random()*21)+'%';root.appendChild(p);setTimeout(()=>p.animate([{opacity:0,transform:'translate(0,0) scale(.2)'},{opacity:.9,transform:`translate(${(Math.random()-.5)*120}px,${-35-Math.random()*110}px) scale(1)`},{opacity:0,transform:`translate(${(Math.random()-.5)*210}px,${-95-Math.random()*180}px) scale(.2)`}],{duration:1000+Math.random()*700,easing:'ease-out',fill:'forwards'}),1080+Math.random()*220)}}

function showRevealV5(item){
 if(!item)return;const r=document.getElementById('reveal');if(!r)return;
 r.querySelector('.phScene')?.remove();
 r.className='reveal primalV5 hatch-'+rarity(item);r.style.display='flex';r.dataset.hatching='1';
 const rr=document.getElementById('revealRarity'),ra=document.getElementById('revealArt'),rn=document.getElementById('revealName'),rs=document.getElementById('revealSerial'),box=r.querySelector('.revealBox');
 if(rr)rr.textContent='';if(ra)ra.innerHTML='';if(rn)rn.textContent='';if(rs)rs.textContent='';if(box){box.style.opacity='0';box.style.transform='translateY(24px)'}
 const url=artUrl(item);
 const scene=document.createElement('div');scene.className='phScene';
 scene.innerHTML=`<div class="phGrid"></div><div class="phTop"><div class="phKicker">DROP1 // PRIMAL HATCH</div><div class="phSignal">LIFE SIGNAL</div></div><div class="phChamber"><div class="phCreature">${url?`<img src="${url}" alt="${item.name||'Creature'}">`:'<div style="font-size:130px;display:grid;place-items:center;height:100%">🦖</div>'}</div><div class="phScan"></div><div class="phFlash"></div><div class="phEgg"><div class="phEggHalf phEggTop"></div><div class="phEggHalf phEggBottom"></div><div class="phCrack"></div></div></div><div class="phDust"></div><div class="phStatus">INCUBATION LOCKED</div><div class="phMeta"><div class="phRarity">◆ ${String(item.rarity||'common').toUpperCase()}</div><div class="phName">${item.name||'Creature'}</div><div class="phSerial">#${String(item.serial_no||0).padStart(6,'0')} · PWR ${item.power||0} · LCK ${item.luck||0}</div></div>`;
 r.insertBefore(scene,r.firstChild);
 const top=scene.querySelector('.phTop'),ch=scene.querySelector('.phChamber'),creature=scene.querySelector('.phCreature'),scan=scene.querySelector('.phScan'),egg=scene.querySelector('.phEgg'),et=scene.querySelector('.phEggTop'),eb=scene.querySelector('.phEggBottom'),cr=scene.querySelector('.phCrack'),fl=scene.querySelector('.phFlash'),status=scene.querySelector('.phStatus'),meta=scene.querySelector('.phMeta'),dust=scene.querySelector('.phDust');
 hatchSound();haptics();addDust(dust);
 top.animate([{opacity:0,transform:'translateY(-7px)'},{opacity:1,transform:'translateY(0)'}],{duration:420,fill:'forwards'});
 ch.animate([{transform:'translate(-50%,-50%) scale(.96)'},{transform:'translate(-50%,-50%) scale(1)'}],{duration:700,easing:'ease-out',fill:'forwards'});
 scan.animate([{opacity:0,transform:'translateY(0)'},{opacity:.9,transform:'translateY(0)'},{opacity:.8,transform:'translateY(330px)'},{opacity:0,transform:'translateY(360px)'}],{duration:950,easing:'ease-in-out',fill:'forwards'});
 setTimeout(()=>{status.textContent='SHELL FRACTURE';cr.style.opacity='1';cr.animate([{transform:'translateX(-50%) rotate(8deg) scaleY(.05)'},{transform:'translateX(-50%) rotate(8deg) scaleY(1)'}],{duration:520,easing:'ease-out',fill:'forwards'});egg.animate([{transform:'translate(-50%,-50%) rotate(0)'},{transform:'translate(-50%,-50%) rotate(-2deg)'},{transform:'translate(-50%,-50%) rotate(3deg)'},{transform:'translate(-50%,-50%) rotate(-3deg)'},{transform:'translate(-50%,-50%) rotate(1deg)'}],{duration:620,easing:'ease-in-out',fill:'forwards'})},620);
 setTimeout(()=>{status.textContent='SPECIMEN AWAKENING';fl.animate([{opacity:0,transform:'translate(-50%,-50%) scale(.1)'},{opacity:1,transform:'translate(-50%,-50%) scale(1)'},{opacity:0,transform:'translate(-50%,-50%) scale(7)'}],{duration:720,easing:'ease-out',fill:'forwards'});et.animate([{transform:'translate(0,0) rotate(0)',opacity:1},{transform:'translate(-105px,-130px) rotate(-42deg) scale(.82)',opacity:0}],{duration:760,easing:'cubic-bezier(.16,.8,.2,1)',fill:'forwards'});eb.animate([{transform:'translate(0,0) rotate(0)',opacity:1},{transform:'translate(115px,135px) rotate(39deg) scale(.84)',opacity:0}],{duration:760,easing:'cubic-bezier(.16,.8,.2,1)',fill:'forwards'});creature.animate([{opacity:.13,filter:'brightness(.35) saturate(.55) blur(3px)',transform:'scale(.9)'},{opacity:1,filter:'brightness(1.08) saturate(1.15) blur(0)',transform:'scale(1.03)'},{opacity:1,filter:'brightness(1) saturate(1.05) blur(0)',transform:'scale(1)'}],{duration:1050,easing:'cubic-bezier(.12,.9,.18,1.05)',fill:'forwards'})},1180);
 setTimeout(()=>{status.textContent='SPECIMEN CONFIRMED';status.animate([{opacity:.8},{opacity:0}],{duration:520,fill:'forwards'});meta.animate([{opacity:0,transform:'translateY(18px)'},{opacity:1,transform:'translateY(-4px)'},{opacity:1,transform:'translateY(0)'}],{duration:620,easing:'cubic-bezier(.2,.8,.2,1)',fill:'forwards'});if(box)box.animate([{opacity:0,transform:'translateY(24px)'},{opacity:1,transform:'translateY(0)'}],{duration:520,easing:'ease-out',fill:'forwards'})},2250);
 setTimeout(()=>{r.dataset.hatching='0'},3000);
}
document.addEventListener('pointerdown',unlockAudio,{capture:true,passive:true});document.addEventListener('touchstart',unlockAudio,{capture:true,passive:true});window.showReveal=showRevealV5;
})();