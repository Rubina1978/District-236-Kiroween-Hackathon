import pygame
from settings import PLAYER_SPEED
from GameScripts.health import LifeLine
from GameScripts.sprite_cache import load as load_sprite

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
        self.frames = [load_sprite(path) for path in self.animation]
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

        # A pygame sprite needs .image (the picture) and .rect (its position).
        # We keep a float position so small per-frame movement does not get
        # rounded away, then sync the rect to it.
        self.pos = pygame.Vector2(pos)
        self.image = self._current_image()
        self.rect = self.image.get_rect(center=self.pos)

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

    def move(self, dt, keys, boundaries, boxes):
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
        shooting = pygame.mouse.get_pressed()[0]

        direction = pygame.Vector2(dx, dy)
        if direction.length_squared() > 0:
            direction = direction.normalize()

            # Move horizontally first
            old_x = self.pos.x
            self.pos.x += direction.x * PLAYER_SPEED * dt
            self.rect.centerx = round(self.pos.x)

            if self.check_collision(boundaries=boundaries, boxes=None):
                self.pos.x = old_x
                self.rect.centerx = round(self.pos.x)

            # Then move vertically
            old_y = self.pos.y
            self.pos.y += direction.y * PLAYER_SPEED * dt
            self.rect.centery = round(self.pos.y)

            if self.check_collision(boundaries=boundaries, boxes=None):
                self.pos.y = old_y
                self.rect.centery = round(self.pos.y)
            
            if self.check_collision(boundaries=None, boxes=boxes):
                pass

            new_moving = True

        else:
            new_moving = False

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
        if (shooting, new_moving, new_facing, new_flip) != (self.shooting, self.moving, self.facing, self.flip_x):
            self.shooting = shooting
            self.moving = new_moving
            self.facing = new_facing
            self.flip_x = new_flip
            if shooting:
                self.set_animator_shoot(new_facing)
            elif new_moving:
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
        self.frames = [load_sprite(path) for path in paths]
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
    
    def check_collision(self, boundaries, boxes):

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

        return False

# ---------------------------
    def take_life(self):
        self.lifeline.lose()
        print(f"Lost a life! You have {self.lifeline.lives} lives remaining!")
    def kill_player(self):
        is_dead = True