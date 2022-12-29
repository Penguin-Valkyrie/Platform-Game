import pygame
import GlobalVariables as gv
import random

# Classes
class Fireball():
    def __init__(self, position, player):
        self.speed = 10
        self.size = 50
        self.image = pygame.image.load('images/fireball.png')
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.forward = player.forward
        self.position = []
        if player.forward == False:
            self.position.append(position[0] - (self.size))
            self.position.append(position[1] + (player.image.get_height() // 2) - (self.size // 2) )
        else:
            self.position.append(position[0] + (player.image.get_width()))
            self.position.append(position[1] + (player.image.get_height() // 2) - (self.size // 2) )


    def update(self):
        if self.forward == True:
            self.position[0] += self.speed
        else:
            self.position[0] -= self.speed

    def draw(self, screen):
        screen.blit(self.image, (self.position[0], self.position[1]))

class Arcane_Magic():
    def __init__(self, position, player, forward):
        self.speed = 8
        self.size = 25
        self.image = pygame.image.load('images/arcane.png')
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.position = []
        self.forward = forward
        if forward == False:
            self.position.append(position[0] - (self.size))
            self.position.append(position[1] + (player.image.get_height() // 2) - (self.size // 2) )
        else:
            self.position.append(position[0] + (player.image.get_width()))
            self.position.append(position[1] + (player.image.get_height() // 2) - (self.size // 2) )

    def update(self):
        if self.forward == True:
            self.position[0] += self.speed
        else:
            self.position[0] -= self.speed

    def draw(self, screen):
        screen.blit(self.image, (self.position[0], self.position[1]))

class Holy():
    def __init__(self, position, player):
        self.health = 10
        self.speed = 12
        self.size = 25
        self.image = pygame.image.load('images/holy.png')
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.position = []
        self.forward = player.forward
        if self.forward == False:
            self.position.append(position[0] - (self.size))
            self.position.append(position[1] + (player.image.get_height() // 2) - (self.size // 2) )
        else:
            self.position.append(position[0] + (player.image.get_width()))
            self.position.append(position[1] + (player.image.get_height() // 2) - (self.size // 2) )

    def update(self):
        if self.forward == True:
            self.position[0] += self.speed
        else:
            self.position[0] -= self.speed

    def draw(self, screen):
        screen.blit(self.image, (self.position[0], self.position[1]))

class Enemy():
    def __init__(self, type, screen):
        if type == 1:
            self.image = pygame.image.load('images/enemy2.png')
            self.speed = 1
            self.health = 2
        elif type == 2:
            self.image = pygame.image.load('images/enemy3.png')
            self.speed = .5
            self.health = 3
        else:
            self.image = pygame.image.load('images/enemy1.png')
            self.speed = 2
            self.health = 1
        self.position = [screen.get_width() + 50, gv.game_floor - self.image.get_height()]
        

    def update(self):
        self.position[0] -= self.speed + gv.world_advance
        pass
    
    def draw(self, screen):
        screen.blit(self.image, self.position)

class Cloud():
    def __init__(self, screen):
        self.position = [screen.get_width(), random.randint(0, 400)]
        self.size = random.randint(50, 200)
        self.image = gv.cloud_images[random.randint(0, len(gv.cloud_images) - 1)]
        self.scaled_image = pygame.transform.scale(self.image, (self.image.get_width() * (self.size / 100), self.image.get_height() * (self.size / 100)))
        self.speed = (self.size / 100)

    def update(self):
        self.position[0] -= self.speed

    def draw(self, screen):
        screen.blit(self.scaled_image, self.position)

class Step_Cloud():
    def __init__(self, screen):
        self.image = pygame.image.load('images/Platform Cloud.png')
        self.position = [screen.get_width() + self.image.get_width(), screen.get_height() - self.image.get_height() - 200]
        self.speed = 1

    def update(self):
        self.position[0] -= self.speed + gv.world_advance

    def draw(self, screen):
        screen.blit(self.image, self.position)

class Background():
    def __init__(self):
        self.image = pygame.image.load('images/background.jpg')
        self.image = pygame.transform.scale(self.image, (1500, 850))
        self.position = 0
        self.timer = 0

    def update(self, world_advance, total_distance):
        self.position -= world_advance
        total_distance += world_advance
        if self.position <= self.image.get_width() * -1:
            self.position = 0

        return total_distance

    def draw(self, screen):
        screen.blit(self.image, (self.position, 0))
        screen.blit(self.image, (self.position + self.image.get_width(), 0))

class Coin():
    def __init__(self, screen, player):
        self.image = pygame.image.load('images/coin.png')
        self.position = []
        self.position.append(screen.get_width() + 100)
        self.position.append(gv.game_floor - player.image.get_height() - (player.jump_height * .75))
        self.speed = player.speed
        self.collision_buffer = 5

    def update(self):
        self.position[0] -= gv.world_advance

    def draw(self, screen):
        screen.blit(self.image, (self.position[0], self.position[1]))

class Heart():
    def __init__(self, screen, player):
        self.image = pygame.image.load('images/heart.png')
        self.position = []
        self.position.append(screen.get_width() + 100)
        self.position.append(gv.game_floor - player.image.get_height() - (player.jump_height + 25))
        self.speed = player.speed
        self.collision_buffer = 0

    def update(self):
        self.position[0] -= gv.world_advance

    def draw(self, screen):
        screen.blit(self.image, (self.position[0], self.position[1]))