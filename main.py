import pygame
import random
import sys

pygame.init()

from player import Player
from asteroid import Asteroid
from picture import Picture
from abstract import Abstract_object        
from coin import Coin
#from text import Text


#######################################################################################################
# 1) 
# 2) 
# 3) 
# 4) Добавить планеты на задний фон 1534
# 5) переделать названия с _ на fF
# 6) вращение метеоритов # много проблем
# 7) убрать ресайз вообще 
# 8) 
# 9) Функция для создания шрифта
# 10) добавть генерацию астеройдов на некоторое время одной функцией
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
    FONT_40 = pygame.font.Font(None, 40)
    FONT_90 = pygame.font.Font(None, 90)
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
        
        hero = Player(x=Game.window_width//2, 
                      y=750, 
                      height=80, 
                      width=80, 
                      health=1000, 
                      frames_paths=frms) 

        #Hero_stats = Text(
        #                ['HEALTH: {}'.format(hero.health),
        #                'SCORE: {}'.format(hero.score) ],
        #                Game.window_height-200,
        #                10)

        draw_pool = [
            hero,
        ]
       
        while GAME_RUN:
            pygame.display.update() 
            Game.clock.tick(Game.FPS)
            Game.count_frames += 1

            if Game.count_frames >= Game.FPS: # заменить делением по модулю
                Game.count_frames = 0

            #### Задний фон ####
            bg_image_1.move(Game.win, Game.window_height)
            bg_image_2.move(Game.win, Game.window_height)
            ####################

            ############### Отрисовка астеройдов ###############
            for astr in Asteroid.all_asteroids:
                """ для монеток и астеройдов нужно вызвать 
                1) draw
                2) infinity_appearance
                3) check_collusion
                4) aster - hit, coin - collect
                """
                astr.draw(Game.win, Game.count_frames)
                astr.infinity_appearance(max_y=-1400)
                if Abstract_object.check_collusion(Game.win, astr, hero, DEBUG):
                    hero.hit(astr)
                if DEBUG:
                    Game.add_debug_info({"HEALTH":hero.health, "SCORE":hero.score})
                    astr.draw_hitbox(Game.win)
            ####################################################

            #Hero_stats.draw(Game.win)

            ################# Отрисовка монет ##################
            for coin in Coin.all_coins:
                coin.draw(Game.win, Game.count_frames)
                coin.infinity_appearance(max_y=-6400)
                if Abstract_object.check_collusion(Game.win, coin, hero, DEBUG): # поменять порядок
                    coin.collect(hero)
                if DEBUG:
                    coin.draw_hitbox(Game.win)
            ####################################################
            if hero.is_dead():
                GAME_RUN = False
            ################ Отрисовка всех объектов из пула ###############
            for obj in draw_pool:
                obj.draw(Game.win, Game.count_frames)
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
                            Menu.pauseScreen(Game.win)
                            Menu('Пауза')
                            

            keys = pygame.key.get_pressed()
            
            ############ Управление игроком ############ 
            if keys[pygame.K_LEFT] and hero.x > hero.speed:
                hero.x -= hero.speed
            if keys[pygame.K_RIGHT] and hero.x < Game.window_width - hero.width - hero.speed:
                hero.x += hero.speed
            if keys[pygame.K_UP] and hero.y > hero.speed:
                hero.y -= hero.speed
            if keys[pygame.K_DOWN] and hero.y < Game.window_height - hero.height - hero.speed - 10:
                hero.y += hero.speed
            ############################################

            if DEBUG:
                Game.add_debug_info({
                                    'x':hero.x, 
                                    'y': hero.y,
                                    'size': pygame.display.get_desktop_sizes(), 
                                    'bg1':bg_image_1.y, 
                                    'bg2': bg_image_2.y,
                                    'obj':Abstract_object.all_objects })
                Game.print_debug_info(Game.win)

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
        pygame.draw.rect(Game.win, Menu.Orange, (Menu.window_width/2-Menu.window_width/3.2, Menu.window_height/2-Menu.window_height/2.35, 1200, 200),10) 
        b1 = Picture('bg/62ec476ce5cbd.jpg',0) 
        Game.win.blit(b1.bg_image,(0,0))


        t0 = Game.FONT_150.render('SPACE INVADERS 2.0', True, Menu.Yellow)
        t0_rect = t0.get_rect(center=(Menu.window_width/2, Menu.window_height/2-Menu.window_height/3))
        Game.win.blit(t0, t0_rect)
    
        t1 = Game.FONT_90.render(text, True, Menu.Yellow)
        t1_rect = t1.get_rect(center=(Menu.window_width/2, Menu.window_height/2))
        Game.win.blit(t1, t1_rect)
    
        t2 = Game.FONT_40.render('Нажмите любую клавишу для продолжения...', True, Menu.Yellow)
        t2_rect = t2.get_rect(center=(Menu.window_width/2, Menu.window_height/2+Menu.window_height/3))
        Game.win.blit(t2, t2_rect)

        while self.__checkKeys() == None:
            pygame.display.update()
            Game.clock.tick(Game.FPS)
    
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
        Asteroid.make_n_asteroids(3)
        Coin.make_n_coins(30)
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