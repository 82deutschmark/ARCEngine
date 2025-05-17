# ARCEngine

A Python library built with numpy support for 2D sprite-based game development.

## Installation

Add ARCEngine to your project using one of these methods:

### Using uv (Recommended)

Add ARCEngine to your `pyproject.toml`:
```toml
[project]
dependencies = [
    "arcengine @ git+https://github.com/yourusername/ARCEngine.git@main",
]
```

Then install with uv:
```bash
uv pip install --editable .
```

### Using pip

Add ARCEngine to your `pyproject.toml`:
```toml
[project]
dependencies = [
    "arcengine @ git+https://github.com/yourusername/ARCEngine.git@main",
]
```

Then install with pip:
```bash
pip install --editable .
```

### Using Poetry

Add ARCEngine to your `pyproject.toml`:
```toml
[tool.poetry.dependencies]
arcengine = { git = "https://github.com/yourusername/ARCEngine.git", branch = "main" }
```

Then install with Poetry:
```bash
poetry install
```

## Requirements

- Python >= 3.8
- NumPy >= 1.24.0

## API Documentation

### Sprite

The `Sprite` class represents a 2D sprite that can be positioned and scaled in the game world.

```python
from arcengine import Sprite, BlockingMode

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
    layer=1  # Higher values render on top
)
```

#### Properties

- `name` (str): The sprite's unique identifier
- `x` (int): X coordinate in pixels
- `y` (int): Y coordinate in pixels
- `scale` (int): Scale factor. Positive values scale up (2 = double size, 3 = triple size). Negative values scale down (-1 = half size, -2 = one-third size, -3 = one-fourth size).
- `blocking` (BlockingMode): Collision detection method
- `pixels` (numpy.ndarray): The sprite's pixel data
- `layer` (int): Z-order layer for rendering (higher values render on top)

#### Methods

##### `__init__(pixels, name=None, x=0, y=0, scale=1, rotation=0, blocking=BlockingMode.NOT_BLOCKED, layer=0)`
Initialize a new Sprite.

- `pixels`: 2D list representing the sprite's pixels
- `name`: Optional sprite name (default: generates UUID)
- `x`: X coordinate in pixels (default: 0)
- `y`: Y coordinate in pixels (default: 0)
- `scale`: Scale factor (default: 1)
- `rotation`: Rotation in degrees (default: 0)
- `blocking`: Collision detection method (default: NOT_BLOCKED)
- `layer`: Z-order layer for rendering (default: 0, higher values render on top)

Raises `ValueError` if scale is 0, pixels is not a 2D list, rotation is invalid, or if downscaling factor doesn't evenly divide sprite dimensions.

##### `clone(new_name=None)`
Create an independent copy of this sprite.

- `new_name`: Optional name for the cloned sprite (default: generates UUID)
- Returns: A new Sprite instance with the same properties but independent state

##### `set_position(x, y)`
Set the sprite's position.

- `x`: New X coordinate in pixels
- `y`: New Y coordinate in pixels

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

### BlockingMode

An enumeration defining different collision detection behaviors for sprites:

- `NOT_BLOCKED`: No collision detection
- `BOUNDING_BOX`: Collision detection using the sprite's bounding box
- `PIXEL_PERFECT`: Collision detection using pixel-perfect testing

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
   uv pip install -e ".[dev]"
   ```

## License

TBD - Currently for Internal Use Only.
