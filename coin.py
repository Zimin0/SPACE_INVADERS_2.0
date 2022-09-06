import pygame
import random
from abstract import Abstract_object


class Coin(Abstract_object):
    all_coins = []
    def __init__(self):
        self.width = self.height = 40
        super().__init__(
                        x=random.randint(0, Abstract_object.window_width-self.width), 
                        y=random.randint(-6400, -self.height), 
                        height=self.width,
                        width=self.height, 
                        health=None, 
                        frames_paths=['coin_40_40.png'])
        self.__value = 10
        self.speed = 2

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
        player.score += self.__value
        Coin.all_coins.pop(Coin.all_coins.index(self))
        





