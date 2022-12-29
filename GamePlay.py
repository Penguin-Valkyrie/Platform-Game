import pygame
import random
import GlobalVariables as gv
from pygame import Vector2
from Player import Player
import CollisionDetection
import NonPlayerClasses as npc

class GameInstance:
    def __init__(self):
        pygame.init()
        self.background = npc.Background()
        self.player = Player()
        self.enemy = []
        self.step_clouds = []
        self.coins = []
        self.hearts = []
        self.distance_message = gv.font.render('Distance: ' + str(int(gv.total_distance // 1)), True, (255, 255, 255))
        self.health_message = gv.font.render('Health: ' + str(self.player.health), True, (255, 255, 255))
        self.coins_message = gv.font.render('Coins: ' + str(self.player.coins_collected), True, (255, 255, 255))

    def update(self, events):

        # Setup
        gv.world_advance = 0

        # EventHandling
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_f:
                    self.player.fireballs.append(npc.Fireball(Vector2(self.player.position), self.player))
                
                elif e.key == pygame.K_d and self.player.attack_buffer <= 0:
                    self.player.arcane_magic.append(npc.Arcane_Magic(Vector2(self.player.position), self.player, True))
                    self.player.arcane_magic.append(npc.Arcane_Magic(Vector2(self.player.position), self.player, False))
                    self.player.attack_buffer = 240

                elif e.key == pygame.K_s and self.player.attack_buffer <= 0:
                    self.player.holy.append(npc.Holy(Vector2(self.player.position), self.player))
                    self.player.attack_buffer = 240
            
        key_pressed = pygame.key.get_pressed()

        if self.player.position[0] >= gv.screen.get_width() // 2 and key_pressed[pygame.K_RIGHT] and not gv.defeated:
            gv.world_advance = self.player.speed

        elif key_pressed[pygame.K_RIGHT]:
            self.player.advance()

        if key_pressed[pygame.K_LEFT]:
            self.player.retreat()

        if key_pressed[pygame.K_SPACE] and self.player.can_jump:
            self.player.jump()

        button_pressed = pygame.mouse.get_pressed()

        if self.player.position[0] >= gv.screen.get_width() // 2 and button_pressed[0] and pygame.mouse.get_pos()[0] > gv.screen.get_width() / 2 and not gv.defeated:
            self.world_advance = self.player.speed
        
        elif button_pressed[0] and pygame.mouse.get_pos()[0] < gv.screen.get_width() / 2:
            self.player.retreat()

        elif button_pressed[0] and pygame.mouse.get_pos()[0] > gv.screen.get_width() / 2:
            self.player.advance()

        # Update Text
        self.distance_message = gv.font.render('Distance: ' + str(int(gv.total_distance // 1)), True, (255, 255, 255))
        self.health_message = gv.font.render('Health: ' + str(self.player.health), True, (255, 255, 255))
        self.coins_message = gv.font.render('Coins: ' + str(self.player.coins_collected), True, (255, 255, 255))

        # Update Clouds
        for c in gv.clouds:
            c.update()
            if c.position[0] < 0 - c.scaled_image.get_width():
                gv.clouds.remove(c)

        if gv.defeated:
            return self

        # Update Player
        self.player.update(self.step_clouds, self.enemy)

        # Update NPCs
        if random.randint(0, 10000) < gv.cloud_likelihood:
            gv.clouds.append(npc.Cloud(gv.screen))
        if random.randint(0, 10000) < gv.platform_likelihood:
            self.step_clouds.append(npc.Step_Cloud(gv.screen))
        if random.randint(0, 10000) < gv.coin_likelihood + (gv.total_distance // 5000):
            self.coins.append(npc.Coin(gv.screen, self.player))
        if random.randint(0, 10000) < gv.platform_likelihood:
            self.step_clouds.append(npc.Step_Cloud(gv.screen))
        if random.randint(0, 10000) < gv.heart_likelihood:
            self.hearts.append(npc.Heart(gv.screen, self.player))


        for s in self.step_clouds:
            s.update()
            if s.position[0] < 0 - s.image.get_width():
                self.step_clouds.remove(s)

        for c in self.coins:
            c.update()
            if CollisionDetection.collision_detection(self.player, c, 2, None, False, self.player.collision_buffer, c.collision_buffer):
                self.coins.remove(c)
                self.player.coins_collected += 1
            if c.position[0] < 0 - c.image.get_width() and self.coins.__contains__(c):
                self.coins.remove(c)

        for h in self.hearts:
            h.update()
            if CollisionDetection.collision_detection(self.player, h, 2, None, False, self.player.collision_buffer, h.collision_buffer):
                self.hearts.remove(h)
                self.player.health += 1
            if h.position[0] < 0 - h.image.get_width() and self.hearts.__contains__(h):
                self.hearts.remove(h)

        if random.randint(0, 10000) < gv.enemy_likelihood + (gv.total_distance // 5000):
            self.enemy.append(npc.Enemy(0, gv.screen))
        elif random.randint(0, 10000) < (gv.enemy_likelihood + (gv.total_distance // 5000)) // 2 and gv.total_distance > 10000:
            self.enemy.append(npc.Enemy(1, gv.screen))
        elif random.randint(0, 10000) < (gv.enemy_likelihood + (gv.total_distance // 5000)) // 5 and gv.total_distance > 25000:
            self.enemy.append(npc.Enemy(2, gv.screen))
        
        for e in self.enemy:
            e.update()
            if e.health <= 0:
                self.enemy.remove(e)
                continue
            if CollisionDetection.collision_detection(self.player, e, 1, None, False, self.player.collision_buffer):
                self.player.health -= 1
                self.enemy.remove(e)

        if self.player.health == 0:
            gv.defeated = True
        
        return self

    def draw(self, screen):
        # Draw Background
        gv.total_distance = self.background.update(gv.world_advance, gv.total_distance)
        self.background.draw(gv.screen)

        # Draw Text
        gv.screen.blit(self.distance_message, (10, 10))
        gv.screen.blit(self.health_message, (gv.screen.get_width() - self.health_message.get_width() - 10, 10))
        gv.screen.blit(self.coins_message, (gv.screen.get_width() - self.coins_message.get_width() - 10, 20 + self.coins_message.get_height()))

        if gv.defeated:
            gv.screen.blit(gv.defeat_message, ((gv.screen.get_width() - gv.defeat_message.get_width()) // 2, (gv.screen.get_height() - gv.defeat_message.get_height()) // 2))

        # Draw Clouds
        for c in gv.clouds:
            c.draw(gv.screen)

        if gv.defeated:
            return

        # Draw Player
        self.player.draw(gv.screen)

        # Draw NPCs
        for s in self.step_clouds:
            s.draw(gv.screen)
        for c in self.coins:
            c.draw(gv.screen)
        for h in self.hearts:
            h.draw(gv.screen)

        # Draw Enemies
        for e in self.enemy:
            e.draw(gv.screen)
