window.DROP1_ART = {};
window.DROP1_MODELS = window.DROP1_MODELS || {};

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
    .d3modal.open{display:flex;flex-direction:column}
    .d3top{display:flex;justify-content:space-between;align-items:center;gap:12px}.d3top .d3title{font-size:20px;font-weight:950;letter-spacing:.04em}.d3close{border:1px solid #385273;background:#0c1624;color:#dcecff;border-radius:999px;padding:9px 13px;font-weight:800}
    .d3stage{flex:1;min-height:360px;margin:14px 0;border:1px solid #284466;border-radius:25px;overflow:hidden;background:radial-gradient(circle at 50% 48%,#163052,#070b12 65%);position:relative;box-shadow:inset 0 0 55px #0008,0 22px 55px #0008}
    .d3stage model-viewer{width:100%;height:100%;min-height:430px;background:transparent;--poster-color:transparent}
    .d3badge{position:absolute;left:14px;top:14px;border:1px solid #4f9fe0;background:#091321d9;border-radius:999px;padding:7px 10px;font-size:10px;font-weight:950;letter-spacing:.13em;text-transform:uppercase;z-index:2}
    .d3hint{position:absolute;left:50%;bottom:12px;transform:translateX(-50%);font-size:10px;color:#a9b9cc;background:#07101bd9;border:1px solid #263c58;padding:7px 11px;border-radius:999px;white-space:nowrap;z-index:2}
    .d3meta{display:grid;grid-template-columns:1fr auto;align-items:end;gap:12px}.d3meta b{font-size:24px}.d3meta span{display:block;color:#95a6bc;font-size:11px;margin-top:4px}.d3actions{display:grid;grid-template-columns:1fr 1fr;gap:9px;margin-top:12px}.d3actions button{border-radius:16px;padding:14px 12px;font-weight:900;border:1px solid #365173;background:#101a29;color:#eef8ff}.d3actions .primary{background:linear-gradient(180deg,#f8fdff,#d9edff);color:#07111e;border-color:#63dcff}
  `;
  document.head.appendChild(style);

  const mv = document.createElement('script');
  mv.type = 'module';
  mv.src = 'https://unpkg.com/@google/model-viewer/dist/model-viewer.min.js';
  document.head.appendChild(mv);

  function renameUI() {
    const h1 = document.querySelector('.hero h1');
    if (h1 && h1.textContent !== 'What will hatch?') h1.textContent = 'What will hatch?';
    const sub = document.querySelector('.hero .subtitle');
    if (sub) sub.textContent = 'Every egg hatches one guaranteed digital creature.';
    const btn = document.getElementById('openBtn');
    if (btn) {
      if (btn.textContent.startsWith('OPEN TEST DROP')) btn.textContent = btn.textContent.replace('OPEN TEST DROP','HATCH TEST EGG');
      else if (btn.textContent.startsWith('OPEN DROP')) btn.textContent = btn.textContent.replace('OPEN DROP','HATCH EGG');
    }
    const hint = document.querySelector('.hint');
    if (hint) hint.textContent = 'Tap a creature to inspect it, rotate available 3D specimens, or list it for trade.';
    const empty = document.querySelector('.empty');
    if (empty) empty.textContent = 'Your first creature is still inside an egg.';
  }

  document.addEventListener('DOMContentLoaded', () => {
    renameUI();
    const observer = new MutationObserver(renameUI);
    observer.observe(document.body,{subtree:true,childList:true,characterData:true});

    const modal = document.createElement('div');
    modal.className = 'd3modal';
    modal.id = 'd3modal';
    modal.innerHTML = `<div class="d3top"><div><div class="d3title" id="d3name">CREATURE</div></div><button class="d3close" id="d3close">CLOSE</button></div><div class="d3stage"><div class="d3badge" id="d3rarity">RARE</div><model-viewer id="d3viewer" camera-controls touch-action="pan-y" auto-rotate auto-rotate-delay="1200" rotation-per-second="14deg" shadow-intensity="1" environment-image="neutral" interaction-prompt="none"></model-viewer><div class="d3hint">DRAG TO ROTATE · PINCH TO ZOOM</div></div><div class="d3meta"><div><b id="d3serial">#000000</b><span id="d3stats">PRIMAL HATCH</span></div></div><div class="d3actions"><button id="d3trade">TRADE</button><button class="primary" id="d3physical">PHYSICAL FIGURE · SOON</button></div>`;
    document.body.appendChild(modal);

    document.getElementById('d3close').onclick = () => modal.classList.remove('open');
    modal.addEventListener('click',e=>{if(e.target===modal)modal.classList.remove('open')});

    const originalOpenDetail = window.openDetail;
    window.openDetail = function(id){
      try {
        const item = window.state?.collection?.find?.(x=>x.item_id===id) || (typeof state!=='undefined' ? state.collection.find(x=>x.item_id===id) : null);
        const model = item && window.DROP1_MODELS[item.id];
        if (!item || !model) return originalOpenDetail ? originalOpenDetail(id) : undefined;
        document.getElementById('d3name').textContent = item.name;
        document.getElementById('d3rarity').textContent = item.rarity.toUpperCase();
        document.getElementById('d3serial').textContent = `#${String(item.serial_no).padStart(6,'0')}`;
        document.getElementById('d3stats').textContent = `${item.set || 'PRIMAL HATCH'} · PWR ${item.power} · LCK ${item.luck}`;
        const viewer = document.getElementById('d3viewer');
        viewer.src = model;
        viewer.setAttribute('alt',item.name);
        if (viewer.availableAnimations?.length) viewer.animationName = viewer.availableAnimations[0];
        viewer.autoplay = true;
        document.getElementById('d3trade').onclick = async()=>{
          try{await api('/api/market/listings',{method:'POST',body:JSON.stringify({item_id:item.item_id,mode:'trade',want_rarity:'',note:''})});toast('Creature listed for trade');setTimeout(()=>location.href='/static/market.html',650)}catch(e){toast(e.message||'Could not list creature')}
        };
        document.getElementById('d3physical').onclick = ()=>toast('Physical figure preview will be enabled after print validation');
        modal.classList.add('open');
      } catch(e) { if(originalOpenDetail) return originalOpenDetail(id); }
    };
  });
})();
