import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

# Colours shared by every menu screen, so they all look like one set.
TEXT_COLOR = (235, 230, 215)
TITLE_COLOR = (240, 190, 60)
HEADING_COLOR = (240, 190, 60)
SHADOW_COLOR = (0, 0, 0)
BUTTON_COLOR = (40, 55, 35)
BUTTON_HOVER_COLOR = (90, 125, 55)
BUTTON_BORDER_COLOR = (200, 170, 80)
PANEL_COLOR = (0, 0, 0, 150)


def make_background():
    """A dark green vertical gradient, drawn once and reused every frame."""
    surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    top = (6, 10, 6)
    bottom = (34, 52, 26)
    for y in range(SCREEN_HEIGHT):
        t = y / (SCREEN_HEIGHT - 1)
        colour = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
        pygame.draw.line(surface, colour, (0, y), (SCREEN_WIDTH, y))
    return surface


def make_panel(size):
    """A see-through dark rectangle with a thin border, for text to sit on."""
    panel = pygame.Surface(size, pygame.SRCALPHA)
    panel.fill(PANEL_COLOR)
    pygame.draw.rect(panel, BUTTON_BORDER_COLOR, panel.get_rect(), width=2, border_radius=6)
    return panel


def render_text(font, text, color, shadow=True):
    """Turn text into a picture (Surface), with a dark shadow behind it.

    Rendering text is slowish, so screens call this once when they are created
    and then just blit the result every frame.
    """
    face = font.render(text, True, color)
    if not shadow:
        return face
    shade = font.render(text, True, SHADOW_COLOR)
    surface = pygame.Surface((face.get_width() + 2, face.get_height() + 2), pygame.SRCALPHA)
    surface.blit(shade, (2, 2))
    surface.blit(face, (0, 0))
    return surface


def wrap_text(text, font, max_width):
    """Split a long sentence into lines that each fit inside max_width pixels."""
    lines = []
    current = ""
    for word in text.split():
        attempt = f"{current} {word}".strip()
        if font.size(attempt)[0] <= max_width:
            current = attempt
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


class Button:
    """A labelled rectangle. `action` is the word handed back when it is chosen."""

    def __init__(self, label, rect, action):
        self.label = label
        self.rect = pygame.Rect(rect)
        self.action = action


class ButtonGroup:
    """A set of buttons that works with the mouse and the keyboard.

    handle_event() returns the action of the chosen button (for example
    "play"), or None if nothing was chosen. main.py decides what an action means.
    """

    def __init__(self, buttons, font):
        self.buttons = buttons
        self.selected = 0
        self.labels = [render_text(font, b.label, TEXT_COLOR) for b in buttons]

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            for index, button in enumerate(self.buttons):
                if button.rect.collidepoint(event.pos):
                    self.selected = index
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for button in self.buttons:
                if button.rect.collidepoint(event.pos):
                    return button.action
        elif event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w, pygame.K_LEFT, pygame.K_a):
                self.selected = (self.selected - 1) % len(self.buttons)
            elif event.key in (pygame.K_DOWN, pygame.K_s, pygame.K_RIGHT, pygame.K_d):
                self.selected = (self.selected + 1) % len(self.buttons)
            elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                return self.buttons[self.selected].action
        return None

    def draw(self, screen):
        for index, button in enumerate(self.buttons):
            colour = BUTTON_HOVER_COLOR if index == self.selected else BUTTON_COLOR
            pygame.draw.rect(screen, colour, button.rect, border_radius=8)
            pygame.draw.rect(screen, BUTTON_BORDER_COLOR, button.rect, width=2, border_radius=8)
            label = self.labels[index]
            screen.blit(label, label.get_rect(center=button.rect.center))
