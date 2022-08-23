import pygame
import random
from abstract import Abstract_object
class Coin(Abstract_object):
    all_coins = []
    def __init__(self, x, y, height, width, health, frames_paths):
        window_width = pygame.display.get_desktop_sizes()[0][0] 
        super().__init__(
            x=random.randint(0, window_width),  
            y=random.randint(-5400, -100), 
            height=80, 
            width=80, 
            health=None, 
            frames_paths='coin_2.png')
            
        self.value = 10
        self.speed = 2
        # попробовать ресайзнуть остальное изображения 
        # добавить ресайз в abstract для всех объектов

        /self.a = []
        /self.a.append(pygame.image.load('coin_2.png')) 
        /self.animation = []
        /self.animation.append(pygame.transform.scale(self.a[0], (80, 80)))

    @staticmethod
    def make_n_coins(count):
        """ Generate n coins. """
        for coin in range(count):
            obj = Coin()
            Coin.all_coins.append(obj)

    def draw(self, win, count_frames):
        self.y += self.speed 
        super().draw(win, count_frames)
    
    def collect(self, player):
        player.score += self.value
        Coin.all_coins.pop(Coin.all_coins.index(self))
        





