# Game Developer Glossary

*A friendly guide to ARCEngine terms for designers and non-technical creators*

---

## Core Concepts

### **Game World**
The space where your game happens. Everything lives inside a 64×64 pixel canvas that players see. Think of it as your game's stage.

### **Actions**
How players interact with your game. Each turn, the player chooses one action (like moving up, down, or clicking somewhere). Your game responds to this action and shows what happens.

### **Frames**
The visual steps that make up an action. Simple actions might show just one frame, but you can create animations by showing multiple frames over a few moments. Each action can show up to 1000 frames.

---

## Building Blocks

### **Levels**
Think of levels as rooms or scenes in your game. Each level contains all the visual elements (sprites) that exist in that space. You can have multiple levels, and players move between them as they progress.

*Use levels when you want to:*
- Create different areas or rooms
- Separate easy and hard challenges
- Tell a story across different scenes

### **Sprites**
These are the visual objects in your game—characters, items, walls, decorations, anything you can see. Each sprite is made of colored pixels on a grid.

*Sprites can be:*
- **Characters** that move around (player, enemies, NPCs)
- **Objects** that interact with characters (keys, doors, switches)
- **Environment** that shapes the space (walls, floors, water)
- **UI elements** that show information (buttons, indicators)

### **Camera**
The window through which players view your game world. While your game world can be larger than 64×64 pixels, the camera shows just a portion of it, scaled to fit the player's screen. You can move the camera to follow action or reveal new areas.

---

## Sprite Properties

### **Position**
Where a sprite exists in your game world (x and y coordinates). This determines where players see it.

### **Layer**
Which sprites appear in front of others. Higher layer numbers render on top—useful for making characters appear above floors or behind objects.

### **Scale**
How big or small a sprite appears. You can make sprites larger (2×, 3× size) or smaller (half size, third size) to create visual variety.

### **Rotation**
How a sprite is oriented. You can rotate sprites in 90-degree increments (up, right, down, left) to face different directions.

### **Interaction**
How sprites behave in the game world:
- **Tangible**: Visible and solid—characters can't walk through these
- **Intangible**: Visible but ghost-like—characters pass through
- **Invisible**: Can't be seen but still solid—like invisible walls
- **Removed**: Neither visible nor solid—completely gone from the game

### **Collision**
How sprites detect when they touch each other:
- **Pixel Perfect**: Only counts as collision when actual colored pixels overlap
- **Bounding Box**: Counts as collision when the rectangular edges touch
- **Not Blocked**: Never collides, even if sprites overlap

---

## Game Flow

### **Turn-Based Play**
Players take turns choosing actions. After each action, your game shows what happened, then waits for the next player input. This creates thoughtful, strategic gameplay rather than real-time action.

### **Winning and Losing**
Your game can declare victory or defeat at any point. When a player wins, they've completed the game's main challenge. When they lose, they might need to restart or try a different approach.

### **Reset Options**
Players can start over in two ways:
- **Level Reset**: Just restart the current room/level
- **Full Reset**: Start the entire game from the beginning

---

## Visual Design

### **Colors**
Your game uses a 16-color palette. Each pixel in your sprites is assigned one of these colors. This creates a consistent, retro visual style and keeps file sizes small.

### **Transparency**
Some pixels can be transparent (invisible). This lets you create irregular shapes—think of character sprites that don't fill their entire rectangular box.

### **Animation**
Create movement by showing multiple frames in sequence. A character walking might show several frames with legs in different positions. An object appearing might fade in over several frames.

---

## Common Patterns

### **Player Character**
Usually the main sprite that responds to player actions. Give it a unique name and make it tangible so it interacts with the world.

### **Walls and Barriers**
Solid sprites that block movement. Use these to create mazes, rooms, or obstacles players must navigate around.

### **Collectibles**
Sprites that disappear when touched. Keys, coins, or power-ups that players gather to progress.

### **Switches and Doors**
Pairs of sprites that work together—touching a switch opens a door elsewhere. This creates cause-and-effect puzzles.

### **Moving Platforms**
Sprites that change position over time, creating dynamic challenges for players to navigate.

---

## Tips for Designers

- **Start simple**: Create basic shapes first, then add details
- **Think in layers**: Put floors on low layers, characters on middle layers, UI on high layers
- **Use names wisely**: Give sprites meaningful names so you can reference them easily
- **Test interactions**: Make sure solid objects actually block movement where intended
- **Consider scale**: Larger sprites are easier to see but take more space
- **Plan your palette**: Use colors consistently to help players understand your game world

---

## Remember

This engine is designed for creativity, not complexity. You don't need programming knowledge to design engaging games—just think about what you want players to see and do, then use these building blocks to bring that vision to life.

The best games start with simple ideas: move a character, collect something, reach a goal. Everything else builds from there.
