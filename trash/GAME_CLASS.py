import pygame

pygame.init()

class Game():
    def __init__(self):
        self.window_height = pygame.display.get_desktop_sizes()[0][1] 
        self.window_width = pygame.display.get_desktop_sizes()[0][0] 
        self.win = pygame.display.set_mode((self.window_width, self.window_height), pygame.FULLSCREEN)
    @staticmethod
    def menu():
        return ...



def main():
    run = True
    while run:
        val = Game.menu()
        if val == 1:
            run = False
        else:
            space_invaders = Game()
            space_invaders.play()

    pygame.quit()

