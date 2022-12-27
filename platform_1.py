import pygame
import random
from pygame import Vector2
from pygame._sdl2 import touch

# Initialize
pygame.init()
screen = pygame.display.set_mode((1200, 800))
pygame.display.set_caption('Platform')
clock = pygame.time.Clock()

# Global Variables
game_over = False
cloud_images = [
    pygame.image.load('images/cloud1.png'),
    pygame.image.load('images/cloud2.png'),
    pygame.image.load('images/cloud3.png')
]
game_floor = screen.get_height() - 100 # Image positions are set so their bottom is on the game_floor
total_distance = 0
font = pygame.font.SysFont('Arial', 48)
enemy_likelihood = 2 #if random.randint(0, 500) < enemy_likelihood
coin_likelihood = 2 #if random.randint(0, 500) < enemy_likelihood
platform_likelihood = 1 #if random.randint(0, 500) < enemy_likelihood
defeated = False
defeat_message = font.render("Defeated!", True, (255, 255, 255))

# Functions

def collision_detection(object1, object2, screen = None, object1BottomOnly = False):
    # Object1 is the object whose corners are being tested
    # Object2 is the object being hit

    if screen is not None:
        pygame.draw.rect(screen, (0, 0, 0), [object2.position[0], object2.position[1], 5, 5])
        pygame.draw.rect(screen, (0, 0, 0), [object2.position[0] + object2.image.get_width(), object2.position[1], 5, 5])
        pygame.draw.rect(screen, (0, 0, 0), [object2.position[0] + object2.image.get_width(), object2.position[1] + object2.image.get_height(), 5, 5])
        pygame.draw.rect(screen, (0, 0, 0), [object2.position[0], object2.position[1] + object2.image.get_height(), 5, 5])
        pygame.draw.rect(screen, (255, 255, 255), [object1.position[0], object1.position[1], 5, 5])
        pygame.draw.rect(screen, (255, 255, 255), [object1.position[0] + object1.image.get_width(), object1.position[1], 5, 5])
        pygame.draw.rect(screen, (255, 255, 255), [object1.position[0] + object1.image.get_width(), object1.position[1] + object1.image.get_height(), 5, 5])
        pygame.draw.rect(screen, (255, 255, 255), [object1.position[0], object1.position[1] + object1.image.get_height(), 5, 5])

    # First two are top left corner of Object1, then they move clockwise
    if (object1BottomOnly == False) and (object2.position[0] + 2 <= object1.position[0] <= object2.position[0] + object2.image.get_width() - 2 and \
        object2.position[1] + 2 <= object1.position[1] <= object2.position[1] + object2.image.get_height() - 2 or \
        object2.position[0] + 2 <= object1.position[0] + object1.image.get_width() <= object2.position[0] + object2.image.get_width() - 2 and \
        object2.position[1] + 2 <= object1.position[1] <= object2.position[1] + object2.image.get_height() - 2 or \
        object2.position[0] + 2 <= object1.position[0] + object1.image.get_width() <= object2.position[0] + object2.image.get_width() - 2 and \
        object2.position[1] + 2 <= object1.position[1] + object1.image.get_height() <= object2.position[1] + object2.image.get_height() - 2 or \
        object2.position[0] + 2 <= object1.position[0] <= object2.position[0] + object2.image.get_width() - 2 and \
        object2.position[1] + 2 <= object1.position[1] + object1.image.get_height() <= object2.position[1] + object2.image.get_height()):

        return True

    elif(object1BottomOnly == True) and (object2.position[0] + 2 <= object1.position[0] + object1.image.get_width() <= object2.position[0] + object2.image.get_width() - 2 and \
        object2.position[1] + 2 <= object1.position[1] + object1.image.get_height() <= object2.position[1] + object2.image.get_height() - 2 or \
        object2.position[0] + 2 <= object1.position[0] <= object2.position[0] + object2.image.get_width() - 2 and \
        object2.position[1] + 2 <= object1.position[1] + object1.image.get_height() <= object2.position[1] + object2.image.get_height()):

        return True

    else:
        return False

# Classes
class Player():
    def __init__(self):
        self.health = 5
        self.image = pygame.image.load('images/character.png')
        self.image_flipped = pygame.transform.flip(self.image, True, False)
        self.position = [100, game_floor - self.image.get_height()]
        self.forward = True # False if moving to the left
        self.can_jump = True
        self.jumping = False
        self.jump_height = 275
        self.floor = game_floor
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
        pygame.draw.rect(screen, (255, 0, 0), [self.position[0] - 15, self.position[1], 10, 100])
        pygame.draw.rect(screen, (0, 0, 0), [self.position[0] - 15, self.position[1], 10, (self.attack_buffer / 240) * 100])

    def advance(self):
        self.forward = True
        if self.position[0] <= screen.get_width() // 2:
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
                if collision_detection(self, p, screen, True):
                    self.can_jump = True
                    self.floor = self.position[1] + self.image.get_height()
                    return
            self.position[1] += self.jumping_speed * (((self.position[1] + self.image.get_width()) / self.floor) ** 1.75)

        if self.position[1] <= self.floor - self.jump_height:
            self.jumping = False

        if self.position[1] + self.image.get_height() > self.floor:
            self.position[1] = self.floor - self.image.get_height()
            if self.floor == game_floor:
                self.can_jump = True
            else:
                self.floor = game_floor

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
    def __init__(self, type):
        if type == 1:
            self.image = pygame.image.load('images/enemy2.png')
            self.speed = 2
            self.health = 2
        elif type == 2:
            self.image = pygame.image.load('images/enemy3.png')
            self.speed = 1
            self.health = 3
        else:
            self.image = pygame.image.load('images/enemy1.png')
            self.speed = 3
            self.health = 1
        self.position = [screen.get_width() + 50, game_floor - self.image.get_height()]
        

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
        self.speed = (self.size / 100)

    def update(self):
        self.position[0] -= self.speed

    def draw(self, screen):
        screen.blit(self.scaled_image, self.position)

class Step_Cloud():
    def __init__(self):
        self.image = pygame.image.load('images/Platform Cloud.png')
        self.position = [screen.get_width() - 100, screen.get_height() - self.image.get_height() - 200]
        self.speed = 1

    def update(self):
        self.position[0] -= self.speed

    def draw(self, screen):
        screen.blit(self.image, self.position)

class Background():
    def __init__(self):
        self.image = pygame.image.load('images/background.jpg')
        self.image = pygame.transform.scale(self.image, (1500, 850))
        self.position = 0
        self.timer = 0

    def update(self):
        if self.position <= self.image.get_width() * -1:
            self.position = 0

    def advance(self, player, total_distance):
        background.position -= player.speed
        total_distance += player.speed

        return total_distance

    def draw(self, screen):
        screen.blit(self.image, (self.position, 0))
        screen.blit(self.image, (self.position + self.image.get_width(), 0))

class Coin():
    def __init__(self, screen, player):
        self.image = pygame.image.load('images/coin.png')
        self.position = []
        self.position.append(screen.get_width() + 100)
        self.position.append(game_floor - player.image.get_height() - (player.jump_height * .75))
        self.speed = player.speed

    def update(self):
        self.position[0] -= self.speed

    def draw(self, screen):
        screen.blit(self.image, (self.position[0], self.position[1]))  

# Global Variables
player = Player()
enemy = []
enemy.append(Enemy(0))
clouds = []
clouds.append(Cloud())
step_clouds = []
step_clouds.append(Step_Cloud())
background = Background()
coins = []


# Game Loop
while not game_over:

    clock.tick(60)

    # Event Handling

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            game_over = True

        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_f:
                player.fireballs.append(Fireball(Vector2(player.position), player))
            
            elif e.key == pygame.K_d and player.attack_buffer <= 0:
                player.arcane_magic.append(Arcane_Magic(Vector2(player.position), player, True))
                player.arcane_magic.append(Arcane_Magic(Vector2(player.position), player, False))
                player.attack_buffer = 240

            elif e.key == pygame.K_s and player.attack_buffer <= 0:
                player.holy.append(Holy(Vector2(player.position), player))
                player.attack_buffer = 240
        
    
    key_pressed = pygame.key.get_pressed()

    if player.position[0] >= screen.get_width() // 2 and key_pressed[pygame.K_RIGHT]:
        total_distance = background.advance(player, total_distance)

    elif key_pressed[pygame.K_RIGHT]:
        player.advance()

    if key_pressed[pygame.K_LEFT]:
        player.retreat()

    if key_pressed[pygame.K_SPACE] and player.can_jump:
        player.jump()

    button_pressed = pygame.mouse.get_pressed()

    if player.position[0] >= screen.get_width() // 2 and button_pressed[0] and pygame.mouse.get_pos()[0] > screen.get_width() / 2:
        total_distance = background.advance(player, total_distance)
    
    elif button_pressed[0] and pygame.mouse.get_pos()[0] < screen.get_width() / 2:
        player.retreat()

    elif button_pressed[0] and pygame.mouse.get_pos()[0] > screen.get_width() / 2:
        player.advance()

    # Draw Background
    background.update()
    background.draw(screen)

    # Text Update
    distance_message = font.render('Distance: ' + str(int(total_distance // 1)), True, (255, 255, 255))
    screen.blit(distance_message, (10, 10))
    health_message = font.render('Health: ' + str(player.health), True, (255, 255, 255))
    screen.blit(health_message, (screen.get_width() - health_message.get_width() - 10, 10))
    coins_message = font.render('Coins: ' + str(player.coins_collected), True, (255, 255, 255))
    screen.blit(coins_message, (screen.get_width() - coins_message.get_width() - 10, 20 + distance_message.get_height()))

    # Clouds Update
    if random.randint(0, 500) < 2:
        clouds.append(Cloud())
    for c in clouds:
        c.update()
        c.draw(screen)
        if c.position[0] < 0 - c.scaled_image.get_width():
            clouds.remove(c)
    
    # Platform Update
    if random.randint(0, 500) < platform_likelihood:
        step_clouds.append(Step_Cloud())
    for s in step_clouds:
        s.update()
        s.draw(screen)
        if s.position[0] < 0 - s.image.get_width():
            step_clouds.remove(s)

    # Check if defeated
    if defeated == True:
        screen.blit(defeat_message, (screen.get_width() // 2 - defeat_message.get_width() // 2, screen.get_height() // 2))
        pygame.display.update()
        continue

    # Coin Update
    if random.randint(0, 500) < coin_likelihood + (total_distance // 5000):
        coins.append(Coin(screen, player))

    for c in coins:
        c.update()
        c.draw(screen)
        if collision_detection(player, c):
            coins.remove(c)
            player.coins_collected += 1

    # Enemy Update
    if random.randint(0, 500) < enemy_likelihood + (total_distance // 5000):
        enemy.append(Enemy(0))
    elif random.randint(0, 500) < (enemy_likelihood + (total_distance // 5000)) // 2 and total_distance > 10000:
        enemy.append(Enemy(1))
    elif random.randint(0, 500) < (enemy_likelihood + (total_distance // 5000)) // 5 and total_distance > 25000:
        enemy.append(Enemy(2))
    
    for e in enemy:
        e.update()
        e.draw(screen)
        if e.health <= 0:
            enemy.remove(e)
            continue
        if collision_detection(e, player):
            player.health -= 1
            enemy.remove(e)

    # Player Update
    player.update(step_clouds)
    player.draw(screen)

    if player.health == 0:
        defeated = True

    # Fireball Update
    for f in player.fireballs:
        f.update()
        f.draw(screen)
        for e in enemy:
            if collision_detection(f, e):
                e.health -= 1
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
                e.health -= 1
                if player.arcane_magic.__contains__(a):
                    player.arcane_magic.remove(a)

        if a.position[0] > screen.get_width() and player.arcane_magic.__contains__(a):
                player.arcane_magic.remove(a)

    # Holy Update
    for h in player.holy:
        h.update()
        h.draw(screen)
        for e in enemy:
            if collision_detection(h, e):
                e.health -= 1
                h.health -= 1

        if h.position[0] > screen.get_width() and player.holy.__contains__(h):
                player.holy.remove(h)
        
        if h.health <= 0 and player.holy.__contains__(h):
            player.holy.remove(h)

    pygame.display.update()

pygame.quit()
