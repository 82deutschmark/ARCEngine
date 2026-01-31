# Author: Claude Sonnet 4
# Date: 2026-01-31
# PURPOSE: World Shifter game logic - the world moves, not you.
#          Core mechanic: player is FIXED, world shifts inversely to input.
#          Collision checks if player center would be on a wall pixel.
# SRP/DRY check: Pass - proper inverse-movement mechanic with pixel collision

"""World Shifter game implementation - Inverse Movement Puzzle."""

from arcengine import ARCBaseGame, Camera, GameAction, Level, Sprite, ToggleableUserDisplay
from games.world_shifter.levels import LEVELS
from games.world_shifter.sprites import ENERGY_PILL, ENERGY_PILL_OFF

# Game identification
GAME_ID = "world_shifter"
VERSION = "0.02"  # Fixed collision detection

# ARC3 Colors - dark background makes floating platforms pop
BACKGROUND_COLOR = 5  # Black - dark void behind floating platforms
LETTERBOX_COLOR = 5   # Black - seamless border

# Wall color in the maze sprites (gray = 2 means blocked)
WALL_COLOR = 2

# Energy configuration - bar at BOTTOM of 64x64 canvas
MAX_ENERGY = 30  # 30 pills = 60 pixels wide at bottom


class WorldShifter(ARCBaseGame):
    """
    The world moves around you, not the other way around.

    A puzzle game where player input moves the entire world in the opposite direction.
    Navigate floating platforms by shifting them toward your fixed position.
    Bring the exit TO you - you cannot move to it.

    Features:
    - Energy tracking: Each move costs 1 energy. Run out and you lose!
    - 6 creative levels with unique floating platform designs
    - Inverse movement creates mind-bending spatial puzzles
    """

    _player: Sprite
    _maze: Sprite
    _energy_ui: ToggleableUserDisplay
    _energy_remaining: int

    def __init__(self) -> None:
        """Initialize the game with camera, energy UI, and levels."""
        # Create energy UI - pills along BOTTOM edge (row 62-63)
        # 30 pills * 2 pixels = 60 pixels, centered with 2px padding each side
        sprite_pairs = []
        for i in range(MAX_ENERGY):
            on_pill = ENERGY_PILL.clone().set_position(2 + i * 2, 62)
            off_pill = ENERGY_PILL_OFF.clone().set_position(2 + i * 2, 62)
            sprite_pairs.append((on_pill, off_pill))

        self._energy_ui = ToggleableUserDisplay(sprite_pairs)

        # Full 64x64 camera - no letterboxing
        camera = Camera(
            width=64,
            height=64,
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
        """Cache references when level loads."""
        self._player = level.get_sprites_by_name("player")[0]
        self._maze = level.get_sprites_by_tag("maze")[0]

        # Reset energy for new level
        self._energy_ui.enable_all_by_tag("energy")
        self._energy_remaining = MAX_ENERGY

    def step(self) -> None:
        """Process one game step with inverse movement."""
        # Determine intended movement direction from input
        # Player presses UP -> world moves DOWN (player effectively moves up relative to world)
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
                self._energy_remaining -= 1

        # Check lose condition (out of energy)
        if moved and self._energy_remaining <= 0:
            self.lose()
            self.complete_action()
            return

        # Check win condition (exit overlaps player position)
        if self._check_exit_collision():
            if self.is_last_level():
                self.win()
            else:
                self.next_level()

        self.complete_action()

    def _get_player_center(self) -> tuple[int, int]:
        """Get the center pixel position of the player sprite."""
        # Player is 3x3, center is at (x+1, y+1)
        return self._player.x + 1, self._player.y + 1

    def _is_wall_at_position(self, world_x: int, world_y: int) -> bool:
        """
        Check if there's a wall at the given world position.
        Returns True if the position is outside the maze or on a wall pixel.
        """
        # Convert world position to maze-local coordinates
        local_x = world_x - self._maze.x
        local_y = world_y - self._maze.y

        # Check bounds - outside maze is considered blocked (void)
        if local_y < 0 or local_y >= len(self._maze.pixels):
            return True
        if local_x < 0 or local_x >= len(self._maze.pixels[0]):
            return True

        # Check pixel color: -1 is transparent (walkable), WALL_COLOR (2) is blocked
        pixel = self._maze.pixels[local_y][local_x]
        return pixel == WALL_COLOR

    def _can_move_world(self, dx: int, dy: int) -> bool:
        """
        Check if world can move in the given direction.
        
        The world moving by (dx, dy) is equivalent to the player moving by (-dx, -dy)
        relative to the world. We check if the player's center would be on a wall.
        """
        player_cx, player_cy = self._get_player_center()
        
        # After world moves by (dx, dy), the player's position relative to the maze
        # changes by (-dx, -dy). So we check the new relative position.
        # In world coords, player stays at (player_cx, player_cy)
        # Maze moves to (maze.x + dx, maze.y + dy)
        # So player's local coords in maze become:
        #   local_x = player_cx - (maze.x + dx) = (player_cx - maze.x) - dx
        #   local_y = player_cy - (maze.y + dy) = (player_cy - maze.y) - dy
        # This is equivalent to checking position (player_cx, player_cy) with maze at new position
        
        # Temporarily calculate what the position would be
        new_maze_x = self._maze.x + dx
        new_maze_y = self._maze.y + dy
        
        local_x = player_cx - new_maze_x
        local_y = player_cy - new_maze_y
        
        # Check bounds
        if local_y < 0 or local_y >= len(self._maze.pixels):
            return False  # Would fall into void
        if local_x < 0 or local_x >= len(self._maze.pixels[0]):
            return False  # Would fall into void
        
        # Check if on wall pixel
        pixel = self._maze.pixels[local_y][local_x]
        if pixel == WALL_COLOR:
            return False  # Would be inside wall
        
        return True

    def _move_world(self, dx: int, dy: int) -> None:
        """Move all moveable sprites in the given direction."""
        moveable = self.current_level.get_sprites_by_tag("moveable")
        for sprite in moveable:
            sprite.move(dx, dy)

    def _check_exit_collision(self) -> bool:
        """
        Check if exit sprite overlaps with player.
        Uses center-point collision for precision.
        """
        exit_sprites = self.current_level.get_sprites_by_tag("exit")
        if not exit_sprites:
            return False
        exit_sprite = exit_sprites[0]
        
        # Get player center
        player_cx, player_cy = self._get_player_center()
        
        # Get exit center (exit is 3x3)
        exit_cx = exit_sprite.x + 1
        exit_cy = exit_sprite.y + 1
        
        # Check if centers are within 1 pixel (overlapping)
        return abs(player_cx - exit_cx) <= 1 and abs(player_cy - exit_cy) <= 1
