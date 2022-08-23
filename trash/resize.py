import cv2

def make_size_name(path, width, height):
    """Добавляет в имя картинки его размеры."""
    lst = path.split('.')
    new_path = "{}_{}_{}.{}".format(lst[0], str(width), str(height), lst[1])
    return new_path

def resize_image(path, width, height):
    """ Изменяет изображение в соответствии с размером экрана пользователя."""
    # проверка на существование таких файлов
    src = cv2.imread(path,  -1) 
    dsize = (width, height)
    output = cv2.resize(src, dsize)

    new_name = make_size_name(path, width, height)
    cv2.imwrite(new_name, output) 
    return new_name






