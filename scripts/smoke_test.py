import os, tempfile, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

tmp = pathlib.Path(tempfile.gettempdir()) / "drop1_ci.db"
try:
    tmp.unlink()
except FileNotFoundError:
    pass

os.environ["DEV_MODE"]="true"
os.environ["FREE_TEST_MODE"]="true"
os.environ["DATABASE_PATH"]=str(tmp)
os.environ["BOT_TOKEN"]="ci-not-a-real-token"
os.environ["BASE_URL"]=""

from fastapi.testclient import TestClient
from app.main import app

H={"X-Telegram-Init-Data":"dev"}

with TestClient(app) as client:
    r=client.get("/health")
    assert r.status_code==200 and r.json()["ok"] is True

    r=client.get("/api/bootstrap",headers=H)
    assert r.status_code==200
    before=r.json()
    assert before["test_mode"] is True

    r=client.post("/api/test/drop",headers=H,json={})
    assert r.status_code==200, r.text
    item_id=r.json()["item_id"]

    after=client.get("/api/bootstrap",headers=H).json()
    assert len(after["collection"])==1
    item=after["collection"][0]
    assert item["item_id"]==item_id

    r=client.post("/api/market/listings",headers=H,json={
        "item_id":item_id,
        "mode":"trade",
        "want_rarity":"rare",
        "note":"CI smoke listing"
    })
    assert r.status_code==200, r.text

    my=client.get("/api/market/my",headers=H)
    assert my.status_code==200 and len(my.json()["listings"])==1

    p=client.get(f"/api/items/{item_id}/provenance")
    assert p.status_code==200
    payload=p.json()
    assert "owner_id" not in payload["item"]
    assert payload["history"][0]["event_type"]=="mint"

print("DROP1 API smoke test passed: health, auth, hatch, collection, listing and provenance.")
