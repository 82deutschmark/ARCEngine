# Author: Claude Sonnet 4
# Date: 2026-01-31
# PURPOSE: Main game logic for World Shifter. Implements inverse movement where player input
#          moves the world in the opposite direction. Player is conceptually fixed while
#          walls, exit, and obstacles shift around them. Includes energy tracking UI.
# SRP/DRY check: Pass - game class with energy UI, follows ARCBaseGame pattern

"""World Shifter game implementation."""

from arcengine import ARCBaseGame, Camera, GameAction, Level, Sprite, ToggleableUserDisplay
from games.world_shifter.levels import LEVELS
from games.world_shifter.sprites import ENERGY_PILL, ENERGY_PILL_OFF

# Game identification
GAME_ID = "world_shifter"
VERSION = "1.0.0"

# ARC3 Colors
BACKGROUND_COLOR = 5  # Black
LETTERBOX_COLOR = 3   # Dark Gray - creates nice contrast

# Energy configuration
MAX_ENERGY = 30  # Moves before losing


class WorldShifter(ARCBaseGame):
    """
    The world moves around you, not the other way around.

    A puzzle game where player input moves the entire world in the opposite direction.
    Navigate mazes by shifting walls and the exit toward your fixed position.

    Features:
    - Energy tracking: Each move costs 1 energy. Run out and you lose!
    - 10 levels of increasing difficulty
    - Unique game_id-version identifier: world_shifter-1.0.0
    """

    _player: Sprite
    _world_origin_x: int
    _world_origin_y: int
    _energy_ui: ToggleableUserDisplay

    def __init__(self) -> None:
        """Initialize the game with camera, energy UI, and levels."""
        # Create energy UI - pills along top edge (30 total)
        sprite_pairs = []
        for i in range(MAX_ENERGY):
            on_pill = ENERGY_PILL.clone().set_position(i * 2, 0)
            off_pill = ENERGY_PILL_OFF.clone().set_position(i * 2, 0)
            sprite_pairs.append((on_pill, off_pill))

        self._energy_ui = ToggleableUserDisplay(sprite_pairs)

        camera = Camera(
            background=BACKGROUND_COLOR,
            letter_box=LETTERBOX_COLOR,
            interfaces=[self._energy_ui],
        )
        super().__init__(
            game_id=f"{GAME_ID}-{VERSION}",
            levels=LEVELS,
            camera=camera,
        )

    def on_set_level(self, level: Level) -> None:
        """Cache references when level loads and track world origin."""
        self._player = level.get_sprites_by_name("player")[0]

        # Track world origin for boundary checking
        maze = level.get_sprites_by_tag("maze")[0]
        self._world_origin_x = maze.x
        self._world_origin_y = maze.y

        # Reset energy for new level
        self._energy_ui.enable_all_by_tag("energy")

    def step(self) -> None:
        """Process one game step with inverse movement."""
        # Determine intended movement direction from input
        dx, dy = 0, 0
        if self.action.id == GameAction.ACTION1:  # Up pressed
            dy = 1  # World moves DOWN (opposite)
        elif self.action.id == GameAction.ACTION2:  # Down pressed
            dy = -1  # World moves UP (opposite)
        elif self.action.id == GameAction.ACTION3:  # Left pressed
            dx = 1  # World moves RIGHT (opposite)
        elif self.action.id == GameAction.ACTION4:  # Right pressed
            dx = -1  # World moves LEFT (opposite)

        # Try to move world if there's movement input
        moved = False
        if dx != 0 or dy != 0:
            if self._can_move_world(dx, dy):
                self._move_world(dx, dy)
                moved = True
                # Consume energy on successful move
                self._energy_ui.disabled_first_by_tag("energy")

        # Check lose condition (out of energy)
        if moved and self._is_out_of_energy():
            self.lose()
            self.complete_action()
            return

        # Check win condition (exit reached player)
        if self._check_exit_collision():
            if self.is_last_level():
                self.win()
            else:
                self.next_level()

        self.complete_action()

    def _is_out_of_energy(self) -> bool:
        """Check if all energy has been consumed."""
        # Check if any energy pills are still enabled
        return not self._energy_ui.disabled_first_by_tag("energy", disable=False)

    def _get_world_offset(self) -> tuple[int, int]:
        """Calculate current world offset from origin."""
        maze = self.current_level.get_sprites_by_tag("maze")[0]
        offset_x = maze.x - self._world_origin_x
        offset_y = maze.y - self._world_origin_y
        return offset_x, offset_y

    def _can_move_world(self, dx: int, dy: int) -> bool:
        """
        Check if world can move in the given direction.

        Validates:
        1. Movement is within defined bounds
        2. Player won't be inside a wall after movement
        """
        # Get current offset
        current_offset_x, current_offset_y = self._get_world_offset()
        new_offset_x = current_offset_x + dx
        new_offset_y = current_offset_y + dy

        # Check bounds from level data
        min_x = self.current_level.get_data("min_x")
        max_x = self.current_level.get_data("max_x")
        min_y = self.current_level.get_data("min_y")
        max_y = self.current_level.get_data("max_y")

        # Use defaults if not specified
        if min_x is None:
            min_x = -10
        if max_x is None:
            max_x = 10
        if min_y is None:
            min_y = -10
        if max_y is None:
            max_y = 10

        if not (min_x <= new_offset_x <= max_x):
            return False
        if not (min_y <= new_offset_y <= max_y):
            return False

        # Check collision: would player be inside a wall after movement?
        # Simulate the movement and check collision
        maze = self.current_level.get_sprites_by_tag("maze")[0]

        # Temporarily move maze to check collision
        maze.move(dx, dy)
        collides = self._player.collides_with(maze)
        maze.move(-dx, -dy)  # Move back

        return not collides

    def _move_world(self, dx: int, dy: int) -> None:
        """Move all moveable sprites in the given direction."""
        moveable = self.current_level.get_sprites_by_tag("moveable")
        for sprite in moveable:
            sprite.move(dx, dy)

    def _check_exit_collision(self) -> bool:
        """Check if exit sprite overlaps with player."""
        exit_sprites = self.current_level.get_sprites_by_tag("exit")
        if not exit_sprites:
            return False
        exit_sprite = exit_sprites[0]
        return self._player.collides_with(exit_sprite)
