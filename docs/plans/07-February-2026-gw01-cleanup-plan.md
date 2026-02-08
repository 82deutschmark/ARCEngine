# Plan: GW01 → GW02 Full Cleanup
None of these are games, in the true sense. They're actually complex interactive reasoning benchmarks. Please keep that in mind. Don't go overly gamey or kids-themed.  
**Date:** 07-February-2026
**Author:** Claude Opus 4.6

## Context
`games/official/gw01.py` is a gravity-well puzzle game where the player tilts the board (WASD) and orbs slide in that direction, fusing and collecting into wells. The code works correctly but suffers from:
1. **Pervasive obfuscation** - every variable, method, sprite name, tag, and level data key uses cryptic 2-3 letter abbreviations
2. **Grayscale color misuse** - platforms use Gray (2) / Darker Gray (4), well centers use Dark Gray (3), letterbox uses Darker Gray (4)
3. **Uncreative sprites** - orbs are plain single-color diamonds, platforms are flat gray boxes

## Scope
**In:** Create `gw02.py` with readable names, fixed colors, improved sprite art. Register in `games/__init__.py`. Update changelog.
**Out:** No logic changes, no level layout changes, no new game mechanics. `gw01.py` left as-is (deprecated).

## Approach
Write `gw02.py` from scratch using `gw01.py` as source, applying all renames, color fixes, and sprite improvements in one pass. Deprecate `gw01.py` by renaming it to `gw01_deprecated.py` (or similar).

## Key Changes

### Colors (grayscale → themed)
- Platform fill: 2 (Gray) → 15 (Purple)
- Platform edge: 4 (Darker Gray) → 13 (Dark Red)
- Well center: 3 (Dark Gray) → 6 (Pink)
- Letterbox: 4 (Darker Gray) → 5 (Black, match background)

### Naming (obfuscated → readable)
- All color constants: `VDC`→`BACKGROUND_COLOR`, `PLT`→`PLATFORM_FILL`, etc.
- All sprite keys: `"plt"`→`"platform"`, `"obl"`→`"orb_light"`, etc.
- All tags: `"sld"`→`"solid"`, `"lgt"`→`"light"`, `"hvy"`→`"heavy"`, `"fsd"`→`"fused"`, etc.
- All methods: `uwl()`→`update_well_pixels()`, `sst()`→`simulate_gravity_step()`, etc.
- All instance vars: `self.col`→`self.orbs_collected`, `self.sim`→`self.simulating`, etc.
- All level data keys: `"ned"`→`"needed"`, `"phs"`→`"phase"`, `"cyc"`→`"cycle"`
- Lookup tables: `FSN`→`FUSION_RULES`, `ACC`→`WELL_ACCEPTS`

### Sprite Art
- Orb light: white center highlight
- Platforms: Dark Red (13) border, Purple (15) fill

## Verification
- `uv run pytest tests/` — all tests pass
- Verify `Gw02` imports and instantiates correctly
