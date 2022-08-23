import random
import pygame

from abstract import Abstract_object

class Asteroid(Abstract_object): 
    all_asteroids = []
    window_width = 1536 #pygame.display.get_desktop_sizes()[0][0] # 1536 1920 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1

    def __init__(self, type):
        self.x = random.randint(0, Asteroid.window_width) 
        self.y = random.randint(-1400, -100) 
        self.speed = random.uniform(2,5)
        self.type = str(type)
        self.damage_collision = 250
        self.__type_init()

    def die(self):
        Asteroid.all_asteroids.pop(Asteroid.all_asteroids.index(self))
        ## add animation ##

    
    @staticmethod
    def make_n_asteroids(count):
        """ Generate asteroid field. """
        for asteroid in range(count):
            obj = Asteroid(random.randint(1,4))
            Asteroid.all_asteroids.append(obj)
            
    
    def draw(self, win, count_frames):
        self.y += self.speed 
        super().draw(win, count_frames)
    
    def __type_init(self):
        sprite_alive = {
            '1': [['asteroids/asteroid_60.png'], 60], 
            '2': [['asteroids/asteroid_80.png'], 80,],
            '3': [['asteroids/asteroid_85.png'], 85],
            '4': [['asteroids/asteroid_100.png'], 100]
            }
        
        self.height = sprite_alive[self.type][1] 
        self.width = sprite_alive[self.type][1]
        self.animation = [] # кадры анимации (load)
        sprites = sprite_alive[self.type][0]

        for sprt in sprites:
            self.animation.append(pygame.image.load(sprt))