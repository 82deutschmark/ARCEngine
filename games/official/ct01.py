# Author: Claude Opus 4.6
# Date: 06-February-2026
# PURPOSE: ct01 - Cascade Tiles. A constraint-satisfaction puzzle reskinning ft09's mechanics.
#          The central twist: each level uses a different click-effect pattern (elp), so the
#          player must deduce which neighbors are affected by each click. Same constraint encoding,
#          color cycling, and timer HUD as ft09, but with clean names and no obfuscation.
#          Depends on: arcengine (ARCBaseGame, Camera, Level, Sprite, RenderableUserDisplay, GameAction)

from __future__ import annotations

import numpy as np

from arcengine import ARCBaseGame, Camera, GameAction, Level, RenderableUserDisplay, Sprite

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
BACKGROUND_COLOR = 4  # Darker Gray
PADDING_COLOR = 4  # Darker Gray
TILE_SPACING = 4  # Pixels between tile origins on the 32x32 grid
TIMER_FILLED_COLOR = 12  # Orange
TIMER_EMPTY_COLOR = 11  # Yellow
PATTERN_ACTIVE_COLOR = 11  # Yellow (active cell in effect-pattern indicator)
PATTERN_INACTIVE_COLOR = 3  # Dark Gray (inactive cell in effect-pattern indicator)

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
    # Background fill (32x32 solid darker-gray, layer -2)
    "bg": Sprite(
        pixels=[[BACKGROUND_COLOR] * 32 for _ in range(32)],
        name="bg",
        visible=True,
        collidable=False,
        layer=-2,
    ),
    # ---------- Level 0 constraints ----------
    # Center tile (14,14) must be red(8). All 8 neighbors must NOT be red.
    "c0_center": Sprite(
        pixels=[
            [2, 2, 2],
            [2, 8, 2],
            [2, 2, 2],
        ],
        name="c0_center",
        visible=True,
        collidable=True,
        tags=["cst"],
    ),
    # ---------- Level 1 constraints ----------
    # Center tile (14,14) must be orange(12). Cardinal neighbors must match (0), corners must not (2).
    "c1_center": Sprite(
        pixels=[
            [2, 0, 2],
            [0, 12, 0],
            [2, 0, 2],
        ],
        name="c1_center",
        visible=True,
        collidable=True,
        tags=["cst"],
    ),
    # Top-left tile (10,10) must stay blue(9). All neighbors must NOT be blue.
    "c1_topleft": Sprite(
        pixels=[
            [2, 2, 2],
            [2, 9, 2],
            [2, 2, 2],
        ],
        name="c1_topleft",
        visible=True,
        collidable=True,
        tags=["cst"],
    ),
    # ---------- Level 2 constraints ----------
    # Top-center tile (14,6) must be yellow(11). W and E neighbors must match.
    "c2_topcenter": Sprite(
        pixels=[
            [2, 2, 2],
            [0, 11, 0],
            [2, 2, 2],
        ],
        name="c2_topcenter",
        visible=True,
        collidable=True,
        tags=["cst"],
    ),
    # Mid-left tile (10,14) must be yellow(11). E neighbor must match.
    "c2_midleft": Sprite(
        pixels=[
            [2, 2, 2],
            [2, 11, 0],
            [2, 2, 2],
        ],
        name="c2_midleft",
        visible=True,
        collidable=True,
        tags=["cst"],
    ),
    # ---------- Level 3 constraints ----------
    # Tile (6,10) must be orange(12). S neighbor must match.
    "c3_topleft": Sprite(
        pixels=[
            [2, 2, 2],
            [2, 12, 2],
            [2, 0, 2],
        ],
        name="c3_topleft",
        visible=True,
        collidable=True,
        tags=["cst"],
    ),
    # Tile (14,10) must be blue(9). S neighbor must match.
    "c3_topmid": Sprite(
        pixels=[
            [2, 2, 2],
            [2, 9, 2],
            [2, 0, 2],
        ],
        name="c3_topmid",
        visible=True,
        collidable=True,
        tags=["cst"],
    ),
    # Tile (6,18) must stay purple(15). E and NE neighbors must match (both stay 15).
    "c3_botleft": Sprite(
        pixels=[
            [2, 2, 0],
            [2, 15, 0],
            [2, 2, 2],
        ],
        name="c3_botleft",
        visible=True,
        collidable=True,
        tags=["cst"],
    ),
    # ---------- Level 4 constraints ----------
    # Tile (6,6) must be red(8). SE must match (diagonal neighbor also toggled).
    "c4_diag00": Sprite(
        pixels=[
            [2, 2, 2],
            [2, 8, 2],
            [2, 2, 0],
        ],
        name="c4_diag00",
        visible=True,
        collidable=True,
        tags=["cst"],
    ),
    # Tile (10,10) must be red(8). NW and SE must match (both on the diagonal).
    "c4_diag11": Sprite(
        pixels=[
            [0, 2, 2],
            [2, 8, 2],
            [2, 2, 0],
        ],
        name="c4_diag11",
        visible=True,
        collidable=True,
        tags=["cst"],
    ),
    # Tile (14,14) must be red(8). NW must match, SE must match.
    "c4_diag22": Sprite(
        pixels=[
            [0, 2, 2],
            [2, 8, 2],
            [2, 2, 0],
        ],
        name="c4_diag22",
        visible=True,
        collidable=True,
        tags=["cst"],
    ),
    # Tile (18,18) must be red(8). NW must match.
    "c4_diag33": Sprite(
        pixels=[
            [0, 2, 2],
            [2, 8, 2],
            [2, 2, 2],
        ],
        name="c4_diag33",
        visible=True,
        collidable=True,
        tags=["cst"],
    ),
    # ---------- Level 5 constraints ----------
    # Tile (6,6) must be yellow(11). E and S and SE must match.
    "c5_corner": Sprite(
        pixels=[
            [2, 2, 2],
            [2, 11, 0],
            [2, 0, 0],
        ],
        name="c5_corner",
        visible=True,
        collidable=True,
        tags=["cst"],
    ),
    # Tile (10,10) must be yellow(11). All 8 neighbors must match.
    "c5_inner": Sprite(
        pixels=[
            [0, 0, 0],
            [0, 11, 0],
            [0, 0, 0],
        ],
        name="c5_inner",
        visible=True,
        collidable=True,
        tags=["cst"],
    ),
    # Tile (14,14) must be yellow(11). NW/N/W must match, NE/E/SW/S/SE must NOT.
    "c5_edge": Sprite(
        pixels=[
            [0, 0, 2],
            [0, 11, 2],
            [2, 2, 2],
        ],
        name="c5_edge",
        visible=True,
        collidable=True,
        tags=["cst"],
    ),
    # Tile (18,18) must stay blue(9). N and W must match (both are blue).
    "c5_farcrn": Sprite(
        pixels=[
            [2, 0, 2],
            [0, 9, 2],
            [2, 2, 2],
        ],
        name="c5_farcrn",
        visible=True,
        collidable=True,
        tags=["cst"],
    ),
    # ---------- Color swatch sprites (2x2 solid blocks) ----------
    "swatch_0": Sprite(pixels=[[0, 0], [0, 0]], name="swatch_0", visible=True, collidable=False),
    "swatch_1": Sprite(pixels=[[0, 0], [0, 0]], name="swatch_1", visible=True, collidable=False),
    "swatch_2": Sprite(pixels=[[0, 0], [0, 0]], name="swatch_2", visible=True, collidable=False),
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
            sprites["c0_center"].clone().set_position(14, 14),
            _build_effect_indicator(_l0_elp).set_position(28, 1),
            sprites["swatch_0"].clone().set_position(29, 5),
            sprites["swatch_1"].clone().set_position(29, 7),
        ],
        grid_size=(32, 32),
        data={
            "timer_budget": 40,
            "color_cycle": [14, 8],
            "effect_pattern": _l0_elp,
        },
        name="intro",
    ),
    # Level 1: "cross" -- plus-shape click effect
    Level(
        sprites=[
            sprites["bg"].clone().set_position(0, 0),
            *_make_tile_grid(3, 3, 10, 10),
            sprites["c1_center"].clone().set_position(14, 14),
            sprites["c1_topleft"].clone().set_position(10, 10),
            _build_effect_indicator([[0, 1, 0], [1, 1, 1], [0, 1, 0]]).set_position(28, 1),
            sprites["swatch_0"].clone().set_position(29, 5),
            sprites["swatch_1"].clone().set_position(29, 7),
        ],
        grid_size=(32, 32),
        data={
            "timer_budget": 48,
            "color_cycle": [9, 12],
            "effect_pattern": [[0, 1, 0], [1, 1, 1], [0, 1, 0]],
        },
        name="cross",
    ),
    # Level 2: "hline" -- horizontal line click effect
    Level(
        sprites=[
            sprites["bg"].clone().set_position(0, 0),
            *_make_tile_grid(4, 3, 10, 6),
            sprites["c2_topcenter"].clone().set_position(14, 6),
            sprites["c2_midleft"].clone().set_position(10, 14),
            _build_effect_indicator([[0, 0, 0], [1, 1, 1], [0, 0, 0]]).set_position(28, 1),
            sprites["swatch_0"].clone().set_position(29, 5),
            sprites["swatch_1"].clone().set_position(29, 7),
        ],
        grid_size=(32, 32),
        data={
            "timer_budget": 64,
            "color_cycle": [8, 11],
            "effect_pattern": [[0, 0, 0], [1, 1, 1], [0, 0, 0]],
        },
        name="hline",
    ),
    # Level 3: "vline" -- vertical line click effect
    Level(
        sprites=[
            sprites["bg"].clone().set_position(0, 0),
            *_make_tile_grid(3, 4, 6, 10),
            sprites["c3_topleft"].clone().set_position(6, 10),
            sprites["c3_topmid"].clone().set_position(14, 10),
            sprites["c3_botleft"].clone().set_position(6, 18),
            _build_effect_indicator([[0, 1, 0], [0, 1, 0], [0, 1, 0]]).set_position(28, 1),
            sprites["swatch_0"].clone().set_position(29, 5),
            sprites["swatch_1"].clone().set_position(29, 7),
            sprites["swatch_2"].clone().set_position(29, 9),
        ],
        grid_size=(32, 32),
        data={
            "timer_budget": 80,
            "color_cycle": [15, 12, 9],
            "effect_pattern": [[0, 1, 0], [0, 1, 0], [0, 1, 0]],
        },
        name="vline",
    ),
    # Level 4: "diag" -- diagonal click effect
    Level(
        sprites=[
            sprites["bg"].clone().set_position(0, 0),
            *_make_tile_grid(4, 4, 6, 6),
            sprites["c4_diag00"].clone().set_position(6, 6),
            sprites["c4_diag11"].clone().set_position(10, 10),
            sprites["c4_diag22"].clone().set_position(14, 14),
            sprites["c4_diag33"].clone().set_position(18, 18),
            _build_effect_indicator([[1, 0, 0], [0, 1, 0], [0, 0, 1]]).set_position(28, 1),
            sprites["swatch_0"].clone().set_position(29, 5),
            sprites["swatch_1"].clone().set_position(29, 7),
        ],
        grid_size=(32, 32),
        data={
            "timer_budget": 96,
            "color_cycle": [14, 8],
            "effect_pattern": [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
        },
        name="diag",
    ),
    # Level 5: "full" -- full 3x3 area click effect
    Level(
        sprites=[
            sprites["bg"].clone().set_position(0, 0),
            *_make_tile_grid(4, 4, 6, 6),
            sprites["c5_corner"].clone().set_position(6, 6),
            sprites["c5_inner"].clone().set_position(10, 10),
            sprites["c5_edge"].clone().set_position(14, 14),
            sprites["c5_farcrn"].clone().set_position(18, 18),
            _build_effect_indicator([[1, 1, 1], [1, 1, 1], [1, 1, 1]]).set_position(28, 1),
            sprites["swatch_0"].clone().set_position(29, 5),
            sprites["swatch_1"].clone().set_position(29, 7),
            sprites["swatch_2"].clone().set_position(29, 9),
        ],
        grid_size=(32, 32),
        data={
            "timer_budget": 128,
            "color_cycle": [9, 11, 8],
            "effect_pattern": [[1, 1, 1], [1, 1, 1], [1, 1, 1]],
        },
        name="full",
    ),
]


# ---------------------------------------------------------------------------
# Timer HUD
# ---------------------------------------------------------------------------
class TimerBar(RenderableUserDisplay):
    """Renders a 1-pixel-tall progress bar on row 63 of the 64x64 frame.

    Filled portion = orange (12), empty = yellow (11). Identical behavior to
    ft09's ``sve`` class, with readable names.
    """

    def __init__(self, budget: int, game: Ct01) -> None:
        self.budget = budget
        self.remaining = budget
        self._game = game

    def tick(self) -> bool:
        """Decrement the timer by one step. Returns False when time is up."""
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
class Ct01(ARCBaseGame):
    """Cascade Tiles -- constraint-satisfaction puzzle with varying click-effect patterns."""

    def __init__(self) -> None:
        initial_budget = levels[0].get_data("timer_budget") or 0
        self.timer = TimerBar(initial_budget, self)

        # Per-level state (populated in on_set_level, must be declared before super().__init__
        # because set_level(0) is called during parent init)
        self.color_cycle: list[int] = []
        self.effect_pattern: list[list[int]] = []
        self.tile_sprites: list[Sprite] = []
        self.constraint_sprites: list[Sprite] = []

        super().__init__("ct01", levels, Camera(0, 0, 16, 16, 4, 4, [self.timer]))
        self.available_actions = [6]

    # ---- Level setup ----

    def on_set_level(self, level: Level) -> None:
        """Called by the engine whenever the active level changes (including init and reset)."""
        # Read level data
        self.color_cycle = level.get_data("color_cycle") or [14, 8]
        self.effect_pattern = level.get_data("effect_pattern") or [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
        budget = level.get_data("timer_budget") or 0
        self.timer.reset(budget)

        # Collect sprites by tag
        self.tile_sprites = self.current_level.get_sprites_by_tag("tile")
        self.constraint_sprites = self.current_level.get_sprites_by_tag("cst")

        # Remap all tiles to the first color in this level's cycle
        first_color = self.color_cycle[0]
        for tile in self.tile_sprites:
            tile.color_remap(tile.pixels[0][0], first_color)

        # Remap color swatches to show available colors
        swatches = [
            s for s in self.current_level.get_sprites()
            if s.name.startswith("swatch_")
        ]
        swatches.sort(key=lambda s: s.name)
        for idx, swatch in enumerate(swatches):
            if idx < len(self.color_cycle):
                swatch.color_remap(swatch.pixels[0][0], self.color_cycle[idx])

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
            - 0 means the neighbor's center color MUST equal the target
            - non-0 means the neighbor's center color MUST NOT equal the target
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
                    must_match = cst.pixels[row][col] == 0
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
