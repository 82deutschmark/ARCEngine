# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- **games/official/gw02.py** - Clean rewrite of Gravity Well puzzle (gw01)
  - All cryptic abbreviations replaced with readable names (e.g., `VDC`→`BACKGROUND_COLOR`, `uwl()`→`update_well_pixels()`, `self.col`→`self.orbs_collected`)
  - Grayscale colors replaced with themed palette: platforms use Purple (15) fill + Dark Red (13) edge, well centers use Pink (6), letterbox uses Black (5) to match background
  - Improved orb sprites: light orbs have white center highlight, heavy orbs have cyan center
  - Full docstrings added to all methods
  - Level comments describe puzzle objectives
  - gw01.py renamed to gw01_deprecated.py and kept for reference
  - **Author**: Claude Sonnet 4

### Changed

- **games/official/ws03.py** - Redesigned player sprite from flat checkerboard to mage/wizard character
  - Old: Blue (9) + Magenta (6) checkerboard pattern (no character shape, just a grid)
  - New: Pointy Purple (15) hat, White (0) gem, Orange (12) magic torso, Magenta (6) robe, Dark Red (13) boots
  - Distinct silhouette from WS04's astronaut; fits WS03's fog-of-war mystery theme
  - **Author**: Cascade (Claude Sonnet 4)

### Fixed

- **games/official/ws04.py** - Fixed unsolvable levels 1-4 due to missing changers
  - Levels had initial shape/color/rotation values that didn't match slot requirements, but lacked the changers needed to change them. Each level's initial values now match slot values for dimensions without a changer:
  - Level 1 (tutorial): initial_shape 2→3, initial_color 9→12 (only rotation changer available)
  - Level 2 (corridor): initial_shape 4→1, initial_color 8→14 (only rotation changer available)
  - Level 3 (diamond): initial_shape 5→0 (has color+rotation changers but no shape changer)
  - Level 4 (split): initial_rotation 180→0 (has shape+color changers but no rotation changer)
  - Levels 5-7 were already correct (all three changers present)
  - **Author**: Cascade (Claude Sonnet 4)

- **games/official/ws04.py** - Fixed energy bar, lives, and progress dot colors using grayscale (0-5) instead of theme colors
  - Energy bar: changed from color 4 (Darker Gray) to 11 (Yellow) for filled segments
  - Lives display: changed from color 3 (Dark Gray) to 15 (Purple) for remaining lives
  - Progress dots: changed completed=4→11 (Yellow), current=3→15 (Purple)
  - **Author**: Claude Opus 4.6

- **games/official/ws04.py** - Redesigned player sprite to match Cyan/Blue/Yellow theme
  - Old: Black outline, Purple helmet, Orange suit (clashed with theme)
  - New: Yellow (11) helmet, Blue (9) suit, Cyan (8) boots/shoulders, Black (5) visor
  - **Author**: Claude Opus 4.6

- **games/official/ws02.py, ws04.py** - Removed spurious `complete_action()` calls in key-error and death-overlay paths
  - Root cause: LS20 (the template) returns from `step()` WITHOUT calling `complete_action()` in error/death paths, allowing the engine to auto-loop and produce a two-frame animation within a single keypress. WS02 and WS04 incorrectly added `complete_action()` before returning, which broke this multi-frame pattern and forced the player to press an extra key to dismiss the error flash or death overlay.
  - WS01 and WS03 were already correct (matched LS20's pattern).
  - **Author**: Cascade (Claude Sonnet 4)

### Added

- **docs/Reference/Engine-Reference/Documentation-Index.md** - Curated mirror of https://docs.arcprize.org/llms.txt for fast navigation of ARC-AGI-3 documentation
  - Groups commands, toolkit pages, platform policies, and templates per official categories
  - Highlights refresh instructions to keep the list synchronized with upstream
  - **Author**: Cascade (OpenAI Assistant)

- **games/official/** - Official ARC-AGI-3 preview games downloaded via `arc-agi` API
  - `ls20.py` - Shape-matching navigation puzzle (7 levels, 4 actions)
  - `ft09.py` - Color-cycling constraint satisfaction (6 levels, 6 actions)
  - `vc33.py` - Rail-switching train routing (7 levels, click-only)
  - All MIT licensed by ARC Prize Foundation
  - **Author**: ARC Prize Foundation (downloaded by Claude Sonnet 4)

- **docs/OFFICIAL_PREVIEW_GAMES.md** - Deep analysis of official preview game mechanics
  - Detailed breakdown of ls20 shape/color/rotation matching
  - ft09 constraint satisfaction logic explained
  - vc33 rail switching and animation system
  - Code patterns and obfuscation notes
  - Instructions for cloning and modification
  - **Author**: Claude Sonnet 4

- **examples/inspect_preview_games.py** - Utility to download and inspect official games via API
  - **Author**: Claude Sonnet 4

- **ARC3_OFFICIAL_EXAMPLES.md** - Comprehensive documentation of official ARC-AGI-3 example games from https://docs.arcprize.org/
  - Official preview games reference (ls20, ft09, vc33)
  - Complete ab12 click-to-remove example with full source code
  - Editing existing games guide
  - Sprite techniques (modification, inline edits, dynamic add/remove)
  - Animation pattern for multi-frame effects
  - Directory structure reference for both official and local formats
  - Color palette reference
  - **Author**: Claude Sonnet 4

- **examples/ab12_template.py** - Clonable game template based on official ARC Prize Foundation example
  - Procedural sprite generation with seeding
  - ACTION6 (click) handling with coordinate conversion
  - Level progression with varying grid sizes
  - Local testing harness included
  - **Author**: Claude Sonnet 4
