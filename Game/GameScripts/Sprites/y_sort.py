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
        self.spawn_interval = 2000  # 3 seconds, milliseconds
        self.last_spawn_time = pygame.time.get_ticks()

        self.max_spiders = 10
        self.display_surface = display_surface
        self.camera = Camera()

        self.ground_sprites = pygame.sprite.Group()
        self.chunk_size = 16
        self.ground_chunks = {}

        self.ground_grid_rows = 0
        self.ground_grid_cols = 0

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
    
    def add_ground_grid(self, grid):

        self.ground_grid_rows = len(grid)
        self.ground_grid_cols = len(grid[0])

        for row_index, row in enumerate(grid):

            for col_index, sprite in enumerate(row):

                if sprite == 0:
                    continue

                chunk_row = row_index // self.chunk_size
                chunk_col = col_index // self.chunk_size

                chunk_key = (chunk_row, chunk_col)

                if chunk_key not in self.ground_chunks:
                    self.ground_chunks[chunk_key] = []

                self.ground_chunks[chunk_key].append(sprite)

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
        self.camera_rect.topleft = (
            int(self.camera.offset.x),
            int(self.camera.offset.y)
        )

        visible_area = self.camera_rect.inflate(
            self.culling_margin * 2,
            self.culling_margin * 2
        )

        # Calculate the visible world area ONCE per frame
        self.camera_rect.topleft = (
            int(self.camera.offset.x),
            int(self.camera.offset.y)
        )

        visible_area = self.camera_rect.inflate(
            self.culling_margin * 2,
            self.culling_margin * 2
        )

        # 0. Draw floor
        self.draw_floor()

        # 1. Draw ground tiles
        # --------------------------------------------------
        # Draw only ground tiles in nearby chunks

        # Convert the four corners of the visible world area
        # from pixel coordinates into isometric grid coordinates.

        corners = [
            (visible_area.left, visible_area.top),
            (visible_area.right, visible_area.top),
            (visible_area.left, visible_area.bottom),
            (visible_area.right, visible_area.bottom)
        ]

        grid_positions = []

        for x, y in corners:

            row = (y / 30) - (x / 60)
            col = (x / 60) + (y / 30)

            grid_positions.append((row, col))


        # Find the grid area covered by the camera.
        # Four extra cells provide a safety margin for tile artwork.

        min_row = int(min(p[0] for p in grid_positions)) - 4
        max_row = int(max(p[0] for p in grid_positions)) + 4

        min_col = int(min(p[1] for p in grid_positions)) - 4
        max_col = int(max(p[1] for p in grid_positions)) + 4


        # Convert grid coordinates into chunk coordinates.

        min_chunk_row = max(0, min_row // self.chunk_size)
        max_chunk_row = min(
            (self.ground_grid_rows - 1) // self.chunk_size,
            max_row // self.chunk_size
        )

        min_chunk_col = max(0, min_col // self.chunk_size)
        max_chunk_col = min(
            (self.ground_grid_cols - 1) // self.chunk_size,
            max_col // self.chunk_size
        )


        # Draw tiles from nearby chunks only.

        for chunk_row in range(min_chunk_row, max_chunk_row + 1):

            for chunk_col in range(min_chunk_col, max_chunk_col + 1):

                chunk_key = (chunk_row, chunk_col)

                for sprite in self.ground_chunks.get(chunk_key, []):

                    if sprite.rect.colliderect(visible_area):

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
            if sprite.rect.colliderect(visible_area)
        ]

        for sprite in sorted(
            visible_sprites,
            key=lambda s: s.rect.bottom
        ):
            # Blink: skip drawing the ant on the "off" beats while it is
            # protected after a bite.
            if sprite is player and player.is_blink_hidden():
                continue

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
