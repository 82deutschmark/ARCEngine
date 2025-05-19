"""
Module for the base game class in ARCEngine.
"""

from typing import List, Optional, final

from .camera import Camera
from .enums import ActionInput, FrameData, GameAction, GameState
from .level import Level
from .sprites import Sprite


class ARCBaseGame:
    """Base class for ARCEngine games that manages levels and camera."""

    _levels: list[Level]
    _current_level_index: int
    _camera: Camera
    _action: GameAction | None
    _action_complete: bool
    _state: GameState
    _score: int
    _game_id: str

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

    @final
    def perform_action(self, action_input: ActionInput) -> FrameData:
        """Perform an action and return the resulting frame data.

        DO NOT OVERRIDE THIS METHOD, Your Game Logic should be in step()

        The base implementation:
        1. Validates the action input
        2. While the action is not complete, call step() and render frames
        3. Returns a FrameData object with the current state

        Args:
            action_input: The action to perform

        Returns:
            FrameData: The resulting frame data
        """
        # Validate action input
        if not action_input.id.validate_data(action_input.data):
            raise ValueError(f"Invalid data for action {action_input.id}")
        self._set_action(action_input)

        frame_list: list[list[list[int]]] = []

        while not self.is_action_complete():
            self.step()
            frame = self.camera.render(self.current_level.get_sprites())
            frame_list.append(frame.tolist())

        # Create and return FrameData
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
        """Complete the action."""
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
        """Win the game."""
        self._state = GameState.WIN

    @final
    def lose(self) -> None:
        """Lose the game."""
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
