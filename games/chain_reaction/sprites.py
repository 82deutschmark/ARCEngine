# Author: Claude Sonnet 4
# Date: 2026-01-31
# PURPOSE: Sprite definitions for Chain Reaction game. Contains player, exit, colored blocks,
#          and wall sprites for all 6 levels. Colored blocks annihilate when matching colors collide.
# SRP/DRY check: Pass - new game sprites following ARC3 color palette

"""Sprite definitions for Chain Reaction."""

from arcengine import BlockingMode, InteractionMode, Sprite

# ARC3 Color Reference:
# 0: White, 1: Light Gray, 2: Gray, 3: Dark Gray, 4: Darker Gray, 5: Black
# 6: Pink, 7: Light Pink, 8: Red, 9: Blue, 10: Light Blue, 11: Yellow
# 12: Orange, 13: Dark Red, 14: Green, 15: Purple

# Player sprite - 1x1 orange
PLAYER = Sprite(
    pixels=[[12]],  # Orange (ARC3 color 12)
    name="player",
    blocking=BlockingMode.BOUNDING_BOX,
    interaction=InteractionMode.TANGIBLE,
    layer=10,
    tags=["player"],
)

# Exit sprite (locked) - 2x2 white (blocked until all blocks cleared)
EXIT_LOCKED = Sprite(
    pixels=[
        [0, 0],
        [0, 0],
    ],  # White (ARC3 color 0) - locked state
    name="exit",
    blocking=BlockingMode.BOUNDING_BOX,
    interaction=InteractionMode.TANGIBLE,
    layer=0,
    tags=["exit", "locked"],
)

# Exit sprite (unlocked) - 2x2 green
EXIT_UNLOCKED = Sprite(
    pixels=[
        [14, 14],
        [14, 14],
    ],  # Green (ARC3 color 14) - unlocked state
    name="exit",
    blocking=BlockingMode.BOUNDING_BOX,
    interaction=InteractionMode.TANGIBLE,
    layer=0,
    tags=["exit"],
)

# Colored block sprites (2x2 each)

# Red blocks (ARC3 color 8)
BLOCK_RED = Sprite(
    pixels=[
        [8, 8],
        [8, 8],
    ],
    name="block_red",
    blocking=BlockingMode.BOUNDING_BOX,
    interaction=InteractionMode.TANGIBLE,
    layer=5,
    tags=["pushable", "colored", "red"],
)

# Blue blocks (ARC3 color 9)
BLOCK_BLUE = Sprite(
    pixels=[
        [9, 9],
        [9, 9],
    ],
    name="block_blue",
    blocking=BlockingMode.BOUNDING_BOX,
    interaction=InteractionMode.TANGIBLE,
    layer=5,
    tags=["pushable", "colored", "blue"],
)

# Yellow blocks (ARC3 color 11)
BLOCK_YELLOW = Sprite(
    pixels=[
        [11, 11],
        [11, 11],
    ],
    name="block_yellow",
    blocking=BlockingMode.BOUNDING_BOX,
    interaction=InteractionMode.TANGIBLE,
    layer=5,
    tags=["pushable", "colored", "yellow"],
)

# Purple blocks (ARC3 color 15)
BLOCK_PURPLE = Sprite(
    pixels=[
        [15, 15],
        [15, 15],
    ],
    name="block_purple",
    blocking=BlockingMode.BOUNDING_BOX,
    interaction=InteractionMode.TANGIBLE,
    layer=5,
    tags=["pushable", "colored", "purple"],
)

# Pink blocks (ARC3 color 6)
BLOCK_PINK = Sprite(
    pixels=[
        [6, 6],
        [6, 6],
    ],
    name="block_pink",
    blocking=BlockingMode.BOUNDING_BOX,
    interaction=InteractionMode.TANGIBLE,
    layer=5,
    tags=["pushable", "colored", "pink"],
)

# Light Blue blocks (ARC3 color 10)
BLOCK_LIGHTBLUE = Sprite(
    pixels=[
        [10, 10],
        [10, 10],
    ],
    name="block_lightblue",
    blocking=BlockingMode.BOUNDING_BOX,
    interaction=InteractionMode.TANGIBLE,
    layer=5,
    tags=["pushable", "colored", "lightblue"],
)

# Wall sprites for each level (using ARC3 color 2 = Gray)

# Level 1 Walls (8x8 - Open Arena)
WALLS_1 = Sprite(
    pixels=[
        [2, 2, 2, 2, 2, 2, 2, 2],
        [2, -1, -1, -1, -1, -1, -1, 2],
        [2, -1, -1, -1, -1, -1, -1, 2],
        [2, -1, -1, -1, -1, -1, -1, 2],
        [2, -1, -1, -1, -1, -1, -1, 2],
        [2, -1, -1, -1, -1, -1, -1, 2],
        [2, -1, -1, -1, -1, -1, -1, 2],
        [2, 2, 2, 2, 2, 2, 2, 2],
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
        [2, 2, 2, 2, 2, 2, 2, 2],
        [2, -1, -1, -1, -1, -1, -1, 2],
        [2, -1, -1, -1, -1, -1, -1, 2],
        [2, -1, -1, 2, 2, -1, -1, 2],
        [2, -1, -1, 2, 2, -1, -1, 2],
        [2, -1, -1, -1, -1, -1, -1, 2],
        [2, -1, -1, -1, -1, -1, -1, 2],
        [2, 2, 2, 2, 2, 2, 2, 2],
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
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        [2, -1, -1, -1, 2, -1, -1, -1, -1, 2],
        [2, -1, -1, -1, 2, -1, -1, -1, -1, 2],
        [2, -1, -1, -1, -1, -1, -1, -1, -1, 2],
        [2, 2, 2, -1, -1, -1, -1, 2, 2, 2],
        [2, -1, -1, -1, -1, -1, -1, -1, -1, 2],
        [2, -1, -1, -1, -1, -1, -1, -1, -1, 2],
        [2, -1, -1, -1, 2, -1, -1, -1, -1, 2],
        [2, -1, -1, -1, 2, -1, -1, -1, -1, 2],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    ],
    name="walls_3",
    blocking=BlockingMode.PIXEL_PERFECT,
    interaction=InteractionMode.TANGIBLE,
    layer=-1,
    tags=["fixed", "walls"],
)

# Level 4 Walls (10x10 - L-Shaped obstacles)
WALLS_4 = Sprite(
    pixels=[
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        [2, -1, -1, -1, -1, -1, -1, -1, -1, 2],
        [2, -1, 2, 2, -1, -1, -1, -1, -1, 2],
        [2, -1, 2, 2, -1, -1, -1, -1, -1, 2],
        [2, -1, -1, -1, -1, -1, -1, -1, -1, 2],
        [2, -1, -1, -1, -1, -1, -1, -1, -1, 2],
        [2, -1, -1, -1, -1, -1, 2, 2, -1, 2],
        [2, -1, -1, -1, -1, -1, 2, 2, -1, 2],
        [2, -1, -1, -1, -1, -1, -1, -1, -1, 2],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
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
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        [2, -1, -1, -1, -1, 2, -1, -1, -1, -1, -1, 2],
        [2, -1, -1, -1, -1, 2, -1, -1, -1, -1, -1, 2],
        [2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 2],
        [2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 2],
        [2, 2, 2, -1, -1, 2, 2, -1, -1, 2, 2, 2],
        [2, -1, -1, -1, -1, 2, 2, -1, -1, -1, -1, 2],
        [2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 2],
        [2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 2],
        [2, -1, -1, -1, -1, 2, -1, -1, -1, -1, -1, 2],
        [2, -1, -1, -1, -1, 2, -1, -1, -1, -1, -1, 2],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
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
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        [2, -1, -1, 2, -1, -1, -1, -1, 2, -1, -1, 2],
        [2, -1, -1, 2, -1, -1, -1, -1, 2, -1, -1, 2],
        [2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 2],
        [2, -1, -1, -1, -1, 2, 2, -1, -1, -1, -1, 2],
        [2, -1, -1, -1, -1, 2, 2, -1, -1, -1, -1, 2],
        [2, -1, -1, -1, -1, 2, 2, -1, -1, -1, -1, 2],
        [2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 2],
        [2, -1, -1, 2, -1, -1, -1, -1, 2, -1, -1, 2],
        [2, -1, -1, 2, -1, -1, -1, -1, 2, -1, -1, 2],
        [2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 2],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
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
    "block_purple": BLOCK_PURPLE,
    "block_pink": BLOCK_PINK,
    "block_lightblue": BLOCK_LIGHTBLUE,
    "walls_1": WALLS_1,
    "walls_2": WALLS_2,
    "walls_3": WALLS_3,
    "walls_4": WALLS_4,
    "walls_5": WALLS_5,
    "walls_6": WALLS_6,
}
