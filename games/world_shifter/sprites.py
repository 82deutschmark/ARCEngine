# Author: Claude Sonnet 4
# Date: 2026-01-31
# PURPOSE: World Shifter sprites - complete creative redesign.
#          Core mechanic: world moves around FIXED player position.
#          Design: floating colorful platforms on dark background.
# SRP/DRY check: Pass - creative sprite designs for world-shifting mechanic

"""Sprite definitions for World Shifter - Creative Redesign."""

from arcengine import BlockingMode, InteractionMode, Sprite

# =============================================================================
# ARC3 Color Palette
# 0: White, 1: Light Gray, 2: Gray, 3: Dark Gray, 4: Darker Gray, 5: Black
# 6: Pink (#E53AA3), 7: Light Pink, 8: Red (#F93C31), 9: Blue (#1E93FF)
# 10: Light Blue (#88D8F1), 11: Yellow (#FFDC00), 12: Orange (#FF851B)
# 13: Dark Red (#921231), 14: Green (#4FCC30), 15: Purple (#A356D0)
# =============================================================================

# Energy UI - yellow pills that deplete to dark red
ENERGY_PILL = Sprite(
    pixels=[
        [11, 11],
        [11, 11],
    ],
    name="energy_pill",
    visible=True,
    collidable=False,
    tags=["energy"],
)

ENERGY_PILL_OFF = Sprite(
    pixels=[
        [13, 13],
        [13, 13],
    ],
    name="energy_pill_off",
    visible=False,
    collidable=False,
)

# Player - FIXED crosshair position (white arms, orange center)
# This is the anchor point - the world moves, not the player
PLAYER = Sprite(
    pixels=[
        [-1, 0, -1],
        [0, 12, 0],
        [-1, 0, -1],
    ],
    name="player",
    blocking=BlockingMode.BOUNDING_BOX,
    interaction=InteractionMode.TANGIBLE,
    layer=10,
    tags=["player"],
)

# Exit - Blue beacon goal (the world brings this TO you)
EXIT = Sprite(
    pixels=[
        [9, 10, 9],
        [10, 9, 10],
        [9, 10, 9],
    ],
    name="exit",
    blocking=BlockingMode.BOUNDING_BOX,
    interaction=InteractionMode.TANGIBLE,
    layer=5,
    tags=["moveable", "exit"],
)

# =============================================================================
# FLOATING WORLD PLATFORMS - Creative shapes that shift around the player
# Gray (2) = solid walls/edges, -1 = walkable transparent space
# Design principle: interesting shapes, not boring rectangles
# =============================================================================

# Level 1: "The Island" - Organic floating platform shape
WORLD_1 = Sprite(
    pixels=[
        [-1, -1, 2, 2, 2, 2, 2, -1, -1, -1],
        [-1, 2, 2, 2, 2, 2, 2, 2, -1, -1],
        [2, 2, 2, -1, -1, -1, 2, 2, 2, -1],
        [2, 2, -1, -1, -1, -1, -1, 2, 2, -1],
        [2, 2, -1, -1, -1, -1, -1, 2, 2, 2],
        [2, 2, -1, -1, -1, -1, -1, -1, 2, 2],
        [2, 2, 2, -1, -1, -1, -1, 2, 2, 2],
        [-1, 2, 2, 2, 2, 2, 2, 2, 2, -1],
        [-1, -1, 2, 2, 2, 2, 2, 2, -1, -1],
        [-1, -1, -1, 2, 2, 2, -1, -1, -1, -1],
    ],
    name="world_1",
    blocking=BlockingMode.PIXEL_PERFECT,
    interaction=InteractionMode.TANGIBLE,
    layer=-1,
    tags=["moveable", "maze"],
)

# Level 2: "Twin Peaks" - Two connected chambers
WORLD_2 = Sprite(
    pixels=[
        [2, 2, 2, 2, -1, -1, 2, 2, 2, 2],
        [2, -1, -1, 2, -1, -1, 2, -1, -1, 2],
        [2, -1, -1, 2, 2, 2, 2, -1, -1, 2],
        [2, -1, -1, -1, -1, -1, -1, -1, -1, 2],
        [2, 2, 2, -1, -1, -1, -1, 2, 2, 2],
        [-1, -1, 2, -1, -1, -1, -1, 2, -1, -1],
        [-1, -1, 2, -1, -1, -1, -1, 2, -1, -1],
        [2, 2, 2, -1, -1, -1, -1, 2, 2, 2],
        [2, -1, -1, -1, -1, -1, -1, -1, -1, 2],
        [2, -1, -1, 2, 2, 2, 2, -1, -1, 2],
        [2, -1, -1, 2, -1, -1, 2, -1, -1, 2],
        [2, 2, 2, 2, -1, -1, 2, 2, 2, 2],
    ],
    name="world_2",
    blocking=BlockingMode.PIXEL_PERFECT,
    interaction=InteractionMode.TANGIBLE,
    layer=-1,
    tags=["moveable", "maze"],
)

# Level 3: "The Spiral" - Spiral path to center
WORLD_3 = Sprite(
    pixels=[
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        [2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 2],
        [2, -1, 2, 2, 2, 2, 2, 2, 2, 2, -1, 2],
        [2, -1, 2, -1, -1, -1, -1, -1, -1, 2, -1, 2],
        [2, -1, 2, -1, 2, 2, 2, 2, -1, 2, -1, 2],
        [2, -1, 2, -1, 2, -1, -1, 2, -1, 2, -1, 2],
        [2, -1, 2, -1, 2, -1, -1, 2, -1, 2, -1, 2],
        [2, -1, 2, -1, 2, 2, -1, 2, -1, 2, -1, 2],
        [2, -1, 2, -1, -1, -1, -1, 2, -1, 2, -1, 2],
        [2, -1, 2, 2, 2, 2, 2, 2, -1, 2, -1, 2],
        [2, -1, -1, -1, -1, -1, -1, -1, -1, 2, -1, 2],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, -1, 2],
    ],
    name="world_3",
    blocking=BlockingMode.PIXEL_PERFECT,
    interaction=InteractionMode.TANGIBLE,
    layer=-1,
    tags=["moveable", "maze"],
)

# Level 4: "Four Rooms" - Connected chambers with central hub
WORLD_4 = Sprite(
    pixels=[
        [-1, 2, 2, 2, 2, -1, -1, 2, 2, 2, 2, -1],
        [2, 2, -1, -1, 2, 2, 2, 2, -1, -1, 2, 2],
        [2, -1, -1, -1, -1, 2, 2, -1, -1, -1, -1, 2],
        [2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 2],
        [2, 2, -1, -1, 2, 2, 2, 2, -1, -1, 2, 2],
        [-1, 2, 2, -1, 2, -1, -1, 2, -1, 2, 2, -1],
        [-1, 2, 2, -1, 2, -1, -1, 2, -1, 2, 2, -1],
        [2, 2, -1, -1, 2, 2, 2, 2, -1, -1, 2, 2],
        [2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 2],
        [2, -1, -1, -1, -1, 2, 2, -1, -1, -1, -1, 2],
        [2, 2, -1, -1, 2, 2, 2, 2, -1, -1, 2, 2],
        [-1, 2, 2, 2, 2, -1, -1, 2, 2, 2, 2, -1],
    ],
    name="world_4",
    blocking=BlockingMode.PIXEL_PERFECT,
    interaction=InteractionMode.TANGIBLE,
    layer=-1,
    tags=["moveable", "maze"],
)

# Level 5: "The Archipelago" - Scattered islands with narrow passages
WORLD_5 = Sprite(
    pixels=[
        [2, 2, 2, -1, -1, -1, -1, -1, -1, 2, 2, 2, 2, 2],
        [2, -1, 2, 2, -1, -1, -1, -1, 2, 2, -1, -1, -1, 2],
        [2, -1, -1, 2, 2, 2, -1, 2, 2, -1, -1, -1, -1, 2],
        [-1, -1, -1, -1, -1, 2, -1, 2, -1, -1, -1, -1, 2, 2],
        [-1, -1, -1, -1, -1, 2, 2, 2, -1, -1, -1, -1, -1, -1],
        [-1, -1, 2, 2, 2, 2, -1, 2, 2, 2, 2, -1, -1, -1],
        [-1, 2, 2, -1, -1, -1, -1, -1, -1, -1, 2, 2, -1, -1],
        [-1, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1, 2, -1, -1],
        [2, 2, -1, -1, 2, 2, -1, 2, 2, -1, -1, 2, 2, -1],
        [2, -1, -1, 2, 2, -1, -1, -1, 2, 2, -1, -1, 2, 2],
        [2, -1, -1, 2, -1, -1, -1, -1, -1, 2, -1, -1, -1, 2],
        [2, 2, -1, 2, -1, -1, -1, -1, -1, 2, -1, -1, -1, 2],
        [-1, 2, 2, 2, 2, -1, -1, -1, 2, 2, -1, -1, 2, 2],
        [-1, -1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, -1],
    ],
    name="world_5",
    blocking=BlockingMode.PIXEL_PERFECT,
    interaction=InteractionMode.TANGIBLE,
    layer=-1,
    tags=["moveable", "maze"],
)

# Level 6: "The Fortress" - Symmetrical structure with winding path
WORLD_6 = Sprite(
    pixels=[
        [-1, -1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, -1, -1],
        [-1, 2, 2, -1, -1, -1, 2, 2, -1, -1, -1, 2, 2, -1],
        [2, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 2, 2],
        [2, -1, -1, -1, 2, 2, -1, -1, 2, 2, -1, -1, -1, 2],
        [2, -1, -1, 2, 2, -1, -1, -1, -1, 2, 2, -1, -1, 2],
        [2, -1, -1, 2, -1, -1, -1, -1, -1, -1, 2, -1, -1, 2],
        [2, 2, -1, -1, -1, -1, 2, 2, -1, -1, -1, -1, 2, 2],
        [2, 2, -1, -1, -1, -1, 2, 2, -1, -1, -1, -1, 2, 2],
        [2, -1, -1, 2, -1, -1, -1, -1, -1, -1, 2, -1, -1, 2],
        [2, -1, -1, 2, 2, -1, -1, -1, -1, 2, 2, -1, -1, 2],
        [2, -1, -1, -1, 2, 2, -1, -1, 2, 2, -1, -1, -1, 2],
        [2, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 2, 2],
        [-1, 2, 2, -1, -1, -1, 2, 2, -1, -1, -1, 2, 2, -1],
        [-1, -1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, -1, -1],
    ],
    name="world_6",
    blocking=BlockingMode.PIXEL_PERFECT,
    interaction=InteractionMode.TANGIBLE,
    layer=-1,
    tags=["moveable", "maze"],
)

# Dictionary for access
SPRITES = {
    "player": PLAYER,
    "exit": EXIT,
    "world_1": WORLD_1,
    "world_2": WORLD_2,
    "world_3": WORLD_3,
    "world_4": WORLD_4,
    "world_5": WORLD_5,
    "world_6": WORLD_6,
}
