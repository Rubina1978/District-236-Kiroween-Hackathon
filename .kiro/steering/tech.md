# District 236: Technical Guidelines

## Stack
- Python 3 with **Pygame 2.6.1** (pinned in `requirements.txt`).
- Git and GitHub for version control.
- Do NOT replace Pygame with another engine.
- Avoid new dependencies. If one seems necessary, explain why and ask first.

## Environment
- Windows, PowerShell, virtual environment in `.venv`.
- Install: `pip install -r requirements.txt`
- Run: `python main.py`
- Never run the game as a long-running background process from the agent. Ask the user to run it and report what they see.

## Pygame conventions
- Keep the main loop in `main.py` short: handle events, update, draw.
- Use `dt` (delta time in seconds, from `clock.tick(60) / 1000`) for movement so speed does not depend on frame rate.
- Use `pygame.Rect` for positions and collisions.
- Use `pygame.sprite.Sprite` and `Group` for game objects once there are several of them.
- Load images once at start-up, not every frame. Use `convert_alpha()` for PNGs with transparency.
- Put constants (screen size, FPS, speeds, colours) in one settings file, not scattered as magic numbers.

## Code style
- Follow PEP 8. Use clear names and short functions.
- Add short comments that explain why, in simple language.
- Keep the existing working code in `main.py` intact; extend it in small steps.

## Git
- Small, focused commits with clear messages.
- Use a branch per feature when working with teammates.
- Do not commit `.venv`.
