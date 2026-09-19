# DROP1 — Mystery Collectibles

Telegram Mini App collectible game. Current product line: **PRIMAL HATCH**.

## Core loop
Hatch an egg → reveal a creature → inspect the exact serial-numbered specimen → build the set → trade duplicates → return for the next global pool.

## Closed beta
- Telegram bot: `@drop1_game_bot`
- Web service: `https://drop1-game.onrender.com`
- Test hatch price: 0 Telegram Stars
- Paid resale: disabled
- Card-for-card creature trading: enabled
- Flagship interactive 3D specimen: Neon Raptor
- Current beta visual assets: premium egg, Neon Raptor, Pebbleback

## Product invariants
- Every paid hatch guarantees one digital creature.
- Published rarity odds: Common 65%, Rare 25%, Epic 8%, Legendary 1.8%, Mythic 0.2%.
- Serial identity survives ownership transfers.
- No cash-out or promised monetary value.
- User-to-user paid resale is not enabled in beta.
- Exact Telegram IDs are not exposed by public provenance.

## Engineering
Python / FastAPI backend, Telegram Mini App frontend, Telegram Stars payment flow, SQLite beta storage, GitHub Actions quality gate, Render deployment.

See:
- `docs/DROP1_PRODUCT_OS.md` — cross-functional release gates.
- `docs/ARCHITECTURE.md` — technical architecture.
- `docs/RELEASE_CANDIDATE.md` — current release state and launch blockers.

## Quality gate
Every push runs:
1. Python compile check.
2. Catalog/rarity invariants.
3. Frontend JavaScript syntax checks.
4. UX release invariants.
5. End-to-end API smoke test: health, dev auth, hatch, collection, listing, provenance.

## Public-launch blockers
Closed beta is functional. Public paid launch remains intentionally blocked until persistent production storage and always-on hosting are enabled, final catalog art coverage is complete, and payment/refund operations are signed off.
