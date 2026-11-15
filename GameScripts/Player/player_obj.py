import pygame

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
        # The current animation is a list of file paths to the PNG frames.
        self.animation = animator.idle_camerafacing()
        # Load every frame ONCE here, not every frame in the main loop.
        # pygame.image.load() returns a Surface (a grid of pixels we can draw).
        # convert_alpha() keeps the transparent edges and makes blitting fast.
        self.frames = [pygame.image.load(path).convert_alpha() for path in self.animation]
        # Which frame we are currently showing (an index into self.frames).
        self.frame_index = 0
        # The time (in ms, from pygame.time.get_ticks()) we last switched frames.
        self.update_time = 0

        # A pygame sprite needs .image (the picture) and .rect (its position).
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=pos)

    def get_animation(self):
        return self.animation

    def get_current_frame(self):
        """Return the Surface for the frame we are currently on."""
        return self.image

    def update_animation(self):
        """Move to the next frame if enough time has passed since the last switch."""
        # pygame.time.get_ticks() gives the number of ms since pygame.init().
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
            # If we've gone past the last frame, loop back to the first.
            if self.frame_index >= len(self.frames):
                self.frame_index = 0
            # Keep .image in sync with the new frame index.
            self.image = self.frames[self.frame_index]

    def _reload_frames(self, paths):
        """Reload frames for a new animation without moving the player."""
        # Remember where the player is so switching animations (which may have a
        # different frame size) doesn't make it jump to a new spot.
        center = self.rect.center
        self.frames = [pygame.image.load(path).convert_alpha() for path in paths]
        self.frame_index = 0
        self.update_time = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=center)

    def set_animator_idle(self, facing):
        """Switch to a different idle animation based on which way the ant faces."""
        if facing == "camera_facing":
            self.animation = self.animator.idle_camerafacing()
        elif facing == "forward_facing":
            self.animation = self.animator.idle_forward()
        elif facing == "side_facing":
            self.animation = self.animator.idle_left()
        self._reload_frames(self.animation)

    def set_animator_run(self, facing):
        """Switch to a different run animation based on which way the ant faces."""
        if facing == "camera_facing":
            self.animation = self.animator.run_camerafacing()
        elif facing == "forward_facing":
            self.animation = self.animator.run_forward()
        elif facing == "side_facing":
            self.animation = self.animator.run_left()
        self._reload_frames(self.animation)
