from enum import Enum, auto


class GameState(Enum):
    """Every screen the game can be showing.

    An Enum is a fixed list of names. It stops typos: GameState.PLAYNG is an
    error straight away, while the text "playng" would silently do nothing.
    """
    MAIN_MENU = auto()
    PLAYING = auto()
    HELP = auto()
    CREDITS = auto()
    GAME_OVER = auto()
    VICTORY = auto()


class GameStateManager:
    """Remembers which screen is active. main.py asks it what to run.

    It only holds the current state. What each state does lives elsewhere
    (the menu screens in GameScripts/UI, the gameplay in main.py).
    """

    def __init__(self, start_state=GameState.MAIN_MENU):
        self.current = start_state
        self.previous = None

    def change_to(self, new_state):
        """Switch to another screen."""
        self.previous = self.current
        self.current = new_state

    def is_state(self, state):
        return self.current == state
