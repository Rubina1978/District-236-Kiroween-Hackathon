from GameScripts.world_builder import world_build

import pygame

pygame.init()

screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
pygame.display.set_caption("Point 236 (Kota 236)")
dt = 0


while running:
    # set time for running 60 sec
    clock.tick(60)
# poll for events
# pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# fill the screen with a color to wipe away anything from last frame
    screen.fill((35, 75, 45))

# flip() the display to put work on screen

    pygame.display.flip()
   
# call function to quit 
pygame.quit()