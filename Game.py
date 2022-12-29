import GlobalVariables as gv
import pygame
from MainMenu import MainMenu

state = MainMenu()

pygame.init()

while not gv.game_over: 

    gv.clock.tick(60)

    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
                gv.game_over = True            

    state = state.update(events)
    state.draw(gv.screen)  
    
    pygame.display.update()

pygame.quit()