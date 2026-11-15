import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT


class Camera:
    def __init__(self):
        # offset is how far the camera has scrolled from the top-left corner
        # of the world. Stored as a Vector2 for easy math.
        self.offset = pygame.Vector2(0, 0)

    def update(self, target):
        # Centre the camera on the target (the player) so the player stays
        # roughly in the middle of the screen as it moves around the world.
        self.offset.x = target.rect.centerx - SCREEN_WIDTH // 2
        self.offset.y = target.rect.centery - SCREEN_HEIGHT // 2

    def apply(self, sprite):
        # Move a sprite's rect by the negative offset so world positions
        # become screen positions. Returns a NEW rect; it does not change the
        # sprite's own rect.
        return sprite.rect.move(-self.offset.x, -self.offset.y)
