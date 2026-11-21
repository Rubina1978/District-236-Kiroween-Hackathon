import pygame
from GameScripts.sprite_cache import load as load_sprite

class Alcohol(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()  # Initialise the Pygame Sprite
        self.type = "alcohol"
        self.is_extracting = False
        self.reward = "x2"
        self.image = load_sprite(image)

        # Give the sprite a rect (needed for positioning/drawing)
        self.rect = self.image.get_rect()

    def interact(self):
        self.is_extracting = True

    def get_type(self):
        return self.type