import pygame
from settings import SPIDER_PERSONAL_SPACE, SPIDER_SPEED_MIN, SPIDER_SPEED_MAX
from GameScripts.sprite_cache import load as load_sprite
import random
import math
# ImportError: attempted relative import beyond top-level package
# from ...settings import PLAYER_SPEED

ANIMATION_COOLDOWN = 100
ATTACK_COOLDOWN = 100

# How long (ms) to wait after the death animation finishes before the spider
# is returned to the pool. Gives the last frame time to be visible.
DEATH_LINGER_MS = 500

class Spider(pygame.sprite.Sprite):
    def __init__(self, animator):
        super().__init__()

        self.is_dead = False
        self.dying = False          # True while the death animation is playing
        self.death_timer = 0        # ms timestamp set when dying starts
        self.animator = animator

        self.speed = random.randint(SPIDER_SPEED_MIN, SPIDER_SPEED_MAX)
        # Animation
        self.facing = "camera_facing"
        self.moving = False
        self.flip_x = False

        self.animation = animator.idle()

        self.frames = [
            load_sprite(path)
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
        """Advance the animation by one frame if enough time has passed.

        Normal animations loop. The death animation plays once and stops on
        the last frame. After it finishes we start a short linger timer; once
        that expires is_dead is set to True so the pool can recycle the spider.
        """
        now = pygame.time.get_ticks()

        # Linger: death animation has finished, wait a moment then mark dead.
        if self.dying and self.frame_index >= len(self.frames) - 1:
            if self.death_timer == 0:
                # First time we land on the last frame — start the timer.
                self.death_timer = now
            elif now - self.death_timer >= DEATH_LINGER_MS:
                self.is_dead = True
            return  # Don't advance past the last frame.

        if now - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = now
            self.frame_index += 1
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

        # After a bite the ant is protected for a while. During that time the
        # spiders keep their distance instead of piling onto the ant.
        protected = player.is_invulnerable()

        if protected and distance < SPIDER_PERSONAL_SPACE:
            # Too close to a protected ant: back away (still facing the ant).
            # A zero-length direction (exactly on the ant) cannot be
            # normalized, so use any direction in that case.
            away = -direction.normalize() if distance > 0 else pygame.Vector2(1, 0)
            self.pos += away * self.speed * dt
            self.rect.center = (
                round(self.pos.x),
                round(self.pos.y)
            )
            new_moving = True
        elif protected and distance < SPIDER_PERSONAL_SPACE + 20:
            # Far enough: wait here until the protection ends. The extra 20 px
            # stops the spider from jittering back and forth on the edge.
            new_moving = False
        elif distance > stopping_distance:

            direction = direction.normalize()

            # Move towards player
            self.pos += direction * self.speed * dt

            # Sync rect with world position
            self.rect.center = (
                round(self.pos.x),
                round(self.pos.y)
            )

            new_moving = True

        else:
            new_moving = False
            self.attack_player(player=player)

        # Determine facing direction
        dx = direction.x if distance > stopping_distance else 0
        dy = direction.y if distance > stopping_distance else 0

        if dx == 0 and dy == 0:
            new_facing = self.facing

        else:
            angle = math.degrees(math.atan2(dy, dx))

            if -22.5 <= angle < 22.5:
                new_facing = "right_facing"

            elif 22.5 <= angle < 67.5:
                new_facing = "rightBottom_facing"

            elif 67.5 <= angle < 112.5:
                new_facing = "camera_facing"

            elif 112.5 <= angle < 157.5:
                new_facing = "leftBottom_facing"

            elif angle >= 157.5 or angle < -157.5:
                new_facing = "left_facing"

            elif -157.5 <= angle < -112.5:
                new_facing = "leftTop_facing"

            elif -112.5 <= angle < -67.5:
                new_facing = "forward_facing"

            else:
                new_facing = "rightTop_facing"
        
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
    
    def attack_player(self, player):
        # The waiting time between hits lives in Player.take_life(), so it
        # works the same no matter how many spiders are touching the ant.
        if not player.lifeline.is_dead():
            # Pass our position so the ant is pushed away from this spider.
            player.take_life(self.pos)
#-----------------------------------------------------------------------------------------------
# IMPORTANT
#----------------------------------------------------------------------------------------

    def _reload_frames(self, paths):
        self.frames = [
            load_sprite(path)
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
            self.animation = self.animator.idle()
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
    
    def set_animator_death(self):
        self.animation = self.animator.death()
    
    def reset(self, position):
        """Reset the spider when it is retrieved from the object pool."""

        # Reset death state
        self.is_dead = False
        self.dying = False
        self.death_timer = 0

        # Reset position
        self.pos = pygame.math.Vector2(position)

        # Reset movement state
        self.moving = False
        self.facing = "camera_facing"
        self.flip_x = False

        # Reset animation
        self.animation = self.animator.idle()
        self.frames = [
            load_sprite(path)
            for path in self.animation
        ]

        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

        # Update image and rect
        self.image = self._current_image()

        self.rect = self.image.get_rect(
            center=self.pos
        )
    
    def kill_spider(self):
        """Switch to the death animation. is_dead is set later by update_animation()."""
        if self.dying:
            return  # already dying, don't restart
        self.dying = True
        self.death_timer = 0
        self._reload_frames(self.animator.death())