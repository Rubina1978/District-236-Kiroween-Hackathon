import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, INVULNERABLE_MS
from .menu_style import (
    TEXT_COLOR, HEADING_COLOR,
    make_background, make_panel, render_text, Button, ButtonGroup,
)

TITLE_Y = 110
PANEL_TOP = 190
LINE_HEIGHT = 32
BUTTON_SIZE = (260, 56)
BUTTON_GAP = 30
BUTTON_Y = 620


class InfoScreen:
    """A simple screen: a big title, some lines of text, and one or two buttons.

    Help, Credits, Game Over and Victory are all this same class with different
    text, so there is only one layout to maintain.

    A line ending with ":" is drawn as a heading. An empty line is a gap.
    """

    def __init__(self, title, title_color, lines, buttons, align="left"):
        self.background = make_background()
        # The last gameplay frame (darkened), shown behind Game Over / Victory.
        self.backdrop = None

        title_font = pygame.font.Font(None, 96)
        heading_font = pygame.font.Font(None, 36)
        text_font = pygame.font.Font(None, 30)
        button_font = pygame.font.Font(None, 40)

        self.title = render_text(title_font, title, title_color)
        self.title_rect = self.title.get_rect(center=(SCREEN_WIDTH // 2, TITLE_Y))

        # Panel sized to fit the text.
        panel_width = 900
        panel_height = len(lines) * LINE_HEIGHT + 40
        self.panel_rect = pygame.Rect(0, PANEL_TOP, panel_width, panel_height)
        self.panel_rect.centerx = SCREEN_WIDTH // 2
        self.panel = make_panel(self.panel_rect.size)

        self.line_items = []
        for index, line in enumerate(lines):
            if not line:
                continue
            is_heading = line.endswith(":")
            font = heading_font if is_heading else text_font
            colour = HEADING_COLOR if is_heading else TEXT_COLOR
            picture = render_text(font, line, colour)
            y = self.panel_rect.top + 20 + index * LINE_HEIGHT
            if align == "center":
                rect = picture.get_rect(midtop=(self.panel_rect.centerx, y))
            else:
                rect = picture.get_rect(topleft=(self.panel_rect.left + 40, y))
            self.line_items.append((picture, rect))

        # Buttons in a row, centred on the screen.
        button_width, button_height = BUTTON_SIZE
        total_width = len(buttons) * button_width + (len(buttons) - 1) * BUTTON_GAP
        left = SCREEN_WIDTH // 2 - total_width // 2
        built = []
        for index, (label, action) in enumerate(buttons):
            rect = (left + index * (button_width + BUTTON_GAP), BUTTON_Y, button_width, button_height)
            built.append(Button(label, rect, action))
        self.buttons = ButtonGroup(built, button_font)

    def update(self, dt):
        """Nothing moves on these screens. main.py calls update() on every menu screen."""

    def set_backdrop(self, surface):
        """Keep a darkened copy of `surface` to draw behind this screen."""
        self.backdrop = surface.copy()
        shade = pygame.Surface(self.backdrop.get_size(), pygame.SRCALPHA)
        shade.fill((0, 0, 0, 170))
        self.backdrop.blit(shade, (0, 0))

    def handle_event(self, event):
        """Returns an action word ("menu" or "play") or None."""
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return "menu"
        return self.buttons.handle_event(event)

    def draw(self, screen):
        screen.blit(self.backdrop if self.backdrop else self.background, (0, 0))
        screen.blit(self.title, self.title_rect)
        screen.blit(self.panel, self.panel_rect)
        for picture, rect in self.line_items:
            screen.blit(picture, rect)
        self.buttons.draw(screen)


def make_help_screen():
    lines = [
        "Controls:",
        "WASD / Arrow Keys - Move the ant",
        "Left mouse click - Shoot toward the cursor",
        "Walk into a loot box to open it",
        "",
        "Good to know:",
        "Loot boxes can give ammo (+10) or an extra life (up to 5).",
        f"After a spider bites you, you are protected for {INVULNERABLE_MS / 1000:g} seconds.",
        "",
        "Objective:",
        "Avoid spiders, collect loot, and find the legendary JD bottle.",
    ]
    return InfoScreen("HELP", HEADING_COLOR, lines, [("Back", "menu")])


def make_credits_screen():
    # Edit these lines as the team adds names. Full asset credits are in Credits.md.
    lines = [
        "Music:",
        "Retro Ant Soldiers - Dylan Austin",
        "",
        "Loot box artwork:",
        "Dani Maccari (dani-maccari.itch.io)",
        "",
        "More credits:",
        "See Credits.md in the project folder.",
    ]
    return InfoScreen("CREDITS", HEADING_COLOR, lines, [("Back", "menu")])


def make_game_over_screen():
    lines = [
        "The spiders got you.",
        "The sacred bottle is still out there...",
    ]
    return InfoScreen(
        "GAME OVER", (210, 50, 40), lines,
        [("Try Again", "play"), ("Main Menu", "menu")], align="center",
    )


def make_victory_screen():
    lines = [
        "You found the legendary JD bottle!",
        "The colony is saved.",
    ]
    return InfoScreen(
        "VICTORY", (240, 190, 60), lines,
        [("Play Again", "play"), ("Main Menu", "menu")], align="center",
    )
