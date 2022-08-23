import pygame

class Abstract_object():
    def __init__(self, x, y, height, width, health, frames_paths):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.health = health
        self.frames_paths = frames_paths # массив с путями к файлам анимации
        self.animation = [] # кадры анимации (load)
        self.die_animation = [] # кадры анимации смерти 
        for sprite in self.frames_paths:
            self.animation.append(pygame.image.load(sprite))
            
    def __draw_animation(self, win, animation_frames, count_frames):
        """ Отрисовывает анимацию по кадрам из animation_frames."""
        win.blit(animation_frames[count_frames//(60//len(animation_frames))], (self.x, self.y))

    
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
    