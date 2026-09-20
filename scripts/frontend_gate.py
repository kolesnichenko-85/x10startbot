from pathlib import Path
import re, subprocess, tempfile, sys

ROOT=Path(__file__).resolve().parents[1]
files=[
    ROOT/"app/static/art.js",
    ROOT/"app/static/hatch_canvas_v22.js",
]
htmls=[
    ROOT/"app/static/index.html",
    ROOT/"app/static/market.html",
]

def check_js(path):
    r=subprocess.run(["node","--check",str(path)],capture_output=True,text=True)
    if r.returncode:
        print(r.stdout)
        print(r.stderr)
        raise SystemExit(f"JS syntax failed: {path}")

for p in files:
    check_js(p)

with tempfile.TemporaryDirectory() as td:
    td=Path(td)
    n=0
    for hp in htmls:
        txt=hp.read_text(encoding="utf-8")
        # Only inline scripts; external src scripts are checked by asset/invariant gate.
        for m in re.finditer(r"<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)</script>",txt,re.I):
            body=m.group(1).strip()
            if not body:
                continue
            p=td/f"{hp.stem}_{n}.js"
            p.write_text(body,encoding="utf-8")
            check_js(p)
            n+=1

# Release-level UX invariants.
index=(ROOT/"app/static/index.html").read_text(encoding="utf-8")
market=(ROOT/"app/static/market.html").read_text(encoding="utf-8")
hatch=(ROOT/"app/static/hatch_canvas_v22.js").read_text(encoding="utf-8")
art=(ROOT/"app/static/art.js").read_text(encoding="utf-8")
checks={
    "onboarding":"ENTER PRIMAL HATCH" in index,
    "hatch_cta":"HATCH EGG" in index or "HATCH TEST EGG" in index,
    "duplicate_grouping":"creatureQty" in index and "SPECIES" in index,
    "market_pair":"YOU OFFER" in market and "YOU GET" in market and "PROPOSE TRADE" in market,
    "real_3d":"neon-raptor.glb" in art and "model-viewer" in art,
    "egg_fallback":"drawEggFallback" in hatch and "primal-egg.png" in hatch,
    "ios_hatch_renderer":"hatchCanvas22" in hatch and "setTimeout(frame,33)" in hatch and "getContext(\"2d\"" in hatch,
    "daily_expedition":"Daily Expedition" in index and "missionList" in index and "dailyClaim" in index,
    "research_scout":"Research Scout" in index and "/api/research/scout" in index,
    "collection_milestones":"COLLECTION MILESTONES" in index and "milestoneGrid" in index,
    "collection_book":"Collection Book" in index and "bookGrid" in index and "renderBook" in index,
    "collector_rank":"rankLine" in index and "renderRank" in index,
    "exact_trade_target":"wantSpecies" in market and "want_character_id" in market and "offerId" in market,
    "invoice_cancel":"/api/purchases/" in index and "/cancel" in index,
    "visible_odds":"PRIMAL HATCH ODDS" in index and "Common 65%" in index and "No cash-out" in index,
    "legal_links":'href="/terms"' in index and 'href="/privacy"' in index,
    "local_model_viewer":"/static/vendor/model-viewer.min.js" in index and "ajax.googleapis.com/ajax/libs/model-viewer" not in index,
    "performance":"loading=\"lazy\"" in index and 'rel="preload" href="/static/assets/primal-egg.png"' in index,
    "rankings":"Collector Rankings" in index and "/api/leaderboard" in index,
}
bad=[k for k,v in checks.items() if not v]
if bad:
    raise SystemExit("Frontend invariant failure: "+", ".join(bad))
print("DROP1 frontend gate passed:", ", ".join(checks))
