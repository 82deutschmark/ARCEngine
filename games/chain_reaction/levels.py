# Author: Claude Sonnet 4
# Date: 2026-01-31
# PURPOSE: Level definitions for Chain Reaction. Each level specifies sprite positions,
#          colored block pairs, and grid size. Blocks must be matched by color to clear.
# SRP/DRY check: Pass - new game levels using sprites from sprites.py

"""Level definitions for Chain Reaction."""

from arcengine import Level
from games.chain_reaction.sprites import SPRITES

# Level 1: First Match (8x8)
# One pair of red blocks - teaches basic push-and-match
LEVEL_1 = Level(
    sprites=[
        SPRITES["walls_1"].clone().set_position(0, 0),
        SPRITES["exit_locked"].clone().set_position(5, 6),
        SPRITES["player"].clone().set_position(1, 6),
        # Red block pair
        SPRITES["block_red"].clone().set_position(2, 2),
        SPRITES["block_red"].clone().set_position(5, 4),
    ],
    grid_size=(8, 8),
)

# Level 2: Walls Matter (8x8)
# One pair of blue blocks with central pillar obstacle
LEVEL_2 = Level(
    sprites=[
        SPRITES["walls_2"].clone().set_position(0, 0),
        SPRITES["exit_locked"].clone().set_position(5, 6),
        SPRITES["player"].clone().set_position(1, 6),
        # Blue block pair
        SPRITES["block_blue"].clone().set_position(1, 1),
        SPRITES["block_blue"].clone().set_position(5, 5),
    ],
    grid_size=(8, 8),
)

# Level 3: Two Colors (10x10)
# One pair of red blocks and one pair of blue blocks
LEVEL_3 = Level(
    sprites=[
        SPRITES["walls_3"].clone().set_position(0, 0),
        SPRITES["exit_locked"].clone().set_position(7, 8),
        SPRITES["player"].clone().set_position(1, 8),
        # Red block pair
        SPRITES["block_red"].clone().set_position(1, 2),
        SPRITES["block_red"].clone().set_position(7, 7),
        # Blue block pair
        SPRITES["block_blue"].clone().set_position(7, 2),
        SPRITES["block_blue"].clone().set_position(1, 7),
    ],
    grid_size=(10, 10),
)

# Level 4: Order Dependency (10x10)
# Two color pairs where solving order matters
LEVEL_4 = Level(
    sprites=[
        SPRITES["walls_4"].clone().set_position(0, 0),
        SPRITES["exit_locked"].clone().set_position(7, 8),
        SPRITES["player"].clone().set_position(1, 8),
        # Yellow block pair
        SPRITES["block_yellow"].clone().set_position(2, 2),
        SPRITES["block_yellow"].clone().set_position(2, 6),
        # Purple block pair
        SPRITES["block_purple"].clone().set_position(6, 3),
        SPRITES["block_purple"].clone().set_position(6, 6),
    ],
    grid_size=(10, 10),
)

# Level 5: The Gauntlet (12x12)
# Three color pairs with pillars creating lanes
LEVEL_5 = Level(
    sprites=[
        SPRITES["walls_5"].clone().set_position(0, 0),
        SPRITES["exit_locked"].clone().set_position(9, 10),
        SPRITES["player"].clone().set_position(1, 10),
        # Red block pair
        SPRITES["block_red"].clone().set_position(2, 3),
        SPRITES["block_red"].clone().set_position(8, 9),
        # Blue block pair
        SPRITES["block_blue"].clone().set_position(8, 3),
        SPRITES["block_blue"].clone().set_position(2, 9),
        # Yellow block pair
        SPRITES["block_yellow"].clone().set_position(3, 7),
        SPRITES["block_yellow"].clone().set_position(7, 7),
    ],
    grid_size=(12, 12),
)

# Level 6: Master Chain (12x12)
# Three color pairs with tight positioning - final challenge
LEVEL_6 = Level(
    sprites=[
        SPRITES["walls_6"].clone().set_position(0, 0),
        SPRITES["exit_locked"].clone().set_position(9, 10),
        SPRITES["player"].clone().set_position(1, 10),
        # Red block pair
        SPRITES["block_red"].clone().set_position(1, 3),
        SPRITES["block_red"].clone().set_position(9, 7),
        # Blue block pair
        SPRITES["block_blue"].clone().set_position(9, 3),
        SPRITES["block_blue"].clone().set_position(1, 7),
        # Purple block pair
        SPRITES["block_purple"].clone().set_position(5, 3),
        SPRITES["block_purple"].clone().set_position(5, 7),
    ],
    grid_size=(12, 12),
)

# All levels in order
LEVELS = [
    LEVEL_1,
    LEVEL_2,
    LEVEL_3,
    LEVEL_4,
    LEVEL_5,
    LEVEL_6,
]
