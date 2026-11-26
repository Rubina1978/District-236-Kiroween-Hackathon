import settings
from .Environment.environment_map import build_environment
from .Environment.tile_map_layer import build_tiles
from .map_obj import GridMap


def world_build(tiles):
    """ Main Function for quick building world/levels """
    # The map size comes from settings.py (smaller on the website version).
    if tiles == True:
        return GridMap(grid=build_tiles(rows=settings.GROUND_ROWS, cols=settings.GROUND_COLS))
    else:
        return GridMap(grid=build_environment(rows=settings.OBJECT_ROWS, cols=settings.OBJECT_COLS))
