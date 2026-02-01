# Author: Claude Opus 4.5
# Date: 2026-02-01
# PURPOSE: Gravity Well - Control gravity to collect orbs into a well.
#          Based on ls20.py structure with World Shifter's cycling rim.
#          COLOR RESONANCE: Yellow + Orange = Green (phases through platforms).
#          Wells cycle colors - only matching orbs are collected.
# SRP/DRY check: Pass - single-file pattern like official games

from typing import List, Optional, Tuple

from arcengine import (
    ARCBaseGame,
    BlockingMode,
    Camera,
    GameAction,
    InteractionMode,
    Level,
    Sprite,
)

# =============================================================================
# COLORS (ARC3 16-color palette - Deep Ocean Theme)
# =============================================================================
VOID = 5            # Black background
PLATFORM = 2        # Gray platforms
PLATFORM_EDGE = 4   # Darker Gray edges
WELL_CENTER = 3     # Dark Gray well depth
WELL_YELLOW = 11    # Yellow phase
WELL_ORANGE = 12    # Orange phase
WELL_GREEN = 14     # Green phase
WELL_ANY = 0        # White - accepts any
ORB_LIGHT = 11      # Yellow orb (slides)
ORB_HEAVY = 12      # Orange orb (1 step)
ORB_FUSED = 14      # Green orb (phases)
ORB_FUSED_MARK = 6  # Pink marker
RIM_A = 9           # Blue rim
RIM_B = 10          # Light Blue rim
LETTERBOX = 4       # Darker Gray


# =============================================================================
# FUSION RULES
# =============================================================================
FUSION = {
    (ORB_LIGHT, ORB_HEAVY): (ORB_FUSED, "fused"),
    (ORB_HEAVY, ORB_LIGHT): (ORB_FUSED, "fused"),
    (ORB_LIGHT, ORB_LIGHT): (ORB_LIGHT, "light"),
    (ORB_HEAVY, ORB_HEAVY): (ORB_HEAVY, "heavy"),
}

ACCEPTS = {
    WELL_YELLOW: [ORB_LIGHT],
    WELL_ORANGE: [ORB_HEAVY],
    WELL_GREEN: [ORB_FUSED],
    WELL_ANY: [ORB_LIGHT, ORB_HEAVY, ORB_FUSED],
}


# =============================================================================
# SPRITES
# =============================================================================
def gen_rim() -> list[list[int]]:
    p = []
    for y in range(64):
        r = []
        for x in range(64):
            rim = x < 2 or x >= 62 or y < 2 or y >= 62
            r.append(RIM_A if rim and (x + y) % 2 == 0 else (RIM_B if rim else -1))
        p.append(r)
    return p


def gen_well(c: int) -> list[list[int]]:
    return [
        [c, c, c, c, c],
        [c, WELL_CENTER, WELL_CENTER, WELL_CENTER, c],
        [c, WELL_CENTER, c, WELL_CENTER, c],
        [c, WELL_CENTER, WELL_CENTER, WELL_CENTER, c],
        [c, c, c, c, c],
    ]


sprites = {
    "platform": Sprite(
        pixels=[
            [PLATFORM_EDGE, PLATFORM_EDGE, PLATFORM_EDGE, PLATFORM_EDGE, PLATFORM_EDGE],
            [PLATFORM_EDGE, PLATFORM, PLATFORM, PLATFORM, PLATFORM_EDGE],
            [PLATFORM_EDGE, PLATFORM, PLATFORM, PLATFORM, PLATFORM_EDGE],
            [PLATFORM_EDGE, PLATFORM, PLATFORM, PLATFORM, PLATFORM_EDGE],
            [PLATFORM_EDGE, PLATFORM_EDGE, PLATFORM_EDGE, PLATFORM_EDGE, PLATFORM_EDGE],
        ],
        name="platform",
        blocking=BlockingMode.BOUNDING_BOX,
        interaction=InteractionMode.TANGIBLE,
        layer=0,
        tags=["solid"],
    ),
    "platform_sm": Sprite(
        pixels=[
            [PLATFORM_EDGE, PLATFORM_EDGE, PLATFORM_EDGE],
            [PLATFORM_EDGE, PLATFORM, PLATFORM_EDGE],
            [PLATFORM_EDGE, PLATFORM_EDGE, PLATFORM_EDGE],
        ],
        name="platform_sm",
        blocking=BlockingMode.BOUNDING_BOX,
        interaction=InteractionMode.TANGIBLE,
        layer=0,
        tags=["solid"],
    ),
    "well": Sprite(
        pixels=gen_well(WELL_ANY),
        name="well",
        blocking=BlockingMode.NOT_BLOCKED,
        interaction=InteractionMode.TANGIBLE,
        layer=-1,
        tags=["well"],
    ),
    "orb_light": Sprite(
        pixels=[[-1, ORB_LIGHT, -1], [ORB_LIGHT, ORB_LIGHT, ORB_LIGHT], [-1, ORB_LIGHT, -1]],
        name="orb_light",
        blocking=BlockingMode.BOUNDING_BOX,
        interaction=InteractionMode.TANGIBLE,
        layer=5,
        tags=["orb", "light"],
    ),
    "orb_heavy": Sprite(
        pixels=[[-1, ORB_HEAVY, -1], [ORB_HEAVY, 8, ORB_HEAVY], [-1, ORB_HEAVY, -1]],
        name="orb_heavy",
        blocking=BlockingMode.BOUNDING_BOX,
        interaction=InteractionMode.TANGIBLE,
        layer=5,
        tags=["orb", "heavy"],
    ),
    "orb_fused": Sprite(
        pixels=[[-1, ORB_FUSED, -1], [ORB_FUSED, ORB_FUSED_MARK, ORB_FUSED], [-1, ORB_FUSED, -1]],
        name="orb_fused",
        blocking=BlockingMode.BOUNDING_BOX,
        interaction=InteractionMode.TANGIBLE,
        layer=5,
        tags=["orb", "fused"],
    ),
    "rim": Sprite(
        pixels=gen_rim(),
        name="rim",
        blocking=BlockingMode.NOT_BLOCKED,
        interaction=InteractionMode.INTANGIBLE,
        layer=20,
        tags=["rim"],
    ),
    "bound_h": Sprite(pixels=[[-2] * 60], name="bound_h", blocking=BlockingMode.BOUNDING_BOX, interaction=InteractionMode.INVISIBLE, layer=10, tags=["bound"]),
    "bound_v": Sprite(pixels=[[-2] for _ in range(60)], name="bound_v", blocking=BlockingMode.BOUNDING_BOX, interaction=InteractionMode.INVISIBLE, layer=10, tags=["bound"]),
}


# =============================================================================
# LEVELS
# =============================================================================
levels = [
    # Level 1: Tutorial - drop 2 yellow orbs
    Level(
        sprites=[
            sprites["rim"].clone().set_position(0, 0),
            sprites["bound_h"].clone().set_position(2, 2),
            sprites["bound_h"].clone().set_position(2, 61),
            sprites["bound_v"].clone().set_position(2, 2),
            sprites["bound_v"].clone().set_position(61, 2),
            sprites["well"].clone().set_position(29, 50),
            sprites["platform"].clone().set_position(20, 30),
            sprites["platform"].clone().set_position(35, 30),
            sprites["orb_light"].clone().set_position(21, 27),
            sprites["orb_light"].clone().set_position(36, 27),
        ],
        grid_size=(64, 64),
        data={"need": 2, "phase": WELL_ANY, "cycle": False},
    ),
    # Level 2: Yellow well only
    Level(
        sprites=[
            sprites["rim"].clone().set_position(0, 0),
            sprites["bound_h"].clone().set_position(2, 2),
            sprites["bound_h"].clone().set_position(2, 61),
            sprites["bound_v"].clone().set_position(2, 2),
            sprites["bound_v"].clone().set_position(61, 2),
            sprites["well"].clone().set_position(29, 45),
            sprites["platform"].clone().set_position(15, 25),
            sprites["platform"].clone().set_position(44, 25),
            sprites["orb_light"].clone().set_position(16, 22),
            sprites["orb_light"].clone().set_position(45, 22),
            sprites["orb_heavy"].clone().set_position(30, 12),
        ],
        grid_size=(64, 64),
        data={"need": 2, "phase": WELL_YELLOW, "cycle": False},
    ),
    # Level 3: Must fuse to create green
    Level(
        sprites=[
            sprites["rim"].clone().set_position(0, 0),
            sprites["bound_h"].clone().set_position(2, 2),
            sprites["bound_h"].clone().set_position(2, 61),
            sprites["bound_v"].clone().set_position(2, 2),
            sprites["bound_v"].clone().set_position(61, 2),
            sprites["well"].clone().set_position(29, 50),
            sprites["platform"].clone().set_position(29, 30),
            sprites["orb_light"].clone().set_position(15, 27),
            sprites["orb_heavy"].clone().set_position(43, 27),
        ],
        grid_size=(64, 64),
        data={"need": 1, "phase": WELL_GREEN, "cycle": False},
    ),
    # Level 4: Cycling well
    Level(
        sprites=[
            sprites["rim"].clone().set_position(0, 0),
            sprites["bound_h"].clone().set_position(2, 2),
            sprites["bound_h"].clone().set_position(2, 61),
            sprites["bound_v"].clone().set_position(2, 2),
            sprites["bound_v"].clone().set_position(61, 2),
            sprites["well"].clone().set_position(29, 50),
            sprites["platform"].clone().set_position(20, 20),
            sprites["platform"].clone().set_position(38, 35),
            sprites["orb_light"].clone().set_position(21, 17),
            sprites["orb_heavy"].clone().set_position(39, 32),
        ],
        grid_size=(64, 64),
        data={"need": 2, "phase": WELL_YELLOW, "cycle": True},
    ),
    # Level 5: Green phases through platform
    Level(
        sprites=[
            sprites["rim"].clone().set_position(0, 0),
            sprites["bound_h"].clone().set_position(2, 2),
            sprites["bound_h"].clone().set_position(2, 61),
            sprites["bound_v"].clone().set_position(2, 2),
            sprites["bound_v"].clone().set_position(61, 2),
            sprites["well"].clone().set_position(29, 52),
            sprites["platform"].clone().set_position(24, 42),
            sprites["platform"].clone().set_position(34, 42),
            sprites["platform"].clone().set_position(20, 20),
            sprites["platform"].clone().set_position(38, 20),
            sprites["orb_light"].clone().set_position(21, 17),
            sprites["orb_heavy"].clone().set_position(39, 17),
        ],
        grid_size=(64, 64),
        data={"need": 1, "phase": WELL_GREEN, "cycle": False},
    ),
    # Level 6: Master challenge
    Level(
        sprites=[
            sprites["rim"].clone().set_position(0, 0),
            sprites["bound_h"].clone().set_position(2, 2),
            sprites["bound_h"].clone().set_position(2, 61),
            sprites["bound_v"].clone().set_position(2, 2),
            sprites["bound_v"].clone().set_position(61, 2),
            sprites["well"].clone().set_position(29, 40),
            sprites["platform_sm"].clone().set_position(15, 15),
            sprites["platform_sm"].clone().set_position(45, 15),
            sprites["platform_sm"].clone().set_position(15, 30),
            sprites["platform_sm"].clone().set_position(45, 30),
            sprites["platform"].clone().set_position(5, 5),
            sprites["platform"].clone().set_position(54, 5),
            sprites["platform"].clone().set_position(5, 50),
            sprites["platform"].clone().set_position(54, 50),
            sprites["orb_light"].clone().set_position(6, 12),
            sprites["orb_light"].clone().set_position(55, 12),
            sprites["orb_heavy"].clone().set_position(6, 47),
            sprites["orb_heavy"].clone().set_position(55, 47),
        ],
        grid_size=(64, 64),
        data={"need": 4, "phase": WELL_YELLOW, "cycle": True},
    ),
]


# =============================================================================
# GAME CLASS
# =============================================================================
class GravityWell(ARCBaseGame):
    _rim: Sprite
    _well: Sprite
    _orbs: List[Sprite]
    _platforms: List[Sprite]
    _rim_phase: int
    _collected: int
    _need: int
    _phase: int
    _cycle: bool
    _seq: List[int]
    _seq_idx: int
    _sim: bool
    _sim_n: int
    _dx: int
    _dy: int

    def __init__(self) -> None:
        super().__init__("gravity_well", levels, Camera(0, 0, 64, 64, VOID, LETTERBOX))

    def on_set_level(self, level: Level) -> None:
        self._rim = level.get_sprites_by_tag("rim")[0]
        self._well = level.get_sprites_by_tag("well")[0]
        self._orbs = level.get_sprites_by_tag("orb")
        self._platforms = level.get_sprites_by_tag("solid")
        self._rim_phase = 0
        self._collected = 0
        self._need = level.get_data("need") or len(self._orbs)
        self._phase = level.get_data("phase") or WELL_ANY
        self._cycle = level.get_data("cycle") or False
        self._seq = [WELL_YELLOW, WELL_ORANGE, WELL_GREEN]
        self._seq_idx = self._seq.index(self._phase) if self._phase in self._seq else 0
        self._sim = False
        self._sim_n = 0
        self._dx = 0
        self._dy = 0
        self._upd_well()

    def _upd_well(self) -> None:
        p = gen_well(self._phase)
        for y in range(5):
            for x in range(5):
                self._well.pixels[y][x] = p[y][x]

    def _cycle_well(self) -> None:
        if not self._cycle:
            return
        self._seq_idx = (self._seq_idx + 1) % len(self._seq)
        self._phase = self._seq[self._seq_idx]
        self._upd_well()

    def _cycle_rim(self) -> None:
        self._rim_phase = (self._rim_phase + 1) % 4
        for y in range(64):
            for x in range(64):
                rim = x < 2 or x >= 62 or y < 2 or y >= 62
                if rim:
                    self._rim.pixels[y][x] = RIM_A if (x + y + self._rim_phase) % 2 == 0 else RIM_B

    def step(self) -> None:
        if self._sim:
            mv, fu = self._sim_step()
            self._sim_n += 1
            self._check_collect()
            if (not mv and not fu) or self._sim_n > 100:
                self._sim = False
                self._check_win()
                self.complete_action()
            return

        dx, dy = 0, 0
        if self.action.id == GameAction.ACTION1:
            dy = -1
        elif self.action.id == GameAction.ACTION2:
            dy = 1
        elif self.action.id == GameAction.ACTION3:
            dx = -1
        elif self.action.id == GameAction.ACTION4:
            dx = 1

        if dx != 0 or dy != 0:
            self._cycle_rim()
            self._cycle_well()
            self._dx, self._dy = dx, dy
            self._sim = True
            self._sim_n = 0
            for o in self._orbs:
                if hasattr(o, '_mv'):
                    o._mv = False
            return

        self.complete_action()

    def _sim_step(self) -> Tuple[bool, bool]:
        mv, fu = False, False
        self._orbs = [o for o in self.current_level.get_sprites_by_tag("orb") if o.interaction != InteractionMode.REMOVED]
        fuse: List[Tuple[Sprite, Sprite]] = []

        for o in self._orbs:
            if o.interaction == InteractionMode.REMOVED:
                continue
            heavy = "heavy" in o.tags
            fused = "fused" in o.tags

            if heavy:
                if not hasattr(o, '_mv'):
                    o._mv = False
                if o._mv:
                    continue

            coll = self._coll_orb(o, self._dx, self._dy)
            if coll:
                fuse.append((o, coll))
                continue

            can, phased = self._can_move(o, self._dx, self._dy, fused)
            if can:
                o.move(self._dx, self._dy)
                mv = True
                if heavy:
                    o._mv = True
                if phased and fused:
                    o.tags = [t for t in o.tags if t != "fused"]
                    o.tags.append("light")
                    o.pixels = [[-1, ORB_FUSED, -1], [ORB_FUSED, WELL_CENTER, ORB_FUSED], [-1, ORB_FUSED, -1]]

        for a, b in fuse:
            if a.interaction == InteractionMode.REMOVED or b.interaction == InteractionMode.REMOVED:
                continue
            self._fuse(a, b)
            fu = True

        return mv, fu

    def _coll_orb(self, o: Sprite, dx: int, dy: int) -> Optional[Sprite]:
        nx, ny = o.x + dx, o.y + dy
        for other in self._orbs:
            if other is o or other.interaction == InteractionMode.REMOVED:
                continue
            if self._overlap(nx, ny, 3, 3, other.x, other.y, 3, 3):
                return other
        return None

    def _can_move(self, o: Sprite, dx: int, dy: int, phase: bool) -> Tuple[bool, bool]:
        nx, ny = o.x + dx, o.y + dy
        if nx < 2 or nx + 3 > 62 or ny < 2 or ny + 3 > 62:
            return False, False
        for p in self._platforms:
            pw = len(p.pixels[0]) if p.pixels else 0
            ph = len(p.pixels) if p.pixels else 0
            if self._overlap(nx, ny, 3, 3, p.x, p.y, pw, ph):
                if phase:
                    return True, True
                return False, False
        return True, False

    def _overlap(self, x1: int, y1: int, w1: int, h1: int, x2: int, y2: int, w2: int, h2: int) -> bool:
        return x1 < x2 + w2 and x1 + w1 > x2 and y1 < y2 + h2 and y1 + h1 > y2

    def _fuse(self, a: Sprite, b: Sprite) -> None:
        c1 = ORB_LIGHT if "light" in a.tags else (ORB_HEAVY if "heavy" in a.tags else ORB_FUSED)
        c2 = ORB_LIGHT if "light" in b.tags else (ORB_HEAVY if "heavy" in b.tags else ORB_FUSED)
        if (c1, c2) not in FUSION:
            return
        rc, rt = FUSION[(c1, c2)]
        a.set_interaction(InteractionMode.REMOVED)
        b.set_interaction(InteractionMode.REMOVED)
        mx, my = (a.x + b.x) // 2, (a.y + b.y) // 2
        new = sprites[f"orb_{rt}"].clone().set_position(mx, my)
        self.current_level.add_sprite(new)

    def _check_collect(self) -> None:
        wx, wy = self._well.x, self._well.y
        acc = ACCEPTS.get(self._phase, [])
        for o in self.current_level.get_sprites_by_tag("orb"):
            if o.interaction == InteractionMode.REMOVED:
                continue
            cx, cy = o.x + 1, o.y + 1
            if wx <= cx <= wx + 4 and wy <= cy <= wy + 4:
                oc = ORB_LIGHT if "light" in o.tags else (ORB_HEAVY if "heavy" in o.tags else ORB_FUSED)
                if oc in acc:
                    o.set_interaction(InteractionMode.REMOVED)
                    self._collected += 1

    def _check_win(self) -> None:
        if self._collected >= self._need:
            if self.is_last_level():
                self.win()
            else:
                self.next_level()
