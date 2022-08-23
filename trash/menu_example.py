# Код

import pygame

pygame.init()

size = (800, 600)
screen = pygame.display.set_mode(size)

FONT = pygame.font.SysFont('arial', 50)


class Menu:
    def __init__(self, x=100, y=100, option_y_padding=75): 
        options_base = {
            'START':1, 
            'QUIT':2
        }
        self.options = [] # опции выбора меню 
        self.callbacks = []  # значения, которые будут возвращены при нажатии кнопки
        self.current_option_index = 0 # индекс пункта меню, который сейчас выбран
        self.x = x
        self.y = y
        self.option_y_padding = option_y_padding
        for opt in options_base.items():
            self.options.append(FONT.render(opt[0], True, (255, 255, 255)))
            self.callbacks.append(opt[1])

    def switch(self, direction):
        self.current_option_index = max(0, min(self.current_option_index + direction, len(self.options) - 1))

    def select(self):
        print(self.callbacks[self.current_option_index])

    def draw(self, surf, x, y, option_y_padding):
        for i, option in enumerate(self.options):
            option_rect: pygame.Rect = option.get_rect()
            option_rect.topleft = (x, y + i * option_y_padding)
            if i == self.current_option_index:
                pygame.draw.rect(surf, (0, 100, 0), option_rect)
            surf.blit(option, option_rect)


running = True


def quit_game():
    global running
    running = False


menu = Menu()

while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            quit_game()
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_w:
                menu.switch(-1)
            elif e.key == pygame.K_s:
                menu.switch(1)
            elif e.key == pygame.K_RETURN:
                menu.select()

    screen.fill((0, 0, 0))

    menu.draw(screen, 100, 100, 75)

    pygame.display.flip()