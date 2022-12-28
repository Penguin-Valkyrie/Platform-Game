import pygame

import pygame

class MainMenu:
    def __init__(self):
        self.font = pygame.font.SysFont('arial', 80)
        self.title = self.font.render("Alian Invasion", True, (255, 255, 255))
        self.title_position = (10, 10)
        self.gameplay_scene = None
        self.clouds

    def update(self, events, screen):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return self.gameplay_scene
        return self

    def draw(self, screen):
        screen.blit(self.title, self.title_position)