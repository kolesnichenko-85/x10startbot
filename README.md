# DROP1 — Mystery Collectibles

Telegram Mini App collectible game. Current season: **PRIMAL HATCH**.  
Current build: **0.13 release candidate / closed beta**.

## Core loop
Hatch → reveal → Collection Book → inspect exact serial → Daily Expedition → Research Scout → trade → return.

## Current product
- Telegram bot: `@drop1_game_bot`
- 30 / 30 Season 1 species with local production artwork.
- Interactive mystery-egg hatch with Telegram iOS Canvas fallback.
- 2 true interactive GLB specimens: Neon Raptor and Crystal Ankyl.
- Serial-numbered digital ownership and public provenance.
- Collection Book, Season Codex, collector ranks, XP, Research Dust, daily missions and streaks.
- Creature-for-creature market with exact serial selection and server-enforced species/rarity targets.
- Pseudonymous rankings, market identities and opaque referral codes.
- Telegram Stars payment flow implemented but server-blocked until persistent storage is connected.
- Paid resale and cash-out disabled.

## Published paid hatch odds
- Common — 65%
- Rare — 25%
- Epic — 8%
- Legendary — 1.8%
- Mythic — 0.2%

Every paid hatch guarantees exactly one digital creature. Progression systems and Research Scout do not change paid hatch odds.

## Engineering
Python / FastAPI backend, Telegram Mini App frontend, Telegram Bot API + Stars, SQLite/Postgres storage adapter, Render deployment, GitHub Actions release gates.

Runtime files:
- `app/main.py` — app, bootstrap, legal pages, Stars flow, rewards and health.
- `app/db.py` — ownership, payments, pool, retention, referrals and analytics.
- `app/market_api.py` — listings, offers, row locks, exact-target validation, atomic swaps and provenance.
- `app/static/index.html` — main Mini App.
- `app/static/hatch_canvas_v22.js` — iPhone-safe hatch renderer.
- `app/static/art.js` — artwork map and 3D specimen viewer.
- `app/static/market.html` — exchange UX.

## Release automation
Every push to `main` runs:
1. Python compilation.
2. Catalog, odds, asset and migration invariants.
3. Frontend JavaScript + UX checks.
4. SQLite end-to-end API smoke.
5. PostgreSQL 17 end-to-end API smoke.
6. After a green gate, a live Render smoke verifies the exact deployed commit, health, security headers, 30-species catalog, public privacy surfaces, legal pages and production assets.

## Current account-level launch blockers
The closed-beta product is live and automatically tested. Public paid hatching remains intentionally locked while:
1. Render web service storage is still ephemeral SQLite instead of the prepared Postgres database.
2. `FREE_TEST_MODE` remains enabled while that storage migration is pending.
3. Before real public traffic, Render Free compute and the expiring Free Postgres plan should be moved to production-grade plans.

The `/health` endpoint exposes `paid_launch_ready` and `launch_blockers`. The server refuses paid invoices while persistent storage is missing.

See `docs/RELEASE_CANDIDATE_012.md` and `docs/DROP1_PRODUCT_OS.md`.
