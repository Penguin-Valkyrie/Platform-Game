import pygame
import GlobalVariables as gv
import CollisionDetection

class Player():
    def __init__(self,):
        self.health = 5
        self.image = pygame.image.load('images/character1.png')
        self.image_flipped = pygame.transform.flip(self.image, True, False)
        self.position = [100, gv.game_floor - self.image.get_height()]
        self.collision_buffer = 15
        self.forward = True # False if moving to the left
        self.can_jump = True
        self.jumping = False
        self.jump_height = 300
        self.floor = gv.game_floor
        self.speed = 4
        self.jumping_speed = 12
        self.fireballs = []
        self.attack_buffer = 0
        self.arcane_magic = []
        self.holy = []
        self.coins_collected = 0
        self.coins_speed_increase = True

    def draw(self, screen):
        if self.forward == True:
            screen.blit(self.image, self.position)
        else:
            screen.blit(self.image_flipped, self.position)
        
        # Draw Attack Buffer
        pygame.draw.rect(screen, (200, 0, 0), [self.position[0], self.position[1], 10, 100])
        pygame.draw.rect(screen, (0, 0, 0), [self.position[0], self.position[1], 10, (self.attack_buffer / 240) * 100])

    def advance(self):
        self.forward = True
        if self.position[0] <= gv.screen.get_width() // 2:
            self.position[0] += self.speed

    def retreat(self):
        self.forward = False
        self.position[0] -= self.speed
        if self.position[0] < 0:
            self.position[0] = 0

    def jump(self):
        self.can_jump = False
        self.jumping = True

    def update(self, platforms):              

        if self.coins_collected >= 20 and self.coins_collected % 20 == 0 and self.coins_speed_increase:
            self.coins_speed_increase = False
            self.speed += .5

        if self.coins_collected % 20 == 1:
            self.coins_speed_increase = True

        if self.attack_buffer > 0:
            self.attack_buffer -= 1

        if self.jumping:
            self.position[1] -= self.jumping_speed * (((self.position[1] + self.image.get_width()) / self.floor) ** 1.75)
        else:
            for p in platforms:
                if CollisionDetection.collision_detection(self, p, 2, None, True, self.collision_buffer):
                    self.can_jump = True
                    self.floor = self.position[1] + self.image.get_height()
                    return
            self.position[1] += self.jumping_speed * (((self.position[1] + self.image.get_width()) / self.floor) ** 1.75)

        if self.position[1] <= self.floor - self.jump_height:
            self.jumping = False

        if self.position[1] + self.image.get_height() > self.floor:
            self.position[1] = self.floor - self.image.get_height()
            if self.floor == gv.game_floor:
                self.can_jump = True
            else:
                self.floor = gv.game_floor
