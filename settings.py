# settings.py
# All shared constants live here so magic numbers don't get scattered
# across the game. Import what you need, e.g.:
#     from settings import SCREEN_WIDTH, TILE_SIZE

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

# Player movement speed in pixels per second. Using a "per second" value with
# delta time keeps the speed the same on any frame rate.
PLAYER_SPEED = 240

# Size of one grid cell in pixels. The environment is laid out on a grid
# where each cell is this many pixels wide and tall.
TILE_SIZE = 120

# Background colour (dark forest green).
BG_COLOR = (35, 75, 45)

# How big to draw each type of map sprite. The number is a multiplier:
# 2 = double size, 3 = triple, 4 = quadruple. To scale just one object type,
# change only its number here. Any type not listed uses ENV_DEFAULT_SCALE.
# The player is not affected - it is loaded separately in player_obj.py.
ENV_SPRITE_SCALES = {
    "tree": 2,
    "rock": 2,
    "bush": 2,
    "box": 2,
}
ENV_DEFAULT_SCALE = 2
