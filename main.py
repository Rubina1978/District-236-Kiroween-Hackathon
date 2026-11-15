import pygame
from GameScripts.world_builder import world_build
from GameScripts.animator_controller import animator_interface
from GameScripts.Player.player_obj import Player
from GameScripts.Sprites.y_sort import YSortCameraGroup
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BG_COLOR

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True
pygame.display.set_caption("Point 236 (Kota 236)")

# Start the player in the middle of the screen.
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

# Load Player & set position.
# Player loads all of its animation frames once when it is created.
player = Player(animator=animator_interface(type="player"), pos=player_pos)

# Build the world (a grid of environment objects).
current_map = world_build()

# Camera group with y-sorting: the player and the environment are drawn together
# in one pass, sorted by Y position so lower sprites appear in front of higher ones.
camera_group = YSortCameraGroup(screen)
camera_group.add(player)
for sprite in current_map.get_sprites():
    camera_group.add(sprite)

# -------------------------------------------------------------------------------------------
# Main game engine loop
# -------------------------------------------------------------------------------------------
while running:
    # dt is delta time in seconds. Movement should use this so speed does not
    # depend on the frame rate.
    dt = clock.tick(FPS) / 1000

    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # KEYDOWN fires once the moment a key is pressed, not every frame while
        # it is held, so switching facing here happens once per press (no flag needed).
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player.set_animator_run(facing="forward_facing")
            elif event.key == pygame.K_DOWN:
                player.set_animator_run(facing="camera_facing")
            elif event.key == pygame.K_LEFT:
                player.set_animator_run(facing="side_facing")
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                player.set_animator_idle(facing="forward_facing")
            elif event.key == pygame.K_DOWN:
                player.set_animator_idle(facing="camera_facing")
            elif event.key == pygame.K_LEFT:
                player.set_animator_idle(facing="side_facing")

    # fill the screen with a colour to wipe away anything from last frame
    screen.fill(BG_COLOR)

    # Advance the player's animation, then draw every sprite (player + map)
    # in one y-sorted pass through the camera.
    player.update_animation()
    camera_group.custom_draw(player)

    # flip() the display to put work on screen
    pygame.display.flip()

# call function to quit
pygame.quit()

# --------------------------------------------------------------------------------------------
