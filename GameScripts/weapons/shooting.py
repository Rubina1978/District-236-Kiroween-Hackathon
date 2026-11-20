import pygame
from .bullet import Bullet

# How fast a bullet travels, in pixels per second.
BULLET_SPEED = 400

class Shooting:
    def __init__(self):
        self.bullets = []

    def remove_old_bullets(self):
        self.bullets = [
            bullet for bullet in self.bullets
            if not bullet.is_too_far()
        ]

    def fire(self, player_pos, direction):
        # Called when the player shoots. Detecting the mouse click belongs in
        # main.py's event loop. This method only makes the bullet.
        self.create_bullet(player_pos, direction)

    def create_bullet(self, player_pos, direction):
        # Copy the ant's position so the bullet starts at the ant. A copy means
        # the bullet moving later does not also move the ant.
        bullet_pos = player_pos.copy()

        # Make the bullet and remember it so we can update and draw it later.
        bullet = Bullet(bullet_pos, direction, BULLET_SPEED)
        self.bullets.append(bullet)

    def update(self, dt):
        for bullet in self.bullets:
            bullet.update(dt)
        self.remove_old_bullets()
