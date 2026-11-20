import pygame

# How long the full fade-in + hold + fade-out cycle takes (milliseconds).
FADE_IN_MS  = 400
HOLD_MS     = 1200
FADE_OUT_MS = 600
TOTAL_MS    = FADE_IN_MS + HOLD_MS + FADE_OUT_MS

# Where the popup sits: top-right corner with a small margin.
MARGIN = 20

# The reward icon is drawn at this size.
ICON_SIZE = 64

# The Amazon logo is drawn at this size, placed above the reward icon.
LOGO_SIZE = 140

# Map from the reward string (set in items.py) to the icon file.
REWARD_ICONS = {
    "ammo":          "Assets/Artwork/Icons/ShotgunShells.png",
    "life":          "Assets/Artwork/Icons/Heart.png",
    "health_potion": "Assets/Artwork/Icons/FirstAid.png",
    # "spider" and "empty" have no icon — no popup is shown for them.
}

AMAZON_LOGO_PATH = "Assets/Artwork/Icons/Amazon Halloween logo.png"


class RewardPopup:
    """Displays a small pop-up in the top-right corner when the player loots a box.

    The popup shows the Amazon Halloween logo above the reward icon.
    It fades in, holds for a moment, then fades out.

    Usage in main.py:
        popup = RewardPopup()                     # create once before the loop
        popup.show("ammo")                        # call when a box is opened
        popup.update(dt)                          # call every frame
        popup.draw(screen)                        # call every frame after update
    """

    def __init__(self):
        # Load images once at startup. scale() resizes them to the fixed sizes
        # defined above so the popup looks consistent regardless of source size.
        raw_logo = pygame.image.load(AMAZON_LOGO_PATH).convert_alpha()
        self._logo = pygame.transform.scale(raw_logo, (LOGO_SIZE, LOGO_SIZE))

        # Pre-load and scale every reward icon into a dict keyed by reward name.
        self._icons = {}
        for reward, path in REWARD_ICONS.items():
            raw = pygame.image.load(path).convert_alpha()
            self._icons[reward] = pygame.transform.scale(raw, (ICON_SIZE, ICON_SIZE))

        # Active state — None means no popup is currently showing.
        self._reward  = None
        self._elapsed = 0   # ms since show() was called

    # ------------------------------------------------------------------
    def show(self, reward):
        """Trigger a popup for the given reward string.

        If the reward has no icon (e.g. "spider", "empty") nothing is shown.
        Calling show() while a popup is already visible restarts it.
        """
        if reward not in self._icons:
            return
        self._reward  = reward
        self._elapsed = 0

    # ------------------------------------------------------------------
    def update(self, dt):
        """Advance the popup timer. dt is delta time in seconds (same as main loop)."""
        if self._reward is None:
            return

        self._elapsed += dt * 1000  # convert seconds → ms

        if self._elapsed >= TOTAL_MS:
            # Popup has fully finished — hide it.
            self._reward = None

    # ------------------------------------------------------------------
    def draw(self, screen):
        """Draw the popup onto screen. Call this every frame after update()."""
        if self._reward is None:
            return

        # Work out the current alpha (0 = invisible, 255 = fully opaque).
        alpha = self._calc_alpha()

        icon = self._icons[self._reward]
        logo = self._logo

        # --- position ---
        # The popup is two images stacked vertically: logo on top, icon below.
        # We anchor the whole block to the top-right corner.
        screen_w = screen.get_width()
        block_w  = max(LOGO_SIZE, ICON_SIZE)
        block_h  = LOGO_SIZE + 8 + ICON_SIZE   # 8 px gap between the two images

        x = screen_w - block_w - MARGIN
        y = MARGIN

        # --- blit with alpha ---
        # pygame Surfaces support per-surface alpha via set_alpha().
        # We copy the images so we can set alpha without affecting the originals.
        logo_copy = logo.copy()
        logo_copy.set_alpha(alpha)

        icon_copy = icon.copy()
        icon_copy.set_alpha(alpha)

        # Centre each image horizontally within the block.
        logo_x = x + (block_w - LOGO_SIZE) // 2
        icon_x = x + (block_w - ICON_SIZE) // 2

        screen.blit(logo_copy, (logo_x, y))
        screen.blit(icon_copy, (icon_x, y + LOGO_SIZE + 8))

    # ------------------------------------------------------------------
    def _calc_alpha(self):
        """Return an alpha value 0-255 based on where we are in the cycle."""
        t = self._elapsed

        if t < FADE_IN_MS:
            # Fade in: go from 0 to 255 over FADE_IN_MS milliseconds.
            return int(255 * t / FADE_IN_MS)

        elif t < FADE_IN_MS + HOLD_MS:
            # Hold: fully visible.
            return 255

        else:
            # Fade out: go from 255 to 0 over FADE_OUT_MS milliseconds.
            t_out = t - FADE_IN_MS - HOLD_MS
            return int(255 * (1 - t_out / FADE_OUT_MS))
