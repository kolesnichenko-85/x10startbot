# DROP1 Product OS

Every meaningful DROP1 change must pass these seven virtual departments before release.

## 1. Product Director
Gate: the change must strengthen at least one core loop: Hatch -> Collect -> Inspect -> Trade -> Return.
Reject: features that add complexity without improving retention, collection desire, trading liquidity, or monetization.

## 2. Game / Economy
Gate: rarity, supply, serial identity, duplicate utility, and market rules remain internally consistent.
Current canonical odds: Common 65%, Rare 25%, Epic 8%, Legendary 1.8%, Mythic 0.2%.
No cash-out or promised monetary value. Paid user-to-user resale remains disabled until a separate compliance and payments review.

## 3. Art Director / UX
Gate: premium creature-first presentation, one clear primary action per screen, mobile-first touch targets, no emoji placeholders in release-quality flagship flows.
Digital creatures may be richer than future physical figures; physical previews must accurately represent manufacturable products.

## 4. Frontend Engineering
Gate: Telegram iOS WebView first, cache-busted static assets, no competing reveal layers, no blocking animation longer than necessary, useful fallback on asset failure.
True 3D must be labelled as 3D only when a GLB/glTF asset is actually rendered. Image parallax is an interactive preview, not 360-degree 3D.

## 5. Backend / Data
Gate: serial identity never changes, ownership swaps are atomic, listing locks prevent double-spend, purchase minting happens only after verified payment.
Test mode must remain isolated from paid launch assumptions.

## 6. Security / Privacy / Compliance
Gate: never expose Telegram IDs or internal ownership references in public provenance. Never log tokens. Randomized paid rewards must show odds and guarantee one digital creature.
No public launch on ephemeral storage.

## 7. QA / Release
Required smoke test on each release:
- Mini App boots on Telegram iOS.
- Hatch button produces one creature.
- Reveal can be closed and repeated.
- Collection count/species count update.
- Exact specimen serial can be inspected.
- Market can select own duplicate/specimen and a target listing.
- Trade proposal/accept/reject/withdraw paths remain functional.
- /health returns ok and current version.
- No uncaught startup error in Render logs.

## Current release priorities
P0: flagship Neon Raptor hatch + specimen experience.
P0: intuitive duplicate-first creature exchange.
P0 before paid launch: persistent production database and always-on hosting.
P1: true animated GLB creature, 360-degree inspection, reaction animations.
P1: art production for all 30 Primal Hatch species.
P2: validated physical-figure pipeline and print-ready masters.
