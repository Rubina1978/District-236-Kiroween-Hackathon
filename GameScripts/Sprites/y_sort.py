import pygame
from GameScripts.camera import Camera


class YSortCameraGroup(pygame.sprite.Group):
    """A sprite group that draws its sprites back-to-front by Y position.

    Sprites with a larger rect.bottom (lower on the screen) are drawn last,
    so they appear in front of sprites higher up. This gives the flat 2D art a
    sense of depth (the "2.5D" look).
    """

    def __init__(self, display_surface):
        # display_surface is the screen we draw everything onto.
        super().__init__()
        self.display_surface = display_surface
        self.camera = Camera()

    def custom_draw(self, player):
        # Keep the camera centred on the player.
        self.camera.update(player)

        # self.sprites() is built into pygame.sprite.Group; it returns every
        # sprite added to this group. Sort them by their bottom edge so that
        # things lower down draw on top.
        for sprite in sorted(self.sprites(), key=lambda s: s.rect.bottom):
            # Apply the camera scroll, then draw to the screen.
            offset_rect = self.camera.apply(sprite)
            self.display_surface.blit(sprite.image, offset_rect)
