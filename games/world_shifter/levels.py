# Author: Claude Opus 4.5
# Date: 2026-01-31
# PURPOSE: Level definitions for World Shifter. Each level specifies sprite positions,
#          grid size, and movement bounds for the world-shifting mechanic.
# SRP/DRY check: Pass - new game levels, uses sprites from sprites.py

"""Level definitions for World Shifter."""

from arcengine import Level
from games.world_shifter.sprites import SPRITES

# Level 1: Tutorial (8x8)
# Simple L-shaped path, teaches inverse movement
# Player at center, exit in top-right area
LEVEL_1 = Level(
    sprites=[
        SPRITES["maze_1"].clone().set_position(0, 0),
        SPRITES["exit"].clone().set_position(6, 1),
        SPRITES["player"].clone().set_position(3, 5),
    ],
    grid_size=(8, 8),
    data={
        "min_x": -3,
        "max_x": 3,
        "min_y": -4,
        "max_y": 4,
    },
)

# Level 2: Longer Journey (8x8)
# More winding path, builds comfort with inverse movement
LEVEL_2 = Level(
    sprites=[
        SPRITES["maze_2"].clone().set_position(0, 0),
        SPRITES["exit"].clone().set_position(6, 6),
        SPRITES["player"].clone().set_position(3, 3),
    ],
    grid_size=(8, 8),
    data={
        "min_x": -3,
        "max_x": 3,
        "min_y": -3,
        "max_y": 3,
    },
)

# Level 3: The Corridor (10x10)
# Tighter spaces, requires precise sequence
LEVEL_3 = Level(
    sprites=[
        SPRITES["maze_3"].clone().set_position(0, 0),
        SPRITES["exit"].clone().set_position(8, 8),
        SPRITES["player"].clone().set_position(4, 4),
    ],
    grid_size=(10, 10),
    data={
        "min_x": -4,
        "max_x": 4,
        "min_y": -4,
        "max_y": 4,
    },
)

# Level 4: The Spiral (10x10)
# Spiral-like structure, tests mental rotation
LEVEL_4 = Level(
    sprites=[
        SPRITES["maze_4"].clone().set_position(0, 0),
        SPRITES["exit"].clone().set_position(8, 1),
        SPRITES["player"].clone().set_position(4, 4),
    ],
    grid_size=(10, 10),
    data={
        "min_x": -4,
        "max_x": 4,
        "min_y": -4,
        "max_y": 4,
    },
)

# Level 5: The Maze (12x12)
# Complex navigation with multiple paths
LEVEL_5 = Level(
    sprites=[
        SPRITES["maze_5"].clone().set_position(0, 0),
        SPRITES["exit"].clone().set_position(10, 10),
        SPRITES["player"].clone().set_position(5, 5),
    ],
    grid_size=(12, 12),
    data={
        "min_x": -5,
        "max_x": 5,
        "min_y": -5,
        "max_y": 5,
    },
)

# Level 6: The Master (12x12)
# Final challenge, most complex maze
LEVEL_6 = Level(
    sprites=[
        SPRITES["maze_6"].clone().set_position(0, 0),
        SPRITES["exit"].clone().set_position(10, 10),
        SPRITES["player"].clone().set_position(5, 5),
    ],
    grid_size=(12, 12),
    data={
        "min_x": -5,
        "max_x": 5,
        "min_y": -5,
        "max_y": 5,
    },
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
