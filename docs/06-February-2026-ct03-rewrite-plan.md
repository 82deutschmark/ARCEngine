# Plan: Rewrite ct03.py -- Best of CT01 + CT03

## Context

Two implementations of "Cascade Tiles" exist: CT01 (Claude) and CT03 (ChatGPT). Both reskin ft09's constraint-satisfaction mechanic with varying click-effect patterns. Each has strengths the other lacks. This plan rewrites `games/official/ct03.py` to combine the best of both.

**CT03's win**: Auto-generates constraint sprites by simulating "solution clicks," so constraints are always correct by construction. Also has a minimap showing the target state.

**CT01's win**: Uses the engine API properly (`get_sprite_at`, `color_remap`, sprites defined in Level constructors), timer only ticks on real tile clicks, constraints are visible to the player.

**CT03's problems to fix**: Lambdas in level data (deepcopy landmine), `remove_all_sprites()` rebuild pattern, manual O(n) tile lookups, direct pixel assignment instead of `color_remap`, timer ticks on empty clicks, no center-cell check in win logic.

## What We're Building

A single file `games/official/ct03.py` (~300 lines) that:
1. Defines levels statically in Level constructors (tiles, bg, swatches, pattern indicator) -- like CT01
2. Generates constraint sprites and minimap dynamically in `on_set_level` -- like CT03
3. Uses engine APIs throughout -- like CT01
4. Only ticks timer on successful tile clicks -- like CT01
5. Keeps constraints visible (not hidden) -- like CT01/ft09
6. Avoids grayscale for non-match indicator (uses color 6 pink instead of 2 gray)

## File to Create (overwrite)

`games/official/ct03.py`

## File to Leave Alone

`games/__init__.py` -- already has ct03 registered, no changes needed.

---

## Exact Specification

### Constants

```python
BACKGROUND_COLOR = 15       # Purple
PADDING_COLOR = 15          # Purple
TILE_SPACING = 4            # Pixels between tile origins
TIMER_FILLED_COLOR = 12     # Orange
TIMER_EMPTY_COLOR = 13      # Dark Red
PATTERN_ACTIVE_COLOR = 11   # Yellow
PATTERN_INACTIVE_COLOR = 13 # Dark Red
NOMATCH_INDICATOR = 6       # Pink (non-zero value for "must NOT match" in constraints)
```

### NEIGHBOR_OFFSETS

Same as CT01. A 3x3 grid of `(dx, dy)` tuples mapping pattern cells to tile-spacing offsets:
```
[(-1,-1), (0,-1), (1,-1)]
[(-1, 0), (0, 0), (1, 0)]
[(-1, 1), (0, 1), (1, 1)]
```

### Sprite Templates (module-level dict)

Only 3 templates needed (everything else is generated):

| Key | Size | Purpose | Tags | Layer | Collidable |
|-----|------|---------|------|-------|------------|
| `"tile"` | 3x3 solid color 14 | Clickable tile (remapped per level) | `["tile"]` | 0 | True |
| `"bg"` | 32x32 solid `BACKGROUND_COLOR` | Background fill | none | -2 | False |
| `"swatch"` | 2x2 solid color 0 | Color reference (remapped per level) | none | 0 | False |

### Level Data Schema

Each Level's `data` dict contains:

| Key | Type | Purpose |
|-----|------|---------|
| `"timer_budget"` | `int` | Steps before game over |
| `"color_cycle"` | `list[int]` | Colors to cycle through on click |
| `"effect_pattern"` | `list[list[int]]` | 3x3 grid, 1=affected, 0=not |
| `"solution_clicks"` | `list[tuple[int,int]]` | `(col_index, row_index)` into the tile grid. These clicks, applied from initial state, produce the target state. |

No lambdas. No functions. Only serializable data.

### Level Definitions (6 levels)

Tiles are placed in the Level constructor. The helper `_make_tile_grid(rows, cols, origin_x, origin_y)` creates cloned tile sprites at TILE_SPACING intervals (same as CT01).

The helper `_build_effect_indicator(elp)` creates a 3x3 sprite showing active/inactive cells (same as CT01).

#### Level 0: "intro" -- Center-Only

| Field | Value |
|-------|-------|
| Grid | 3 cols x 3 rows, origin (10, 10) |
| `effect_pattern` | `[[0,0,0],[0,1,0],[0,0,0]]` |
| `color_cycle` | `[14, 8]` (green, red) |
| `timer_budget` | 40 |
| `solution_clicks` | `[(1, 1)]` -- click center tile |

Sprites in Level constructor:
- `bg` at (0,0)
- 9 tiles from `_make_tile_grid(3, 3, 10, 10)`
- effect indicator at (28, 1)
- 2 swatches at (29, 5) and (29, 7)

#### Level 1: "cross" -- Plus Shape

| Field | Value |
|-------|-------|
| Grid | 3 cols x 3 rows, origin (10, 10) |
| `effect_pattern` | `[[0,1,0],[1,1,1],[0,1,0]]` |
| `color_cycle` | `[9, 12]` (blue, orange) |
| `timer_budget` | 48 |
| `solution_clicks` | `[(1, 1)]` -- click center |

Sprites: same structure as L0, 2 swatches.

#### Level 2: "hline" -- Horizontal Line

| Field | Value |
|-------|-------|
| Grid | 3 cols x 4 rows, origin (10, 6) |
| `effect_pattern` | `[[0,0,0],[1,1,1],[0,0,0]]` |
| `color_cycle` | `[8, 11]` (red, yellow) |
| `timer_budget` | 64 |
| `solution_clicks` | `[(1, 0), (0, 2)]` -- click top-center, then left of row 2 |

Sprites: bg, 12 tiles, indicator, 2 swatches.

#### Level 3: "vline" -- Vertical Line

| Field | Value |
|-------|-------|
| Grid | 4 cols x 3 rows, origin (6, 10) |
| `effect_pattern` | `[[0,1,0],[0,1,0],[0,1,0]]` |
| `color_cycle` | `[15, 12, 9]` (purple, orange, blue) |
| `timer_budget` | 80 |
| `solution_clicks` | `[(0, 0), (2, 0), (2, 0)]` -- click col 0 top once, col 2 top twice |

Sprites: bg, 12 tiles, indicator, 3 swatches at (29,5), (29,7), (29,9).

#### Level 4: "diag" -- Diagonal

| Field | Value |
|-------|-------|
| Grid | 4 cols x 4 rows, origin (6, 6) |
| `effect_pattern` | `[[1,0,0],[0,1,0],[0,0,1]]` |
| `color_cycle` | `[14, 8]` (green, red) |
| `timer_budget` | 96 |
| `solution_clicks` | `[(0, 0), (3, 3)]` -- click top-left and bottom-right corners |

Sprites: bg, 16 tiles, indicator, 2 swatches.

#### Level 5: "full" -- Full 3x3

| Field | Value |
|-------|-------|
| Grid | 4 cols x 4 rows, origin (6, 6) |
| `effect_pattern` | `[[1,1,1],[1,1,1],[1,1,1]]` |
| `color_cycle` | `[9, 11, 8]` (blue, yellow, red) |
| `timer_budget` | 128 |
| `solution_clicks` | `[(1, 1)]` -- click tile at index (1,1) |

Sprites: bg, 16 tiles, indicator, 3 swatches.

---

### TimerBar Class

Identical to CT01's `TimerBar`. Renders 1px bar on row 63. `tick()` decrements and returns False when expired. `reset(new_budget)` resets to full.

### Ct03 Class

#### `__init__(self)`

1. Declare per-level state variables (before super): `color_cycle`, `effect_pattern`, `tile_sprites`, `constraint_sprites`
2. Create `self.timer = TimerBar(levels[0].get_data("timer_budget"), self)`
3. Call `super().__init__("ct03", levels, Camera(0, 0, 16, 16, BACKGROUND_COLOR, PADDING_COLOR, [self.timer]))`
4. Set `self.available_actions = [6]`

#### `on_set_level(self, level)`

This is where constraints and minimap are **generated** (CT03's best idea). Steps:

1. Read `color_cycle`, `effect_pattern`, `timer_budget`, `solution_clicks` from level data
2. Reset timer with new budget
3. Collect tile sprites by tag `"tile"`, store in `self.tile_sprites`
4. Remap all tiles to `color_cycle[0]` using `color_remap`
5. Remap swatches to show available colors

**Generate target state:**

6. Build a position-to-tile lookup: `{(tile.x, tile.y): tile for tile in self.tile_sprites}`
7. Build sorted unique x-coords and y-coords from tile positions -> `xs`, `ys`
8. Create a cycle-index dict: `target_indices = {(t.x, t.y): 0 for t in self.tile_sprites}`
9. For each `(col_idx, row_idx)` in `solution_clicks`:
   - Look up the clicked tile position: `(xs[col_idx], ys[row_idx])`
   - For each active cell in `effect_pattern`:
     - Compute neighbor position using NEIGHBOR_OFFSETS and TILE_SPACING
     - If a tile exists there: `target_indices[(nx, ny)] = (target_indices[(nx, ny)] + 1) % len(color_cycle)`

**Generate constraint sprites and add to level:**

10. For each tile `t`:
    - `target_color = color_cycle[target_indices[(t.x, t.y)]]`
    - Build a 3x3 pixel array:
      - Center `[1][1]` = `target_color`
      - For each of 8 surrounding cells: look up the neighbor tile at the offset position
        - If neighbor exists: `0` if neighbor's target color == target_color, else `NOMATCH_INDICATOR`
        - If no neighbor: `NOMATCH_INDICATOR`
    - Create a Sprite with these pixels, positioned at `(t.x, t.y)`, `tags=["cst"]`, `visible=True`, `collidable=False`
    - Add to level via `self.current_level.add_sprite(...)`
11. Store constraint sprites in `self.constraint_sprites`

**Generate minimap sprite and add to level:**

12. Create a numpy array of shape `(len(ys), len(xs))` filled with `BACKGROUND_COLOR`
13. For each tile position, set the corresponding cell to `color_cycle[target_indices[(tx, ty)]]`
14. Create a Sprite from this array, position at `(28, 12)`, add to level

#### `step(self)`

Same logic as CT01's `step()`:

1. If RESET: `complete_action()` and return
2. If not ACTION6: `complete_action()` and return
3. Convert screen coords to grid coords via `camera.display_to_grid`
4. If no grid pos: `complete_action()` and return (NO timer tick)
5. Find clicked tile via `get_sprite_at(gx, gy, "tile")`
6. If no tile: `complete_action()` and return (NO timer tick)
7. Apply effect pattern: for each active cell, find neighbor via `get_sprite_at`, cycle color via `color_remap`
8. Check win: if `_check_constraints()` is True, call `next_level()`, `complete_action()`, return
9. Tick timer: if `timer.tick()` returns False, call `lose()`
10. `complete_action()`

#### `_check_constraints(self)`

Same logic as CT01's `_check_constraints()` -- iterates all constraint sprites, checks center cell AND 8 neighbors. Returns True only if every rule is satisfied. Uses `get_sprite_at` for lookups.

---

### Key Differences from Current CT03

| Aspect | Current CT03 | New CT03 |
|--------|-------------|----------|
| Sprites in Level constructor | No (rebuilt in on_set_level) | Yes (tiles, bg, swatches, indicator) |
| Constraints generated | Yes | Yes (same approach, better API usage) |
| Lambdas in data | Yes (deepcopy landmine) | No (solution_clicks are plain tuples) |
| Timer on empty click | Yes (ticks) | No (matches ft09) |
| Tile lookup | Manual loop | `get_sprite_at()` |
| Color cycling | `s.pixels[:] = nxt` | `color_remap(old, new)` |
| Constraints visible | No (hidden) | Yes (visible, collidable=False) |
| Win check center cell | Skipped | Checked |
| Minimap | Yes | Yes |
| remove_all_sprites | Yes | No |

### Key Differences from CT01

| Aspect | CT01 | New CT03 |
|--------|------|----------|
| Constraint design | Manual (error-prone) | Auto-generated from solution_clicks |
| Minimap | No | Yes |
| Constraint sprite defs | ~200 lines in sprites dict | 0 lines (generated) |
| Color palette | Grayscale bg (color 4) | Purple bg (color 15), no grayscale |

---

## Reference Files

| File | Role |
|------|------|
| `games/official/ct01.py` | Reference for engine API usage, step/win-check logic, TimerBar, level structure |
| `games/official/ct03.py` | Reference for constraint generation algorithm, minimap, solution_clicks concept |
| `games/official/ft09.py` | Original game being reskinned; constraint encoding spec |
| `arcengine/base_game.py` | `set_level()` calls `camera.resize(grid_size)` then `on_set_level()` |
| `arcengine/camera.py` | `display_to_grid()`, `replace_interface()` |
| `arcengine/level.py` | `get_sprite_at()`, `get_sprites_by_tag()`, `add_sprite()`, `get_sprites()` |
| `arcengine/sprites.py` | `color_remap()`, `clone()`, `set_position()` |
| `arcengine/interfaces.py` | `RenderableUserDisplay` base class |

## Engine Gotchas (must follow)

1. **Init order**: `super().__init__()` calls `set_level(0)` -> `on_set_level()`. Declare all instance variables BEFORE `super().__init__()`.
2. **Camera resize**: `set_level()` calls `camera.resize(grid_size)`. Camera(0,0,16,16,...) with grid_size=(32,32) becomes 32x32 viewport at 2x scale.
3. **Level private attrs**: Use `level.get_sprites()` not `level.sprites` (it's `level._sprites`).
4. **FrameData fields**: `.state` (not `.game_state`), `.frame` is a list at output level.
5. **Sprite pixels**: Stored as numpy int8 arrays after init. `color_remap(old, new)` works per-sprite instance.

---

## Verification

1. **Import test**: `python -c "from games.official.ct03 import Ct03; g = Ct03(); print('OK', g.game_id)"`

2. **Registry test**: `python -c "from games import get_game; g = get_game('ct03'); print('OK')"`

3. **Solve all 6 levels** (display coords = grid_coord * 2 since camera is 32x32 at 2x):
```python
from games import get_game
from arcengine import ActionInput, GameAction

g = get_game('ct03')
# Grid positions for solution clicks, converted to display coords:
# Tile at grid (x, y) -> display (x*2, y*2)  (since 32x32 viewport, scale=2)
solutions = {
    0: [(14, 14)],                          # center of 3x3 at origin (10,10)
    1: [(14, 14)],                          # center
    2: [(14, 6), (10, 14)],                 # top-center, left of row 2
    3: [(6, 10), (14, 10), (14, 10)],       # col0-top, col2-top x2
    4: [(6, 6), (18, 18)],                  # corners
    5: [(10, 10)],                          # tile (1,1)
}
for level_idx in range(6):
    for gx, gy in solutions[level_idx]:
        r = g.perform_action(ActionInput(id=GameAction.ACTION6, data={'x': gx*2, 'y': gy*2}))
    expected = 'WIN' if level_idx == 5 else 'NOT_FINISHED'
    assert r.state.name == expected, f"Level {level_idx}: expected {expected}, got {r.state.name}"
    print(f"Level {level_idx}: OK (completed={r.levels_completed})")
print("All levels solved!")
```

4. **Timer test**: Click actual tiles 40+ times on level 0 without solving -> GAME_OVER

5. **Empty click test**: Click empty space -> no timer tick (verify timer.remaining unchanged)

6. **Existing tests**: `uv run pytest tests/` -- all 99 tests pass (ct03 is not tested by existing suite, just shouldn't break anything)
