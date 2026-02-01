# Author: Claude Opus 4
# Date: 2026-01-31
# PURPOSE: World Shifter - completely redesigned following complex_maze.py pattern.
#          Large 50x50 mazes, checkered rim that cycles on movement, inverse movement.
#          Single-file pattern with sprites/levels inline.
# SRP/DRY check: Pass - cloned from working complex_maze.py pattern

"""World Shifter: The world moves around you, not the other way around.

A puzzle game where player input moves the entire world in the opposite direction.
Features a dynamic checkered rim that cycles colors on each move.
Navigate large mazes by shifting them toward your fixed position.
"""

from arcengine import ARCBaseGame, BlockingMode, Camera, GameAction, InteractionMode, Level, Sprite

# =============================================================================
# GAME IDENTIFICATION
# =============================================================================
GAME_ID = "world_shifter"
VERSION = "0.03"

# =============================================================================
# COLORS (ARC3 16-color palette)
# =============================================================================
BACKGROUND = 5     # Black - void behind everything
WALL_COLOR = 2     # Gray - maze walls
PATH_COLOR = -1    # Transparent - walkable areas

# Rim colors - two pairs that alternate in checkerboard pattern
RIM_COLOR_A1 = 9   # Blue
RIM_COLOR_A2 = 10  # Light Blue
RIM_COLOR_B1 = 11  # Yellow
RIM_COLOR_B2 = 12  # Orange

# Player and exit
PLAYER_CENTER = 8  # Red center
PLAYER_ARMS = 0    # White arms
EXIT_COLOR_1 = 14  # Green
EXIT_COLOR_2 = 6   # Pink

# =============================================================================
# HELPER: Generate a large maze procedurally
# =============================================================================
def generate_maze(width: int, height: int, seed: int = 0) -> list[list[int]]:
    """Generate a simple maze pattern for the given dimensions.
    
    Uses a basic pattern: walls on edges and scattered internal walls.
    -1 = walkable (transparent), WALL_COLOR (2) = blocked
    """
    import random
    rng = random.Random(seed)
    
    maze = []
    for y in range(height):
        row = []
        for x in range(width):
            # Outer walls
            if x == 0 or x == width - 1 or y == 0 or y == height - 1:
                row.append(WALL_COLOR)
            # Internal grid pattern with gaps
            elif x % 6 == 0 and y % 4 != 0:
                row.append(WALL_COLOR)
            elif y % 6 == 0 and x % 4 != 0:
                row.append(WALL_COLOR)
            # Random scattered walls (sparse)
            elif rng.random() < 0.08:
                row.append(WALL_COLOR)
            else:
                row.append(PATH_COLOR)
        maze.append(row)
    
    # Ensure starting area is clear (center-ish)
    cx, cy = width // 2, height // 2
    for dy in range(-3, 4):
        for dx in range(-3, 4):
            nx, ny = cx + dx, cy + dy
            if 1 <= nx < width - 1 and 1 <= ny < height - 1:
                maze[ny][nx] = PATH_COLOR
    
    return maze


def generate_checkered_rim() -> list[list[int]]:
    """Generate a 64x64 checkered rim pattern (2 pixels wide).
    
    Returns pixels where:
    - Outer 2 pixels on all sides form a checkerboard
    - Interior (60x60) is transparent (-1)
    """
    size = 64
    rim_width = 2
    pixels = []
    
    for y in range(size):
        row = []
        for x in range(size):
            # Check if in rim area
            in_rim = (x < rim_width or x >= size - rim_width or
                      y < rim_width or y >= size - rim_width)
            
            if in_rim:
                # Checkerboard pattern
                if (x + y) % 2 == 0:
                    row.append(RIM_COLOR_A1)
                else:
                    row.append(RIM_COLOR_A2)
            else:
                row.append(-1)  # Transparent interior
        pixels.append(row)
    
    return pixels


# =============================================================================
# SPRITES
# =============================================================================

# Player - fixed crosshair in center (white arms, red center)
PLAYER = Sprite(
    pixels=[
        [-1, PLAYER_ARMS, -1],
        [PLAYER_ARMS, PLAYER_CENTER, PLAYER_ARMS],
        [-1, PLAYER_ARMS, -1],
    ],
    name="player",
    blocking=BlockingMode.BOUNDING_BOX,
    interaction=InteractionMode.TANGIBLE,
    layer=10,
    tags=["player"],
)

# Exit beacon - green/pink pattern
EXIT = Sprite(
    pixels=[
        [EXIT_COLOR_1, EXIT_COLOR_2, EXIT_COLOR_1],
        [EXIT_COLOR_2, EXIT_COLOR_1, EXIT_COLOR_2],
        [EXIT_COLOR_1, EXIT_COLOR_2, EXIT_COLOR_1],
    ],
    name="exit",
    blocking=BlockingMode.BOUNDING_BOX,
    interaction=InteractionMode.TANGIBLE,
    layer=5,
    tags=["moveable", "exit"],
)

# Checkered rim sprite (covers full 64x64, only rim pixels visible)
RIM = Sprite(
    pixels=generate_checkered_rim(),
    name="rim",
    blocking=BlockingMode.NOT_BLOCKED,
    interaction=InteractionMode.INTANGIBLE,
    layer=20,  # On top of everything
    tags=["rim"],
)

# Large maze sprites - 50x50 playable area
MAZE_1 = Sprite(
    pixels=generate_maze(50, 50, seed=1),
    name="maze_1",
    blocking=BlockingMode.PIXEL_PERFECT,
    interaction=InteractionMode.TANGIBLE,
    layer=-1,
    tags=["moveable", "maze"],
)

MAZE_2 = Sprite(
    pixels=generate_maze(50, 50, seed=42),
    name="maze_2",
    blocking=BlockingMode.PIXEL_PERFECT,
    interaction=InteractionMode.TANGIBLE,
    layer=-1,
    tags=["moveable", "maze"],
)

MAZE_3 = Sprite(
    pixels=generate_maze(50, 50, seed=123),
    name="maze_3",
    blocking=BlockingMode.PIXEL_PERFECT,
    interaction=InteractionMode.TANGIBLE,
    layer=-1,
    tags=["moveable", "maze"],
)

MAZE_4 = Sprite(
    pixels=generate_maze(50, 50, seed=999),
    name="maze_4",
    blocking=BlockingMode.PIXEL_PERFECT,
    interaction=InteractionMode.TANGIBLE,
    layer=-1,
    tags=["moveable", "maze"],
)

# Sprite dictionary for easy access
sprites = {
    "player": PLAYER,
    "exit": EXIT,
    "rim": RIM,
    "maze_1": MAZE_1,
    "maze_2": MAZE_2,
    "maze_3": MAZE_3,
    "maze_4": MAZE_4,
}

# =============================================================================
# LEVELS
# =============================================================================
# Player fixed at center of 64x64 (31, 31 for 3x3 sprite = center at 32, 32)
# Maze positioned so player starts in walkable area
# Exit placed far from player start

PLAYER_X = 31
PLAYER_Y = 31

levels = [
    # Level 1: Introduction - maze starts centered, exit top-left
    Level(
        sprites=[
            sprites["rim"].clone().set_position(0, 0),
            sprites["maze_1"].clone().set_position(7, 7),
            sprites["exit"].clone().set_position(12, 12),
            sprites["player"].clone().set_position(PLAYER_X, PLAYER_Y),
        ],
        grid_size=(64, 64),
        data={
            "rim_phase": 0,
        },
    ),
    # Level 2: Harder maze, exit bottom-right
    Level(
        sprites=[
            sprites["rim"].clone().set_position(0, 0),
            sprites["maze_2"].clone().set_position(7, 7),
            sprites["exit"].clone().set_position(48, 48),
            sprites["player"].clone().set_position(PLAYER_X, PLAYER_Y),
        ],
        grid_size=(64, 64),
        data={
            "rim_phase": 0,
        },
    ),
    # Level 3: Different pattern, exit top-right
    Level(
        sprites=[
            sprites["rim"].clone().set_position(0, 0),
            sprites["maze_3"].clone().set_position(7, 7),
            sprites["exit"].clone().set_position(48, 12),
            sprites["player"].clone().set_position(PLAYER_X, PLAYER_Y),
        ],
        grid_size=(64, 64),
        data={
            "rim_phase": 0,
        },
    ),
    # Level 4: Final challenge, exit bottom-left
    Level(
        sprites=[
            sprites["rim"].clone().set_position(0, 0),
            sprites["maze_4"].clone().set_position(7, 7),
            sprites["exit"].clone().set_position(12, 48),
            sprites["player"].clone().set_position(PLAYER_X, PLAYER_Y),
        ],
        grid_size=(64, 64),
        data={
            "rim_phase": 0,
        },
    ),
]

# =============================================================================
# GAME CLASS
# =============================================================================


class WorldShifter(ARCBaseGame):
    """The world moves around you, not the other way around.
    
    Navigate large mazes by shifting them toward your fixed position.
    The checkered rim cycles colors on each move, adding visual feedback.
    Bring the exit TO you - you cannot move to it.
    """

    _player: Sprite
    _maze: Sprite
    _rim: Sprite
    _rim_phase: int

    def __init__(self) -> None:
        """Initialize game with full 64x64 camera."""
        camera = Camera(
            width=64,
            height=64,
            background=BACKGROUND,
            letter_box=BACKGROUND,
        )
        super().__init__(
            game_id=f"{GAME_ID}-{VERSION}",
            levels=levels,
            camera=camera,
        )

    def on_set_level(self, level: Level) -> None:
        """Cache references when level loads."""
        self._player = level.get_sprites_by_name("player")[0]
        self._maze = level.get_sprites_by_tag("maze")[0]
        self._rim = level.get_sprites_by_tag("rim")[0]
        self._rim_phase = 0

    def step(self) -> None:
        """Process one game step with inverse movement."""
        # Determine movement direction (INVERTED)
        dx, dy = 0, 0
        if self.action.id == GameAction.ACTION1:  # Up -> world moves down
            dy = 1
        elif self.action.id == GameAction.ACTION2:  # Down -> world moves up
            dy = -1
        elif self.action.id == GameAction.ACTION3:  # Left -> world moves right
            dx = 1
        elif self.action.id == GameAction.ACTION4:  # Right -> world moves left
            dx = -1

        # Try to move world
        if dx != 0 or dy != 0:
            if self._can_move_world(dx, dy):
                self._move_world(dx, dy)
                self._cycle_rim()  # Visual feedback on movement

        # Check win condition
        if self._check_exit_collision():
            if self.is_last_level():
                self.win()
            else:
                self.next_level()

        self.complete_action()

    def _get_player_center(self) -> tuple[int, int]:
        """Get center pixel of player (3x3 sprite)."""
        return self._player.x + 1, self._player.y + 1

    def _can_move_world(self, dx: int, dy: int) -> bool:
        """Check if world can move without player hitting a wall."""
        player_cx, player_cy = self._get_player_center()
        
        # Calculate player's position relative to maze after move
        new_maze_x = self._maze.x + dx
        new_maze_y = self._maze.y + dy
        
        local_x = player_cx - new_maze_x
        local_y = player_cy - new_maze_y
        
        # Check bounds
        if local_y < 0 or local_y >= len(self._maze.pixels):
            return False
        if local_x < 0 or local_x >= len(self._maze.pixels[0]):
            return False
        
        # Check if on wall pixel
        pixel = self._maze.pixels[local_y][local_x]
        return pixel != WALL_COLOR

    def _move_world(self, dx: int, dy: int) -> None:
        """Move all moveable sprites."""
        for sprite in self.current_level.get_sprites_by_tag("moveable"):
            sprite.move(dx, dy)

    def _cycle_rim(self) -> None:
        """Cycle the rim colors to create visual movement feedback."""
        self._rim_phase = (self._rim_phase + 1) % 4
        
        # Rotate through color pairs
        if self._rim_phase == 0:
            c1, c2 = RIM_COLOR_A1, RIM_COLOR_A2
        elif self._rim_phase == 1:
            c1, c2 = RIM_COLOR_B1, RIM_COLOR_B2
        elif self._rim_phase == 2:
            c1, c2 = RIM_COLOR_A2, RIM_COLOR_A1
        else:
            c1, c2 = RIM_COLOR_B2, RIM_COLOR_B1
        
        # Update rim pixels
        size = 64
        rim_width = 2
        for y in range(size):
            for x in range(size):
                in_rim = (x < rim_width or x >= size - rim_width or
                          y < rim_width or y >= size - rim_width)
                if in_rim:
                    if (x + y) % 2 == 0:
                        self._rim.pixels[y][x] = c1
                    else:
                        self._rim.pixels[y][x] = c2

    def _check_exit_collision(self) -> bool:
        """Check if exit overlaps with player (center-point collision)."""
        exit_sprites = self.current_level.get_sprites_by_tag("exit")
        if not exit_sprites:
            return False
        exit_sprite = exit_sprites[0]
        
        player_cx, player_cy = self._get_player_center()
        exit_cx = exit_sprite.x + 1
        exit_cy = exit_sprite.y + 1
        
        return abs(player_cx - exit_cx) <= 1 and abs(player_cy - exit_cy) <= 1


# =============================================================================
# MAIN (for testing)
# =============================================================================
if __name__ == "__main__":
    from arcengine import ActionInput

    game = WorldShifter()
    result = game.perform_action(ActionInput(id=GameAction.RESET))
    print(f"World Shifter v{VERSION}")
    print(f"Initial state: {result.state}")
    print(f"Level: 1/{result.win_levels}")
    print("Controls: WASD/Arrows move the WORLD in opposite direction")
