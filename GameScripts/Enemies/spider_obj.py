import pygame
# ImportError: attempted relative import beyond top-level package
# from ...settings import PLAYER_SPEED

PLAYER_SPEED = 240
ANIMATION_COOLDOWN = 100
class Spider(pygame.sprite.Sprite):
    def __init__(self, animator):
        super().__init__()

        self.is_dead = False
        self.animator = animator

        # Animation
        self.facing = "camera_facing"
        self.moving = False
        self.flip_x = False

        self.animation = animator.idle()

        self.frames = [
            pygame.image.load(path).convert_alpha()
            for path in self.animation
        ]

        self.frame_index = 0
        self.update_time = 0

        self.image = self._current_image()

        # Position
        self.pos = pygame.math.Vector2(0, 0)

        self.rect = self.image.get_rect()

    
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
        """Move to the next frame if enough time has passed since the last switch."""
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
            # If we've gone past the last frame, loop back to the first.
            if self.frame_index >= len(self.frames):
                self.frame_index = 0
            self.image = self._current_image()

#----------------------------------------------------------------------------------------
# IMPORTANT
#----------------------------------------------------------------------------------------
    def move(self, dt, player):
        """Move towards the player and select the appropriate directional animation."""
        # Calculate direction towards player
        direction = pygame.Vector2(
            player.pos.x - self.pos.x,
            player.pos.y - self.pos.y
        )

        # Distance to player
        distance = direction.length()

        # Stop when sufficiently close
        stopping_distance = 10

        if distance > stopping_distance:

            direction = direction.normalize()

            # Move towards player
            self.pos += direction * PLAYER_SPEED * dt

            # Sync rect with world position
            self.rect.center = (
                round(self.pos.x),
                round(self.pos.y)
            )

            new_moving = True

        else:
            new_moving = False

        # Determine facing direction.
        # Diagonals must be checked before cardinals.

        dx = direction.x if distance > stopping_distance else 0
        dy = direction.y if distance > stopping_distance else 0

        if dx == 0 and dy == 0:

            new_facing = self.facing

        elif dx < 0 and dy < 0:
            new_facing = "leftTop_facing"

        elif dx > 0 and dy < 0:
            new_facing = "rightTop_facing"

        elif dx < 0 and dy > 0:
            new_facing = "leftBottom_facing"

        elif dx > 0 and dy > 0:
            new_facing = "rightBottom_facing"

        elif dy < 0:
            new_facing = "forward_facing"

        elif dy > 0:
            new_facing = "camera_facing"

        elif dx < 0:
            new_facing = "left_facing"

        else:
            new_facing = "right_facing"

        new_flip = False

        # Only change animation when necessary

        if (new_moving, new_facing, new_flip) != (
            self.moving,
            self.facing,
            self.flip_x
        ):

            self.moving = new_moving
            self.facing = new_facing
            self.flip_x = new_flip

            if self.moving:
                self.set_animator_move(new_facing)

            else:
                self.set_animator_idle(new_facing)
#-----------------------------------------------------------------------------------------------
# IMPORTANT
#----------------------------------------------------------------------------------------

    def _reload_frames(self, paths):
        self.frames = [
            pygame.image.load(path).convert_alpha()
            for path in paths
        ]
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

        self.image = self._current_image()

        self.rect = self.image.get_rect(
            center=self.pos
        )

    def set_animator_idle(self, facing):
        """Switch to a different idle animation based on which way the ant faces."""

        if facing == "camera_facing":
            self.animation = self.animator.idle()
        elif facing == "forward_facing":
            self.animation = self.animator.idle()
        elif facing == "left_facing":
            self.animation = self.animator.idle()
        elif facing == "leftBottom_facing":
            self.animation = self.animator.idle()
        elif facing == "leftTop_facing":
            self.animation = self.animator.idle()
        elif facing == "right_facing":
            self.animation = self.animator.idlet()
        elif facing == "rightBottom_facing":
            self.animation = self.animator.idle()
        elif facing == "rightTop_facing":
            self.animation = self.animator.idle()
            
        self._reload_frames(self.animation)
    
    def set_animator_move(self, facing):
        """Switch to a different run animation based on which way the ant faces."""
        
        if facing == "camera_facing":
            self.animation = self.animator.move_camerafacing()
        elif facing == "forward_facing":
            self.animation = self.animator.move_forward()
        elif facing == "left_facing":
            self.animation = self.animator.move_left()
        elif facing == "leftBottom_facing":
            self.animation = self.animator.move_leftBottom()
        elif facing == "leftTop_facing":
            self.animation = self.animator.move_leftTop()
        elif facing == "right_facing":
            self.animation = self.animator.move_right()
        elif facing == "rightBottom_facing":
            self.animation = self.animator.move_rightBottom()
        elif facing == "rightTop_facing":
            self.animation = self.animator.move_rightTop()
        self._reload_frames(self.animation)
    
    def reset(self, position):
        """Reset the spider when it is retrieved from the object pool."""

        # Reset death state
        self.is_dead = False

        # Reset position
        self.pos = pygame.math.Vector2(position)

        # Reset movement state
        self.moving = False
        self.facing = "camera_facing"
        self.flip_x = False

        # Reset animation
        self.animation = self.animator.idle()
        self.frames = [
            pygame.image.load(path).convert_alpha()
            for path in self.animation
        ]

        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

        # Update image and rect
        self.image = self._current_image()

        self.rect = self.image.get_rect(
            center=self.pos
        )