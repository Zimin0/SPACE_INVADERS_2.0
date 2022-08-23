#import pygame
#
#class Text():
#    # создать массив надписей и прогружать его 
#    # передавать словарь с значениями и функцией draw его обновлять 
#    """ Text - массив строк. """
#    Yellow = [254,192,0]
#    Orange = [255,77,0]
#    font = pygame.font.Font(None, 60)
#    def __init__(self, text, x, y):
#        self.text = text
#        self.x = x
#        self.y = y
#        rendered_lines = []
#        for line in self.text:
#            r_line = Text.font.render(line, True, Text.Yellow)
#            rendered_lines.append(r_line)
#    
#    def reload_info(self):
#        ...
#        
#    
#    def draw(self, win, ):
#        #__t0 = Game.FONT_150.render('SPACE INVADERS 2.0', True, Menu.Yellow)
#        #__t0_rect = __t0.get_rect(center=(Menu.window_width/2, Menu.window_height/2-Menu.window_height/3))
#        #Game.win.blit(__t0, __t0_rect)
#        y = 0
#        for line in self.text:
#            win.blit(rendered_text, (1200, self.y+y))
#            y += 50
#    