import pygame

BULLET_COLOR = (0, 0, 0)
BULLET_RADIUS = 4

# The bullet's collision box. Small enough to feel fair.
BULLET_RECT_SIZE = 8


class Bullet:
    def __init__(self, position, direction, speed):
        self.position = position.copy()
        self.direction = direction
        self.speed = speed
        self.start_position = position.copy()
        self.max_distance = 400

        # rect is used for collision. It is a small square centred on the
        # bullet's world position and kept in sync every frame in update().
        # pygame.Rect needs integers, so we round the position.
        self.rect = pygame.Rect(0, 0, BULLET_RECT_SIZE, BULLET_RECT_SIZE)
        self.rect.center = (round(self.position.x), round(self.position.y))

    def update(self, dt):
        self.position += self.direction * self.speed * dt
        # Keep the rect in sync with the new position each frame.
        self.rect.center = (round(self.position.x), round(self.position.y))

    def draw(self, screen, camera_offset):
        # self.position is a world position. Subtract the camera offset to get
        # the position on screen.
        screen_pos = self.position - camera_offset
        center = (round(screen_pos.x), round(screen_pos.y))
        pygame.draw.circle(screen, BULLET_COLOR, center, BULLET_RADIUS)

    def distance_travelled(self):
        return self.position.distance_to(self.start_position)

    def is_too_far(self):
        return self.distance_travelled() > self.max_distance

    def hits(self, sprite):
        """True if this bullet's rect overlaps the sprite's rect.

        colliderect() is Pygame's built-in rectangle overlap check. It is
        pixel-perfect for axis-aligned boxes and much more reliable than a
        distance check, because it respects the actual shape of the spider's
        sprite rather than treating it as a single point.
        """
        return self.rect.colliderect(sprite.rect)
