import pygame
import GlobalVariables as gv
from GamePlay import GameInstance
import NonPlayerClasses as npc

class MainMenu:
    def __init__(self):
        self.font = pygame.font.SysFont('arial', 80)
        self.title = self.font.render("Wizards Defense", True, (255, 255, 255))
        self.title_position = ((gv.screen.get_width() - self.title.get_width()) // 2, (gv.screen.get_height() - self.title.get_height()) // 2.5)
        self.begin_text = self.font.render("Press SPACE to start", True, (255, 255, 255))
        self.begin_text_position = ((gv.screen.get_width() - self.begin_text.get_width()) // 2, (gv.screen.get_height() - self.begin_text.get_height()) // 1.75)
        self.clouds = gv.clouds
        self.background = npc.Background()

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return GameInstance()

        for c in self.clouds:
            c.update()

        self.background.update(gv.world_advance, gv.total_distance)

        return self

    def draw(self, screen):
        
        self.background.draw(gv.screen)

        screen.blit(self.title, self.title_position)

        screen.blit(self.begin_text, self.begin_text_position)

        for c in self.clouds:
            c.draw(gv.screen)

    def run(self):
        self.update(gv.screen)
        self.draw()
