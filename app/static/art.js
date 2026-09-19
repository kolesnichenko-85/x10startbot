window.DROP1_ART={
  'r002':'/static/assets/neon-raptor.png'
};
window.DROP1_SPIN={
  'r002':['/static/assets/neon-raptor.png']
};
window.DROP1_PHYSICAL={};

(function(){
  function init(){
  const openBtn=document.getElementById('openBtn');
  if(!openBtn) return;

  const css=`
  .specimenModal{position:fixed;inset:0;z-index:96;display:none;flex-direction:column;background:radial-gradient(circle at 50% 20%,#15345c 0,#07101a 42%,#020407 76%);color:#fff;padding:calc(14px + env(safe-area-inset-top)) 14px calc(16px + env(safe-area-inset-bottom));overflow:auto}
  .specimenModal.open{display:flex}
  .specTop{display:flex;align-items:center;justify-content:space-between;gap:12px;min-height:46px}.specTopLeft{min-width:0}.specKicker{font-size:8px;font-weight:950;letter-spacing:.22em;color:#8fa5bf}.specTitle{font-size:22px;font-weight:950;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.specClose{min-width:72px;min-height:44px;border:1px solid #35506f;background:#081321;color:#eaf6ff;border-radius:999px;padding:9px 13px;font-weight:900}
  .specStage{position:relative;margin:12px 0 12px;min-height:390px;border:1px solid #315477;border-radius:28px;overflow:hidden;background:radial-gradient(circle at 50% 40%,#173b66,#07101a 68%);box-shadow:0 30px 80px #000c,inset 0 0 60px #64cfff0a;touch-action:pan-y}
  .specStage:before{content:'';position:absolute;left:-20%;right:-20%;bottom:-13%;height:38%;opacity:.18;transform:perspective(520px) rotateX(64deg);background-image:linear-gradient(#5ae5ff22 1px,transparent 1px),linear-gradient(90deg,#5ae5ff22 1px,transparent 1px);background-size:34px 34px}
  .specArt{position:absolute;inset:0;display:grid;place-items:center;transition:transform .18s ease-out;will-change:transform}.specArt img{width:100%;height:100%;object-fit:cover;object-position:50% 20%;display:block;filter:drop-shadow(0 28px 38px #000d)}
  .specFallback{width:78%;height:72%;display:grid;place-items:center;border:1px solid #304967;border-radius:28px;background:radial-gradient(circle,#22486f,#07101a 68%);font-size:120px;filter:drop-shadow(0 22px 30px #000d)}
  .specRarity{position:absolute;z-index:3;left:14px;top:14px;border:1px solid #55ddff;background:#06101de8;border-radius:999px;padding:7px 10px;font-size:9px;font-weight:950;letter-spacing:.14em;text-transform:uppercase;box-shadow:0 0 20px #47d8ff33}.specRarity.epic{color:#eb8bff;border-color:#a653d8}.specRarity.legendary{color:#ffe072;border-color:#a97825}.specRarity.mythic{color:#a8ffff;border-color:#bc5cdc}
  .specInspect{position:absolute;z-index:3;left:50%;bottom:12px;transform:translateX(-50%);border:1px solid #2a415d;background:#06101de8;border-radius:999px;padding:7px 10px;color:#9fb0c5;font-size:9px;white-space:nowrap}
  .specBody{display:grid;gap:10px}.specIdentity{display:flex;align-items:end;justify-content:space-between;gap:12px}.specSerial{font-size:25px;font-weight:950}.specSet{font-size:9px;color:#8395ad;letter-spacing:.13em;text-align:right}
  .specStats{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}.specStat{border:1px solid #293f5b;background:#08121f;border-radius:16px;padding:11px 7px;text-align:center}.specStat b{display:block;font-size:20px}.specStat span{font-size:8px;color:#8192a9;letter-spacing:.09em}
  .specSection{border:1px solid #253a55;background:#07101bcc;border-radius:16px;padding:11px}.specSectionTitle{font-size:8px;color:#8192aa;font-weight:950;letter-spacing:.13em;margin-bottom:8px}.specimens{display:flex;gap:7px;overflow:auto;scrollbar-width:none}.specimens::-webkit-scrollbar{display:none}.specChip{white-space:nowrap;min-height:38px;border:1px solid #2c405c;background:#0b1624;color:#a9b8ca;border-radius:999px;padding:8px 10px;font-size:10px;font-weight:900}.specChip.active{background:#e8f8ff;color:#06101b;border-color:#59ddff}.specProvenance{font-size:11px;color:#a6b5c7;line-height:1.55}.specActions{display:grid;grid-template-columns:1fr 1fr;gap:8px}.specActions button{min-height:48px;border-radius:15px;padding:12px 10px;font-weight:950;border:1px solid #2d435f;background:#0e1928;color:#fff}.specActions .primary{background:linear-gradient(180deg,#f8fdff,#ddecff);color:#06101b;border-color:#5bdcff}.specActions .disabled{opacity:.45}.specActions .wide{grid-column:1/-1}
  @media(max-width:380px){.specStage{min-height:350px}.specSerial{font-size:22px}}
  `;
  const style=document.createElement('style');style.textContent=css;document.head.appendChild(style);

  const modal=document.createElement('div');
  modal.className='specimenModal';
  modal.innerHTML=`
    <div class="specTop">
      <div class="specTopLeft"><div class="specKicker">DROP1 · PRIMAL HATCH</div><div class="specTitle" id="specName">CREATURE</div></div>
      <button class="specClose" id="specClose">CLOSE</button>
    </div>
    <div class="specStage" id="specStage">
      <div class="specRarity" id="specRarity">COMMON</div>
      <div class="specArt" id="specArt"></div>
      <div class="specInspect">DRAG TO INSPECT · TRUE 3D COMING NEXT</div>
    </div>
    <div class="specBody">
      <div class="specIdentity"><div><div class="specSerial" id="specSerial">#000000</div><div style="font-size:10px;color:#8fa0b6;margin-top:2px" id="specAcquired"></div></div><div class="specSet" id="specSet"></div></div>
      <div class="specStats"><div class="specStat"><b id="specPower">0</b><span>POWER</span></div><div class="specStat"><b id="specLuck">0</b><span>LUCK</span></div><div class="specStat"><b id="specCount">1</b><span>SPECIMENS</span></div></div>
      <div class="specSection"><div class="specSectionTitle">YOUR COPIES · CHOOSE EXACT SERIAL</div><div class="specimens" id="specimens"></div></div>
      <div class="specSection"><div class="specSectionTitle">PROVENANCE</div><div class="specProvenance" id="specProvenance">Loading ownership record…</div></div>
      <div class="specActions"><button id="specShare">SHARE</button><button class="primary" id="specTrade">TRADE THIS SPECIMEN</button><button class="disabled wide" id="specPhysical" disabled>PHYSICAL FIGURE · PRODUCTION PIPELINE</button></div>
    </div>`;
  document.body.appendChild(modal);

  const q=id=>document.getElementById(id);
  const stage=q('specStage'), art=q('specArt');
  let current=null, group=[], drag=false, startX=0, tilt=0;

  function safeDate(v){try{return new Date(v).toLocaleDateString(undefined,{year:'numeric',month:'short',day:'numeric'})}catch(e){return ''}}
  function renderArt(item){
    const url=window.DROP1_ART[item.id]||'';
    art.innerHTML=url?'<img src="'+url+'" alt="'+item.name+'">':'<div class="specFallback">'+(item.emoji||'🦖')+'</div>';
  }
  async function loadProvenance(item){
    q('specProvenance').textContent='Loading ownership record…';
    try{
      const r=await fetch('/api/items/'+item.item_id+'/provenance');
      const d=await r.json();
      if(!r.ok) throw new Error('provenance unavailable');
      q('specProvenance').textContent='Minted '+safeDate(d.minted_at||item.acquired_at)+' · '+(d.trade_count||0)+' completed trade'+((d.trade_count||0)===1?'':'s')+' · Serial identity preserved across transfers.';
    }catch(e){q('specProvenance').textContent='Mint record available. Detailed provenance is temporarily unavailable.'}
  }
  function choose(item){
    current=item;
    q('specName').textContent=item.name;
    q('specRarity').textContent=String(item.rarity||'').toUpperCase();
    q('specRarity').className='specRarity '+String(item.rarity||'');
    q('specSerial').textContent='#'+String(item.serial_no||0).padStart(6,'0');
    q('specAcquired').textContent='Acquired '+safeDate(item.acquired_at);
    q('specSet').textContent=(item.set||'PRIMAL HATCH').toUpperCase();
    q('specPower').textContent=item.power||0;q('specLuck').textContent=item.luck||0;q('specCount').textContent=group.length||1;
    renderArt(item);
    q('specimens').innerHTML=group.map(x=>'<button class="specChip '+(x.item_id===item.item_id?'active':'')+'" data-id="'+x.item_id+'">#'+String(x.serial_no||0).padStart(6,'0')+'</button>').join('');
    q('specimens').querySelectorAll('.specChip').forEach(b=>b.onclick=()=>{const n=group.find(x=>x.item_id===Number(b.dataset.id));if(n)choose(n)});
    loadProvenance(item);
  }
  function open(item){
    group=(window.state?.collection||[]).filter(x=>x.id===item.id).sort((a,b)=>a.serial_no-b.serial_no);
    if(!group.length) group=[item];
    modal.classList.add('open');choose(item);
    try{window.Telegram?.WebApp?.HapticFeedback?.impactOccurred?.('light')}catch(e){}
  }
  q('specClose').onclick=()=>modal.classList.remove('open');
  q('specTrade').onclick=async()=>{
    if(!current)return;
    try{
      await window.api('/api/market/listings',{method:'POST',body:JSON.stringify({item_id:current.item_id,mode:'trade',want_rarity:'',note:''})});
      window.toast('Creature listed for trade');
      setTimeout(()=>location.href='/static/market.html',550);
    }catch(e){window.toast(e.message||'Could not list creature')}
  };
  q('specShare').onclick=()=>{
    if(!current)return;
    const url=window.state?.share_url||'';
    const t='I hatched '+current.name+' #'+String(current.serial_no||0).padStart(6,'0')+' in DROP1.';
    if(window.Telegram?.WebApp?.openTelegramLink&&url) window.Telegram.WebApp.openTelegramLink('https://t.me/share/url?url='+encodeURIComponent(url)+'&text='+encodeURIComponent(t));
    else window.toast('Share link unavailable');
  };
  stage.addEventListener('pointerdown',e=>{drag=true;startX=e.clientX;stage.setPointerCapture?.(e.pointerId)});
  stage.addEventListener('pointermove',e=>{if(!drag)return;tilt=Math.max(-10,Math.min(10,(e.clientX-startX)/12));art.style.transform='perspective(700px) rotateY('+tilt+'deg) scale(1.015)'});
  function resetTilt(){drag=false;tilt=0;art.style.transform='perspective(700px) rotateY(0deg) scale(1)'}
  stage.addEventListener('pointerup',resetTilt);stage.addEventListener('pointercancel',resetTilt);

  const original=window.openDetail;
  window.openDetail=function(id){
    const item=(window.state?.collection||[]).find(x=>x.item_id===id);
    if(item) return open(item);
    if(original) return original(id);
  };
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',init,{once:true}); else init();
})();