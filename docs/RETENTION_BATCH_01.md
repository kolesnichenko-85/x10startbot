# DROP1 — Retention Batch 01 Approval

Status: APPROVED FOR CLOSED BETA

## Product Director
Goal: make the core loop worth repeating without changing paid rarity odds.

Approved loop:
Hatch → Inspect → Daily Expedition → Build Season Codex → Use duplicates for Dust → Scout a missing species → Trade → Return next day.

No mechanic in this batch changes published hatch odds or introduces cash-out, resale value promises, or paid user-to-user resale.

## Game / Economy
Implemented:
- Daily check-in reward: 15 XP + 1 Research Dust.
- Every 7th consecutive check-in adds +50 XP +2 Dust.
- Daily missions:
  - Hatch one creature: +20 XP +1 Dust.
  - Inspect one specimen: +10 XP.
  - Visit the exchange: +10 XP +1 Dust.
- Duplicate hatch: +1 Research Dust while the exact duplicate specimen remains owned and tradeable.
- Collection milestones:
  - 5 species: +50 XP +2 Dust.
  - 10 species: +100 XP +4 Dust.
  - 20 species: +250 XP +8 Dust.
  - 30 species: +500 XP +15 Dust.
- Research Scout costs 2 Dust once per UTC day and reveals one missing species target. It does not alter hatch odds.

Economy rule: Dust currently has no cash value and cannot be purchased, withdrawn, or converted to Stars.

## UX / Art
Implemented:
- Daily Expedition panel.
- Visible streak.
- XP and Dust reward copy before claim.
- Three claimable daily mission rows.
- Collection milestone track.
- Season Codex with progress by rarity collection:
  - Primal Hatch
  - Primal Flux
  - Ancient Core
  - Alpha Line
  - Origin
- Research Scout target sends the collector to the Market.
- Market prioritizes today's Scout target.

## Backend / Data
Implemented:
- daily_streak and last_daily_claim on users.
- daily_mission_claims.
- daily_scout_targets.
- idempotent reward keys.
- Postgres row locks where reward spending needs serialization.
- Duplicate Dust awarded at mint time.
- Same retention code path works on SQLite beta storage and Postgres.

## Security / Compliance
- No raw Telegram identity is added to public market output.
- Scout target does not alter random paid reward odds.
- Dust cannot purchase hatches and is not represented as monetary value.
- Reward endpoints are server-validated; clients cannot self-award XP or Dust.
- Paid resale remains disabled.

## QA
Release gate must verify:
- Daily reward cannot be claimed twice.
- Mission cannot be claimed before completion.
- Mission cannot be claimed twice.
- 5-species milestone requires five unique species.
- Research Scout requires 2 Dust and can only establish one target per day.
- SQLite and Postgres smoke tests pass.
- Existing hatch odds remain exactly 65 / 25 / 8 / 1.8 / 0.2.
- Trade and provenance tests remain green.

## Next product gate
Before adding more currencies or reward types, validate whether players actually use:
1. Daily Expedition.
2. Research Scout.
3. Market after Scout.
4. Duplicate trading.

If these are used, next retention batch can add ranks, badges, and limited season objectives. If they are ignored, simplify rather than stacking more systems.
