import pygame
import cv2
pygame.init()

class Data():
    window_height = pygame.display.get_desktop_sizes()[0][1] 
    window_width = pygame.display.get_desktop_sizes()[0][0] 
    clock = pygame.time.Clock()
    win = pygame.display.set_mode((window_width, window_height), pygame.FULLSCREEN)
    FONT_20 = pygame.font.Font(None, 20)
    FONT_40 = pygame.font.Font(None, 40)
    FONT_90 = pygame.font.Font(None, 90)
    FONT_150 = pygame.font.Font(None, 150)
    FONT_180 = pygame.font.Font(None, 200)

    FPS = 60
    count_frames = 0

    bg_image = 'bg/bg_1920_1080.png'
    coin_image = 'coin_orig_40_40.png'
    menu_image = 'bg/62ec476ce5cbd.jpg'
    hero_images = [
                    'ship/space_ship_1.png', 
                    'ship/space_ship_2.png', 
                    'ship/space_ship_3.png', 
                    'ship/space_ship_4.png']
    
    asteroid_images = [
                    'asteroids/asteroid_60.png',
                    'asteroids/asteroid_80.png',
                    'asteroids/asteroid_85.png',
                    'asteroids/asteroid_100.png']

    
    Hit_Boxes = {
        'window': (1920,1080),
        'player': (80, 80),
        'coin': (40, 40),
        'asteroid_1': (60, 60),
        'asteroid_2': (80, 80),
        'asteroid_3': (85, 85),
        'asteroid_4': (100, 100)
    }

    def __init__(self):
        # Грязно !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1 # 
        self.resize_image( Data.bg_image,'window')
        self.resize_image( Data.coin_image, 'coin')
        self.resize_image( Data.menu_image,'window')
        self.resize_image( Data.hero_images[0], 'player')
        self.resize_image( Data.hero_images[1], 'player')
        self.resize_image( Data.hero_images[2], 'player')
        self.resize_image( Data.hero_images[3], 'player')
        self.resize_image( Data.hero_images[3], 'player')
        self.resize_image( Data.asteroid_images[0], 'asteroid_1')
        self.resize_image( Data.asteroid_images[1], 'asteroid_2')
        self.resize_image( Data.asteroid_images[2], 'asteroid_3')
        self.resize_image( Data.asteroid_images[3], 'asteroid_4')

        

    

    def __claculate_size(self, DATA_name, window_w, window_h, DATA):
        """ POSSIBLE LAGS !!!"""
        if DATA_name == 'window':
            return window_w, window_h

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

    def resize_image(self, path, DATA_name):
        """ Изменяет изображение в соответствии с размером экрана пользователя."""
        # сделать проверку на существование таких файлов
        width, height = self.__claculate_size(DATA_name, window_w=Data.window_width, window_h=Data.window_height, Data=Data.Hit_Boxes)
        src = cv2.imread(path,  -1) 
        dsize = (width, height)
        output = cv2.resize(src, dsize)

        new_name = self.__make_size_name(path, width, height)
        cv2.imwrite(new_name, output) 
        return new_name
    
obj1 = Data()



