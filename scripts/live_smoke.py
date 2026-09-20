import json
import os
import time
import urllib.error
import urllib.request

BASE_URL=os.getenv("DROP1_LIVE_URL","https://drop1-game.onrender.com").rstrip("/")

def request(path, method="GET", timeout=30):
    req=urllib.request.Request(
        BASE_URL+path,
        method=method,
        headers={"User-Agent":"DROP1-Live-Smoke/1.0","Accept":"*/*"},
    )
    with urllib.request.urlopen(req,timeout=timeout) as r:
        body=r.read()
        return r.status,{k.lower():v for k,v in r.headers.items()},body

def wait_health():
    last=None
    for attempt in range(10):
        try:
            status,headers,body=request("/health",timeout=35)
            if status==200:
                data=json.loads(body.decode())
                if data.get("ok") is True:
                    return headers,data
                last=f"health ok flag missing: {data}"
        except Exception as e:
            last=repr(e)
        time.sleep(8)
    raise AssertionError(f"live health never became ready: {last}")

headers,health=wait_health()
assert str(health.get("version","")).startswith("0.13."), health
assert isinstance(health.get("launch_blockers"),list), health
if health.get("paid_launch_ready"):
    assert health["launch_blockers"]==[], health
else:
    assert health["launch_blockers"], health

status,root_headers,root=request("/")
assert status==200
root_text=root.decode("utf-8")
for token in ("Collection Book","Collector Rankings","PRIMAL HATCH ODDS","Daily Expedition"):
    assert token in root_text, token
assert root_headers.get("x-content-type-options")=="nosniff"
assert root_headers.get("referrer-policy")=="no-referrer"
assert "camera=()" in root_headers.get("permissions-policy","")

status,_,catalog_body=request("/api/catalog")
catalog=json.loads(catalog_body.decode())["characters"]
assert len(catalog)==30, len(catalog)
assert all("weight" not in x for x in catalog)

status,_,leaders_body=request("/api/leaderboard")
leaders=json.loads(leaders_body.decode()).get("leaders",[])
for row in leaders:
    for forbidden in ("telegram_id","username","first_name","ref_code"):
        assert forbidden not in row, (forbidden,row)

status,art_headers,art_body=request("/static/art.js")
assert status==200
art=art_body.decode("utf-8")
for prefix,count in (("c",10),("r",8),("e",6),("l",4),("m",2)):
    for n in range(1,count+1):
        cid=f"{prefix}{n:03d}"
        assert f"'{cid}':" in art, cid
assert "no-store" in art_headers.get("cache-control","")

for path,min_size in (
    ("/static/assets/primal-egg.png",500000),
    ("/static/vendor/model-viewer.min.js",500000),
    ("/static/models/neon-raptor.glb",1000000),
    ("/static/models/crystal-ankyl.glb",1000000),
):
    status,h,b=request(path)
    assert status==200, path
    assert len(b)>=min_size,(path,len(b))
    if path.startswith("/static/vendor/") or path.startswith("/static/models/"):
        assert "immutable" in h.get("cache-control",""),(path,h.get("cache-control"))

for path,needle in (
    ("/odds","Common — 65.0%"),
    ("/terms","DROP1 Terms — Beta"),
    ("/privacy","DROP1 Privacy — Beta"),
):
    status,_,body=request(path)
    assert status==200,path
    assert needle in body.decode("utf-8"),(path,needle)

status,_,_=request("/",method="HEAD")
assert status==200

print("DROP1 live smoke passed")
print(json.dumps({
    "version":health.get("version"),
    "stage":health.get("stage"),
    "storage":health.get("storage"),
    "persistent_storage":health.get("persistent_storage"),
    "paid_launch_ready":health.get("paid_launch_ready"),
    "launch_blockers":health.get("launch_blockers"),
},ensure_ascii=False))
