import pygame
import random
from settings import ENV_SPRITE_SCALES, ENV_DEFAULT_SCALE


class EnvrionmentObject(pygame.sprite.Sprite):
    """A piece of the environment (tree, rock, bush, box) drawn on the map.

    Now extends pygame.sprite.Sprite so it has the .image and .rect attributes
    that the camera and y-sort group rely on, and so it can be added to a
    sprite group alongside the player.
    """

    def __init__(self, type, artwork, x, y):
        # Call the parent Sprite constructor first so this object works with
        # pygame sprite groups.
        super().__init__()
        self.type = type
        self.artwork = artwork

        # Load the PNG ONCE when the object is created, not every frame.
        # convert_alpha() keeps the transparent edges and makes blitting fast.
        if self.type == "box":
            path = f"Assets/Artwork/Environment/Objects/Box/{self.type}_1.png"
        else:
            path = f"Assets/Artwork/Environment/Scenery/{self.type}.png"

        self.image = pygame.image.load(path).convert_alpha()
        # Double the size of every map sprite (trees, rocks, bushes, boxes).
        # scale2x is made for pixel art and makes the image exactly 2x bigger.
        # The player is loaded separately in player_obj.py, so it is unaffected.
        if self.type == "tree":
            self.image = pygame.transform.scale2x(self.image)
            self.image = pygame.transform.scale2x(self.image)
        else:
            self.image = pygame.transform.scale2x(self.image)
        # rect is where the sprite sits in the world. x, y come from its grid
        # cell (col * TILE_SIZE, row * TILE_SIZE).
        self.rect = self.image.get_rect(topleft=(x, y))

    def get_type(self):
        return self.type

    def get_artwork(self):
        return self.artwork

    def give_loot(self):
        items = [
            "junk",
            "spider",
            "health"
        ]
        if self.type == "box":
            return random.choice(items)
        else:
            return 0
