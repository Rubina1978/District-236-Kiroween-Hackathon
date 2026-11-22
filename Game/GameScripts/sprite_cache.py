# sprite_cache.py
# A single shared dictionary that holds every loaded sprite Surface.
# Any module that needs to load a PNG should use load() from here instead of
# calling pygame.image.load() directly.
#
# How it works:
#   - The first time a path is requested, we load it from disk and store it.
#   - Every time after that, we return the Surface we already have in memory.
#   - This means no PNG is ever read from disk more than once per session.

import pygame

_cache: dict[str, pygame.Surface] = {}


def load(path: str) -> pygame.Surface:
    """Return the Surface for *path*, loading it from disk only on the first call."""
    if path not in _cache:
        _cache[path] = pygame.image.load(path).convert_alpha()
    return _cache[path]


def clear():
    """Empty the cache. Only needed if you want to free memory at a level boundary."""
    _cache.clear()
