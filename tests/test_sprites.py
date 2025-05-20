"""Tests for the sprites module."""

import unittest

import numpy as np

from arcengine import BlockingMode, InteractionMode, Sprite


class TestSprite(unittest.TestCase):
    """Test cases for the Sprite class."""

    def test_sprite_initialization(self):
        """Test basic sprite initialization with different input types."""
        # Test with valid 2D list
        pixels_list = [[1, 2], [3, 4]]
        sprite = Sprite(pixels_list)
        self.assertTrue(np.array_equal(sprite.pixels, np.array(pixels_list, dtype=np.int8)))
        self.assertEqual(sprite.x, 0)
        self.assertEqual(sprite.y, 0)
        self.assertEqual(sprite.scale, 1)
        self.assertEqual(sprite.rotation, 0)
        self.assertEqual(sprite.blocking, BlockingMode.NOT_BLOCKED)
        self.assertEqual(sprite.interaction, InteractionMode.TANGIBLE)

        # Test with custom parameters
        sprite = Sprite(
            pixels_list,
            x=10,
            y=20,
            scale=2,
            rotation=90,
            blocking=BlockingMode.BOUNDING_BOX,
            interaction=InteractionMode.INTANGIBLE,
        )
        self.assertTrue(np.array_equal(sprite.pixels, np.array(pixels_list, dtype=np.int8)))
        self.assertEqual(sprite.x, 10)
        self.assertEqual(sprite.y, 20)
        self.assertEqual(sprite.scale, 2)
        self.assertEqual(sprite.rotation, 90)
        self.assertEqual(sprite.blocking, BlockingMode.BOUNDING_BOX)
        self.assertEqual(sprite.interaction, InteractionMode.INTANGIBLE)

        # Test invalid rotation on init
        with self.assertRaises(ValueError):
            Sprite(pixels_list, rotation=45)

        # Test invalid scale on init
        with self.assertRaises(ValueError) as ctx:
            Sprite(pixels_list, scale=0)
        self.assertEqual(str(ctx.exception), "Scale cannot be zero")

        # Test invalid downscale on init
        with self.assertRaises(ValueError) as ctx:
            Sprite(pixels_list, scale=-3)
        self.assertIn("must be divisible by scale factor", str(ctx.exception))

    def test_invalid_inputs(self):
        """Test that invalid inputs raise appropriate errors."""
        # Test with 1D list
        with self.assertRaises(ValueError):
            Sprite([1, 2, 3])

        # Test with numpy array (should fail)
        with self.assertRaises(ValueError):
            Sprite(np.array([[1, 2], [3, 4]]))

        # Test with invalid nested structure
        with self.assertRaises(ValueError):
            Sprite([[1, 2], 3])

        # Test with empty list
        with self.assertRaises(ValueError):
            Sprite([])

    def test_scale_validation(self):
        """Test that scale cannot be set to zero and validates downscale factors."""
        # Create a 6x6 sprite to test various scale factors
        pixels = [
            [1, 1, 1, 2, 2, 2],
            [1, 1, 1, 2, 2, 2],
            [1, 1, 1, 2, 2, 2],
            [3, 3, 3, 4, 4, 4],
            [3, 3, 3, 4, 4, 4],
            [3, 3, 3, 4, 4, 4],
        ]
        sprite = Sprite(pixels)

        # Test setting valid scales
        valid_scales = [1, 2, 3, -1, -2]  # -1 = half size, -2 = one-third size
        for scale in valid_scales:
            sprite.set_scale(scale)
            self.assertEqual(sprite.scale, scale)

        # Test setting scale to zero
        with self.assertRaises(ValueError) as ctx:
            sprite.set_scale(0)
        self.assertEqual(str(ctx.exception), "Scale cannot be zero")

        # Test invalid downscale factors
        with self.assertRaises(ValueError) as ctx:
            sprite.set_scale(-3)  # Would try to divide by 4, 6x6 not divisible by 4
        self.assertIn("must be divisible by scale factor", str(ctx.exception))

        # Test scale remains unchanged after failed set
        self.assertEqual(sprite.scale, valid_scales[-1])

    def test_adjust_scale(self):
        """Test the adjust_scale method."""
        # Create a 6x6 sprite to test various scale factors
        pixels = [
            [1, 1, 1, 2, 2, 2],
            [1, 1, 1, 2, 2, 2],
            [1, 1, 1, 2, 2, 2],
            [3, 3, 3, 4, 4, 4],
            [3, 3, 3, 4, 4, 4],
            [3, 3, 3, 4, 4, 4],
        ]
        sprite = Sprite(pixels)

        # Test no change
        sprite.set_scale(2)
        sprite.adjust_scale(0)
        self.assertEqual(sprite.scale, 2)

        # Test positive adjustments
        sprite.set_scale(1)
        sprite.adjust_scale(2)  # 1 -> 2 -> 3
        self.assertEqual(sprite.scale, 3)

        # Test negative adjustments (downscaling)
        sprite.set_scale(1)
        sprite.adjust_scale(-2)  # 1 -> 0 -> -1 (half size)
        self.assertEqual(sprite.scale, -1)  # -1 means half size

        # Test moving from downscale to upscale
        sprite.set_scale(-2)  # one-third size
        sprite.adjust_scale(3)  # -2 -> -1 -> 0 -> 1
        self.assertEqual(sprite.scale, 1)

        # Test moving from upscale to downscale
        sprite.set_scale(2)
        sprite.adjust_scale(-3)  # 2 -> 1 -> 0 -> -1 (half size)
        self.assertEqual(sprite.scale, -1)

        # Test invalid scale transitions
        with self.assertRaises(ValueError) as ctx:
            sprite.set_scale(1)
            sprite.adjust_scale(-4)  # Would try to reach -3, which needs factor of 4
        self.assertIn("must be divisible by scale factor", str(ctx.exception))

    def test_rotation_methods(self):
        """Test the set_rotation and rotate methods."""
        sprite = Sprite([[1, 2], [3, 4]])

        # Test set_rotation with valid values
        valid_rotations = [0, 90, 180, 270]
        for rotation in valid_rotations:
            sprite.set_rotation(rotation)
            self.assertEqual(sprite.rotation, rotation)

        # Test set_rotation with invalid values
        invalid_rotations = [45, 100, 200, -45]
        for rotation in invalid_rotations:
            with self.assertRaises(ValueError):
                sprite.set_rotation(rotation)

        # Test rotate with valid deltas
        sprite.set_rotation(0)
        sprite.rotate(90)  # 0 -> 90
        self.assertEqual(sprite.rotation, 90)
        sprite.rotate(90)  # 90 -> 180
        self.assertEqual(sprite.rotation, 180)
        sprite.rotate(90)  # 180 -> 270
        self.assertEqual(sprite.rotation, 270)
        sprite.rotate(90)  # 270 -> 0
        self.assertEqual(sprite.rotation, 0)

        # Test negative rotations
        sprite.set_rotation(0)
        sprite.rotate(-90)  # 0 -> 270
        self.assertEqual(sprite.rotation, 270)
        sprite.rotate(-90)  # 270 -> 180
        self.assertEqual(sprite.rotation, 180)
        sprite.rotate(-90)  # 180 -> 90
        self.assertEqual(sprite.rotation, 90)
        sprite.rotate(-90)  # 90 -> 0
        self.assertEqual(sprite.rotation, 0)

        # Test wraparound cases
        sprite.set_rotation(270)
        sprite.rotate(90)  # 270 -> 0
        self.assertEqual(sprite.rotation, 0)

        sprite.set_rotation(0)
        sprite.rotate(-90)  # 0 -> 270
        self.assertEqual(sprite.rotation, 270)

        sprite.set_rotation(0)
        sprite.rotate(-180)  # 0 -> 270
        self.assertEqual(sprite.rotation, 180)

        sprite.set_rotation(180)
        sprite.rotate(180)  # 0 -> 270
        self.assertEqual(sprite.rotation, 0)

        sprite.set_rotation(0)
        sprite.rotate(-270)  # 0 -> 270
        self.assertEqual(sprite.rotation, 90)

        sprite.set_rotation(180)
        sprite.rotate(270)  # 0 -> 270
        self.assertEqual(sprite.rotation, 90)

        # Test rotate with invalid deltas
        with self.assertRaises(ValueError):
            sprite.rotate(45)

        # Test rotation normalization
        sprite.set_rotation(360)  # Should normalize to 0
        self.assertEqual(sprite.rotation, 0)
        sprite.set_rotation(450)  # Should normalize to 90
        self.assertEqual(sprite.rotation, 90)
        sprite.rotate(360)  # Should stay at 90
        self.assertEqual(sprite.rotation, 90)

    def test_sprite_render_no_transform(self):
        """Test sprite rendering without any transformations."""
        pixels = [[1, 2], [3, 4]]
        sprite = Sprite(pixels)
        rendered = sprite.render()
        self.assertTrue(np.array_equal(rendered, np.array(pixels, dtype=np.int8)))
        self.assertEqual(rendered.dtype, np.int8)

    def test_sprite_render_rotation(self):
        """Test sprite rotation rendering."""
        pixels = [[1, 2], [3, 4]]

        # Test 90 degree rotation (clockwise)
        sprite = Sprite(pixels, rotation=90)
        expected_90 = np.array([[3, 1], [4, 2]], dtype=np.int8)
        rendered = sprite.render()
        self.assertTrue(np.array_equal(rendered, expected_90))

        # Test 180 degree rotation
        sprite.set_rotation(180)
        expected_180 = np.array([[4, 3], [2, 1]], dtype=np.int8)
        rendered = sprite.render()
        self.assertTrue(np.array_equal(rendered, expected_180))

        # Test 270 degree rotation
        sprite.set_rotation(270)
        expected_270 = np.array([[2, 4], [1, 3]], dtype=np.int8)
        rendered = sprite.render()
        self.assertTrue(np.array_equal(rendered, expected_270))

        # Test negative rotation
        sprite.set_rotation(0)
        sprite.rotate(-90)  # Should be equivalent to 270
        rendered = sprite.render()
        self.assertTrue(np.array_equal(rendered, expected_270))

    def test_sprite_render_scaling(self):
        """Test sprite scaling rendering."""
        pixels = [
            [1, 1, 1, 2, 2, 2],
            [1, 1, 1, 2, 2, 2],
            [1, 1, 1, 2, 2, 2],
            [3, 3, 3, 4, 4, 4],
            [3, 3, 3, 4, 4, 4],
            [3, 3, 3, 4, 4, 4],
        ]

        # Test upscaling by 2
        sprite = Sprite(pixels, scale=2)
        expected_upscale = np.array(
            [
                [1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2],
                [1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2],
                [1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2],
                [1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2],
                [1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2],
                [1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2],
                [3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4],
                [3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4],
                [3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4],
                [3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4],
                [3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4],
                [3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4],
            ],
            dtype=np.int8,
        )
        rendered = sprite.render()
        self.assertTrue(np.array_equal(rendered, expected_upscale))

        # Test downscaling by 2 (scale=-1, half size)
        sprite = Sprite(pixels, scale=-1)
        expected_downscale = np.array(
            [
                [1, 2, 2],
                [3, 4, 4],
                [3, 4, 4],
            ],
            dtype=np.int8,
        )
        rendered = sprite.render()
        self.assertTrue(np.array_equal(rendered, expected_downscale))

        # Test downscaling by 3 (scale=-2, one-third size)
        sprite = Sprite(pixels, scale=-2)
        expected_downscale = np.array(
            [
                [1, 2],
                [3, 4],
            ],
            dtype=np.int8,
        )
        rendered = sprite.render()
        self.assertTrue(np.array_equal(rendered, expected_downscale))

    def test_sprite_render_combined(self):
        """Test sprite rendering with both rotation and scaling."""
        pixels = [
            [1, 1, 1, 2, 2, 2],
            [1, 1, 1, 2, 2, 2],
            [1, 1, 1, 2, 2, 2],
            [3, 3, 3, 4, 4, 4],
            [3, 3, 3, 4, 4, 4],
            [3, 3, 3, 4, 4, 4],
        ]

        # Test 90 degree rotation with scale 2
        sprite = Sprite(pixels, rotation=90, scale=2)
        expected = np.array(
            [
                [3, 3, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1],
                [3, 3, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1],
                [3, 3, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1],
                [3, 3, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1],
                [3, 3, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1],
                [3, 3, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1],
                [4, 4, 4, 4, 4, 4, 2, 2, 2, 2, 2, 2],
                [4, 4, 4, 4, 4, 4, 2, 2, 2, 2, 2, 2],
                [4, 4, 4, 4, 4, 4, 2, 2, 2, 2, 2, 2],
                [4, 4, 4, 4, 4, 4, 2, 2, 2, 2, 2, 2],
                [4, 4, 4, 4, 4, 4, 2, 2, 2, 2, 2, 2],
                [4, 4, 4, 4, 4, 4, 2, 2, 2, 2, 2, 2],
            ],
            dtype=np.int8,
        )
        rendered = sprite.render()
        self.assertTrue(np.array_equal(rendered, expected))

        # Test 90 degree rotation with scale -2 (one-third size)
        sprite = Sprite(pixels, rotation=90, scale=-2)
        expected = np.array(
            [
                [3, 1],
                [4, 2],
            ],
            dtype=np.int8,
        )
        rendered = sprite.render()
        self.assertTrue(np.array_equal(rendered, expected))

    def test_sprite_clone(self):
        """Test sprite cloning functionality."""
        # Create original sprite with some non-default values
        pixels = [[1, 2], [3, 4]]
        original = Sprite(
            pixels=pixels,
            name="original",
            x=10,
            y=20,
            scale=2,
            rotation=90,
            blocking=BlockingMode.BOUNDING_BOX,
        )

        # Create clone with default name (should be the same name)
        clone1 = original.clone()
        self.assertTrue(np.array_equal(clone1.pixels, original.pixels))
        self.assertEqual(clone1.x, original.x)
        self.assertEqual(clone1.y, original.y)
        self.assertEqual(clone1.scale, original.scale)
        self.assertEqual(clone1.rotation, original.rotation)
        self.assertEqual(clone1.blocking, original.blocking)
        self.assertEqual(clone1.name, original.name)  # Should get new UUID

        # Create clone with specific name
        clone2 = original.clone(new_name="clone2")
        self.assertEqual(clone2.name, "clone2")

        # Verify independence of clones
        original.set_position(30, 40)
        original.set_rotation(180)
        original.set_scale(3)
        self.assertEqual(clone1.x, 10)  # Should keep original values
        self.assertEqual(clone1.y, 20)
        self.assertEqual(clone1.rotation, 90)
        self.assertEqual(clone1.scale, 2)

        # Modify pixels of original
        original.pixels[0, 0] = 9
        self.assertEqual(clone1.pixels[0, 0], 1)  # Should keep original value

        # Verify rendered output is independent
        original_rendered = original.render()
        clone1_rendered = clone1.render()
        self.assertFalse(np.array_equal(original_rendered, clone1_rendered))

    def test_interaction_mode(self):
        """Test interaction mode functionality."""
        # Test sprite interaction mode
        sprite = Sprite([[1]], interaction=InteractionMode.TANGIBLE)
        self.assertTrue(sprite.is_visible)
        self.assertTrue(sprite.is_collidable)

        sprite.set_interaction(InteractionMode.INTANGIBLE)
        self.assertTrue(sprite.is_visible)
        self.assertFalse(sprite.is_collidable)

        sprite.set_interaction(InteractionMode.INVISIBLE)
        self.assertFalse(sprite.is_visible)
        self.assertTrue(sprite.is_collidable)

        sprite.set_interaction(InteractionMode.REMOVED)
        self.assertFalse(sprite.is_visible)
        self.assertFalse(sprite.is_collidable)

    def test_collision_basic_rules(self):
        """Test basic collision rules (self-collision and collidable status)."""
        sprite1 = Sprite([[1]], x=0, y=0, blocking=BlockingMode.BOUNDING_BOX)
        sprite2 = Sprite([[1]], x=0, y=0, blocking=BlockingMode.BOUNDING_BOX)

        # Test self-collision
        self.assertFalse(sprite1.collides_with(sprite1))

        # Test non-collidable interaction modes
        sprite1.set_interaction(InteractionMode.INTANGIBLE)
        self.assertFalse(sprite1.collides_with(sprite2))
        sprite1.set_interaction(InteractionMode.TANGIBLE)
        sprite2.set_interaction(InteractionMode.REMOVED)
        self.assertFalse(sprite1.collides_with(sprite2))

        # Test NOT_BLOCKED mode
        sprite1.set_interaction(InteractionMode.TANGIBLE)
        sprite2.set_interaction(InteractionMode.TANGIBLE)
        sprite1.set_blocking(BlockingMode.NOT_BLOCKED)
        self.assertFalse(sprite1.collides_with(sprite2))
        sprite1.set_blocking(BlockingMode.BOUNDING_BOX)
        sprite2.set_blocking(BlockingMode.NOT_BLOCKED)
        self.assertFalse(sprite1.collides_with(sprite2))

    def test_bounding_box_collision(self):
        """Test bounding box collision detection."""
        # Create two 2x2 sprites
        sprite1 = Sprite([[1, 1], [1, 1]], blocking=BlockingMode.BOUNDING_BOX)
        sprite2 = Sprite([[2, 2], [2, 2]], blocking=BlockingMode.BOUNDING_BOX)

        # Test no collision when sprites are apart
        sprite1.set_position(0, 0)
        sprite2.set_position(3, 3)
        self.assertFalse(sprite1.collides_with(sprite2))

        # Test collision when sprites overlap
        sprite2.set_position(1, 1)
        self.assertTrue(sprite1.collides_with(sprite2))

        # Test collision is commutative
        self.assertTrue(sprite2.collides_with(sprite1))

        # Test edge touching counts as collision
        sprite2.set_position(2, 2)
        self.assertFalse(sprite1.collides_with(sprite2))

        # Test with scaled sprites
        sprite1.set_scale(2)  # Now 4x4
        sprite2.set_position(3, 3)
        self.assertTrue(sprite1.collides_with(sprite2))

        # Test with rotated sprites
        sprite1.set_rotation(90)  # Rotation shouldn't affect bounding box
        self.assertTrue(sprite1.collides_with(sprite2))

        # Test with invisible but collidable sprite
        sprite2.set_interaction(InteractionMode.INVISIBLE)
        self.assertTrue(sprite1.collides_with(sprite2))

    def test_pixel_perfect_collision(self):
        """Test pixel-perfect collision detection."""
        # Create two sprites with transparent pixels (-1)
        sprite1 = Sprite([[-1, 1], [1, -1]], blocking=BlockingMode.PIXEL_PERFECT)

        sprite2 = Sprite([[2, -1], [-1, 2]], blocking=BlockingMode.PIXEL_PERFECT)

        # Test no collision when sprites are apart
        sprite1.set_position(0, 0)
        sprite2.set_position(3, 3)
        self.assertFalse(sprite1.collides_with(sprite2))

        # Test no collision when transparent pixels overlap
        sprite2.set_position(1, 1)  # Overlaps only on transparent pixels
        self.assertFalse(sprite1.collides_with(sprite2))

        # Test collision when non-transparent pixels overlap
        sprite2.set_position(1, 0)  # Direct overlap of non-transparent pixels
        self.assertTrue(sprite1.collides_with(sprite2))

        # Test with one sprite using PIXEL_PERFECT and other using BOUNDING_BOX
        sprite2.set_blocking(BlockingMode.BOUNDING_BOX)
        sprite2.set_position(1, 1)  # Would collide with bounding box, but not pixels
        self.assertFalse(sprite1.collides_with(sprite2))

        # Test with scaled sprites
        sprite1.set_scale(2)  # Now 4x4 with scaled transparent pixels
        sprite2.set_position(2, 0)
        self.assertTrue(sprite1.collides_with(sprite2))  # Non-transparent pixels overlap

        # Test with rotated sprites
        sprite1.set_rotation(90)
        sprite2.set_position(0, 0)
        self.assertTrue(sprite1.collides_with(sprite2))  # Should still collide after rotation

    def test_sprite_movement(self):
        """Test sprite movement functionality."""
        sprite = Sprite([[1]], x=5, y=5)
        self.assertEqual(sprite.x, 5)
        self.assertEqual(sprite.y, 5)

        # Test positive movement
        sprite.move(3, 2)
        self.assertEqual(sprite.x, 8)
        self.assertEqual(sprite.y, 7)

        # Test negative movement
        sprite.move(-4, -3)
        self.assertEqual(sprite.x, 4)
        self.assertEqual(sprite.y, 4)

        # Test zero movement
        sprite.move(0, 0)
        self.assertEqual(sprite.x, 4)
        self.assertEqual(sprite.y, 4)

        # Test movement affects collision detection
        sprite1 = Sprite([[1]], blocking=BlockingMode.BOUNDING_BOX)
        sprite2 = Sprite([[2]], blocking=BlockingMode.BOUNDING_BOX)

        sprite1.set_position(0, 0)
        sprite2.set_position(2, 2)
        self.assertFalse(sprite1.collides_with(sprite2))

        sprite1.move(1, 1)
        sprite2.move(-1, -1)
        self.assertTrue(sprite1.collides_with(sprite2))

        # Test with floating point values (should be converted to int)
        sprite.move(1.7, -2.3)
        self.assertEqual(sprite.x, 5)  # 4 + 1
        self.assertEqual(sprite.y, 2)  # 4 - 2


if __name__ == "__main__":
    unittest.main()
