import pygame
import pygame_menu
from game import start_game, show_best
from sqlite import reg_user

pygame.init()
'''Создаем окно заставки'''
surface = pygame.display.set_mode((460, 530))
bg_image = pygame.image.load("snake.jpg")
timer = pygame.time.Clock()


def start_game_button():
    name = user_name.get_value()
    password = user_pass.get_value()

    if reg_user(name, password):
        start_game(name)
    else:
        return

'''Создаем объект класса меню'''
menu = pygame_menu.Menu(
    title='Змейка',
    height=300,
    width=240,
    theme=pygame_menu.themes.THEME_GREEN
)
''' Настраиваем пункты меню'''
user_name = menu.add.text_input('Имя: ', default='User', maxchar=10)
user_pass = menu.add.text_input('Пароль: ', default='123', maxchar=10)
menu.add.button('Игра', start_game_button)
menu.add.button('5 лучших', show_best)
menu.add.button('Выход', pygame_menu.events.EXIT)

'''Запускаем основной цикл меню'''
def mainloop(win):
    while True:
        win.blit(bg_image, (0, 0))

        evvents = pygame.event.get()
        for evvent in evvents:
            if evvent.type == pygame.QUIT:
                exit()

        if menu.is_enabled():
            menu.update(evvents)
            menu.draw(win)

        pygame.display.update()
        timer.tick(60)

'''Точка входа'''
if __name__ == '__main__':
    mainloop(surface)
