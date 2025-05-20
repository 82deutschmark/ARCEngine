"""A simple maze game implementation."""

from arcengine import ARCBaseGame, BlockingMode, Camera, GameAction, InteractionMode, Level, Sprite, ToggleableUserDisplay

# Global sprite definitions
PLAYER_SPRITE = Sprite(pixels=[[8]], name="player", blocking=BlockingMode.PIXEL_PERFECT, interaction=InteractionMode.TANGIBLE, tags=["fixed"])

ENERGY_PILL_ON_SPRITE = Sprite(pixels=[[6, 6], [6, 6]], name="energy_pill", blocking=BlockingMode.NOT_BLOCKED, interaction=InteractionMode.INTANGIBLE, tags=["energy"])

ENERGY_PILL_OFF_SPRITE = Sprite(
    pixels=[[3, 3], [3, 3]],
    name="energy_pill_off",
    blocking=BlockingMode.NOT_BLOCKED,
    interaction=InteractionMode.REMOVED,
)

# Create the levels with all sprites
EXIT_SPRITE = Sprite(
    pixels=[[9]],
    name="exit",
    blocking=BlockingMode.PIXEL_PERFECT,
    interaction=InteractionMode.TANGIBLE,
    tags=["fixed"],  # Render below player and exit
)

MAZE_1_SPRITE = Sprite(
    pixels=[[5, 5, 5, 5, 5, 5, 5, 5], [5, -1, -1, -1, 5, -1, -1, 5], [5, -1, 5, -1, 5, -1, 5, 5], [5, -1, 5, -1, -1, -1, -1, 5], [5, -1, 5, 5, 5, 5, -1, 5], [5, -1, -1, -1, -1, 5, -1, 5], [5, 5, 5, 5, -1, 5, -1, 5], [5, 5, 5, 5, 5, 5, 5, 5]],
    name="maze_1",
    blocking=BlockingMode.PIXEL_PERFECT,
    interaction=InteractionMode.TANGIBLE,
    layer=-1,
)

MAZE_2_SPRITE = Sprite(
    pixels=[
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [5, -1, -1, -1, 5, -1, -1, -1, -1, -1, -1, 5],
        [5, -1, 5, -1, 5, -1, 5, 5, 5, 5, -1, 5],
        [5, -1, 5, -1, -2, -1, 5, 5, -1, 5, -1, 5],
        [5, -1, 5, -1, -2, -1, 5, 5, -1, 5, -1, 5],
        [5, -1, 5, -1, -2, -1, 5, 5, -1, 5, -1, 5],
        [5, -1, 5, -1, -2, -1, 5, 5, -1, 5, -1, 5],
        [5, -1, 5, -1, -1, -1, 5, 5, -1, 5, -1, 5],
        [5, -1, 5, 5, 5, 5, 5, 5, -1, 5, -1, 5],
        [5, -1, 5, 5, 5, 5, 4, 4, -1, 5, -1, 5],
        [5, -1, -1, -1, -1, -1, -1, -1, -1, 5, -1, 5],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
    ],
    name="maze_2",
    blocking=BlockingMode.PIXEL_PERFECT,
    interaction=InteractionMode.TANGIBLE,
    layer=-1,
)

MAZE_3_SPRITE = Sprite(
    pixels=[
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [5, -1, -1, -1, -1, -2, -1, -1, -1, -1, -1, 5],
        [5, 5, 5, 5, -1, 5, -1, 5, 5, 5, -1, 5],
        [5, 5, 5, 5, -1, 5, -1, 5, 5, 5, -1, 5],
        [5, 5, 5, 5, -1, 5, -1, 5, 5, 5, -1, 5],
        [5, 5, 5, 5, -1, 5, -1, 5, 5, 5, -1, 5],
        [5, 5, 5, 5, -1, -2, -1, 5, 5, 5, -1, 5],
        [5, 5, 5, 5, -1, -2, -1, 5, 5, 5, -1, 5],
        [5, 5, 5, 5, -1, -2, -1, 5, 5, 5, -1, 5],
        [5, 5, 5, 5, -1, -1, -1, 5, -1, -1, -1, 5],
        [5, 5, 5, 5, -1, -2, -2, 5, 5, 5, -1, 5],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
    ],
    name="maze_3",
    blocking=BlockingMode.PIXEL_PERFECT,
    interaction=InteractionMode.TANGIBLE,
    layer=-1,
)

BLOCK_ORANGE_SPRITE = Sprite(
    pixels=[[12]],
    name="block_orange",
    blocking=BlockingMode.PIXEL_PERFECT,
    interaction=InteractionMode.TANGIBLE,
    tags=["fixed"],  # Render below player and exit
)

MAZE_4_SPRITE = Sprite(
    pixels=[
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [5, -1, 5, -1, -1, -1, -1, -1, -1, 5, -1, 5],
        [5, -1, 5, 5, 5, 5, 5, -1, 5, 5, -1, 5],
        [5, -1, 5, 5, 5, 5, 5, -1, 5, 5, -1, 5],
        [5, -1, 5, 5, 5, 5, 5, -1, -2, -2, -1, 5],
        [5, -1, 5, 5, 5, 5, 5, -1, 5, 5, -1, 5],
        [5, -1, -1, -1, 5, 5, 5, -1, 5, 5, -1, 5],
        [5, -1, -1, -1, 5, 5, 5, -1, 5, 5, -1, 5],
        [5, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 5],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
    ],
    name="maze_4",
    blocking=BlockingMode.PIXEL_PERFECT,
    interaction=InteractionMode.TANGIBLE,
    layer=-1,
)

MAZE_5_SPRITE = Sprite(
    pixels=[
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [5, -1, 5, 5, 5, 5, 5, 5, 5, 5, -1, 5],
        [5, -1, 5, 5, 5, 5, 5, 5, 5, 5, -1, 5],
        [5, -1, 5, 5, 5, 5, 5, 5, 5, 5, -1, 5],
        [5, -1, 5, 5, 5, 5, 5, 5, 5, 5, -1, 5],
        [5, -1, 5, 5, 5, 5, 5, 5, 5, 5, -1, 5],
        [5, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 5],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, -1, 5],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, -1, 5],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, -1, 5],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, -1, 5],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
    ],
    name="maze_5",
    blocking=BlockingMode.PIXEL_PERFECT,
    interaction=InteractionMode.TANGIBLE,
    layer=-1,
)

ORANGE_BLOCK_FLEX_SPRITE = Sprite(
    pixels=[[12]],
    name="block_orange_flex",
    blocking=BlockingMode.PIXEL_PERFECT,
    interaction=InteractionMode.TANGIBLE,
    tags=["floating"],  # Render below player and exit
)

LEVEL_1 = Level(
    sprites=[
        PLAYER_SPRITE.clone().set_position(1, 1),  # Layer: -1
        MAZE_1_SPRITE.clone().set_position(0, 0),  # Layer: 0
        EXIT_SPRITE.clone().set_position(6, 6),  # Layer: 0
    ],
    grid_size=(8, 8),
)

LEVEL_2 = Level(
    sprites=[
        PLAYER_SPRITE.clone().set_position(1, 1),  # Layer: -1
        MAZE_2_SPRITE.clone().set_position(0, 0),  # Layer: 0
        EXIT_SPRITE.clone().set_position(10, 10),  # Layer: 0
    ],
    grid_size=(12, 12),
)

LEVEL_3 = Level(
    sprites=[
        MAZE_3_SPRITE.clone().set_position(0, 0),  # Layer: 0
        EXIT_SPRITE.clone().set_position(8, 9),  # Layer: 0
        PLAYER_SPRITE.clone().set_position(1, 1),  # Layer: 0
        BLOCK_ORANGE_SPRITE.clone().set_position(4, 2),  # Layer: 0
        BLOCK_ORANGE_SPRITE.clone().set_position(10, 2),  # Layer: 0
    ],
    grid_size=(12, 12),
)

LEVEL_4 = Level(
    sprites=[
        MAZE_4_SPRITE.clone().set_position(0, 0),  # Layer: 0
        PLAYER_SPRITE.clone().set_position(1, 1),  # Layer: 0
        EXIT_SPRITE.clone().set_position(10, 1),  # Layer: 0
        BLOCK_ORANGE_SPRITE.clone().set_position(3, 8),  # Layer: 0
        BLOCK_ORANGE_SPRITE.clone().set_position(10, 8),  # Layer: 0
    ],
    grid_size=(12, 12),
)

LEVEL_5 = Level(
    sprites=[
        MAZE_5_SPRITE.clone().set_position(0, 0),  # Layer: 0
        PLAYER_SPRITE.clone().set_position(1, 1),  # Layer: 0
        EXIT_SPRITE.clone().set_position(10, 1),  # Layer: 0
        BLOCK_ORANGE_SPRITE.clone().set_position(10, 6),  # Layer: 0
        ORANGE_BLOCK_FLEX_SPRITE.clone().set_position(5, 8),  # Layer: 0
    ],
    grid_size=(12, 12),
)


class ComplexMaze(ARCBaseGame):
    """A simple maze game where the player navigates to the exit."""

    _ui: ToggleableUserDisplay

    def __init__(self) -> None:
        """Initialize the SimpleMaze game."""
        # Create camera with white background and letterbox
        camera = Camera(width=8, height=8, background=0, letter_box=0)  # White background and letterbox

        # Initialize the base game
        super().__init__(game_id="simple_maze", levels=[LEVEL_1, LEVEL_2, LEVEL_3, LEVEL_4, LEVEL_5], camera=camera)

        # Create our UI
        sprite_pairs = []
        for i in range(32):
            sprite_pairs.append((ENERGY_PILL_ON_SPRITE.clone().set_position(i * 2, 0), ENERGY_PILL_OFF_SPRITE.clone().set_position(i * 2, 0)))
            print(f"{sprite_pairs[0][0].tags}")
        for i in range(31):
            sprite_pairs.append((ENERGY_PILL_ON_SPRITE.clone().set_position(62, i * 2 + 2), ENERGY_PILL_OFF_SPRITE.clone().set_position(62, i * 2 + 2)))
            print(f"{sprite_pairs[0][0].tags}")
        self._ui = ToggleableUserDisplay(sprite_pairs)
        self.camera.replace_interface([self._ui])

    def step(self) -> None:
        """Step the game forward based on the current action."""

        # Handle movement based on action ID
        dx = 0
        dy = 0
        if self.action.id == GameAction.ACTION1:
            dy = -1
        elif self.action.id == GameAction.ACTION2:  # Move Down
            dy = 1
        elif self.action.id == GameAction.ACTION3:  # Move Left
            dx = -1
        elif self.action.id == GameAction.ACTION4:  # Move Right
            dx = 1

        self._try_pushing_move(dx, dy)

        if not self._ui.disabled_first_by_tag("energy"):
            self.lose()  # will auto win if last level

        self.complete_action()

    def _try_pushing_move(self, dx: int, dy: int) -> None:
        collided = self.try_move("player", dx, dy)

        # Check if player collided with exit
        if collided and any(sprite.name == "exit" for sprite in collided):
            self.next_level()
            self.camera.x = 0
            self.camera.y = 0
            self._ui.enable_all_by_tag("energy")

        if collided:
            for sprite in collided:
                if sprite.name.startswith("block"):
                    # Try to push the block in the same direction
                    block_collided = self.try_move_sprite(sprite, dx, dy)

                    # If block collided with another block of same name, destroy both
                    if block_collided:
                        for other_sprite in block_collided:
                            print(f"{other_sprite.name} vs {sprite.name}")
                            if sprite.name.startswith(other_sprite.name):
                                sprite.set_interaction(InteractionMode.REMOVED)
                                other_sprite.set_interaction(InteractionMode.REMOVED)
                                break
                    else:
                        self.try_move("player", dx, dy)

                if sprite.name.startswith("maze"):
                    sprite.move(dx, dy)
                    fixed_sprites = self.current_level.get_sprites_by_tag("fixed")
                    self.camera.move(dx, dy)
                    for fixed_sprite in fixed_sprites:
                        fixed_sprite.move(dx, dy)
