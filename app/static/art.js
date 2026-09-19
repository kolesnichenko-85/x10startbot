window.DROP1_ART={
'r002':'/static/assets/neon-raptor.png'
};
window.DROP1_SPIN={
'r002':['/static/assets/neon-raptor.png']
};
window.DROP1_PHYSICAL={};

(function(){
const css=`
.tag:after{content:' · PRIMAL HATCH';color:#63e8ff}
.capsuleScene .capsule{width:126px;height:162px;border-radius:52% 48% 46% 54%/61% 61% 39% 39%;transform:none;background:radial-gradient(circle at 38% 26%,#dffcff 0,#80edff 12%,#4767d6 42%,#281643 72%,#090d18 100%);border:2px solid #75edff;box-shadow:0 0 22px #68e4ff,0 0 64px #795cff75,inset -18px -22px 30px #100d2c88;animation:eggFloat 2.6s ease-in-out infinite;position:relative;overflow:hidden}.capsuleScene .core{display:none!important}
.capsuleScene .capsule:before,.capsuleScene .capsule:after{content:'';position:absolute;height:2px;background:#c8fbff;box-shadow:0 0 10px #76ecff;opacity:.8;transform-origin:left center}.capsuleScene .capsule:before{width:52px;left:18px;top:74px;transform:rotate(17deg)}.capsuleScene .capsule:after{width:44px;right:9px;top:88px;transform:rotate(-22deg)}
@keyframes eggFloat{0%,100%{transform:translateY(0) rotate(-2deg)}50%{transform:translateY(-8px) rotate(2deg)}}

.reveal.hatchFx{overflow:hidden;--h1:#72e9ff;--h2:#7b5cff}
.reveal.hatch-common{--h1:#e8fbff;--h2:#8bb8d8}.reveal.hatch-rare{--h1:#5be7ff;--h2:#2c7dff}.reveal.hatch-epic{--h1:#e06dff;--h2:#7a47ff}.reveal.hatch-legendary{--h1:#ffe06a;--h2:#ff8b22}.reveal.hatch-mythic{--h1:#80ffff;--h2:#ff63e6}
.reveal.hatchFx:before{content:'';position:absolute;z-index:5;left:50%;top:45%;width:160px;height:204px;border-radius:52% 48% 46% 54%/61% 61% 39% 39%;background:
linear-gradient(72deg,transparent 44%,#efffff 45%,#efffff 47%,transparent 48%) 48% 47%/62px 88px no-repeat,
linear-gradient(112deg,transparent 46%,#efffff 47%,#efffff 49%,transparent 50%) 58% 61%/72px 98px no-repeat,
radial-gradient(circle at 35% 23%,#fff 0,var(--h1) 14%,#5368d8 42%,#2c1b58 72%,#090d18 100%);border:2px solid var(--h1);box-shadow:0 0 30px var(--h1),0 0 105px var(--h2);transform:translate(-50%,-50%);animation:eggBreak 1.45s cubic-bezier(.2,.8,.18,1) forwards}
.reveal.hatchFx:after{content:'';position:absolute;z-index:4;left:50%;top:45%;width:30px;height:30px;border-radius:50%;background:#fff;box-shadow:0 0 28px 18px var(--h1),0 0 95px 55px var(--h2);transform:translate(-50%,-50%) scale(.1);animation:hatchFlash 1.35s ease-out forwards}
.reveal.hatchFx .revealBox{opacity:0;transform:translateY(30px) scale(.82);animation:creaturePop .95s .92s cubic-bezier(.12,.92,.18,1.15) forwards}
.reveal.hatchFx .revealCard{box-shadow:0 0 58px color-mix(in srgb,var(--h1) 60%,transparent),0 28px 80px #000;animation:cardPulse 2.2s 1.85s ease-in-out infinite}
@keyframes eggBreak{0%{transform:translate(-50%,-50%) scale(.72) rotate(0);filter:brightness(1)}22%{transform:translate(-50%,-50%) scale(.92) rotate(-3deg)}35%{transform:translate(-50%,-50%) scale(.96) rotate(4deg)}48%{transform:translate(-50%,-50%) scale(1.01) rotate(-5deg);filter:brightness(1.25)}61%{transform:translate(-50%,-50%) scale(1.04) rotate(3deg);opacity:1}100%{transform:translate(-50%,-50%) scale(1.8);opacity:0;filter:blur(12px) brightness(1.8)}}
@keyframes hatchFlash{0%,53%{opacity:0;transform:translate(-50%,-50%) scale(.1)}65%{opacity:1;transform:translate(-50%,-50%) scale(1)}100%{opacity:0;transform:translate(-50%,-50%) scale(6)}}
@keyframes creaturePop{0%{opacity:0;transform:translateY(30px) scale(.82) rotateY(22deg)}70%{opacity:1;transform:translateY(-7px) scale(1.05) rotateY(-3deg)}100%{opacity:1;transform:translateY(0) scale(1) rotateY(0)}}
@keyframes cardPulse{0%,100%{filter:brightness(1);transform:translateY(0)}50%{filter:brightness(1.14);transform:translateY(-3px)}}

.d3modal{position:fixed;inset:0;z-index:95;display:none;flex-direction:column;background:radial-gradient(circle at 50% 28%,#16345b 0,#080d17 48%,#020407 100%);padding:calc(18px + env(safe-area-inset-top)) 14px calc(18px + env(safe-area-inset-bottom));color:#fff}.d3modal.open{display:flex}.d3top{display:flex;align-items:center;justify-content:space-between;gap:12px}.d3title{font-size:21px;font-weight:950}.d3close{border:1px solid #36506f;background:#0c1624;color:#e8f5ff;border-radius:999px;padding:9px 13px;font-weight:850}.d3stage{flex:1;min-height:390px;margin:14px 0;border:1px solid #315277;border-radius:26px;overflow:hidden;position:relative;background:radial-gradient(circle at 50% 45%,#183b65,#070b12 68%);touch-action:none;user-select:none}.spinFrame{width:100%;height:100%;min-height:430px;object-fit:contain;display:block;pointer-events:none;filter:drop-shadow(0 24px 30px #000b);animation:idleFloat 3.1s ease-in-out infinite}.d3badge{position:absolute;z-index:2;left:14px;top:14px;border:1px solid #51b9ee;background:#081321e8;border-radius:999px;padding:7px 10px;font-size:10px;font-weight:950;letter-spacing:.13em}.d3hint{position:absolute;z-index:2;left:50%;bottom:12px;transform:translateX(-50%);border:1px solid #2a405d;background:#07101be8;border-radius:999px;padding:7px 11px;font-size:10px;color:#b8c7d8;white-space:nowrap}.d3meta b{font-size:25px}.d3meta span{display:block;margin-top:4px;color:#91a3b8;font-size:11px}.d3actions{display:grid;grid-template-columns:1fr 1fr;gap:9px;margin-top:12px}.d3actions button{border-radius:16px;padding:14px 10px;font-weight:950;border:1px solid #365173;background:#101a29;color:#eef8ff}.d3actions .primary{background:linear-gradient(180deg,#f9fdff,#daedff);color:#07111e;border-color:#63dcff}
@keyframes idleFloat{0%,100%{transform:translateY(0) scale(1)}50%{transform:translateY(-5px) scale(1.012)}}`;
const st=document.createElement('style');st.textContent=css;document.head.appendChild(st);

let audioCtx=null;
function unlockAudio(){
 try{const AC=window.AudioContext||window.webkitAudioContext;if(!AC)return;if(!audioCtx)audioCtx=new AC();if(audioCtx.state==='suspended')audioCtx.resume()}catch(e){}
}
function crackBurst(t,dur=.08,level=.22){
 if(!audioCtx)return;const sr=audioCtx.sampleRate,b=audioCtx.createBuffer(1,Math.max(1,Math.floor(sr*dur)),sr),d=b.getChannelData(0);for(let i=0;i<d.length;i++)d[i]=(Math.random()*2-1)*(1-i/d.length);const s=audioCtx.createBufferSource(),f=audioCtx.createBiquadFilter(),g=audioCtx.createGain();s.buffer=b;f.type='highpass';f.frequency.value=850;g.gain.setValueAtTime(level,t);g.gain.exponentialRampToValueAtTime(.001,t+dur);s.connect(f);f.connect(g);g.connect(audioCtx.destination);s.start(t);s.stop(t+dur+.02)
}
function playHatchSound(){
 try{unlockAudio();if(!audioCtx||audioCtx.state!=='running')return;const n=audioCtx.currentTime+.02;const hum=audioCtx.createOscillator(),hg=audioCtx.createGain();hum.type='sine';hum.frequency.setValueAtTime(85,n);hum.frequency.exponentialRampToValueAtTime(190,n+.7);hg.gain.setValueAtTime(.001,n);hg.gain.exponentialRampToValueAtTime(.09,n+.12);hg.gain.exponentialRampToValueAtTime(.001,n+.82);hum.connect(hg);hg.connect(audioCtx.destination);hum.start(n);hum.stop(n+.85);crackBurst(n+.22,.07,.25);crackBurst(n+.39,.06,.3);crackBurst(n+.56,.09,.38);const ch=audioCtx.createOscillator(),cg=audioCtx.createGain();ch.type='triangle';ch.frequency.setValueAtTime(560,n+.58);ch.frequency.exponentialRampToValueAtTime(980,n+.9);cg.gain.setValueAtTime(.001,n+.58);cg.gain.exponentialRampToValueAtTime(.08,n+.64);cg.gain.exponentialRampToValueAtTime(.001,n+1.02);ch.connect(cg);cg.connect(audioCtx.destination);ch.start(n+.58);ch.stop(n+1.05)}catch(e){}
}
function setText(el,text){if(el&&el.textContent!==text)el.textContent=text}
function renameUI(){
 const main=document.getElementById('openBtn');
 if(main){
  setText(document.querySelector('.hero h1'),'What will hatch?');
  setText(document.querySelector('.hero .subtitle'),'Every egg hatches one guaranteed digital creature.');
  const t=main.textContent||'';
  if(t.startsWith('OPEN TEST DROP'))main.textContent=t.replace('OPEN TEST DROP','HATCH TEST EGG');
  else if(t.startsWith('OPEN DROP'))main.textContent=t.replace('OPEN DROP','HATCH EGG');
  setText(document.querySelector('.hint'),'Tap a creature to inspect it, rotate available specimens, or list it for trade.');
  return;
 }
 if(location.pathname.includes('market.html')){
  setText(document.querySelector('.hero p'),'Owners choose what they want in return. DROP1 provides ownership and trade rails; it does not set creature prices or guarantee value.');
  setText(document.getElementById('openList'),'＋ LIST A CREATURE');
  setText(document.querySelector('.legal'),'Creature-for-creature trading only in this beta. Paid resale is not enabled yet.');
 }
}

function runHatchFx(revealEl){
 if(window.showReveal&&window.showReveal.name==='showRevealV5')return;
 if(!revealEl||revealEl.style.display!=='flex'||revealEl.dataset.hatching==='1')return;
 revealEl.dataset.hatching='1';
 const rt=(document.getElementById('revealRarity')?.textContent||'common').toLowerCase();
 const rarity=['mythic','legendary','epic','rare','common'].find(r=>rt.includes(r))||'common';
 revealEl.classList.remove('hatchFx','hatch-common','hatch-rare','hatch-epic','hatch-legendary','hatch-mythic');
 void revealEl.offsetWidth;
 revealEl.classList.add('hatchFx','hatch-'+rarity);
 playHatchSound();
 try{window.Telegram?.WebApp?.HapticFeedback?.impactOccurred?.('medium');setTimeout(()=>window.Telegram?.WebApp?.HapticFeedback?.impactOccurred?.('heavy'),520);setTimeout(()=>window.Telegram?.WebApp?.HapticFeedback?.notificationOccurred?.('success'),930)}catch(e){}
 setTimeout(()=>{revealEl.classList.remove('hatchFx');revealEl.dataset.hatching='0'},2300);
}

document.addEventListener('pointerdown',unlockAudio,{passive:true});
document.addEventListener('touchstart',unlockAudio,{passive:true});

document.addEventListener('DOMContentLoaded',()=>{
 renameUI();setTimeout(renameUI,350);setTimeout(renameUI,1200);setTimeout(renameUI,2500);
 if(!document.getElementById('openBtn'))return;
 const revealEl=document.getElementById('reveal');
 if(revealEl){
  const ro=new MutationObserver(()=>{if(revealEl.style.display==='flex')runHatchFx(revealEl);else revealEl.dataset.hatching='0'});
  ro.observe(revealEl,{attributes:true,attributeFilter:['style']});
 }
 const modal=document.createElement('div');modal.className='d3modal';modal.innerHTML=`<div class="d3top"><div class="d3title" id="d3name">CREATURE</div><button class="d3close" id="d3close">CLOSE</button></div><div class="d3stage" id="d3stage"><div class="d3badge" id="d3rarity">RARE</div><img class="spinFrame" id="d3spin" alt="Creature"><div class="d3hint" id="d3hint">DRAG LEFT / RIGHT TO ROTATE</div></div><div class="d3meta"><b id="d3serial">#000000</b><span id="d3stats">PRIMAL HATCH</span></div><div class="d3actions"><button id="d3trade">TRADE</button><button class="primary" id="d3physical">PHYSICAL PREVIEW</button></div>`;document.body.appendChild(modal);
 const q=id=>document.getElementById(id),spin=q('d3spin'),stage=q('d3stage'),close=q('d3close'),physical=q('d3physical');
 let frames=[],frame=0,lastX=0,drag=false,timer=null,item=null,physicalMode=false;
 function draw(){if(frames.length)spin.src=frames[(frame%frames.length+frames.length)%frames.length]}
 function restart(){clearInterval(timer);timer=setInterval(()=>{if(!drag&&!physicalMode&&frames.length){frame=(frame+1)%frames.length;draw()}},1500)}
 function digital(){physicalMode=false;frames=(item&&window.DROP1_SPIN[item.id])||[];frame=0;if(frames.length){draw();frames.forEach(u=>{const i=new Image();i.src=u});restart()}physical.textContent=window.DROP1_PHYSICAL[item?.id]?'PHYSICAL PREVIEW':'PHYSICAL FIGURE · SOON';q('d3hint').textContent='DRAG LEFT / RIGHT TO ROTATE'}
 close.onclick=()=>{clearInterval(timer);modal.classList.remove('open')};
 stage.addEventListener('pointerdown',e=>{if(!frames.length||physicalMode)return;drag=true;lastX=e.clientX;clearInterval(timer);stage.setPointerCapture?.(e.pointerId)});
 stage.addEventListener('pointermove',e=>{if(!drag||physicalMode||!frames.length)return;const dx=e.clientX-lastX;if(Math.abs(dx)>=18){frame+=(dx<0?1:-1);lastX=e.clientX;draw()}});
 stage.addEventListener('pointerup',()=>{drag=false;restart()});stage.addEventListener('pointercancel',()=>{drag=false;restart()});
 const original=window.openDetail;
 window.openDetail=function(id){
  try{
   const found=(typeof state!=='undefined'&&state?.collection)?state.collection.find(x=>x.item_id===id):null;
   if(!found||!window.DROP1_SPIN[found.id])return original?original(id):undefined;
   item=found;setText(q('d3name'),item.name);setText(q('d3rarity'),String(item.rarity||'').toUpperCase());setText(q('d3serial'),`#${String(item.serial_no||0).padStart(6,'0')}`);setText(q('d3stats'),`PRIMAL HATCH · PWR ${item.power} · LCK ${item.luck}`);digital();
   q('d3trade').onclick=async()=>{try{await api('/api/market/listings',{method:'POST',body:JSON.stringify({item_id:item.item_id,mode:'trade',want_rarity:'',note:''})});toast('Creature listed for trade');setTimeout(()=>location.href='/static/market.html',650)}catch(e){toast(e.message||'Could not list creature')}};
   physical.onclick=()=>{const p=window.DROP1_PHYSICAL[item.id];if(!p)return toast('Physical figure preview will unlock after print validation');if(!physicalMode){physicalMode=true;clearInterval(timer);frames=[];spin.src=p;q('d3hint').textContent='PHYSICAL FIGURE CONCEPT · PROTOTYPE';physical.textContent='BACK TO DIGITAL'}else digital()};
   modal.classList.add('open');
  }catch(e){console.error('DROP1 viewer error',e);if(original)return original(id)}
 };
});
})();
