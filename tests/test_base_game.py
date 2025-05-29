"""Tests for the base game module."""

import unittest

import numpy as np

from arcengine import (
    ActionInput,
    ARCBaseGame,
    BlockingMode,
    Camera,
    GameAction,
    GameState,
    Level,
    Sprite,
)


class TestGame(ARCBaseGame):
    """Test implementation of TestGame."""

    def __init__(self, game_id: str, levels: list[Level], camera: Camera | None = None) -> None:
        super().__init__(game_id=game_id, levels=levels, camera=camera)
        self._step_count = 0
        self._level_index = -1

    def step(self) -> None:
        """Step the game, completing after 3 steps."""
        self._step_count += 1
        if self._step_count >= 3:
            self.complete_action()

    def on_set_level(self, level: Level) -> None:
        self._level_index = self._current_level_index


class TestARCBaseGame(unittest.TestCase):
    """Test cases for the TestGame class."""

    def test_initialization(self):
        """Test basic game initialization."""
        # Create test levels
        level1 = Level([Sprite([[1]], name="player")])
        level2 = Level([Sprite([[2]], name="enemy")])

        # Test with default camera
        game = TestGame("test_game", [level1, level2])
        self.assertEqual(len(game._levels), 2)
        self.assertEqual(game._current_level_index, 0)
        self.assertEqual(game.camera.width, 64)  # Default camera size
        self.assertEqual(game.camera.height, 64)

        # Test with custom camera
        camera = Camera(width=32, height=32)
        game = TestGame("test_game", [level1, level2], camera=camera)
        self.assertEqual(game.camera.width, 32)
        self.assertEqual(game.camera.height, 32)

        # Test empty levels list
        with self.assertRaises(ValueError) as ctx:
            TestGame("test_game", [])
        self.assertIn("must have at least one level", str(ctx.exception))

    def test_camera_resizes_to_level_size(self):
        """Test basic game initialization."""
        # Create test levels
        level1 = Level([Sprite([[1]], name="player")], grid_size=(8, 8))
        level2 = Level([Sprite([[2]], name="enemy")], grid_size=(12, 12))

        # Test with custom camera
        camera = Camera(width=32, height=32)
        game = TestGame("test_game", [level1, level2], camera=camera)
        self.assertEqual(game.camera.width, 8)
        self.assertEqual(game.camera.height, 8)

        game.set_level(1)
        self.assertEqual(game.camera.width, 12)
        self.assertEqual(game.camera.height, 12)

    def test_level_management(self):
        """Test level management functionality."""
        # Create test levels
        level1 = Level([Sprite([[1]], name="player")])
        level2 = Level([Sprite([[2]], name="enemy")])
        game = TestGame("test_game", [level1, level2])

        # Test current level
        self.assertEqual(game.current_level, game._levels[0])

        # Test level switching
        game.set_level(1)
        self.assertEqual(game.current_level, game._levels[1])

        # Test invalid level index
        with self.assertRaises(IndexError) as ctx:
            game.set_level(2)
        self.assertIn("out of range", str(ctx.exception))

        with self.assertRaises(IndexError) as ctx:
            game.set_level(-1)
        self.assertIn("out of range", str(ctx.exception))

    def test_level_cloning(self):
        """Test that levels are properly cloned."""
        # Create a level with a sprite
        sprite = Sprite([[1]], name="player")
        level = Level([sprite])
        game = TestGame("test_game", [level])

        # Verify the level was cloned
        self.assertIsNot(game._levels[0], level)

        # Verify sprites were cloned
        original_sprites = level.get_sprites()
        game_sprites = game._levels[0].get_sprites()
        self.assertEqual(len(original_sprites), len(game_sprites))
        self.assertIsNot(original_sprites[0], game_sprites[0])

        # Verify modifications to original don't affect game
        sprite.set_position(10, 10)
        self.assertEqual(game_sprites[0].x, 0)  # Should still be at original position

    def test_try_move(self):
        """Test the try_move method."""
        # Create a level with multiple sprites
        player = Sprite([[1]], name="player", x=0, y=0, blocking=BlockingMode.BOUNDING_BOX)
        wall1 = Sprite([[2]], name="wall1", x=2, y=0, blocking=BlockingMode.BOUNDING_BOX)
        wall2 = Sprite([[2]], name="wall2", x=0, y=1, blocking=BlockingMode.BOUNDING_BOX)
        level = Level([player, wall1, wall2])
        game = TestGame("test_game", [level])

        player = game.current_level.get_sprites_by_name("player")[0]

        # Test successful move
        collisions = game.try_move("player", 1, 0)
        self.assertEqual(collisions, [])
        self.assertEqual(player.x, 1)
        self.assertEqual(player.y, 0)

        # Test collision with wall1
        collisions = game.try_move("player", 1, 0)
        self.assertEqual(collisions[0].name, "wall1")
        self.assertEqual(player.x, 1)  # Position should not change
        self.assertEqual(player.y, 0)

        # Test collision with wall2
        player.set_position(0, 0)  # Reset position
        collisions = game.try_move("player", 0, 1)
        self.assertEqual(collisions[0].name, "wall2")
        self.assertEqual(player.x, 0)  # Position should not change
        self.assertEqual(player.y, 0)

        # Test non-existent sprite
        with self.assertRaises(ValueError) as ctx:
            game.try_move("nonexistent", 1, 0)
        self.assertIn("No sprite found with name", str(ctx.exception))

    def test_camera_properties(self):
        """Test camera property getters and setters."""
        game = TestGame("test_game", [Level()])

        # Test initial values
        self.assertEqual(game.camera.x, 0)
        self.assertEqual(game.camera.y, 0)
        self.assertEqual(game.camera.width, 64)
        self.assertEqual(game.camera.height, 64)

        # Test setters
        game.camera.x = 10
        game.camera.y = 20
        game.camera.width = 32
        game.camera.height = 32

        self.assertEqual(game.camera.x, 10)
        self.assertEqual(game.camera.y, 20)
        self.assertEqual(game.camera.width, 32)
        self.assertEqual(game.camera.height, 32)

    def test_perform_action(self):
        """Test performing an action and collecting frames."""
        # Create a test level with a sprite
        sprite = Sprite([[1, 1], [1, 1]], x=0, y=0)
        level = Level([sprite])

        # Create a test game
        game = TestGame("test_game", [level])

        # Create an action input
        action_input = ActionInput(id=GameAction.ACTION1)

        # Perform the action
        frame_data = game.perform_action(action_input)

        # Verify the frame data
        self.assertEqual(frame_data.game_id, "test_game")
        self.assertEqual(frame_data.state, GameState.NOT_FINISHED)
        self.assertEqual(frame_data.score, 0)
        self.assertEqual(frame_data.action_input, action_input)

        # Verify we got 3 frames (one for each step)
        self.assertEqual(len(frame_data.frame), 3)

        # Verify each frame is a 64x64 array
        for frame in frame_data.frame:
            self.assertEqual(len(frame), 64)
            self.assertEqual(len(frame[0]), 64)

        # Verify the sprite is visible in the first frame
        first_frame = np.array(frame_data.frame[0])
        self.assertEqual(first_frame[0, 0], 1)
        self.assertEqual(first_frame[0, 1], 1)
        self.assertEqual(first_frame[1, 0], 1)
        self.assertEqual(first_frame[1, 1], 1)

    def test_multiple_levels(self):
        """Test performing actions with multiple levels."""
        # Create two levels with different sprites
        sprite1 = Sprite([[1, 1], [1, 1]], x=0, y=0)
        sprite2 = Sprite([[2, 2], [2, 2]], x=0, y=0)
        level1 = Level([sprite1])
        level2 = Level([sprite2])

        # Create a test game with both levels
        game = TestGame("test_game", [level1, level2])

        # Perform action on first level
        action_input = ActionInput(id=GameAction.ACTION1)
        frame_data1 = game.perform_action(action_input)

        # Switch to second level
        game.set_level(1)

        # Perform action on second level
        frame_data2 = game.perform_action(action_input)

        # Verify frames show different sprites
        first_frame1 = np.array(frame_data1.frame[0])
        first_frame2 = np.array(frame_data2.frame[0])

        self.assertEqual(first_frame1[0, 0], 1)  # First level shows sprite1
        self.assertEqual(first_frame2[0, 0], 2)  # Second level shows sprite2

    def test_full_reset_gives_fresh_game(self):
        """Test performing actions with multiple levels."""
        # Create two levels with different sprites
        sprite1 = Sprite([[1, 1], [1, 1]], x=0, y=0)
        level1 = Level([sprite1])

        # Create a test game with both levels
        game = TestGame("test_game", [level1])

        # Simulate some game logic
        game_sprite_1 = game.current_level._sprites[0]
        game_sprite_1.set_position(1, 1)
        game._score = 100

        self.assertEqual(game_sprite_1.x, 1)
        self.assertEqual(game_sprite_1.y, 1)
        self.assertEqual(game._score, 100)

        game.full_reset()

        game_sprite_2 = game.current_level._sprites[0]
        self.assertNotEqual(game_sprite_2, game_sprite_1)
        self.assertEqual(game_sprite_2.x, 0)
        self.assertEqual(game._score, 0)

    def test_level_reset_only_resets_current_level(self):
        """Test performing actions with multiple levels."""
        # Create two levels with different sprites
        sprite1 = Sprite([[1, 1], [1, 1]], x=0, y=0)
        level1 = Level([sprite1])
        level2 = Level([sprite1.clone().set_position(1, 1)])

        # Create a test game with both levels
        game = TestGame("test_game", [level1, level2])

        # Simulate some game logic
        game_sprite_1 = game.current_level._sprites[0]
        game_sprite_1.set_position(10, 10)
        game._score = 100

        self.assertEqual(game_sprite_1.x, 10)
        self.assertEqual(game_sprite_1.y, 10)
        self.assertEqual(game._score, 100)

        game.next_level()

        game_sprite_2 = game.current_level._sprites[0]

        self.assertNotEqual(game_sprite_2, game_sprite_1)
        self.assertEqual(game_sprite_2.x, 1)
        self.assertEqual(game_sprite_2.y, 1)
        self.assertEqual(game._score, 101)

        # Simulate some game logic
        game_sprite_2 = game.current_level._sprites[0]
        game_sprite_2.set_position(9, 9)

        self.assertEqual(game._score, 101)
        self.assertNotEqual(game_sprite_2, game_sprite_1)
        self.assertEqual(game_sprite_2.x, 9)
        self.assertEqual(game_sprite_2.y, 9)

    def test_reset_action_count(self):
        """Test that the reset action count is properly set."""
        # Create a test level with a sprite
        sprite = Sprite([[1, 1], [1, 1]], x=0, y=0)
        level1 = Level([sprite])
        level2 = Level([sprite.clone().set_position(1, 1)])

        # Create a test game
        game = TestGame("test_game", [level1, level2])

        game.next_level()

        # Perform an action and simulate a step
        game.perform_action(ActionInput(id=GameAction.ACTION1))
        game_sprite_1 = game.current_level._sprites[0]
        game_sprite_1.move(2, 2)

        game_sprite_1 = game.current_level._sprites[0]
        self.assertEqual(game_sprite_1.x, 3)
        self.assertEqual(game_sprite_1.y, 3)
        self.assertEqual(game._action_count, 1)

        game.perform_action(ActionInput(id=GameAction.RESET))

        game_sprite_2 = game.current_level._sprites[0]
        self.assertEqual(game._action_count, 0)
        self.assertEqual(game._current_level_index, 1)
        self.assertEqual(game_sprite_2.x, 1)
        self.assertEqual(game_sprite_2.y, 1)
        self.assertNotAlmostEqual(game_sprite_1.x, game_sprite_2.x)

        # another reset with no action should do a full reset
        game.perform_action(ActionInput(id=GameAction.RESET))

        game_sprite_3 = game.current_level._sprites[0]
        self.assertEqual(game._action_count, 0)
        self.assertEqual(game._current_level_index, 0)
        self.assertEqual(game_sprite_3.x, 0)
        self.assertEqual(game_sprite_3.y, 0)
        self.assertNotAlmostEqual(game_sprite_1.x, game_sprite_3.x)
        self.assertNotAlmostEqual(game_sprite_2.x, game_sprite_3.x)

    def test_set_level_by_name(self):
        """Test setting the current level by name."""
        # Create a test level with a sprite
        sprite = Sprite([[1, 1], [1, 1]], x=0, y=0)
        level1 = Level([sprite], name="level1")
        level2 = Level([sprite.clone().set_position(1, 1)], name="level2")
        game = TestGame("test_game", [level1, level2])

        game.set_level_by_name("level1")
        self.assertEqual(game.current_level.name, level1.name)
        # check that the on_level_set is called and the level index is set correctly
        self.assertEqual(game._level_index, 0)

        game.set_level_by_name("level2")
        self.assertEqual(game.current_level.name, level2.name)
        # check that the on_level_set is called and the level index is set correctly
        self.assertEqual(game._level_index, 1)

        with self.assertRaises(ValueError) as ctx:
            game.set_level_by_name("nonexistent")
        self.assertIn("not found", str(ctx.exception))
