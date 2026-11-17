# Needs a full fitting

class Spider:
    def __init__(self, animator, pos):
        self.animator = animator
        self.pos = pos

        self.animation = animator.idle()

        self.frames = [pygame.image.load(path).convert_alpha() for path in self.animation]
        self.frame_index = 0
        # The time (in ms, from pygame.time.get_ticks()) we last switched frames.
        self.update_time = 0

        # Facing + movement state. We only swap animations when one of these
        # actually changes, so we don't reload frames from disk every frame.
        self.facing = "camera_facing"
        self.moving = False
        # True while the player is shooting. Like moving, this is part of the
        # state we compare, so the animation only swaps when it actually changes.
        self.shooting = False
        # When moving right we mirror the (left-facing) side art for now. Swap
        # this for real right-facing art when those frames are ready.
        self.flip_x = False

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

    def move(self, dt, keys):
        """ This is the important part to program for the spider AI logic.
            In Dylan's words, it should handle the correct facing direction
            for movement. This facing logic can also be found in set_animator methods.

            When moving in a direction, it should call the set_animation methods, and pass
            the facing parameter. This functionality can be observed in full in player_obj.py
        """

    def _reload_frames(self, paths):
        """Reload frames for a new animation without moving the player.

        self.pos is the source of truth for the player's position (kept as a
        float so small per-frame movement is not lost). The rect is just a
        rounded view of it, so we re-centre the rect on self.pos rather than
        snapping self.pos back to the rounded rect.
        """
        self.frames = [pygame.image.load(path).convert_alpha() for path in paths]
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