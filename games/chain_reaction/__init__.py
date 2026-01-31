# Author: Claude Sonnet 4
# Date: 2026-01-31
# PURPOSE: Chain Reaction game package. Exports the game class and metadata.
# SRP/DRY check: Pass - exports game implementation from game.py

"""
Chain Reaction: Match colors. Clear the board. Escape.

A Sokoban-style puzzle game where pushing colored blocks into matching blocks
destroys both. Clear all colored blocks to unlock the exit.
"""

from games.chain_reaction.game import ChainReaction

GAME_ID = "chain_reaction"
VERSION = "1.0.0"

__all__ = ["ChainReaction", "GAME_ID", "VERSION"]
