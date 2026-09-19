import os, tempfile, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

tmp = pathlib.Path(tempfile.gettempdir()) / "drop1_ci.db"
try:
    tmp.unlink()
except FileNotFoundError:
    pass

os.environ["DEV_MODE"]="true"
os.environ["FREE_TEST_MODE"]="true"
os.environ.setdefault("DATABASE_PATH", str(tmp))
os.environ["BOT_TOKEN"]="ci-not-a-real-token"
os.environ["BASE_URL"]=""

from fastapi.testclient import TestClient
from app.main import app

H1={"X-Telegram-Init-Data":"dev:777000001"}
H2={"X-Telegram-Init-Data":"dev:777000002"}

with TestClient(app) as client:
    health=client.get("/health")
    assert health.status_code==200 and health.json()["ok"] is True

    # Collector 1 hatches and lists a specimen.
    before=client.get("/api/bootstrap",headers=H1)
    assert before.status_code==200 and before.json()["test_mode"] is True
    hatch1=client.post("/api/test/drop",headers=H1,json={})
    assert hatch1.status_code==200, hatch1.text
    item1=hatch1.json()["item_id"]

    after1=client.get("/api/bootstrap",headers=H1).json()
    assert len(after1["collection"])==1
    specimen1=after1["collection"][0]
    assert specimen1["item_id"]==item1

    listing=client.post("/api/market/listings",headers=H1,json={
        "item_id":item1,
        "mode":"trade",
        "want_rarity":"rare",
        "note":"CI smoke listing"
    })
    assert listing.status_code==200, listing.text
    listing_id=listing.json()["listing_id"]

    # Public market is authenticated and never exposes raw collector identity.
    feed=client.get("/api/market",headers=H1)
    assert feed.status_code==200, feed.text
    rows=feed.json()["listings"]
    assert len(rows)==1
    seller=rows[0]["seller"]
    assert seller["is_mine"] is True
    assert seller["label"]=="You"
    for forbidden in ("id","username","first_name","telegram_id"):
        assert forbidden not in seller
    assert "owner_id" not in rows[0]["item"]

    # Collector 2 hatches and offers their exact serial.
    b2=client.get("/api/bootstrap",headers=H2)
    assert b2.status_code==200
    hatch2=client.post("/api/test/drop",headers=H2,json={})
    assert hatch2.status_code==200, hatch2.text
    item2=hatch2.json()["item_id"]

    offer=client.post(f"/api/market/listings/{listing_id}/offers",headers=H2,json={
        "offered_item_id":item2,
        "note":"CI trade offer"
    })
    assert offer.status_code==200, offer.text
    offer_id=offer.json()["offer_id"]

    received=client.get("/api/market/my",headers=H1)
    assert received.status_code==200
    assert len(received.json()["received_offers"])==1
    offerer=received.json()["received_offers"][0]["offerer"]
    assert offerer["is_mine"] is False
    assert offerer["label"].startswith("Collector ")
    for forbidden in ("id","username","first_name","telegram_id"):
        assert forbidden not in offerer

    # Accepting performs an atomic ownership swap.
    accepted=client.post(f"/api/market/offers/{offer_id}/accept",headers=H1,json={})
    assert accepted.status_code==200, accepted.text

    final1=client.get("/api/bootstrap",headers=H1).json()["collection"]
    final2=client.get("/api/bootstrap",headers=H2).json()["collection"]
    assert len(final1)==1 and final1[0]["item_id"]==item2
    assert len(final2)==1 and final2[0]["item_id"]==item1

    p1=client.get(f"/api/items/{item1}/provenance")
    p2=client.get(f"/api/items/{item2}/provenance")
    assert p1.status_code==200 and p2.status_code==200
    for payload in (p1.json(),p2.json()):
        assert "owner_id" not in payload["item"]
        assert payload["history"][0]["event_type"]=="mint"
        assert payload["trade_count"]==1
        assert payload["history"][-1]["event_type"]=="trade"

print("DROP1 API smoke test passed: health, two-user hatch, privacy-safe market, offer, atomic trade and provenance.")
