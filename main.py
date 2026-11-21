import pygame
from GameScripts.world_builder import world_build
from GameScripts.animator_controller import animator_interface
from GameScripts.Player.player_obj import Player
from GameScripts.Sprites.y_sort import YSortCameraGroup
from GameScripts.weapons.shooting import Shooting
from GameScripts.UI.display_rewards import RewardPopup
from GameScripts.UI.damage_flash import DamageFlash
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BG_COLOR
import random

def draw_ui(screen, player):

    # Health icon
    screen.blit(heart_icon, (20, 20))

    # Health counter
    health_text = ui_font.render(
        f"{player.lifeline.lives}/{player.lifeline.max_lives}",
        True,
        (255, 255, 255)
    )

    screen.blit(health_text, (60, 24))

    # Ammo icon
    screen.blit(ammo_icon, (20, 65))

    # Ammo counter
    ammo_text = ui_font.render(
        str(player.ammo),
        True,
        (255, 255, 255)
    )

    screen.blit(ammo_text, (60, 69))

    # For boxes opened
    screen.blit(box_icon, (20, 115))

    box_text = ui_font.render(
        f"{times_boxes_opened}/100",
        True,
        (255, 255, 255)
    )

    screen.blit(box_text, (60, 115))

pygame.init()

# Load background music
pygame.mixer.music.load("Assets/Audio/Background/AntSoldierGameMastered.wav")
pygame.mixer.music.play(-1)

# Walk sound effects
walk1 = pygame.mixer.Sound("Assets/Audio/SoundFX/Run/Fantozzi-StoneL1.ogg")
walk2 = pygame.mixer.Sound("Assets/Audio/SoundFX/Run/Fantozzi-StoneL2.ogg")
walk3 = pygame.mixer.Sound("Assets/Audio/SoundFX/Run/Fantozzi-StoneL3.ogg")
walk4 = pygame.mixer.Sound("Assets/Audio/SoundFX/Run/Fantozzi-StoneR1.ogg")
walk5 = pygame.mixer.Sound("Assets/Audio/SoundFX/Run/Fantozzi-StoneR2.ogg")
walk6 = pygame.mixer.Sound("Assets/Audio/SoundFX/Run/Fantozzi-StoneR3.ogg")

walk1.set_volume(0.08)
walk2.set_volume(0.08)
walk3.set_volume(0.08)
walk4.set_volume(0.08)
walk5.set_volume(0.08)
walk6.set_volume(0.08)

walk_channel = pygame.mixer.Channel(1)

# shooting sound effects
shot1 = pygame.mixer.Sound("Assets/Audio/SoundFX/Shoot/shots/shotgun.wav")
shot2 = pygame.mixer.Sound("Assets/Audio/SoundFX/Shoot/shots/rifle.wav")
shot1.set_volume(0.25)
shot2.set_volume(0.25)

shoot_channel = pygame.mixer.Channel(2)

shoot_sounds = [shot1, shot2]
walking_sounds = [walk1, walk2, walk3, walk4, walk5, walk6]

cardboard_box = pygame.mixer.Sound("Assets/Audio/SoundFX/Box/cardboard_box.wav")
cardboard_box.set_volume(0.55)
ouch = pygame.mixer.Sound("Assets/Audio/SoundFX/Combat/ouch.wav")

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

# Load UI icons
heart_icon = pygame.image.load(
    "Assets/Artwork/Icons/Heart.png"
).convert_alpha()

ammo_icon = pygame.image.load(
    "Assets/Artwork/Icons/ShotgunShells.png"
).convert_alpha()

box_icon = pygame.image.load(
    "Assets/Artwork/Environment/Objects/Box/box_1.png"
)

# Resize icons (optional)
heart_icon = pygame.transform.scale(heart_icon, (32, 32))
ammo_icon = pygame.transform.scale(ammo_icon, (32, 32))
box_icon = pygame.transform.scale(box_icon, (32, 32))

# Font for UI counters
ui_font = pygame.font.Font(None, 32)

# Holds every bullet that is currently flying.
shooting = Shooting()

# Reward popup — shown in the top-right corner when the player loots a box.
reward_popup = RewardPopup()

# Red flash over the screen when the ant is bitten.
damage_flash = DamageFlash()

# Build the world (a grid of environment objects).
current_map = world_build(False)
tile_map = world_build(True)
boundaries = []
boxes = []
times_boxes_opened = 0

# Camera group with y-sorting: the player and the environment are drawn together
# in one pass, sorted by Y position so lower sprites appear in front of higher ones.
camera_group = YSortCameraGroup(screen)
camera_group.add(player)

alcohol_bottle = None
has_bottle_spawned = False
for sprite in current_map.get_sprites():
    if sprite.type != "alcohol":
        camera_group.add(sprite)
    else:
        alcohol_bottle = sprite

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

print(len(boxes))

# -------------------------------------------------------------------------------------------
# Main game engine loop
# -------------------------------------------------------------------------------------------
while running:
    # dt is delta time in seconds. Movement uses this so speed does not depend
    # on the frame rate.
    dt = clock.tick(FPS) / 1000

    if player.lifeline.is_dead():
        print("You died... Game Over")
        running = False

    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # MOUSEBUTTONDOWN fires once per click. button 1 is the left button.
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if not shoot_channel.get_busy():
                if player.ammo > 0:
                    if not shoot_channel.get_busy():
                        shot = random.choice(shoot_sounds)
                        shoot_channel.play(shot)
                    # where the cursor is on the screen
                    mouse_screen = pygame.Vector2(pygame.mouse.get_pos())

                    # Screen to world: Add how far the camera has scrolled
                    mouse_world = mouse_screen + camera_group.get_camera().offset
                    
                    # Direction from the ant to the cursor
                    direction = mouse_world - player.pos

                    # normalise() fails on a zero-length vector (a click exactly on the ant),\
                    # so only continue when the vector has some length. 
                    if direction.length_squared() > 0:
                        direction = direction.normalize()
                        # Commented out print(direction) and print(ammo)because the terminal builds garbage 
                        # memory/stack overflow or something like that
                        # I'm not pro, don't quote me on terminology!! lululul
                        # print(direction)
                        player.face_towards(direction)
                        player.start_shooting()
                        shooting.fire(player.pos, direction)
                        player.ammo -= 1
                        # print(player.ammo)

    # Read the keyboard state every frame and pass it to the player. Holding a
    # key moves continuously; the player switches to run while held and idle on
    # release. Movement logic lives in player_obj, so the loop stays short.
    keys = pygame.key.get_pressed()

    moving = (
        keys[pygame.K_w] or
        keys[pygame.K_a] or
        keys[pygame.K_s] or
        keys[pygame.K_d]
    )

    if moving:
        if not walk_channel.get_busy():
            walk_sound = random.choice(walking_sounds)
            walk_channel.play(walk_sound)
    else:
        walk_channel.stop()

    # for boundary in boundaries:
    #     if player.is_near(boundary):
    #         print("you are near boundary")
    #         player.push_back(boundary)
    
    player.move(dt, keys, boundaries, boxes, alcohol_bottle)

    # check_collision returns the reward string when a fresh box is opened.
    # Pass it to the popup so the icon appears in the corner.
    reward = player.last_reward
    if reward:
        cardboard_box.play()
        reward_popup.show(reward)
        player.last_reward = None
        times_boxes_opened += 1
    

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

    # A spider bit the ant this frame: start the red flash, then clear the flag.
    if player.just_hit:
        ouch.play()
        damage_flash.trigger()
        player.just_hit = False

    camera_group.custom_draw(player)

    # Move and draw the bullets. This comes after custom_draw because that call
    # updates the camera, and bullets need the camera offset to be drawn in the
    # right place on screen.
    shooting.update(dt)
    camera_group.get_camera().offset
    player_pos - camera_group.get_camera().offset
    player_pos.normalize()
    for bullet in shooting.bullets:
        bullet.draw(screen, camera_group.get_camera().offset)

    # Return fully-dead spiders to the pool so they can be reused.
    camera_group.enemy_pool.check_dead()

    for bullet in shooting.bullets[:]:
        for spider in camera_group.enemy_pool.get_activated_enemies():
            if not spider.dying and bullet.hits(spider):
                spider.kill_spider()
                shooting.bullets.remove(bullet)
                break  # one bullet kills one spider; stop checking this bullet

    # Red damage flash. Drawn before the popup and HUD so they stay readable.
    damage_flash.update(dt)
    damage_flash.draw(screen)

    # Advance the popup timer and draw it on top of everything.
    reward_popup.update(dt)
    reward_popup.draw(screen)

    # Icons/UI (User Interface)
    draw_ui(screen, player)

    # Last bit - Just to spawn the bottle
    if has_bottle_spawned == False and times_boxes_opened >= 100:
        camera_group.add(alcohol_bottle)
    
    # flip() the display to put work on screen
    pygame.display.flip()

# call function to quit
pygame.quit()

# --------------------------------------------------------------------------------------------
