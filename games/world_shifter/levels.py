# Author: Claude Sonnet 4
# Date: 2026-01-31
# PURPOSE: World Shifter level definitions - complete redesign.
#          NO SCALING - native resolution for clean visuals.
#          Player fixed at center, world platforms shift around them.
# SRP/DRY check: Pass - clean level definitions with creative world layouts

"""Level definitions for World Shifter - Creative Redesign."""

from arcengine import Level
from games.world_shifter.sprites import SPRITES

# Player is always fixed at center of 64x64 canvas (accounting for energy bar)
# Position: (31, 29) puts 3x3 player centered in playable area
PLAYER_X = 31
PLAYER_Y = 29

# Level 1: "The Island" - Simple floating platform (10x10)
# Teaches the basic mechanic: world moves, you stay fixed
# Player center (32,30) → maze-local (5,5) = walkable
# Exit needs to be >1 pixel away from player to not auto-collide
LEVEL_1 = Level(
    sprites=[
        SPRITES["world_1"].clone().set_position(27, 25),
        SPRITES["exit"].clone().set_position(28, 26),  # Center at (29,27), 3+ pixels from player
        SPRITES["player"].clone().set_position(PLAYER_X, PLAYER_Y),
    ],
    grid_size=(64, 64),
    data={
        "min_x": -8,
        "max_x": 8,
        "min_y": -8,
        "max_y": 8,
    },
)

# Level 2: "Twin Peaks" - Two chambers connected (10x12)
# Learn to navigate between distinct areas
# Player center (32,30) → maze-local (5,7) = walkable
# Exit placed in upper chamber, far from player
LEVEL_2 = Level(
    sprites=[
        SPRITES["world_2"].clone().set_position(27, 23),
        SPRITES["exit"].clone().set_position(28, 24),  # Center at (29,25), upper chamber
        SPRITES["player"].clone().set_position(PLAYER_X, PLAYER_Y),
    ],
    grid_size=(64, 64),
    data={
        "min_x": -10,
        "max_x": 10,
        "min_y": -10,
        "max_y": 10,
    },
)

# Level 3: "The Spiral" - Wind your way to the center (12x12)
# Exit is at spiral center - must think in reverse
# Player starts at outer edge, exit in center (far enough to not auto-collide)
LEVEL_3 = Level(
    sprites=[
        SPRITES["world_3"].clone().set_position(26, 23),
        SPRITES["exit"].clone().set_position(28, 26),  # Center at (29,27), spiral center
        SPRITES["player"].clone().set_position(PLAYER_X, PLAYER_Y),
    ],
    grid_size=(64, 64),
    data={
        "min_x": -12,
        "max_x": 12,
        "min_y": -12,
        "max_y": 12,
    },
)

# Level 4: "Four Rooms" - Navigate connected chambers (12x12)
# Multiple paths, must choose wisely
LEVEL_4 = Level(
    sprites=[
        SPRITES["world_4"].clone().set_position(26, 23),
        SPRITES["exit"].clone().set_position(30, 26),  # Center at (31,27), maze-local (5,4)
        SPRITES["player"].clone().set_position(PLAYER_X, PLAYER_Y),
    ],
    grid_size=(64, 64),
    data={
        "min_x": -12,
        "max_x": 12,
        "min_y": -12,
        "max_y": 12,
    },
)

# Level 5: "The Archipelago" - Island hopping (14x14)
# Scattered platforms with narrow passages
LEVEL_5 = Level(
    sprites=[
        SPRITES["world_5"].clone().set_position(25, 22),
        SPRITES["exit"].clone().set_position(28, 26),  # Center at (29,27), in archipelago
        SPRITES["player"].clone().set_position(PLAYER_X, PLAYER_Y),
    ],
    grid_size=(64, 64),
    data={
        "min_x": -14,
        "max_x": 14,
        "min_y": -14,
        "max_y": 14,
    },
)

# Level 6: "The Fortress" - Final challenge (14x14)
# Symmetrical fortress with winding interior path
LEVEL_6 = Level(
    sprites=[
        SPRITES["world_6"].clone().set_position(25, 22),
        SPRITES["exit"].clone().set_position(28, 25),  # Center at (29,26), fortress center
        SPRITES["player"].clone().set_position(PLAYER_X, PLAYER_Y),
    ],
    grid_size=(64, 64),
    data={
        "min_x": -14,
        "max_x": 14,
        "min_y": -14,
        "max_y": 14,
    },
)

# All levels in progression order
LEVELS = [
    LEVEL_1,
    LEVEL_2,
    LEVEL_3,
    LEVEL_4,
    LEVEL_5,
    LEVEL_6,
]
