# Author: Claude Opus 4.5
# Date: 2026-01-31
# PURPOSE: Chain Reaction game package. Exports the main game class for registry access.
# SRP/DRY check: Pass - new game package

"""
Chain Reaction: Match colors. Clear the board. Escape.

A Sokoban-style puzzle game where pushing colored blocks into matching blocks
destroys both. Clear all colored blocks to unlock the exit.
"""

from games.chain_reaction.game import ChainReaction

__all__ = ["ChainReaction"]

GAME_ID = "chain_reaction"
VERSION = "1.0.0"
