import pygame
from GameScripts.camera import Camera


class YSortCameraGroup(pygame.sprite.Group):

    def __init__(self, display_surface):
        super().__init__()

        self.display_surface = display_surface
        self.camera = Camera()

        # Separate group for ground tiles
        self.ground_sprites = pygame.sprite.Group()

    def custom_draw(self, player):

        # Update camera position
        self.camera.update(player)

        # 1. Draw ground tiles FIRST (never Y-sorted)
        for sprite in self.ground_sprites:
            offset_rect = self.camera.apply(sprite)
            self.display_surface.blit(sprite.image, offset_rect)

        # 2. Draw everything else using Y-sorting
        for sprite in sorted(self.sprites(), key=lambda s: s.rect.bottom):
            offset_rect = self.camera.apply(sprite)
            self.display_surface.blit(sprite.image, offset_rect)
