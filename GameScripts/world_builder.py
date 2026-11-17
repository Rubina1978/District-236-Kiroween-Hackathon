from .Environment.environment_map import build_environment
from .Environment.tile_map_layer import build_tiles
from .map_obj import GridMap

def world_build(tiles):
    """ Main Function for quick building world/levels """

    if tiles == True:
        return GridMap(grid=build_tiles())
    else:
        return GridMap(grid=build_environment())