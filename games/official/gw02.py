# Author: Claude Sonnet 4
# Date: 2026-02-07
# PURPOSE: gw02 - Gravity Well puzzle (cleaned version of gw01). Control gravity to collect orbs into wells.
#          Yellow+Orange fuse to Green. Wells cycle colors. Green phases through platforms.
#          Improvements over gw01: readable names, themed colors (purple/pink), improved sprite art.
# SRP/DRY check: Pass

from typing import List, Optional, Tuple

from arcengine import ARCBaseGame, BlockingMode, Camera, GameAction, InteractionMode, Level, Sprite

# Colors - themed palette replacing grayscale
BACKGROUND_COLOR = 5   # void/background (black)
PLATFORM_FILL = 15     # platform fill (purple)
PLATFORM_EDGE = 13     # platform edge (dark red)
WELL_CENTER = 6        # well center (pink)
WELL_YELLOW = 11       # well accepts yellow orbs
WELL_ORANGE = 12       # well accepts orange orbs
WELL_GREEN = 14        # well accepts green/fused orbs
WELL_ANY = 0           # well accepts any orb (white)
ORB_LIGHT = 11         # light orb color (yellow)
ORB_HEAVY = 12         # heavy orb color (orange)
ORB_FUSED = 14         # fused orb color (green)
ORB_FUSED_MARK = 6     # fused orb center mark (pink)
RIM_COLOR_A = 9        # rim alternating color A (maroon)
RIM_COLOR_B = 10       # rim alternating color B (dark orange)
LETTERBOX_COLOR = 5    # letterbox matches background (black)


def generate_rim_pixels() -> list[list[int]]:
    """Generate the decorative rim border pixels (64x64 with 2-pixel border)."""
    pixels = []
    for y in range(64):
        row = []
        for x in range(64):
            is_rim = x < 2 or x >= 62 or y < 2 or y >= 62
            row.append(RIM_COLOR_A if is_rim and (x + y) % 2 == 0 else (RIM_COLOR_B if is_rim else -1))
        pixels.append(row)
    return pixels


def generate_well_pixels(well_color: int) -> list[list[int]]:
    """Generate well sprite pixels with the specified acceptance color."""
    return [
        [well_color, well_color, well_color, well_color, well_color],
        [well_color, WELL_CENTER, WELL_CENTER, WELL_CENTER, well_color],
        [well_color, WELL_CENTER, well_color, WELL_CENTER, well_color],
        [well_color, WELL_CENTER, WELL_CENTER, WELL_CENTER, well_color],
        [well_color, well_color, well_color, well_color, well_color],
    ]


# Sprite definitions with readable names and improved colors
sprites = {
    "platform": Sprite(
        pixels=[
            [PLATFORM_EDGE, PLATFORM_EDGE, PLATFORM_EDGE, PLATFORM_EDGE, PLATFORM_EDGE],
            [PLATFORM_EDGE, PLATFORM_FILL, PLATFORM_FILL, PLATFORM_FILL, PLATFORM_EDGE],
            [PLATFORM_EDGE, PLATFORM_FILL, PLATFORM_FILL, PLATFORM_FILL, PLATFORM_EDGE],
            [PLATFORM_EDGE, PLATFORM_FILL, PLATFORM_FILL, PLATFORM_FILL, PLATFORM_EDGE],
            [PLATFORM_EDGE, PLATFORM_EDGE, PLATFORM_EDGE, PLATFORM_EDGE, PLATFORM_EDGE],
        ],
        name="platform",
        blocking=BlockingMode.BOUNDING_BOX,
        interaction=InteractionMode.TANGIBLE,
        layer=0,
        tags=["solid"],
    ),
    "platform_small": Sprite(
        pixels=[
            [PLATFORM_EDGE, PLATFORM_EDGE, PLATFORM_EDGE],
            [PLATFORM_EDGE, PLATFORM_FILL, PLATFORM_EDGE],
            [PLATFORM_EDGE, PLATFORM_EDGE, PLATFORM_EDGE],
        ],
        name="platform_small",
        blocking=BlockingMode.BOUNDING_BOX,
        interaction=InteractionMode.TANGIBLE,
        layer=0,
        tags=["solid"],
    ),
    "well": Sprite(
        pixels=generate_well_pixels(WELL_ANY),
        name="well",
        blocking=BlockingMode.NOT_BLOCKED,
        interaction=InteractionMode.TANGIBLE,
        layer=-1,
        tags=["well"],
    ),
    "orb_light": Sprite(
        pixels=[
            [-1, ORB_LIGHT, -1],
            [ORB_LIGHT, 0, ORB_LIGHT],  # white center highlight
            [-1, ORB_LIGHT, -1],
        ],
        name="orb_light",
        blocking=BlockingMode.BOUNDING_BOX,
        interaction=InteractionMode.TANGIBLE,
        layer=5,
        tags=["orb", "light"],
    ),
    "orb_heavy": Sprite(
        pixels=[
            [-1, ORB_HEAVY, -1],
            [ORB_HEAVY, 8, ORB_HEAVY],  # cyan center for contrast
            [-1, ORB_HEAVY, -1],
        ],
        name="orb_heavy",
        blocking=BlockingMode.BOUNDING_BOX,
        interaction=InteractionMode.TANGIBLE,
        layer=5,
        tags=["orb", "heavy"],
    ),
    "orb_fused": Sprite(
        pixels=[
            [-1, ORB_FUSED, -1],
            [ORB_FUSED, ORB_FUSED_MARK, ORB_FUSED],
            [-1, ORB_FUSED, -1],
        ],
        name="orb_fused",
        blocking=BlockingMode.BOUNDING_BOX,
        interaction=InteractionMode.TANGIBLE,
        layer=5,
        tags=["orb", "fused"],
    ),
    "rim": Sprite(
        pixels=generate_rim_pixels(),
        name="rim",
        blocking=BlockingMode.NOT_BLOCKED,
        interaction=InteractionMode.INTANGIBLE,
        layer=20,
        tags=["rim"],
    ),
    "boundary_horizontal": Sprite(pixels=[[-2] * 60], name="boundary_horizontal", blocking=BlockingMode.BOUNDING_BOX, interaction=InteractionMode.INVISIBLE, layer=10, tags=["boundary"]),
    "boundary_vertical": Sprite(pixels=[[-2] for _ in range(60)], name="boundary_vertical", blocking=BlockingMode.BOUNDING_BOX, interaction=InteractionMode.INVISIBLE, layer=10, tags=["boundary"]),
}

# Fusion rules: (orb_color_a, orb_color_b) -> (result_color, result_tag)
FUSION_RULES = {
    (ORB_LIGHT, ORB_HEAVY): (ORB_FUSED, "fused"),
    (ORB_HEAVY, ORB_LIGHT): (ORB_FUSED, "fused"),
    (ORB_LIGHT, ORB_LIGHT): (ORB_LIGHT, "light"),
    (ORB_HEAVY, ORB_HEAVY): (ORB_HEAVY, "heavy"),
}

# Well acceptance rules: well_color -> list of orb colors accepted
WELL_ACCEPTS = {
    WELL_YELLOW: [ORB_LIGHT],
    WELL_ORANGE: [ORB_HEAVY],
    WELL_GREEN: [ORB_FUSED],
    WELL_ANY: [ORB_LIGHT, ORB_HEAVY, ORB_FUSED],
}

levels = [
    # Level 1: Tutorial - collect 2 yellow orbs into white well
    Level(
        sprites=[
            sprites["rim"].clone().set_position(0, 0),
            sprites["boundary_horizontal"].clone().set_position(2, 2),
            sprites["boundary_horizontal"].clone().set_position(2, 61),
            sprites["boundary_vertical"].clone().set_position(2, 2),
            sprites["boundary_vertical"].clone().set_position(61, 2),
            sprites["well"].clone().set_position(29, 50),
            sprites["platform"].clone().set_position(20, 30),
            sprites["platform"].clone().set_position(35, 30),
            sprites["orb_light"].clone().set_position(21, 27),
            sprites["orb_light"].clone().set_position(36, 27),
        ],
        grid_size=(64, 64),
        data={"needed": 2, "phase": WELL_ANY, "cycle": False},
    ),
    # Level 2: Yellow well only accepts yellow orbs (orange orb is a distractor)
    Level(
        sprites=[
            sprites["rim"].clone().set_position(0, 0),
            sprites["boundary_horizontal"].clone().set_position(2, 2),
            sprites["boundary_horizontal"].clone().set_position(2, 61),
            sprites["boundary_vertical"].clone().set_position(2, 2),
            sprites["boundary_vertical"].clone().set_position(61, 2),
            sprites["well"].clone().set_position(29, 45),
            sprites["platform"].clone().set_position(15, 25),
            sprites["platform"].clone().set_position(44, 25),
            sprites["orb_light"].clone().set_position(16, 22),
            sprites["orb_light"].clone().set_position(45, 22),
            sprites["orb_heavy"].clone().set_position(30, 12),
        ],
        grid_size=(64, 64),
        data={"needed": 2, "phase": WELL_YELLOW, "cycle": False},
    ),
    # Level 3: Green well requires fusing yellow + orange
    Level(
        sprites=[
            sprites["rim"].clone().set_position(0, 0),
            sprites["boundary_horizontal"].clone().set_position(2, 2),
            sprites["boundary_horizontal"].clone().set_position(2, 61),
            sprites["boundary_vertical"].clone().set_position(2, 2),
            sprites["boundary_vertical"].clone().set_position(61, 2),
            sprites["well"].clone().set_position(29, 50),
            sprites["platform"].clone().set_position(29, 30),
            sprites["orb_light"].clone().set_position(15, 27),
            sprites["orb_heavy"].clone().set_position(43, 27),
        ],
        grid_size=(64, 64),
        data={"needed": 1, "phase": WELL_GREEN, "cycle": False},
    ),
    # Level 4: Cycling well (yellow -> orange -> green)
    Level(
        sprites=[
            sprites["rim"].clone().set_position(0, 0),
            sprites["boundary_horizontal"].clone().set_position(2, 2),
            sprites["boundary_horizontal"].clone().set_position(2, 61),
            sprites["boundary_vertical"].clone().set_position(2, 2),
            sprites["boundary_vertical"].clone().set_position(61, 2),
            sprites["well"].clone().set_position(29, 50),
            sprites["platform"].clone().set_position(20, 20),
            sprites["platform"].clone().set_position(38, 35),
            sprites["orb_light"].clone().set_position(21, 17),
            sprites["orb_heavy"].clone().set_position(39, 32),
        ],
        grid_size=(64, 64),
        data={"needed": 2, "phase": WELL_YELLOW, "cycle": True},
    ),
    # Level 5: Fusion through platforms (green orbs phase through)
    Level(
        sprites=[
            sprites["rim"].clone().set_position(0, 0),
            sprites["boundary_horizontal"].clone().set_position(2, 2),
            sprites["boundary_horizontal"].clone().set_position(2, 61),
            sprites["boundary_vertical"].clone().set_position(2, 2),
            sprites["boundary_vertical"].clone().set_position(61, 2),
            sprites["well"].clone().set_position(29, 52),
            sprites["platform"].clone().set_position(24, 42),
            sprites["platform"].clone().set_position(34, 42),
            sprites["platform"].clone().set_position(20, 20),
            sprites["platform"].clone().set_position(38, 20),
            sprites["orb_light"].clone().set_position(21, 17),
            sprites["orb_heavy"].clone().set_position(39, 17),
        ],
        grid_size=(64, 64),
        data={"needed": 1, "phase": WELL_GREEN, "cycle": False},
    ),
    # Level 6: Complex multi-orb cycling puzzle
    Level(
        sprites=[
            sprites["rim"].clone().set_position(0, 0),
            sprites["boundary_horizontal"].clone().set_position(2, 2),
            sprites["boundary_horizontal"].clone().set_position(2, 61),
            sprites["boundary_vertical"].clone().set_position(2, 2),
            sprites["boundary_vertical"].clone().set_position(61, 2),
            sprites["well"].clone().set_position(29, 40),
            sprites["platform_small"].clone().set_position(15, 15),
            sprites["platform_small"].clone().set_position(45, 15),
            sprites["platform_small"].clone().set_position(15, 30),
            sprites["platform_small"].clone().set_position(45, 30),
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
        data={"needed": 4, "phase": WELL_YELLOW, "cycle": True},
    ),
]


class Gw02(ARCBaseGame):
    """Gravity Well puzzle game - tilt board to slide orbs into wells."""

    def __init__(self) -> None:
        super().__init__("gw02", levels, Camera(0, 0, 64, 64, BACKGROUND_COLOR, LETTERBOX_COLOR))

    def on_set_level(self, level: Level) -> None:
        """Initialize level state when a new level is loaded."""
        self.rim_sprite = level.get_sprites_by_tag("rim")[0]
        self.well_sprite = level.get_sprites_by_tag("well")[0]
        self.orb_sprites = level.get_sprites_by_tag("orb")
        self.solid_sprites = level.get_sprites_by_tag("solid")

        # Rim animation phase
        self.rim_phase = 0

        # Collection tracking
        self.orbs_collected = 0
        self.orbs_needed = level.get_data("needed") or len(self.orb_sprites)

        # Well phase (what color orbs it accepts)
        self.well_phase = level.get_data("phase") or WELL_ANY
        self.well_cycles = level.get_data("cycle") or False
        self.phase_sequence = [WELL_YELLOW, WELL_ORANGE, WELL_GREEN]
        self.phase_index = self.phase_sequence.index(self.well_phase) if self.well_phase in self.phase_sequence else 0

        # Simulation state
        self.simulating = False
        self.simulation_steps = 0
        self.gravity_dx = 0
        self.gravity_dy = 0

        self.update_well_pixels()

    def update_well_pixels(self) -> None:
        """Update well sprite to reflect current acceptance phase."""
        pixels = generate_well_pixels(self.well_phase)
        for y in range(5):
            for x in range(5):
                self.well_sprite.pixels[y][x] = pixels[y][x]

    def cycle_well_phase(self) -> None:
        """Advance well to next phase in cycle (if cycling enabled)."""
        if not self.well_cycles:
            return
        self.phase_index = (self.phase_index + 1) % len(self.phase_sequence)
        self.well_phase = self.phase_sequence[self.phase_index]
        self.update_well_pixels()

    def animate_rim(self) -> None:
        """Animate the decorative rim border."""
        self.rim_phase = (self.rim_phase + 1) % 4
        for y in range(64):
            for x in range(64):
                is_rim = x < 2 or x >= 62 or y < 2 or y >= 62
                if is_rim:
                    self.rim_sprite.pixels[y][x] = RIM_COLOR_A if (x + y + self.rim_phase) % 2 == 0 else RIM_COLOR_B

    def step(self) -> None:
        """Process one game step (handles input or simulation tick)."""
        # If simulating gravity, process one tick
        if self.simulating:
            moved, fused = self.simulate_gravity_step()
            self.simulation_steps += 1
            self.check_orb_collection()

            # End simulation when nothing moves or max steps reached
            if (not moved and not fused) or self.simulation_steps > 100:
                self.simulating = False
                self.check_level_complete()
                self.complete_action()
            return

        # Process player input (WASD to tilt board)
        dx, dy = 0, 0
        if self.action.id == GameAction.ACTION1:
            dy = -1  # W = tilt up
        elif self.action.id == GameAction.ACTION2:
            dy = 1   # S = tilt down
        elif self.action.id == GameAction.ACTION3:
            dx = -1  # A = tilt left
        elif self.action.id == GameAction.ACTION4:
            dx = 1   # D = tilt right

        if dx != 0 or dy != 0:
            self.animate_rim()
            self.cycle_well_phase()
            self.gravity_dx, self.gravity_dy = dx, dy
            self.simulating = True
            self.simulation_steps = 0
            # Reset per-action movement flags for heavy orbs
            for orb in self.orb_sprites:
                if hasattr(orb, "moved_this_action"):
                    orb.moved_this_action = False
            return

        self.complete_action()

    def simulate_gravity_step(self) -> Tuple[bool, bool]:
        """Simulate one step of gravity. Returns (any_moved, any_fused)."""
        moved, fused = False, False

        # Refresh orb list (some may have been removed)
        self.orb_sprites = [o for o in self.current_level.get_sprites_by_tag("orb") if o.interaction != InteractionMode.REMOVED]

        # Sort orbs so leading orb (closest to destination edge) moves first
        # This prevents false collisions between orbs moving same direction
        if self.gravity_dx > 0:
            self.orb_sprites.sort(key=lambda o: -o.x)
        elif self.gravity_dx < 0:
            self.orb_sprites.sort(key=lambda o: o.x)
        elif self.gravity_dy > 0:
            self.orb_sprites.sort(key=lambda o: -o.y)
        elif self.gravity_dy < 0:
            self.orb_sprites.sort(key=lambda o: o.y)

        # Collect fusion pairs
        fusion_pairs: List[Tuple[Sprite, Sprite]] = []

        for orb in self.orb_sprites:
            if orb.interaction == InteractionMode.REMOVED:
                continue

            is_heavy = "heavy" in orb.tags
            is_fused = "fused" in orb.tags

            # Heavy orbs only move once per action
            if is_heavy:
                if not hasattr(orb, "moved_this_action"):
                    orb.moved_this_action = False
                if orb.moved_this_action:
                    continue

            # Check if another orb is in the way (potential fusion)
            colliding_orb = self.find_colliding_orb(orb, self.gravity_dx, self.gravity_dy)
            if colliding_orb:
                fusion_pairs.append((orb, colliding_orb))
                continue

            # Check if orb can move (fused orbs can phase through platforms)
            can_move, _ = self.check_movement(orb, self.gravity_dx, self.gravity_dy, is_fused)
            if can_move:
                orb.move(self.gravity_dx, self.gravity_dy)
                moved = True
                if is_heavy:
                    orb.moved_this_action = True

        # Process fusions
        for orb_a, orb_b in fusion_pairs:
            if orb_a.interaction == InteractionMode.REMOVED or orb_b.interaction == InteractionMode.REMOVED:
                continue
            if self.fuse_orbs(orb_a, orb_b):
                fused = True

        return moved, fused

    def find_colliding_orb(self, orb: Sprite, dx: int, dy: int) -> Optional[Sprite]:
        """Find another orb that would be hit if this orb moves."""
        next_x, next_y = orb.x + dx, orb.y + dy
        for other in self.orb_sprites:
            if other is orb or other.interaction == InteractionMode.REMOVED:
                continue
            if self.rectangles_overlap(next_x, next_y, 3, 3, other.x, other.y, 3, 3):
                return other
        return None

    def check_movement(self, orb: Sprite, dx: int, dy: int, can_phase: bool) -> Tuple[bool, bool]:
        """Check if orb can move. Returns (can_move, phased_through)."""
        next_x, next_y = orb.x + dx, orb.y + dy

        # Check bounds
        if next_x < 2 or next_x + 3 > 62 or next_y < 2 or next_y + 3 > 62:
            return False, False

        # Check platform collisions
        for platform in self.solid_sprites:
            platform_height = len(platform.pixels)
            platform_width = len(platform.pixels[0]) if platform_height > 0 else 0
            if self.rectangles_overlap(next_x, next_y, 3, 3, platform.x, platform.y, platform_width, platform_height):
                if can_phase:
                    return True, True  # Fused orbs phase through
                return False, False

        return True, False

    def rectangles_overlap(self, x1: int, y1: int, w1: int, h1: int, x2: int, y2: int, w2: int, h2: int) -> bool:
        """Check if two rectangles overlap."""
        return x1 < x2 + w2 and x1 + w1 > x2 and y1 < y2 + h2 and y1 + h1 > y2

    def fuse_orbs(self, orb_a: Sprite, orb_b: Sprite) -> bool:
        """Attempt to fuse two orbs. Returns True if fusion occurred."""
        color_a = ORB_LIGHT if "light" in orb_a.tags else (ORB_HEAVY if "heavy" in orb_a.tags else ORB_FUSED)
        color_b = ORB_LIGHT if "light" in orb_b.tags else (ORB_HEAVY if "heavy" in orb_b.tags else ORB_FUSED)

        if (color_a, color_b) not in FUSION_RULES:
            return False

        result_color, result_tag = FUSION_RULES[(color_a, color_b)]

        # Remove both orbs
        orb_a.set_interaction(InteractionMode.REMOVED)
        orb_b.set_interaction(InteractionMode.REMOVED)

        # Create new orb at midpoint
        mid_x, mid_y = (orb_a.x + orb_b.x) // 2, (orb_a.y + orb_b.y) // 2
        tag_to_sprite = {"fused": "orb_fused", "light": "orb_light", "heavy": "orb_heavy"}
        new_orb = sprites[tag_to_sprite[result_tag]].clone().set_position(mid_x, mid_y)
        self.current_level.add_sprite(new_orb)

        return True

    def check_orb_collection(self) -> None:
        """Check if any orbs have entered the well and should be collected."""
        well_x, well_y = self.well_sprite.x, self.well_sprite.y
        accepted_colors = WELL_ACCEPTS.get(self.well_phase, [])

        for orb in self.current_level.get_sprites_by_tag("orb"):
            if orb.interaction == InteractionMode.REMOVED:
                continue

            # Check if orb center is inside well
            orb_center_x, orb_center_y = orb.x + 1, orb.y + 1
            if well_x <= orb_center_x <= well_x + 4 and well_y <= orb_center_y <= well_y + 4:
                orb_color = ORB_LIGHT if "light" in orb.tags else (ORB_HEAVY if "heavy" in orb.tags else ORB_FUSED)
                if orb_color in accepted_colors:
                    orb.set_interaction(InteractionMode.REMOVED)
                    self.orbs_collected += 1

    def check_level_complete(self) -> None:
        """Check if enough orbs collected to complete level."""
        if self.orbs_collected >= self.orbs_needed:
            if self.is_last_level():
                self.win()
            else:
                self.next_level()
