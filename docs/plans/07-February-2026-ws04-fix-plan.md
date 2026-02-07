# Plan - Fix WS04 Sprite Placement and Energy Bar Colors

## Goal
Fix critical issues in `games/official/ws04.py`:
1.  **Sprite Placement**: Remove the duplicate player sprite in Level 1 and ensure the shape-changer (`vxy`) and other changers are correctly placed and not overlapping doorways.
2.  **Energy Bar Colors**: Update the energy bar and lives display to use non-gray colors (Yellow 11 and Purple 15) instead of 0-5.
3.  **Color Consistency**: Correct the comments and usage of colors to match `Arc3Colors.md` (e.g., color 8 is Red, not Cyan).

## Proposed Changes

### 1. `games/official/ws04.py`

#### Energy Interface (`VerticalEnergyInterface`)
- Update `render_interface` to use color `11` (Yellow) for the energy bar and `15` (Purple) for the empty part.
- Update lives display to use color `11` or `15`.
- Update level progress dots to use non-gray colors.

#### Level 1 (`tutorial`)
- Remove the duplicate `pca` sprite (it was likely added twice or at the wrong position).
- Verify all other sprites are in their intended positions.

#### Color Mapping & Comments
- Update the theme description to correctly identify color `8` as Red (or change it to `10` if Cyan was intended, but the user seems to like the Red frames in the screenshot).
- Ensure color `4` (Darker Gray) is replaced with `11` (Yellow) where appropriate.

## TODOs
1.  [ ] Modify `VerticalEnergyInterface.render_interface` in `games/official/ws04.py` to fix energy bar and lives colors.
2.  [ ] Modify `Level 1` sprite list in `games/official/ws04.py` to remove duplicate player sprite and fix placements.
3.  [ ] Update color comments and palette in `games/official/ws04.py`.
4.  [ ] Verify the changes by running the game (if possible) or carefully checking coordinates.
5.  [ ] Update `CHANGELOG.md`.

## Verification Steps
- Check that no colors 0-5 are used in the UI elements on the right.
- Ensure only one player sprite exists in Level 1.
- Confirm the shape-changer and other changers are not overlapping the door frame in any level.


Art needs to be more creative in general. The player sprite looks awful. It's gray on top of pink. We could be much more creative with how this looks. I believe it's a five by five box. I mean, there's a lot we could do in terms of a five by five grid pixel art.