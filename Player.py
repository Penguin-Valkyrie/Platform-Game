import pygame
import GlobalVariables as gv
import CollisionDetection
import NonPlayerClasses as npc

class Player():
    def __init__(self,):
        self.health = 5
        self.height = 100

        # Walking Images
        self.image_walking_index = 0
        self.walking_image_speed = 150
        self.image_walking_load = pygame.image.load('images/character_walk.png')
        self.image_walking_load = pygame.transform.scale(self.image_walking_load, (self.image_walking_load.get_width() * (self.height / self.image_walking_load.get_height()), self.height))
        
        self.width = self.image_walking_load.get_width() / 4

        self.images_walking = []
        self.images_walking_flipped = []
        for i in range(0, 4):
            self.images_walking.append(pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32))
            self.images_walking[i].blit(self.image_walking_load, (0, 0), [i * self.width, 0, self.width, self.height])
            self.images_walking_flipped.append(pygame.transform.flip(self.images_walking[i], True, False))

        # Jumping Images
        self.image_jumping_index = 0
        self.jumping_image_speed = 100
        self.image_jumping_load = pygame.image.load('images/character_jump.png')
        self.image_jumping_load = pygame.transform.scale(self.image_jumping_load, (self.image_jumping_load.get_width() * (self.height / self.image_jumping_load.get_height()), self.height))
        
        self.images_jumping = []
        self.images_jumping_flipped = []
        for i in range(0, 7):
            self.images_jumping.append(pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32))
            self.images_jumping[i].blit(self.image_jumping_load, (0, 0), [i * self.width, 0, self.width, self.height])
            self.images_jumping_flipped.append(pygame.transform.flip(self.images_jumping[i], True, False))

        # Attacking Images
        self.image_attack_index = 0
        self.attack_image_speed = 100
        self.image_attack_load = pygame.image.load('images/character_attack.png')
        self.image_attack_load = pygame.transform.scale(self.image_attack_load, (self.image_attack_load.get_width() * (self.height / self.image_attack_load.get_height()), self.height))
        
        self.images_attack = []
        self.images_attack_flipped = []
        for i in range(0, 4):
            self.images_attack.append(pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32))
            self.images_attack[i].blit(self.image_attack_load, (0, 0), [i * self.width, 0, self.width, self.height])
            self.images_attack_flipped.append(pygame.transform.flip(self.images_attack[i], True, False))

        self.position = [100, gv.game_floor - self.height]
        self.collision_buffer = 20
        self.forward = True # False if moving to the left
        self.can_jump = True
        self.jumping = False
        self.jump_height = 300
        self.floor = gv.game_floor
        self.speed = 4
        self.jumping_speed = 12

        self.attacking = False
        self.attacks = []
        self.attack_buffer = 0
        self.coins_collected = 0
        self.coins_speed_increase = True

    def draw(self, screen):        
        if self.forward == True:
            if self.can_jump == False:
                screen.blit(self.images_jumping[self.image_jumping_index], self.position)
            elif self.attacking == True:
                screen.blit(self.images_attack[self.image_attack_index], self.position)
            else:
                screen.blit(self.images_walking[self.image_walking_index], self.position)
        else:
            if self.can_jump == False:
                screen.blit(self.images_jumping_flipped[self.image_jumping_index], self.position)
            elif self.attacking == True:
                screen.blit(self.images_attack_flipped[self.image_attack_index], self.position)
            else:
                screen.blit(self.images_walking_flipped[self.image_walking_index], self.position)
        
        # Draw Attack Buffer
        pygame.draw.rect(screen, (200, 0, 0), [self.position[0], self.position[1] + 10, 7, 90])
        pygame.draw.rect(screen, (0, 0, 0), [self.position[0], self.position[1] + 10, 7, (self.attack_buffer / 240) * 90])

        # Draw Attacks
        for a in self.attacks:
            a.draw(gv.screen)

    def advance(self):
        self.forward = True
        if not self.attacking:
            if self.position[0] <= gv.screen.get_width() // 2:
                self.position[0] += self.speed
            self.walking_image_speed -= gv.clock.get_time()
            if self.walking_image_speed <= 0:
                self.walking_image_speed = 100
                self.image_walking_index += 1
                if self.image_walking_index > 3:
                    self.image_walking_index = 0

    def retreat(self):
        self.forward = False
        self.position[0] -= self.speed
        if self.position[0] < 0:
            self.position[0] = 0
        self.walking_image_speed -= gv.clock.get_time()
        if self.walking_image_speed <= 0:
            self.walking_image_speed = 100
            self.image_walking_index += 1
            if self.image_walking_index > 3:
                self.image_walking_index = 0

    def jump(self):
        self.can_jump = False
        self.jumping = True

    def attack(self, type):
        self.attacking = True
        self.attacks.append(type)

    def update(self, platforms, enemies):              

        if self.coins_collected >= 20 and self.coins_collected % 20 == 0 and self.coins_speed_increase:
            self.speed += .5
            self.coins_speed_increase = False
        
        if self.coins_collected % 20 == 1:
            self.coins_speed_increase = True

        # Attack Update

        if self.attack_buffer > 0:
            self.attack_buffer -= 1

        if self.attacking:
            self.attack_image_speed -= gv.clock.get_time()
            if self.attack_image_speed <= 0:
                self.attack_image_speed = 100
                self.image_attack_index += 1
                if self.image_attack_index >= len(self.images_attack) - 1:
                    self.image_attack_index = 0
                    self.attacking = False

        for a in self.attacks:
            a.update()
            for e in enemies:
                if CollisionDetection.collision_detection(a, e):
                    gv.score += 100
                    e.health -= 1
                    a.health -= 1
                    if a.health <= 0 and self.attacks.__contains__(a):
                        self.attacks.remove(a)
                        return

                if a.position[0] > gv.screen.get_width() and self.attacks.__contains__(a):
                    self.attacks.remove(a)
                    return

            if a.position[0] < 0 - a.width and self.attacks.__contains__(a):
                self.attacks.remove(a)
                return

            if a.position[1] > gv.game_floor and self.attacks.__contains__(a):
                self.attacks.remove(a)

        # Jumping Update:
        if self.jumping:
            self.jumping_image_speed -= gv.clock.get_time()
            if self.image_jumping_index < 3:
                self.jumping_image_speed -= gv.clock.get_time() * 3
                if self.jumping_image_speed <= 0:
                    self.image_jumping_index += 1
                    self.jumping_image_speed = 100
            else:
                self.position[1] -= self.jumping_speed * (((self.position[1] + self.height) / self.floor) ** 1.75)
        else:
            if self.image_jumping_index < 6:
                self.jumping_image_speed -= gv.clock.get_time()
                if self.jumping_image_speed <= 0:
                    self.jumping_image_speed = 100
                    self.image_jumping_index += 1
            for p in platforms:
                if CollisionDetection.collision_detection(self, p, 2, True, self.collision_buffer):
                    self.can_jump = True
                    self.image_jumping_index = 0
                    self.floor = self.position[1] + self.height
                    return
            self.position[1] += self.jumping_speed * (((self.position[1] + self.height) / self.floor) ** 1.75)

        if self.position[1] <= self.floor - self.jump_height:
            self.jumping = False

        if self.position[1] + self.height > self.floor:
            self.position[1] = self.floor - self.height
            self.image_jumping_index = 0
            if self.floor == gv.game_floor:
                self.can_jump = True
            else:
                self.floor = gv.game_floor