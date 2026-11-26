# settings.py
# All shared constants live here so magic numbers don't get scattered
# across the game. Import what you need, e.g.:
#     from settings import SCREEN_WIDTH, TILE_SIZE
import sys

# True when the game runs in a web browser (the website version). Browsers are
# much slower than a computer at building the map, so the web version uses a
# smaller map and simpler music handling.
RUNNING_ON_WEB = sys.platform == "emscripten"

# Map size, counted in grid cells (rows, columns). The ground grid has twice as
# many cells as the objects grid because ground tiles are half the size, so the
# two always cover the same area. The ant starts near the middle-top of the map.
if RUNNING_ON_WEB:
    GROUND_ROWS, GROUND_COLS = 72, 128      # about 9,200 ground tiles
    OBJECT_ROWS, OBJECT_COLS = 36, 62       # trees, rocks, bushes and boxes
else:
    GROUND_ROWS, GROUND_COLS = 144, 256     # about 36,900 ground tiles
    OBJECT_ROWS, OBJECT_COLS = 72, 124

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
KNOCKBACK_DISTANCE = 100
# How long (seconds) the push takes. A short time feels like a shove.
KNOCKBACK_SECONDS = 0.2
# Seconds the red flash takes to fade out after the ant is bitten.
DAMAGE_FLASH_SECONDS = 0.25

# --- Menu (menu artwork and text only; none of this touches gameplay) ---
# Placeholder title and story. Change the text here whenever you rename the game.
GAME_TITLE = "DISTRICT 236"
# What the bottle is called in the game text. Change it here and the menu,
# help and victory screens all update.
BOTTLE_NAME = "Ant Whiskey"
MENU_STORY = (
    "The world has fallen into decay. Giant spiders roam the wasteland while "
    "the ant colonies struggle to survive. Legend speaks of a sacred bottle of "
    f"{BOTTLE_NAME} hidden beyond the ruins. Many ants have searched. None have returned."
)

# Menu artwork files. Replace these two PNGs to change the pictures; no code
# changes needed. If a file is missing, a scaled-up copy of a gameplay sprite
# is shown instead (the gameplay sprite itself is never changed).
MENU_ANT_IMAGE = "Assets/Artwork/Menu/menu_ant.png"
MENU_SPIDER_IMAGE = "Assets/Artwork/Menu/menu_spider.png"

# The empty space (width, height in pixels) each picture is fitted into, on the
# left and right of the buttons. Any image size works: it is shrunk or grown to
# fit this space first, keeping its proportions.
MENU_ART_BOX = (360, 300)

# How big each picture is inside that space. 1.0 fills the space, 0.5 is half
# size, 1.2 is a little larger. These only affect the menu pictures.
MENU_ANT_SCALE = 1.0
MENU_SPIDER_SCALE = 1.0
# How fast the main-menu story types itself out (characters per second).
MENU_TYPEWRITER_CPS = 45

# Spiders keep at least this far (pixels) from the ant while it is protected
# after a bite, so they do not pile onto it. Larger = more breathing room.
SPIDER_PERSONAL_SPACE = 100

# How fast spiders walk, in pixels per second. Each spider gets a random speed
# between these two numbers when it is created. The ant walks at PLAYER_SPEED
# (240), so spiders below that can be outrun; spiders above it cannot.
SPIDER_SPEED_MIN = 150
SPIDER_SPEED_MAX = 235

# How much bigger the ant is drawn than its original picture. Any number works
# (1 = original, 1.5 = half again, 2 = double). Its collision box grows with it,
# because the box is built from the picture.
# On screen at 1.5 the ant is about 48 px tall: taller than a spider (29) and a
# box (36), a bit shorter than a rock (56), well below a tree (120-138).
PLAYER_SCALE = 1.5

# --- Ending ---
# The bottle picture shown when the chest opens and on the Victory screen.
BOTTLE_IMAGE = "Assets/Artwork/Environment/Objects/Bottle/AntWhiskey.png"
# Seconds the chest-opening moment lasts before the Victory screen appears.
BOTTLE_REVEAL_SECONDS = 2.5
