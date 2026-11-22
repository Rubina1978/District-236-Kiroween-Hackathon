import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, DAMAGE_FLASH_SECONDS

# Red, and how strong it is at the first moment (0 = invisible, 255 = solid).
FLASH_COLOR = (255, 0, 0)
FLASH_MAX_ALPHA = 120


class DamageFlash:
    """A red tint over the whole screen that fades out after the ant is bitten.

    Usage in main.py:
        flash = DamageFlash()      # create once before the loop
        flash.trigger()            # call when the ant is bitten
        flash.update(dt)           # call every frame
        flash.draw(screen)         # call every frame
    """

    def __init__(self):
        # SRCALPHA gives the surface a per-pixel transparency channel, so we
        # can draw a see-through red layer on top of the game.
        self.overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        self.time_left = 0.0

    def trigger(self):
        """Start (or restart) the flash."""
        self.time_left = DAMAGE_FLASH_SECONDS

    def update(self, dt):
        # Count down in seconds. max() stops it going below zero.
        if self.time_left > 0:
            self.time_left = max(0.0, self.time_left - dt)

    def draw(self, screen):
        if self.time_left <= 0:
            return
        # fade goes from 1 (just bitten) down to 0 (flash over).
        fade = self.time_left / DAMAGE_FLASH_SECONDS
        self.overlay.fill((*FLASH_COLOR, int(FLASH_MAX_ALPHA * fade)))
        screen.blit(self.overlay, (0, 0))
