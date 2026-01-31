# Author: Claude Opus 4.5
# Date: 2026-01-31
# PURPOSE: Game registry providing centralized discovery and instantiation of all ARCEngine games.
#          Enables shareability via stable game_ids and supports iteration through versioning.
# SRP/DRY check: Pass - new module, no existing registry functionality

"""
ARCEngine Game Registry

Provides a central place to discover and instantiate available games.
Each game is identified by a unique game_id.

Usage:
    from games import get_game, list_games

    # Get available games
    available = list_games()  # ["world_shifter", "chain_reaction"]

    # Instantiate a game
    game = get_game("world_shifter")
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from arcengine import ARCBaseGame

# Lazy imports to avoid circular dependencies and improve startup time
_GAME_REGISTRY: dict[str, str] = {
    "world_shifter": "games.world_shifter",
    "chain_reaction": "games.chain_reaction",
}


def get_game(game_id: str) -> "ARCBaseGame":
    """
    Instantiate a game by its ID.

    Args:
        game_id: The unique identifier for the game (e.g., "world_shifter")

    Returns:
        A new instance of the requested game

    Raises:
        ValueError: If game_id is not recognized
    """
    if game_id not in _GAME_REGISTRY:
        available = ", ".join(sorted(_GAME_REGISTRY.keys()))
        raise ValueError(f"Unknown game: {game_id}. Available games: {available}")

    if game_id == "world_shifter":
        from games.world_shifter import WorldShifter

        return WorldShifter()
    elif game_id == "chain_reaction":
        from games.chain_reaction import ChainReaction

        return ChainReaction()
    else:
        raise ValueError(f"Game {game_id} registered but not implemented")


def list_games() -> list[str]:
    """
    Return list of available game IDs.

    Returns:
        Sorted list of game identifiers
    """
    return sorted(_GAME_REGISTRY.keys())
