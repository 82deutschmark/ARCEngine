# Author: Claude Haiku 4.5
# Date: 06-February-2026
# PURPOSE: ct03 - Cascade Tiles. Constraint-satisfaction puzzle with varying click-effect patterns.
#          Combines CT01's proper engine API usage and level structure with CT03's auto-generated
#          constraints from solution_clicks. Defines levels statically, generates constraints
#          dynamically in on_set_level(). Uses color 6 (pink) for "no match" indicator, purple
#          background, and timer only ticks on successful tile clicks.
#          Depends on: arcengine (ARCBaseGame, Camera, Level, Sprite, RenderableUserDisplay, GameAction)

from __future__ import annotations

import numpy as np

from arcengine import ARCBaseGame, Camera, GameAction, Level, RenderableUserDisplay, Sprite

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
BACKGROUND_COLOR = 15       # Purple
PADDING_COLOR = 15          # Purple
TILE_SPACING = 4            # Pixels between tile origins
TIMER_FILLED_COLOR = 12     # Orange
TIMER_EMPTY_COLOR = 13      # Dark Red
PATTERN_ACTIVE_COLOR = 11   # Yellow
PATTERN_INACTIVE_COLOR = 13 # Dark Red
MATCH_INDICATOR = 7         # Light Orange (constraint: neighbor MUST match target color)
NOMATCH_INDICATOR = 6       # Pink (constraint: neighbor must NOT match target color)

# Neighbor offset lookup: for each cell (row, col) in a 3x3 pattern, the (dx, dy)
# offset in tile-spacing units from the clicked tile.
NEIGHBOR_OFFSETS: list[list[tuple[int, int]]] = [
    [(-1, -1), (0, -1), (1, -1)],
    [(-1, 0), (0, 0), (1, 0)],
    [(-1, 1), (0, 1), (1, 1)],
]

# ---------------------------------------------------------------------------
# Sprite templates
# ---------------------------------------------------------------------------
sprites: dict[str, Sprite] = {
    # Clickable tile (3x3, solid green by default -- remapped per level)
    "tile": Sprite(
        pixels=[
            [14, 14, 14],
            [14, 14, 14],
            [14, 14, 14],
        ],
        name="tile",
        visible=True,
        collidable=True,
        tags=["tile"],
    ),
    # Background fill (32x32 solid purple, layer -2)
    "bg": Sprite(
        pixels=[[BACKGROUND_COLOR] * 32 for _ in range(32)],
        name="bg",
        visible=True,
        collidable=False,
        layer=-2,
    ),
    # Color swatch sprites (2x2 solid blocks, remapped per level)
    "swatch": Sprite(
        pixels=[[BACKGROUND_COLOR, BACKGROUND_COLOR], [BACKGROUND_COLOR, BACKGROUND_COLOR]],
        name="swatch",
        visible=True,
        collidable=False,
    ),
}


def _build_effect_indicator(elp: list[list[int]]) -> Sprite:
    """Build a 3x3 sprite showing which cells in the effect pattern are active."""
    pixels = [
        [PATTERN_ACTIVE_COLOR if elp[r][c] else PATTERN_INACTIVE_COLOR for c in range(3)]
        for r in range(3)
    ]
    return Sprite(pixels=pixels, name="epat", visible=True, collidable=False)


def _make_tile_grid(rows: int, cols: int, origin_x: int, origin_y: int) -> list[Sprite]:
    """Create a grid of tile clones at TILE_SPACING intervals."""
    tiles = []
    for r in range(rows):
        for c in range(cols):
            tile = sprites["tile"].clone().set_position(
                origin_x + c * TILE_SPACING,
                origin_y + r * TILE_SPACING,
            )
            tiles.append(tile)
    return tiles


# ---------------------------------------------------------------------------
# Level definitions
# ---------------------------------------------------------------------------

# Level 0: "intro" -- center-only click effect
_l0_elp = [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
_l0_tiles = _make_tile_grid(3, 3, 10, 10)
levels = [
    Level(
        sprites=[
            sprites["bg"].clone().set_position(0, 0),
            *_l0_tiles,
            _build_effect_indicator(_l0_elp).set_position(28, 1),
            sprites["swatch"].clone().set_position(29, 5),
            sprites["swatch"].clone().set_position(29, 7),
        ],
        grid_size=(32, 32),
        data={
            "timer_budget": 40,
            "color_cycle": [14, 8],
            "effect_pattern": _l0_elp,
            "solution_clicks": [(1, 1)],
        },
        name="intro",
    ),
    # Level 1: "cross" -- plus-shape click effect
    Level(
        sprites=[
            sprites["bg"].clone().set_position(0, 0),
            *_make_tile_grid(3, 3, 10, 10),
            _build_effect_indicator([[0, 1, 0], [1, 1, 1], [0, 1, 0]]).set_position(28, 1),
            sprites["swatch"].clone().set_position(29, 5),
            sprites["swatch"].clone().set_position(29, 7),
        ],
        grid_size=(32, 32),
        data={
            "timer_budget": 48,
            "color_cycle": [9, 12],
            "effect_pattern": [[0, 1, 0], [1, 1, 1], [0, 1, 0]],
            "solution_clicks": [(1, 1)],
        },
        name="cross",
    ),
    # Level 2: "hline" -- horizontal line click effect
    Level(
        sprites=[
            sprites["bg"].clone().set_position(0, 0),
            *_make_tile_grid(4, 3, 10, 6),
            _build_effect_indicator([[0, 0, 0], [1, 1, 1], [0, 0, 0]]).set_position(28, 1),
            sprites["swatch"].clone().set_position(29, 5),
            sprites["swatch"].clone().set_position(29, 7),
        ],
        grid_size=(32, 32),
        data={
            "timer_budget": 64,
            "color_cycle": [8, 11],
            "effect_pattern": [[0, 0, 0], [1, 1, 1], [0, 0, 0]],
            "solution_clicks": [(1, 0), (0, 2)],
        },
        name="hline",
    ),
    # Level 3: "vline" -- vertical line click effect
    Level(
        sprites=[
            sprites["bg"].clone().set_position(0, 0),
            *_make_tile_grid(3, 4, 6, 10),
            _build_effect_indicator([[0, 1, 0], [0, 1, 0], [0, 1, 0]]).set_position(28, 1),
            sprites["swatch"].clone().set_position(29, 5),
            sprites["swatch"].clone().set_position(29, 7),
            sprites["swatch"].clone().set_position(29, 9),
        ],
        grid_size=(32, 32),
        data={
            "timer_budget": 80,
            "color_cycle": [15, 12, 9],
            "effect_pattern": [[0, 1, 0], [0, 1, 0], [0, 1, 0]],
            "solution_clicks": [(0, 0), (2, 0), (2, 0)],
        },
        name="vline",
    ),
    # Level 4: "diag" -- diagonal click effect
    Level(
        sprites=[
            sprites["bg"].clone().set_position(0, 0),
            *_make_tile_grid(4, 4, 6, 6),
            _build_effect_indicator([[1, 0, 0], [0, 1, 0], [0, 0, 1]]).set_position(28, 1),
            sprites["swatch"].clone().set_position(29, 5),
            sprites["swatch"].clone().set_position(29, 7),
        ],
        grid_size=(32, 32),
        data={
            "timer_budget": 96,
            "color_cycle": [14, 8],
            "effect_pattern": [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
            "solution_clicks": [(0, 0), (3, 3)],
        },
        name="diag",
    ),
    # Level 5: "full" -- full 3x3 area click effect
    Level(
        sprites=[
            sprites["bg"].clone().set_position(0, 0),
            *_make_tile_grid(4, 4, 6, 6),
            _build_effect_indicator([[1, 1, 1], [1, 1, 1], [1, 1, 1]]).set_position(28, 1),
            sprites["swatch"].clone().set_position(29, 5),
            sprites["swatch"].clone().set_position(29, 7),
            sprites["swatch"].clone().set_position(29, 9),
        ],
        grid_size=(32, 32),
        data={
            "timer_budget": 128,
            "color_cycle": [9, 11, 8],
            "effect_pattern": [[1, 1, 1], [1, 1, 1], [1, 1, 1]],
            "solution_clicks": [(1, 1)],
        },
        name="full",
    ),
    # Level 6: "corners" -- four diagonal neighbors affected
    Level(
        sprites=[
            sprites["bg"].clone().set_position(0, 0),
            *_make_tile_grid(4, 4, 6, 6),
            _build_effect_indicator([[1, 0, 1], [0, 0, 0], [1, 0, 1]]).set_position(28, 1),
            sprites["swatch"].clone().set_position(29, 5),
            sprites["swatch"].clone().set_position(29, 7),
        ],
        grid_size=(32, 32),
        data={
            "timer_budget": 96,
            "color_cycle": [10, 13],
            "effect_pattern": [[1, 0, 1], [0, 0, 0], [1, 0, 1]],
            "solution_clicks": [(1, 1), (2, 2)],
        },
        name="corners",
    ),
    # Level 7: "antidiag" -- anti-diagonal (upper-right to lower-left)
    Level(
        sprites=[
            sprites["bg"].clone().set_position(0, 0),
            *_make_tile_grid(4, 4, 6, 6),
            _build_effect_indicator([[0, 0, 1], [0, 1, 0], [1, 0, 0]]).set_position(28, 1),
            sprites["swatch"].clone().set_position(29, 5),
            sprites["swatch"].clone().set_position(29, 7),
            sprites["swatch"].clone().set_position(29, 9),
        ],
        grid_size=(32, 32),
        data={
            "timer_budget": 112,
            "color_cycle": [12, 10, 15],
            "effect_pattern": [[0, 0, 1], [0, 1, 0], [1, 0, 0]],
            "solution_clicks": [(1, 1), (2, 2)],
        },
        name="antidiag",
    ),
    # Level 8: "lshape" -- L-shaped effect (left column + bottom row)
    Level(
        sprites=[
            sprites["bg"].clone().set_position(0, 0),
            *_make_tile_grid(4, 4, 6, 6),
            _build_effect_indicator([[1, 0, 0], [1, 0, 0], [1, 1, 1]]).set_position(28, 1),
            sprites["swatch"].clone().set_position(29, 5),
            sprites["swatch"].clone().set_position(29, 7),
            sprites["swatch"].clone().set_position(29, 9),
        ],
        grid_size=(32, 32),
        data={
            "timer_budget": 128,
            "color_cycle": [11, 8, 14],
            "effect_pattern": [[1, 0, 0], [1, 0, 0], [1, 1, 1]],
            "solution_clicks": [(2, 1), (1, 2)],
        },
        name="lshape",
    ),
    # Level 9: "tshape" -- T-shaped effect (top row + center column down)
    Level(
        sprites=[
            sprites["bg"].clone().set_position(0, 0),
            *_make_tile_grid(5, 5, 4, 4),
            _build_effect_indicator([[1, 1, 1], [0, 1, 0], [0, 1, 0]]).set_position(28, 1),
            sprites["swatch"].clone().set_position(29, 5),
            sprites["swatch"].clone().set_position(29, 7),
            sprites["swatch"].clone().set_position(29, 9),
        ],
        grid_size=(32, 32),
        data={
            "timer_budget": 160,
            "color_cycle": [15, 8, 10],
            "effect_pattern": [[1, 1, 1], [0, 1, 0], [0, 1, 0]],
            "solution_clicks": [(2, 2), (1, 3)],
        },
        name="tshape",
    ),
]


# ---------------------------------------------------------------------------
# Timer HUD
# ---------------------------------------------------------------------------
class TimerBar(RenderableUserDisplay):
    """Renders a 1-pixel-tall progress bar on row 63 of the 64x64 frame.

    Filled portion = orange (12), empty = dark red (13). Identical behavior to
    CT01's TimerBar.
    """

    def __init__(self, budget: int, game: Ct03) -> None:
        self.budget = budget
        self.remaining = budget
        self._game = game

    def tick(self) -> bool:
        """Decrement the timer by one step. Returns False when expired."""
        if self.remaining > 0:
            self.remaining -= 1
        return self.remaining > 0

    def reset(self, new_budget: int | None = None) -> None:
        """Reset timer to full. Optionally change the budget."""
        if new_budget is not None:
            self.budget = new_budget
        self.remaining = self.budget

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        if self.budget == 0:
            return frame
        fraction = self.remaining / self.budget
        filled_pixels = round(64 * fraction)
        for x in range(64):
            frame[63, x] = TIMER_FILLED_COLOR if x < filled_pixels else TIMER_EMPTY_COLOR
        return frame


# ---------------------------------------------------------------------------
# Game class
# ---------------------------------------------------------------------------
class Ct03(ARCBaseGame):
    """Cascade Tiles -- constraint-satisfaction puzzle with varying click-effect patterns.

    Combines CT01's engine API usage with CT03's auto-generated constraints.
    """

    def __init__(self) -> None:
        initial_budget = levels[0].get_data("timer_budget") or 0
        self.timer = TimerBar(initial_budget, self)

        # Per-level state (populated in on_set_level, must be declared before super().__init__
        # because set_level(0) is called during parent init)
        self.color_cycle: list[int] = []
        self.effect_pattern: list[list[int]] = []
        self.tile_sprites: list[Sprite] = []
        self.constraint_sprites: list[Sprite] = []

        super().__init__("ct03", levels, Camera(0, 0, 16, 16, BACKGROUND_COLOR, PADDING_COLOR, [self.timer]))
        self.available_actions = [6]

    # ---- Level setup ----

    def on_set_level(self, level: Level) -> None:
        """Called by the engine whenever the active level changes (including init and reset).

        Generates constraint sprites and minimap dynamically based on solution_clicks.
        """
        # Read level data
        self.color_cycle = level.get_data("color_cycle") or [14, 8]
        self.effect_pattern = level.get_data("effect_pattern") or [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
        solution_clicks = level.get_data("solution_clicks") or []
        budget = level.get_data("timer_budget") or 0
        self.timer.reset(budget)

        # Collect sprites by tag
        self.tile_sprites = self.current_level.get_sprites_by_tag("tile")
        self.constraint_sprites = []

        # Remap all tiles to the first color in this level's cycle
        first_color = self.color_cycle[0]
        for tile in self.tile_sprites:
            tile.color_remap(tile.pixels[0][0], first_color)

        # Remap color swatches to show available colors
        swatches = [
            s for s in self.current_level.get_sprites()
            if s.name.startswith("swatch")
        ]
        swatches.sort(key=lambda s: (s.x, s.y))
        for idx, swatch in enumerate(swatches):
            if idx < len(self.color_cycle):
                swatch.color_remap(swatch.pixels[0][0], self.color_cycle[idx])

        # --- Generate target state by simulating solution clicks ---

        # Build position-to-tile lookup and sorted coordinate lists
        pos_to_tile = {(t.x, t.y): t for t in self.tile_sprites}
        xs = sorted({t.x for t in self.tile_sprites})
        ys = sorted({t.y for t in self.tile_sprites})

        # Initialize target indices for each tile (0 = first color in cycle)
        target_indices = {(t.x, t.y): 0 for t in self.tile_sprites}

        # Simulate each solution click
        for col_idx, row_idx in solution_clicks:
            if col_idx < 0 or col_idx >= len(xs) or row_idx < 0 or row_idx >= len(ys):
                continue

            clicked_x, clicked_y = xs[col_idx], ys[row_idx]
            clicked_tile = pos_to_tile.get((clicked_x, clicked_y))
            if not clicked_tile:
                continue

            # Apply effect pattern: for each active cell, cycle the corresponding neighbor
            for row in range(3):
                for col in range(3):
                    if self.effect_pattern[row][col] == 1:
                        dx, dy = NEIGHBOR_OFFSETS[row][col]
                        neighbor_x = clicked_x + dx * TILE_SPACING
                        neighbor_y = clicked_y + dy * TILE_SPACING
                        neighbor = pos_to_tile.get((neighbor_x, neighbor_y))
                        if neighbor:
                            target_indices[(neighbor_x, neighbor_y)] = (
                                target_indices[(neighbor_x, neighbor_y)] + 1
                            ) % len(self.color_cycle)

        # --- Generate constraint sprites ---

        for tile in self.tile_sprites:
            target_color = self.color_cycle[target_indices[(tile.x, tile.y)]]

            # Build 3x3 constraint pixel array (filled with MATCH_INDICATOR by default)
            constraint_pixels = np.full((3, 3), MATCH_INDICATOR, dtype=np.int8)
            constraint_pixels[1, 1] = target_color

            for row in range(3):
                for col in range(3):
                    if row == 1 and col == 1:
                        continue

                    dx, dy = NEIGHBOR_OFFSETS[row][col]
                    neighbor_x = tile.x + dx * TILE_SPACING
                    neighbor_y = tile.y + dy * TILE_SPACING
                    neighbor = pos_to_tile.get((neighbor_x, neighbor_y))

                    if neighbor:
                        neighbor_target_color = self.color_cycle[target_indices[(neighbor_x, neighbor_y)]]
                        constraint_pixels[row, col] = MATCH_INDICATOR if neighbor_target_color == target_color else NOMATCH_INDICATOR
                    else:
                        constraint_pixels[row, col] = NOMATCH_INDICATOR

            # Create constraint sprite
            constraint_sprite = Sprite(
                pixels=constraint_pixels,
                x=tile.x,
                y=tile.y,
                name=f"cst_{tile.name}",
                tags=["cst"],
                visible=True,
                collidable=False,
            )
            self.current_level.add_sprite(constraint_sprite)
            self.constraint_sprites.append(constraint_sprite)

        # --- Generate minimap sprite ---

        minimap_pixels = np.full((len(ys), len(xs)), BACKGROUND_COLOR, dtype=np.int8)
        for row_idx, y in enumerate(ys):
            for col_idx, x in enumerate(xs):
                tile = pos_to_tile.get((x, y))
                if tile:
                    minimap_pixels[row_idx, col_idx] = self.color_cycle[target_indices[(x, y)]]

        minimap_sprite = Sprite(
            pixels=minimap_pixels,
            x=28,
            y=12,
            name="minimap",
            visible=True,
            collidable=False,
        )
        self.current_level.add_sprite(minimap_sprite)

    # ---- Main game loop ----

    def step(self) -> None:
        # RESET is handled automatically by the engine; just complete the action.
        if self.action.id == GameAction.RESET:
            self.complete_action()
            return

        # Only respond to ACTION6 (click)
        if self.action.id != GameAction.ACTION6:
            self.complete_action()
            return

        # Convert screen coordinates to grid coordinates
        click_x = self.action.data.get("x", 0)
        click_y = self.action.data.get("y", 0)
        grid_pos = self.camera.display_to_grid(click_x, click_y)

        if not grid_pos:
            self.complete_action()
            return

        gx, gy = grid_pos

        # Find the clicked tile
        clicked_tile = self.current_level.get_sprite_at(gx, gy, "tile")
        if not clicked_tile:
            self.complete_action()
            return

        # Apply the effect pattern: for each active cell in the 3x3 pattern,
        # find the tile at the corresponding offset and cycle its color.
        for row in range(3):
            for col in range(3):
                if self.effect_pattern[row][col] == 1:
                    dx, dy = NEIGHBOR_OFFSETS[row][col]
                    target_x = clicked_tile.x + dx * TILE_SPACING
                    target_y = clicked_tile.y + dy * TILE_SPACING
                    neighbor = self.current_level.get_sprite_at(target_x, target_y, "tile")
                    if neighbor:
                        current_color = neighbor.pixels[1][1]
                        current_idx = self.color_cycle.index(current_color)
                        next_color = self.color_cycle[(current_idx + 1) % len(self.color_cycle)]
                        neighbor.color_remap(current_color, next_color)

        # Check win condition
        if self._check_constraints():
            self.next_level()
            self.complete_action()
            return

        # Tick the timer; lose if expired
        if not self.timer.tick():
            self.lose()

        self.complete_action()

    # ---- Win-check logic ----

    def _check_constraints(self) -> bool:
        """Evaluate all constraint sprites. Returns True if every constraint is satisfied.

        Each constraint sprite (tag 'cst') encodes:
        - Center pixel [1][1] = target color for the tile at this position
        - Each of the 8 surrounding pixels encodes a rule for the tile at the
          corresponding 4px offset:
            - MATCH_INDICATOR (7) means the neighbor's center color MUST equal the target
            - NOMATCH_INDICATOR (6) means the neighbor's center color MUST NOT equal the target
        - If no tile exists at an offset position, that rule is skipped.
        """
        for cst in self.constraint_sprites:
            target_color = cst.pixels[1][1]

            for row in range(3):
                for col in range(3):
                    if row == 1 and col == 1:
                        # Center cell: the tile at this position must be the target color
                        tile_here = self.current_level.get_sprite_at(cst.x, cst.y, "tile")
                        if tile_here and tile_here.pixels[1][1] != target_color:
                            return False
                        continue

                    # Surrounding cell: check neighbor rule
                    must_match = cst.pixels[row][col] == MATCH_INDICATOR
                    dx, dy = NEIGHBOR_OFFSETS[row][col]
                    neighbor_x = cst.x + dx * TILE_SPACING
                    neighbor_y = cst.y + dy * TILE_SPACING
                    neighbor = self.current_level.get_sprite_at(neighbor_x, neighbor_y, "tile")

                    if not neighbor:
                        continue  # No tile at this offset -- rule is vacuously satisfied

                    neighbor_color = neighbor.pixels[1][1]
                    if must_match and neighbor_color != target_color:
                        return False
                    if not must_match and neighbor_color == target_color:
                        return False

        return True
