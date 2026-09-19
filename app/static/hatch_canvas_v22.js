(function(){
  window.DROP1_PREMIUM_HATCH=true;
  const EGG="/static/assets/primal-egg.png";
  const ART=()=>window.DROP1_ART||{};

  const css=`
  .reveal.canvasV22{position:fixed!important;inset:0!important;display:flex!important;align-items:stretch!important;justify-content:center!important;padding:0!important;background:#02040a!important;overflow:hidden!important}
  .reveal.canvasV22 .revealBox{position:absolute!important;z-index:5!important;left:16px!important;right:16px!important;bottom:calc(16px + env(safe-area-inset-bottom))!important;max-width:none!important;width:auto!important;opacity:0;transform:translateY(18px);transition:opacity .28s ease,transform .28s ease}
  .reveal.canvasV22.ready .revealBox{opacity:1;transform:translateY(0)}
  .reveal.canvasV22 .revealEyebrow,.reveal.canvasV22 .revealCard,.reveal.canvasV22 #revealName,.reveal.canvasV22 #revealSerial{display:none!important}
  .reveal.canvasV22 .revealBtns{display:grid!important;grid-template-columns:1.15fr 1fr!important;gap:9px!important;margin:0!important}
  .reveal.canvasV22 .revealBtns .btn{padding:14px 10px!important;border-radius:16px!important;font-size:13px!important}
  .hatchCanvas22{position:absolute;inset:0;width:100%;height:100%;display:block;z-index:1;background:#02040a}
  .hatchHud22{position:absolute;z-index:4;left:0;right:0;top:calc(20px + env(safe-area-inset-top));text-align:center;pointer-events:none}
  .hatchKicker22{font-size:10px;letter-spacing:.28em;font-weight:950;color:#9aacbf}.hatchKicker22 b{color:#54e6ff}
  .hatchStatus22{margin-top:9px;font-size:9px;letter-spacing:.24em;color:#7f95ab;font-weight:900}
  .hatchMeta22{position:absolute;z-index:4;left:18px;right:18px;bottom:calc(92px + env(safe-area-inset-bottom));text-align:center;opacity:0;transform:translateY(14px);transition:opacity .3s ease,transform .3s ease;pointer-events:none}
  .hatchMeta22.show{opacity:1;transform:translateY(0)}
  .hatchRarity22{font-size:10px;letter-spacing:.2em;color:#72e7ff;font-weight:950;text-transform:uppercase}.hatchName22{font-size:34px;line-height:1.02;font-weight:950;margin-top:7px}.hatchSerial22{font-size:11px;color:#9babc0;margin-top:5px;letter-spacing:.06em}
  `;
  const st=document.createElement("style");st.textContent=css;document.head.appendChild(st);

  function preload(src){return new Promise(resolve=>{if(!src)return resolve(null);const i=new Image();i.onload=()=>resolve(i);i.onerror=()=>resolve(null);i.src=src})}
  function clamp(v,a=0,b=1){return Math.max(a,Math.min(b,v))}
  function ease(t){t=clamp(t);return 1-Math.pow(1-t,3)}
  function lerp(a,b,t){return a+(b-a)*t}
  function roundedRect(ctx,x,y,w,h,r){ctx.beginPath();ctx.roundRect(x,y,w,h,r)}
  function haptic(kind){try{window.Telegram?.WebApp?.HapticFeedback?.impactOccurred?.(kind)}catch(e){}}

  function fitContain(i,maxW,maxH){if(!i)return [0,0];const s=Math.min(maxW/i.width,maxH/i.height);return [i.width*s,i.height*s]}
  function glow(ctx,x,y,r,c1,c2){
    const g=ctx.createRadialGradient(x,y,0,x,y,r);
    g.addColorStop(0,c1);g.addColorStop(1,c2);ctx.fillStyle=g;ctx.fillRect(x-r,y-r,r*2,r*2);
  }

  function drawEggFallback(ctx,cx,cy,w,h){
    ctx.save();ctx.translate(cx,cy);
    const g=ctx.createRadialGradient(-w*.16,-h*.22,5,0,0,w*.72);
    g.addColorStop(0,"#e8ffff");g.addColorStop(.16,"#87efff");g.addColorStop(.48,"#5b68cf");g.addColorStop(.78,"#30214e");g.addColorStop(1,"#0a0d17");
    ctx.fillStyle=g;ctx.strokeStyle="#79eaff";ctx.lineWidth=2;
    ctx.beginPath();
    ctx.moveTo(0,-h*.5);
    ctx.bezierCurveTo(w*.38,-h*.47,w*.52,-h*.13,w*.48,h*.17);
    ctx.bezierCurveTo(w*.43,h*.47,w*.22,h*.52,0,h*.52);
    ctx.bezierCurveTo(-w*.22,h*.52,-w*.43,h*.47,-w*.48,h*.17);
    ctx.bezierCurveTo(-w*.52,-h*.13,-w*.38,-h*.47,0,-h*.5);
    ctx.closePath();ctx.fill();ctx.stroke();ctx.restore();
  }

  function crackLines(ctx,cx,cy,s,alpha){
    if(alpha<=0)return;
    ctx.save();ctx.strokeStyle="rgba(190,250,255,"+alpha+")";ctx.lineWidth=Math.max(1.4,s*.006);ctx.shadowColor="#79efff";ctx.shadowBlur=12;
    const branches=[
      [[0,-.13],[-.08,-.05],[-.03,.02],[-.13,.10]],
      [[0,-.12],[.08,-.06],[.035,.02],[.14,.08]],
      [[-.02,.01],[-.05,.10],[-.015,.17],[-.08,.24]],
      [[.02,.02],[.05,.11],[.01,.18],[.08,.25]]
    ];
    for(const b of branches){ctx.beginPath();b.forEach((p,i)=>{const x=cx+p[0]*s,y=cy+p[1]*s;(i?ctx.lineTo(x,y):ctx.moveTo(x,y))});ctx.stroke()}
    ctx.restore();
  }

  async function cinematic(item){
    const r=document.getElementById("reveal"); if(!r)return;
    if(r._hatchTimer){clearInterval(r._hatchTimer);r._hatchTimer=null}
    r.className="reveal canvasV22";r.style.display="flex";r.dataset.hatching="1";
    const old=r.querySelector(".hatchCanvas22");if(old)old.remove();
    const oldHud=r.querySelector(".hatchHud22");if(oldHud)oldHud.remove();
    const oldMeta=r.querySelector(".hatchMeta22");if(oldMeta)oldMeta.remove();

    const canvas=document.createElement("canvas");canvas.className="hatchCanvas22";r.insertBefore(canvas,r.firstChild);
    const hud=document.createElement("div");hud.className="hatchHud22";hud.innerHTML='<div class="hatchKicker22">PRIMAL HATCH <b>// CINEMATIC</b></div><div class="hatchStatus22">INCUBATION LOCKED</div>';r.appendChild(hud);
    const meta=document.createElement("div");meta.className="hatchMeta22";
    meta.innerHTML='<div class="hatchRarity22">'+String(item.rarity||"common")+'</div><div class="hatchName22">'+String(item.name||"Creature")+'</div><div class="hatchSerial22">#'+String(item.serial_no||0).padStart(6,"0")+' · PWR '+(item.power||0)+' · LCK '+(item.luck||0)+'</div>';
    r.appendChild(meta);
    const status=hud.querySelector(".hatchStatus22");
    const box=r.querySelector(".revealBox");if(box){box.style.opacity="0";box.style.transform="translateY(18px)"}

    const artSrc=ART()[item.id||item.character_id]||"";
    const [eggImg,creatureImg]=await Promise.all([preload(EGG),preload(artSrc)]);

    const dpr=Math.min(window.devicePixelRatio||1,2);
    function resize(){const rect=canvas.getBoundingClientRect();canvas.width=Math.max(1,Math.round(rect.width*dpr));canvas.height=Math.max(1,Math.round(rect.height*dpr))}
    resize();
    const ctx=canvas.getContext("2d",{alpha:false});
    const started=performance.now();
    let fractured=false,awakened=false,confirmed=false;
    haptic("light");

    function frame(){
      const now=performance.now(),ms=now-started;
      const W=canvas.width/dpr,H=canvas.height/dpr;
      ctx.setTransform(dpr,0,0,dpr,0,0);
      ctx.clearRect(0,0,W,H);
      const bg=ctx.createRadialGradient(W*.5,H*.39,10,W*.5,H*.42,Math.max(W,H)*.72);
      bg.addColorStop(0,"#153d72");bg.addColorStop(.42,"#07101b");bg.addColorStop(1,"#02040a");ctx.fillStyle=bg;ctx.fillRect(0,0,W,H);

      // soft chamber rings
      ctx.save();ctx.strokeStyle="rgba(92,226,255,.12)";ctx.lineWidth=1;
      for(let n=0;n<3;n++){ctx.beginPath();ctx.ellipse(W*.5,H*.43,W*(.29+n*.07),H*(.14+n*.04),0,0,Math.PI*2);ctx.stroke()}ctx.restore();

      const cx=W*.5,cy=H*.43,base=Math.min(W*.58,H*.34);
      let eggA=1,eggScale=.82,rot=0,creatureA=.02,creatureScale=.86,flash=0,crack=0;

      const intro=ease(ms/650);eggScale=lerp(.78,.98,intro);
      if(ms>680&&ms<1500){
        const p=clamp((ms-680)/820);rot=(Math.sin(p*45)*5.5+Math.sin(p*71)*2.2)*(1-p*.25);eggScale=.98+Math.sin(p*Math.PI)*.04;crack=clamp((p-.18)/.55);
        if(!fractured){fractured=true;status.textContent="SHELL FRACTURE";haptic("medium")}
      }
      if(ms>=1450){
        const p=clamp((ms-1450)/720);eggA=1-ease(p);eggScale=1.02+ease(p)*.30;flash=Math.sin(Math.PI*clamp(p*1.25));
        const cp=ease(clamp((ms-1580)/850));creatureA=.03+.97*cp;creatureScale=.86+.14*cp+.03*Math.sin(cp*Math.PI);
        if(!awakened){awakened=true;status.textContent="SPECIMEN AWAKENING";haptic("heavy")}
      }
      if(ms>=2380&&!confirmed){confirmed=true;status.textContent="SPECIMEN CONFIRMED";meta.classList.add("show");r.classList.add("ready");haptic("light")}

      // scanner
      if(ms>120&&ms<1020){const p=(ms-120)/900;ctx.fillStyle="rgba(100,235,255,"+(Math.sin(Math.PI*p)*.55)+")";ctx.fillRect(W*.12,H*.25+H*.37*p,W*.76,1.5)}

      // creature first, behind egg
      if(creatureImg&&creatureA>0){
        const [cw,ch]=fitContain(creatureImg,W*.74,H*.56);
        ctx.save();ctx.globalAlpha=creatureA;ctx.translate(cx,cy);ctx.scale(creatureScale,creatureScale);ctx.shadowColor="#50ddff";ctx.shadowBlur=32;ctx.drawImage(creatureImg,-cw/2,-ch/2,cw,ch);ctx.restore();
      }

      // egg aura
      ctx.save();ctx.globalAlpha=.55*eggA;glow(ctx,cx,cy,base*.72,"rgba(76,226,255,.28)","rgba(60,70,180,0)");ctx.restore();

      if(eggA>.01){
        ctx.save();ctx.globalAlpha=eggA;ctx.translate(cx,cy);ctx.rotate(rot*Math.PI/180);ctx.scale(eggScale,eggScale);
        const ew=base*.62,eh=base*.78;
        ctx.shadowColor="#4be4ff";ctx.shadowBlur=24;
        if(eggImg){const [iw,ih]=fitContain(eggImg,ew,eh);ctx.drawImage(eggImg,-iw/2,-ih/2,iw,ih)}else drawEggFallback(ctx,0,0,ew*.72,eh);
        ctx.restore();
        crackLines(ctx,cx,cy,base,crack*eggA);
      }

      if(flash>0){ctx.save();ctx.globalAlpha=flash*.88;glow(ctx,cx,cy,Math.max(W,H)*.45,"rgba(255,255,255,.98)","rgba(92,210,255,0)");ctx.restore()}

      if(ms<3250){r._hatchTimer=setTimeout(frame,33)}
      else{r.dataset.hatching="0";status.style.opacity=".35";meta.classList.add("show");r.classList.add("ready")}
    }
    frame();
  }

  const old=window.showReveal;
  window.showReveal=function(item){return cinematic(item)};
})();