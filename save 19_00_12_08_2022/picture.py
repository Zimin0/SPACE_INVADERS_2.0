import pygame

class Picture():
    ''' Класс картинок. '''
    def __init__(self, path, y=0):
        self.y = y
        self.path = path
        self.bg_image = pygame.image.load(self.path) # full_bg.jpg back_ground.png bg_1536_864.jpg
    
    
    def move(self, win, window_height): 
        '''Для картинок заднего фона.'''
        if self.y > window_height:
            self.y = -window_height
        self.y += 1
        win.blit(self.bg_image, (0, self.y)) # вынести в отдельный draw 