# ARCEngine

A Python library for 2D sprite-based game development.

## Installation

```bash
pip install arcengine
```

## Development Setup

1. Clone the repository
2. Install development dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```
3. Install git hooks:
   ```bash
   pre-commit install
   ```

The project uses `ruff` for linting and formatting code, and `mypy` for static type checking.

## API Documentation

### ARCBaseGame

The base class for ARCEngine games that manages levels and camera.

```python
from arcengine import ARCBaseGame, Level, Camera

# Create a game with levels and optional custom camera
game = ARCBaseGame(levels=[level1, level2], camera=camera)  # camera is optional
```

#### Properties

- `current_level` (Level): The current active level
- `camera` (Camera): The game's camera
- `game_id` (str): The game's identifier (should be set by subclasses)
- `action` (GameAction): The current action being performed

#### Methods

##### `__init__(levels, camera=None)`
Initialize a new game.

- `levels`: List of levels to initialize the game with. Each level will be cloned.
- `camera`: Optional camera to use. If not provided, a default 64x64 camera will be created.

Raises `ValueError` if levels list is empty.

##### `set_level(index)`
Set the current level by index.

- `index`: The index of the level to set as current

Raises `IndexError` if index is out of range.

##### `perform_action(action_input)`
Perform an action and return the resulting frame data.

This method should not be overridden. Game logic should be implemented in the `step()` method.

- `action_input`: The action to perform
- Returns: FrameData containing the rendered frames and game state

##### `step()`
Step the game. This is where your game logic should be implemented.

REQUIRED: Call `complete_action()` when the action is complete. It does not need to be called every step, but once the action is complete. The engine will keep calling step and rendering frames until the action is complete.

##### `complete_action()`
Mark the current action as complete.

##### `is_action_complete()`
Check if the current action is complete.

- Returns: True if the action is complete, False otherwise

### Sprite

The `Sprite` class represents a 2D sprite that can be positioned and scaled in the game world.

```python
from arcengine import Sprite, BlockingMode, InteractionMode

# Create a simple 2x2 sprite
sprite = Sprite([
    [1, 2],
    [3, 4]
])

# Create a sprite with custom properties
sprite = Sprite(
    pixels=[[1, 2], [3, 4]],
    name="player",
    x=10,
    y=20,
    scale=2,
    rotation=90,
    blocking=BlockingMode.BOUNDING_BOX,
    layer=1,  # Higher values render on top
    interaction=InteractionMode.TANGIBLE
)
```

#### Properties

- `name` (str): The sprite's unique identifier
- `x` (int): X coordinate in pixels
- `y` (int): Y coordinate in pixels
- `scale` (int): Scale factor. Positive values scale up (2 = double size, 3 = triple size). Negative values scale down (-1 = half size, -2 = one-third size, -3 = one-fourth size).
- `rotation` (int): Rotation in degrees (0, 90, 180, or 270)
- `blocking` (BlockingMode): Collision detection method
- `pixels` (numpy.ndarray): The sprite's pixel data
- `layer` (int): Z-order layer for rendering (higher values render on top)
- `interaction` (InteractionMode): How the sprite interacts with the game world
- `is_visible` (bool): Whether the sprite should be rendered
- `is_collidable` (bool): Whether the sprite should participate in collisions

#### Methods

##### `__init__(pixels, name=None, x=0, y=0, scale=1, rotation=0, blocking=BlockingMode.NOT_BLOCKED, layer=0, interaction=InteractionMode.TANGIBLE)`
Initialize a new Sprite.

- `pixels`: 2D list representing the sprite's pixels
- `name`: Optional sprite name (default: generates UUID)
- `x`: X coordinate in pixels (default: 0)
- `y`: Y coordinate in pixels (default: 0)
- `scale`: Scale factor (default: 1)
- `rotation`: Rotation in degrees (default: 0)
- `blocking`: Collision detection method (default: NOT_BLOCKED)
- `layer`: Z-order layer for rendering (default: 0, higher values render on top)
- `interaction`: How the sprite interacts with the game world (default: TANGIBLE)

Raises `ValueError` if scale is 0, pixels is not a 2D list, rotation is invalid, or if downscaling factor doesn't evenly divide sprite dimensions.

##### `clone(new_name=None)`
Create an independent copy of this sprite.

- `new_name`: Optional name for the cloned sprite (default: generates UUID)
- Returns: A new Sprite instance with the same properties but independent state

##### `set_position(x, y)`
Set the sprite's position.

- `x`: New X coordinate in pixels
- `y`: New Y coordinate in pixels

##### `move(dx, dy)`
Move the sprite by the given deltas.

- `dx`: Change in x position (positive = right, negative = left)
- `dy`: Change in y position (positive = down, negative = up)

##### `set_scale(scale)`
Set the sprite's scale factor.

- `scale`: The new scale factor:
  * Positive values scale up (2 = double size, 3 = triple size)
  * Negative values scale down (-1 = half size, -2 = one-third size, -3 = one-fourth size)
  * Zero is invalid
- Raises `ValueError` if scale is 0 or if downscaling factor doesn't evenly divide sprite dimensions

For example:
```python
sprite = Sprite([[1, 2], [3, 4]])

# Upscaling examples
sprite.set_scale(2)  # Doubles size in both dimensions
sprite.set_scale(3)  # Triples size in both dimensions

# Downscaling examples
sprite.set_scale(-1)  # Half size (divide dimensions by 2)
sprite.set_scale(-2)  # One-third size (divide dimensions by 3)
sprite.set_scale(-3)  # One-fourth size (divide dimensions by 4)
```

##### `adjust_scale(delta)`
Adjust the sprite's scale by a delta value, moving one step at a time.

The method will adjust the scale by incrementing or decrementing by 1 repeatedly until reaching the target scale. This ensures smooth transitions and validates each step.

Negative scales indicate downscaling factors:
- scale = -1: half size (divide by 2)
- scale = -2: one-third size (divide by 3)
- scale = -3: one-fourth size (divide by 4)

Examples:
- Current scale 1, delta +2 -> Steps through: 1 -> 2 -> 3
- Current scale 1, delta -2 -> Steps through: 1 -> 0 -> -1 (half size)
- Current scale -2, delta +3 -> Steps through: -2 -> -1 -> 0 -> 1

Raises `ValueError` if any intermediate scale would be 0 or if a downscaling factor doesn't evenly divide sprite dimensions.

##### `set_rotation(rotation)`
Set the sprite's rotation to a specific value.

- `rotation`: The new rotation in degrees (must be 0, 90, 180, or 270)
- Raises `ValueError` if rotation is not a valid 90-degree increment

##### `rotate(delta)`
Rotate the sprite by a given amount.

- `delta`: The change in rotation in degrees (must result in a valid rotation)
- Raises `ValueError` if resulting rotation is not a valid 90-degree increment

##### `render()`
Render the sprite with current scale and rotation.

- Returns: A 2D numpy array representing the rendered sprite
- Raises `ValueError` if downscaling factor doesn't evenly divide the sprite dimensions

##### `set_layer(layer)`
Set the sprite's rendering layer.

- `layer`: New layer value. Higher values render on top.

##### `set_blocking(blocking)`
Set the sprite's blocking behavior.

- `blocking`: The new blocking behavior (BlockingMode enum value)
- Raises `ValueError` if blocking is not a BlockingMode enum value

##### `set_name(name)`
Set the sprite's name.

- `name`: New name for the sprite
- Raises `ValueError` if name is empty

##### `set_interaction(interaction)`
Set the sprite's interaction mode.

- `interaction`: The new interaction mode (InteractionMode enum value)
- Raises `ValueError` if interaction is not an InteractionMode enum value

##### `collides_with(other)`
Check if this sprite collides with another sprite.

The collision check follows these rules:
1. A sprite cannot collide with itself
2. Non-collidable sprites (based on interaction mode) never collide
3. For collidable sprites, the collision detection method is based on their blocking mode:
   - NOT_BLOCKED: Always returns False
   - BOUNDING_BOX: Simple rectangular collision check
   - PIXEL_PERFECT: Precise pixel-level collision detection

- `other`: The other sprite to check collision with
- Returns: True if the sprites collide, False otherwise

### BlockingMode

An enumeration defining different collision detection behaviors for sprites:

- `NOT_BLOCKED`: No collision detection
- `BOUNDING_BOX`: Collision detection using the sprite's bounding box
- `PIXEL_PERFECT`: Collision detection using pixel-perfect testing

### InteractionMode

An enumeration defining how a sprite interacts with the game world:

- `TANGIBLE`: Visible and can be collided with
- `INTANGIBLE`: Visible but cannot be collided with (ghost-like)
- `INVISIBLE`: Not visible but can be collided with (invisible wall)
- `REMOVED`: Not visible and cannot be collided with (effectively removed)

### Camera

The `Camera` class defines a viewport into the game world, handling rendering of sprites and viewport scaling.

```python
from arcengine import Camera

# Create a default 64x64 camera
camera = Camera()

# Create a custom camera
camera = Camera(
    x=10,
    y=20,
    width=32,
    height=32,
    background=1,  # Background color index
    letter_box=2   # Letter box color index
)
```

#### Properties

- `x` (int): X coordinate in pixels
- `y` (int): Y coordinate in pixels
- `width` (int): Viewport width in pixels (max: 64)
- `height` (int): Viewport height in pixels (max: 64)
- `background` (int): Background color index
- `letter_box` (int): Letter box color index

#### Methods

##### `__init__(x=0, y=0, width=64, height=64, background=5, letter_box=5)`
Initialize a new Camera.

- `x`: X coordinate in pixels (default: 0)
- `y`: Y coordinate in pixels (default: 0)
- `width`: Viewport width in pixels (default: 64, max: 64)
- `height`: Viewport height in pixels (default: 64, max: 64)
- `background`: Background color index (default: 5 - Black)
- `letter_box`: Letter box color index (default: 5 - Black)

Raises `ValueError` if width or height exceed 64 pixels.

##### `render(sprites)`
Render the camera view.

- `sprites`: List of sprites to render
- Returns: A 64x64 numpy array representing the rendered view

The rendered output is always 64x64 pixels. If the camera's viewport is smaller, the view will be scaled up uniformly (maintaining aspect ratio) to fit within 64x64, and the remaining space will be filled with the letter_box color.

### Level

The `Level` class manages a collection of sprites, providing methods to add, remove, and query sprites.

```python
from arcengine import Level, Sprite

# Create an empty level
level = Level()

# Create a level with initial sprites
sprites = [
    Sprite([[1]], name="player"),
    Sprite([[2]], name="enemy")
]
level = Level(sprites=sprites)
```

#### Methods

##### `__init__(sprites=None)`
Initialize a new Level.

- `sprites`: Optional list of sprites to initialize the level with

##### `add_sprite(sprite)`
Add a sprite to the level.

- `sprite`: The sprite to add

##### `remove_sprite(sprite)`
Remove a sprite from the level.

- `sprite`: The sprite to remove

##### `get_sprites()`
Get all sprites in the level.

- Returns: A copy of the list of all sprites in the level

##### `get_sprites_by_name(name)`
Get all sprites with the given name.

- `name`: The name to search for
- Returns: List of sprites with the given name

##### `clone()`
Create a deep copy of this level.

- Returns: A new Level instance with cloned sprites

## Usage

```python
from arcengine import example

# Add usage examples here
```

## Development

To set up the development environment:

1. Clone the repository:
   ```bash
   git clone git@github.com:yourusername/ARCEngine.git
   cd ARCEngine
   ```

2. Create and activate a virtual environment using uv:
   ```bash
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install development dependencies:
   ```bash
   uv sync
   ```

4. Install git hooks:

```bash
pre-commit install
```

You're now ready to contribute! This repo uses [`ruff`](https://github.com/astral-sh/ruff) to lint and format code and [`mypy`](https://github.com/python/mypy) for static type checking. You can run all of the tools manually like this:

```bash
pre-commit run --all-files
```

Note: by default these tools will run automatically before `git commit`. It's also recommended to set up `ruff` [inside your IDE](https://docs.astral.sh/ruff/editors/setup/).

## License

TBD - Currently for Internal Use Only.
