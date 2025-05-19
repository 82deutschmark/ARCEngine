"""
Module for level-related functionality in the ARCEngine.
"""

from typing import List, Optional
from .sprites import Sprite


class Level:
    """A level that manages a collection of sprites."""

    def __init__(self, sprites: Optional[List[Sprite]] = None):
        """Initialize a new Level.

        Args:
            sprites: Optional list of sprites to initialize the level with
        """
        self._sprites: List[Sprite] = []
        if sprites:
            for sprite in sprites:
                self.add_sprite(sprite)

    def add_sprite(self, sprite: Sprite) -> None:
        """Add a sprite to the level.

        Args:
            sprite: The sprite to add
        """
        self._sprites.append(sprite)

    def remove_sprite(self, sprite: Sprite) -> None:
        """Remove a sprite from the level.

        Args:
            sprite: The sprite to remove
        """
        if sprite in self._sprites:
            self._sprites.remove(sprite)

    def get_sprites(self) -> List[Sprite]:
        """Get all sprites in the level.

        Returns:
            List[Sprite]: All sprites in the level
        """
        return self._sprites.copy()  # Return copy to prevent external modification

    def get_sprites_by_name(self, name: str) -> List[Sprite]:
        """Get all sprites with the given name.

        Args:
            name: The name to search for

        Returns:
            List[Sprite]: All sprites with the given name
        """
        return [s for s in self._sprites if s.name == name]

    def clone(self) -> "Level":
        """Create a deep copy of this level.

        Returns:
            Level: A new Level instance with cloned sprites
        """
        # Clone each sprite and create new level
        cloned_sprites = [sprite.clone() for sprite in self._sprites]
        return Level(sprites=cloned_sprites)
