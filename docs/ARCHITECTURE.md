# DROP1 Architecture

## Runtime topology
Telegram client → Telegram Mini App WebView → FastAPI service on Render → SQLite (closed beta) or PostgreSQL (production path).

Telegram Bot API is used for:
- `/start`, `/collection`, `/odds`, `/leaderboard`, `/terms`, `/privacy`, `/support`
- Telegram Stars invoice creation
- pre-checkout validation
- successful-payment confirmation
- Web App launch buttons

## Backend modules
- `app/main.py`: lifecycle, health, bootstrap, Stars reservation/payment flow, free QA hatch, legal pages, rewards and analytics intake.
- `app/auth.py`: Telegram Mini App initData HMAC and timestamp verification.
- `app/catalog.py`: 30 Primal Hatch species and canonical rarity weights.
- `app/db.py`: users, opaque referral codes, purchases, serials, owned specimens, pool, rewards, retention and analytics.
- `app/market_api.py`: listings, offers, PostgreSQL row locks, target validation, atomic ownership swaps and provenance.
- `app/storage.py`: SQLite/PostgreSQL adapter.
- `app/telegram.py`: Telegram Bot API integration.

## Frontend
- `app/static/index.html`: onboarding, global pool, hatch CTA, Daily Expedition, Codex, Collection Book and rankings.
- `app/static/hatch_canvas_v22.js`: Canvas hatch cinematic used for Telegram iOS reliability.
- `app/static/art.js`: complete art map, true-3D specimen viewer for supported GLBs, exact serial selector and provenance entry.
- `app/static/market.html`: duplicate-first ownership rail, exact serial selection, exact target listing, offer workflow and activity.
- `app/static/vendor/model-viewer.min.js`: self-hosted pinned 3D runtime.

## Ownership model
An owned specimen is a durable row containing species id, globally monotonic per-species serial, purchase identity, current owner and acquisition timestamp. A completed trade changes only the owner; serial and mint identity remain immutable.

## Market safety
The beta supports creature-for-creature exchange only. On PostgreSQL, listings/offers lock relevant rows so the same specimen cannot concurrently become both a listing and an offer. Listing target species or rarity is enforced on the server and rechecked at acceptance. Ownership swaps and provenance writes occur in one transaction.

## Payment safety
A paid hatch:
1. reserves one slot in the daily pool for a short TTL;
2. rejects a second active reservation for the same collector;
3. validates Telegram pre-checkout amount, payer and reservation expiry;
4. mints only after Telegram successful-payment confirmation;
5. is idempotent for duplicate Telegram delivery;
6. is server-blocked when persistent storage is not available.

## Privacy
Public market/provenance/ranking surfaces do not intentionally expose raw Telegram IDs. Collector labels derive from random opaque referral codes where available. Referral deep links do not contain Telegram IDs.

## Storage
The code path is dual-tested against SQLite and PostgreSQL 17 on every push. The current live closed beta still reports ephemeral SQLite. Public paid invoices remain locked until the Render service is connected to persistent PostgreSQL.

## Release automation
- `.github/workflows/drop1-quality.yml`: compile, product invariants, frontend gates, SQLite smoke, PostgreSQL smoke.
- `.github/workflows/drop1-live-smoke.yml`: waits for Render and verifies the exact deployed commit plus live endpoints/assets.
