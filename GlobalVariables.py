import pygame

pygame.init()

screen = pygame.display.set_mode((1200, 800))
pygame.display.set_caption('Platform')
clock = pygame.time.Clock()

game_over = False
cloud_images = [
    pygame.image.load('images/cloud1.png'),
    pygame.image.load('images/cloud2.png'),
    pygame.image.load('images/cloud3.png')
]
game_floor = screen.get_height() - 100 # Image positions are set so their bottom is on the game_floor
total_distance = 0
font = pygame.font.SysFont('Arial', 48)
enemy_likelihood = 60 #if random.randint(0, 10000) < enemy_likelihood
coin_likelihood = 40 #if random.randint(0, 10000) < coin_likelihood
platform_likelihood = 10 #if random.randint(0, 10000) < platform_likelihood
cloud_likelihood = 30 #if random.randint(0, 10000) < cloud_likelihood
defeated = False
defeat_message = font.render("Defeated!", True, (255, 255, 255))
world_advance = 0