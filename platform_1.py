import pygame
import math

# Initialize
pygame.init()
screen = pygame.display.set_mode((1200, 800))
pygame.display.set_caption('Platform')
clock = pygame.time.Clock()
game_floor = screen.get_height() - 200

# Global Variables
game_over = False

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
        self.jump_height = 250
        self.speed = 3
        self.jumping_speed = 15

    def draw(self, screen):
        if self.forward == False:
            screen.blit(self.image_flipped, self.position)
        else:
            screen.blit(self.image, self.position)

    def update(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_RIGHT]:
            self.forward = True
            self.position[0] += self.speed
        if key_pressed[pygame.K_LEFT]:
            self.forward = False
            self.position[0] -= self.speed
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

# Functions

# Global Variables
player = Player([200, game_floor])

# Game Loop
while not game_over:

    clock.tick(60)

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            game_over = True

    pygame.draw.rect(screen, (0, 0, 0), [0, 0, screen.get_width(), screen.get_height()])

    # Player Update
    player.update()
    player.draw(screen)

    pygame.display.update()

pygame.quit()
