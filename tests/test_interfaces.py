"""Tests for the interfaces module."""

import unittest

import numpy as np

from arcengine import (
    Sprite,
    ToggleableUserDisplay,
)


class TestToggleableUserDisplay(unittest.TestCase):
    """Test cases for the ToggleableUserDisplay class."""

    def test_initialization(self):
        """Test initialization with sprite pairs."""
        # Create test sprites
        sprite1 = Sprite([[1, 1], [1, 1]], name="sprite1")
        sprite2 = Sprite([[2, 2], [2, 2]], name="sprite2")
        sprite3 = Sprite([[3, 3], [3, 3]], name="sprite3")
        sprite4 = Sprite([[4, 4], [4, 4]], name="sprite4")

        # Create toggleable UI element with sprite pairs
        ui_element = ToggleableUserDisplay([(sprite1, sprite2), (sprite3, sprite4)])

        # Verify sprites were cloned
        self.assertEqual(len(ui_element._sprite_pairs), 2)
        self.assertIsNot(ui_element._sprite_pairs[0][0], sprite1)
        self.assertIsNot(ui_element._sprite_pairs[0][1], sprite2)
        self.assertIsNot(ui_element._sprite_pairs[1][0], sprite3)
        self.assertIsNot(ui_element._sprite_pairs[1][1], sprite4)

    def test_enable_disable(self):
        """Test enabling and disabling sprite pairs."""
        # Create test sprites
        sprite1 = Sprite([[1, 1], [1, 1]], name="sprite1")
        sprite2 = Sprite([[2, 2], [2, 2]], name="sprite2")
        ui_element = ToggleableUserDisplay([(sprite1, sprite2)])

        # Test enabling
        ui_element.enable(0)
        self.assertTrue(ui_element.is_enabled(0))

        # Test disabling
        ui_element.disable(0)
        self.assertFalse(ui_element.is_enabled(0))

        # Test invalid index
        with self.assertRaises(ValueError):
            ui_element.enable(1)
        with self.assertRaises(ValueError):
            ui_element.disable(1)

    def test_render_interface(self):
        """Test rendering sprites to a frame."""
        # Create test sprites with different layers
        sprite1 = Sprite([[1, 1], [1, 1]], name="sprite1", x=0, y=0, layer=1)
        sprite2 = Sprite([[2, 2], [2, 2]], name="sprite2", x=1, y=1, layer=2)
        sprite3 = Sprite([[3, 3], [3, 3]], name="sprite3", x=2, y=2, layer=0)
        sprite4 = Sprite([[4, 4], [4, 4]], name="sprite4", x=3, y=3, layer=3)

        # Create toggleable UI element
        ui_element = ToggleableUserDisplay([(sprite1, sprite2), (sprite3, sprite4)])

        # Enable first pair, disable second pair
        ui_element.enable(0)
        ui_element.disable(1)

        # Create frame and render
        frame = np.zeros((64, 64), dtype=np.int32)
        ui_element.render_interface(frame)

        # Verify frame was modified
        # Verify sprite1 is visible (enabled)
        self.assertEqual(frame[0, 0], 1)
        self.assertEqual(frame[0, 1], 1)
        self.assertEqual(frame[1, 0], 1)
        self.assertEqual(frame[1, 1], 1)

        # Verify sprite2 is not visible (disabled)
        self.assertEqual(frame[1, 1], 1)  # Overwritten by sprite1
        self.assertEqual(frame[1, 2], 0)
        self.assertEqual(frame[2, 1], 0)
        self.assertEqual(frame[2, 2], 0)

        # Verify sprite3 is not visible (disabled)
        self.assertEqual(frame[2, 2], 0)
        self.assertEqual(frame[2, 3], 0)
        self.assertEqual(frame[3, 2], 0)
        self.assertEqual(frame[3, 3], 4)  # Overwritten by sprite4

        # Verify sprite4 is visible (enabled)
        self.assertEqual(frame[3, 3], 4)
        self.assertEqual(frame[3, 4], 4)
        self.assertEqual(frame[4, 3], 4)
        self.assertEqual(frame[4, 4], 4)

    def test_render_interface_clipping(self):
        """Test rendering sprites that extend beyond frame boundaries."""
        # Create a sprite that extends beyond frame boundaries
        sprite1 = Sprite([[1, 1], [1, 1]], name="sprite1", x=63, y=63)
        sprite2 = Sprite([[2, 2], [2, 2]], name="sprite2", x=62, y=62)
        ui_element = ToggleableUserDisplay([(sprite1, sprite2)])

        # Enable the sprite pair
        ui_element.enable(0)

        # Create frame and render
        frame = np.zeros((64, 64), dtype=np.int32)
        ui_element.render_interface(frame)

        # Verify only visible portion was rendered
        self.assertEqual(frame[63, 63], 1)  # Only one pixel should be visible
        self.assertEqual(frame[62, 63], 0)  # Rest should be clipped
        self.assertEqual(frame[63, 62], 0)  # Rest should be clipped
