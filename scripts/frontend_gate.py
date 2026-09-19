from pathlib import Path
import re, subprocess, tempfile, sys

ROOT=Path(__file__).resolve().parents[1]
files=[
    ROOT/"app/static/art.js",
    ROOT/"app/static/hatch_v2.js",
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
hatch=(ROOT/"app/static/hatch_v2.js").read_text(encoding="utf-8")
art=(ROOT/"app/static/art.js").read_text(encoding="utf-8")
checks={
    "onboarding":"ENTER PRIMAL HATCH" in index,
    "hatch_cta":"HATCH EGG" in index or "HATCH TEST EGG" in index,
    "duplicate_grouping":"creatureQty" in index and "SPECIES" in index,
    "market_pair":"YOU OFFER" in market and "YOU GET" in market and "PROPOSE TRADE" in market,
    "real_3d":"neon-raptor.glb" in art and "model-viewer" in art,
    "egg_fallback":"p6EggCssFallback" in hatch and "primal-egg.png" in hatch,\n    "ios_hatch_renderer":"runIOSHatch" in hatch and "requestAnimationFrame" in hatch and "IS_IOS" in hatch,
}
bad=[k for k,v in checks.items() if not v]
if bad:
    raise SystemExit("Frontend invariant failure: "+", ".join(bad))
print("DROP1 frontend gate passed:", ", ".join(checks))
