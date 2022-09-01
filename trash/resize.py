import cv2

def __make_size_name(path, width, height):
    """Добавляет в имя картинки его размеры."""
    lst = path.split('.')
    new_path = "{}_{}_{}.{}".format(lst[0], str(width), str(height), lst[1])
    return new_path

def resize_image(path, width, height):
    """ Изменяет изображение в соответствии с размером экрана пользователя."""
    # сделать проверку на существование таких файлов
    src = cv2.imread(path,  -1) 
    dsize = (width, height)
    output = cv2.resize(src, dsize)

    new_name = __make_size_name(path, width, height)
    cv2.imwrite(new_name, output) 
    return new_name

DATA = {
    'window': (1920,1080),
    'player': (80, 80),
    'coin': (40, 40),
    'asteroid_1': (60, 60),
    'asteroid_2': (80, 80),
    'asteroid_3': (85, 85),
    'asteroid_4': (100, 100)
}

coefficients = []

def claculate_size():




resize_image('coin_orig.png', 40, 40)



