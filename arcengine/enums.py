"""
Module containing enums used throughout the ARCEngine.
"""

from enum import Enum, auto


class BlockingMode(Enum):
    """Enum defining different collision detection behaviors for sprites."""
    NOT_BLOCKED = auto()      # No collision detection
    BOUNDING_BOX = auto()     # Simple rectangular collision detection
    PIXEL_PERFECT = auto()    # Precise pixel-level collision detection


class InteractionMode(Enum):
    """Enum defining how a sprite interacts with the game world visually and physically."""
    TANGIBLE = auto()         # Visible and can be collided with
    INTANGIBLE = auto()       # Visible but cannot be collided with (ghost-like)
    INVISIBLE = auto()        # Not visible but can be collided with (invisible wall)
    REMOVED = auto()          # Not visible and cannot be collided with (effectively removed) 