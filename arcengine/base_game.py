"""
Module for the base game class in ARCEngine.
"""

from typing import List, Optional, final

from numpy import ndarray

from .camera import Camera
from .enums import ActionInput, FrameData, FrameDataRaw, GameAction, GameState
from .level import Level
from .sprites import Sprite


class ARCBaseGame:
    """Base class for ARCEngine games that manages levels and camera.

    This is a base class that games should inherit from. and extend with game logic.
    It handles the game loop and rendering.

    Custom game logic should be implemented in the step() method.
    """

    _game_id: str
    _levels: list[Level]
    _current_level_index: int
    _camera: Camera
    _action: GameAction | None
    _action_complete: bool
    _state: GameState
    _score: int

    def __init__(
        self,
        game_id: str,
        levels: List[Level],
        camera: Optional[Camera] = None,
    ) -> None:
        """Initialize a new game.

        Args:
            levels: List of levels to initialize the game with. Each level will be cloned.
            camera: Optional camera to use. If not provided, a default 64x64 camera will be created.

        Raises:
            ValueError: If levels list is empty
        """
        if not levels:
            raise ValueError("Game must have at least one level")

        # Game ID should be set by subclasses
        self._game_id = game_id

        # Clone each level to prevent external modification
        self._levels = [level.clone() for level in levels]
        self._current_level_index = 0

        # Use provided camera or create default
        self._camera = camera if camera is not None else Camera()

        # Game state
        self._state = GameState.NOT_PLAYED
        self._score = 0
        self._action = None
        self._action_complete = False

    @property
    @final
    def current_level(self) -> Level:
        """Get the current level.

        Returns:
            Level: The current level
        """
        return self._levels[self._current_level_index]

    @property
    @final
    def camera(self) -> Camera:
        """Get the game's camera.

        Returns:
            Camera: The game's camera
        """
        return self._camera

    @property
    @final
    def game_id(self) -> str:
        """Get the game's ID.

        Returns:
            str: The game's ID
        """
        return self._game_id

    @final
    def set_level(self, index: int) -> None:
        """Set the current level by index.

        Args:
            index: The index of the level to set as current

        Raises:
            IndexError: If index is out of range
        """
        if not 0 <= index < len(self._levels):
            raise IndexError(
                f"Level index {index} out of range [0, {len(self._levels)})"
            )
        self._current_level_index = index

    @property
    @final
    def level_index(self) -> int:
        """Get the current level index.

        Returns:
            int: The current level index
        """
        return self._current_level_index

    @final
    def perform_action(
        self, action_input: ActionInput, raw: bool = False
    ) -> FrameData | FrameDataRaw:
        """Perform an action and return the resulting frame data.

        DO NOT OVERRIDE THIS METHOD, Your Game Logic should be in step()

        The base implementation:
        1. While the action is not complete, call step() and render frames
        2. Returns a FrameData object with the current state

        Args:
            action_input: The action to perform

        Returns:
            FrameData: The resulting frame data
        """
        # Validate action input
        self._set_action(action_input)

        frame_list: list[ndarray | list[list[int]]] = []

        while not self.is_action_complete():
            self.step()
            frame = self.camera.render(self.current_level.get_sprites())
            if raw:
                frame_list.append(frame)
            else:
                frame_list.append(frame.tolist())

        # Create and return FrameData
        if raw:
            frame_raw = FrameDataRaw()
            frame_raw.game_id = self._game_id
            frame_raw.frame = frame_list
            frame_raw.state = self._state
            frame_raw.score = self._score
            frame_raw.action_input = action_input
            return frame_raw

        return FrameData(
            game_id=self._game_id,
            frame=frame_list,
            state=self._state,
            score=self._score,
            action_input=action_input,
        )

    @property
    @final
    def action(self) -> GameAction | None:
        """Get the current action."""
        return self._action

    @final
    def _set_action(self, action_input: ActionInput) -> None:
        """Set the action to perform.

        Args:
            action_input: The action to perform
        """
        self._action = action_input.id
        self._action_complete = False

    @final
    def complete_action(self) -> None:
        """Complete the action. Call this when the provided action is fully resolved"""
        self._action_complete = True

    @final
    def is_action_complete(self) -> bool:
        """Check if the action is complete.

        Returns:
            bool: True if the action is complete, False otherwise
        """
        return self._action_complete

    @final
    def win(self) -> None:
        """Call this when the player has beaten the game."""
        self._state = GameState.WIN

    @final
    def lose(self) -> None:
        """Call this when the player has losses the game."""
        self._state = GameState.GAME_OVER

    def step(self) -> None:
        """Step the game.  This is where your game logic should be implemented.

        REQUIRED: Call complete_action() when the action is complete.
          It does not need to be called every step, but once the action is complete.
          The engine will keep calling step and rendering frames until the action is complete.
        """

        self.complete_action()

    def try_move(self, sprite_name: str, dx: int, dy: int) -> List[Sprite]:
        """Try to move a sprite and return a list of sprites it collides with.

        This method attempts to move the sprite by the given deltas and checks for collisions.
        If any collisions are detected, the sprite is not moved and the method returns a list
        of sprite names that were collided with.

        Args:
            sprite_name: The name of the sprite to move.
            dx: The change in x position (positive = right, negative = left).
            dy: The change in y position (positive = down, negative = up).

        Returns:
            A list of sprite names that the sprite collided with. If no collisions occurred,
            the sprite is moved and an empty list is returned.

        Raises:
            ValueError: If no sprite with the given name is found.
        """
        # Get the sprite to move
        sprites = self.current_level.get_sprites_by_name(sprite_name)
        if not sprites:
            raise ValueError(f"No sprite found with name: {sprite_name}")
        sprite = sprites[0]  # Use the first sprite with this name

        # Store original position
        original_x = sprite.x
        original_y = sprite.y

        # Try the move
        sprite.move(dx, dy)

        # Check for collisions with all other sprites
        collisions = []
        for other in self.current_level.get_sprites():
            if sprite.collides_with(other):
                collisions.append(other)

        # If there were collisions, revert the move
        if collisions:
            sprite.set_position(original_x, original_y)

        return collisions

    def is_last_level(self) -> bool:
        """Check if the current level is the last level.

        Returns:
            bool: True if the current level is the last level, False otherwise
        """
        return self._current_level_index == len(self._levels) - 1

    def next_level(self) -> None:
        """Move to the next level."""
        if not self.is_last_level():
            self._current_level_index += 1
        else:
            self.win()
