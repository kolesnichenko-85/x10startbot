# DROP1 0.13 Closed-Beta Release Candidate

This file supersedes the older 0.9 release note.

## Implemented
- Telegram bot and Mini App launch.
- iPhone-safe 0-Star closed-beta hatch.
- Global daily pool.
- 30 / 30 Season 1 species with production artwork.
- Mystery egg fracture/reveal cinematic.
- Two true interactive GLB specimens with 2D fallback.
- Serial-numbered ownership and immutable provenance.
- Collection Book and five-part Season Codex.
- Daily Expedition, streaks, missions, milestones, XP, Research Dust and Research Scout.
- Collector ranks and privacy-safe leaderboard.
- Duplicate-first exchange with exact specimen/serial selection.
- Exact desired species or rarity with server-side enforcement.
- PostgreSQL locking for market race protection and atomic swaps.
- Opaque referral codes.
- Published odds, Terms and Privacy surfaces in both Mini App and bot.
- Stars invoice reservation, cancellation, pre-checkout and idempotent minting.
- Paid launch guard on ephemeral storage.
- Self-hosted 3D runtime and production cache headers.
- Automated SQLite + PostgreSQL release tests.
- Exact-commit live Render smoke after green CI.

## Deliberately disabled
- Paid user-to-user resale.
- Cash-out.
- Investment/value claims.
- Physical figure ordering.
- Public paid acquisition while infrastructure gates remain red.

## Remaining account-level gates before paid public launch
1. Connect the existing Render PostgreSQL database to `drop1-game` as `DATABASE_URL`.
2. Verify `/health` reports `storage=postgres` and `persistent_storage=true`.
3. Move web compute from sleeping Free service to always-on production compute.
4. Move the expiring Free PostgreSQL instance to a persistent production plan.
5. Set `FREE_TEST_MODE=false` only after steps 1–4.
6. Perform one live Stars QA purchase and support/reconciliation drill before acquisition.

## Closed-beta acceptance state
Automated gates cover boot, 30-species rotation, rewards, referral privacy, signed Telegram auth, payment reservation abuse, exact-target trades, atomic swaps, provenance, frontend syntax, iPhone renderer and production asset delivery. The live Render build is checked after every green quality gate.
