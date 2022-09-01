import pygame
import cv2


class Picture():
    ''' Класс картинок. '''
    
    DATA = {
        'window': (1920,1080),
        'player': (80, 80),
        'coin': (40, 40),
        'asteroid_1': (60, 60),
        'asteroid_2': (80, 80),
        'asteroid_3': (85, 85),
        'asteroid_4': (100, 100)
    }
    def __init__(self, path, window_w, window_h, DATA_name, x=0, y=0):
        self.x = x
        self.y = y
        self.path = path
        self.resize_image(self.path, window_w, window_h, DATA_name)
        self.image = pygame.image.load(self.path) # full_bg.jpg back_ground.png bg_1536_864.jpg
    
    
    def move(self, win, window_height): 
        '''Для картинок заднего фона.'''
        if self.y > window_height:
            self.y = -window_height
        self.y += 1
        self.draw(win)

    def draw(self, win, frames=None): 
        win.blit(self.image, (self.x, self.y))
    
    ###################### Ресайз картинок ######################
    def __claculate_size(self, window_w, window_h, DATA_name, DATA):
        """ POSSIBLE LAGS !!!"""
        x = DATA[DATA_name][0]
        y = DATA[DATA_name][1]
        coef_x = DATA['window'][0] * DATA['window'][1] / x
        coef_y = DATA['window'][0] * DATA['window'][1] / y

        new_x = window_w * window_h / coef_x
        new_y = window_w * window_h / coef_y

        return int(new_x), int(new_y)

    def __make_size_name(self, path, width, height):
        """Добавляет в имя картинки его размеры."""
        lst = path.split('.')
        new_path = "{}_{}_{}.{}".format(lst[0], str(width), str(height), lst[1])
        return new_path

    def resize_image(self, path, window_w, window_h, DATA_name):
        """ Изменяет изображение в соответствии с размером экрана пользователя."""
        # сделать проверку на существование таких файлов
        width, height = self.__claculate_size(window_w, window_h, DATA_name, Picture.DATA)
        src = cv2.imread(path,  -1) 
        dsize = (width, height)
        output = cv2.resize(src, dsize)

        new_name = self.__make_size_name(path, width, height)
        cv2.imwrite(new_name, output) 
        return new_name
    #############################################################