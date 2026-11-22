import math
import os
import pygame
from settings import MENU_ART_BOX

# Menu-only animation numbers.
FRAME_SECONDS = 0.1     # how long each animation frame is shown
TURN_SECONDS = 0.25     # how long the turn (squeeze and swap) takes
BOB_PIXELS = 6          # up/down bounce, only used for a custom menu picture


def _load_frames(paths):
    # A NEW surface for each file. The menu only resizes copies, so the
    # gameplay sprites are never changed.
    return [pygame.image.load(path).convert_alpha() for path in paths]


class MenuCharacter:
    """The ant or the spider on the title screen.

    It has two choices at any moment:
      * facing: toward the camera (start) or turned toward the other character
      * mode:   idle (calm) or active (legs moving, when the mouse is on a button)

    Each of the four combinations has its own list of animation frames.
    If a custom menu picture exists (menu_ant.png / menu_spider.png), that
    single picture is used instead: it bounces when active and is mirrored
    when turned.
    """

    def __init__(self, center, scale, image_path,
                 front_idle, front_active, turned_idle, turned_active):
        self.center_x, center_y = center
        self.custom_picture = os.path.exists(image_path)

        if self.custom_picture:
            picture = pygame.image.load(image_path).convert_alpha()
            fit = self._fit(picture, scale)
            size = self._scaled_size(picture, fit)
            front = pygame.transform.smoothscale(picture, size)
            turned = pygame.transform.flip(front, True, False)
            self.sets = {
                "front_idle": [front], "front_active": [front],
                "turned_idle": [turned], "turned_active": [turned],
            }
            reference = front
        else:
            raw = {
                "front_idle": _load_frames(front_idle),
                "front_active": _load_frames(front_active),
                "turned_idle": _load_frames(turned_idle),
                "turned_active": _load_frames(turned_active),
            }
            # One zoom for every frame (worked out from the first one) so the
            # character keeps the same pixel size when its animation changes.
            fit = self._fit(raw["front_idle"][0], scale)
            self.sets = {
                name: [
                    pygame.transform.scale(frame, self._scaled_size(frame, fit))
                    for frame in frames
                ]
                for name, frames in raw.items()
            }
            reference = self.sets["front_idle"][0]

        # Feet stay on one line, so frames of different heights do not jump.
        self.bottom = center_y + reference.get_height() // 2

        self.time = 0.0          # drives the animation frames and the bounce
        self.turned = False      # True once the turn has finished
        self.turning = False
        self.turn_waiting = False   # True while waiting for the turn delay to run out
        self.turn_delay = 0.0
        self.turn_progress = 0.0
        self.engaged = False     # True while the mouse is on a button

    @staticmethod
    def _fit(image, scale):
        box_width, box_height = MENU_ART_BOX
        return min(box_width / image.get_width(), box_height / image.get_height()) * scale

    @staticmethod
    def _scaled_size(image, fit):
        return (max(1, round(image.get_width() * fit)), max(1, round(image.get_height() * fit)))

    def start_turn(self, delay=0.0):
        """Turn toward the other character, after `delay` seconds.

        Does nothing if already turned or already turning.
        """
        if not self.turned and not self.turning:
            self.turn_delay = delay
            self.turn_waiting = True

    def reset(self):
        """Face the camera again, calm and idle, ready to turn once more."""
        self.turned = False
        self.turning = False
        self.turn_waiting = False
        self.turn_progress = 0.0

    def update(self, dt, engaged):
        self.time += dt
        self.engaged = engaged

        # Wait out the delay, then begin the turn.
        if self.turn_waiting:
            self.turn_delay -= dt
            if self.turn_delay <= 0:
                self.turn_waiting = False
                self.turning = True
                self.turn_progress = 0.0

        if self.turning:
            self.turn_progress += dt / TURN_SECONDS
            if self.turn_progress >= 1.0:
                self.turning = False
                self.turned = True

    def _current_frame(self):
        # Halfway through the turn the picture switches to the turned frames.
        showing_turned = self.turned or (self.turning and self.turn_progress >= 0.5)
        name = ("turned_" if showing_turned else "front_") + ("active" if self.engaged else "idle")
        frames = self.sets[name]
        return frames[int(self.time / FRAME_SECONDS) % len(frames)]

    def draw(self, screen):
        frame = self._current_frame()

        # During the turn the picture squeezes to a thin line and opens again.
        if self.turning:
            squeeze = abs(1.0 - 2.0 * self.turn_progress)
            width = max(1, int(frame.get_width() * squeeze))
            frame = pygame.transform.scale(frame, (width, frame.get_height()))

        bob = 0
        if self.custom_picture and self.engaged:
            bob = -abs(math.sin(self.time * 10)) * BOB_PIXELS
        screen.blit(frame, frame.get_rect(midbottom=(self.center_x, self.bottom + bob)))
