import pygame

# Orange-yellow, and the bullet size in pixels.
BULLET_COLOR = (0, 0, 0)
BULLET_RADIUS = 2


class Bullet:
    def __init__(self, position, direction, speed):
        self.position = position.copy()
        self.direction = direction
        self.speed = speed
        self.start_position = position.copy()
        self.max_distance = 400

    def update(self, dt):
        self.position += self.direction * self.speed * dt

    def draw(self, screen, camera_offset):
        # self.position is a WORLD position (where the bullet is in the forest).
        # The screen only shows part of the world, so subtract how far the
        # camera has scrolled to get the position on the screen.
        screen_pos = self.position - camera_offset

        # draw.circle needs a centre and a radius. The centre must be whole
        # numbers (pixels), so round both values.
        center = (round(screen_pos.x), round(screen_pos.y))
        pygame.draw.circle(screen, BULLET_COLOR, center, BULLET_RADIUS)

    def distance_travelled(self):
        return self.position.distance_to(self.start_position)

    def is_too_far(self):
        # True once the bullet has flown past its maximum range.
        return self.distance_travelled() > self.max_distance
    
    def is_near(self, obj, distance=15):

        bullet_pos = self.position
        object_pos = pygame.Vector2(obj.rect.midbottom)

        return bullet_pos.distance_to(object_pos) <= distance
