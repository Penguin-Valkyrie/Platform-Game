import pygame
import random
import GlobalVariables as gv
from pygame import Vector2
from Player import Player
import CollisionDetection

# Initialize
pygame.init()

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
        self.position[0] -= self.speed + world_advance
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
        self.position[0] -= self.speed + world_advance

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
        self.position[0] -= world_advance

    def draw(self, screen):
        screen.blit(self.image, (self.position[0], self.position[1]))  

# Global Variables
player = Player()
enemy = []
enemy.append(Enemy(0, gv.screen))
clouds = []
clouds.append(Cloud(gv.screen))
step_clouds = []
step_clouds.append(Step_Cloud(gv.screen))
background = Background()
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
                player.fireballs.append(Fireball(Vector2(player.position), player))
            
            elif e.key == pygame.K_d and player.attack_buffer <= 0:
                player.arcane_magic.append(Arcane_Magic(Vector2(player.position), player, True))
                player.arcane_magic.append(Arcane_Magic(Vector2(player.position), player, False))
                player.attack_buffer = 240

            elif e.key == pygame.K_s and player.attack_buffer <= 0:
                player.holy.append(Holy(Vector2(player.position), player))
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
        clouds.append(Cloud(gv.screen))
    for c in clouds:
        c.update()
        c.draw(gv.screen)
        if c.position[0] < 0 - c.scaled_image.get_width():
            clouds.remove(c)
    
    # Platform Update
    if random.randint(0, 10000) < gv.platform_likelihood:
        step_clouds.append(Step_Cloud(gv.screen))
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
        coins.append(Coin(gv.screen, player))

    for c in coins:
        c.update()
        c.draw(gv.screen)
        if CollisionDetection.collision_detection(player, c, 2, None, False, player.collision_buffer, c.collision_buffer):
            coins.remove(c)
            player.coins_collected += 1

    # Enemy Update
    if random.randint(0, 10000) < gv.enemy_likelihood + (gv.total_distance // 5000):
        enemy.append(Enemy(0, gv.screen))
    elif random.randint(0, 10000) < (gv.enemy_likelihood + (gv.total_distance // 5000)) // 2 and gv.total_distance > 10000:
        enemy.append(Enemy(1, gv.screen))
    elif random.randint(0, 10000) < (gv.enemy_likelihood + (gv.total_distance // 5000)) // 5 and gv.total_distance > 25000:
        enemy.append(Enemy(2, gv.screen))
    
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
