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

    def fire(self, player_pos, facing):
        # Called when the player shoots. Detecting the mouse click belongs in
        # main.py's event loop. This method only makes the bullet.
        self.create_bullet(player_pos, facing)

    def create_bullet(self, player_pos, facing):
        # Copy the ant's position so the bullet starts at the ant. A copy means
        # the bullet moving later does not also move the ant.
        bullet_pos = player_pos.copy()

        # Start with no direction. The if/elif below fills it in from the way
        # the ant faces. In Pygame the y axis points DOWN, so up is -1.
        bullet_direction = pygame.Vector2(0, 0)

        if facing == "right_facing":
            bullet_direction.x = 1
            bullet_direction.y = 0
        elif facing == "left_facing":
            bullet_direction.x = -1
            bullet_direction.y = 0
        elif facing == "forward_facing":
            bullet_direction.x = 0
            bullet_direction.y = -1
        elif facing == "camera_facing":
            bullet_direction.x = 0
            bullet_direction.y = 1
        elif facing == "rightTop_facing":
            bullet_direction.x = 1
            bullet_direction.y = -1
        elif facing == "leftTop_facing":
            bullet_direction.x = -1
            bullet_direction.y = -1
        elif facing == "leftBottom_facing":
            bullet_direction.x = -1
            bullet_direction.y = 1
        elif facing == "rightBottom_facing":
            bullet_direction.x = 1
            bullet_direction.y = 1

        # If the facing name was not recognised the direction is still (0, 0).
        # A bullet with no direction would sit still forever, so make none.
        if bullet_direction.length_squared() == 0:
            return

        # A diagonal like (1, -1) is about 1.41 long, so it would travel faster
        # than a straight one. normalize() shrinks every direction to length 1.
        bullet_direction = bullet_direction.normalize()

        # Make the bullet and remember it so we can update and draw it later.
        bullet = Bullet(bullet_pos, bullet_direction, BULLET_SPEED)
        self.bullets.append(bullet)

    def update(self, dt):
        for bullet in self.bullets:
            bullet.update(dt)
        self.remove_old_bullets()