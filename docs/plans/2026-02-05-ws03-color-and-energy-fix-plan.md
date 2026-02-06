# WS03 Color Scheme & Energy Placement Fix Plan

**Author:** Claude Opus 4.6 / Claude Haiku 4.5
**Date:** 2026-02-05 (Revised)
**File:** `external/ARCEngine/games/official/ws03.py`
**Reference:** World Shifter visual style (magenta border, clean health bar)

## Problem Summary

WS03 has excessive gray (color 5) and visual clutter. The goal is to improve visual clarity by:

1. **Replace gray border with magenta** - Use color 6 for world border (like World Shifter)
2. **Improve health bar design** - Clearer color separation and visual readability
3. **Refactor player sprite** - Make it half the current size with colors 14 (green) and 10 (light blue)
4. **Clean up excess grays** - Remove overuse of color 5 and dark grays (2, 3, 4)

## ARC3 Color Index Reference

```
0:  White (#FFFFFF)
1:  Light Gray (#CCCCCC)
2:  Gray (#999999)
3:  Dark Gray (#666666)
4:  Darker Gray (#333333)
5:  Black (#000000) - AVOID OVERUSE
6:  Magenta/Pink (#E53AA3) - World border, distinctive UI elements
7:  Light Pink (#FF7BCC)
8:  Red (#F93C31)
9:  Blue (#1E93FF)
10: Light Blue (#88D8F1) - Player sprite
11: Yellow (#FFDC00)
12: Orange (#FF851B) - Health/energy bars
13: Dark Red (#921231)
14: Green (#4FCC30) - Player sprite
15: Purple (#A356D0)
```

**Strategy:** Use vibrant, distinctive colors; avoid gray (5) and dull grays (2-4) except for fog of war.


### Sprite Changes: WS03 → Improved (World Shifter Style)

| Sprite | Role | Current | Target | Notes |
|--------|------|---------|--------|-------|
| `dcb` | Player shape option | 6 (magenta) | 6 (magenta) | Keep - distinctive |
| `fij` | Player shape option | 6 (magenta) | 6 (magenta) | Keep - distinctive |
| `ggk` | Gate border | 5 (gray) | 6 (magenta) | Match world border |
| `hep` | Level boundary block | 5 (gray) | 6 (magenta) | Match world border |
| `hul` | Goal area backdrop | 13 (dark red) | 13 (dark red) | Keep |
| `kdj` | Key indicator on HUD | 6 (magenta) | 6 (magenta) | Keep |
| `kdy` | Rotation button | 6+1 (magenta+gray) | 6+12 (magenta+orange) | Improve color contrast |
| `krg` | Death/reset flash | 8 (red) | 8 (red) | Keep |
| `lhs` | Target landing pad | 5 (gray) | 6 (magenta) | Match world border |
| `lyd` | Player shape option | 6 (magenta) | 6 (magenta) | Keep - distinctive |
| `mgu` | World border | 5 (gray) + 4 (dark gray) | 6 (magenta) + 13 (dark red) | NEW: Use magenta (like World Shifter) |
| `nio` | Player shape option | 6 (magenta) | 6 (magenta) | Keep |
| `nlo` | Interior wall blocks | 4 (darker gray) | 13 (dark red) | Better contrast |
| `opw` | Player shape option | 6 (magenta) | 6 (magenta) | Keep |
| `pca` | **Player piece** | **12+15 (orange+gray)** | **14+10 (green+light blue) @ 50% scale** | **KEY CHANGE: Half size, new colors** |
| `qqv` | Color-change button | 15,8,6,11,12 | 15,8,6,11,12 | Keep current palette |
| `rzt` | Key/target marker | 6 (magenta) | 6 (magenta) | Keep |
| `snw` | Gate border | 5 (gray) | 6 (magenta) | Match world border |
| `tmx` | Player shape option | 6 (magenta) | 6 (magenta) | Keep |
| `tuv` | Hidden level boundary | 6 (magenta) | 6 (magenta) | Keep |
| `ulq` | Hidden gate outline | 6 (magenta) | 6 (magenta) | Keep |
| `vxy` | Shape-change button | 6 (magenta) | 6 (magenta) | Keep |
| `zba` | Energy pickup ring | 11 (yellow) | 12 (orange) | Better visual hierarchy |

### Global Constants

| Constant | Current | Target | Notes |
|----------|---------|--------|-------|
| `BACKGROUND_COLOR` | 5 (black) | 0 (white) | Better clarity |
| `PADDING_COLOR` | 5 (black) | 0 (white) | Better clarity |
| Fog overlay color | 5 (black) | 5 (black) | Keep (obscures behind magenta border) |

### Health/Energy Bar Colors

| Element | Current | Target | Notes |
|---------|---------|--------|-------|
| Energy bar filled | 11 (yellow) | 12 (orange) | Better saturation |
| Energy bar empty | 5 (black) | 0 (white) | Clearer contrast |
| Lives filled | 8 (red) | 14 (green) | Matches WS01 style |
| Lives empty | 5 (black) | 0 (white) | Clearer contrast |

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

## What WS03 Should KEEP (Core Identity)

1. **Permanent fog of war** - The defining feature of WS03 (unlike WS01)
   - `self.qee = True` always, not driven by level data
   - Fog overlay rendered at line 71-75 (jvq.render_interface)
2. **Seeded randomness** - Enable deterministic play testing
   - `seed` parameter in constructor
3. **Extra energy pickups** - Compensate for fog difficulty
4. **Gameplay mechanics** - All sprites, levels, and logic from WS01

## Key Difference: WS03 vs WS01

WS03 is NOT a complete recolor of WS01. It is WS01 + permanent fog of war with improved visual design.

## Implementation Steps

### Step 1: Update player sprite `pca` (line 30)
Create new half-size sprite using colors 14 (green) and 10 (light blue):
- Current: 5×5 pixels with colors 12+15
- Target: Scaled 50% (approximately 2-3px), colors 14+10

### Step 2: Update world border sprites (lines 19, 26, 33)
- `hep`: Change from 5 → 6 (magenta)
- `mgu`: Change from 5+4 → 6+13 (magenta + dark red)
- `snw`: Change from 5 → 6 (magenta)

### Step 3: Update other border sprites (lines 18, 24, 32)
- `ggk`: Change from 5 → 6 (magenta)
- `lhs`: Change from 5 → 6 (magenta)
- `ulq`: Change from 6 → 6 (keep magenta for consistency)

### Step 4: Update global constants (lines 41-42)
```python
BACKGROUND_COLOR = 0  # white instead of 5 (black)
PADDING_COLOR = 0     # white instead of 5 (black)
```

### Step 5: Update render_interface health bar colors (lines 89, 95)
- Line 89: Energy bar filled `11` → `12` (yellow → orange), empty `5` → `0` (black → white)
- Line 95: Lives filled `8` → `14` (red → green), empty `5` → `0` (black → white)

### Step 6: Update interior wall colors (line 28)
- `nlo`: Change from 4 → 13 (darker gray → dark red) for better contrast

### Step 7: Update button colors (lines 22, 31)
- `kdy`: Change from [−2, −2, 6, −2, −2] blue accent to orange (12) accent
- `qqv`: Review color palette, keep or adjust for consistency

## Verification

1. Visual check: Compare against World Shifter screenshot
2. Magenta border clearly distinguishes play area
3. Health bar is readable with orange (filled) and white (empty)
4. Player sprite is half-size and uses green+light blue colors
5. Interior walls are dark red (not dull gray)
6. **CONFIRM**: Fog of war still works and obscures properly with world border
