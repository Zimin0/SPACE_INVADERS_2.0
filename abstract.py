import pygame
import random

class Abstract_object():
    all_objects = []
    window_height = pygame.display.get_desktop_sizes()[0][1] # 864 1080
    window_width = pygame.display.get_desktop_sizes()[0][0] # 1536 1920
    def __init__(self, x, y, height, width, health, frames_paths):
        Abstract_object.all_objects.append(self)
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.health = health
        self.__frames_paths = frames_paths # массив с путями к файлам анимации
        self.animation = [] # кадры анимации (load)
        for sprite in self.__frames_paths:
            orig_pic =  pygame.image.load(sprite)
            self.animation.append(orig_pic)
            
    def __draw_animation(self, win, animation_frames, count_frames):
        """ Отрисовывает анимацию по кадрам из animation_frames."""
        win.blit(animation_frames[count_frames//(60//len(animation_frames))], (self.x, self.y))
    
    def infinity_appearance(self, on=True):
        """ Объекты, уходя за нижний край экрана, будут перемещаться за верхний край экрана."""
        if on:
            if self.y > Abstract_object.window_height: # ушли за нижний край экрана
                self.x = random.randint(0, Abstract_object.window_width) 
                self.y = -100 #random.randint(max_y, -self.height)
    
    #def die(self, linl_to_obj, link):
    #    # Сделать die у абстракта, вызывать его параллельно с hit
    #    Asteroid.all_asteroids.pop(Asteroid.all_asteroids.index(astr))   
    @staticmethod
    def check_collusion(win, obj1, obj2, DEBUG):
        """ DANGEROUS!!! POSSIBLE LAGS THERE!!!!"""
        if obj1.y > -100:
            if (obj1.y < obj2.y + obj2.width) and (obj1.y + obj1.width > obj2.y):
                if (obj1.x + obj1.height > obj2.x) and (obj1.x < obj2.x + obj2.height):
                    if DEBUG:
                        font_30 = pygame.font.Font(None, 30) # вынести две эти строки, будет больше производительность
                        text = font_30.render('Столкновение!', True, (0, 255, 0))
                        win.blit(text, (300, 0))
                    return True

    def draw_hitbox(self, win):
        pygame.draw.rect(win, (255, 0, 0), (self.x, self.y, self.height, self.width),2) 
    
    def draw(self, win, count_frames):
        """ Отрисовка объекта (или если нет фреймов анимации - хитбокса) на поле."""
        if len(self.animation) > 0:
            self.__draw_animation(win, self.animation, count_frames)
        else:
            self.draw_hitbox(win)
    