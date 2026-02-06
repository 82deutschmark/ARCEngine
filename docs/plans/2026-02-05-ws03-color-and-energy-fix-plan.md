# WS03 Color Scheme & Energy Placement Fix Plan

**Author:** Claude Opus 4.6
**Date:** 2026-02-05
**File:** `external/ARCEngine/games/official/ws03.py`
**Reference:** `external/ARCEngine/games/official/ws01.py` (source of truth for colors)

## Problem Summary

WS03 was created as a variant of WS01 with permanent fog of war + seeded randomness. The gameplay mechanics work well, but:

1. **Colors are completely wrong** - every sprite uses the wrong color palette
2. **Energy pickups are inaccessible** - placed inside walls or unreachable areas
3. **Special buttons lost their distinctive appearance** - the shape-change (kdy) and color-change (qqv) buttons use wrong colors

## Detailed Color Audit: WS01 vs WS03

### ARC Color Index Reference
```
0 = black, 1 = blue, 2 = red, 3 = green, 4 = yellow
5 = gray, 6 = magenta, 7 = orange, 8 = azure, 9 = maroon
10 = ?, 11 = ?, 12 = ?, 13 = ?, 14 = green, 15 = gray-light
```

### Sprite-by-Sprite Color Differences

| Sprite | Role | WS01 Color(s) | WS03 Color(s) | Fix Needed |
|--------|------|---------------|---------------|------------|
| `dcb` | Player shape option | 9 (maroon) | 6 (magenta) | Change to 9 |
| `fij` | Player shape option | 9 (maroon) | 6 (magenta) | Change to 9 |
| `ggk` | Gate border (dual-target) | 2 (red) | 5 (gray) | Change to 2 |
| `hep` | Level boundary block | 2 (red) | 5 (gray) | Change to 2 |
| `hul` | Goal area backdrop | 15 (gray-light) | 13 | Keep 13 (same) |
| `kdj` | Key indicator on HUD | 9 (maroon) | 6 (magenta) | Change to 9 |
| `kdy` | Rotation button | 9+7 (maroon+orange) | 6+1 (magenta+blue) | Change to 9+7 |
| `krg` | Death/reset flash | 12 (orange) | 8 (azure) | Change to 12 |
| `lhs` | Target landing pad | 2 (red) | 5 (gray) | Change to 2 |
| `lyd` | Player shape option | 9 (maroon) | 6 (magenta) | Change to 9 |
| `mgu` | World border (left wall + bottom box) | 2 (wall) + 13 (box border) | 5 (wall) + 4 (box border) | Change to 2+13 |
| `nio` | Player shape option | 9 (maroon) | 6 (magenta) | Change to 9 |
| `nlo` | Interior wall blocks | 13 (gray) | 4 (yellow) | Change to 13 |
| `opw` | Player shape option | 9 (maroon) | 6 (magenta) | Change to 9 |
| `pca` | Player piece (top+bottom) | 8+6 (azure+magenta) | 12+15 (orange+gray) | Change to 8+6 |
| `qqv` | Color-change button | 6,11,9,14,8 | 15,8,6,11,12 | Change to 6,11,9,14,8 |
| `rzt` | Key/target marker diagonal | 9 (maroon) | 6 (magenta) | Change to 9 |
| `snw` | Gate border | 2 (red) | 5 (gray) | Change to 2 |
| `tmx` | Player shape option | 9 (maroon) | 6 (magenta) | Change to 9 |
| `tuv` | Hidden level boundary | 9 (maroon) | 6 (magenta) | Change to 9 |
| `ulq` | Hidden gate outline | 9 (maroon) | 6 (magenta) | Change to 9 |
| `vxy` | Shape-change button | 9 (maroon) | 6 (magenta) | Change to 9 |
| `zba` | Energy pickup ring | 12 (orange) | 11 (yellow) | Change to 12 |

### Global Constants

| Constant | WS01 | WS03 | Fix |
|----------|------|------|-----|
| `BACKGROUND_COLOR` | 15 | 5 | Change to 15 |
| `PADDING_COLOR` | 15 | 5 | Change to 15 |
| `self.hul` (color cycle array) | [8, 6, 11, 14] | [12, 9, 14, 8] | Change to [8, 6, 11, 14] |

### Render Interface Colors (jvq class)

| Element | WS01 | WS03 | Fix |
|---------|------|------|-----|
| Fog overlay color | 2 (red) | 5 (gray) | Change to 2 |
| Empty fog area color | 15 | 5 | Change to 15 |
| Energy bar filled | 12 (orange) | 11 (yellow) | Change to 12 |
| Energy bar empty | 15 | 5 | Change to 15 |
| Lives filled | 14 (green) | 8 (azure) | Change to 14 |
| Lives empty | 15 | 5 | Change to 15 |

## Energy Pickup Accessibility Audit

WS03 added "fog compensation" energy pickups beyond what WS01 has. Need to verify each zba position is reachable (not inside nlo wall blocks).

**Approach:** For each level, map the nlo wall positions and verify no zba pickup overlaps with a wall block. If a zba is at position (x, y) and an nlo wall covers that 5x5 area, the pickup is trapped.

### WS01 energy counts per level (baseline):
- Level 1 (krg): 0 pickups
- Level 2 (mgu): 2 pickups
- Level 3 (puq): 3 pickups
- Level 4 (tmx): 4 pickups
- Level 5 (zba): 3 pickups
- Level 6 (lyd): 5 pickups
- Level 7 (fij): 6 pickups

### WS03 energy counts per level:
- Level 1 (krg): 2 pickups (WS01 had 0, added 2 "fog compensation")
- Level 2 (mgu): 4 pickups (WS01 had 2, added 2)
- Level 3 (puq): 5 pickups (WS01 had 3, added 2)
- Level 4 (tmx): 6 pickups (WS01 had 4, added 2)
- Level 5 (zba): 5 pickups (WS01 had 3, added 2)
- Level 6 (lyd): 7 pickups (WS01 had 5, added 2)
- Level 7 (fij): 6 pickups (same as WS01)

**Strategy for fixing inaccessible pickups:** I'll need to verify each fog-compensation pickup position against the wall layout. Any pickup sitting inside a wall block will be relocated to a nearby open corridor.

## What WS03 Should KEEP (gameplay mechanics)

1. Permanent fog of war (`self.qee = True` always, not driven by level data `kdy`)
2. Seeded randomness (`seed` parameter in constructor)
3. Extra energy pickups to compensate for fog difficulty (but in accessible locations)
4. The `__init__` signature accepting `seed` parameter

## Implementation Steps

### Step 1: Fix all sprite color definitions (lines 16-38)
Replace every sprite definition to use WS01's exact colors.

### Step 2: Fix global constants (lines 41-42)
```python
BACKGROUND_COLOR = 15
PADDING_COLOR = 15
```

### Step 3: Fix jvq render_interface colors (lines 65-96)
- Line 75: fog overlay `5` -> `2`
- Line 89: energy bar filled `11` -> `12`, empty `5` -> `15`
- Line 95: lives filled `8` -> `14`, empty `5` -> `15`

### Step 4: Fix color cycle array in Ws03.__init__ (line 274)
```python
self.hul = [8, 6, 11, 14]  # was [12, 9, 14, 8]
```

### Step 5: Fix kbj flash color in step() (line 366)
```python
self.nlo.color_remap(None, 5)  # already 5 in WS03, WS01 also uses 5 - OK
```

### Step 6: Audit and fix energy pickup positions
For each level, verify zba positions against nlo wall grid and relocate any inaccessible ones.

## Verification

1. Run the game and visually compare WS03 against WS01 screenshot
2. Verify all energy pickups are reachable by playing through each level
3. Confirm fog of war still works with correct overlay color (red/2, not gray)
4. Confirm color-change and shape-change buttons have their distinctive WS01 appearance
