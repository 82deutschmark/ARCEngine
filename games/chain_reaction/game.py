# Author: Claude Sonnet 4
# Date: 2026-01-31
# PURPOSE: Main game logic for Chain Reaction using FULL 64x64 canvas.
#          Sokoban-style block pushing with move counter at bottom.
# SRP/DRY check: Pass - game class designed for 64x64 canvas like official ARC3 games

"""Chain Reaction game implementation - Full 64x64 canvas design."""

from arcengine import ARCBaseGame, BlockingMode, Camera, GameAction, InteractionMode, Level, Sprite, ToggleableUserDisplay
from games.chain_reaction.levels import LEVELS
from games.chain_reaction.sprites import MOVE_COUNTER, MOVE_COUNTER_OFF

# Game identification
GAME_ID = "chain_reaction"
VERSION = "0.01"  # Initial release

# ARC3 Colors
BACKGROUND_COLOR = 3  # Dark Gray - floor color like official games
LETTERBOX_COLOR = 5   # Black - outer border

# Move configuration - bar at BOTTOM of 64x64 canvas
MAX_MOVES = 25  # 25 pills = 50 pixels wide at bottom

# Color tags used for matching
COLOR_TAGS = {"red", "blue", "yellow", "purple", "pink", "lightblue"}


class ChainReaction(ARCBaseGame):
    """
    Push colored blocks into matching pairs to clear the board.

    A Sokoban-style puzzle game where pushing colored blocks into matching
    blocks destroys both. Clear all colored blocks to unlock the exit.

    Features:
    - Move tracking: Each move costs 1 from your move budget. Run out and you lose!
    - 6 levels of increasing difficulty with more color pairs
    - Unique game_id-version identifier: chain_reaction-1.0.0
    """

    _player: Sprite
    _exit: Sprite
    _move_ui: ToggleableUserDisplay
    _moves_remaining: int

    def __init__(self) -> None:
        """Initialize the game with camera, move UI, and levels."""
        # Create move counter UI - pills along BOTTOM edge (row 62-63)
        # 25 pills * 2 pixels = 50 pixels, centered with 7px padding each side
        sprite_pairs = []
        for i in range(MAX_MOVES):
            on_counter = MOVE_COUNTER.clone().set_position(7 + i * 2, 62)
            off_counter = MOVE_COUNTER_OFF.clone().set_position(7 + i * 2, 62)
            sprite_pairs.append((on_counter, off_counter))

        self._move_ui = ToggleableUserDisplay(sprite_pairs)

        # Full 64x64 camera - no letterboxing
        camera = Camera(
            width=64,
            height=64,
            background=BACKGROUND_COLOR,
            letter_box=LETTERBOX_COLOR,
            interfaces=[self._move_ui],
        )
        super().__init__(
            game_id=f"{GAME_ID}-{VERSION}",
            levels=LEVELS,
            camera=camera,
        )

    def on_set_level(self, level: Level) -> None:
        """Cache references when level loads."""
        self._player = level.get_sprites_by_name("player")[0]
        exit_sprites = level.get_sprites_by_tag("exit")
        if exit_sprites:
            self._exit = exit_sprites[0]

        # Reset move counter for new level
        self._move_ui.enable_all_by_tag("moves")
        self._moves_remaining = MAX_MOVES

    def step(self) -> None:
        """Process one game step."""
        # Determine movement direction from input
        dx, dy = 0, 0
        if self.action.id == GameAction.ACTION1:  # Up
            dy = -1
        elif self.action.id == GameAction.ACTION2:  # Down
            dy = 1
        elif self.action.id == GameAction.ACTION3:  # Left
            dx = -1
        elif self.action.id == GameAction.ACTION4:  # Right
            dx = 1

        # Try to move player
        moved = False
        if dx != 0 or dy != 0:
            moved = self._try_move_player(dx, dy)
            if moved:
                # Consume a move
                self._move_ui.disabled_first_by_tag("moves")
                self._moves_remaining -= 1

        # Check lose condition (out of moves)
        if moved and self._moves_remaining <= 0:
            self.lose()
            self.complete_action()
            return

        # Update exit state based on remaining blocks
        self._update_exit_state()

        # Check if player reached unlocked exit
        if self._is_exit_unlocked() and self._player_on_exit():
            if self.is_last_level():
                self.win()
            else:
                self.next_level()

        self.complete_action()

    def _try_move_player(self, dx: int, dy: int) -> bool:
        """Attempt to move player, handling block pushing. Returns True if moved."""
        target_x = self._player.x + dx
        target_y = self._player.y + dy

        # Check what's at the target position
        blocking_sprite = self._get_blocking_sprite_at(target_x, target_y)

        if blocking_sprite is None:
            # Empty space - just move
            self._player.move(dx, dy)
            return True
        elif "pushable" in blocking_sprite.tags:
            # Found a pushable block - try to push it
            return self._try_push_block(blocking_sprite, dx, dy)
        # If blocked by wall or non-pushable, do nothing
        return False

    def _get_blocking_sprite_at(self, x: int, y: int) -> Sprite | None:
        """Get blocking sprite at position, if any."""
        for sprite in self.current_level.get_sprites():
            if sprite.interaction == InteractionMode.REMOVED:
                continue
            if sprite == self._player:
                continue
            if sprite.blocking == BlockingMode.NOT_BLOCKED:
                continue

            # Check if sprite occupies this position
            if self._sprite_occupies_position(sprite, x, y):
                return sprite
        return None

    def _sprite_occupies_position(self, sprite: Sprite, x: int, y: int) -> bool:
        """Check if a sprite occupies the given position."""
        # Get sprite bounds
        sprite_left = sprite.x
        sprite_top = sprite.y
        sprite_right = sprite.x + len(sprite.pixels[0]) - 1
        sprite_bottom = sprite.y + len(sprite.pixels) - 1

        return sprite_left <= x <= sprite_right and sprite_top <= y <= sprite_bottom

    def _try_push_block(self, block: Sprite, dx: int, dy: int) -> bool:
        """Attempt to push a block, handling matches. Returns True if player moved."""
        # Calculate where block would move
        block_target_x = block.x + dx
        block_target_y = block.y + dy

        # Check what's at the block's target position
        target_sprite = self._get_blocking_sprite_at(block_target_x, block_target_y)

        if target_sprite is None:
            # Empty space - move block and player
            block.move(dx, dy)
            self._player.move(dx, dy)
            return True
        elif "colored" in target_sprite.tags:
            # Check if colors match
            if self._check_match(block, target_sprite):
                # Colors match! Destroy both blocks
                self._destroy_pair(block, target_sprite)
                # Player moves into now-empty space
                self._player.move(dx, dy)
                return True
            # If colors don't match, block can't move
        # If blocked by wall or other non-matching obstacle, do nothing
        return False

    def _check_match(self, block1: Sprite, block2: Sprite) -> bool:
        """Check if two blocks have the same color tag."""
        if "colored" not in block2.tags:
            return False

        # Find color tag for each block
        block1_color = self._get_color_tag(block1)
        block2_color = self._get_color_tag(block2)

        return block1_color is not None and block1_color == block2_color

    def _get_color_tag(self, sprite: Sprite) -> str | None:
        """Get the color tag from a sprite's tags."""
        for tag in sprite.tags:
            if tag in COLOR_TAGS:
                return tag
        return None

    def _destroy_pair(self, block1: Sprite, block2: Sprite) -> None:
        """Remove both blocks from play."""
        block1.set_interaction(InteractionMode.REMOVED)
        block2.set_interaction(InteractionMode.REMOVED)

    def _count_remaining_blocks(self) -> int:
        """Count how many colored blocks remain."""
        count = 0
        for sprite in self.current_level.get_sprites():
            if "colored" in sprite.tags and sprite.interaction != InteractionMode.REMOVED:
                count += 1
        return count

    def _is_exit_unlocked(self) -> bool:
        """Check if exit should be unlocked (all blocks cleared)."""
        return self._count_remaining_blocks() == 0

    def _update_exit_state(self) -> None:
        """Update exit sprite appearance based on state."""
        if self._is_exit_unlocked():
            # Change exit to unlocked appearance (green)
            self._exit.pixels = [[14, 14], [14, 14]]
            if "locked" in self._exit.tags:
                self._exit.tags.remove("locked")

    def _player_on_exit(self) -> bool:
        """Check if player overlaps with exit."""
        return self._player.collides_with(self._exit)
