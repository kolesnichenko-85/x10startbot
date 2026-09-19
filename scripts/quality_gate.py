from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]

def load_catalog():
    spec = importlib.util.spec_from_file_location("drop1_catalog", ROOT / "app" / "catalog.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.CATALOG

def main():
    catalog = load_catalog()
    assert len(catalog) == 30, f"Expected 30 Primal Hatch species, got {len(catalog)}"
    total = sum(int(x["weight"]) for x in catalog)
    assert total == 10000, f"Rarity weights must total 10000, got {total}"
    by_rarity = {}
    for x in catalog:
        by_rarity[x["rarity"]] = by_rarity.get(x["rarity"], 0) + int(x["weight"])
    expected = {"common": 6500, "rare": 2500, "epic": 800, "legendary": 180, "mythic": 20}
    assert by_rarity == expected, f"Odds drifted: {by_rarity}"

    required = [
        ROOT / "app/static/assets/neon-raptor.webp",
        ROOT / "app/static/assets/primal-egg.webp",
        ROOT / "app/static/models/neon-raptor.glb",
        ROOT / "app/static/models/crystal-ankyl.glb",
        ROOT / "app/static/assets/species/crystal-ankyl.png",
        ROOT / "app/static/index.html",
        ROOT / "app/static/market.html",
        ROOT / "app/static/art.js",
        ROOT / "app/static/hatch_canvas_v22.js",
        ROOT / "docs/DROP1_PRODUCT_OS.md",
    ]
    for p in required:
        assert p.exists() and p.stat().st_size > 0, f"Missing release asset: {p}"

    runtime = "\n".join((ROOT / p).read_text(errors="ignore") for p in [
        "app/static/index.html",
        "app/static/market.html",
        "app/static/art.js",
        "app/static/hatch_canvas_v22.js",
    ])
    forbidden = ["img.theapi.app/temp/", "dnznrvs05pmza.cloudfront.net"]
    for needle in forbidden:
        assert needle not in runtime, f"Temporary asset URL leaked into runtime: {needle}"

    index = (ROOT / "app/static/index.html").read_text()
    market = (ROOT / "app/static/market.html").read_text()
    art = (ROOT / "app/static/art.js").read_text()
    hatch = (ROOT / "app/static/hatch_canvas_v22.js").read_text()
    assert "HATCH TEST EGG" in index or "HATCH EGG" in index
    assert "PROPOSE TRADE" in market
    assert "/static/models/neon-raptor.glb" in art
    assert "/static/models/crystal-ankyl.glb" in art
    assert "/static/assets/primal-egg.png" in hatch
    print("DROP1 quality gate passed: catalog, odds, assets, hatch, 3D and market invariants OK.")

if __name__ == "__main__":
    main()
