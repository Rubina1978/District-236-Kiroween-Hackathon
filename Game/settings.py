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

# Background colour: the average colour of the grass tiles. It shows anywhere
# the world has no tiles (for example past the edge of the map), so it should
# look like forest floor and not like a black hole.
BG_COLOR = (55, 90, 32)

# How big to draw each type of map sprite. The number is a multiplier:
# 2 = double size, 3 = triple, 4 = quadruple. To scale just one object type,
# change only its number here. Any type not listed uses ENV_DEFAULT_SCALE.
# The player is not affected - it is loaded separately in player_obj.py.
# How far apart ground tiles sit, in pixels, along the isometric grid. These
# match the (60 / 2) and (30 / 2) used in tile_map_layer.py. The floor pattern
# needs the same spacing so its tiles line up with the real ground.
ISO_STEP_X = 30
ISO_STEP_Y = 15

ENV_SPRITE_SCALES = {
    "tree": 2,
    "rock": 2,
    "bush": 2,
    "box": 2,
}
ENV_DEFAULT_SCALE = 2

# --- Combat balance ---

INVULNERABLE_MS = 2000
# Milliseconds between each blink (show / hide) while the ant is protected.
BLINK_MS = 100
# How far (pixels) a bite pushes the ant away from the spider.
KNOCKBACK_DISTANCE = 40
# How long (seconds) the push takes. A short time feels like a shove.
KNOCKBACK_SECONDS = 0.15
# Seconds the red flash takes to fade out after the ant is bitten.
DAMAGE_FLASH_SECONDS = 0.25
