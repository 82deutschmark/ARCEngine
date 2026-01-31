# Author: Claude Sonnet 4
# Date: 2026-01-31
# PURPOSE: Level definitions for World Shifter using FULL 64x64 canvas.
#          Mazes are scaled 4x to fill the canvas. Energy bar at bottom (row 62-63).
# SRP/DRY check: Pass - levels designed for 64x64 canvas like official ARC3 games

"""Level definitions for World Shifter - Full 64x64 canvas design."""

from arcengine import Level
from games.world_shifter.sprites import SPRITES

# MAZE SCALE FACTOR - multiply base maze by this to fill 64x64 canvas
# 8x8 maze * 4 = 32x32, positioned to fill playable area (leaving room for energy bar)
# 12x12 maze * 4 = 48x48, fills most of canvas
MAZE_SCALE = 4

# Level 1: Tutorial (8x8 base * 4 = 32x32)
# Simple L-shaped path, teaches inverse movement
# Player fixed at center (30, 28), world moves around them
LEVEL_1 = Level(
    sprites=[
        SPRITES["maze_1"].clone().set_position(16, 14).set_scale(MAZE_SCALE),
        SPRITES["exit"].clone().set_position(40, 18),
        SPRITES["player"].clone().set_position(30, 28),
    ],
    grid_size=(64, 64),
    data={
        "min_x": -12,
        "max_x": 12,
        "min_y": -16,
        "max_y": 16,
    },
)

# Level 2: Longer Journey (8x8 base * 4 = 32x32)
# More winding path, builds comfort with inverse movement
LEVEL_2 = Level(
    sprites=[
        SPRITES["maze_2"].clone().set_position(16, 14).set_scale(MAZE_SCALE),
        SPRITES["exit"].clone().set_position(40, 38),
        SPRITES["player"].clone().set_position(30, 28),
    ],
    grid_size=(64, 64),
    data={
        "min_x": -12,
        "max_x": 12,
        "min_y": -12,
        "max_y": 12,
    },
)

# Level 3: The Corridor (10x10 base * 4 = 40x40)
# Tighter spaces, requires precise sequence
LEVEL_3 = Level(
    sprites=[
        SPRITES["maze_3"].clone().set_position(12, 10).set_scale(MAZE_SCALE),
        SPRITES["exit"].clone().set_position(44, 42),
        SPRITES["player"].clone().set_position(30, 28),
    ],
    grid_size=(64, 64),
    data={
        "min_x": -16,
        "max_x": 16,
        "min_y": -16,
        "max_y": 16,
    },
)

# Level 4: The Spiral (10x10 base * 4 = 40x40)
# Spiral-like structure, tests mental rotation
LEVEL_4 = Level(
    sprites=[
        SPRITES["maze_4"].clone().set_position(12, 10).set_scale(MAZE_SCALE),
        SPRITES["exit"].clone().set_position(44, 14),
        SPRITES["player"].clone().set_position(30, 28),
    ],
    grid_size=(64, 64),
    data={
        "min_x": -16,
        "max_x": 16,
        "min_y": -16,
        "max_y": 16,
    },
)

# Level 5: The Maze (12x12 base * 4 = 48x48)
# Complex navigation with multiple paths
LEVEL_5 = Level(
    sprites=[
        SPRITES["maze_5"].clone().set_position(8, 6).set_scale(MAZE_SCALE),
        SPRITES["exit"].clone().set_position(48, 46),
        SPRITES["player"].clone().set_position(30, 28),
    ],
    grid_size=(64, 64),
    data={
        "min_x": -20,
        "max_x": 20,
        "min_y": -20,
        "max_y": 20,
    },
)

# Level 6: The Master (12x12 base * 4 = 48x48)
# Final challenge, most complex maze
LEVEL_6 = Level(
    sprites=[
        SPRITES["maze_6"].clone().set_position(8, 6).set_scale(MAZE_SCALE),
        SPRITES["exit"].clone().set_position(48, 46),
        SPRITES["player"].clone().set_position(30, 28),
    ],
    grid_size=(64, 64),
    data={
        "min_x": -20,
        "max_x": 20,
        "min_y": -20,
        "max_y": 20,
    },
)

# All levels in order (6 levels for now, all using 64x64 canvas)
LEVELS = [
    LEVEL_1,
    LEVEL_2,
    LEVEL_3,
    LEVEL_4,
    LEVEL_5,
    LEVEL_6,
]
