import pygame
from settings import SCREEN_HEIGHT, SCREEN_WIDTH
from GameScripts.camera import Camera


class YSortCameraGroup(pygame.sprite.Group):

    def __init__(self, display_surface):
        super().__init__()

        self.display_surface = display_surface
        self.camera = Camera()

        self.ground_sprites = pygame.sprite.Group()

        # Environment culling
        self.culling_margin = 200

        self.camera_rect = pygame.Rect(
            0, 0,
            SCREEN_WIDTH,
            SCREEN_HEIGHT
        )

    def is_visible(self, sprite):

        # Camera's world-space rectangle
        self.camera_rect.topleft = (
            int(self.camera.offset.x),
            int(self.camera.offset.y)
        )

        # Add some extra visibility around screen edges
        visible_area = self.camera_rect.inflate(
            self.culling_margin * 2,
            self.culling_margin * 2
        )

        return sprite.rect.colliderect(visible_area)

    def custom_draw(self, player):

        # Update camera
        self.camera.update(player)

        # 1. Draw ground tiles
        for sprite in self.ground_sprites:

            if self.is_visible(sprite):

                offset_rect = self.camera.apply(sprite)

                self.display_surface.blit(
                    sprite.image,
                    offset_rect
                )

        # 2. Draw Y-sorted sprites, with culling
        visible_sprites = [
            sprite for sprite in self.sprites()
            if self.is_visible(sprite)
        ]

        for sprite in sorted(
            visible_sprites,
            key=lambda s: s.rect.bottom
        ):

            offset_rect = self.camera.apply(sprite)

            self.display_surface.blit(
                sprite.image,
                offset_rect
            )

    def get_camera(self):
        return self.camera
