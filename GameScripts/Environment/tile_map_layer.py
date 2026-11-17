from .environment_obj import EnvrionmentObject
from settings import TILE_SIZE
import random, math


def build_tiles(rows=18 * 8, cols=32 * 8):
    """Return a rows x cols grid filled with 0 or EnvironmentObject."""

    tile_map = [[0 for _ in range(cols)] for _ in range(rows)]

    for r in range(rows):
        for c in range(cols):
            x = (c - r) * (60 / 2)
            y = (c + r) * (30 / 2)

            tile_map[r][c] = generate_tile(x, y)
    
    for r in range(rows):
        for c in range(cols):
            if r == 0 or r == rows - 1 or c == 0 or c == cols - 1:

                tile_map[r][c].set_boundary()

    return tile_map


def generate_tile(x, y):
    """Create one random environment object placed at pixel position (x, y)."""

    obj_type_array = [
        "grass1",
        "grass2",
        "grass3"
    ]

    random_type = random.choice(obj_type_array)

    return EnvrionmentObject(
        type=random_type,
        artwork=random_type,
        x=x,
        y=y
    )