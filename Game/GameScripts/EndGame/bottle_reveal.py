import math
import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, BOTTLE_IMAGE, BOTTLE_REVEAL_SECONDS
from GameScripts.sprite_cache import load as load_sprite

# Numbers that only shape this animation.
RISE_SECONDS = 1.0      # how long the bottle takes to pop up out of the chest
RISE_PIXELS = 80        # how far up it floats
START_INSIDE = 45       # pixels below the chest's top edge where it starts
BOB_PIXELS = 5          # gentle up-and-down float after it has risen
FLASH_SECONDS = 0.5     # the golden flash at the moment the chest opens
GLOW_RADIUS = 90
GLOW_COLOR = (255, 210, 80)
FLASH_MAX_ALPHA = 150


def _make_glow():
    """A soft golden circle: big faint rings first, then smaller stronger ones."""
    size = GLOW_RADIUS * 2
    glow = pygame.Surface((size, size), pygame.SRCALPHA)
    for radius in range(GLOW_RADIUS, 0, -3):
        alpha = int(110 * (1 - radius / GLOW_RADIUS) ** 1.5)
        pygame.draw.circle(glow, (*GLOW_COLOR, alpha), (GLOW_RADIUS, GLOW_RADIUS), radius)
    return glow


class BottleReveal:
    """The ending: the chest opens and the bottle floats up out of it.

    Time here is real time (milliseconds from pygame.time.get_ticks()), so the
    moment lasts BOTTLE_REVEAL_SECONDS on the clock, whatever the game speed.

    Usage in main.py:
        reveal = BottleReveal()        # once, after the window exists
        reveal.start(chest.rect)       # when the chest is opened
        reveal.update()                # every frame
        reveal.draw(screen, offset)    # every frame, after the world is drawn
        if reveal.finished: ...        # time to show the Victory screen
        reveal.reset()                 # when a new game starts
    """

    def __init__(self):
        self.image = load_sprite(BOTTLE_IMAGE)
        self.glow = _make_glow()
        self.flash = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        self.reset()

    def reset(self):
        self.active = False      # True from the chest opening onwards
        self.finished = False
        self.chest_rect = None
        self.start_ticks = 0

    def start(self, chest_rect):
        self.active = True
        self.finished = False
        self.chest_rect = chest_rect
        self.start_ticks = pygame.time.get_ticks()

    def _elapsed(self):
        return (pygame.time.get_ticks() - self.start_ticks) / 1000

    def update(self):
        if self.active and not self.finished and self._elapsed() >= BOTTLE_REVEAL_SECONDS:
            self.finished = True

    def draw(self, screen, camera_offset):
        if not self.active:
            return
        t = self._elapsed()

        # Rise fast at first, then slow down (ease out), then float gently.
        progress = min(t / RISE_SECONDS, 1.0)
        rise = RISE_PIXELS * (1 - (1 - progress) ** 2)
        bob = math.sin((t - RISE_SECONDS) * 4) * BOB_PIXELS if t > RISE_SECONDS else 0

        # World position of the bottle's bottom edge, then convert to the screen.
        world_x = self.chest_rect.centerx
        world_bottom = self.chest_rect.top + START_INSIDE - rise + bob
        screen_x = world_x - camera_offset.x
        screen_bottom = world_bottom - camera_offset.y

        # Golden glow behind the bottle, then the bottle itself.
        glow_center = (screen_x, screen_bottom - self.image.get_height() * 0.4)
        screen.blit(self.glow, self.glow.get_rect(center=glow_center))
        screen.blit(self.image, self.image.get_rect(midbottom=(screen_x, screen_bottom)))

        # A quick golden flash over the whole screen when the chest opens.
        if t < FLASH_SECONDS:
            alpha = int(FLASH_MAX_ALPHA * (1 - t / FLASH_SECONDS))
            self.flash.fill((*GLOW_COLOR, alpha))
            screen.blit(self.flash, (0, 0))
