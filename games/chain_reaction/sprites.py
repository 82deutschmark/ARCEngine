# Author: Claude Opus 4.5
# Date: 2026-01-31
# PURPOSE: Sprite definitions for Chain Reaction game. Contains player, exit (locked/unlocked),
#          colored blocks for matching, and wall sprites for all 6 levels.
# SRP/DRY check: Pass - new game sprites, no existing chain reaction assets

"""Sprite definitions for Chain Reaction."""

from arcengine import BlockingMode, InteractionMode, Sprite

# Player sprite - 1x1 orange
PLAYER = Sprite(
    pixels=[[8]],
    name="player",
    blocking=BlockingMode.BOUNDING_BOX,
    interaction=InteractionMode.TANGIBLE,
    layer=10,
    tags=["player"],
)

# Exit sprite (locked) - 2x2 white, blocks until all colored blocks cleared
EXIT_LOCKED = Sprite(
    pixels=[
        [7, 7],
        [7, 7],
    ],
    name="exit",
    blocking=BlockingMode.BOUNDING_BOX,
    interaction=InteractionMode.TANGIBLE,
    layer=0,
    tags=["exit", "locked"],
)

# Exit sprite (unlocked) - 2x2 green, goal achieved
EXIT_UNLOCKED = Sprite(
    pixels=[
        [6, 6],
        [6, 6],
    ],
    name="exit",
    blocking=BlockingMode.BOUNDING_BOX,
    interaction=InteractionMode.TANGIBLE,
    layer=0,
    tags=["exit"],
)

# Colored blocks - 2x2 for visibility
BLOCK_RED = Sprite(
    pixels=[
        [2, 2],
        [2, 2],
    ],
    name="block_red",
    blocking=BlockingMode.BOUNDING_BOX,
    interaction=InteractionMode.TANGIBLE,
    tags=["pushable", "colored", "red"],
)

BLOCK_BLUE = Sprite(
    pixels=[
        [9, 9],
        [9, 9],
    ],
    name="block_blue",
    blocking=BlockingMode.BOUNDING_BOX,
    interaction=InteractionMode.TANGIBLE,
    tags=["pushable", "colored", "blue"],
)

BLOCK_YELLOW = Sprite(
    pixels=[
        [4, 4],
        [4, 4],
    ],
    name="block_yellow",
    blocking=BlockingMode.BOUNDING_BOX,
    interaction=InteractionMode.TANGIBLE,
    tags=["pushable", "colored", "yellow"],
)

BLOCK_CYAN = Sprite(
    pixels=[
        [3, 3],
        [3, 3],
    ],
    name="block_cyan",
    blocking=BlockingMode.BOUNDING_BOX,
    interaction=InteractionMode.TANGIBLE,
    tags=["pushable", "colored", "cyan"],
)

BLOCK_PURPLE = Sprite(
    pixels=[
        [12, 12],
        [12, 12],
    ],
    name="block_purple",
    blocking=BlockingMode.BOUNDING_BOX,
    interaction=InteractionMode.TANGIBLE,
    tags=["pushable", "colored", "purple"],
)

BLOCK_GREEN = Sprite(
    pixels=[
        [6, 6],
        [6, 6],
    ],
    name="block_green",
    blocking=BlockingMode.BOUNDING_BOX,
    interaction=InteractionMode.TANGIBLE,
    tags=["pushable", "colored", "green"],
)

# Wall sprites for each level

# Level 1 Walls (8x8 - Open Arena)
WALLS_1 = Sprite(
    pixels=[
        [5, 5, 5, 5, 5, 5, 5, 5],
        [5, -1, -1, -1, -1, -1, -1, 5],
        [5, -1, -1, -1, -1, -1, -1, 5],
        [5, -1, -1, -1, -1, -1, -1, 5],
        [5, -1, -1, -1, -1, -1, -1, 5],
        [5, -1, -1, -1, -1, -1, -1, 5],
        [5, -1, -1, -1, -1, -1, -1, 5],
        [5, 5, 5, 5, 5, 5, 5, 5],
    ],
    name="walls_1",
    blocking=BlockingMode.PIXEL_PERFECT,
    interaction=InteractionMode.TANGIBLE,
    layer=-1,
    tags=["fixed", "walls"],
)

# Level 2 Walls (8x8 - Central Pillar)
WALLS_2 = Sprite(
    pixels=[
        [5, 5, 5, 5, 5, 5, 5, 5],
        [5, -1, -1, -1, -1, -1, -1, 5],
        [5, -1, -1, -1, -1, -1, -1, 5],
        [5, -1, -1, 5, 5, -1, -1, 5],
        [5, -1, -1, 5, 5, -1, -1, 5],
        [5, -1, -1, -1, -1, -1, -1, 5],
        [5, -1, -1, -1, -1, -1, -1, 5],
        [5, 5, 5, 5, 5, 5, 5, 5],
    ],
    name="walls_2",
    blocking=BlockingMode.PIXEL_PERFECT,
    interaction=InteractionMode.TANGIBLE,
    layer=-1,
    tags=["fixed", "walls"],
)

# Level 3 Walls (10x10 - Corridors)
WALLS_3 = Sprite(
    pixels=[
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [5, -1, -1, -1, 5, -1, -1, -1, -1, 5],
        [5, -1, -1, -1, 5, -1, -1, -1, -1, 5],
        [5, -1, -1, -1, -1, -1, -1, -1, -1, 5],
        [5, 5, 5, -1, -1, -1, -1, 5, 5, 5],
        [5, -1, -1, -1, -1, -1, -1, -1, -1, 5],
        [5, -1, -1, -1, -1, -1, -1, -1, -1, 5],
        [5, -1, -1, -1, 5, -1, -1, -1, -1, 5],
        [5, -1, -1, -1, 5, -1, -1, -1, -1, 5],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
    ],
    name="walls_3",
    blocking=BlockingMode.PIXEL_PERFECT,
    interaction=InteractionMode.TANGIBLE,
    layer=-1,
    tags=["fixed", "walls"],
)

# Level 4 Walls (10x10 - L-Shaped)
WALLS_4 = Sprite(
    pixels=[
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [5, -1, -1, -1, -1, -1, -1, -1, -1, 5],
        [5, -1, 5, 5, -1, -1, -1, -1, -1, 5],
        [5, -1, 5, 5, -1, -1, -1, -1, -1, 5],
        [5, -1, -1, -1, -1, -1, -1, -1, -1, 5],
        [5, -1, -1, -1, -1, -1, -1, -1, -1, 5],
        [5, -1, -1, -1, -1, -1, 5, 5, -1, 5],
        [5, -1, -1, -1, -1, -1, 5, 5, -1, 5],
        [5, -1, -1, -1, -1, -1, -1, -1, -1, 5],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
    ],
    name="walls_4",
    blocking=BlockingMode.PIXEL_PERFECT,
    interaction=InteractionMode.TANGIBLE,
    layer=-1,
    tags=["fixed", "walls"],
)

# Level 5 Walls (12x12 - Complex)
WALLS_5 = Sprite(
    pixels=[
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [5, -1, -1, -1, -1, 5, -1, -1, -1, -1, -1, 5],
        [5, -1, -1, -1, -1, 5, -1, -1, -1, -1, -1, 5],
        [5, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 5],
        [5, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 5],
        [5, 5, 5, -1, -1, 5, 5, -1, -1, 5, 5, 5],
        [5, -1, -1, -1, -1, 5, 5, -1, -1, -1, -1, 5],
        [5, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 5],
        [5, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 5],
        [5, -1, -1, -1, -1, 5, -1, -1, -1, -1, -1, 5],
        [5, -1, -1, -1, -1, 5, -1, -1, -1, -1, -1, 5],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
    ],
    name="walls_5",
    blocking=BlockingMode.PIXEL_PERFECT,
    interaction=InteractionMode.TANGIBLE,
    layer=-1,
    tags=["fixed", "walls"],
)

# Level 6 Walls (12x12 - Master)
WALLS_6 = Sprite(
    pixels=[
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [5, -1, -1, 5, -1, -1, -1, -1, 5, -1, -1, 5],
        [5, -1, -1, 5, -1, -1, -1, -1, 5, -1, -1, 5],
        [5, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 5],
        [5, -1, -1, -1, -1, 5, 5, -1, -1, -1, -1, 5],
        [5, -1, -1, -1, -1, 5, 5, -1, -1, -1, -1, 5],
        [5, -1, -1, -1, -1, 5, 5, -1, -1, -1, -1, 5],
        [5, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 5],
        [5, -1, -1, 5, -1, -1, -1, -1, 5, -1, -1, 5],
        [5, -1, -1, 5, -1, -1, -1, -1, 5, -1, -1, 5],
        [5, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 5],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
    ],
    name="walls_6",
    blocking=BlockingMode.PIXEL_PERFECT,
    interaction=InteractionMode.TANGIBLE,
    layer=-1,
    tags=["fixed", "walls"],
)

# Dictionary for easy access
SPRITES = {
    "player": PLAYER,
    "exit_locked": EXIT_LOCKED,
    "exit_unlocked": EXIT_UNLOCKED,
    "block_red": BLOCK_RED,
    "block_blue": BLOCK_BLUE,
    "block_yellow": BLOCK_YELLOW,
    "block_cyan": BLOCK_CYAN,
    "block_purple": BLOCK_PURPLE,
    "block_green": BLOCK_GREEN,
    "walls_1": WALLS_1,
    "walls_2": WALLS_2,
    "walls_3": WALLS_3,
    "walls_4": WALLS_4,
    "walls_5": WALLS_5,
    "walls_6": WALLS_6,
}
