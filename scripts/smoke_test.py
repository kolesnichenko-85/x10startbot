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
from app.db import reserve_purchase

H1={"X-Telegram-Init-Data":"dev:777000001"}
H2={"X-Telegram-Init-Data":"dev:777000002"}
H3={"X-Telegram-Init-Data":"dev:777000003"}
H4={"X-Telegram-Init-Data":"dev:777000004"}

with TestClient(app) as client:
    health=client.get("/health")
    assert health.status_code==200 and health.json()["ok"] is True

    # Retention loop: daily claim, missions, collection milestone and duplicate Dust.
    r3=client.get("/api/bootstrap",headers=H3)
    assert r3.status_code==200
    retention=r3.json()["retention"]
    assert retention["daily"]["can_claim"] is True

    daily=client.post("/api/rewards/daily",headers=H3,json={})
    assert daily.status_code==200, daily.text
    assert daily.json()["reward"]["streak"]==1
    assert daily.json()["reward"]["dust"]>=1

    # Five sequential QA hatches are distinct release-quality species.
    for _ in range(5):
        h=client.post("/api/test/drop",headers=H3,json={})
        assert h.status_code==200, h.text

    # Hatch mission derives from ownership; inspect and market missions derive from product events.
    assert client.post("/api/events",headers=H3,json={"event":"specimen_open","source":"ci"}).status_code==200
    assert client.post("/api/events",headers=H3,json={"event":"market_open","source":"ci"}).status_code==200
    for key in ("hatch_one","inspect_one","visit_market"):
        claim=client.post(f"/api/missions/{key}/claim",headers=H3,json={})
        assert claim.status_code==200, (key, claim.text)

    milestone=client.post("/api/milestones/5/claim",headers=H3,json={})
    assert milestone.status_code==200, milestone.text
    after_rewards=client.get("/api/bootstrap",headers=H3).json()
    assert after_rewards["retention"]["daily"]["claimed"] is True
    assert all(m["claimed"] for m in after_rewards["retention"]["missions"])
    assert next(x for x in after_rewards["retention"]["milestones"] if x["threshold"]==5)["claimed"] is True
    assert after_rewards["user"]["dust"]>=5
    before_scout_dust=after_rewards["user"]["dust"]
    scout=client.post("/api/research/scout",headers=H3,json={})
    assert scout.status_code==200, scout.text
    assert scout.json()["target"] is not None
    after_scout=client.get("/api/bootstrap",headers=H3).json()
    assert after_scout["retention"]["scout_target"] is not None
    assert after_scout["user"]["dust"]==before_scout_dust-2

    # Finished Season 1: the free QA rotation must expose every catalog species once.
    ids=[]
    for _ in range(30):
        h=client.post("/api/test/drop",headers=H4,json={})
        assert h.status_code==200, h.text
        ids.append(h.json()["character"]["id"])
    assert len(ids)==30 and len(set(ids))==30, ids
    season=client.get("/api/bootstrap",headers=H4).json()
    assert season["unique_count"]==30
    assert len(season["catalog"])==30
    assert sum(x["owned"] for x in season["season_sets"])==30
    # 31st hatch repeats the first species and therefore creates useful duplicate Dust.
    before_dust=season["user"]["dust"]
    repeat=client.post("/api/test/drop",headers=H4,json={})
    assert repeat.status_code==200
    final_season=client.get("/api/bootstrap",headers=H4).json()
    assert final_season["unique_count"]==30
    assert final_season["user"]["dust"]==before_dust+1

    # One user cannot reserve the global paid pool repeatedly.
    reserve_purchase("ci_res_1",777000001,50,200,10,3,300,ttl_minutes=10)
    try:
        reserve_purchase("ci_res_2",777000001,50,200,10,3,300,ttl_minutes=10)
        raise AssertionError("second active reservation should be blocked")
    except ValueError as e:
        assert str(e)=="active_reservation_exists"
    cancelled=client.post("/api/purchases/ci_res_1/cancel",headers=H1,json={})
    assert cancelled.status_code==200, cancelled.text
    reserve_purchase("ci_res_2",777000001,50,200,10,3,300,ttl_minutes=10)
    assert client.post("/api/purchases/ci_res_2/cancel",headers=H1,json={}).status_code==200

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

print("DROP1 API smoke test passed: 30-species season, rewards, reservation anti-abuse, exact market trade and provenance.")
