# Author: Claude Opus 4.5
# Date: 2026-01-31
# PURPOSE: Main game logic for Chain Reaction. Implements Sokoban-style push mechanics where
#          matching colored blocks destroy each other. Clear all blocks to unlock the exit.
# SRP/DRY check: Pass - new game class, follows ARCBaseGame pattern from examples

"""Chain Reaction game implementation."""

from arcengine import ARCBaseGame, Camera, GameAction, InteractionMode, Level, Sprite
from games.chain_reaction.levels import LEVELS

BACKGROUND_COLOR = 0  # Black
LETTERBOX_COLOR = 1  # Dark blue

# Color tags used for matching
COLOR_TAGS = {"red", "blue", "yellow", "cyan", "purple", "green"}


class ChainReaction(ARCBaseGame):
    """
    Push colored blocks into matching pairs to clear the board.

    A Sokoban-style puzzle game where pushing colored blocks into matching blocks
    destroys both. Clear all colored blocks to unlock the exit and escape.
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
        self._exit = level.get_sprites_by_tag("exit")[0]

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
            collisions = self.try_move("player", dx, dy)

            # Handle block pushing if player hit something
            if collisions:
                for sprite in collisions:
                    if "pushable" in sprite.tags:
                        self._try_push_block(sprite, dx, dy)
                        break  # Only push one block at a time

            # Check if player reached unlocked exit
            if self._is_exit_unlocked():
                # Re-check collision with exit after potential movement
                player_collisions = self._player.collides_with(self._exit)
                if player_collisions:
                    self._handle_level_complete()

        # Update exit visual state
        self._update_exit_state()

        self.complete_action()

    def _try_push_block(self, block: Sprite, dx: int, dy: int) -> None:
        """
        Attempt to push a block, handling matches.

        If the block hits a matching colored block, both are destroyed.
        If the block moves successfully, the player follows.
        """
        # Try to move the block
        block_collisions = self.try_move_sprite(block, dx, dy)

        if block_collisions:
            # Block hit something - check for color match
            for other in block_collisions:
                if self._check_match(block, other):
                    # Colors match! Destroy both
                    self._destroy_pair(block, other)
                    # Player can now move into the space where the block was
                    self.try_move("player", dx, dy)
                    return
            # No match - block couldn't move (hit wall or wrong color)
            # Player stays in place (already handled by initial try_move)
        else:
            # Block moved successfully, player follows
            self.try_move("player", dx, dy)

    def _check_match(self, block1: Sprite, block2: Sprite) -> bool:
        """Check if two blocks have the same color tag."""
        if "colored" not in block2.tags:
            return False

        # Find color tag for each block
        block1_color = self._get_color_tag(block1)
        block2_color = self._get_color_tag(block2)

        return block1_color is not None and block1_color == block2_color

    def _get_color_tag(self, sprite: Sprite) -> str | None:
        """Extract the color tag from a sprite's tags."""
        for tag in sprite.tags:
            if tag in COLOR_TAGS:
                return tag
        return None

    def _destroy_pair(self, block1: Sprite, block2: Sprite) -> None:
        """Remove both blocks from play."""
        block1.set_interaction(InteractionMode.REMOVED)
        block2.set_interaction(InteractionMode.REMOVED)

    def _count_remaining_blocks(self) -> int:
        """Count how many colored blocks remain (not removed)."""
        colored = self.current_level.get_sprites_by_tag("colored")
        return sum(1 for s in colored if s.interaction != InteractionMode.REMOVED)

    def _is_exit_unlocked(self) -> bool:
        """Check if exit should be unlocked (all blocks cleared)."""
        return self._count_remaining_blocks() == 0

    def _update_exit_state(self) -> None:
        """Update exit sprite appearance based on state."""
        if self._is_exit_unlocked():
            # Change exit to unlocked appearance (green)
            self._exit.pixels = [[6, 6], [6, 6]]
            if "locked" in self._exit.tags:
                self._exit.tags.remove("locked")

    def _handle_level_complete(self) -> None:
        """Handle completion of current level."""
        if self.is_last_level():
            self.win()
        else:
            self.next_level()
