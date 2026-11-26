import math
import pygame
from settings import (
    PLAYER_SPEED, INVULNERABLE_MS, BLINK_MS,
    KNOCKBACK_DISTANCE, KNOCKBACK_SECONDS, PLAYER_SCALE,
)
from GameScripts.health import LifeLine
from GameScripts.sprite_cache import load as load_sprite

# Enlarged copies of the ant's pictures, kept by file path. The shared sprite
# cache is not changed, so other code that loads the same files is unaffected.
_scaled_frames = {}


def load_player_frame(path):
    """The ant's picture for `path`, enlarged by PLAYER_SCALE (done only once)."""
    if path not in _scaled_frames:
        image = load_sprite(path)
        size = (
            round(image.get_width() * PLAYER_SCALE),
            round(image.get_height() * PLAYER_SCALE),
        )
        if float(PLAYER_SCALE).is_integer():
            # Whole numbers (2, 3...): copy the pixels without blurring, so
            # pixel art stays crisp.
            _scaled_frames[path] = pygame.transform.scale(image, size)
        else:
            # In-between sizes (like 1.5): first enlarge to the next whole
            # number with crisp pixels, then shrink smoothly to the final size.
            # This keeps the pixels even instead of some 1 wide and some 2 wide.
            step = math.ceil(PLAYER_SCALE)
            crisp = pygame.transform.scale(
                image, (image.get_width() * step, image.get_height() * step)
            )
            _scaled_frames[path] = pygame.transform.smoothscale(crisp, size)
    return _scaled_frames[path]


# How long (in milliseconds) each animation frame stays on screen before
# switching to the next one. 100 ms = 10 animation frames per second.
ANIMATION_COOLDOWN = 100


class Player(pygame.sprite.Sprite):

    """The ant the player controls.

    Extends pygame.sprite.Sprite so it has .image and .rect and can be added
    to the same sprite group as the environment for y-sorting.
    """

    def __init__(self, animator, pos):
        # Call the parent Sprite constructor first.
        super().__init__()
        self.animator = animator
        self.ammo = 20
        # The current animation is a list of file paths to the PNG frames.
        self.animation = animator.idle_camerafacing()
        # Load every frame ONCE here, not every frame in the main loop.
        # pygame.image.load() returns a Surface; convert_alpha() keeps the
        # transparent edges and makes blitting fast.
        self.frames = [load_player_frame(path) for path in self.animation]
        self.frame_index = 0
        # The time (in ms, from pygame.time.get_ticks()) we last switched frames.
        self.update_time = 0
        self.lifeline = LifeLine()
        # Facing + movement state. We only swap animations when one of these
        # actually changes, so we don't reload frames from disk every frame.
        self.facing = "camera_facing"
        self.moving = False
        # True while the player is shooting.
        self.shooting = False
        # When moving right we mirror the (left-facing) side art for now.
        self.flip_x = False

        # Set by check_collision() when a box is freshly opened.
        # main.py reads this once per frame and clears it.
        self.last_reward = None
        # Facing chosen by aiming with the mouse. It overrides the walking
        # facing until aim_until (a time in ms from pygame.time.get_ticks()).
        self.aim_facing = None
        self.aim_until = 0
        # Time (ms) of the last hit taken. Starts far in the past so the very
        # first hit is never blocked by the cooldown.
        self.last_hit_time = -INVULNERABLE_MS
        # Set to True when the ant is bitten. main.py reads it once per frame
        # (to start the red flash) and sets it back to False.
        self.just_hit = False
        # Knockback: the direction of the push and how many seconds are left.
        self.knockback_dir = pygame.Vector2(0, 0)
        self.knockback_time_left = 0.0

        # A pygame sprite needs .image (the picture) and .rect (its position).
        # We keep a float position so small per-frame movement does not get
        # rounded away, then sync the rect to it.
        self.pos = pygame.Vector2(pos)
        self.image = self._current_image()
        self.rect = self.image.get_rect(center=self.pos)

        # True while the shooting animation is playing.
        self.shooting = False

        # Tracks whether the shooting animation has reached its final frame.
        self.shoot_finished = False

        # For scoring
        self.multiplier = 1

        # for end game
        self.can_trigger_extraction = False
        self.bottle_in_game = False

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
        """Advance animation frames, looping normal animations but not shooting."""

        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()

            if self.shooting:
                # If this is the final frame, finish the shooting animation.
                if self.frame_index >= len(self.frames) - 1:
                    self.shoot_finished = True
                    return

                self.frame_index += 1

            else:
                # Normal idle and running animations loop.
                self.frame_index += 1

                if self.frame_index >= len(self.frames):
                    self.frame_index = 0

            self.image = self._current_image()
    
    def start_shooting(self):
        """Start a fresh shooting animation."""

        self.shooting = True
        self.shoot_finished = False

        # Lock the facing direction to where the player aimed.
        self.facing = self.aim_facing
        self.flip_x = False

        self.set_animator_shoot(self.facing)

    def move(self, dt, keys, boundaries, boxes, alcohol):
        """Move the ant based on held keys and keep its facing/animation in sync.

        dt is delta time in seconds; multiplying speed by dt keeps the speed the
        same no matter the frame rate. keys is the list from pygame.key.get_pressed().
        """
        # Read direction from the arrow keys (WASD works too).
        dx = int(keys[pygame.K_RIGHT] or keys[pygame.K_d]) \
           - int(keys[pygame.K_LEFT] or keys[pygame.K_a])
        dy = int(keys[pygame.K_DOWN] or keys[pygame.K_s]) \
           - int(keys[pygame.K_UP] or keys[pygame.K_w])

        # Shooting: is the left mouse button held? pygame.mouse.get_pressed()
        # returns a tuple (left, middle, right) of booleans, so [0] is the left
        # button. keys only holds KEYBOARD state, so it cannot tell us about the
        # mouse - that is why keys[MOUSEBUTTONDOWN] never returned True here.
        shooting = self.shooting

        direction = pygame.Vector2(dx, dy)
        if direction.length_squared() > 0:
            direction = direction.normalize()

            # Move horizontally first
            old_x = self.pos.x
            self.pos.x += direction.x * PLAYER_SPEED * dt
            self.rect.centerx = round(self.pos.x)

            if self.check_collision(boundaries=boundaries, boxes=None, alcohol=None):
                self.pos.x = old_x
                self.rect.centerx = round(self.pos.x)

            # Then move vertically
            old_y = self.pos.y
            self.pos.y += direction.y * PLAYER_SPEED * dt
            self.rect.centery = round(self.pos.y)

            if self.check_collision(boundaries=boundaries, boxes=None, alcohol=None):
                self.pos.y = old_y
                self.rect.centery = round(self.pos.y)
            
            if self.check_collision(boundaries=None, boxes=boxes, alcohol=None):
                pass

            if self.check_collision(boundaries=None, boxes=None, alcohol=alcohol):
                self.pos.y = old_y
                self.rect.centery = round(self.pos.y)
                self.pos.x = old_x
                self.rect.centerx = round(self.pos.x)

            new_moving = True

        else:
            new_moving = False

        # Slide the ant away from the spider that bit it (does nothing when
        # there is no knockback running).
        self._apply_knockback(dt, boundaries)

        # Pick a facing from the movement direction.
        # Diagonals (both axes pressed) must be checked FIRST. An up-left press
        # also has dy < 0, so if we checked "forward" first the diagonal branch
        # would never be reached. With diagonals first, the cardinals below only
        # match when exactly one axis is pressed.
        if dx == 0 and dy == 0:
            # No keys held: keep the last facing so the idle pose still matches.
            new_facing, new_flip = self.facing, self.flip_x
        elif dx < 0 and dy < 0:
            new_facing, new_flip = "leftTop_facing", False
        elif dx > 0 and dy < 0:
            new_facing, new_flip = "rightTop_facing", False
        elif dx < 0 and dy > 0:
            new_facing, new_flip = "leftBottom_facing", False
        elif dx > 0 and dy > 0:
            new_facing, new_flip = "rightBottom_facing", False
        elif dy < 0:
            new_facing, new_flip = "forward_facing", False
        elif dy > 0:
            new_facing, new_flip = "camera_facing", False
        elif dx < 0:
            new_facing, new_flip = "left_facing", False
        else:  # dx > 0
            new_facing, new_flip = "right_facing", False

        # Just after a shot, face the aim direction instead of the walking one.
        if pygame.time.get_ticks() < self.aim_until:
            new_facing = self.aim_facing

        # Only swap animations when the shooting/moving/facing state actually
        # changes, otherwise we would reload the PNGs from disk every frame.
        # Shooting takes priority: while shooting you see the shoot pose even
        # if you are also moving; otherwise run while moving, else idle.
        # Shooting animation takes priority over walking and idle.
        if self.shooting:

            if not self.shoot_finished:
                self.moving = new_moving
                return

            # Shooting animation has finished.
            self.shooting = False
            self.shoot_finished = False

            # Force the transition back to the appropriate animation.
            self.moving = new_moving
            self.facing = new_facing
            self.flip_x = new_flip

            if new_moving:
                self.set_animator_run(new_facing)
            else:
                self.set_animator_idle(new_facing)

            return

        # Normal movement animation.
        if (new_moving, new_facing, new_flip) != (
            self.moving, self.facing, self.flip_x
        ):
            self.moving = new_moving
            self.facing = new_facing
            self.flip_x = new_flip

            if new_moving:
                self.set_animator_run(new_facing)
            else:
                self.set_animator_idle(new_facing)
        

    def _reload_frames(self, paths):
        """Reload frames for a new animation without moving the player.

        self.pos is the source of truth for the player's position (kept as a
        float so small per-frame movement is not lost). The rect is just a
        rounded view of it, so we re-centre the rect on self.pos rather than
        snapping self.pos back to the rounded rect.
        """
        self.frames = [load_player_frame(path) for path in paths]
        self.frame_index = 0
        self.update_time = 0
        self.image = self._current_image()
        # Recentre the rect on the existing position; do not move the player.
        self.rect = self.image.get_rect(center=self.pos)

    def set_animator_idle(self, facing):
        """Switch to a different idle animation based on which way the ant faces."""

        if facing == "camera_facing":
            self.animation = self.animator.idle_camerafacing()
        elif facing == "forward_facing":
            self.animation = self.animator.idle_forward()
        elif facing == "left_facing":
            self.animation = self.animator.idle_left()
        elif facing == "leftBottom_facing":
            self.animation = self.animator.idle_leftBottom()
        elif facing == "leftTop_facing":
            self.animation = self.animator.idle_leftTop()
        elif facing == "right_facing":
            self.animation = self.animator.idle_right()
        elif facing == "rightBottom_facing":
            self.animation = self.animator.idle_rightBottom()
        elif facing == "rightTop_facing":
            self.animation = self.animator.idle_rightTop()
            
        self._reload_frames(self.animation)

    def set_animator_run(self, facing):
        """Switch to a different run animation based on which way the ant faces."""
        
        if facing == "camera_facing":
            self.animation = self.animator.run_camerafacing()
        elif facing == "forward_facing":
            self.animation = self.animator.run_forward()
        elif facing == "left_facing":
            self.animation = self.animator.run_left()
        elif facing == "leftBottom_facing":
            self.animation = self.animator.run_leftBottom()
        elif facing == "leftTop_facing":
            self.animation = self.animator.run_leftTop()
        elif facing == "right_facing":
            self.animation = self.animator.run_right()
        elif facing == "rightBottom_facing":
            self.animation = self.animator.run_rightBottom()
        elif facing == "rightTop_facing":
            self.animation = self.animator.run_rightTop()
        self._reload_frames(self.animation)
    
    def set_animator_shoot(self, facing):
        """Switch to a different run animation based on which way the ant faces."""

        if facing == "camera_facing":
            self.animation = self.animator.shoot_camerafacing()
        elif facing == "forward_facing":
            self.animation = self.animator.shoot_forward()
        elif facing == "left_facing":
            self.animation = self.animator.shoot_left()
        elif facing == "leftBottom_facing":
            self.animation = self.animator.shoot_leftBottom()
        elif facing == "leftTop_facing":
            self.animation = self.animator.shoot_leftTop()
        elif facing == "right_facing":
            self.animation = self.animator.shoot_right()
        elif facing == "rightBottom_facing":
            self.animation = self.animator.shoot_rightBottom()
        elif facing == "rightTop_facing":
            self.animation = self.animator.shoot_rightTop()
        self._reload_frames(self.animation)

    def face_towards(self, direction):
        """Turn the ant toward an aim direction (a normalized Vector2)."""
    # A component smaller than 0.38 counts as "not that way". 0.38 is
    # sin(22.5 degrees), which splits the circle into 8 equal slices.
        dx = 0 if abs(direction.x) < 0.38 else (1 if direction.x > 0 else -1)
        dy = 0 if abs(direction.y) < 0.38 else (1 if direction.y > 0 else -1)

    # Same names as in move(). Diagonals first, then the 4 straight ones.
        if dx < 0 and dy < 0:
            self.aim_facing = "leftTop_facing"
        elif dx > 0 and dy < 0:
            self.aim_facing = "rightTop_facing"
        elif dx < 0 and dy > 0:
            self.aim_facing = "leftBottom_facing"
        elif dx > 0 and dy > 0:
            self.aim_facing = "rightBottom_facing"
        elif dy < 0:
            self.aim_facing = "forward_facing"
        elif dy > 0:
            self.aim_facing = "camera_facing"
        elif dx < 0:
            self.aim_facing = "left_facing"
        else:
            self.aim_facing = "right_facing"

        # The aim facing wins over the walking facing until this time (ms).
        self.aim_until = pygame.time.get_ticks() + 300

    def is_near(self, obj, distance=1):

        player_pos = pygame.Vector2(self.rect.center)
        object_pos = pygame.Vector2(obj.rect.midbottom)

        return player_pos.distance_to(object_pos) <= distance
    
    def check_collision(self, boundaries, boxes, alcohol):

        if boxes != None:
            for box in boxes:

                if self.rect.colliderect(box.rect):

                    reward = box.give_loot(self)
                    # reward is a string like "ammo" if the box was just opened,
                    # or None if it was already open. Store it so main.py can
                    # trigger the reward popup.
                    if reward:
                        self.last_reward = reward
                    return True

        if boundaries != None:
            for boundary in boundaries:

                if self.rect.colliderect(boundary.rect):
                    return True
        
        if alcohol != None and self.bottle_in_game == True and self.can_trigger_extraction == False:
            if self.rect.colliderect(alcohol.rect):
                self.can_trigger_extraction = True

        return False

# ---------------------------
    def is_invulnerable(self):
        """True while the ant is still protected after a bite."""
        return pygame.time.get_ticks() - self.last_hit_time < INVULNERABLE_MS

    def is_blink_hidden(self):
        """True on the 'off' beats of the blink, so the ant is not drawn.

        While protected, time since the hit is cut into slices of BLINK_MS.
        Even slices (0, 2, 4...) hide the ant, odd slices show it.
        """
        if not self.is_invulnerable():
            return False
        slice_number = (pygame.time.get_ticks() - self.last_hit_time) // BLINK_MS
        return slice_number % 2 == 0

    def take_life(self, attacker_pos=None):
        # While protected, bites from any spider are ignored, so spiders
        # standing on the ant cannot take every life in a fraction of a second.
        if self.is_invulnerable():
            return
        self.last_hit_time = pygame.time.get_ticks()
        self.just_hit = True
        self.lifeline.lose()

        # Push the ant away from the spider that bit it.
        if attacker_pos is not None:
            away = self.pos - pygame.Vector2(attacker_pos)
            if away.length_squared() == 0:
                # Exactly on top of each other: pick any direction.
                away = pygame.Vector2(0, 1)
            self.knockback_dir = away.normalize()
            self.knockback_time_left = KNOCKBACK_SECONDS

    def _apply_knockback(self, dt, boundaries):
        """Move the ant along the knockback direction for this frame.

        Same idea as move(): try x, then y, and undo a step that would put
        the ant inside a boundary, so the push never goes through walls.
        """
        if self.knockback_time_left <= 0:
            return

        # Never use more time than is left, so the push ends at exactly
        # KNOCKBACK_DISTANCE pixels.
        step_time = min(dt, self.knockback_time_left)
        self.knockback_time_left -= step_time
        speed = KNOCKBACK_DISTANCE / KNOCKBACK_SECONDS
        step = self.knockback_dir * speed * step_time

        old_x = self.pos.x
        self.pos.x += step.x
        self.rect.centerx = round(self.pos.x)
        if self.check_collision(boundaries=boundaries, boxes=None, alcohol=None):
            self.pos.x = old_x
            self.rect.centerx = round(self.pos.x)

        old_y = self.pos.y
        self.pos.y += step.y
        self.rect.centery = round(self.pos.y)
        if self.check_collision(boundaries=boundaries, boxes=None, alcohol=None):
            self.pos.y = old_y
            self.rect.centery = round(self.pos.y)

    def kill_player(self):
        is_dead = True