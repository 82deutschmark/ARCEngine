# Author: Claude Opus 4.5
# Date: 2026-01-31
# PURPOSE: World Shifter game package. Exports the main game class for registry access.
# SRP/DRY check: Pass - new game package

"""
World Shifter: The world moves, not you.

A puzzle game where player input moves the entire world in the opposite direction.
Navigate mazes by shifting walls, obstacles, and the exit toward your fixed position.
"""

from games.world_shifter.game import WorldShifter

__all__ = ["WorldShifter"]

GAME_ID = "world_shifter"
VERSION = "1.0.0"
