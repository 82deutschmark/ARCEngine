"""
Module for level-related functionality in the ARCEngine.
"""

import copy
from typing import Any, List, Optional, Tuple

from .enums import BlockingMode
from .sprites import Sprite


class Level:
    """A level that manages a collection of sprites."""

    _sprites: List[Sprite]
    _grid_size: Tuple[int, int] | None
    _data: dict[str, Any]
    _name: str

    def __init__(
        self,
        sprites: Optional[List[Sprite]] = None,
        grid_size: Tuple[int, int] | None = None,
        data: dict[str, Any] = {},
        name: str = "Level",
    ):
        """Initialize a new Level.

        Args:
            sprites: Optional list of sprites to initialize the level with
        """
        self._sprites: List[Sprite] = []
        if sprites:
            for sprite in sprites:
                self.add_sprite(sprite)
        self._grid_size = grid_size
        self._data = data
        self._name = name

    def remove_all_sprites(self) -> None:
        """Remove all sprites from the level."""
        self._sprites = []

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

    def get_sprites_by_tag(self, tag: str) -> List[Sprite]:
        """Get all sprites that have the given tag.

        Args:
            tag: The tag to search for

        Returns:
            List[Sprite]: All sprites that have the given tag
        """
        return [s for s in self._sprites if tag in s.tags]

    def get_sprites_by_tags(self, tags: List[str]) -> List[Sprite]:
        """Get all sprites that have all of the given tags.

        Args:
            tags: The tags to search for

        Returns:
            List[Sprite]: All sprites that have all of the given tags
        """
        if not tags:
            return []
        return [s for s in self._sprites if all(tag in s.tags for tag in tags)]

    def get_sprites_by_any_tag(self, tags: List[str]) -> List[Sprite]:
        """Get all sprites that have any of the specified tags.

        Args:
            tags: List of tags to search for

        Returns:
            List[Sprite]: List of sprites that have any of the specified tags
        """
        return [sprite for sprite in self._sprites if any(tag in sprite.tags for tag in tags)]

    def get_all_tags(self) -> set[str]:
        """Get all unique tags from all sprites in the level.

        This method collects all tags from all sprites and returns them as a set,
        ensuring each tag appears only once in the result.

        Returns:
            set[str]: A set containing all unique tags from all sprites
        """
        all_tags = set()
        for sprite in self._sprites:
            all_tags.update(sprite.tags)
        return all_tags

    def get_sprite_at(self, x: int, y: int, tag: Optional[str] = None, ignore_collidable: bool = False) -> Sprite | None:
        """Get the sprite at the given coordinates.

        This method returns the first sprite that is at the given coordinates.
        If a tag is provided, it will return the first sprite that has the given tag.

        Args:
            x: The x coordinate
            y: The y coordinate
            tag: The tag to search for
        """
        sprites = sorted(self._sprites, key=lambda sprite: sprite.layer, reverse=True)
        for sprite in sprites:
            if (ignore_collidable or sprite.is_collidable) and x >= sprite.x and y >= sprite.y and x < sprite.x + sprite.width and y < sprite.y + sprite.height:
                if sprite.blocking == BlockingMode.PIXEL_PERFECT:
                    pixels = sprite.render()
                    if pixels[y - sprite.y][x - sprite.x] == -1:
                        continue
                if tag is None or tag in sprite.tags:
                    return sprite
        return None

    def collides_with(self, sprite: Sprite, ignoreMode: bool = False) -> List[Sprite]:
        """Checks all sprites in the level for collisions with the given sprite.

        Args:
            sprite: The sprite to check for collisions
        """
        return [s for s in self._sprites if sprite.collides_with(other=s, ignoreMode=ignoreMode)]

    @property
    def name(self) -> str:
        """Get the name of the level."""
        return self._name

    def get_data(self, key: str) -> Any:
        return self._data.get(key)

    @property
    def grid_size(self) -> Tuple[int, int] | None:
        """Get the grid size of the level.

        Returns:
            Tuple[int, int]: The grid size of the level
        """
        return self._grid_size

    def clone(self) -> "Level":
        """Create a deep copy of this level.

        Returns:
            Level: A new Level instance with cloned sprites
        """
        # Clone each sprite and create new level
        cloned_sprites = [sprite.clone() for sprite in self._sprites]
        return Level(name=self._name, sprites=cloned_sprites, grid_size=self._grid_size, data=copy.deepcopy(self._data))
