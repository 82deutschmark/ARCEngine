# World Shifter: Game Design Document

**Author:** Claude Opus 4.5
**Date:** 31-January-2026
**Status:** Draft
**Version:** 1.0.0

> **You don't move. The world moves around you.**

---

## 1. Game Concept

### Title
World Shifter

### Elevator Pitch
Navigate mazes by pushing the entire world in the opposite direction of your input. You're fixed at the center while walls, obstacles, and the exit slide toward you.

### Core Innovation
Traditional maze games move the player through a static world. World Shifter inverts this: the player is conceptually stationary while the world shifts around them. This creates a mind-bending spatial reasoning challenge where players must think in reverse.

### Why It Works for ARCEngine
- **Proven mechanic**: Level 5 of `complex_maze.py` demonstrates world-moving with `move_maze: True`
- **Simple implementation**: Invert dx/dy and apply to world sprites instead of player
- **Constraint-native**: Works perfectly within 64x64, turn-based, 16-color limitations
- **Visually distinctive**: Immediately readable in a GIF or screenshot

### Target Experience
Players should feel:
1. Initial confusion (wait, I'm not moving?)
2. "Aha" moment (the world moves, not me!)
3. Growing mastery (I can think in reverse now)
4. Satisfaction (I navigated by staying still)

---

## 2. Core Mechanics

### 2.1 Movement (Inverse)

| Input | Action | Visual Result |
|-------|--------|---------------|
| ACTION1 (W/Up) | Push world DOWN | World slides down, exit approaches from above |
| ACTION2 (S/Down) | Push world UP | World slides up, exit approaches from below |
| ACTION3 (A/Left) | Push world RIGHT | World slides right, exit approaches from left |
| ACTION4 (D/Right) | Push world LEFT | World slides left, exit approaches from right |
| ACTION5 (Space) | Wait (no movement) | Pause for timing puzzles (future) |
| ACTION7 (Z) | Undo | Revert last move |

### 2.2 Player Behavior
- Player sprite is always at a fixed screen position (center of playable area)
- Player is rendered on top of all world sprites
- Player does NOT move on action input
- Player collides with world sprites (prevents illegal moves)

### 2.3 World Behavior
- All sprites tagged `"moveable"` shift in the **opposite** direction of player input
- World movement is blocked if player would collide with a wall
- World has bounded movement limits (cannot scroll infinitely)

### 2.4 Win Condition
- The **exit** sprite collides with the player position
- When exit reaches the player, level is complete
- Complete all levels to win the game

### 2.5 Lose Condition
- **None** for base game (relaxed puzzle)
- Future extension: move counter, hazards

### 2.6 Boundary Rules
Each level defines movement boundaries via `data`:
```python
data = {
    "min_x": -5,   # World can shift left this far
    "max_x": 0,    # World can shift right this far
    "min_y": -5,   # World can shift up this far
    "max_y": 0,    # World can shift down this far
}
```

The world's origin position is tracked, and movement is clamped to these bounds.

---

## 3. Visual Design

### 3.1 Color Palette Usage

| Element | Color Index | Color Name | Rationale |
|---------|-------------|------------|-----------|
| Background | 0 | Black | Clean contrast |
| Player | 8 | Orange | Warm, focal point |
| Walls | 5 | Gray | Neutral, structural |
| Exit | 6 | Green | Goal = positive color |
| Letterbox | 1 | Dark Blue | Frame the action |

### 3.2 Grid Sizes
- **Levels 1-2**: 8x8 (tutorial)
- **Levels 3-4**: 10x10 (intermediate)
- **Levels 5-6**: 12x12 (advanced)

### 3.3 Camera
- Camera viewport matches grid size
- Auto-scales to 64x64 with letterboxing
- Player appears centered in the visible area

---

## 4. Sprites Specification

### 4.1 Player Sprite
```python
"player": Sprite(
    pixels=[[8]],  # Orange 1x1
    name="player",
    blocking=BlockingMode.BOUNDING_BOX,
    interaction=InteractionMode.TANGIBLE,
    layer=10,  # Render on top
    tags=["player"],
)
```

### 4.2 Exit Sprite
```python
"exit": Sprite(
    pixels=[[6]],  # Green 1x1
    name="exit",
    blocking=BlockingMode.BOUNDING_BOX,
    interaction=InteractionMode.TANGIBLE,
    tags=["moveable", "exit"],
)
```

### 4.3 Wall Sprites (Various Configurations)

**Level 1 Maze (8x8 - Tutorial)**
```python
"maze_1": Sprite(
    pixels=[
        [5, 5, 5, 5, 5, 5, 5, 5],
        [5, -1, -1, -1, -1, -1, -1, 5],
        [5, -1, 5, 5, 5, 5, -1, 5],
        [5, -1, 5, -1, -1, -1, -1, 5],
        [5, -1, 5, -1, 5, 5, 5, 5],
        [5, -1, -1, -1, -1, -1, -1, 5],
        [5, -1, 5, 5, 5, 5, -1, 5],
        [5, 5, 5, 5, 5, 5, 5, 5],
    ],
    name="maze_1",
    blocking=BlockingMode.PIXEL_PERFECT,
    interaction=InteractionMode.TANGIBLE,
    layer=-1,
    tags=["moveable", "maze"],
)
```

**Level 2 Maze (8x8 - Longer Path)**
```python
"maze_2": Sprite(
    pixels=[
        [5, 5, 5, 5, 5, 5, 5, 5],
        [5, -1, -1, -1, 5, -1, -1, 5],
        [5, 5, 5, -1, 5, -1, 5, 5],
        [5, -1, -1, -1, -1, -1, -1, 5],
        [5, -1, 5, 5, 5, 5, -1, 5],
        [5, -1, -1, -1, -1, 5, -1, 5],
        [5, 5, 5, 5, -1, -1, -1, 5],
        [5, 5, 5, 5, 5, 5, 5, 5],
    ],
    name="maze_2",
    blocking=BlockingMode.PIXEL_PERFECT,
    interaction=InteractionMode.TANGIBLE,
    layer=-1,
    tags=["moveable", "maze"],
)
```

**Level 3 Maze (10x10 - Intermediate)**
```python
"maze_3": Sprite(
    pixels=[
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [5, -1, -1, -1, -1, 5, -1, -1, -1, 5],
        [5, -1, 5, 5, -1, 5, -1, 5, -1, 5],
        [5, -1, 5, -1, -1, -1, -1, 5, -1, 5],
        [5, -1, 5, -1, 5, 5, 5, 5, -1, 5],
        [5, -1, -1, -1, -1, -1, -1, -1, -1, 5],
        [5, 5, 5, 5, 5, -1, 5, 5, -1, 5],
        [5, -1, -1, -1, -1, -1, -1, -1, -1, 5],
        [5, -1, 5, 5, 5, 5, 5, 5, -1, 5],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
    ],
    name="maze_3",
    blocking=BlockingMode.PIXEL_PERFECT,
    interaction=InteractionMode.TANGIBLE,
    layer=-1,
    tags=["moveable", "maze"],
)
```

**Level 4 Maze (10x10 - Winding Path)**
```python
"maze_4": Sprite(
    pixels=[
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [5, -1, 5, -1, -1, -1, -1, -1, -1, 5],
        [5, -1, 5, -1, 5, 5, 5, 5, -1, 5],
        [5, -1, 5, -1, 5, -1, -1, -1, -1, 5],
        [5, -1, 5, -1, 5, -1, 5, 5, 5, 5],
        [5, -1, 5, -1, 5, -1, -1, -1, -1, 5],
        [5, -1, -1, -1, 5, 5, 5, 5, -1, 5],
        [5, 5, 5, -1, -1, -1, -1, -1, -1, 5],
        [5, -1, -1, -1, 5, 5, 5, 5, -1, 5],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
    ],
    name="maze_4",
    blocking=BlockingMode.PIXEL_PERFECT,
    interaction=InteractionMode.TANGIBLE,
    layer=-1,
    tags=["moveable", "maze"],
)
```

**Level 5 Maze (12x12 - Complex)**
```python
"maze_5": Sprite(
    pixels=[
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [5, -1, -1, -1, 5, -1, -1, -1, -1, -1, -1, 5],
        [5, -1, 5, -1, 5, -1, 5, 5, 5, 5, -1, 5],
        [5, -1, 5, -1, -1, -1, -1, -1, -1, 5, -1, 5],
        [5, -1, 5, 5, 5, 5, 5, -1, 5, 5, -1, 5],
        [5, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 5],
        [5, 5, 5, -1, 5, 5, 5, 5, 5, -1, 5, 5],
        [5, -1, -1, -1, 5, -1, -1, -1, -1, -1, -1, 5],
        [5, -1, 5, 5, 5, -1, 5, 5, 5, 5, -1, 5],
        [5, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 5],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, -1, 5],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
    ],
    name="maze_5",
    blocking=BlockingMode.PIXEL_PERFECT,
    interaction=InteractionMode.TANGIBLE,
    layer=-1,
    tags=["moveable", "maze"],
)
```

**Level 6 Maze (12x12 - Master)**
```python
"maze_6": Sprite(
    pixels=[
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [5, -1, 5, -1, -1, -1, 5, -1, -1, -1, -1, 5],
        [5, -1, 5, -1, 5, -1, 5, -1, 5, 5, -1, 5],
        [5, -1, -1, -1, 5, -1, -1, -1, 5, -1, -1, 5],
        [5, 5, 5, 5, 5, -1, 5, 5, 5, -1, 5, 5],
        [5, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 5],
        [5, -1, 5, 5, 5, 5, 5, -1, 5, 5, -1, 5],
        [5, -1, -1, -1, -1, -1, 5, -1, -1, -1, -1, 5],
        [5, 5, -1, 5, 5, -1, 5, 5, 5, 5, -1, 5],
        [5, -1, -1, -1, -1, -1, -1, -1, -1, 5, -1, 5],
        [5, -1, 5, 5, 5, 5, 5, 5, -1, -1, -1, 5],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
    ],
    name="maze_6",
    blocking=BlockingMode.PIXEL_PERFECT,
    interaction=InteractionMode.TANGIBLE,
    layer=-1,
    tags=["moveable", "maze"],
)
```

---

## 5. Level Design

### Level Design Philosophy
1. **Progressive complexity**: Each level introduces one new challenge
2. **Exit placement matters**: Exit position determines required path
3. **Boundary awareness**: Players must understand world limits
4. **Aha moments**: Each level should have a satisfying solution discovery

### Level Specifications

#### Level 1: The Basics (8x8)
**Goal**: Teach inverse movement concept
**Setup**:
- Player at center (3, 3)
- Exit at (6, 1) - top right of maze
- Simple L-shaped path
- Movement bounds: 3 tiles in each direction

```
##########
#      E #  <- Exit here
# #### # #
# #      #
# # #####
#        #
# ###### #
##########
    P       <- Player fixed here conceptually
```

**What player learns**: "Push right" makes the world go left, bringing the exit closer.

#### Level 2: Longer Journey (8x8)
**Goal**: Build comfort with inverse movement
**Setup**:
- Exit in opposite corner from apparent path
- Requires multiple direction changes
- Slightly larger bounds

#### Level 3: The Corridor (10x10)
**Goal**: Introduce tighter spaces
**Setup**:
- Narrow winding path
- Exit requires precise sequence of moves
- Builds confidence with the mechanic

#### Level 4: The Spiral (10x10)
**Goal**: Spatial planning challenge
**Setup**:
- Spiral-like maze structure
- Exit at center (must bring world to you in spiral)
- Tests mental rotation

#### Level 5: The Maze (12x12)
**Goal**: Complex navigation
**Setup**:
- Multiple viable paths (some dead ends)
- Exit placement requires longer planning
- Larger movement bounds

#### Level 6: The Master (12x12)
**Goal**: Final challenge
**Setup**:
- Most complex maze structure
- Requires full mastery of inverse thinking
- Exit in deceptive position

---

## 6. Game Class Structure

### 6.1 Class Overview

```python
class WorldShifter(ARCBaseGame):
    """The world moves around you, not the other way around."""

    # Type hints for instance attributes
    _player: Sprite
    _world_origin_x: int  # Track world's starting position
    _world_origin_y: int

    def __init__(self) -> None:
        """Initialize game with camera and levels."""
        ...

    def on_set_level(self, level: Level) -> None:
        """Cache references when level loads."""
        ...

    def step(self) -> None:
        """Process one game step with inverse movement."""
        ...

    def _get_world_offset(self) -> tuple[int, int]:
        """Calculate current world offset from origin."""
        ...

    def _can_move_world(self, dx: int, dy: int) -> bool:
        """Check if world movement is within bounds and valid."""
        ...

    def _move_world(self, dx: int, dy: int) -> None:
        """Move all world sprites in the given direction."""
        ...

    def _check_exit_collision(self) -> bool:
        """Check if exit has reached the player position."""
        ...
```

### 6.2 Core Logic Flow

```python
def step(self) -> None:
    """Process one game step."""

    # 1. Determine intended movement direction
    dx, dy = 0, 0
    if self.action.id == GameAction.ACTION1:      # Up pressed
        dy = 1   # World moves DOWN (opposite)
    elif self.action.id == GameAction.ACTION2:    # Down pressed
        dy = -1  # World moves UP (opposite)
    elif self.action.id == GameAction.ACTION3:    # Left pressed
        dx = 1   # World moves RIGHT (opposite)
    elif self.action.id == GameAction.ACTION4:    # Right pressed
        dx = -1  # World moves LEFT (opposite)

    # 2. Check if movement is valid
    if dx != 0 or dy != 0:
        if self._can_move_world(dx, dy):
            self._move_world(dx, dy)

    # 3. Check win condition (exit reached player)
    if self._check_exit_collision():
        if self.is_last_level():
            self.win()
        else:
            self.next_level()

    # 4. Complete the action
    self.complete_action()
```

### 6.3 World Movement Logic

```python
def _can_move_world(self, dx: int, dy: int) -> bool:
    """Check if world can move in the given direction."""

    # Get current offset
    current_offset_x, current_offset_y = self._get_world_offset()
    new_offset_x = current_offset_x + dx
    new_offset_y = current_offset_y + dy

    # Check bounds from level data
    min_x = self.current_level.get_data("min_x") or -10
    max_x = self.current_level.get_data("max_x") or 10
    min_y = self.current_level.get_data("min_y") or -10
    max_y = self.current_level.get_data("max_y") or 10

    if not (min_x <= new_offset_x <= max_x):
        return False
    if not (min_y <= new_offset_y <= max_y):
        return False

    # Check collision: would player be inside a wall after movement?
    # Get maze sprite and check if player position would collide
    player_pos = (self._player.x, self._player.y)
    maze = self.current_level.get_sprites_by_tag("maze")[0]

    # Simulate: if maze moves by (dx, dy), does player's fixed position
    # now overlap with a wall pixel?
    # Use collision detection to verify

    return True  # Simplified - implement full collision check

def _move_world(self, dx: int, dy: int) -> None:
    """Move all moveable sprites."""
    moveable = self.current_level.get_sprites_by_tag("moveable")
    for sprite in moveable:
        sprite.move(dx, dy)
```

### 6.4 Exit Collision Detection

```python
def _check_exit_collision(self) -> bool:
    """Check if exit sprite overlaps with player."""
    exit_sprite = self.current_level.get_sprites_by_tag("exit")[0]
    return self._player.collides_with(exit_sprite)
```

---

## 7. Implementation Checklist

### Phase 1: Project Setup
- [ ] Create `games/` directory
- [ ] Create `games/__init__.py` (registry)
- [ ] Create `games/world_shifter/` directory
- [ ] Create `games/world_shifter/__init__.py`

### Phase 2: Sprites
- [ ] Create `games/world_shifter/sprites.py`
- [ ] Define player sprite
- [ ] Define exit sprite
- [ ] Define maze sprites for all 6 levels

### Phase 3: Levels
- [ ] Create `games/world_shifter/levels.py`
- [ ] Define Level 1 (tutorial)
- [ ] Define Level 2 (longer path)
- [ ] Define Level 3 (10x10)
- [ ] Define Level 4 (10x10 spiral)
- [ ] Define Level 5 (12x12)
- [ ] Define Level 6 (12x12 master)

### Phase 4: Game Logic
- [ ] Create `games/world_shifter/game.py`
- [ ] Implement `__init__` with camera setup
- [ ] Implement `on_set_level` to cache references
- [ ] Implement inverse movement in `step()`
- [ ] Implement `_can_move_world()` with bounds checking
- [ ] Implement `_move_world()` for all moveable sprites
- [ ] Implement `_check_exit_collision()` for win detection

### Phase 5: Registry
- [ ] Register WorldShifter in `games/__init__.py`

### Phase 6: Testing
- [ ] Create `tests/games/test_world_shifter.py`
- [ ] Test inverse movement (up input moves world down)
- [ ] Test boundary limits (world stops at bounds)
- [ ] Test collision (can't move world into player)
- [ ] Test win condition (exit reaches player)
- [ ] Test full playthrough of all levels

### Phase 7: Polish
- [ ] Playtest all levels for difficulty curve
- [ ] Adjust maze designs if needed
- [ ] Verify visual clarity at 64x64

---

## 8. Testing Guide

### 8.1 Manual Testing

```python
from games import get_game
from arcengine import ActionInput, GameAction

# Create game
game = get_game("world_shifter")

# Get initial frame
frames = list(game.perform_action(ActionInput(id=GameAction.RESET)))
print(f"Initial state: {frames[-1].state}")

# Test inverse movement: press "right" should move world "left"
frames = list(game.perform_action(ActionInput(id=GameAction.ACTION4)))
# Observe: exit and maze moved left, player stayed in place

# Continue until exit reaches player
# ...
```

### 8.2 Automated Test Cases

```python
def test_inverse_movement_right():
    """Pressing right should move world left."""
    game = WorldShifter()
    list(game.perform_action(ActionInput(id=GameAction.RESET)))

    # Get initial exit position
    exit_before = game.current_level.get_sprites_by_tag("exit")[0]
    x_before = exit_before.x

    # Move right
    list(game.perform_action(ActionInput(id=GameAction.ACTION4)))

    # Exit should have moved left (x decreased)
    exit_after = game.current_level.get_sprites_by_tag("exit")[0]
    assert exit_after.x < x_before or game.state != GameState.NOT_FINISHED

def test_boundary_enforcement():
    """World should not move beyond defined bounds."""
    game = WorldShifter()
    list(game.perform_action(ActionInput(id=GameAction.RESET)))

    # Move in one direction many times
    for _ in range(20):
        list(game.perform_action(ActionInput(id=GameAction.ACTION4)))

    # World should have stopped at boundary, not gone infinitely
    maze = game.current_level.get_sprites_by_tag("maze")[0]
    assert maze.x >= game.current_level.get_data("min_x")

def test_win_condition():
    """Game should win when exit reaches player."""
    # Would need to know exact solution path
    # Or set up a trivial level for testing
    pass
```

---

## 9. Extension Ideas (Post-MVP)

### 9.1 Move Counter UI
Display moves taken using `ToggleableUserDisplay` in letterbox area.

### 9.2 Hazards
- **Spikes**: If spikes reach player position, level resets
- **Chasers**: Enemies that move toward player each turn

### 9.3 Portals
World-wrapping: moving world off one edge brings it in from the other.

### 9.4 Multi-World Levels
Some sprites are on "layer A" (move together), others on "layer B" (move separately).

### 9.5 Time Challenge
Optional par moves for each level, star rating system.

---

## 10. File Structure Summary

```
games/
├── __init__.py              # Registry with get_game(), list_games()
└── world_shifter/
    ├── __init__.py          # Exports WorldShifter, GAME_ID, VERSION
    ├── sprites.py           # SPRITES dict with all sprite definitions
    ├── levels.py            # LEVELS list with all level definitions
    └── game.py              # WorldShifter class with game logic
```

---

## Summary

**World Shifter** is a puzzle game that inverts the fundamental assumption of maze navigation. By shifting the world instead of the player, it creates a fresh spatial reasoning challenge using proven ARCEngine mechanics.

**Key implementation points:**
1. Player is fixed; world sprites are tagged `"moveable"`
2. Input direction is inverted before applying to world sprites
3. Collision prevents world from moving player into walls
4. Exit reaching player triggers level completion
5. Level `data` defines movement bounds

**Estimated implementation effort:** 150-200 lines of code across 4 files.
