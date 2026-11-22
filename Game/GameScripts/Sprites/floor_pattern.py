import random
import pygame
from settings import ISO_STEP_X, ISO_STEP_Y

GRASS_TILES = ["grass1", "grass2", "grass3"]

# The pattern is this many "repeats" wide and tall. A bigger number gives a
# less obvious repeat but a bigger Surface in memory.
REPEATS = 8


def build_floor_pattern():
    """Build ONE small picture of grass that can be repeated forever.

    Why: the real ground only exists inside the map. Outside it the screen
    would show a flat colour. Repeating this pattern behind everything makes
    the area past the edge look like forest too, without creating more tiles.
    """
    # Load and double the size of each grass tile, the same as the real ground.
    images = []
    for name in GRASS_TILES:
        image = pygame.image.load(f"Assets/Artwork/Tiles/{name}.png").convert_alpha()
        images.append(pygame.transform.scale2x(image))

    # The tile grid repeats every 2 steps across and every 2 steps down.
    width = ISO_STEP_X * 2 * REPEATS
    height = ISO_STEP_Y * 2 * REPEATS

    # SRCALPHA means this Surface keeps transparency, like a PNG.
    pattern = pygame.Surface((width, height), pygame.SRCALPHA)

    # Decide which grass picture each grid point gets BEFORE drawing, so the
    # shifted copies below use the same picture as the original.
    spots = []
    for y in range(0, height, ISO_STEP_Y):
        for x in range(0, width, ISO_STEP_X):
            # Only every second grid point holds a tile (the grid is a diamond).
            if (x // ISO_STEP_X + y // ISO_STEP_Y) % 2 == 0:
                spots.append((x, y, random.choice(images)))

    # Tiles near the right/bottom edge stick out past the pattern. Drawing
    # extra copies shifted by one pattern size wraps that part round to the
    # left/top, so the repeat has no visible seam. The shifted copies are
    # drawn FIRST so the normal tiles end up in front of them, like the
    # real ground where lower tiles overlap the ones above.
    for shift_y in (-height, 0):
        for shift_x in (-width, 0):
            for x, y, image in spots:
                pattern.blit(image, (x + shift_x, y + shift_y))

    return pattern
