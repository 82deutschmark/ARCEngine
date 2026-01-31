# Author: Claude Sonnet 4
# Date: 2026-01-31
# PURPOSE: World Shifter game package. Exports game class, ID, and version for registry.
# SRP/DRY check: Pass - game package with proper versioning and 64x64 canvas

"""
World Shifter: The world moves, not you.

A puzzle game where player input moves the entire world in the opposite direction.
Navigate mazes by shifting walls, obstacles, and the exit toward your fixed position.

Features:
- Full 64x64 canvas like official ARC3 games
- Energy tracking UI at BOTTOM of canvas (30 moves per level)
- Scaled 4x sprites for visibility
- 6 levels of increasing difficulty
- game_id-version key: world_shifter-0.01
"""

from games.world_shifter.game import WorldShifter, GAME_ID, VERSION

__all__ = ["WorldShifter", "GAME_ID", "VERSION"]
