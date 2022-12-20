import pygame
import random
from pygame import Vector2

# Initialize
pygame.init()
screen = pygame.display.set_mode((1200, 800))
pygame.display.set_caption('Platform')
clock = pygame.time.Clock()

# Global Variables
game_over = False
cloud_images = [
    pygame.image.load('images/cloud1.png'),
    pygame.image.load('images/cloud2.png')
]
game_floor = screen.get_height() - 200
total_distance = 0
font = pygame.font.SysFont('Arial', 32)

enemy_likelihood = 2 #if random.randint(0, 500) < enemy_likelihood


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
        self.arcane_magic = []

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
            self.position[1] -= self.jumping_speed * ((self.position[1] / game_floor) ** 1.75)

        if self.falling:
            self.position[1] += self.jumping_speed * ((self.position[1] / game_floor) ** 1.75)

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

class Enemy():
    def __init__(self):
        self.image = pygame.image.load('images/enemy1.png')
        self.position = [screen.get_width() + 50, game_floor]
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

    def update(self, player, total_distance):
        key_pressed = pygame.key.get_pressed()
        if player.position[0] >= screen.get_width() // 2 and key_pressed[pygame.K_RIGHT]:
                self.position -= self.speed
                total_distance += self.speed * 10
        if self.position <= self.image.get_width() * -1:
            self.position = 0

        return total_distance

    def draw(self, screen):
        screen.blit(self.image, (self.position, 0))
        screen.blit(self.image, (self.position + self.image.get_width(), 0))

# Functions

def collision_detection(object1, object2):
    # Object1 is the object whose corners are being tested
    # Object2 is the object being hit

    # First two are top left corner of Object1, then they move clockwise
    if object2.position[0] + 2 < object1.position[0] < object2.position[0] + object2.image.get_width() - 2 and \
        object2.position[1] + 2 < object1.position[1] < object2.position[1] + object2.image.get_height() - 2 or \
        object2.position[0] + 2 < object1.position[0] + object1.image.get_width() < object2.position[0] + object2.image.get_width() - 2 and \
        object2.position[1] + 2 < object1.position[1] < object2.position[1] + object2.image.get_height() - 2 or \
        object2.position[0] + 2 < object1.position[0] + object1.image.get_width() < object2.position[0] + object2.image.get_width() - 2 and \
        object2.position[1] + 2 < object1.position[1] + object1.image.get_height() < object2.position[1] + object2.image.get_height() - 2 or \
        object2.position[0] + 2 < object1.position[0] < object2.position[0] + object2.image.get_width() - 2 and \
        object2.position[1] + 2 < object1.position[1] + object1.image.get_height() < object2.position[1] + object2.image.get_height():
        return True
    else:
        return False
    

# Global Variables
player = Player([200, game_floor])
enemy = []
enemy.append(Enemy())
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
            
            elif e.key == pygame.K_d:
                player.arcane_magic.append(Arcane_Magic(Vector2(player.position), player, True))
                player.arcane_magic.append(Arcane_Magic(Vector2(player.position), player, False))

    # Draw Background
    total_distance = background.update(player, total_distance)
    background.draw(screen)

    # Distance Update
    distance_message = font.render('Distance: ' + str(total_distance), True, (255, 255, 255))
    screen.blit(distance_message, (10, 10))

    # Clouds Update
    if random.randint(0, 500) < 2:
        clouds.append(Cloud())
    for c in clouds:
        c.update()
        c.draw(screen)
        if c.position[0] < 0 - c.scaled_image.get_width():
            clouds.remove(c)

    # Enemy Update
    if random.randint(0, 500) < enemy_likelihood + (total_distance // 5000):
        enemy.append(Enemy())
    
    for e in enemy:
        e.update()
        e.draw(screen)

    # Player Update
    player.update()
    player.draw(screen)

    # Fireball Update
    for f in player.fireballs:
        f.update()
        f.draw(screen)
        for e in enemy:
            if collision_detection(f, e):
                enemy.remove(e)
                if player.fireballs.__contains__(f):
                    player.fireballs.remove(f)

            if f.position[0] > screen.get_width() and player.fireballs.__contains__(f):
                player.fireballs.remove(f)

    # Arcane Update
    for a in player.arcane_magic:
        a.update()
        a.draw(screen)
        for e in enemy:
            if collision_detection(a, e):
                enemy.remove(e)
                if player.arcane_magic.__contains__(a):
                    player.arcane_magic.remove(a)

            if a.position[0] > screen.get_width() and player.arcane_magic.__contains__(a):
                player.arcane_magic.remove(a)

    pygame.display.update()

pygame.quit()
