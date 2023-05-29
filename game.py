import pygame
import sys
import random
import time
from sqlite import edit_scores, read_scores, get_best

pygame.init()

FRAME_COLOUR = (0, 255, 204)
WHITE = (255, 255, 255)
BLUE = (203, 255, 255)
RED = (255, 0, 0)
HEADER_COLOR = (0, 204, 253)
SNAKE_COLOR = (0, 102, 0)
SIZE_BLOCK = 20
COUNT_BLOCKS = 20
HEADER_MARGIN = 70
MARGIN = 1
size = [SIZE_BLOCK * COUNT_BLOCKS + 2 * SIZE_BLOCK + MARGIN * COUNT_BLOCKS,
        SIZE_BLOCK * COUNT_BLOCKS + 2 * SIZE_BLOCK + MARGIN * COUNT_BLOCKS + HEADER_MARGIN]

screen = pygame.display.set_mode(size)
pygame.display.set_caption('Змейка')
timer = pygame.time.Clock()
arial_36 = pygame.font.SysFont('arial', 36)


'''Класс змейки'''
class SnakeBlock:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def is_inside(self):
        return 0 <= self.x < COUNT_BLOCKS and 0 <= self.y < COUNT_BLOCKS

    def __eq__(self, other) -> bool:
        return isinstance(other, SnakeBlock) and self.x == other.x and self.y == other.y


'''Рисуем игровое поле'''
def draw_block(color, row, colomn):
    pygame.draw.rect(screen, color, [SIZE_BLOCK + colomn * SIZE_BLOCK + MARGIN * (colomn + 1),
                                     HEADER_MARGIN + SIZE_BLOCK + row * SIZE_BLOCK + MARGIN * (row + 1),
                                     SIZE_BLOCK, SIZE_BLOCK])


def start_game(name):
    last_scores = read_scores(name)
    print(last_scores)

    def get_random_empty_block():
        x = random.randint(0, COUNT_BLOCKS - 1)
        y = random.randint(0, COUNT_BLOCKS - 1)
        empty_block = SnakeBlock(x, y)
        while empty_block in snake_blocks:
            empty_block.x = random.randint(0, COUNT_BLOCKS - 1)
            empty_block.y = random.randint(0, COUNT_BLOCKS - 1)
        return empty_block

    '''Создаем объект змейки '''
    snake_blocks = [SnakeBlock(9, 8), SnakeBlock(9, 9), SnakeBlock(9, 10)]
    apple = get_random_empty_block()
    d_row = buf_row = 0
    d_col = buf_col = 1
    total = 0
    speed = 1

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print('Exit')
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and d_col != 0:
                    buf_row = -1
                    buf_col = 0
                elif event.key == pygame.K_DOWN and d_col != 0:
                    buf_row = 1
                    buf_col = 0
                elif event.key == pygame.K_LEFT and d_row != 0:
                    buf_row = 0
                    buf_col = -1
                elif event.key == pygame.K_RIGHT and d_row != 0:
                    buf_row = 0
                    buf_col = 1

        screen.fill(FRAME_COLOUR)
        pygame.draw.rect(screen, HEADER_COLOR, [0, 0, size[0], HEADER_MARGIN])
        text_name = arial_36.render(name, False, WHITE)
        text_total = arial_36.render(f"Total: {total}", False, WHITE)
        text_speed = arial_36.render(f"Speed: {speed}", False, WHITE)
        screen.blit(text_total, (SIZE_BLOCK, SIZE_BLOCK))
        screen.blit(text_name, (SIZE_BLOCK + 150, SIZE_BLOCK))
        screen.blit(text_speed, (SIZE_BLOCK + 300, SIZE_BLOCK))

        for row in range(COUNT_BLOCKS):
            for column in range(COUNT_BLOCKS):
                if (row + column) % 2 == 0:
                    color = BLUE
                else:
                    color = WHITE

                draw_block(color, row, column)

        head = snake_blocks[-1]
        if not head.is_inside():
            if total > last_scores:
                edit_scores(name, total)
            print('crash')
            time.sleep(3)
            break

        draw_block(RED, apple.x, apple.y)
        for block in snake_blocks:
            draw_block(SNAKE_COLOR, block.x, block.y)

        if apple == head:
            total += 1
            speed = total // 5 + 1
            snake_blocks.append(apple)
            apple = get_random_empty_block()

        d_row = buf_row
        d_col = buf_col
        new_head = SnakeBlock(head.x + buf_row, head.y + buf_col)

        if new_head in snake_blocks:
            print('crash yourself')
            if total > last_scores:
                edit_scores(name, total)
            time.sleep(3)
            break

        snake_blocks.append(new_head)
        snake_blocks.pop(0)

        pygame.display.flip()
        timer.tick(3)


def show_best():
    items = get_best()
    arial_36 = pygame.font.SysFont('arial', 36)
    screen.fill((186, 214, 177))
    for i, (name, _, scores) in enumerate(items, start=1):
        text = arial_36.render(str(i) + ". " + str(name) + " " + str(scores) + " очков ", True, (255, 255, 255))
        screen.blit(text, (100, 100 + i * 50))

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
        pygame.display.update()
        timer.tick(60)
