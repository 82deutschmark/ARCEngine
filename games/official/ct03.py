
# Author: Cascade (ChatGPT)
# Date: 2026-02-06
# PURPOSE: Implementation of 'Cascade Tiles' (ct03), a reskin of ft09 with varying click patterns and no grayscale colors.
#          Uses colors 6-15 only. Each level introduces a different click-effect pattern (center, cross, hline, vline, diag, full).
# SRP/DRY check: Pass - Reuses ARCEngine core, distinct game logic.

import numpy as np
from arcengine import ARCBaseGame, Camera, Level, RenderableUserDisplay, Sprite

# Color palette constants (strictly colors 6-15, no grayscale 0-5)
BACKGROUND_COLOR = 15  # Purple
PADDING_COLOR = 15     # Purple
ACTIVE_PATTERN_COLOR = 11  # Yellow
INACTIVE_PATTERN_COLOR = 13  # Dark Red
TIMER_FULL_COLOR = 12  # Orange
TIMER_EMPTY_COLOR = 13  # Dark Red
CONSTRAINT_NOMATCH_COLOR = 13  # Dark Red


class TimerBar(RenderableUserDisplay):
    """Manages the timer budget and renders a 1-pixel bar at the bottom of the 64x64 output."""

    def __init__(self, budget: int) -> None:
        self.budget = budget
        self.remaining = budget

    def tick(self) -> bool:
        """Decrements timer. Returns False if expired."""
        if self.budget <= 0:
            return True
        self.remaining -= 1
        return self.remaining > 0

    def reset(self) -> None:
        self.remaining = self.budget

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        """Draw the timer bar on the bottom row of the 64x64 frame."""
        if self.budget <= 0:
            return frame

        fill_width = round(64 * (self.remaining / self.budget)) if self.remaining > 0 else 0
        for x in range(64):
            frame[63, x] = TIMER_FULL_COLOR if x < fill_width else TIMER_EMPTY_COLOR
        return frame


class Ct03(ARCBaseGame):
    """Cascade Tiles - constraint-satisfaction puzzle with varying click-effect patterns."""

    def __init__(self) -> None:
        self.timer: TimerBar | None = None
        self.tile_sprites: list[Sprite] = []
        self.current_elp: list[list[int]] = [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
        self.current_cwU: list[int] = [14, 8]
        self.current_kCv: int = 40

        # Level configs: each dict is stored in Level.data
        configs = [
            {"name": "intro", "elp": [[0, 0, 0], [0, 1, 0], [0, 0, 0]], "cwU": [14, 8], "kCv": 40,
             "layout": lambda: self._grid_layout(3, 3, 10, 10), "clicks": [(1, 1)]},
            {"name": "cross", "elp": [[0, 1, 0], [1, 1, 1], [0, 1, 0]], "cwU": [9, 12], "kCv": 48,
             "layout": lambda: self._grid_layout(3, 3, 10, 10), "clicks": [(0, 1), (2, 1), (1, 0), (1, 2)]},
            {"name": "hline", "elp": [[0, 0, 0], [1, 1, 1], [0, 0, 0]], "cwU": [8, 11], "kCv": 64,
             "layout": lambda: self._grid_layout(3, 4, 10, 6), "clicks": [(0, 0), (1, 1), (2, 2), (0, 3)]},
            {"name": "vline", "elp": [[0, 1, 0], [0, 1, 0], [0, 1, 0]], "cwU": [15, 12, 9], "kCv": 80,
             "layout": lambda: self._grid_layout(4, 3, 6, 10), "clicks": [(0, 0), (1, 1), (2, 2), (3, 0)]},
            {"name": "diag", "elp": [[1, 0, 0], [0, 1, 0], [0, 0, 1]], "cwU": [14, 8], "kCv": 96,
             "layout": lambda: self._grid_layout(4, 4, 6, 6), "clicks": [(0, 0), (0, 3), (3, 0), (3, 3), (1, 1), (2, 2)]},
            {"name": "full", "elp": [[1, 1, 1], [1, 1, 1], [1, 1, 1]], "cwU": [9, 11, 8], "kCv": 128,
             "layout": lambda: self._grid_layout(4, 4, 6, 6), "clicks": [(1, 1), (2, 2), (0, 0), (3, 3)]},
        ]

        # Build Level objects
        levels = [Level(grid_size=(32, 32), data=c, name=c["name"]) for c in configs]

        # Timer for level 0
        self.timer = TimerBar(configs[0]["kCv"])

        super().__init__(
            game_id="ct03",
            levels=levels,
            camera=Camera(0, 0, 16, 16, BACKGROUND_COLOR, PADDING_COLOR, [self.timer]),
            available_actions=[6],
        )

    # -- helpers --

    def _grid_layout(self, cols: int, rows: int, start_x: int, start_y: int, spacing: int = 4) -> list[tuple[int, int]]:
        """Return a list of (x, y) grid positions for a rectangular tile grid."""
        return [(start_x + c * spacing, start_y + r * spacing) for r in range(rows) for c in range(cols)]

    # -- level setup --

    def on_set_level(self, level: Level) -> None:
        """Populate the level with sprites based on its config data."""
        self.current_elp = level.get_data("elp")
        self.current_cwU = level.get_data("cwU")
        self.current_kCv = level.get_data("kCv")
        layout_func = level.get_data("layout")
        clicks = level.get_data("clicks")

        # Reset timer for this level
        self.timer = TimerBar(self.current_kCv)
        self.camera.replace_interface([self.timer])

        # Wipe any sprites already on the level
        self.current_level.remove_all_sprites()

        # 1. Background (32x32 solid)
        self.current_level.add_sprite(Sprite(
            pixels=np.full((32, 32), BACKGROUND_COLOR, dtype=np.int8),
            name="bg", layer=-2, visible=True, collidable=False,
        ))

        # 2. Effect-pattern indicator (top-right, 3x3)
        pat = np.zeros((3, 3), dtype=np.int8)
        for r in range(3):
            for c in range(3):
                pat[r, c] = ACTIVE_PATTERN_COLOR if self.current_elp[r][c] else INACTIVE_PATTERN_COLOR
        self.current_level.add_sprite(Sprite(
            pixels=pat, name="epat", x=28, y=1, visible=True, collidable=False,
        ))

        # 3. Color swatches (top-right, below pattern)
        for i, color in enumerate(self.current_cwU):
            self.current_level.add_sprite(Sprite(
                pixels=np.full((2, 2), color, dtype=np.int8),
                name=f"swatch_{i}", x=29, y=5 + i * 2, visible=True, collidable=False,
            ))

        # 4. Clickable tiles
        positions = layout_func()
        base_color = self.current_cwU[0]
        self.tile_sprites = []
        for idx, (tx, ty) in enumerate(positions):
            t = Sprite(
                pixels=np.full((3, 3), base_color, dtype=np.int8),
                name=f"tile_{idx}", x=tx, y=ty, tags=["tile"], visible=True, collidable=True,
            )
            self.current_level.add_sprite(t)
            self.tile_sprites.append(t)

        # 5. Simulate solution clicks to derive target state
        tile_indices: dict[str, int] = {t.name: 0 for t in self.tile_sprites}

        def _tile_at(x: int, y: int) -> Sprite | None:
            for t in self.tile_sprites:
                if t.x == x and t.y == y:
                    return t
            return None

        xs = sorted({p[0] for p in positions})
        ys = sorted({p[1] for p in positions})

        for click_c, click_r in clicks:
            if click_c < 0 or click_c >= len(xs) or click_r < 0 or click_r >= len(ys):
                continue
            clicked = _tile_at(xs[click_c], ys[click_r])
            if not clicked:
                continue
            for pr in range(3):
                for pc in range(3):
                    if self.current_elp[pr][pc] == 1:
                        target = _tile_at(clicked.x + (pc - 1) * 4, clicked.y + (pr - 1) * 4)
                        if target:
                            tile_indices[target.name] = (tile_indices[target.name] + 1) % len(self.current_cwU)

        # 6. Constraint sprites (invisible, logic-only)
        for t in self.tile_sprites:
            target_color = self.current_cwU[tile_indices[t.name]]
            c_px = np.zeros((3, 3), dtype=np.int8)
            c_px[1, 1] = target_color
            for pr in range(3):
                for pc in range(3):
                    if pr == 1 and pc == 1:
                        continue
                    neighbor = _tile_at(t.x + (pc - 1) * 4, t.y + (pr - 1) * 4)
                    if neighbor:
                        nc = self.current_cwU[tile_indices[neighbor.name]]
                        c_px[pr, pc] = 0 if nc == target_color else CONSTRAINT_NOMATCH_COLOR
                    else:
                        c_px[pr, pc] = CONSTRAINT_NOMATCH_COLOR
            self.current_level.add_sprite(Sprite(
                pixels=c_px, name=f"cst_{t.name}", x=t.x, y=t.y,
                tags=["cst"], visible=False, collidable=False,
            ))

        # 7. Target minimap (visual goal for the player)
        map_h, map_w = len(ys), len(xs)
        mm = np.full((map_h, map_w), BACKGROUND_COLOR, dtype=np.int8)
        for ri, ry in enumerate(ys):
            for ci, cx in enumerate(xs):
                t = _tile_at(cx, ry)
                if t:
                    mm[ri, ci] = self.current_cwU[tile_indices[t.name]]
        self.current_level.add_sprite(Sprite(
            pixels=mm, name="minimap", x=28, y=12, visible=True, collidable=False,
        ))

    # -- game loop --

    def step(self) -> None:
        """Handle one action (ACTION6 click)."""
        # Non-click actions just complete immediately
        if self.action.id.value != 6:
            self.complete_action()
            return

        # Resolve screen coords to grid coords
        sx = self.action.data.get("x", 0)
        sy = self.action.data.get("y", 0)
        result = self.camera.display_to_grid(sx, sy)
        if not result:
            if not self.timer.tick():
                self.lose()
            self.complete_action()
            return

        gx, gy = result

        # Find the clicked tile (3x3 sprites)
        clicked: Sprite | None = None
        for s in self.current_level.get_sprites_by_tag("tile"):
            if s.x <= gx < s.x + 3 and s.y <= gy < s.y + 3:
                clicked = s
                break

        if not clicked:
            if not self.timer.tick():
                self.lose()
            self.complete_action()
            return

        # Apply the effect pattern centered on the clicked tile
        affected: list[Sprite] = []
        for pr in range(3):
            for pc in range(3):
                if self.current_elp[pr][pc] == 1:
                    tx = clicked.x + (pc - 1) * 4
                    ty = clicked.y + (pr - 1) * 4
                    for s in self.current_level.get_sprites_by_tag("tile"):
                        if s.x == tx and s.y == ty:
                            affected.append(s)
                            break

        # Cycle colors on affected tiles
        for s in affected:
            cur = int(s.pixels[1, 1])
            try:
                idx = self.current_cwU.index(cur)
            except ValueError:
                idx = 0
            nxt = self.current_cwU[(idx + 1) % len(self.current_cwU)]
            s.pixels[:] = nxt

        # Win check
        if self._check_win():
            self.next_level()
        else:
            if not self.timer.tick():
                self.lose()

        self.complete_action()

    # -- win condition --

    def _check_win(self) -> bool:
        """Return True when every constraint is satisfied."""
        constraints = self.current_level.get_sprites_by_tag("cst")
        tiles = self.current_level.get_sprites_by_tag("tile")

        def _color_at(x: int, y: int) -> int | None:
            for t in tiles:
                if t.x == x and t.y == y:
                    return int(t.pixels[1, 1])
            return None

        for c in constraints:
            target = int(c.pixels[1, 1])
            for pr in range(3):
                for pc in range(3):
                    if pr == 1 and pc == 1:
                        continue
                    rule = int(c.pixels[pr, pc])
                    actual = _color_at(c.x + (pc - 1) * 4, c.y + (pr - 1) * 4)
                    if actual is None:
                        continue
                    # rule 0 = must match target; non-0 = must NOT match target
                    if rule == 0 and actual != target:
                        return False
                    if rule != 0 and actual == target:
                        return False
        return True

