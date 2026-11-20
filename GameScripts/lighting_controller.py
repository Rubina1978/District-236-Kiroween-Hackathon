import pygame
import math


class LightingController:

    def __init__(self, screen_width, screen_height):

        self.width = screen_width
        self.height = screen_height

        # Darkness settings
        self.darkness_alpha = 140

        # Light settings
        self.light_radius = 400

        # Create darkness overlay
        self.overlay = pygame.Surface(
            (self.width, self.height),
            pygame.SRCALPHA
        )

        # Create radial light mask
        self.light_mask = pygame.Surface(
            (self.light_radius * 2, self.light_radius * 2),
            pygame.SRCALPHA
        )

        self.create_light_mask()

    def create_light_mask(self):

        center = self.light_radius

        # Start completely transparent
        self.light_mask.fill((0, 0, 0, 0))

        for radius in range(self.light_radius, 0, -1):

            distance = radius / self.light_radius

            # Darkness increases towards the outer edge
            alpha = int(255)

            pygame.draw.circle(
                self.light_mask,
                (0, 0, 0, alpha),
                (center, center),
                radius
            )
            pygame.draw.circle(
                self.light_mask,
                (0, 0, 0, 0),
                (center, center),
                2
            )

    def draw(self, display_surface, player, camera):

        # Fill screen with darkness
        self.overlay.fill((20, 5, 30, self.darkness_alpha))

        # Find player's screen position
        player_screen = camera.apply(player)

        light_rect = self.light_mask.get_rect(
            center=player_screen.center
        )

        # Remove darkness around player
        self.overlay.blit(
            self.light_mask,
            light_rect,
            special_flags=pygame.BLEND_RGBA_SUB
        )

        # Apply darkness
        display_surface.blit(
            self.overlay,
            (0, 0)
        )