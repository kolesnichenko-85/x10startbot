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
        ROOT / "app/static/vendor/model-viewer.min.js",
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
    forbidden = ["img.theapi.app/temp/", "dnznrvs05pmza.cloudfront.net", "ajax.googleapis.com/ajax/libs/model-viewer"]
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

CREATURE_BATCH_01_IDS = ("c002","c003","c004","c005","c006","r003","r004","e001","e002","l001")

def check_creature_batch_01():
    art = (ROOT / "app/static/art.js").read_text()
    catalog = (ROOT / "app/catalog.py").read_text()
    for cid in CREATURE_BATCH_01_IDS:
        assert f"'{cid}':" in art, f"Missing polished art mapping for {cid}"
        assert f'"id":"{cid}"' in catalog, f"Missing catalog entry for {cid}"

check_creature_batch_01()

def check_retention_runtime():
    db = (ROOT / "app/db.py").read_text()
    main_py = (ROOT / "app/main.py").read_text()
    index = (ROOT / "app/static/index.html").read_text()
    assert "def retention_state" in db
    assert "def claim_daily_reward" in db
    assert "def claim_daily_mission" in db
    assert "def claim_collection_milestone" in db
    assert "def spend_research_scout" in db
    assert "/api/rewards/daily" in main_py
    assert "/api/research/scout" in main_py
    assert "Daily Expedition" in index
    assert "Research Dust" in index

check_retention_runtime()


ALL_ART_IDS = (
    "c001","c002","c003","c004","c005","c006","c007","c008","c009","c010",
    "r001","r002","r003","r004","r005","r006","r007","r008",
    "e001","e002","e003","e004","e005","e006",
    "l001","l002","l003","l004","m001","m002"
)

def check_full_catalog_art():
    art = (ROOT / "app/static/art.js").read_text()
    import re
    pairs = dict(re.findall(r"'([cerml]\d{3})':'([^']+)'", art))
    for cid in ALL_ART_IDS:
        assert cid in pairs, f"Missing art mapping for {cid}"
        path = pairs[cid]
        if path.startswith("/static/"):
            p = ROOT / "app" / path.lstrip("/")
            assert p.exists() and p.stat().st_size > 0, f"Missing local art asset for {cid}: {p}"
    assert len([cid for cid in ALL_ART_IDS if cid in pairs]) == 30

check_full_catalog_art()


def check_paid_launch_guard():
    main_py = (ROOT / "app/main.py").read_text()
    assert "persistent_storage_ready()" in main_py
    assert "paid_launch_ready" in main_py
    assert "Paid DROP is locked until persistent storage is connected" in main_py

check_paid_launch_guard()
