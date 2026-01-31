# Author: Claude Opus 4.5
# Date: 2026-01-31
# PURPOSE: Sprite definitions for World Shifter game. Contains player, exit, and maze sprites
#          for all 6 levels. Sprites tagged "moveable" shift when player provides input.
# SRP/DRY check: Pass - new game sprites, no existing world shifter assets

"""Sprite definitions for World Shifter."""

from arcengine import BlockingMode, InteractionMode, Sprite

# Player sprite - fixed position, renders on top
PLAYER = Sprite(
    pixels=[[8]],  # Orange 1x1
    name="player",
    blocking=BlockingMode.BOUNDING_BOX,
    interaction=InteractionMode.TANGIBLE,
    layer=10,
    tags=["player"],
)

# Exit sprite - part of moveable world
EXIT = Sprite(
    pixels=[[6]],  # Green 1x1
    name="exit",
    blocking=BlockingMode.BOUNDING_BOX,
    interaction=InteractionMode.TANGIBLE,
    layer=5,
    tags=["moveable", "exit"],
)

# Level 1 Maze (8x8 - Tutorial)
MAZE_1 = Sprite(
    pixels=[
        [5, 5, 5, 5, 5, 5, 5, 5],
        [5, -1, -1, -1, -1, -1, -1, 5],
        [5, -1, 5, 5, 5, 5, -1, 5],
        [5, -1, 5, -1, -1, -1, -1, 5],
        [5, -1, 5, -1, 5, 5, 5, 5],
        [5, -1, -1, -1, -1, -1, -1, 5],
        [5, -1, 5, 5, 5, 5, -1, 5],
        [5, 5, 5, 5, 5, 5, 5, 5],
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
        [5, 5, 5, 5, 5, 5, 5, 5],
        [5, -1, -1, -1, 5, -1, -1, 5],
        [5, 5, 5, -1, 5, -1, 5, 5],
        [5, -1, -1, -1, -1, -1, -1, 5],
        [5, -1, 5, 5, 5, 5, -1, 5],
        [5, -1, -1, -1, -1, 5, -1, 5],
        [5, 5, 5, 5, -1, -1, -1, 5],
        [5, 5, 5, 5, 5, 5, 5, 5],
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
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [5, -1, -1, -1, -1, 5, -1, -1, -1, 5],
        [5, -1, 5, 5, -1, 5, -1, 5, -1, 5],
        [5, -1, 5, -1, -1, -1, -1, 5, -1, 5],
        [5, -1, 5, -1, 5, 5, 5, 5, -1, 5],
        [5, -1, -1, -1, -1, -1, -1, -1, -1, 5],
        [5, 5, 5, 5, 5, -1, 5, 5, -1, 5],
        [5, -1, -1, -1, -1, -1, -1, -1, -1, 5],
        [5, -1, 5, 5, 5, 5, 5, 5, -1, 5],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
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
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [5, -1, 5, -1, -1, -1, -1, -1, -1, 5],
        [5, -1, 5, -1, 5, 5, 5, 5, -1, 5],
        [5, -1, 5, -1, 5, -1, -1, -1, -1, 5],
        [5, -1, 5, -1, 5, -1, 5, 5, 5, 5],
        [5, -1, 5, -1, 5, -1, -1, -1, -1, 5],
        [5, -1, -1, -1, 5, 5, 5, 5, -1, 5],
        [5, 5, 5, -1, -1, -1, -1, -1, -1, 5],
        [5, -1, -1, -1, 5, 5, 5, 5, -1, 5],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
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
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [5, -1, -1, -1, 5, -1, -1, -1, -1, -1, -1, 5],
        [5, -1, 5, -1, 5, -1, 5, 5, 5, 5, -1, 5],
        [5, -1, 5, -1, -1, -1, -1, -1, -1, 5, -1, 5],
        [5, -1, 5, 5, 5, 5, 5, -1, 5, 5, -1, 5],
        [5, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 5],
        [5, 5, 5, -1, 5, 5, 5, 5, 5, -1, 5, 5],
        [5, -1, -1, -1, 5, -1, -1, -1, -1, -1, -1, 5],
        [5, -1, 5, 5, 5, -1, 5, 5, 5, 5, -1, 5],
        [5, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 5],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, -1, 5],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
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
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [5, -1, 5, -1, -1, -1, 5, -1, -1, -1, -1, 5],
        [5, -1, 5, -1, 5, -1, 5, -1, 5, 5, -1, 5],
        [5, -1, -1, -1, 5, -1, -1, -1, 5, -1, -1, 5],
        [5, 5, 5, 5, 5, -1, 5, 5, 5, -1, 5, 5],
        [5, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 5],
        [5, -1, 5, 5, 5, 5, 5, -1, 5, 5, -1, 5],
        [5, -1, -1, -1, -1, -1, 5, -1, -1, -1, -1, 5],
        [5, 5, -1, 5, 5, -1, 5, 5, 5, 5, -1, 5],
        [5, -1, -1, -1, -1, -1, -1, -1, -1, 5, -1, 5],
        [5, -1, 5, 5, 5, 5, 5, 5, -1, -1, -1, 5],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
    ],
    name="maze_6",
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
}
