import pygame
import random
from settings import ENV_SPRITE_SCALES, ENV_DEFAULT_SCALE
from GameScripts.items import Items
from GameScripts.sprite_cache import load as load_sprite

# Enlarged pictures, made once per file and shared by every object that uses
# that file. The map has about 37,000 ground tiles but only 3 grass pictures,
# so this avoids making 37,000 copies (which froze the web version).
_scaled_images = {}


def _scaled_image(path, times):
    """The picture at `path`, made 2x bigger `times` times (once per file)."""
    key = (path, times)
    if key not in _scaled_images:
        image = load_sprite(path)
        for _ in range(times):
            image = pygame.transform.scale2x(image)
        _scaled_images[key] = image
    return _scaled_images[key]

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

        self.items = Items()

        # Load the PNG ONCE when the object is created, not every frame.
        # convert_alpha() keeps the transparent edges and makes blitting fast.
        if self.type == "box" and self.artwork != self.type:
            path = f"Assets/Artwork/Environment/Objects/Chest/sprite_chest1.png"
        elif self.type == "box":
            path = f"Assets/Artwork/Environment/Objects/Box/{self.type}_1.png"
        elif self.type == "grass1":
            path = f"Assets/Artwork/Tiles/{self.type}.png"
        elif self.type == "grass2":
            path = f"Assets/Artwork/Tiles/{self.type}.png"
        elif self.type == "grass3":
            path = f"Assets/Artwork/Tiles/{self.type}.png"
        else:
            path = f"Assets/Artwork/Environment/Scenery/{self.type}.png"

        # Double the size of every map sprite (trees, rocks, bushes, boxes).
        # scale2x is made for pixel art and makes the image exactly 2x bigger.
        # The player is loaded separately in player_obj.py, so it is unaffected.
        # Trees and rocks are doubled twice (4x bigger).
        times = 2 if self.type in ("tree", "rock") else 1
        self.image = _scaled_image(path, times)
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
        """Open the box, apply the reward, and return the reward string.

        Returns None if the box was already opened or is not a box.
        main.py uses the return value to trigger the reward popup.
        """
        # Prevent multiple loot rewards
        if self.opened:
            return None

        if self.type == "box" and self.artwork == self.type:

            self.items.box_opened(player)
            self.opened = True
            self.set_box_animation()
            return self.items.reward  # e.g. "ammo", "life", "health_potion"

        elif self.type == "box" and self.artwork != self.type:
            self.opened = True
            self.artwork = "Assets/Artwork/Environment/Objects/Chest/sprite_chest0.png"
            # Show the open chest (same 2x enlargement as the closed one).
            self.image = pygame.transform.scale2x(load_sprite(self.artwork))
            return "whiskey"

        return None

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
            pygame.transform.scale2x(load_sprite(path))
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
