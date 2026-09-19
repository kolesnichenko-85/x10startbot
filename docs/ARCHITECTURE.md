# DROP1 Architecture

## Runtime topology
Telegram client → Telegram Mini App WebView → FastAPI service on Render.

Telegram Bot API is used for:
- `/start`, `/collection`, `/odds`, `/leaderboard`, `/support`
- Stars invoices and pre-checkout validation
- successful-payment confirmation
- Web App launch buttons

## Backend modules
- `app/main.py`: app lifecycle, health, bootstrap, Stars invoice/payment flow, free QA hatch, legal pages, analytics intake.
- `app/auth.py`: Telegram Mini App initData HMAC verification.
- `app/catalog.py`: Primal Hatch species and rarity weights.
- `app/db.py`: users, purchases, serials, owned specimens, rewards, analytics.
- `app/market_api.py`: listings, offers, atomic ownership swaps, provenance.
- `app/telegram.py`: Telegram Bot API integration.

## Frontend
- `app/static/index.html`: onboarding, global pool, hatch CTA, set progress, creature gallery.
- `app/static/hatch_v2.js`: egg reveal sequence, sound/haptics, 3D flagship reveal.
- `app/static/art.js`: premium art map, 3D specimen viewer, exact serial selector, provenance and trade entry.
- `app/static/market.html`: duplicate-first creature selection, serial selection, target listing, offer workflow and activity.

## Ownership model
An owned specimen is a durable row with:
- character/species id
- globally monotonic serial per species
- purchase identity
- current owner
- acquisition timestamp

A completed trade changes only the owner. The serial and mint identity are preserved.

## Market safety
The beta supports creature-for-creature exchange only. A listed specimen and a specimen locked in a pending offer cannot be spent twice. Accepting an offer performs the ownership swap in one database transaction and closes competing offers.

## 3D
Neon Raptor has a local GLB asset and a local 2D fallback. The Mini App uses a pinned `model-viewer` web component. If 3D fails to initialize in Telegram WebView, the viewer falls back to the polished poster instead of leaving a blank stage.

## Storage
The current web service still uses ephemeral SQLite. A free Render Postgres instance already exists, but the web service still requires its internal database URL to be connected before any public paid launch. No public paid traffic should be accepted on ephemeral storage.

## Release automation
`.github/workflows/drop1-quality.yml` enforces Python, product, frontend and API smoke gates on each push.
