from GameScripts.world_builder import world_build
from GameScripts.animator_controller import animator_interface
from GameScripts.Player.player_obj import Player
import pygame

pygame.init()

screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
pygame.display.set_caption("Point 236 (Kota 236)")
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

# Load Player & set position.
# Player loads all of its animation frames once when it is created.
player = Player(animator=animator_interface(type="player"))
player_sprite_rect = player.get_current_frame().get_rect()
player_sprite_rect.center = (player_pos.x, player_pos.y)

# -------------------------------------------------------------------------------------------
# Main game engine loop
# -------------------------------------------------------------------------------------------
while running:
    # set time for running 60 sec
    clock.tick(60)
# poll for events
# pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # KEYDOWN fires once the moment a key is pressed, not every frame while
        # it is held, so switching facing here happens once per press (no flag needed).
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player.set_animator_idle(facing="forward_facing")
            elif event.key == pygame.K_DOWN:
                player.set_animator_idle(facing="camera_facing")
            elif event.key == pygame.K_LEFT:
                player.set_animator_idle(facing="side_facing")

# fill the screen with a color to wipe away anything from last frame
    screen.fill((35, 75, 45))

# Advance the player's animation and draw the current frame.
    player.update_animation()
    screen.blit(player.get_current_frame(), player_sprite_rect)

# flip() the display to put work on screen

    pygame.display.flip()
   
# call function to quit 
pygame.quit()


# --------------------------------------------------------------------------------------------
