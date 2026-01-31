# Author: Claude Sonnet 4
# Date: 2026-01-31
# PURPOSE: Main game logic for Chain Reaction. Implements Sokoban-style block pushing
#          where matching colored blocks annihilate each other. Clear all blocks to unlock exit.
# SRP/DRY check: Pass - new game class following ARCBaseGame pattern

"""Chain Reaction game implementation."""

from arcengine import ARCBaseGame, Camera, GameAction, InteractionMode, Level, Sprite
from games.chain_reaction.levels import LEVELS

BACKGROUND_COLOR = 5  # Black (ARC3 color 5)
LETTERBOX_COLOR = 4   # Darker Gray (ARC3 color 4)

# Color tags used for matching
COLOR_TAGS = {"red", "blue", "yellow", "purple", "pink", "lightblue"}


class ChainReaction(ARCBaseGame):
    """
    Push colored blocks into matching pairs to clear the board.

    A Sokoban-style puzzle game where pushing colored blocks into matching
    blocks destroys both. Clear all colored blocks to unlock the exit.
    """

    _player: Sprite
    _exit: Sprite

    def __init__(self) -> None:
        """Initialize the game with camera and levels."""
        camera = Camera(
            background=BACKGROUND_COLOR,
            letter_box=LETTERBOX_COLOR,
        )
        super().__init__(
            game_id="chain_reaction",
            levels=LEVELS,
            camera=camera,
        )

    def on_set_level(self, level: Level) -> None:
        """Cache references when level loads."""
        self._player = level.get_sprites_by_name("player")[0]
        exit_sprites = level.get_sprites_by_tag("exit")
        if exit_sprites:
            self._exit = exit_sprites[0]

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
        if dx != 0 or dy != 0:
            self._try_move_player(dx, dy)

        # Update exit state based on remaining blocks
        self._update_exit_state()

        # Check if player reached unlocked exit
        if self._is_exit_unlocked() and self._player_on_exit():
            if self.is_last_level():
                self.win()
            else:
                self.next_level()

        self.complete_action()

    def _try_move_player(self, dx: int, dy: int) -> None:
        """Attempt to move player, handling block pushing."""
        target_x = self._player.x + dx
        target_y = self._player.y + dy

        # Check what's at the target position
        blocking_sprite = self._get_blocking_sprite_at(target_x, target_y)

        if blocking_sprite is None:
            # Empty space - just move
            self._player.move(dx, dy)
        elif "pushable" in blocking_sprite.tags:
            # Found a pushable block - try to push it
            self._try_push_block(blocking_sprite, dx, dy)
        # If blocked by wall or non-pushable, do nothing

    def _get_blocking_sprite_at(self, x: int, y: int) -> Sprite | None:
        """Get blocking sprite at position, if any."""
        for sprite in self.current_level.sprites:
            if sprite.interaction == InteractionMode.REMOVED:
                continue
            if sprite == self._player:
                continue
            if sprite.blocking == sprite.blocking.NONE:
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

    def _try_push_block(self, block: Sprite, dx: int, dy: int) -> None:
        """Attempt to push a block, handling matches."""
        # Calculate where block would move
        block_target_x = block.x + dx
        block_target_y = block.y + dy

        # Check what's at the block's target position
        target_sprite = self._get_blocking_sprite_at(block_target_x, block_target_y)

        if target_sprite is None:
            # Empty space - move block and player
            block.move(dx, dy)
            self._player.move(dx, dy)
        elif "colored" in target_sprite.tags:
            # Check if colors match
            if self._check_match(block, target_sprite):
                # Colors match! Destroy both blocks
                self._destroy_pair(block, target_sprite)
                # Player moves into now-empty space
                self._player.move(dx, dy)
            # If colors don't match, block can't move
        # If blocked by wall or other non-matching obstacle, do nothing

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
        for sprite in self.current_level.sprites:
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
