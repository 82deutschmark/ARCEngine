
import sys
import os
import numpy as np

sys.path.append(os.getcwd())

# -- Import --
try:
    from games.official.ct03 import Ct03
    print("Import successful")
except ImportError as e:
    print(f"Import failed: {e}")
    sys.exit(1)

# -- Instantiation --
try:
    game = Ct03()
    print(f"Instantiation successful: {game.game_id}")
except Exception as e:
    print(f"Instantiation failed: {e}")
    sys.exit(1)

# -- Camera colors --
print("Checking colors...")
print(f"  Camera background: {game.camera.background}")
print(f"  Camera letter_box: {game.camera.letter_box}")
if game.camera.background <= 5:
    print("  FAIL: Camera background color <= 5")
if game.camera.letter_box <= 5:
    print("  FAIL: Camera letter_box color <= 5")

# -- Sprites (level 0 already set by __init__) --
print("Checking Level 0 sprites...")
sprites = game.current_level.get_sprites()
print(f"  Sprite count: {len(sprites)}")
bad_visible = []
for s in sprites:
    if not s.is_visible:
        continue  # invisible constraint sprites may use 0 for logic encoding
    has_bad = False
    for row in s.pixels:
        for p in row:
            if 0 <= int(p) <= 5:
                has_bad = True
                break
        if has_bad:
            break
    if has_bad:
        bad_visible.append(s.name)
if bad_visible:
    print(f"  FAIL: Visible sprites with color 0-5: {bad_visible}")
else:
    print("  OK: No visible sprites use colors 0-5")

# -- Action test: click center tile on Level 0 --
print("Checking Step Logic...")
from arcengine import ActionInput, GameAction

center_tile = None
for s in game.current_level.get_sprites_by_tag("tile"):
    if s.x == 14 and s.y == 14:
        center_tile = s
        break

if not center_tile:
    print("  FAIL: Could not find center tile at (14,14)")
else:
    initial_color = int(center_tile.pixels[1, 1])
    print(f"  Center tile at ({center_tile.x},{center_tile.y}), initial color={initial_color}")

    # Camera is resized to level grid_size (32x32), so scale = 64/32 = 2
    # Grid 15 (center of 3x3 tile at 14) -> screen 15*2 = 30
    screen_x, screen_y = 15 * 2, 15 * 2
    action = ActionInput(id=GameAction.ACTION6.value, data={"x": screen_x, "y": screen_y})
    frame_data = game.perform_action(action)

    new_color = int(center_tile.pixels[1, 1])
    print(f"  After click: color={new_color}")
    if new_color != initial_color:
        print(f"  SUCCESS: Color cycled {initial_color} -> {new_color}")
    else:
        print("  FAIL: Color did not change")

print("Done.")
