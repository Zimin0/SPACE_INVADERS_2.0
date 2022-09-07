import pygame
import random
import sys

pygame.init()

from player import Player
from asteroid import Asteroid
from picture import Picture
from abstract import Abstract_object        
from coin import Coin
from Data import Data
#from text import Text


#######################################################################################################
# 1)  
# 2) 
# 3) 
# 4) Добавить планеты на задний фон 1534
# 5) переделать названия с _ на fF
# 6) вращение метеоритов # много проблем
# 7) добавить ресайз на все картинки  
# 8) 
# 9) Функция для создания шрифта
# 10) добавть генерацию астеройдов на некоторое время одной функцией
#
#######################################################################################################
      
# КОЛ-ВО КАРТИНОК ДОЛЖНО БЫТЬ ДЕЛИТЕЛЕМ 60-ТИ !!!!





class Game():
    __Debug_info = {}

    ###################### Дебаг режим ######################
    @staticmethod
    def print_debug_info(win):
        """ Вывод информации для дебагинга """
        y = 0 
        for pair in Game.__Debug_info.items():
            line = '{} = {}'.format(pair[0], pair[1])
            text = Data.FONT_20.render(line, True, (255, 0, 0))
            win.blit(text, (0, y))
            y += 35

    @staticmethod
    def add_debug_info(information):
        for pair in information.items(): 
            Game.__Debug_info[pair[0]] = pair[1]
    #########################################################

    def play(self):
        ####################### Предзагрузка #######################
        GAME_RUN = True
        DEBUG = 0 
        #frms = ['ship/space_ship_1.png', 'ship/space_ship_2.png', 'ship/space_ship_3.png', 'ship/space_ship_4.png']
        #-------------- Резайз ВСЕХ картинок --------------#

        bg_image_1 = Picture(
                            path=Data.bg_image, 
                            window_w=Data.window_width, 
                            window_h=Data.window_height, 
                            DATA_name='window', 
                            y=0) 

        bg_image_2 = Picture(
                            path=Data.bg_image, 
                            window_w=Data.window_width, 
                            window_h=Data.window_height, 
                            DATA_name='window', 
                            y=-Data.window_height-1)  
        
        hero = Player(
                     x=Data.window_width//2, 
                     y=750, 
                     height=Data.Hit_Boxes['player'][0], 
                     width=Data.Hit_Boxes['player'][1], 
                     health=1000, 
                     frames_paths=Data.hero_images) 

        #Hero_stats = Text(
        #                ['HEALTH: {}'.format(hero.health),
        #                'SCORE: {}'.format(hero.score) ],
        #                game.window_height-200,
        #                10)

        draw_pool = [
            hero,
        ]

        def time():
            Data.clock.tick(Data.FPS)
            Data.count_frames += 1
            if Data.count_frames >= Data.FPS: # заменить делением по модулю
                Data.count_frames = 0
        
       ############################################################
        while GAME_RUN:
            pygame.display.update() 
            time()

            #### Задний фон ####
            bg_image_1.move(Data.win, Data.window_height)
            bg_image_2.move(Data.win, Data.window_height)
            ####################

            ############### Отрисовка астеройдов ###############
            for astr in Asteroid.all_asteroids:
                astr.draw(Data.win, Data.count_frames)
                astr.infinity_appearance()
                if Abstract_object.check_collusion(Data.win, astr, hero, DEBUG):
                    hero.hit(astr)
                if DEBUG:
                    astr.draw_hitbox(Data.win)
            ####################################################

            #Hero_stats.draw(Game.win)

            ################# Отрисовка монет ##################
            for coin in Coin.all_coins:
                coin.draw(Data.win, Data.count_frames)
                coin.infinity_appearance() 
                if Abstract_object.check_collusion(Data.win, coin, hero, DEBUG): # поменять порядок
                    coin.collect(hero)
                if DEBUG:
                    coin.draw_hitbox(Data.win)
            ####################################################
            if hero.is_dead():
                GAME_RUN = False
            ################ Отрисовка всех объектов из пула ###############
            for obj in draw_pool:
                obj.draw(Data.win, Data.count_frames)
                if DEBUG:
                    obj.draw_hitbox(Data.win)
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
                            Menu.pauseScreen(Data.win)
                            Menu('Пауза')
                            

            keys = pygame.key.get_pressed()
            
            ############ Управление игроком ############ 
            if keys[pygame.K_LEFT] and hero.x > hero.speed:
                hero.x -= hero.speed
            if keys[pygame.K_RIGHT] and hero.x < Data.window_width - hero.width - hero.speed:
                hero.x += hero.speed
            if keys[pygame.K_UP] and hero.y > hero.speed:
                hero.y -= hero.speed
            if keys[pygame.K_DOWN] and hero.y < Data.window_height - hero.height - hero.speed - 10:
                hero.y += hero.speed
            ############################################

            if DEBUG:
                Game.add_debug_info({
                                    'x':hero.x, 
                                    'y': hero.y,
                                    'size': pygame.display.get_desktop_sizes(), 
                                    'bg1':bg_image_1.y, 
                                    'bg2': bg_image_2.y,
                                    'obj':Abstract_object.all_objects,
                                    "HEALTH":hero.health, 
                                    "SCORE":hero.score })
                
                Game.print_debug_info(Data.win)

    def end_game(self):
        Coin.all_coins.clear()
        Asteroid.all_asteroids.clear()



class Menu():
    Yellow = [254,192,0]
    Orange = [255,77,0]
    FONT_40 = pygame.font.Font(None, 40)
    FONT_90 = pygame.font.Font(None, 90)
    FONT_150 = pygame.font.Font(None, 150)

    window_height = pygame.display.get_desktop_sizes()[0][1] # 864 1080
    window_width = pygame.display.get_desktop_sizes()[0][0] # 1536 1920


    def __init__(self, text): # bg_start.jpg
        pygame.draw.rect(Data.win, Menu.Orange, (Menu.window_width/2-Menu.window_width/3.2, Menu.window_height/2-Menu.window_height/2.35, 1200, 200),10) 
        b1 = Picture(
            path='bg/62ec476ce5cbd.jpg', 
            window_w=Data.window_width, 
            window_h=Data.window_height, 
            DATA_name='window')
        Data.win.blit(b1.image,(0,0))


        t0 = Data.FONT_150.render('SPACE INVADERS 2.0', True, Menu.Yellow)
        t0_rect = t0.get_rect(center=(Menu.window_width/2, Menu.window_height/2-Menu.window_height/3))
        Data.win.blit(t0, t0_rect)
    
        t1 = Data.FONT_90.render(text, True, Menu.Yellow)
        t1_rect = t1.get_rect(center=(Menu.window_width/2, Menu.window_height/2))
        Data.win.blit(t1, t1_rect)
    
        t2 = Data.FONT_40.render('Нажмите любую клавишу для продолжения...', True, Menu.Yellow)
        t2_rect = t2.get_rect(center=(Menu.window_width/2, Menu.window_height/2+Menu.window_height/3))
        Data.win.blit(t2, t2_rect)

        while self.__checkKeys() == None:
            pygame.display.update()
            Data.clock.tick(Data.FPS)
    
    @staticmethod
    def pauseScreen(win):
        """Заливка экрана."""
        pause = pygame.Surface((Menu.window_width, Menu.window_height), pygame.SRCALPHA)   
        pause.fill(Menu.Yellow + [127]) # ((0, 221, 255, 127)               
        win.blit(pause, (0, 0)) 


    def __checkKeys(self):
        self.__quitGame() ##################################!!!!!!!!!!!!!!!! Зачем
        for event in pygame.event.get([pygame.KEYDOWN, pygame.KEYUP]):
            if event.type == pygame.KEYDOWN:
                continue
            return event.key
        return None
    
    def __quitGame(self):
        for event in pygame.event.get(pygame.QUIT): # проверка всех событий, приводящих к выходу из игры
            self.__stopGame() 
        for event in pygame.event.get(pygame.KEYUP): 
            if event.key == pygame.K_ESCAPE:
                self.__stopGame() 
            pygame.event.post(event) 

    def __stopGame(self):
        global SpaceInvaders
        SpaceInvaders.GAME_RUN = False


def main():
    pygame.init()
    pygame.display.set_caption("SPACE INVADERS")

    SpaceInvaders = Game()
    Menu('Стартуем!')
    
    while True:
        Asteroid.make_n_asteroids(30)
        Coin.make_n_coins(15)
        #pygame.time.set_timer(Game.add_debug_info({'time':True}),1000)
        SpaceInvaders.play()
        Menu('Конец игры!')
        SpaceInvaders.end_game()

if __name__ == '__main__':
    main()



#pygame.quit()

## Полезности ##
#win.fill((0,0,0))
#print(pygame.display.get_desktop_sizes())