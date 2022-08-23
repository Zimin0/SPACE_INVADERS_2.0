import random
import pygame

from abstract import Abstract_object

class Asteroid(Abstract_object): 
    all_asteroids = []
    def __init__(self, type):
        self.type = str(type) 
        self.__type_init()
        super().__init__(
                        x=random.randint(0, Abstract_object.window_width), 
                        y=random.randint(-1400, -100), 
                        height=self.height, 
                        width=self.width, 
                        health=None, 
                        frames_paths=self.sprites
                        )
        self.speed = random.uniform(2,5) 
        self.damage_collision = 250 

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
        # почему не ресайз - при ресайзе очень сильно дергается изображение на последнем кадре
        __sprite_alive = {
            '1': [['asteroids/asteroid_60.png'], 60], 
            '2': [['asteroids/asteroid_80.png'], 80,],
            '3': [['asteroids/asteroid_85.png'], 85],
            '4': [['asteroids/asteroid_100.png'], 100]
            }
        
        self.height = __sprite_alive[self.type][1] 
        self.width = __sprite_alive[self.type][1]
        self.sprites = __sprite_alive[self.type][0]