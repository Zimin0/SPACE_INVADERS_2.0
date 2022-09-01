import pygame
pygame.init()

class Data():
    window_height = pygame.display.get_desktop_sizes()[0][1] 
    window_width = pygame.display.get_desktop_sizes()[0][0] 
    clock = pygame.time.Clock()
    win = pygame.display.set_mode((window_width, window_height), pygame.FULLSCREEN)
    FONT_20 = pygame.font.Font(None, 20)
    FONT_40 = pygame.font.Font(None, 40)
    FONT_90 = pygame.font.Font(None, 90)
    FONT_150 = pygame.font.Font(None, 150)

    FPS = 60
    count_frames = 0

    bg_image = 'bg/bg_1920_1080.png'
    coin_image = 'coin_orig_40_40.png'
    menu_image = 'bg/62ec476ce5cbd.jpg'
    hero_images = [
                    'ship/space_ship_1.png', 
                    'ship/space_ship_2.png', 
                    'ship/space_ship_3.png', 
                    'ship/space_ship_4.png']
    asteroid_images = [
                    'asteroids/asteroid_60.png',
                    'asteroids/asteroid_80.png',
                    'asteroids/asteroid_85.png',
                    'asteroids/asteroid_100.png']
    

