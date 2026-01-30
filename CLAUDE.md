# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build & Development Commands

```bash
# Setup
uv venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
uv sync

# Install git hooks (runs ruff + mypy on commit)
pre-commit install

# Run all linting/formatting/type checking
pre-commit run --all-files

# Run tests
python -m pytest                          # All tests
python -m pytest tests/test_base_game.py  # Single file
python -m pytest -v                       # Verbose
```

## Architecture

ARCEngine is a Python 2D sprite game engine designed for ARC-AGI-3. It enforces specific constraints:
- 64×64 pixel output grid with 16 colors
- Turn-based gameplay (6 actions + RESET)
- Each action produces 1-N frames

### Core Components

**`ARCBaseGame`** (`base_game.py`) - Abstract game controller that subclasses override:
- Manages multiple `Level` objects (cloned on init)
- Main game loop in `perform_action()` calls `step()` until `complete_action()` is called (max 1000 frames)
- `try_move()` handles collision-aware sprite movement
- Game states: NOT_PLAYED, NOT_FINISHED, WIN, GAME_OVER

**`Level`** (`level.py`) - Sprite container:
- Sprite queries by name, tag, position
- Collision detection via `collides_with()`
- Auto-merges sprites tagged "sys_static" on init for optimization

**`Camera`** (`camera.py`) - Viewport and renderer:
- Always outputs 64×64, auto-scales smaller viewports with letterboxing
- Renders sprites in layer order, then UI interfaces
- `display_to_grid()` converts screen coords to game coords

**`Sprite`** (`sprites.py`) - Visual entity:
- Pixels are palette indices (-1 = transparent)
- Rotation limited to 0°, 90°, 180°, 270°
- Scale: positive = upscale, negative = downscale (-1 = half size)
- BlockingMode: PIXEL_PERFECT, BOUNDING_BOX, NOT_BLOCKED
- InteractionMode: TANGIBLE, INTANGIBLE, INVISIBLE, REMOVED

**Data models** (`enums.py`):
- `GameAction`: RESET (0), ACTION1-7 (ACTION6 uses ComplexAction with x,y coordinates)
- `ActionInput`, `FrameData`, `FrameDataRaw`

### Game Flow

```
ARCBaseGame.perform_action(action_input)
  └── while not complete:
        └── step()        # Your game logic
        └── camera.render() → 64x64 frame
```

Subclasses implement `step()` and call `complete_action()` when done handling input.

### Action Conventions

- ACTION1-4: Up/Down/Left/Right (WASD)
- ACTION5: Spacebar
- ACTION6: Click (has x,y coordinates)
- ACTION7: Undo (Z key)

## Code Style

- Line length: 280 characters (for sprite pixel data)
- Strict mypy type checking (tests excluded)
- Pydantic for data validation
