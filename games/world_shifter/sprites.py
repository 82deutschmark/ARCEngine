# Author: Claude Sonnet 4
# Date: 2026-01-31
# PURPOSE: Sprite definitions for World Shifter game. Contains player, exit, maze sprites,
#          and energy UI sprites for all 10 levels. Sprites tagged "moveable" shift on input.
# SRP/DRY check: Pass - game sprites with energy UI, using ARC3 color palette

"""Sprite definitions for World Shifter."""

from arcengine import BlockingMode, InteractionMode, Sprite

# =============================================================================
# ARC3 Color Reference (from shared/config/arc3Colors.ts)
# 0: White, 1: Light Gray, 2: Gray, 3: Dark Gray, 4: Darker Gray, 5: Black
# 6: Pink (#E53AA3), 7: Light Pink, 8: Red, 9: Blue, 10: Light Blue
# 11: Yellow, 12: Orange, 13: Dark Red, 14: Green, 15: Purple
# =============================================================================

# Energy UI sprites - displayed along top of 64x64 canvas
ENERGY_PILL = Sprite(
    pixels=[
        [6, 6],
        [6, 6],
    ],  # Pink 2x2 - vibrant energy indicator
    name="energy_pill",
    visible=True,
    collidable=False,
    tags=["energy"],
)

ENERGY_PILL_OFF = Sprite(
    pixels=[
        [3, 3],
        [3, 3],
    ],  # Dark Gray 2x2 - depleted energy
    name="energy_pill_off",
    visible=False,
    collidable=False,
)

# Player sprite - fixed position, renders on top
# Using bright Orange for high visibility
PLAYER = Sprite(
    pixels=[[12]],  # Orange 1x1 (ARC3 color 12)
    name="player",
    blocking=BlockingMode.BOUNDING_BOX,
    interaction=InteractionMode.TANGIBLE,
    layer=10,
    tags=["player"],
)

# Exit sprite - part of moveable world
# Bright Green indicates goal/success
EXIT = Sprite(
    pixels=[[14]],  # Green 1x1 (ARC3 color 14)
    name="exit",
    blocking=BlockingMode.BOUNDING_BOX,
    interaction=InteractionMode.TANGIBLE,
    layer=5,
    tags=["moveable", "exit"],
)

# Level 1 Maze (8x8 - Tutorial)
# ARC3 color 2 = Gray for walls
MAZE_1 = Sprite(
    pixels=[
        [2, 2, 2, 2, 2, 2, 2, 2],
        [2, -1, -1, -1, -1, -1, -1, 2],
        [2, -1, 2, 2, 2, 2, -1, 2],
        [2, -1, 2, -1, -1, -1, -1, 2],
        [2, -1, 2, -1, 2, 2, 2, 2],
        [2, -1, -1, -1, -1, -1, -1, 2],
        [2, -1, 2, 2, 2, 2, -1, 2],
        [2, 2, 2, 2, 2, 2, 2, 2],
    ],
    name="maze_1",
    blocking=BlockingMode.PIXEL_PERFECT,
    interaction=InteractionMode.TANGIBLE,
    layer=-1,
    tags=["moveable", "maze"],
)

# Level 2 Maze (8x8 - Longer Path)
MAZE_2 = Sprite(
    pixels=[
        [2, 2, 2, 2, 2, 2, 2, 2],
        [2, -1, -1, -1, 2, -1, -1, 2],
        [2, 2, 2, -1, 2, -1, 2, 2],
        [2, -1, -1, -1, -1, -1, -1, 2],
        [2, -1, 2, 2, 2, 2, -1, 2],
        [2, -1, -1, -1, -1, 2, -1, 2],
        [2, 2, 2, 2, -1, -1, -1, 2],
        [2, 2, 2, 2, 2, 2, 2, 2],
    ],
    name="maze_2",
    blocking=BlockingMode.PIXEL_PERFECT,
    interaction=InteractionMode.TANGIBLE,
    layer=-1,
    tags=["moveable", "maze"],
)

# Level 3 Maze (10x10 - Intermediate)
MAZE_3 = Sprite(
    pixels=[
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        [2, -1, -1, -1, -1, 2, -1, -1, -1, 2],
        [2, -1, 2, 2, -1, 2, -1, 2, -1, 2],
        [2, -1, 2, -1, -1, -1, -1, 2, -1, 2],
        [2, -1, 2, -1, 2, 2, 2, 2, -1, 2],
        [2, -1, -1, -1, -1, -1, -1, -1, -1, 2],
        [2, 2, 2, 2, 2, -1, 2, 2, -1, 2],
        [2, -1, -1, -1, -1, -1, -1, -1, -1, 2],
        [2, -1, 2, 2, 2, 2, 2, 2, -1, 2],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    ],
    name="maze_3",
    blocking=BlockingMode.PIXEL_PERFECT,
    interaction=InteractionMode.TANGIBLE,
    layer=-1,
    tags=["moveable", "maze"],
)

# Level 4 Maze (10x10 - Winding Path)
MAZE_4 = Sprite(
    pixels=[
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        [2, -1, 2, -1, -1, -1, -1, -1, -1, 2],
        [2, -1, 2, -1, 2, 2, 2, 2, -1, 2],
        [2, -1, 2, -1, 2, -1, -1, -1, -1, 2],
        [2, -1, 2, -1, 2, -1, 2, 2, 2, 2],
        [2, -1, 2, -1, 2, -1, -1, -1, -1, 2],
        [2, -1, -1, -1, 2, 2, 2, 2, -1, 2],
        [2, 2, 2, -1, -1, -1, -1, -1, -1, 2],
        [2, -1, -1, -1, 2, 2, 2, 2, -1, 2],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    ],
    name="maze_4",
    blocking=BlockingMode.PIXEL_PERFECT,
    interaction=InteractionMode.TANGIBLE,
    layer=-1,
    tags=["moveable", "maze"],
)

# Level 5 Maze (12x12 - Complex)
MAZE_5 = Sprite(
    pixels=[
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        [2, -1, -1, -1, 2, -1, -1, -1, -1, -1, -1, 2],
        [2, -1, 2, -1, 2, -1, 2, 2, 2, 2, -1, 2],
        [2, -1, 2, -1, -1, -1, -1, -1, -1, 2, -1, 2],
        [2, -1, 2, 2, 2, 2, 2, -1, 2, 2, -1, 2],
        [2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 2],
        [2, 2, 2, -1, 2, 2, 2, 2, 2, -1, 2, 2],
        [2, -1, -1, -1, 2, -1, -1, -1, -1, -1, -1, 2],
        [2, -1, 2, 2, 2, -1, 2, 2, 2, 2, -1, 2],
        [2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 2],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, -1, 2],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    ],
    name="maze_5",
    blocking=BlockingMode.PIXEL_PERFECT,
    interaction=InteractionMode.TANGIBLE,
    layer=-1,
    tags=["moveable", "maze"],
)

# Level 6 Maze (12x12 - Master)
MAZE_6 = Sprite(
    pixels=[
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        [2, -1, 2, -1, -1, -1, 2, -1, -1, -1, -1, 2],
        [2, -1, 2, -1, 2, -1, 2, -1, 2, 2, -1, 2],
        [2, -1, -1, -1, 2, -1, -1, -1, 2, -1, -1, 2],
        [2, 2, 2, 2, 2, -1, 2, 2, 2, -1, 2, 2],
        [2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 2],
        [2, -1, 2, 2, 2, 2, 2, -1, 2, 2, -1, 2],
        [2, -1, -1, -1, -1, -1, 2, -1, -1, -1, -1, 2],
        [2, 2, -1, 2, 2, -1, 2, 2, 2, 2, -1, 2],
        [2, -1, -1, -1, -1, -1, -1, -1, -1, 2, -1, 2],
        [2, -1, 2, 2, 2, 2, 2, 2, -1, -1, -1, 2],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    ],
    name="maze_6",
    blocking=BlockingMode.PIXEL_PERFECT,
    interaction=InteractionMode.TANGIBLE,
    layer=-1,
    tags=["moveable", "maze"],
)

# Level 7 Maze (10x10 - The Gauntlet)
# Narrow corridors requiring precise navigation
MAZE_7 = Sprite(
    pixels=[
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        [2, -1, -1, 2, -1, -1, -1, -1, -1, 2],
        [2, 2, -1, 2, -1, 2, 2, 2, -1, 2],
        [2, -1, -1, -1, -1, -1, -1, 2, -1, 2],
        [2, -1, 2, 2, 2, 2, -1, 2, -1, 2],
        [2, -1, 2, -1, -1, -1, -1, -1, -1, 2],
        [2, -1, 2, -1, 2, 2, 2, 2, 2, 2],
        [2, -1, -1, -1, -1, -1, -1, -1, -1, 2],
        [2, 2, 2, 2, 2, 2, 2, 2, -1, 2],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    ],
    name="maze_7",
    blocking=BlockingMode.PIXEL_PERFECT,
    interaction=InteractionMode.TANGIBLE,
    layer=-1,
    tags=["moveable", "maze"],
)

# Level 8 Maze (12x12 - Crossroads)
# Multiple intersection points requiring careful planning
MAZE_8 = Sprite(
    pixels=[
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        [2, -1, -1, -1, -1, 2, 2, -1, -1, -1, -1, 2],
        [2, -1, 2, 2, -1, -1, -1, -1, 2, 2, -1, 2],
        [2, -1, 2, -1, -1, 2, 2, -1, -1, 2, -1, 2],
        [2, -1, -1, -1, 2, 2, 2, 2, -1, -1, -1, 2],
        [2, 2, 2, -1, -1, -1, -1, -1, -1, 2, 2, 2],
        [2, 2, 2, -1, -1, -1, -1, -1, -1, 2, 2, 2],
        [2, -1, -1, -1, 2, 2, 2, 2, -1, -1, -1, 2],
        [2, -1, 2, -1, -1, 2, 2, -1, -1, 2, -1, 2],
        [2, -1, 2, 2, -1, -1, -1, -1, 2, 2, -1, 2],
        [2, -1, -1, -1, -1, 2, 2, -1, -1, -1, -1, 2],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    ],
    name="maze_8",
    blocking=BlockingMode.PIXEL_PERFECT,
    interaction=InteractionMode.TANGIBLE,
    layer=-1,
    tags=["moveable", "maze"],
)

# Level 9 Maze (14x14 - The Labyrinth)
# Large maze with winding paths
MAZE_9 = Sprite(
    pixels=[
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        [2, -1, -1, -1, 2, -1, -1, -1, -1, 2, -1, -1, -1, 2],
        [2, -1, 2, -1, 2, -1, 2, 2, -1, 2, -1, 2, -1, 2],
        [2, -1, 2, -1, -1, -1, 2, -1, -1, -1, -1, 2, -1, 2],
        [2, -1, 2, 2, 2, 2, 2, -1, 2, 2, 2, 2, -1, 2],
        [2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 2],
        [2, 2, 2, -1, 2, 2, 2, 2, 2, 2, -1, 2, 2, 2],
        [2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 2],
        [2, -1, 2, 2, 2, 2, -1, 2, 2, 2, 2, 2, -1, 2],
        [2, -1, 2, -1, -1, -1, -1, 2, -1, -1, -1, 2, -1, 2],
        [2, -1, 2, -1, 2, 2, -1, 2, -1, 2, -1, 2, -1, 2],
        [2, -1, -1, -1, 2, -1, -1, -1, -1, 2, -1, -1, -1, 2],
        [2, 2, 2, 2, 2, -1, 2, 2, 2, 2, 2, 2, -1, 2],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    ],
    name="maze_9",
    blocking=BlockingMode.PIXEL_PERFECT,
    interaction=InteractionMode.TANGIBLE,
    layer=-1,
    tags=["moveable", "maze"],
)

# Level 10 Maze (14x14 - The Ultimate Challenge)
# Most complex maze with multiple dead ends
MAZE_10 = Sprite(
    pixels=[
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        [2, -1, 2, -1, -1, -1, 2, 2, -1, -1, -1, 2, -1, 2],
        [2, -1, 2, -1, 2, -1, -1, -1, -1, 2, -1, 2, -1, 2],
        [2, -1, -1, -1, 2, 2, 2, -1, 2, 2, -1, -1, -1, 2],
        [2, 2, 2, -1, -1, -1, 2, -1, 2, -1, -1, 2, 2, 2],
        [2, -1, -1, -1, 2, -1, -1, -1, -1, -1, 2, -1, -1, 2],
        [2, -1, 2, 2, 2, 2, 2, -1, 2, 2, 2, 2, -1, 2],
        [2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 2],
        [2, -1, 2, 2, 2, 2, -1, 2, 2, 2, 2, 2, -1, 2],
        [2, -1, -1, -1, -1, 2, -1, -1, -1, 2, -1, -1, -1, 2],
        [2, 2, 2, 2, -1, 2, -1, 2, -1, 2, -1, 2, 2, 2],
        [2, -1, -1, -1, -1, -1, -1, 2, -1, -1, -1, -1, -1, 2],
        [2, -1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, -1, 2],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    ],
    name="maze_10",
    blocking=BlockingMode.PIXEL_PERFECT,
    interaction=InteractionMode.TANGIBLE,
    layer=-1,
    tags=["moveable", "maze"],
)

# Dictionary for easy access by level
SPRITES = {
    "player": PLAYER,
    "exit": EXIT,
    "maze_1": MAZE_1,
    "maze_2": MAZE_2,
    "maze_3": MAZE_3,
    "maze_4": MAZE_4,
    "maze_5": MAZE_5,
    "maze_6": MAZE_6,
    "maze_7": MAZE_7,
    "maze_8": MAZE_8,
    "maze_9": MAZE_9,
    "maze_10": MAZE_10,
}
