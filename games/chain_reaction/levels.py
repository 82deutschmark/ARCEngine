# Author: Claude Sonnet 4
# Date: 2026-01-31
# PURPOSE: Level definitions for Chain Reaction using FULL 64x64 canvas.
#          Walls and blocks scaled 4x to fill canvas. Move bar at bottom (row 62-63).
# SRP/DRY check: Pass - levels designed for 64x64 canvas like official ARC3 games

"""Level definitions for Chain Reaction - Full 64x64 canvas design."""

from arcengine import Level
from games.chain_reaction.sprites import SPRITES

# SCALE FACTOR - multiply base sprites by this to fill 64x64 canvas
# 8x8 walls * 4 = 32x32, 12x12 walls * 4 = 48x48
SCALE = 4

# Level 1: First Match (8x8 base * 4 = 32x32)
# One pair of red blocks - teaches basic push-and-match
LEVEL_1 = Level(
    sprites=[
        SPRITES["walls_1"].clone().set_position(16, 14).set_scale(SCALE),
        SPRITES["exit_locked"].clone().set_position(36, 38),
        SPRITES["player"].clone().set_position(20, 38),
        # Red block pair - scaled positions
        SPRITES["block_red"].clone().set_position(24, 22),
        SPRITES["block_red"].clone().set_position(36, 30),
    ],
    grid_size=(64, 64),
)

# Level 2: Walls Matter (8x8 base * 4 = 32x32)
# One pair of blue blocks with central pillar obstacle
LEVEL_2 = Level(
    sprites=[
        SPRITES["walls_2"].clone().set_position(16, 14).set_scale(SCALE),
        SPRITES["exit_locked"].clone().set_position(36, 38),
        SPRITES["player"].clone().set_position(20, 38),
        # Blue block pair - scaled positions
        SPRITES["block_blue"].clone().set_position(20, 18),
        SPRITES["block_blue"].clone().set_position(36, 34),
    ],
    grid_size=(64, 64),
)

# Level 3: Two Colors (10x10 base * 4 = 40x40)
# One pair of red blocks and one pair of blue blocks
LEVEL_3 = Level(
    sprites=[
        SPRITES["walls_3"].clone().set_position(12, 10).set_scale(SCALE),
        SPRITES["exit_locked"].clone().set_position(40, 42),
        SPRITES["player"].clone().set_position(16, 42),
        # Red block pair - scaled positions
        SPRITES["block_red"].clone().set_position(16, 18),
        SPRITES["block_red"].clone().set_position(40, 38),
        # Blue block pair - scaled positions
        SPRITES["block_blue"].clone().set_position(40, 18),
        SPRITES["block_blue"].clone().set_position(16, 38),
    ],
    grid_size=(64, 64),
)

# Level 4: Order Dependency (10x10 base * 4 = 40x40)
# Two color pairs where solving order matters
LEVEL_4 = Level(
    sprites=[
        SPRITES["walls_4"].clone().set_position(12, 10).set_scale(SCALE),
        SPRITES["exit_locked"].clone().set_position(40, 42),
        SPRITES["player"].clone().set_position(16, 42),
        # Yellow block pair - scaled positions
        SPRITES["block_yellow"].clone().set_position(20, 18),
        SPRITES["block_yellow"].clone().set_position(20, 34),
        # Purple block pair - scaled positions
        SPRITES["block_purple"].clone().set_position(36, 22),
        SPRITES["block_purple"].clone().set_position(36, 34),
    ],
    grid_size=(64, 64),
)

# Level 5: The Gauntlet (12x12 base * 4 = 48x48)
# Three color pairs with pillars creating lanes
LEVEL_5 = Level(
    sprites=[
        SPRITES["walls_5"].clone().set_position(8, 6).set_scale(SCALE),
        SPRITES["exit_locked"].clone().set_position(44, 46),
        SPRITES["player"].clone().set_position(12, 46),
        # Red block pair - scaled positions
        SPRITES["block_red"].clone().set_position(16, 18),
        SPRITES["block_red"].clone().set_position(40, 42),
        # Blue block pair - scaled positions
        SPRITES["block_blue"].clone().set_position(40, 18),
        SPRITES["block_blue"].clone().set_position(16, 42),
        # Yellow block pair - scaled positions
        SPRITES["block_yellow"].clone().set_position(20, 34),
        SPRITES["block_yellow"].clone().set_position(36, 34),
    ],
    grid_size=(64, 64),
)

# Level 6: Master Chain (12x12 base * 4 = 48x48)
# Three color pairs with tight positioning - final challenge
LEVEL_6 = Level(
    sprites=[
        SPRITES["walls_6"].clone().set_position(8, 6).set_scale(SCALE),
        SPRITES["exit_locked"].clone().set_position(44, 46),
        SPRITES["player"].clone().set_position(12, 46),
        # Red block pair - scaled positions
        SPRITES["block_red"].clone().set_position(12, 18),
        SPRITES["block_red"].clone().set_position(44, 34),
        # Blue block pair - scaled positions
        SPRITES["block_blue"].clone().set_position(44, 18),
        SPRITES["block_blue"].clone().set_position(12, 34),
        # Purple block pair - scaled positions
        SPRITES["block_purple"].clone().set_position(28, 18),
        SPRITES["block_purple"].clone().set_position(28, 34),
    ],
    grid_size=(64, 64),
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
