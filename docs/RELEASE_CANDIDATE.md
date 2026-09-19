# DROP1 v0.9 Closed Beta Release Candidate

## Product status
The current build is a **closed-beta vertical slice**, not a public paid release.

### Implemented
- Telegram bot and Mini App launch.
- 0-Star QA hatch flow.
- Global daily drop pool that expands with new collectors.
- Premium egg visual with PNG fallback for Telegram iOS.
- Hatch sound, haptics, crack/flash/reveal choreography.
- Real interactive Neon Raptor GLB in the specimen viewer.
- 3D Neon Raptor after flagship hatch, with 2D fallback.
- Serial-numbered ownership.
- Collection grouped by species and duplicate count.
- Set completion progress.
- Exact specimen/serial selection.
- Public provenance without exposing owner Telegram IDs.
- Duplicate-first market.
- Create/cancel listings.
- Create/withdraw/reject/accept trade offers.
- Atomic ownership swaps.
- Referral deep-link foundation.
- Onboarding.
- Product analytics events.
- Terms, privacy and odds pages.
- Automated backend/frontend/API quality gates.

### Deliberately disabled
- User-to-user paid resale.
- Cash-out.
- Any promise of monetary appreciation.
- Physical-figure ordering.
- Public advertising/acquisition.

## Release gates still required before public paid launch
1. Sync the prepared Render Blueprint once so `DATABASE_URL` points the existing `drop1-game` service at the existing `drop1-db`. The dual SQLite/Postgres adapter and both smoke suites already pass.
2. Before public traffic, move the Render web service from sleeping Free compute to always-on compute and move the free Postgres database to a non-expiring paid plan.
3. Complete release-quality visual coverage for all active hatchable species.
4. Test Stars purchase, cancellation, duplicate Telegram updates and refund/reconciliation paths using a live paid QA purchase.
5. Add operator/support identity and a real human support route.
6. Validate physical-figure manufacturing economics before enabling ordering.

## Acceptance criteria for closed beta
- App boots in Telegram iOS.
- Egg is visible before fracture.
- One 0-Star hatch creates exactly one specimen.
- Reveal finishes without blocking the UI.
- Collection and set progress update.
- Neon Raptor opens as interactive 3D or safe fallback.
- Exact serial can be selected.
- Market supports own-specimen + target listing selection.
- CI passes all gates.
- Render deploy is Live.
