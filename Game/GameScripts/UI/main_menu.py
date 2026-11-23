import pygame
from settings import (
    SCREEN_WIDTH, GAME_TITLE, MENU_STORY, MENU_TYPEWRITER_CPS, BOTTLE_NAME,
    MENU_ANT_IMAGE, MENU_SPIDER_IMAGE, MENU_ANT_SCALE, MENU_SPIDER_SCALE,
)
from GameScripts.animator_controller import animator_interface
from .menu_character import MenuCharacter
from .menu_style import (
    TEXT_COLOR, TITLE_COLOR, HEADING_COLOR,
    make_background, make_panel, render_text, wrap_text, Button, ButtonGroup,
)

# Layout of the title screen (pixels). These only position menu items.
TITLE_Y = 48
STORY_TOP = 98
STORY_WIDTH = 900
STORY_LINE_HEIGHT = 30
MIDDLE_CENTER_Y = 390          # the ant, the buttons and the spider line up here
ANT_CENTER_X = 210
SPIDER_CENTER_X = SCREEN_WIDTH - 210
BUTTON_SIZE = (260, 56)
BUTTON_GAP = 18
PANEL_RECT = pygame.Rect(140, 560, 1000, 140)

# After a key press the characters stay "excited" for this many seconds, so
# keyboard players see the reaction too (mouse players use the real hover).
KEY_REACTION_SECONDS = 0.8

# When the menu opens after a game, the characters wait this long (seconds)
# facing the camera before they turn, so the player sees the turn happen.
TURN_DELAY_SECONDS = 0.7


class MainMenu:
    """The title screen: story at the top, ant | buttons | spider, controls below."""

    def __init__(self):
        self.background = make_background()

        title_font = pygame.font.Font(None, 84)
        self.story_font = pygame.font.Font(None, 28)
        button_font = pygame.font.Font(None, 40)
        heading_font = pygame.font.Font(None, 30)
        text_font = pygame.font.Font(None, 26)

        # Text is turned into pictures once here, then only blitted each frame.
        self.title = render_text(title_font, GAME_TITLE, TITLE_COLOR)
        self.title_rect = self.title.get_rect(center=(SCREEN_WIDTH // 2, TITLE_Y))

        # The story types itself out one time. The wrapped lines are worked out
        # first, so the words do not jump to a new line while they appear.
        self.story_lines = wrap_text(MENU_STORY, self.story_font, STORY_WIDTH)
        self.story_full = [render_text(self.story_font, line, TEXT_COLOR) for line in self.story_lines]
        self.story_total = sum(len(line) for line in self.story_lines)
        self.chars_shown = 0.0
        self.typing_done = False

        # The two characters use the same animations as the game (the files are
        # only read, never changed). Facing the camera at first, then they turn.
        ant = animator_interface(type="player")
        spider = animator_interface(type="spider")
        self.ant = MenuCharacter(
            (ANT_CENTER_X, MIDDLE_CENTER_Y), MENU_ANT_SCALE, MENU_ANT_IMAGE,
            front_idle=ant.idle_camerafacing(), front_active=ant.run_camerafacing(),
            turned_idle=ant.idle_right(), turned_active=ant.run_right(),
        )
        self.spider = MenuCharacter(
            (SPIDER_CENTER_X, MIDDLE_CENTER_Y), MENU_SPIDER_SCALE, MENU_SPIDER_IMAGE,
            front_idle=spider.idle(), front_active=spider.move_camerafacing(),
            turned_idle=spider.move_left()[:1], turned_active=spider.move_left(),
        )
        self.key_reaction = 0.0

        # Four buttons stacked in the middle, centred vertically around MIDDLE_CENTER_Y.
        labels = [("Play", "play"), ("Help", "help"), ("Credits", "credits"), ("Quit", "quit")]
        button_width, button_height = BUTTON_SIZE
        total_height = len(labels) * button_height + (len(labels) - 1) * BUTTON_GAP
        top = MIDDLE_CENTER_Y - total_height // 2
        buttons = []
        for index, (label, action) in enumerate(labels):
            rect = (
                SCREEN_WIDTH // 2 - button_width // 2,
                top + index * (button_height + BUTTON_GAP),
                button_width,
                button_height,
            )
            buttons.append(Button(label, rect, action))
        self.buttons = ButtonGroup(buttons, button_font)

        # Instructions panel at the bottom.
        self.panel = make_panel(PANEL_RECT.size)
        self.instruction_items = []
        left_x = PANEL_RECT.left + 40
        right_x = PANEL_RECT.centerx + 20
        self._add_text(heading_font, "Controls:", HEADING_COLOR, left_x, PANEL_RECT.top + 14)
        controls = [
            "WASD / Arrow Keys - Move",
            "Left mouse click - Shoot",
            "Walk into loot boxes to open them",
        ]
        for index, line in enumerate(controls):
            self._add_text(text_font, line, TEXT_COLOR, left_x, PANEL_RECT.top + 46 + index * 28)
        self._add_text(heading_font, "Objective:", HEADING_COLOR, right_x, PANEL_RECT.top + 14)
        objective = f"Avoid spiders, collect loot, and find the legendary {BOTTLE_NAME}."
        for index, line in enumerate(wrap_text(objective, text_font, PANEL_RECT.right - 40 - right_x)):
            self._add_text(text_font, line, TEXT_COLOR, right_x, PANEL_RECT.top + 46 + index * 28)

    def _add_text(self, font, text, color, x, y):
        picture = render_text(font, text, color)
        self.instruction_items.append((picture, (x, y)))

    def _finish_typing(self):
        """Show the whole story, then let the two characters turn to each other."""
        self.typing_done = True
        self.chars_shown = self.story_total
        self.ant.start_turn()
        self.spider.start_turn()

    def replay_characters(self):
        """Ant and spider face the camera again, then turn toward each other.

        Called when the player comes back to this menu after a game. The story
        text stays as it is.
        """
        self.ant.reset()
        self.spider.reset()
        self.ant.start_turn(delay=TURN_DELAY_SECONDS)
        self.spider.start_turn(delay=TURN_DELAY_SECONDS)

    def handle_event(self, event):
        """Returns "play", "help", "credits", "quit" or None."""
        # A click or key press skips the typing. The same click still goes on
        # to the buttons below, so clicking Play straight away works.
        if not self.typing_done and event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
            self._finish_typing()
        if event.type == pygame.KEYDOWN:
            self.key_reaction = KEY_REACTION_SECONDS
        return self.buttons.handle_event(event)

    def update(self, dt):
        # A long first frame (while the menu loads) must not type the story at once.
        dt = min(dt, 0.05)

        if not self.typing_done:
            self.chars_shown += MENU_TYPEWRITER_CPS * dt
            if self.chars_shown >= self.story_total:
                self._finish_typing()

        self.key_reaction = max(0.0, self.key_reaction - dt)
        mouse_on_button = any(
            button.rect.collidepoint(pygame.mouse.get_pos()) for button in self.buttons.buttons
        )
        engaged = mouse_on_button or self.key_reaction > 0
        self.ant.update(dt, engaged)
        self.spider.update(dt, engaged)

    def _draw_story(self, screen):
        remaining = int(self.chars_shown)
        for index, full_line in enumerate(self.story_full):
            y = STORY_TOP + index * STORY_LINE_HEIGHT
            if self.typing_done:
                screen.blit(full_line, full_line.get_rect(center=(SCREEN_WIDTH // 2, y)))
                continue
            shown = min(len(self.story_lines[index]), remaining)
            remaining -= shown
            if shown <= 0:
                break
            # Draw the typed part starting where the finished line would start,
            # so the text grows to the right instead of sliding around.
            partial = render_text(self.story_font, self.story_lines[index][:shown], TEXT_COLOR)
            left = SCREEN_WIDTH // 2 - full_line.get_width() // 2
            screen.blit(partial, partial.get_rect(midleft=(left, y)))

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        screen.blit(self.title, self.title_rect)
        self._draw_story(screen)

        self.ant.draw(screen)
        self.spider.draw(screen)
        self.buttons.draw(screen)

        screen.blit(self.panel, PANEL_RECT)
        for picture, position in self.instruction_items:
            screen.blit(picture, position)
