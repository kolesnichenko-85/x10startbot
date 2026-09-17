(function(){
const css=`
.reveal.primalV2{overflow:hidden;position:fixed;--h1:#e8fbff;--h2:#7b5cff}
.reveal.primalV2.hatch-common{--h1:#e8fbff;--h2:#7da4c5}.reveal.primalV2.hatch-rare{--h1:#5be7ff;--h2:#2f7cff}.reveal.primalV2.hatch-epic{--h1:#df69ff;--h2:#7049ff}.reveal.primalV2.hatch-legendary{--h1:#ffe46a;--h2:#ff9124}.reveal.primalV2.hatch-mythic{--h1:#80ffff;--h2:#ff63e6}
.reveal.primalV2.hatchFx:before,.reveal.primalV2.hatchFx:after{display:none!important}.reveal.primalV2.hatchFx .revealBox{animation:none!important}
.reveal.primalV2 .revealBox{opacity:0!important;transform:translateY(28px) scale(.86)!important;animation:v2CreatureIn .9s 1.5s cubic-bezier(.15,.9,.2,1.12) forwards!important;position:relative;z-index:4}
.v2HatchLayer{position:absolute;inset:0;z-index:20;display:grid;place-items:center;pointer-events:none}.v2EggRig{position:relative;width:190px;height:240px;animation:v2Shake 1s cubic-bezier(.36,.07,.19,.97) both}.v2EggHalf{position:absolute;inset:0;border:2px solid var(--h1);background:radial-gradient(circle at 34% 22%,#fff 0,var(--h1) 14%,#5369d8 43%,#2a194f 73%,#090d18 100%);box-shadow:0 0 30px var(--h1),0 0 96px var(--h2)}
.v2EggTop{clip-path:polygon(0 0,100% 0,100% 52%,86% 49%,74% 58%,61% 49%,47% 59%,31% 48%,15% 56%,0 51%);border-radius:52% 48% 0 0/64% 64% 0 0;animation:v2TopBreak .8s .9s cubic-bezier(.2,.8,.2,1) forwards}.v2EggBottom{clip-path:polygon(0 50%,15% 55%,31% 47%,47% 58%,61% 48%,74% 57%,86% 48%,100% 51%,100% 100%,0 100%);border-radius:0 0 46% 54%/0 0 39% 39%;animation:v2BottomBreak .8s .9s cubic-bezier(.2,.8,.2,1) forwards}
.v2Crack{position:absolute;left:50%;top:39%;width:9px;height:98px;transform:translateX(-50%) rotate(11deg);background:#fff;filter:drop-shadow(0 0 9px var(--h1));clip-path:polygon(42% 0,100% 0,60% 28%,100% 28%,28% 58%,74% 58%,0 100%,28% 67%,0 67%,58% 36%,20% 36%);opacity:0;animation:v2Crack .75s .28s ease-out forwards}.v2Glow{position:absolute;width:30px;height:30px;border-radius:50%;background:#fff;box-shadow:0 0 34px 22px var(--h1),0 0 120px 72px var(--h2);opacity:0;animation:v2Flash 1.75s ease-out forwards}.v2Label{position:absolute;bottom:18%;font-size:11px;font-weight:950;letter-spacing:.24em;color:#e8fdff;text-shadow:0 0 12px var(--h1);animation:v2Label 1.7s ease forwards}
@keyframes v2Shake{0%{transform:scale(.82) rotate(0)}14%{transform:scale(.9) rotate(-4deg) translateX(-5px)}28%{transform:scale(.94) rotate(5deg) translateX(6px)}42%{transform:scale(.97) rotate(-6deg) translateX(-7px)}56%{transform:scale(1) rotate(5deg) translateX(7px)}70%{transform:scale(1.02) rotate(-4deg) translateX(-5px)}84%{transform:scale(1.04) rotate(3deg) translateX(4px)}100%{transform:scale(1.05) rotate(0)}}
@keyframes v2Crack{0%{opacity:0;transform:translateX(-50%) scaleY(.05) rotate(11deg)}45%{opacity:1}100%{opacity:1;transform:translateX(-50%) scaleY(1) rotate(11deg)}}
@keyframes v2TopBreak{0%{transform:translate(0,0) rotate(0);opacity:1}100%{transform:translate(-95px,-125px) rotate(-42deg) scale(.82);opacity:0}}
@keyframes v2BottomBreak{0%{transform:translate(0,0) rotate(0);opacity:1}100%{transform:translate(105px,120px) rotate(38deg) scale(.84);opacity:0}}
@keyframes v2Flash{0%,52%{opacity:0;transform:scale(.1)}66%{opacity:1;transform:scale(1)}100%{opacity:0;transform:scale(7)}}
@keyframes v2CreatureIn{0%{opacity:0;transform:translateY(28px) scale(.86)}72%{opacity:1;transform:translateY(-7px) scale(1.05)}100%{opacity:1;transform:translateY(0) scale(1)}}
@keyframes v2Label{0%,72%{opacity:.9}100%{opacity:0}}
`;
const st=document.createElement('style');st.textContent=css;document.head.appendChild(st);
let ctx=null;
function unlock(){try{const AC=window.AudioContext||window.webkitAudioContext;if(!AC)return;if(!ctx)ctx=new AC();if(ctx.state==='suspended')ctx.resume();const o=ctx.createOscillator(),g=ctx.createGain();g.gain.value=.00001;o.connect(g);g.connect(ctx.destination);o.start();o.stop(ctx.currentTime+.02)}catch(e){}}
function burst(t,d=.08,v=.34){if(!ctx)return;const sr=ctx.sampleRate,b=ctx.createBuffer(1,Math.max(1,Math.floor(sr*d)),sr),x=b.getChannelData(0);for(let i=0;i<x.length;i++)x[i]=(Math.random()*2-1)*(1-i/x.length);const s=ctx.createBufferSource(),f=ctx.createBiquadFilter(),g=ctx.createGain();s.buffer=b;f.type='highpass';f.frequency.value=900;g.gain.setValueAtTime(v,t);g.gain.exponentialRampToValueAtTime(.001,t+d);s.connect(f);f.connect(g);g.connect(ctx.destination);s.start(t)}
function sound(){try{if(!ctx||ctx.state!=='running')return;const n=ctx.currentTime+.02;const o=ctx.createOscillator(),g=ctx.createGain();o.type='sine';o.frequency.setValueAtTime(70,n);o.frequency.exponentialRampToValueAtTime(160,n+.9);g.gain.setValueAtTime(.01,n);g.gain.exponentialRampToValueAtTime(.12,n+.18);g.gain.exponentialRampToValueAtTime(.001,n+1.25);o.connect(g);g.connect(ctx.destination);o.start(n);o.stop(n+1.3);burst(n+.28,.05,.22);burst(n+.54,.07,.34);burst(n+.82,.12,.52);const p=ctx.createOscillator(),pg=ctx.createGain();p.type='triangle';p.frequency.setValueAtTime(390,n+.82);p.frequency.exponentialRampToValueAtTime(1050,n+1.18);pg.gain.setValueAtTime(.001,n+.8);pg.gain.exponentialRampToValueAtTime(.1,n+.88);pg.gain.exponentialRampToValueAtTime(.001,n+1.25);p.connect(pg);pg.connect(ctx.destination);p.start(n+.8);p.stop(n+1.27)}catch(e){}}
function rarity(item){return String(item?.rarity||'common').toLowerCase()}
function fallback(item){return `<div style="font-size:92px;display:grid;place-items:center;height:100%">${item.emoji||'🦖'}</div>`}
function revealV2(item){
 if(!item)return;const r=document.getElementById('reveal');if(!r)return;
 r.dataset.hatching='1';r.querySelector('.v2HatchLayer')?.remove();
 const rr=document.getElementById('revealRarity'),ra=document.getElementById('revealArt'),rn=document.getElementById('revealName'),rs=document.getElementById('revealSerial');
 if(rr)rr.textContent=`${String(item.rarity||'common').toUpperCase()} HATCH`;
 if(ra){const a=window.DROP1_ART?.[item.id||item.character_id];ra.innerHTML=a?`<img src="${a}" alt="${item.name||'Creature'}">`:(typeof window.artHtml==='function'?window.artHtml(item):fallback(item))}
 if(rn)rn.textContent=item.name||'Creature';if(rs)rs.textContent=`#${String(item.serial_no||0).padStart(6,'0')} · PWR ${item.power||0} · LCK ${item.luck||0}`;
 r.classList.remove('primalV2','hatch-common','hatch-rare','hatch-epic','hatch-legendary','hatch-mythic');void r.offsetWidth;r.classList.add('primalV2','hatch-'+rarity(item));
 const layer=document.createElement('div');layer.className='v2HatchLayer';layer.innerHTML='<div class="v2Glow"></div><div class="v2EggRig"><div class="v2EggHalf v2EggTop"></div><div class="v2EggHalf v2EggBottom"></div><div class="v2Crack"></div></div><div class="v2Label">PRIMAL HATCH</div>';r.insertBefore(layer,r.firstChild);r.style.display='flex';sound();
 try{window.Telegram?.WebApp?.HapticFeedback?.impactOccurred?.('medium');setTimeout(()=>window.Telegram?.WebApp?.HapticFeedback?.impactOccurred?.('heavy'),760);setTimeout(()=>window.Telegram?.WebApp?.HapticFeedback?.notificationOccurred?.('success'),1450)}catch(e){}
 setTimeout(()=>{layer.remove();r.dataset.hatching='0'},2100)
}
document.addEventListener('pointerdown',unlock,{capture:true,passive:true});document.addEventListener('touchstart',unlock,{capture:true,passive:true});
window.showReveal=revealV2;
const b=document.getElementById('openBtn');if(b){b.addEventListener('pointerdown',unlock,{passive:true});b.addEventListener('touchstart',unlock,{passive:true})}
})();
