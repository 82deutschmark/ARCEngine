"""
Module for sprite-related classes and functionality in the ARCEngine.
"""

import uuid
from typing import List, Optional

import numpy as np
from numpy import ndarray

from .enums import BlockingMode, InteractionMode


def _downscale_mode(arr: np.ndarray, factor: int) -> np.ndarray:
    """
    Nearest-neighbor style down-scaling for palette images.
    For each non-overlapping block it keeps the dominant color
    (mode), breaking ties by the highest palette index.

    Parameters
    ----------
    arr : 2-D np.ndarray
        Input image of dtype int8 / uint8 holding palette indices.
    factor : int
        The integer scale factor (e.g. 2 turns 64×64 → 32×32).

    Returns
    -------
    np.ndarray
        The down-scaled image, same dtype as the input.

    Raises
    ------
    ValueError
        If the array dimensions are not divisible by the scale factor.
    """
    H, W = arr.shape
    if H % factor != 0 or W % factor != 0:
        raise ValueError(f"Array dimensions ({H}, {W}) must be divisible by scale factor {factor}")

    # Step 1: split into blocks → shape (out_h, out_w, factor, factor)
    blocks = arr.reshape(H // factor, factor, -1, factor).swapaxes(1, 2)
    blocks = blocks.reshape(-1, factor * factor)

    # Step 2: find dominant color for each block
    max_index = arr.max()  # upper bound for palette indices
    out = np.empty(len(blocks), dtype=arr.dtype)

    for i, blk in enumerate(blocks):
        cnts = np.bincount(blk.astype(np.int16), minlength=max_index + 1)
        # Get the indices where we have the maximum count
        max_count = cnts.max()
        max_indices = np.where(cnts == max_count)[0]
        # Among the most frequent values, pick the highest
        out[i] = max_indices[-1]

    # Step 3: reshape to 2-D image
    return out.reshape(H // factor, W // factor)


class Sprite:
    """A 2D sprite that can be positioned and scaled in the game world."""

    # Valid rotation values in degrees (clockwise)
    VALID_ROTATIONS = {0, 90, 180, 270}

    pixels: ndarray
    _name: str
    _x: int
    _y: int
    _layer: int
    _rotation: int
    _mirror_ud: bool
    _mirror_lr: bool
    _scale: int  # Use set_scale to validate scale factor
    _blocking: BlockingMode
    _interaction: InteractionMode
    _tags: list[str]

    def __init__(
        self,
        pixels: List[List[int]],
        name: Optional[str] = None,
        x: int = 0,
        y: int = 0,
        layer: int = 0,
        scale: int = 1,
        rotation: int = 0,
        mirror_ud: bool = False,
        mirror_lr: bool = False,
        blocking: BlockingMode = BlockingMode.NOT_BLOCKED,
        interaction: InteractionMode = InteractionMode.TANGIBLE,
        tags: list[str] = [],
    ):
        """Initialize a new Sprite.

        Args:
            pixels: 2D list representing the sprite's pixels
            name: Sprite name (default: None, will generate UUID)
            x: X coordinate in pixels (default: 0)
            y: Y coordinate in pixels (default: 0)
            layer: Z-order layer for rendering (default: 0, higher values render on top)
            scale: Scale factor (default: 1)
            rotation: Rotation in degrees (default: 0)
            blocking: Collision detection method (default: NOT_BLOCKED)
            interaction: How the sprite interacts with the game world (default: TANGIBLE)

        Raises:
            ValueError: If scale is 0, pixels is not a 2D list, rotation is invalid,
                       or if downscaling factor doesn't evenly divide sprite dimensions
        """
        if not isinstance(pixels, list) or not all(isinstance(row, list) for row in pixels):
            raise ValueError("Pixels must be a 2D list")

        self.pixels = np.array(pixels, dtype=np.int8)
        if self.pixels.ndim != 2:
            raise ValueError("Pixels must be a 2D array")

        self._name = name if name is not None else str(uuid.uuid4())
        self._x = int(x)
        self._y = int(y)
        self._layer = int(layer)
        self._set_rotation(rotation)
        self._mirror_ud = mirror_ud
        self._mirror_lr = mirror_lr
        self._blocking = blocking
        self.set_scale(scale)  # Use set_scale to validate scale factor
        self._interaction = interaction
        self._tags = tags

    def clone(self, new_name: Optional[str] = None) -> "Sprite":
        """Create an independent copy of this sprite.

        Args:
            new_name: Optional name for the cloned sprite. If None, reuses current name.

        Returns:
            A new Sprite instance with the same properties but independent state.
        """
        # Create a deep copy of the pixels array
        pixels_copy = self.pixels.copy()

        # Create a new sprite with copied properties
        return Sprite(
            pixels=pixels_copy.tolist(),  # Convert back to list for constructor
            name=new_name if new_name is not None else self._name,  # Use new name or generate new UUID
            x=self._x,
            y=self._y,
            scale=self._scale,
            rotation=self.rotation,  # Use the public property to get normalized value
            mirror_ud=self._mirror_ud,
            mirror_lr=self._mirror_lr,
            blocking=self._blocking,
            layer=self._layer,
            interaction=self._interaction,
            tags=self._tags.copy(),  # Copy the tags list
        )

    def _set_rotation(self, rotation: int) -> None:
        """Internal method to set rotation with validation.

        Args:
            rotation: The rotation value in degrees

        Raises:
            ValueError: If rotation is not a valid 90-degree increment
        """
        normalized = rotation % 360
        if normalized not in self.VALID_ROTATIONS:
            raise ValueError(f"Rotation must be one of {self.VALID_ROTATIONS}, got {rotation}")
        self.rotation = normalized

    def set_rotation(self, rotation: int) -> "Sprite":
        """Set the sprite's rotation to a specific value.

        Args:
            rotation: The new rotation in degrees (must be 0, 90, 180, or 270)

        Raises:
            ValueError: If rotation is not a valid 90-degree increment
        """
        self._set_rotation(int(rotation))
        return self

    def rotate(self, delta: int) -> "Sprite":
        """Rotate the sprite by a given amount.

        Args:
            delta: The change in rotation in degrees (must result in a valid rotation)

        Raises:
            ValueError: If resulting rotation is not a valid 90-degree increment
        """
        if delta < 0:
            delta = 360 + (delta % 360)
        new_rotation = (self.rotation + delta) % 360
        self._set_rotation(new_rotation)
        return self

    def set_position(self, x: int, y: int) -> "Sprite":
        """Set the sprite's position.

        Args:
            x: New X coordinate in pixels
            y: New Y coordinate in pixels
        """
        self._x = int(x)
        self._y = int(y)
        return self

    def set_scale(self, scale: int) -> "Sprite":
        """Set the sprite's scale factor.

        Args:
            scale: The new scale factor. Positive values scale up, negative values scale down.
                  Negative values indicate divisor: -1 means half size (divide by 2), -2 means one-third size, etc.

        Raises:
            ValueError: If scale is 0 or if downscaling factor doesn't evenly divide sprite dimensions
        """
        scale_int = int(scale)
        if scale_int == 0:
            raise ValueError("Scale cannot be zero")

        # For downscaling, validate dimensions are divisible by scale factor
        if scale_int < 0:
            H, W = self.pixels.shape
            factor = -scale_int + 1  # -1 -> 2, -2 -> 3, -3 -> 4, etc.
            if H % factor != 0 or W % factor != 0:
                raise ValueError(f"Array dimensions ({H}, {W}) must be divisible by scale factor {factor}")

        self._scale = scale_int
        return self

    def adjust_scale(self, delta: int) -> None:
        """Adjust the sprite's scale by a delta value, moving one step at a time.

        The method will adjust the scale by incrementing or decrementing by 1
        repeatedly until reaching the target scale. This ensures smooth transitions
        and validates each step.

        Negative scales indicate downscaling factors:
        -1 = half size (1/2)
        -2 = one-third size (1/3)
        -3 = one-fourth size (1/4)
        etc.

        For example:
        - Current scale 1, delta +2 -> Steps through: 1 -> 2 -> 3
        - Current scale 1, delta -2 -> Steps through: 1 -> 0 -> -1 (half size)
        - Current scale -2, delta +3 -> Steps through: -2 -> -1 -> 0 -> 1

        Args:
            delta: The total change in scale to apply. Positive values increase scale,
                  negative values decrease it.

        Raises:
            ValueError: If any intermediate scale would be 0 or if a downscaling factor
                       doesn't evenly divide sprite dimensions
        """
        if delta == 0:
            return

        # Determine direction of change
        step = 1 if delta > 0 else -1
        target_scale = self._scale + delta

        # Take steps one at a time
        while self._scale != target_scale:
            next_scale = self._scale + step

            # Skip over zero since it's invalid
            if next_scale == 0:
                next_scale = step

            # Let ValueError propagate up
            self.set_scale(next_scale)

    def set_blocking(self, blocking: BlockingMode) -> "Sprite":
        """Set the sprite's blocking behavior.

        Args:
            blocking: The new blocking behavior
        """
        if not isinstance(blocking, BlockingMode):
            raise ValueError("blocking must be a BlockingMode enum value")
        self._blocking = blocking
        return self

    def set_name(self, name: str) -> "Sprite":
        """Set the sprite's name.

        Args:
            name: New name for the sprite
        """
        if not name:
            raise ValueError("Name cannot be empty")
        self._name = name
        return self

    @property
    def name(self) -> str:
        """Get the sprite's name."""
        return self._name

    @property
    def x(self) -> int:
        """Get the current X coordinate."""
        return self._x

    @property
    def y(self) -> int:
        """Get the current Y coordinate."""
        return self._y

    @property
    def scale(self) -> int:
        """Get the current scale factor."""
        return self._scale

    @property
    def blocking(self) -> BlockingMode:
        """Get the current blocking behavior."""
        return self._blocking

    @property
    def layer(self) -> int:
        """Get the current rendering layer."""
        return self._layer

    @property
    def tags(self) -> list[str]:
        """Get the current tags."""
        return self._tags

    @property
    def mirror_ud(self) -> bool:
        """Get the current mirror up/down state."""
        return self._mirror_ud

    @property
    def mirror_lr(self) -> bool:
        """Get the current mirror left/right state."""
        return self._mirror_lr

    def set_mirror_ud(self, mirror_ud: bool) -> "Sprite":
        """Set the sprite's mirror up/down state."""
        self._mirror_ud = mirror_ud
        return self

    def set_mirror_lr(self, mirror_lr: bool) -> "Sprite":
        """Set the sprite's mirror left/right state."""
        self._mirror_lr = mirror_lr
        return self

    def set_layer(self, layer: int) -> "Sprite":
        """Set the sprite's rendering layer.

        Args:
            layer: New layer value. Higher values render on top.
        """
        self._layer = int(layer)
        return self

    @property
    def interaction(self) -> InteractionMode:
        """Get the current interaction mode."""
        return self._interaction

    def set_interaction(self, interaction: InteractionMode) -> "Sprite":
        """Set the sprite's interaction mode.

        Args:
            interaction: The new interaction mode

        Raises:
            ValueError: If interaction is not an InteractionMode enum value
        """
        if not isinstance(interaction, InteractionMode):
            raise ValueError("interaction must be an InteractionMode enum value")
        self._interaction = interaction
        return self

    @property
    def is_visible(self) -> bool:
        """Check if a sprite with this interaction mode should be rendered.

        Returns:
            bool: True if the sprite should be visible, False otherwise
        """
        return self._interaction in {
            InteractionMode.TANGIBLE,
            InteractionMode.INTANGIBLE,
        }

    @property
    def width(self) -> int:
        """Get the sprite's width."""
        return int(self.pixels.shape[1])

    @property
    def height(self) -> int:
        """Get the sprite's height."""
        return int(self.pixels.shape[0])

    @property
    def is_collidable(self) -> bool:
        """Check if a sprite with this interaction mode should participate in collisions.

        Returns:
            bool: True if the sprite should be checked for collisions, False otherwise
        """
        return self._interaction in {
            InteractionMode.TANGIBLE,
            InteractionMode.INVISIBLE,
        }

    def render(self) -> np.ndarray:
        """Render the sprite with current scale and rotation.

        Returns:
            np.ndarray: The rendered sprite as a 2D numpy array
        """
        # Start with the base pixels
        result = self.pixels.copy()

        # Handle rotation first (if any)
        if self.rotation != 0:
            # Convert degrees to number of 90-degree rotations (clockwise)
            k = int((-self.rotation % 360) / 90)  # Negative for clockwise rotation
            if k != 0:
                result = np.rot90(result, k=k)

        if self._mirror_ud:
            result = np.flipud(result)
        if self._mirror_lr:
            result = np.fliplr(result)

        # Handle scaling
        if self._scale != 1:
            if self._scale > 1:
                # For upscaling, repeat the array in both dimensions
                result = np.repeat(np.repeat(result, self._scale, axis=0), self._scale, axis=1)
            else:  # self._scale < 0
                # For downscaling, use mode-based approach
                # Convert negative scale to actual divisor (e.g. -1 -> 2, -2 -> 3)
                factor = -self._scale + 1  # -1 -> 2, -2 -> 3, -3 -> 4, etc.
                result = _downscale_mode(result, factor)

        return result

    def collides_with(self, other: "Sprite") -> bool:
        """Check if this sprite collides with another sprite.

        The collision check follows these rules:
        1. A sprite cannot collide with itself
        2. Non-collidable sprites (based on interaction mode) never collide
        3. For collidable sprites, the collision detection method is based on their blocking mode:
           - NOT_BLOCKED: Always returns False
           - BOUNDING_BOX: Simple rectangular collision check
           - PIXEL_PERFECT: Precise pixel-level collision detection

        Args:
            other: The other sprite to check collision with

        Returns:
            bool: True if the sprites collide, False otherwise
        """
        # Rule 1: A sprite cannot collide with itself
        if self is other:
            return False

        # Rule 2: Both sprites must be collidable
        if not (self.is_collidable and other.is_collidable):
            return False

        # Rule 3: Handle different blocking modes
        if self._blocking == BlockingMode.NOT_BLOCKED or other._blocking == BlockingMode.NOT_BLOCKED:
            return False

        # Get sprite dimensions after rendering (accounts for rotation and scaling)
        self_pixels = self.render()
        other_pixels = other.render()
        self_height, self_width = self_pixels.shape
        other_height, other_width = other_pixels.shape

        # First check bounding box collision
        # If there's no bounding box collision, there can't be pixel collision
        if self._x >= other._x + other_width or self._x + self_width <= other._x or self._y >= other._y + other_height or self._y + self_height <= other._y:
            return False

        # If either sprite uses PIXEL_PERFECT, do pixel-level collision detection
        if self._blocking == BlockingMode.PIXEL_PERFECT or other._blocking == BlockingMode.PIXEL_PERFECT:
            # Calculate intersection region
            x_min = max(self._x, other._x)
            x_max = min(self._x + self_width, other._x + other_width)
            y_min = max(self._y, other._y)
            y_max = min(self._y + self_height, other._y + other_height)

            # Get the overlapping regions from both sprites
            self_x_start = x_min - self._x
            self_x_end = x_max - self._x
            self_y_start = y_min - self._y
            self_y_end = y_max - self._y

            other_x_start = x_min - other._x
            other_x_end = x_max - other._x
            other_y_start = y_min - other._y
            other_y_end = y_max - other._y

            # Extract overlapping regions
            self_region = self_pixels[self_y_start:self_y_end, self_x_start:self_x_end]
            other_region = other_pixels[other_y_start:other_y_end, other_x_start:other_x_end]

            # Check if any non-transparent pixels overlap
            self_mask = self_region != -1
            other_mask = other_region != -1
            return bool(np.any(self_mask & other_mask))

        # Otherwise, we already know there's a bounding box collision
        return True

    def move(self, dx: int, dy: int) -> None:
        """Move the sprite by the given deltas.

        Args:
            dx: Change in x position (positive = right, negative = left)
            dy: Change in y position (positive = down, negative = up)
        """
        self._x += int(dx)
        self._y += int(dy)
