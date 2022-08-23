from abstract import Abstract_object

class Player(Abstract_object):
    """ Класс игрока - (x, y, height, width, health, pic) """
    def __init__(self, x, y, height, width, health, frames_paths):
        super().__init__(x, y, height, width, health, frames_paths)
        self.speed = 4 
        self.score = 0

    def hit(self, link):
        self.health -= link.damage_collision
        link.die()
        # __del__

