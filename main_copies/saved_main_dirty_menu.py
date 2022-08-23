import pygame
import random

pygame.init()



window_height = pygame.display.get_desktop_sizes()[0][1] # 864 
window_width = pygame.display.get_desktop_sizes()[0][0] # 1536
win = pygame.display.set_mode((window_width, window_height), pygame.FULLSCREEN)

pygame.display.set_caption("SPACE INVADERS")
clock = pygame.time.Clock()

# КОЛ-ВО КАРТИНОК ДОЛЖНО БЫТЬ ДЕЛИТЕЛЕМ 60-ТИ !!!!

FONT = pygame.font.Font(None, 40)

def debug_information(win, information):
    """ Вывод информации для дебагинга """
    global FONT
    y = 0
    for pair in information.items():
        line = '{} = {}'.format(pair[0], pair[1])
        text = FONT.render(line, True, (255, 0, 0))
        win.blit(text, (0, y))
        y += 35





class Abstract_object():
    count_frames = 0
    how_many_objects = 0
    
    window_height = pygame.display.get_desktop_sizes()[0][1] # 864 1080
    window_width = pygame.display.get_desktop_sizes()[0][0] # 1536 1920

    def __init__(self, x, y, height, width, health, frames_paths):
        Abstract_object.how_many_objects += 1   
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.health = health
        self.frames_paths = frames_paths # массив с путями к файлам анимации
        self.animation = [] # кадры анимации (load)
        for sprite in self.frames_paths:
            self.animation.append(pygame.image.load(sprite))
    
    @classmethod
    def get_objects_count(cls):
        return cls.how_many_objects

    def draw_hitbox(self, win):
        red = (255,0,0)
        pygame.draw.rect(win, red, (self.x, self.y, self.height, self.width),2) 
    
    def draw(self, win):
        if Abstract_object.count_frames >= 60:
            Abstract_object.count_frames = 0
        
        if len(self.animation) > 0:
            win.blit(self.animation[Abstract_object.count_frames//(60//len(self.animation))], (self.x, self.y))
        else:
            self.draw_hitbox(win)

class Player(Abstract_object):
    """ Класс игрока - (x, y, height, width, health, pic) """
    def __init__(self, x, y, height, width, health, frames_paths):
        super().__init__(x, y, height, width, health, frames_paths)
        self.speed = 4

class Picture():
    ''' Класс картинок. '''
    def __init__(self, path, y=0):
        self.y = y
        self.path = path
        self.bg_image = pygame.image.load(self.path) # full_bg.jpg back_ground.png bg_1536_864.jpg
    
    def move(self,win): 
        '''Для картинок заднего фона.'''
        if self.y > Abstract_object.window_height:
            self.y = -Abstract_object.window_height
        self.y += 1
        win.blit(self.bg_image, (0, self.y))

class Asteroid(Abstract_object): # Asteroid_field
    all_asteroids = []
    def __init__(self, type):
        Abstract_object.how_many_objects += 1 # для подсчета общего кол-ва сущностей
        self.x = random.randint(0, Abstract_object.window_width) 
        self.y = random.randint(-1400, -100) 
        self.type = str(type)
        self.speed = random.uniform(2,5)
        self.__type_init()
    
    @staticmethod
    def make_n_asteroids(count):
        for asteroid in range(count):
            Asteroid.all_asteroids.append(Asteroid(random.randint(1,4)))
    
    def draw(self, win):
        self.y += self.speed 
        super().draw(win)

    
    def __type_init(self):
        sprite = {
            '1': [['asteroids/asteroid_60.png'], 60],
            '2': [['asteroids/asteroid_80.png'], 80],
            '3': [['asteroids/asteroid_85.png'], 85],
            '4': [['asteroids/asteroid_100.png'], 100]
            }
        
        self.height = sprite[self.type][1] 
        self.width = sprite[self.type][1]
        self.animation = [] # кадры анимации (load)
        sprites = sprite[self.type][0]

        for sprt in sprites:
            self.animation.append(pygame.image.load(sprt))



def quit_game():
    SPACE_IVADERS.MENU_RUN = False
    SPACE_IVADERS.GAME_RUN = False

def quit_menu():
    SPACE_IVADERS.MENU_RUN = False
    SPACE_IVADERS.GAME_RUN = True



class Menu:
    def __init__(self, x=100, y=100, option_y_padding=75): 
        optionss = {
            'START':1, 
            'QUIT':2
        }
        self.options = [] # опции выбора меню 
        self.callbacks = []  # список функций, которые привязаны к меню
        self.current_option_index = 0 # индекс пункта меню, который сейчас выбран
        self.x = x
        self.y = y
        self.option_y_padding = option_y_padding

    def append_option(self, option, callback):
        self.options.append(FONT.render(option, True, (255, 255, 255)))
        self.callbacks.append(callback)

    def switch(self, direction):
        self.current_option_index = max(0, min(self.current_option_index + direction, len(self.options) - 1))

    def select(self):
        self.callbacks[self.current_option_index]()

    def draw(self, surf):
        win.fill((0, 0, 0))
        for i, option in enumerate(self.options):
            option_rect: pygame.Rect = option.get_rect()
            option_rect.topleft = (self.x, self.y + i * self.option_y_padding)
            if i == self.current_option_index:
                pygame.draw.rect(surf, (0, 100, 0), option_rect)
            surf.blit(option, option_rect)




# Игрок
frms = ['ship/space_ship_1.png', 'ship/space_ship_2.png', 'ship/space_ship_3.png', 'ship/space_ship_4.png']
player = Player(700,750,80,80,1000,frms )


# объекты
#player2 = Abstract_object(500,590,50,130,1000,[])
bg_image_1 = Picture('bg/bg_1920_1080.png',0) 
bg_image_2 = Picture('bg/bg_1920_1080.png',-window_height-1) 
Asteroid.make_n_asteroids(40)

# общие переменные
asteroids = Asteroid.all_asteroids

class Game():
    def __init__(self):
        self.DEBUG = 0
        self.GAME_RUN = True
        self.MENU_RUN = True
        self.draw_pool = [
            player,
        ]
        

    def play(self):
        #### Задний фон ####
        win.fill((0,0,0)) # можно убрать 
        bg_image_1.move(win)
        bg_image_2.move(win)
        ####################

        Abstract_object.count_frames += 1

        # Отрисовка астеройдов
        for astr in asteroids:
            astr.draw(win)
            if astr.y > window_height: # ушли за нижний край экрана
                astr.x = random.randint(0, Abstract_object.window_width) 
                astr.y = random.randint(-1400, -100) 
                #asteroids.pop(asteroids.index(astr))
            if self.DEBUG:
                astr.draw_hitbox(win)


        # Отрисовка всех объектов из пула 
        for obj in self.draw_pool:
            obj.draw(win)
            if self.DEBUG:
                obj.draw_hitbox(win)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.GAME_RUN = False
            # одиночные нажатия клавиш
            if event.type == pygame.KEYDOWN:
                if pygame.key.get_pressed()[pygame.K_F1]: # режим дебага
                    self.DEBUG = (self.DEBUG + 1) % 2

        keys = pygame.key.get_pressed()

        #### Управление игроком ####
        if keys[pygame.K_LEFT] and player.x > player.speed:
            player.x -= player.speed
        if keys[pygame.K_RIGHT] and player.x < window_width - player.width - player.speed:
            player.x += player.speed
        if keys[pygame.K_UP] and player.y > player.speed:
            player.y -= player.speed
        if keys[pygame.K_DOWN] and player.y < window_height - player.height - player.speed - 10:
            player.y += player.speed

        ############################
        if self.DEBUG:
            debug_information(win, {'x':player.x, 'y': player.y,'size': pygame.display.get_desktop_sizes(), 'entities': Abstract_object.get_objects_count()}) 

SPACE_IVADERS = Game()

MENU = Menu()
MENU.append_option('START', quit_menu)
MENU.append_option('QUIT', quit_game)


while SPACE_IVADERS.MENU_RUN:
    MENU.draw(win)
    for e in pygame.event.get():
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_UP:
                MENU.switch(-1)
            elif e.key == pygame.K_DOWN:
                MENU.switch(1)
            elif e.key == pygame.K_RETURN:
                MENU.select()
    pygame.display.update()


while SPACE_IVADERS.GAME_RUN: 
    clock.tick(60)
    SPACE_IVADERS.play()

    pygame.display.update()

    

pygame.quit()




## Полезности ##
#win.fill((0,0,0))
#print(pygame.display.get_desktop_sizes())