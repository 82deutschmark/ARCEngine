"""A simple maze game implementation."""

from arcengine import (
    ARCBaseGame,
    BlockingMode,
    Camera,
    GameAction,
    InteractionMode,
    Level,
    Sprite,
)

# Global sprite definitions
PLAYER_SPRITE = Sprite(
    pixels=[[8]],  # Red player
    name="player",
    blocking=BlockingMode.BOUNDING_BOX,
    interaction=InteractionMode.TANGIBLE,
)

EXIT_SPRITE = Sprite(
    pixels=[[9]],  # Blue exit
    name="exit",
    blocking=BlockingMode.BOUNDING_BOX,
    interaction=InteractionMode.TANGIBLE,
)

# Level 1 definition (8x8)
LEVEL_1_MAZE = Sprite(
    pixels=[
        [5, 5, 5, 5, 5, 5, 5, 5],  # Row 0
        [5, -1, -1, -1, 5, -1, -1, 5],  # Row 1
        [5, -1, 5, -1, 5, -1, 5, 5],  # Row 2
        [5, -1, 5, -1, -1, -1, -1, 5],  # Row 3
        [5, -1, 5, 5, 5, 5, -1, 5],  # Row 4
        [5, -1, -1, -1, -1, 5, -1, 5],  # Row 5
        [5, 5, 5, 5, -1, -1, -1, 5],  # Row 6
        [5, 5, 5, 5, 5, 5, 5, 5],  # Row 7
    ],
    name="maze_1",
    blocking=BlockingMode.PIXEL_PERFECT,
    interaction=InteractionMode.TANGIBLE,
    layer=-1,  # Render below player and exit
)

# Level 2 definition (12x12)
LEVEL_2_MAZE = Sprite(
    pixels=[
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],  # Row 0
        [5, -1, -1, -1, 5, -1, -1, -1, -1, -1, -1, 5],  # Row 1
        [5, -1, 5, -1, 5, -1, 5, 5, 5, 5, -1, 5],  # Row 2
        [5, -1, 5, -1, -1, -1, -1, -1, -1, 5, -1, 5],  # Row 3
        [5, -1, 5, 5, 5, 5, 5, 5, -1, 5, -1, 5],  # Row 4
        [5, -1, -1, -1, -1, -1, -1, 5, -1, 5, -1, 5],  # Row 5
        [5, 5, 5, 5, 5, 5, -1, 5, -1, 5, -1, 5],  # Row 6
        [5, -1, -1, -1, -1, 5, -1, 5, -1, 5, -1, 5],  # Row 7
        [5, -1, 5, 5, -1, 5, -1, 5, -1, 5, -1, 5],  # Row 8
        [5, -1, 5, -1, -1, 5, -1, -1, -1, 5, -1, 5],  # Row 9
        [5, -1, -1, -1, 5, 5, 5, 5, 5, 5, -1, 5],  # Row 10
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],  # Row 11
    ],
    name="maze_2",
    blocking=BlockingMode.PIXEL_PERFECT,
    interaction=InteractionMode.TANGIBLE,
    layer=-1,  # Render below player and exit
)

# Create the levels with all sprites
LEVEL_1 = Level(
    sprites=[
        LEVEL_1_MAZE,
        PLAYER_SPRITE.clone().set_position(1, 1),  # Start position
        EXIT_SPRITE.clone().set_position(7, 7),  # Exit position
    ]
)

LEVEL_2 = Level(
    sprites=[
        LEVEL_2_MAZE,
        PLAYER_SPRITE.clone().set_position(1, 1),  # Start position
        EXIT_SPRITE.clone().set_position(11, 11),  # Exit position
    ]
)


class SimpleMaze(ARCBaseGame):
    """A simple maze game where the player navigates to the exit."""

    def __init__(self) -> None:
        """Initialize the SimpleMaze game."""
        # Create camera with white background and letterbox
        camera = Camera(
            width=8, height=8, background=0, letter_box=0
        )  # White background and letterbox

        # Initialize the base game
        super().__init__(
            game_id="simple_maze", levels=[LEVEL_1, LEVEL_2], camera=camera
        )

    def next_level(self) -> None:
        """Move to the next level and resize camera."""
        super().next_level()
        # Resize camera based on level index (8 + level_index * 4)
        size = 8 + (self.level_index * 4)
        self.camera.resize(size, size)

    def step(self) -> None:
        """Step the game forward based on the current action."""

        # Handle movement based on action ID
        dx = 0
        dy = 0
        if self.action == GameAction.ACTION1:
            dy = -1
        elif self.action == GameAction.ACTION2:  # Move Down
            dy = 1
        elif self.action == GameAction.ACTION3:  # Move Left
            dx = -1
        elif self.action == GameAction.ACTION4:  # Move Right
            dx = 1

        collided = self.try_move("player", dx, dy)

        # Check if player collided with exit
        if collided and any(sprite.name == "exit" for sprite in collided):
            self.next_level()  # will auto win if last level

        self.complete_action()
