from .Environment.environment_map import build_environment
from .map_obj import GridMap

def world_build():
    """ Main Function for quick building world/levels """

    return GridMap(grid=build_environment())