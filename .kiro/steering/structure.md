# Kota236: Project Structure

## Current state
Only `main.py` exists: a window, a 60 FPS clock, a quit event and a green background. Everything below is a **plan**. Create files only when a feature needs them, not in advance.

## Planned layout
```
main.py            # entry point, main loop only
settings.py        # constants: screen size, FPS, speeds, colours
player.py          # the ant: movement, shooting, ammo, health
bullet.py          # projectiles
enemies.py         # spider sprites, uses the teammate's AI code
items.py           # ammo boxes, health kits, final bottle
ghost.py           # hint character
hud.py             # ammo and health display
assets/
  images/          # PNG sprites from the artist
  sounds/          # optional
```

## Rules
- One responsibility per file. Keep files short and readable.
- `main.py` wires things together; game logic lives in the other modules.
- Avoid circular imports. Shared constants go in `settings.py`.
- Teammate boundaries:
  - Spider AI is written by a teammate. Keep a small, clear interface (for example, a spider has an `update(dt, player_pos)` method) so their code plugs in without edits to the rest of the game.
  - Artwork arrives as PNG files in `assets/images/`. Sprite sizes and file naming are **to be agreed** with the artist. Until then, use simple coloured rectangles as placeholders.
