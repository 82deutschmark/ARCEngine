# Author: Claude Sonnet 4
# Date: 2026-01-31
# PURPOSE: Chain Reaction game package. Exports game class, ID, and version for registry.
# SRP/DRY check: Pass - game package with proper versioning

"""
Chain Reaction: Match colors. Clear the board. Escape.

A Sokoban-style puzzle game where pushing colored blocks into matching blocks
destroys both. Clear all colored blocks to unlock the exit.

Features:
- Move tracking UI (25 moves per level)
- 6 levels with increasing color pairs
- game_id-version key: chain_reaction-1.0.0
"""

from games.chain_reaction.game import ChainReaction, GAME_ID, VERSION

__all__ = ["ChainReaction", "GAME_ID", "VERSION"]
