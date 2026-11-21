import pygame
from GameScripts.sprite_cache import load as load_sprite

class Alcohol(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()  # Initialise the Pygame Sprite
        self.type = "alcohol"
        self.is_extracting = False
        self.reward = "x2"
        self.image = load_sprite(image)
        self.image = pygame.transform.scale2x(self.image)
        self.image = pygame.transform.scale2x(self.image)

        # Give the sprite a rect (needed for positioning/drawing)
        self.rect = self.image.get_rect(topleft=(x, y))

    def interact(self):
        self.is_extracting = True

    def get_type(self):
        return self.type