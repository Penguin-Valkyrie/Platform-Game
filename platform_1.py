import pygame
import random
from pygame import Vector2

# Initialize
pygame.init()
screen = pygame.display.set_mode((1200, 800))
pygame.display.set_caption('Platform')
clock = pygame.time.Clock()
game_floor = screen.get_height() - 200

# Global Variables
game_over = False
cloud_images = [
    pygame.image.load('images/cloud1.png'),
    pygame.image.load('images/cloud2.png')
]


# Classes
class Player():
    def __init__(self, position):
        self.position = position
        self.image = pygame.image.load('images/character.png')
        self.image_flipped = pygame.transform.flip(self.image, True, False)
        self.forward = True # False if moving to the left
        self.can_jump = True
        self.jumping = False
        self.falling = False
        self.jump_height = 275
        self.speed = 3
        self.jumping_speed = 15
        self.fireballs = []

    def draw(self, screen):
        if self.forward == True:
            screen.blit(self.image, self.position)
        else:
            screen.blit(self.image_flipped, self.position)

    def update(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_RIGHT]:
            self.forward = True

            if self.position[0] <= screen.get_width() // 2:
                self.position[0] += self.speed

        if key_pressed[pygame.K_LEFT]:
            self.forward = False
            self.position[0] -= self.speed
            if self.position[0] < 0:
                self.position[0] = 0

        if key_pressed[pygame.K_SPACE] and self.can_jump:
            self.can_jump = False
            self.jumping = True

        if self.jumping:
            self.position[1] -= self.jumping_speed * ((self.position[1] / game_floor) ** 1.5)

        if self.falling:
            self.position[1] += self.jumping_speed * ((self.position[1] / game_floor) ** 1.5)

        if self.position[1] <= game_floor - self.jump_height:
            self.jumping = False
            self.falling = True

        if self.position[1] > game_floor:
            self.position[1] = game_floor
            self.falling = False
            self.can_jump = True

class Fireball():
    def __init__(self, position, player):
        self.speed = 10
        self.size = 25
        self.forward = player.forward
        self.position = []
        self.position.append(position[0] + (self.size // 2) + (player.image.get_width() // 2))
        self.position.append(position[1] + (self.size // 2) + (player.image.get_height() // 2))

    def update(self):
        if self.forward == True:
            self.position[0] += self.speed
        else:
            self.position[0] -= self.speed

    def draw(self, screen):
        pygame.draw.circle(screen, (0, 100, 200), [self.position[0], self.position[1]], self.size)
        pygame.draw.circle(screen, (150, 100, 200), [self.position[0], self.position[1]], self.size // 1.25)
        pygame.draw.circle(screen, (255, 150, 255), [self.position[0], self.position[1]], self.size // 1.75)
        pygame.draw.circle(screen, (255, 255, 255), [self.position[0], self.position[1]], self.size // 2.5)

class Enemy():
    def __init__(self):
        self.image = pygame.image.load('images/enemy1.png')
        self.position = [screen.get_width() - 100, game_floor]
        self.speed = 3

    def update(self):
        self.position[0] -= self.speed
        pass
    
    def draw(self, screen):
        screen.blit(self.image, self.position)

class Cloud():
    def __init__(self):
        self.position = [screen.get_width(), random.randint(0, 400)]
        self.size = random.randint(50, 200)
        self.image = cloud_images[random.randint(0, len(cloud_images) - 1)]
        self.scaled_image = pygame.transform.scale(self.image, (self.image.get_width() * (self.size / 100), self.image.get_height() * (self.size / 100)))
        self.speed = 1 * (self.size / 100)

    def update(self):
        self.position[0] -= self.speed

    def draw(self, screen):
        screen.blit(self.scaled_image, self.position)

class Background():
    def __init__(self):
        self.image = pygame.image.load('images/background.jpg')
        self.image = pygame.transform.scale(self.image, (1500, 850))
        self.position = 0
        self.timer = 0
        self.speed = 4

    def update(self, player):
        key_pressed = pygame.key.get_pressed()
        if player.position[0] >= screen.get_width() // 2 and key_pressed[pygame.K_RIGHT]:
                self.position -= self.speed
        if self.position <= - 250:
            self.position = 0

    def draw(self, screen):
        screen.blit(self.image, (self.position, 0))

# Functions

# Global Variables
player = Player([200, game_floor])
enemy = Enemy()
clouds = []
clouds.append(Cloud())
background = Background()

# Game Loop
while not game_over:

    clock.tick(60)

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            game_over = True

        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_f:
                player.fireballs.append(Fireball(Vector2(player.position), player))

    # Draw Background
    background.update(player)
    background.draw(screen)

    # Clouds Update
    if random.randint(0, 500) < 5:
        clouds.append(Cloud())
    for c in clouds:
        c.update()
        c.draw(screen)
        if c.position[0] < 0 - c.scaled_image.get_width():
            clouds.remove(c)

    # Enemy Update
    enemy.update()
    enemy.draw(screen)

    # Player Update
    player.update()
    player.draw(screen)

    # Fireball Update
    for f in player.fireballs:
        f.update()
        f.draw(screen)
        if f.position[0] > screen.get_width():
            player.fireballs.remove(f)

    pygame.display.update()

pygame.quit()
