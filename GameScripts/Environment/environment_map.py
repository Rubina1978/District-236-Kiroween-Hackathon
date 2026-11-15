from .environment_obj import EnvrionmentObject
import random

def build_environment(rows=18, cols=32):
    """Return a rows x cols grid filled with 0 (empty)."""
    environment_map = [[0 for _ in range(cols)] for _ in range(rows)]

    for _ in range((rows * cols)):
        r, c = random.randrange(18), random.randrange(32)
        environment_map[r][c] = generate_envrionment_obj()

    return environment_map
    
    # Dylan's note
    # ------------------------------------------------
    # For testing the output - I might need this code for something later
    # ------------------------------------------------
    # for row in environment_map:
    #     for each in row:
    #         if isinstance(each, EnvrionmentObject):
    #             print(each.get_type())
    #         else:
    #             print(each)

def generate_envrionment_obj():
    """ Function for quick envrionment obj generation """

    obj_type_array = [
        "tree",
        "rock",
        "bush",
        "box",
    ]

    random_type = random.choice(obj_type_array)

    obj = EnvrionmentObject(type=random_type, artwork=random_type)
    return obj

build_environment()