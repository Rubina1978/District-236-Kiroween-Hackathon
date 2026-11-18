import pygame
from settings import SCREEN_HEIGHT, SCREEN_WIDTH
from GameScripts.camera import Camera
from GameScripts.Sprites.floor_pattern import build_floor_pattern


class YSortCameraGroup(pygame.sprite.Group):

    def __init__(self, display_surface):
        super().__init__()

        self.display_surface = display_surface
        self.camera = Camera()

        self.ground_sprites = pygame.sprite.Group()

        # Built once here, not every frame. Drawn behind the real ground so
        # the area past the edge of the map still looks like forest.
        self.floor = build_floor_pattern()

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

    def draw_floor(self):
        # Repeat the floor pattern across the whole screen. The % (modulo)
        # keeps the pattern moving with the camera, so it looks fixed to the
        # world, while we only ever draw a handful of copies.
        width, height = self.floor.get_size()
        start_x = -(int(self.camera.offset.x) % width)
        start_y = -(int(self.camera.offset.y) % height)
        for x in range(start_x, SCREEN_WIDTH, width):
            for y in range(start_y, SCREEN_HEIGHT, height):
                self.display_surface.blit(self.floor, (x, y))

    def custom_draw(self, player):

        # Update camera
        self.camera.update(player)

        # 0. Draw the repeating floor behind everything
        self.draw_floor()

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
