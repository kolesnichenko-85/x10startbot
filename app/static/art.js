window.DROP1_ART = {
  'r002':'https://dnznrvs05pmza.cloudfront.net/gemini/gemini-3-pro-image/images/c9c69c6d-059d-44ff-91f1-1dcfdc30f03b/fc9ace10-2f2a-44c5-aaf0-34de567c76ea/Single_standalone_full_body_3D_game_character_concept_for_DR.png?_jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJrZXlIYXNoIjoiZGM1ZGNkZDJjNzM4OTJhZSIsImJ1Y2tldCI6InJ1bndheS10YXNrLWFydGlmYWN0cyIsInN0YWdlIjoicHJvZCIsImV4cCI6MTc4OTc2ODY1OH0.k4vT8ehvXPCbHMsgDuFmAcw3cLJKw8e1gEgL4241tEQ'
};
window.DROP1_MODELS = window.DROP1_MODELS || {};
window.DROP1_SPIN = {
  'r002':[
    'https://dnznrvs05pmza.cloudfront.net/gemini/gemini-3-pro-image/images/c9c69c6d-059d-44ff-91f1-1dcfdc30f03b/fc9ace10-2f2a-44c5-aaf0-34de567c76ea/Single_standalone_full_body_3D_game_character_concept_for_DR.png?_jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJrZXlIYXNoIjoiZGM1ZGNkZDJjNzM4OTJhZSIsImJ1Y2tldCI6InJ1bndheS10YXNrLWFydGlmYWN0cyIsInN0YWdlIjoicHJvZCIsImV4cCI6MTc4OTc2ODY1OH0.k4vT8ehvXPCbHMsgDuFmAcw3cLJKw8e1gEgL4241tEQ',
    'https://dnznrvs05pmza.cloudfront.net/gemini/gemini-3-pro-image/images/ca12dd2d-9436-4bc3-9114-57846d917ccf/63668fd8-810d-4422-985a-82684bac8eee/Use__raptor_as_the_strict_character_identity_reference__Crea.png?_jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJrZXlIYXNoIjoiNDU1NGYwZGUzYWE1NzFiMiIsImJ1Y2tldCI6InJ1bndheS10YXNrLWFydGlmYWN0cyIsInN0YWdlIjoicHJvZCIsImV4cCI6MTc4OTc2NzM5MH0.0DlXV_6T12O-HJRagkg6IvOdQSFf41y2QcyxNBZbnbE',
    'https://dnznrvs05pmza.cloudfront.net/gemini/gemini-3-pro-image/images/6012d94a-7eae-46ba-926f-033562e5cceb/9c9a0699-09cc-4b66-a0cb-3f2fbebe87e8/Use__raptor_as_the_strict_character_identity_reference__Crea.png?_jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJrZXlIYXNoIjoiZDY2OGZhYjliZmM3ZmZjOCIsImJ1Y2tldCI6InJ1bndheS10YXNrLWFydGlmYWN0cyIsInN0YWdlIjoicHJvZCIsImV4cCI6MTc4OTgwMjU1M30.LsclCbBInonCVxaBJeloslFAGKO0G82tl1YPEkKiJcI',
    'https://dnznrvs05pmza.cloudfront.net/gemini/gemini-3-pro-image/images/699fc3e0-5173-4520-b8f2-1ee88cc1f8c3/c3701739-135a-4285-aa80-eaa1dfe15a0f/Use__raptor_as_the_strict_character_identity_reference__Crea.png?_jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJrZXlIYXNoIjoiN2UyN2MyN2EwMzc0ZDdlZSIsImJ1Y2tldCI6InJ1bndheS10YXNrLWFydGlmYWN0cyIsInN0YWdlIjoicHJvZCIsImV4cCI6MTc4OTc3MDEwNn0.AzxkPabyNIXp-KfOg7xdJewYu7eqCoNJZ34mjKVIfYU'
  ]
};

(function () {
  const style = document.createElement('style');
  style.textContent = `
    .tag:after{content:' · PRIMAL HATCH';color:#63e8ff}
    .capsuleScene .capsule{width:126px;height:162px;border-radius:52% 48% 46% 54% / 61% 61% 39% 39%;transform:none;background:radial-gradient(circle at 38% 26%,#dffcff 0,#80edff 12%,#4767d6 42%,#281643 72%,#090d18 100%);border:2px solid #75edff;box-shadow:0 0 22px #68e4ff,0 0 64px #795cff75,inset -18px -22px 30px #100d2c88;animation:eggFloat 2.6s ease-in-out infinite;position:relative;overflow:hidden}
    .capsuleScene .capsule:before,.capsuleScene .capsule:after{content:'';position:absolute;height:2px;background:#b8f8ff;box-shadow:0 0 10px #76ecff;opacity:.75;transform-origin:left center}
    .capsuleScene .capsule:before{width:52px;left:18px;top:74px;transform:rotate(17deg)}
    .capsuleScene .capsule:after{width:44px;right:9px;top:88px;transform:rotate(-22deg)}
    .capsuleScene .core{display:none!important}
    @keyframes eggFloat{0%,100%{transform:translateY(0) rotate(-2deg)}45%{transform:translateY(-8px) rotate(2deg)}55%{transform:translateY(-8px) rotate(-1deg)}}
    .d3modal{position:fixed;inset:0;z-index:95;display:none;background:radial-gradient(circle at 50% 30%,#132c4d 0,#070b13 48%,#020407 100%);padding:calc(18px + env(safe-area-inset-top)) 14px calc(20px + env(safe-area-inset-bottom));color:#fff}
    .d3modal.open{display:flex;flex-direction:column}.d3top{display:flex;justify-content:space-between;align-items:center;gap:12px}.d3title{font-size:20px;font-weight:950;letter-spacing:.04em}.d3close{border:1px solid #385273;background:#0c1624;color:#dcecff;border-radius:999px;padding:9px 13px;font-weight:800}
    .d3stage{flex:1;min-height:360px;margin:14px 0;border:1px solid #284466;border-radius:25px;overflow:hidden;background:radial-gradient(circle at 50% 48%,#163052,#070b12 65%);position:relative;box-shadow:inset 0 0 55px #0008,0 22px 55px #0008;touch-action:none;user-select:none}
    .d3stage model-viewer{width:100%;height:100%;min-height:430px;background:transparent;--poster-color:transparent}.spinFrame{display:none;width:100%;height:100%;min-height:430px;object-fit:contain;pointer-events:none;filter:drop-shadow(0 22px 28px #000a);animation:creatureIdle 3.2s ease-in-out infinite}
    @keyframes creatureIdle{0%,100%{transform:translateY(0) scale(1)}50%{transform:translateY(-5px) scale(1.012)}}
    .d3badge{position:absolute;left:14px;top:14px;border:1px solid #4f9fe0;background:#091321d9;border-radius:999px;padding:7px 10px;font-size:10px;font-weight:950;letter-spacing:.13em;text-transform:uppercase;z-index:2}.d3hint{position:absolute;left:50%;bottom:12px;transform:translateX(-50%);font-size:10px;color:#a9b9cc;background:#07101bd9;border:1px solid #263c58;padding:7px 11px;border-radius:999px;white-space:nowrap;z-index:2}
    .d3meta{display:grid;grid-template-columns:1fr auto;align-items:end;gap:12px}.d3meta b{font-size:24px}.d3meta span{display:block;color:#95a6bc;font-size:11px;margin-top:4px}.d3actions{display:grid;grid-template-columns:1fr 1fr;gap:9px;margin-top:12px}.d3actions button{border-radius:16px;padding:14px 12px;font-weight:900;border:1px solid #365173;background:#101a29;color:#eef8ff}.d3actions .primary{background:linear-gradient(180deg,#f8fdff,#d9edff);color:#07111e;border-color:#63dcff}
  `;
  document.head.appendChild(style);

  const mv = document.createElement('script'); mv.type='module'; mv.src='https://unpkg.com/@google/model-viewer/dist/model-viewer.min.js'; document.head.appendChild(mv);

  function renameUI(){const h1=document.querySelector('.hero h1');if(h1&&h1.textContent!=='What will hatch?')h1.textContent='What will hatch?';const sub=document.querySelector('.hero .subtitle');if(sub)sub.textContent='Every egg hatches one guaranteed digital creature.';const btn=document.getElementById('openBtn');if(btn){if(btn.textContent.startsWith('OPEN TEST DROP'))btn.textContent=btn.textContent.replace('OPEN TEST DROP','HATCH TEST EGG');else if(btn.textContent.startsWith('OPEN DROP'))btn.textContent=btn.textContent.replace('OPEN DROP','HATCH EGG')}const hint=document.querySelector('.hint');if(hint)hint.textContent='Tap a creature to inspect it, rotate available specimens, or list it for trade.';const empty=document.querySelector('.empty');if(empty)empty.textContent='Your first creature is still inside an egg.'}

  document.addEventListener('DOMContentLoaded',()=>{
    renameUI();new MutationObserver(renameUI).observe(document.body,{subtree:true,childList:true,characterData:true});
    const modal=document.createElement('div');modal.className='d3modal';modal.id='d3modal';modal.innerHTML=`<div class="d3top"><div class="d3title" id="d3name">CREATURE</div><button class="d3close" id="d3close">CLOSE</button></div><div class="d3stage" id="d3stage"><div class="d3badge" id="d3rarity">RARE</div><model-viewer id="d3viewer" camera-controls touch-action="none" auto-rotate auto-rotate-delay="1200" rotation-per-second="14deg" shadow-intensity="1" environment-image="neutral" interaction-prompt="none"></model-viewer><img class="spinFrame" id="d3spin" alt="Rotatable creature"><div class="d3hint" id="d3hint">DRAG TO ROTATE · PINCH TO ZOOM</div></div><div class="d3meta"><div><b id="d3serial">#000000</b><span id="d3stats">PRIMAL HATCH</span></div></div><div class="d3actions"><button id="d3trade">TRADE</button><button class="primary" id="d3physical">PHYSICAL FIGURE · SOON</button></div>`;document.body.appendChild(modal);
    d3close.onclick=()=>modal.classList.remove('open');modal.addEventListener('click',e=>{if(e.target===modal)modal.classList.remove('open')});
    let frames=[],frame=0,startX=0,lastX=0,dragging=false,autoTimer=null;
    function drawFrame(){if(frames.length)d3spin.src=frames[(frame%frames.length+frames.length)%frames.length]}
    d3stage.addEventListener('pointerdown',e=>{if(!frames.length)return;dragging=true;startX=lastX=e.clientX;d3stage.setPointerCapture?.(e.pointerId);clearInterval(autoTimer)});
    d3stage.addEventListener('pointermove',e=>{if(!dragging||!frames.length)return;const dx=e.clientX-lastX;if(Math.abs(dx)>=18){frame+=(dx<0?1:-1);lastX=e.clientX;drawFrame()}});
    const stop=e=>{dragging=false};d3stage.addEventListener('pointerup',stop);d3stage.addEventListener('pointercancel',stop);

    const originalOpenDetail=window.openDetail;
    window.openDetail=function(id){try{const item=(typeof state!=='undefined'&&state?.collection)?state.collection.find(x=>x.item_id===id):null;const model=item&&window.DROP1_MODELS[item.id];const spin=item&&window.DROP1_SPIN[item.id];if(!item||(!model&&!spin))return originalOpenDetail?originalOpenDetail(id):undefined;d3name.textContent=item.name;d3rarity.textContent=item.rarity.toUpperCase();d3serial.textContent=`#${String(item.serial_no).padStart(6,'0')}`;d3stats.textContent=`${item.set||'PRIMAL HATCH'} · PWR ${item.power} · LCK ${item.luck}`;clearInterval(autoTimer);if(model){d3viewer.style.display='block';d3spin.style.display='none';d3viewer.src=model;d3viewer.setAttribute('alt',item.name);d3viewer.autoplay=true;d3hint.textContent='DRAG TO ROTATE · PINCH TO ZOOM'}else{frames=spin;frame=0;frames.forEach(src=>{const i=new Image();i.src=src});d3viewer.style.display='none';d3spin.style.display='block';drawFrame();d3hint.textContent='DRAG LEFT / RIGHT TO ROTATE';autoTimer=setInterval(()=>{if(!dragging){frame++;drawFrame()}},1500)}d3trade.onclick=async()=>{try{await api('/api/market/listings',{method:'POST',body:JSON.stringify({item_id:item.item_id,mode:'trade',want_rarity:'',note:''})});toast('Creature listed for trade');setTimeout(()=>location.href='/static/market.html',650)}catch(e){toast(e.message||'Could not list creature')}};d3physical.onclick=()=>toast('Physical figure preview will unlock after print validation');modal.classList.add('open')}catch(e){if(originalOpenDetail)return originalOpenDetail(id)}};
  });
})();
