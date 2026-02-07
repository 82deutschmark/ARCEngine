# 020626-ct03-cascade-tiles-plan

## Objective

Create a new ARCEngine game `ct03` ("Cascade Tiles") as a reskin of `ft09` (Functional Tiles). The game reuses ft09's proven constraint-satisfaction mechanic but makes the **click-effect pattern** the central puzzle element.

**Constraint**: Avoid using colors 0-5 (grayscale/black/white). All visuals must use colors 6-15.

## CT03 Design Specification

### Game Identity

- **Game ID**: `ct03`
- **Class Name**: `Ct03`
- **Display Name**: "Cascade Tiles"
- **Concept**: Constraint-satisfaction puzzle where each level has a different click-effect pattern.

### Color Palette Adjustments (No Grayscale)

- **Background**: Color 15 (Purple) - replaces Color 4/5.
- **Padding/Borders**: Color 15 (Purple).
- **Inactive/Empty Slots**: Color 13 (Dark Red) - replaces Color 3.
- **Constraint Visuals**:
    - "Match" (Center): Target Color
    - "No Match" (Surround): Color 13 (Dark Red) - replaces Color 2/3.
- **Timer**:
    - Full: Color 12 (Orange)
    - Empty: Color 13 (Dark Red) - replaces Color 11/3 mixed use.
- **Effect Pattern Indicator**:
    - Active: Color 11 (Yellow)
    - Inactive: Color 13 (Dark Red)

### Mechanics (Identical to Plan)

1. **Constraint System**: 3x3 `cst`-tagged sprites. Center = target. Neighbors = match/no-match rules.
2. **Color Cycling**: Clicking advances tile through `cwU` list.
3. **Effect Pattern (`elp`)**: Varies per level (Center, Cross, HLine, VLine, Diag, Full).
4. **Timer**: Steps budget.

### Levels

Same logical layout as `ct01` plan, just visual re-mapping.

1. **Level 0 (Intro)**: Center-only, 2 colors.
2. **Level 1 (Cross)**: Plus shape, 2 colors.
3. **Level 2 (HLine)**: Horizontal line, 2 colors.
4. **Level 3 (VLine)**: Vertical line, 3 colors.
5. **Level 4 (Diag)**: Diagonal, 2 colors.
6. **Level 5 (Full)**: Full 3x3, 3 colors.

### Files

- `games/official/ct03.py`
- `games/__init__.py` registration.

### Verification

1. Import test.
2. Render test (ensure no 0-5 colors).
3. Gameplay loop test.
