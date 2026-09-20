# DROP1 — Release Candidate 0.12

Status: PRODUCT-COMPLETE FOR CLOSED BETA  
Paid public launch: ACCOUNT INFRASTRUCTURE GATED

## Product
The complete Season 1 loop is implemented:

Hatch → Reveal → Collection Book → Inspect exact serial → Daily Expedition → Research Dust → Scout a missing species → Market → Exact-species trade → Provenance → Return.

## Content
- 30 / 30 catalog species have production artwork stored locally in the repository.
- Test mode rotates through all 30 species exactly once before repeating.
- Neon Raptor and Crystal Ankyl are true interactive GLB specimens.
- Other creatures use premium production renders and never claim to be true 3D.
- Mystery egg animation includes the iPhone Canvas fallback.

## Economy
Published paid odds are unchanged:
- Common 65%
- Rare 25%
- Epic 8%
- Legendary 1.8%
- Mythic 0.2%

Every paid egg guarantees one creature.
Research Dust does not alter paid odds and has no cash value.
Paid user-to-user resale and cash-out are disabled.

## Retention
- Daily Expedition streak
- Daily missions
- Collection milestones
- Duplicate Dust
- Research Scout
- Season Codex
- Collector ranks
- Full 30-species Collection Book

## Market
- Creature-for-creature trades
- Exact specimen / serial selection
- Exact desired species or rarity
- Scout target prioritization
- Atomic ownership swap
- Listing and offer locks
- Public provenance without owner Telegram IDs

## Privacy and security
- Market collector identity is pseudonymized.
- Public leaderboard is pseudonymized.
- Referral links use opaque random codes, not Telegram IDs.
- Webhook secret is not written to logs.
- Model-viewer is self-hosted.
- Basic response security headers are enabled.
- A user cannot reserve the global paid pool repeatedly with concurrent invoices.
- Cancelled invoices release their reservation immediately.
- Paid invoices are server-blocked while storage is ephemeral.

## Automated release QA
Every push checks:
- Python syntax
- exact 30-species catalog
- exact rarity probabilities
- local runtime assets
- all 30 artwork mappings
- iPhone hatch renderer
- Collection Book / Codex / Expedition / Scout
- exact-target market UX
- visible odds and legal links
- SQLite smoke suite
- Postgres 17 smoke suite
- full 30-species QA rotation
- duplicate economy
- two-user atomic trade
- provenance privacy
- referral/leaderboard privacy
- payment reservation anti-abuse

## Account-level launch gates
These are deliberately not bypassed by code.

1. Connect the existing Render Postgres database to the existing web service as DATABASE_URL. The application is already dual-tested on SQLite and Postgres.
2. Move Render web compute from Free to an always-on paid plan before public paid traffic.
3. Move the current free Render Postgres database to a persistent paid plan before its expiry.
4. After 1–3 are confirmed, set FREE_TEST_MODE=false. Only then does the Stars purchase path become available.

The health endpoint reports paid_launch_ready and launch_blockers. Paid purchases remain blocked if persistent storage is missing.
