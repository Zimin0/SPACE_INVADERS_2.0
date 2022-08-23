import pygame
import random
import sys

pygame.init()


#######################################################################################################
# 1) Красиво оформить меню
# 2) 
# 3) Раскидать в разные папки
# 4) Добавить планеты на задний фон 1534
# 5) переделать названия с _ на fF
# 6) 
# 7) Гугл диск
# 8) Нарулить инкапсуляцию
# 9) Функция для создания шрифта
#
#
#######################################################################################################


# КОЛ-ВО КАРТИНОК ДОЛЖНО БЫТЬ ДЕЛИТЕЛЕМ 60-ТИ !!!!





class Game():
    count_frames = 0
    window_height = pygame.display.get_desktop_sizes()[0][1] # 864 1080
    window_width = pygame.display.get_desktop_sizes()[0][0] # 1536 1920
    clock = pygame.time.Clock()
    FPS = 60
    win = pygame.display.set_mode((window_width, window_height), pygame.FULLSCREEN)
    FONT_20 = pygame.font.Font(None, 20)
    FONT_30 = pygame.font.Font(None, 30)
    FONT_40 = pygame.font.Font(None, 40)
    FONT_60 = pygame.font.Font(None, 60)
    FONT_90 = pygame.font.Font(None, 90)
    FONT_120 = pygame.font.Font(None, 120)
    FONT_150 = pygame.font.Font(None, 150)
    __Debug_info = {}

    @staticmethod
    def print_debug_info(win):
        """ Вывод информации для дебагинга """
        y = 0
        for pair in Game.__Debug_info.items():
            line = '{} = {}'.format(pair[0], pair[1])
            text = Game.FONT_20.render(line, True, (255, 0, 0))
            win.blit(text, (0, y))
            y += 35

    @staticmethod
    def add_debug_info(information):
        for pair in information.items(): 
            Game.__Debug_info[pair[0]] = pair[1]

    def play(self):
        GAME_RUN = True
        DEBUG = 0
        frms = ['ship/space_ship_1.png', 'ship/space_ship_2.png', 'ship/space_ship_3.png', 'ship/space_ship_4.png']
        bg_image_1 = Picture('bg/bg_{}_{}.png'.format(Game.window_width,Game.window_height),0) 
        bg_image_2 = Picture('bg/bg_{}_{}.png'.format(Game.window_width,Game.window_height),-Game.window_height-1) 
        hero = Player(x=Game.window_width//2, y=750, height=80, width=80, health=1000, frames_paths=frms) 
        draw_pool = [
            hero,
        ]
        while GAME_RUN:
            Game.clock.tick(Game.FPS)
            Game.count_frames += 1

            #### Задний фон ####
            Game.win.fill((0,0,0)) # можно убрать 
            bg_image_1.move(Game.win)
            bg_image_2.move(Game.win)
            ####################

            ############### Отрисовка астеройдов ###############
            for astr in Asteroid.all_asteroids:
                astr.draw(Game.win)
                if astr.y > Game.window_height: # ушли за нижний край экрана
                    astr.x = random.randint(0, Game.window_width) 
                    astr.y = random.randint(-1400, -100) 
                    #Asteroid.all_asteroids.pop(Asteroid.all_asteroids.index(astr))
                if Abstract_object.check_collusion(astr,hero,DEBUG):
                    hero.hit("ASTEROID", astr)
                if DEBUG:
                    Game.add_debug_info({"HEALTH":hero.health})
                    astr.draw_hitbox(Game.win)
                    Game.add_debug_info({'Объекты':Abstract_object.list_of_objects})
            ####################################################

            if hero.health <= 0:
                GAME_RUN = False

            ################ Отрисовка всех объектов из пула ###############
            for obj in draw_pool:
                obj.draw(Game.win)
                if DEBUG:
                    obj.draw_hitbox(Game.win)
            ################################################################

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # одиночные нажатия клавиш
                if event.type == pygame.KEYDOWN:
                    if pygame.key.get_pressed()[pygame.K_F1]: # режим дебага
                        DEBUG = (DEBUG + 1) % 2
                    if pygame.key.get_pressed()[pygame.K_0]:
                        GAME_RUN = False
                    if pygame.key.get_pressed()[pygame.K_1]:
                        hero.health -= 100
                if event.type == pygame.KEYUP:
                        if event.key == pygame.K_SPACE:
                            Menu.pauseScreen()
                            Menu('Пауза')
                            

            keys = pygame.key.get_pressed()
            
            #### Управление игроком #### 
            if keys[pygame.K_LEFT] and hero.x > hero.speed:
                hero.x -= hero.speed
            if keys[pygame.K_RIGHT] and hero.x < Game.window_width - hero.width - hero.speed:
                hero.x += hero.speed
            if keys[pygame.K_UP] and hero.y > hero.speed:
                hero.y -= hero.speed
            if keys[pygame.K_DOWN] and hero.y < Game.window_height - hero.height - hero.speed - 10:
                hero.y += hero.speed
            ############################

            if DEBUG:
                Game.add_debug_info({'x':hero.x, 'y': hero.y,'size': pygame.display.get_desktop_sizes(), 'entities': Abstract_object.get_objects_count()+len(Asteroid.all_asteroids), 'bg1':bg_image_1.y, 'bg2': bg_image_2.y})
                Game.print_debug_info(Game.win)

            pygame.display.update() 

    def end_game(self):
        Abstract_object.list_of_objects.clear()
        Asteroid.all_asteroids.clear()
            
class Abstract_object():
    list_of_objects = []

    def __init__(self, x, y, height, width, health, frames_paths):
        Abstract_object.list_of_objects.append(self)   
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
        return len(cls.list_of_objects)
    
    @staticmethod
    def check_collusion(obj1, obj2,DEBUG):
        if obj1.y > -100:
            if (obj1.y < obj2.y + obj2.width) and (obj1.y + obj1.width > obj2.y):
                if (obj1.x + obj1.height > obj2.x) and (obj1.x < obj2.x + obj2.height):
                    if DEBUG:
                        text = Game.FONT_30.render('Столкновение!', True, (0, 255, 0))
                        Game.win.blit(text, (300, 0))
                    return True

    def draw_hitbox(self, win):
        red = (255,0,0)
        pygame.draw.rect(win, red, (self.x, self.y, self.height, self.width),2) 
    
    def draw(self, win):
        if Game.count_frames >= 60:
            Game.count_frames = 0
        
        if len(self.animation) > 0:
            win.blit(self.animation[Game.count_frames//(60//len(self.animation))], (self.x, self.y))
        else:
            self.draw_hitbox(win)

class Player(Abstract_object):
    """ Класс игрока - (x, y, height, width, health, pic) """
    def __init__(self, x, y, height, width, health, frames_paths):
        super().__init__(x, y, height, width, health, frames_paths)
        self.speed = 4 

    def hit(self, obj_type, link):
        Abstract_object.list_of_objects.pop(Abstract_object.list_of_objects.index(link))
        self.health -= link.damage_collision
        if obj_type == 'ASTEROID':
            Asteroid.all_asteroids.pop(Asteroid.all_asteroids.index(link))

class Picture():
    ''' Класс картинок. '''
    def __init__(self, path, y=0):
        Abstract_object.list_of_objects.append(self)   
        self.y = y
        self.path = path
        self.bg_image = pygame.image.load(self.path) # full_bg.jpg back_ground.png bg_1536_864.jpg
    
    def draw(self):
        Game.win.blit(self.bg_image, (0, 0))
    
    def move(self,win): 
        '''Для картинок заднего фона.'''
        if self.y > Game.window_height:
            self.y = -Game.window_height
        self.y += 1
        win.blit(self.bg_image, (0, self.y))

class Asteroid(Abstract_object): 
    all_asteroids = []
    def __init__(self, type):
        self.x = random.randint(0, Game.window_width) 
        self.y = random.randint(-1400, -100) 
        self.type = str(type)
        self.speed = random.uniform(2,5)
        self.damage_collision = 250
        self.__type_init()
    
    @staticmethod
    def make_n_asteroids(count):
        """ Generate asteroid field. """
        for asteroid in range(count):
            obj = Asteroid(random.randint(1,4))
            Asteroid.all_asteroids.append(obj)
            Abstract_object.list_of_objects.append(obj)
            
    
    def draw(self, win):
        self.y += self.speed 
        super().draw(win)
    
    def __type_init(self):
        sprite = {
            '1': [['asteroids/asteroid_60.png'], 60], 
            '2': [['asteroids/asteroid_80.png'], 80,],
            '3': [['asteroids/asteroid_85.png'], 85],
            '4': [['asteroids/asteroid_100.png'], 100]
            }
        
        self.height = sprite[self.type][1] 
        self.width = sprite[self.type][1]
        self.animation = [] # кадры анимации (load)
        sprites = sprite[self.type][0]

        for sprt in sprites:
            self.animation.append(pygame.image.load(sprt))

class Menu():
    Yellow = [254,192,0]
    Orange = [255,77,0]

    def __init__(self, text): # bg_start.jpg
        pygame.draw.rect(Game.win, Menu.Orange, (Game.window_width/2-Game.window_width/3.2, Game.window_height/2-Game.window_height/2.35, 1200, 200),10) 
        b1 = Picture('bg/62ec476ce5cbd.jpg'.format(Game.window_width,Game.window_height),0) 
        b1.draw()

        t0 = Game.FONT_150.render('SPACE INVADERS 2.0', True, Menu.Yellow)
        t0_rect = t0.get_rect(center=(Game.window_width/2, Game.window_height/2-Game.window_height/3))
        Game.win.blit(t0, t0_rect)
    
        t1 = Game.FONT_90.render(text, True, Menu.Yellow)
        t1_rect = t1.get_rect(center=(Game.window_width/2, Game.window_height/2))
        Game.win.blit(t1, t1_rect)
    
        t2 = Game.FONT_40.render('Нажмите любую клавишу для продолжения...', True, Menu.Yellow)
        t2_rect = t2.get_rect(center=(Game.window_width/2, Game.window_height/2+Game.window_height/3))
        Game.win.blit(t2, t2_rect)

        while self.checkKeys() == None:
            pygame.display.update()
            Game.clock.tick(Game.FPS)
    
    @classmethod
    def pauseScreen(cls):
        """Заливка экрана"""
        pause = pygame.Surface((Game.window_width, Game.window_height), pygame.SRCALPHA)   
        pause.fill(Menu.Yellow + [127]) # ((0, 221, 255, 127)               
        Game.win.blit(pause, (0, 0)) 

    def checkKeys(self):
        self.quitGame() ##################################!!!!!!!!!!!!!!!! Зачем
        for event in pygame.event.get([pygame.KEYDOWN, pygame.KEYUP]):
            if event.type == pygame.KEYDOWN:
                continue
            return event.key
        return None
    
    def quitGame(self):
        for event in pygame.event.get(pygame.QUIT): # проверка всех событий, приводящих к выходу из игры
            self.stopGame() 
        for event in pygame.event.get(pygame.KEYUP): 
            if event.key == pygame.K_ESCAPE:
                self.stopGame() 
            pygame.event.post(event) 

    def stopGame(self):
        global SpaceInvaders
        SpaceInvaders.GAME_RUN = False


def main():
    pygame.init()
    pygame.display.set_caption("SPACE INVADERS")

    SpaceInvaders = Game()
    Menu('Стартуем!')
    
    while True:
        Asteroid.make_n_asteroids(30)
        SpaceInvaders.play()
        Menu('Конец игры!')
        SpaceInvaders.end_game()

if __name__ == '__main__':
    main()



#pygame.quit()

## Полезности ##
#win.fill((0,0,0))
#print(pygame.display.get_desktop_sizes())