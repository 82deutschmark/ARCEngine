"""Tests for the level module."""

import unittest
from arcengine import Level, Sprite

class TestLevel(unittest.TestCase):
    """Test cases for the Level class."""

    def test_sprite_management(self):
        """Test basic sprite management functionality."""
        level = Level()
        
        # Test empty level
        self.assertEqual(len(level.get_sprites()), 0)
        
        # Create some test sprites
        sprite1 = Sprite([[1]], name="box")
        sprite2 = Sprite([[2]], name="box")
        sprite3 = Sprite([[3]], name="player")
        
        # Test adding sprites
        level.add_sprite(sprite1)
        self.assertEqual(len(level.get_sprites()), 1)
        
        level.add_sprite(sprite2)
        level.add_sprite(sprite3)
        self.assertEqual(len(level.get_sprites()), 3)
        
        # Test getting sprites by name
        boxes = level.get_sprites_by_name("box")
        self.assertEqual(len(boxes), 2)
        self.assertIn(sprite1, boxes)
        self.assertIn(sprite2, boxes)
        
        players = level.get_sprites_by_name("player")
        self.assertEqual(len(players), 1)
        self.assertEqual(players[0], sprite3)
        
        # Test removing sprites
        level.remove_sprite(sprite1)
        self.assertEqual(len(level.get_sprites()), 2)
        self.assertEqual(len(level.get_sprites_by_name("box")), 1)
        
        # Test removing non-existent sprite (should not raise)
        level.remove_sprite(sprite1)
        self.assertEqual(len(level.get_sprites()), 2)
        
        # Verify get_sprites() returns a copy
        sprites = level.get_sprites()
        sprites.clear()  # Should not affect the level's sprites
        self.assertEqual(len(level.get_sprites()), 2)
        
    def test_sprite_list_constructor(self):
        """Test constructing a level with an initial sprite list."""
        # Create test sprites
        sprite1 = Sprite([[1]], name="box")
        sprite2 = Sprite([[2]], name="player")
        
        # Create level with sprites
        level = Level(sprites=[sprite1, sprite2])
        
        # Verify sprites were added
        self.assertEqual(len(level.get_sprites()), 2)
        self.assertEqual(len(level.get_sprites_by_name("box")), 1)
        self.assertEqual(len(level.get_sprites_by_name("player")), 1)
        
    def test_level_clone(self):
        """Test cloning a level with all its sprites."""
        # Create original level with sprites
        sprite1 = Sprite([[1]], name="box", x=10, y=20)
        sprite2 = Sprite([[2]], name="player", x=30, y=40)
        original = Level(sprites=[sprite1, sprite2])
        
        # Clone the level
        cloned = original.clone()
        
        # Verify same number of sprites
        self.assertEqual(len(cloned.get_sprites()), len(original.get_sprites()))
        
        # Get sprites by name from both levels
        orig_box = original.get_sprites_by_name("box")[0]
        clone_box = cloned.get_sprites_by_name("box")[0]
        
        # Verify sprites have same properties but are different objects
        self.assertNotEqual(id(orig_box), id(clone_box))  # Different objects
        self.assertEqual(orig_box.name, clone_box.name)   # Same name
        self.assertEqual(orig_box.x, clone_box.x)         # Same position
        self.assertEqual(orig_box.y, clone_box.y)
        
        # Modify original sprite, verify clone is unaffected
        orig_box.set_position(50, 60)
        self.assertEqual(clone_box.x, 10)  # Original position
        self.assertEqual(clone_box.y, 20) 