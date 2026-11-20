import pygame
from settings import SCREEN_HEIGHT, SCREEN_WIDTH
from GameScripts.camera import Camera
from GameScripts.Sprites.floor_pattern import build_floor_pattern
from GameScripts.Enemies.pooling_system import PoolingSystem
from GameScripts.lighting_controller import LightingController
import random


class YSortCameraGroup(pygame.sprite.Group):

    def __init__(self, display_surface):
        super().__init__()

        self.lighting = LightingController(
            SCREEN_WIDTH,
            SCREEN_HEIGHT
        )
        self.spawn_interval = 3000  # 3 seconds, milliseconds
        self.last_spawn_time = pygame.time.get_ticks()

        self.max_spiders = 10
        self.display_surface = display_surface
        self.camera = Camera()

        self.ground_sprites = pygame.sprite.Group()

        # Built once here, not every frame. Drawn behind the real ground so
        # the area past the edge of the map still looks like forest.
        self.floor = build_floor_pattern()

        # This is for drawing the enemies
        self.enemy_pool = PoolingSystem()
        self.enemies_to_spawn = self.enemy_pool.get_activated_enemies()

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

        self.camera.update(player)

        # 0. Draw floor
        self.draw_floor()

        # 1. Draw ground tiles
        for sprite in self.ground_sprites:

            if self.is_visible(sprite):

                offset_rect = self.camera.apply(sprite)

                self.display_surface.blit(
                    sprite.image,
                    offset_rect
                )

        # 2. Combine regular sprites and active enemies
        all_sprites = list(self.sprites()) + self.enemies_to_spawn

        # 3. Cull and Y-sort everything together
        visible_sprites = [
            sprite for sprite in all_sprites
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
        
        self.lighting.draw(
            self.display_surface,
            player,
            self.camera
        )

    def get_camera(self):
        return self.camera
    
# ------------------------------------------------------------
    def spawn_enemy(self):

        current_time = pygame.time.get_ticks()

        # Check whether enough time has passed
        if current_time - self.last_spawn_time >= self.spawn_interval:

            # Check maximum active spider count
            if len(self.enemy_pool.activated) < self.max_spiders:

                spawn_position = self.get_random_spawn_position()

                self.enemy_pool.respawn_spider(spawn_position)

            self.last_spawn_time = current_time

    def get_random_spawn_position(self, margin=150):

        camera = self.camera_rect

        direction = random.choice([
            "top",
            "bottom",
            "left",
            "right"
        ])

        if direction == "top":

            x = random.randint(
                camera.left,
                camera.right
            )

            y = camera.top - margin

        elif direction == "bottom":

            x = random.randint(
                camera.left,
                camera.right
            )

            y = camera.bottom + margin

        elif direction == "left":

            x = camera.left - margin

            y = random.randint(
                camera.top,
                camera.bottom
            )

        else:

            x = camera.right + margin

            y = random.randint(
                camera.top,
                camera.bottom
            )

        return (x, y)
