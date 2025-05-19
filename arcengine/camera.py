"""
Module for camera-related functionality in the ARCEngine.
"""

from typing import List, Tuple

import numpy as np

from arcengine.sprites import Sprite


class Camera:
    """A camera that defines the viewport into the game world."""

    # Maximum allowed dimensions
    MAX_DIMENSION = 64

    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        width: int = 64,
        height: int = 64,
        background: int = 5,
        letter_box: int = 5,
    ):
        """Initialize a new Camera.

        Args:
            x: X coordinate in pixels (default: 0)
            y: Y coordinate in pixels (default: 0)
            width: Viewport width in pixels (default: 64, max: 64)
            height: Viewport height in pixels (default: 64, max: 64)
            background: Background color index (default: 5 - Black)
            letter_box: Letter box color index (default: 5 - Black)

        Raises:
            ValueError: If width or height exceed 64 pixels
        """
        self._x = int(x)
        self._y = int(y)

        # Validate and set dimensions
        width_int = int(width)
        height_int = int(height)
        if width_int > self.MAX_DIMENSION:
            raise ValueError(f"Width cannot exceed {self.MAX_DIMENSION} pixels")
        if height_int > self.MAX_DIMENSION:
            raise ValueError(f"Height cannot exceed {self.MAX_DIMENSION} pixels")
        self._width = width_int
        self._height = height_int

        self._background = int(background)
        self._letter_box = int(letter_box)

    def _calculate_scale_and_offset(self) -> Tuple[int, int, int]:
        """Calculate the scale factor and offsets for letterboxing.

        Returns:
            Tuple[int, int, int]: (scale, x_offset, y_offset)
            - scale: The uniform scale factor to fit viewport in 64x64
            - x_offset: Horizontal offset for centering
            - y_offset: Vertical offset for centering
        """
        # Calculate maximum possible scale that fits in MAX_DIMENSION
        scale_x = self.MAX_DIMENSION // self._width
        scale_y = self.MAX_DIMENSION // self._height
        scale = min(scale_x, scale_y)

        # Calculate scaled dimensions
        scaled_width = self._width * scale
        scaled_height = self._height * scale

        # Only use offsets if we can't scale up to fill the screen
        x_offset = (self.MAX_DIMENSION - scaled_width) // 2
        y_offset = (self.MAX_DIMENSION - scaled_height) // 2

        return scale, x_offset, y_offset

    def _raw_render(self, sprites: List[Sprite]) -> np.ndarray:
        """Internal method to render the camera view.

        Args:
            sprites: List of sprites to render. Sprites are rendered in order of their layer
                    value (lower layers first). Negative pixel values are treated as transparent.
                    Only visible sprites (based on their interaction mode) will be rendered.

        Returns:
            np.ndarray: The rendered view as a 2D numpy array
        """
        # Create background array filled with background color
        output = np.full((self._height, self._width), self._background, dtype=np.int8)

        if not sprites:
            return output

        # Sort sprites by layer (lower layers first) and filter out non-visible sprites
        sorted_sprites = sorted(
            (s for s in sprites if s.is_visible), key=lambda s: s.layer
        )

        for sprite in sorted_sprites:
            # Get the sprite's rendered pixels (handles rotation and scaling)
            sprite_pixels = sprite.render()
            sprite_height, sprite_width = sprite_pixels.shape

            # Calculate sprite position relative to camera
            rel_x = sprite.x - self._x
            rel_y = sprite.y - self._y

            # Calculate the intersection with viewport
            dest_x_start = max(0, rel_x)
            dest_x_end = min(self._width, rel_x + sprite_width)
            dest_y_start = max(0, rel_y)
            dest_y_end = min(self._height, rel_y + sprite_height)

            # Skip if sprite is completely outside viewport
            if dest_x_end <= dest_x_start or dest_y_end <= dest_y_start:
                continue

            # Calculate source region from sprite
            sprite_x_start = max(0, -rel_x)
            sprite_x_end = sprite_width - max(0, (rel_x + sprite_width) - self._width)
            sprite_y_start = max(0, -rel_y)
            sprite_y_end = sprite_height - max(
                0, (rel_y + sprite_height) - self._height
            )

            # Get the sprite region we're going to copy
            sprite_region = sprite_pixels[
                sprite_y_start:sprite_y_end, sprite_x_start:sprite_x_end
            ]

            # Create a mask for non-negative (visible) pixels
            visible_mask = sprite_region >= 0

            # Update only the non-transparent pixels
            output[dest_y_start:dest_y_end, dest_x_start:dest_x_end][visible_mask] = (
                sprite_region[visible_mask]
            )

        return output

    def render(self, sprites: List[Sprite]) -> np.ndarray:
        """Render the camera view.

        The rendered output is always 64x64 pixels. If the camera's viewport is smaller,
        the view will be scaled up uniformly (maintaining aspect ratio) to fit within
        64x64, and the remaining space will be filled with the letter_box color.

        Args:
            sprites: List of sprites to render (currently unused)

        Returns:
            np.ndarray: The rendered view as a 64x64 numpy array
        """
        # Start with a letter-boxed canvas
        output = np.full(
            (self.MAX_DIMENSION, self.MAX_DIMENSION), self._letter_box, dtype=np.int8
        )

        # Get the raw camera view
        view = self._raw_render(sprites)

        # Calculate scaling and offsets
        scale, x_offset, y_offset = self._calculate_scale_and_offset()

        # Scale up the view using numpy's repeat
        if scale > 1:
            view = np.repeat(np.repeat(view, scale, axis=0), scale, axis=1)

        # Insert the scaled view into the letter-boxed output
        output[
            y_offset : y_offset + view.shape[0], x_offset : x_offset + view.shape[1]
        ] = view

        return output
