import pygame
import random
from settings import ENV_SPRITE_SCALES, ENV_DEFAULT_SCALE


class EnvrionmentObject(pygame.sprite.Sprite):
    """A piece of the environment (tree, rock, bush, box) drawn on the map.

    Now extends pygame.sprite.Sprite so it has the .image and .rect attributes
    that the camera and y-sort group rely on, and so it can be added to a
    sprite group alongside the player.
    """

    def __init__(self, type, artwork, x, y, animator):
        # Call the parent Sprite constructor first so this object works with
        # pygame sprite groups.
        super().__init__()
        self.type = type
        self.artwork = artwork
        self.is_boundary = False

        # for box animations
        self.animator = animator
        self.animation = None
        self.frames = []

        self.frame_index = 0
        self.update_time = 0

        self.animation_playing = False
        self.opened = False

        self.animation_cooldown = 200

        # Load the PNG ONCE when the object is created, not every frame.
        # convert_alpha() keeps the transparent edges and makes blitting fast.
        if self.type == "box":
            path = f"Assets/Artwork/Environment/Objects/Box/{self.type}_1.png"
        elif self.type == "grass1":
            path = f"Assets/Artwork/Tiles/{self.type}.png"
        elif self.type == "grass2":
            path = f"Assets/Artwork/Tiles/{self.type}.png"
        elif self.type == "grass3":
            path = f"Assets/Artwork/Tiles/{self.type}.png"
        else:
            path = f"Assets/Artwork/Environment/Scenery/{self.type}.png"

        self.image = pygame.image.load(path).convert_alpha()
        # Double the size of every map sprite (trees, rocks, bushes, boxes).
        # scale2x is made for pixel art and makes the image exactly 2x bigger.
        # The player is loaded separately in player_obj.py, so it is unaffected.
        if self.type == "tree":
            self.image = pygame.transform.scale2x(self.image)
            self.image = pygame.transform.scale2x(self.image)
        elif self.type == "grass1" or self.type == "grass2" or self.type == "grass3":
            self.image = pygame.transform.scale2x(self.image)
        else:
            self.image = pygame.transform.scale2x(self.image)
        # rect is where the sprite sits in the world. x, y come from its grid
        # cell (col * TILE_SIZE, row * TILE_SIZE).
        self.rect = self.image.get_rect(topleft=(x, y))

    def get_type(self):
        return self.type

    def get_artwork(self):
        return self.artwork
    
    def get_image(self):
        return self.image
    
    def get_type(self):
        return self.type

#---------------------------------------------------------------------------------------------
# if obj is a box

    def give_loot(self, player):

        # Prevent multiple loot rewards
        if self.opened:
            return

        if self.type == "box":

            player.ammo += 10

            self.opened = True
            self.set_box_animation()
    
    def get_animation(self):
        return self.animation

    def get_current_frame(self):
        """Return the Surface for the frame we are currently on."""
        return self.image

    def _current_image(self):
        """The current frame, mirrored horizontally if facing right."""
        img = self.frames[self.frame_index]
        if self.flip_x:
            img = pygame.transform.flip(img, True, False)
        return img

    def update_animation(self):

        if not self.animation_playing:
            return

        current_time = pygame.time.get_ticks()

        if current_time - self.update_time >= self.animation_cooldown:

            self.update_time = current_time

            if self.frame_index < len(self.frames) - 1:

                self.frame_index += 1
                self.image = self.frames[self.frame_index]

            else:

                # Animation finished
                self.animation_playing = False

    def set_box_animation(self):

        if self.type != "box":
            return

        # Get animation frames from your animator
        self.animation = self.animator.box_open

        self.frames = [
            pygame.transform.scale2x(
                pygame.image.load(path).convert_alpha()
            )
            for path in self.animation
        ]

        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

        self.image = self.frames[self.frame_index]

        self.animation_playing = True

#--------------------------------------------------------------------------------------------

    # if obj is boundary
    def set_boundary(self):
        self.is_boundary = True
    def get_boundary(self):
        return self.is_boundary
