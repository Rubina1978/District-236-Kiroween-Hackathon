from .environment_obj import EnvrionmentObject
from ..EndGame.Alcohol_Bottle import Alcohol
from GameScripts.animator_controller import animator_interface
from settings import TILE_SIZE
import random, math


def build_environment(rows=18 *4, cols=31 * 4):
    """Return a rows x cols grid filled with 0 (empty) or EnvrionmentObject."""

    environment_map = [[0 for _ in range(cols)] for _ in range(rows)]
    # Fill roughly half the cells with a random environment object.
    for _ in range(math.floor((rows * cols) / 8)):
        r = random.randrange(rows)
        c = random.randrange(cols)
        # Convert the grid cell into pixel coordinates for the sprite's rect.
        x = (c - r) * (120 / 2)
        y = (c + r) * (60 / 2)
        environment_map[r][c] = generate_envrionment_obj(x, y)
    

    # for generating the alcohol bottle with co-ordinates
    r = random.randint(16, 28)
    random.randrange(4, 14)

    x = (c - r) * (120 / 2)
    y = (c + r) * (60 / 2)

    environment_map[r][c] = generate_chest(x, y)

    return environment_map


def generate_envrionment_obj(x, y):
    """Create one random environment object placed at pixel position (x, y)."""

    obj_type_array = [
        "tree1",
        "tree2",
        "rock",
        "bush",
        "box",
    ]

    random_type = random.choice(obj_type_array)
    if random_type == "box":
        return EnvrionmentObject(type=random_type, artwork=random_type, x=x, y=y, animator=animator_interface(random_type))
    else:
        return EnvrionmentObject(type=random_type, artwork=random_type, x=x, y=y, animator=None)

def generate_chest(x, y):
    return EnvrionmentObject(
        type="box", 
        artwork="Assets/Artwork/Environment/Objects/Chest/treasure_chest_open_1x.png", 
        x=x, 
        y=y, 
        animator=None
    )