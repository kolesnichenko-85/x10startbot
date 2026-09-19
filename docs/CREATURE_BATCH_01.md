# DROP1 — Creature Batch 01 Approval

Status: APPROVED FOR CLOSED BETA

## Batch
1. Moss Trike — Common
2. Ember Hatchling — Common
3. Pocket Raptor — Common
4. Tidejaw — Common
5. Suncrest — Common
6. Volt Stego — Rare
7. Obsidian Spino — Rare
8. Void Rex — Epic
9. Aurora Quetzal — Epic
10. Aurum Rex — Legendary

## Product review
- Species mix gives visible progression from approachable common creatures to aspirational legendary.
- No paid-resale language or investment framing.
- Existing published rarity odds remain unchanged.
- Free QA rotation can exercise every approved creature without affecting paid draw logic.

## Art review
- Every creature has a distinct silhouette and material language.
- Palette remains inside the Primal Hatch world: obsidian/navy base, cyan/violet energy, rarity-specific accents.
- Assets are framed as full-body collectible specimens, not cards.
- Crystal Ankyl and Neon Raptor remain true interactive 3D reference specimens; Batch 01 creatures use premium rendered specimen art until their GLB models pass the 3D pipeline.

## Engineering review
- All ten IDs already exist in the canonical catalog.
- Artwork is mapped by canonical creature ID.
- Collection, detail viewer, market, serials and provenance use the same IDs.
- Paid weighted draw is untouched.

## QA review
- Free test hatch rotates through all ten new creatures plus the existing polished reference specimens.
- Required checks: hatch reveal, collection grouping, specimen detail, exact serial selection, listing, offer, trade, provenance.
- SQLite and Postgres smoke suites remain mandatory release gates.

## Deferred
- GLB conversion for the ten-creature batch is not marked complete until generated models pass quality review.
- Physical printable versions remain a separate production pipeline.
