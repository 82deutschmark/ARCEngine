# Author: Claude Sonnet 4
# Date: 2026-01-31
# PURPOSE: Game registry providing centralized discovery and instantiation of all ARCEngine games.
#          Enables shareability via stable game_id-version keys for variants and sharing.
# SRP/DRY check: Pass - registry module with version support

"""
ARCEngine Game Registry

Provides a central place to discover and instantiate available games.
Each game is identified by a unique game_id-version key.

Usage:
    from games import get_game, list_games, get_game_info

    # Get available games
    available = list_games()  # ["chain_reaction", "world_shifter"]

    # Instantiate a game by base ID
    game = get_game("world_shifter")

    # Get full info including version
    info = get_game_info("world_shifter")  # {"id": "world_shifter", "version": "1.0.0", "full_id": "world_shifter-1.0.0"}
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from arcengine import ARCBaseGame

# Game registry with version info
# Format: base_id -> (module_path, version)
_GAME_REGISTRY: dict[str, tuple[str, str]] = {
    "world_shifter": ("games.world_shifter", "1.0.0"),
    "chain_reaction": ("games.chain_reaction", "1.0.0"),
}


def get_game(game_id: str) -> "ARCBaseGame":
    """
    Instantiate a game by its ID.

    Args:
        game_id: The base identifier for the game (e.g., "world_shifter")
                 Can also accept full game_id-version format (e.g., "world_shifter-1.0.0")

    Returns:
        A new instance of the requested game

    Raises:
        ValueError: If game_id is not recognized
    """
    # Handle full game_id-version format
    base_id = game_id.split("-")[0] if "-" in game_id else game_id

    if base_id not in _GAME_REGISTRY:
        available = ", ".join(sorted(_GAME_REGISTRY.keys()))
        raise ValueError(f"Unknown game: {game_id}. Available games: {available}")

    if base_id == "world_shifter":
        from games.world_shifter import WorldShifter

        return WorldShifter()
    elif base_id == "chain_reaction":
        from games.chain_reaction import ChainReaction

        return ChainReaction()
    else:
        raise ValueError(f"Game {game_id} registered but not implemented")


def list_games() -> list[str]:
    """
    Return list of available game base IDs.

    Returns:
        Sorted list of game identifiers
    """
    return sorted(_GAME_REGISTRY.keys())


def get_game_info(game_id: str) -> dict[str, str]:
    """
    Get metadata about a game including version.

    Args:
        game_id: The base identifier for the game

    Returns:
        Dict with id, version, and full_id (game_id-version format)

    Raises:
        ValueError: If game_id is not recognized
    """
    if game_id not in _GAME_REGISTRY:
        available = ", ".join(sorted(_GAME_REGISTRY.keys()))
        raise ValueError(f"Unknown game: {game_id}. Available games: {available}")

    module_path, version = _GAME_REGISTRY[game_id]
    return {
        "id": game_id,
        "version": version,
        "full_id": f"{game_id}-{version}",
        "module": module_path,
    }


def list_games_with_versions() -> list[dict[str, str]]:
    """
    Return list of all games with their version info.

    Returns:
        List of dicts with id, version, and full_id for each game
    """
    return [get_game_info(game_id) for game_id in sorted(_GAME_REGISTRY.keys())]
