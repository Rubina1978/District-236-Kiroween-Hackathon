import pygame
from GameScripts.world_builder import world_build
from GameScripts.animator_controller import animator_interface
from GameScripts.Player.player_obj import Player
from GameScripts.Sprites.y_sort import YSortCameraGroup
from GameScripts.weapons.shooting import Shooting
from GameScripts.UI.display_rewards import RewardPopup
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BG_COLOR

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True
pygame.display.set_caption("Point 236 (Kota 236)")

# Start the player in the middle of the screen.
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height())

# Load Player & set position.
# Player loads all of its animation frames once when it is created.
player = Player(animator=animator_interface(type="player"), pos=player_pos)
print("Starting ammo:", player.ammo)
# Holds every bullet that is currently flying.
shooting = Shooting()

# Reward popup — shown in the top-right corner when the player loots a box.
reward_popup = RewardPopup()

# Build the world (a grid of environment objects).
current_map = world_build(False)
tile_map = world_build(True)
boundaries = []
boxes = []

# Camera group with y-sorting: the player and the environment are drawn together
# in one pass, sorted by Y position so lower sprites appear in front of higher ones.
camera_group = YSortCameraGroup(screen)
camera_group.add(player)

for sprite in current_map.get_sprites():
    camera_group.add(sprite)

for sprite in tile_map.get_sprites():
    camera_group.ground_sprites.add(sprite)

for row in tile_map.grid:
    for obj in row:

        if obj != 0 and obj.get_boundary():
            boundaries.append(obj)

for row in current_map.grid:
    for obj in row:
        if obj != 0 and obj.get_type() == "box":
            boxes.append(obj)


# -------------------------------------------------------------------------------------------
# Main game engine loop
# -------------------------------------------------------------------------------------------
while running:
    # dt is delta time in seconds. Movement uses this so speed does not depend
    # on the frame rate.
    dt = clock.tick(FPS) / 1000

    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # MOUSEBUTTONDOWN fires once per click. button 1 is the left button.
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if player.ammo > 0:
                shooting.fire(player.pos, player.facing)
                player.ammo -= 1
                print(player.ammo)
                
            


    # Read the keyboard state every frame and pass it to the player. Holding a
    # key moves continuously; the player switches to run while held and idle on
    # release. Movement logic lives in player_obj, so the loop stays short.
    keys = pygame.key.get_pressed()

    # for boundary in boundaries:
    #     if player.is_near(boundary):
    #         print("you are near boundary")
    #         player.push_back(boundary)
    
    player.move(dt, keys, boundaries, boxes)

    # check_collision returns the reward string when a fresh box is opened.
    # Pass it to the popup so the icon appears in the corner.
    reward = player.last_reward
    if reward:
        reward_popup.show(reward)
        player.last_reward = None
    

    # fill the screen with a colour to wipe away anything from last frame
    screen.fill(BG_COLOR)

    # Advance the player's animation, then draw every sprite (player + map)
    # in one y-sorted pass through the camera.
    for box in boxes:
        box.update_animation()
    
    player.update_animation()

    # Spawn enemies
    camera_group.spawn_enemy()

    # Update enemies
    for spider in camera_group.enemy_pool.get_activated_enemies():
        if not spider.dying:
            spider.move(dt, player)
        spider.update_animation()

    camera_group.custom_draw(player)

    # Move and draw the bullets. This comes after custom_draw because that call
    # updates the camera, and bullets need the camera offset to be drawn in the
    # right place on screen.
    shooting.update(dt)
    camera_offset = camera_group.get_camera().offset
    for bullet in shooting.bullets:
        bullet.draw(screen, camera_offset)

    # Return fully-dead spiders to the pool so they can be reused.
    camera_group.enemy_pool.check_dead()

    for bullet in shooting.bullets[:]:
        for spider in camera_group.enemy_pool.get_activated_enemies():
            if not spider.dying and bullet.hits(spider):
                spider.kill_spider()
                shooting.bullets.remove(bullet)
                break  # one bullet kills one spider; stop checking this bullet

    # Advance the popup timer and draw it on top of everything.
    reward_popup.update(dt)
    reward_popup.draw(screen)
    
    # flip() the display to put work on screen
    pygame.display.flip()

# call function to quit
pygame.quit()

# --------------------------------------------------------------------------------------------
