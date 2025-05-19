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
        self.assertEqual(orig_box.name, clone_box.name)  # Same name
        self.assertEqual(orig_box.x, clone_box.x)  # Same position
        self.assertEqual(orig_box.y, clone_box.y)

        # Modify original sprite, verify clone is unaffected
        orig_box.set_position(50, 60)
        self.assertEqual(clone_box.x, 10)  # Original position
        self.assertEqual(clone_box.y, 20)

    def test_sprite_tags(self):
        """Test sprite tag-related functionality."""
        # Create test sprites with various tags
        sprite1 = Sprite([[1]], name="enemy1", tags=["enemy", "flying"])
        sprite2 = Sprite([[2]], name="enemy2", tags=["enemy", "ground"])
        sprite3 = Sprite([[3]], name="player", tags=["player", "ground"])
        sprite4 = Sprite([[4]], name="obstacle", tags=["obstacle"])

        # Create level with sprites
        level = Level(sprites=[sprite1, sprite2, sprite3, sprite4])

        # Test get_sprites_by_tag
        enemies = level.get_sprites_by_tag("enemy")
        self.assertEqual(len(enemies), 2)
        self.assertIn(sprite1, enemies)
        self.assertIn(sprite2, enemies)

        ground_units = level.get_sprites_by_tag("ground")
        self.assertEqual(len(ground_units), 2)
        self.assertIn(sprite2, ground_units)
        self.assertIn(sprite3, ground_units)

        # Test get_sprites_by_tags (AND)
        flying_enemies = level.get_sprites_by_tags(["enemy", "flying"])
        self.assertEqual(len(flying_enemies), 1)
        self.assertEqual(flying_enemies[0], sprite1)

        ground_enemies = level.get_sprites_by_tags(["enemy", "ground"])
        self.assertEqual(len(ground_enemies), 1)
        self.assertEqual(ground_enemies[0], sprite2)

        # Test get_sprites_by_any_tag (OR)
        ground_or_flying = level.get_sprites_by_any_tag(["ground", "flying"])
        self.assertEqual(len(ground_or_flying), 3)
        self.assertIn(sprite1, ground_or_flying)  # flying
        self.assertIn(sprite2, ground_or_flying)  # ground
        self.assertIn(sprite3, ground_or_flying)  # ground

        # Test with non-existent tags
        self.assertEqual(len(level.get_sprites_by_tag("nonexistent")), 0)
        self.assertEqual(len(level.get_sprites_by_tags(["enemy", "nonexistent"])), 0)
        self.assertEqual(len(level.get_sprites_by_any_tag(["nonexistent"])), 0)

        # Test with empty tag list
        self.assertEqual(len(level.get_sprites_by_tags([])), 0)
        self.assertEqual(len(level.get_sprites_by_any_tag([])), 0)

        all_tags = level.get_all_tags()
        self.assertEqual(len(all_tags), 5)
        self.assertIn("enemy", all_tags)
        self.assertIn("flying", all_tags)
        self.assertIn("ground", all_tags)
        self.assertIn("obstacle", all_tags)
        self.assertIn("player", all_tags)
