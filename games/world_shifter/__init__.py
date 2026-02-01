# Author: Claude Opus 4
# Date: 2026-01-31
# PURPOSE: World Shifter game package - redesigned with large mazes and checkered rim.
# SRP/DRY check: Pass - single-file pattern following complex_maze.py

"""
World Shifter: The world moves around you, not the other way around.

A puzzle game where player input moves the entire world in the opposite direction.
Navigate large 50x50 mazes by shifting them toward your fixed position.
Features a dynamic checkered rim that cycles colors on each move.

Features:
- Full 64x64 canvas with 50x50 playable mazes
- Checkered rim border that cycles colors on movement
- Inverse movement mechanic (push up = world moves down)
- 4 levels of procedurally generated mazes
- game_id-version: world_shifter-0.03
"""

from games.world_shifter.game import GAME_ID, VERSION, WorldShifter

__all__ = ["WorldShifter", "GAME_ID", "VERSION"]
