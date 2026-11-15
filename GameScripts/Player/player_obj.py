import pygame

# How long (in milliseconds) each animation frame stays on screen before
# switching to the next one. 100 ms = 10 animation frames per second.
ANIMATION_COOLDOWN = 100


class Player:
    def __init__(self, animator):
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

    def get_animation(self):
        return self.animation

    def get_current_frame(self):
        """Return the Surface for the frame we are currently on."""
        return self.frames[self.frame_index]

    def update_animation(self):
        """Move to the next frame if enough time has passed since the last switch."""
        # pygame.time.get_ticks() gives the number of ms since pygame.init().
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
            # If we've gone past the last frame, loop back to the first.
            if self.frame_index >= len(self.frames):
                self.frame_index = 0

    def set_animator_idle(self, facing):
        """Switch to a different idle animation based on which way the ant faces."""
        if facing == "camera_facing":
            self.animation = self.animator.idle_camerafacing()
        elif facing == "forward_facing":
            self.animation = self.animator.idle_forward()
        elif facing == "side_facing":
            self.animation = self.animator.idle_left()

        # Reload frames for the new animation and restart from the first frame.
        self.frames = [pygame.image.load(path).convert_alpha() for path in self.animation]
        self.frame_index = 0
        self.update_time = 0
