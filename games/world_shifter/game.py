# Author: Claude Opus 4.5
# Date: 2026-01-31
# PURPOSE: Main game logic for World Shifter. Implements inverse movement where player input
#          moves the world in the opposite direction. Player is conceptually fixed while
#          walls, exit, and obstacles shift around them.
# SRP/DRY check: Pass - new game class, follows ARCBaseGame pattern from examples

"""World Shifter game implementation."""

from arcengine import ARCBaseGame, Camera, GameAction, Level, Sprite
from games.world_shifter.levels import LEVELS

BACKGROUND_COLOR = 0  # Black
LETTERBOX_COLOR = 1  # Dark blue


class WorldShifter(ARCBaseGame):
    """
    The world moves around you, not the other way around.

    A puzzle game where player input moves the entire world in the opposite direction.
    Navigate mazes by shifting walls and the exit toward your fixed position.
    """

    _player: Sprite
    _world_origin_x: int
    _world_origin_y: int

    def __init__(self) -> None:
        """Initialize the game with camera and levels."""
        camera = Camera(
            background=BACKGROUND_COLOR,
            letter_box=LETTERBOX_COLOR,
        )
        super().__init__(
            game_id="world_shifter",
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
        if dx != 0 or dy != 0:
            if self._can_move_world(dx, dy):
                self._move_world(dx, dy)

        # Check win condition (exit reached player)
        if self._check_exit_collision():
            if self.is_last_level():
                self.win()
            else:
                self.next_level()

        self.complete_action()

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
