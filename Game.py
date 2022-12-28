import pygame
import random
import GlobalVariables as gv
from pygame import Vector2
from Player import Player
import CollisionDetection
import NonPlayerClasses as npc

# Initialize
pygame.init()

# Global Variables
player = Player()
enemy = []
enemy.append(npc.Enemy(0, gv.screen))
step_clouds = []
step_clouds.append(npc.Step_Cloud(gv.screen))
background = npc.Background()
coins = []

# Game Loop
while not gv.game_over:

    gv.clock.tick(60)

    # Setup
    world_advance = 0

    # Event Handling
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            gv.game_over = True

        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_f:
                player.fireballs.append(npc.Fireball(Vector2(player.position), player))
            
            elif e.key == pygame.K_d and player.attack_buffer <= 0:
                player.arcane_magic.append(npc.Arcane_Magic(Vector2(player.position), player, True))
                player.arcane_magic.append(npc.Arcane_Magic(Vector2(player.position), player, False))
                player.attack_buffer = 240

            elif e.key == pygame.K_s and player.attack_buffer <= 0:
                player.holy.append(npc.Holy(Vector2(player.position), player))
                player.attack_buffer = 240
        
    
    key_pressed = pygame.key.get_pressed()

    if player.position[0] >= gv.screen.get_width() // 2 and key_pressed[pygame.K_RIGHT] and not gv.defeated:
        world_advance = player.speed - 1

    elif key_pressed[pygame.K_RIGHT]:
        player.advance()

    if key_pressed[pygame.K_LEFT]:
        player.retreat()

    if key_pressed[pygame.K_SPACE] and player.can_jump:
        player.jump()

    button_pressed = pygame.mouse.get_pressed()

    if player.position[0] >= gv.screen.get_width() // 2 and button_pressed[0] and pygame.mouse.get_pos()[0] > gv.screen.get_width() / 2 and not gv.defeated:
        world_advance = player.speed - 1
    
    elif button_pressed[0] and pygame.mouse.get_pos()[0] < gv.screen.get_width() / 2:
        player.retreat()

    elif button_pressed[0] and pygame.mouse.get_pos()[0] > gv.screen.get_width() / 2:
        player.advance()

    # Draw Background
    gv.total_distance = background.update(world_advance, gv.total_distance)
    background.draw(gv.screen)

    # Text Update
    distance_message = gv.font.render('Distance: ' + str(int(gv.total_distance // 1)), True, (255, 255, 255))
    gv.screen.blit(distance_message, (10, 10))
    health_message = gv.font.render('Health: ' + str(player.health), True, (255, 255, 255))
    gv.screen.blit(health_message, (gv.screen.get_width() - health_message.get_width() - 10, 10))
    coins_message = gv.font.render('Coins: ' + str(player.coins_collected), True, (255, 255, 255))
    gv.screen.blit(coins_message, (gv.screen.get_width() - coins_message.get_width() - 10, 20 + distance_message.get_height()))

    # Clouds Update
    if random.randint(0, 10000) < gv.cloud_likelihood:
        gv.clouds.append(npc.Cloud(gv.screen))
    for c in gv.clouds:
        c.update()
        c.draw(gv.screen)
        if c.position[0] < 0 - c.scaled_image.get_width():
            gv.clouds.remove(c)
    
    # Platform Update
    if random.randint(0, 10000) < gv.platform_likelihood:
        step_clouds.append(npc.Step_Cloud(gv.screen))
    for s in step_clouds:
        s.update()
        s.draw(gv.screen)
        if s.position[0] < 0 - s.image.get_width():
            step_clouds.remove(s)

    # Check if defeated
    if gv.defeated:
        gv.screen.blit(gv.defeat_message, (gv.screen.get_width() // 2 - gv.defeat_message.get_width() // 2, gv.screen.get_height() // 2))
        pygame.display.update()
        continue

    # Coin Update
    if random.randint(0, 10000) < gv.coin_likelihood + (gv.total_distance // 5000):
        coins.append(npc.Coin(gv.screen, player))

    for c in coins:
        c.update()
        c.draw(gv.screen)
        if CollisionDetection.collision_detection(player, c, 2, None, False, player.collision_buffer, c.collision_buffer):
            coins.remove(c)
            player.coins_collected += 1

    # Enemy Update
    if random.randint(0, 10000) < gv.enemy_likelihood + (gv.total_distance // 5000):
        enemy.append(npc.Enemy(0, gv.screen))
    elif random.randint(0, 10000) < (gv.enemy_likelihood + (gv.total_distance // 5000)) // 2 and gv.total_distance > 10000:
        enemy.append(npc.Enemy(1, gv.screen))
    elif random.randint(0, 10000) < (gv.enemy_likelihood + (gv.total_distance // 5000)) // 5 and gv.total_distance > 25000:
        enemy.append(npc.Enemy(2, gv.screen))
    
    for e in enemy:
        e.update()
        e.draw(gv.screen)
        if e.health <= 0:
            enemy.remove(e)
            continue
        if CollisionDetection.collision_detection(player, e, 1, gv.screen, False, player.collision_buffer):
            player.health -= 1
            enemy.remove(e)

    # Player Update
    player.update(step_clouds)
    player.draw(gv.screen)

    if player.health == 0:
        gv.defeated = True

    # Fireball Update
    for f in player.fireballs:
        f.update()
        f.draw(gv.screen)
        for e in enemy:
            if CollisionDetection.collision_detection(f, e):
                e.health -= 1
                if player.fireballs.__contains__(f):
                    player.fireballs.remove(f)

            if f.position[0] > gv.screen.get_width() and player.fireballs.__contains__(f):
                player.fireballs.remove(f)

    # Arcane Update
    for a in player.arcane_magic:
        a.update()
        a.draw(gv.screen)
        for e in enemy:
            if CollisionDetection.collision_detection(a, e):
                e.health -= 1
                if player.arcane_magic.__contains__(a):
                    player.arcane_magic.remove(a)

        if a.position[0] > gv.screen.get_width() and player.arcane_magic.__contains__(a):
                player.arcane_magic.remove(a)

    # Holy Update
    for h in player.holy:
        h.update()
        h.draw(gv.screen)
        for e in enemy:
            if CollisionDetection.collision_detection(h, e):
                e.health -= 1
                h.health -= 1

        if h.position[0] > gv.screen.get_width() and player.holy.__contains__(h):
                player.holy.remove(h)
        
        if h.health <= 0 and player.holy.__contains__(h):
            player.holy.remove(h)

    pygame.display.update()

pygame.quit()
