import pygame
import random


from button import Button
from storage import DatabaseManager

db = DatabaseManager('database.db')

pygame.init()

white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

width, height = 600, 400

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Змейка!')

clock = pygame.time.Clock()

snake_block = 10
snake_speed = 15

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

play_again = Button(width / 2 - 100, height / 2, 200, 50, white, 'Начать сначала', black)
close_game = Button(width / 2 - 100, height / 2 + 70, 200, 50, white, 'Закрыть', black)
play_game = Button(width / 2 - 100, height / 2, 200, 50, white, 'Начать игру!', black)
queue = 1


def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(screen, white, [x[0], x[1], snake_block, snake_block])


def message(msg, color, h=0):
    msg = font_style.render(msg, True, color)
    screen.blit(msg, [width / 10, height / 3 + h])


def draw_button(x, y, width, height, text):
    pygame.draw.rect(screen, white, (x, y, width, height))
    font = pygame.font.Font(None, 36)
    text = font.render(text, True, black)
    text_rect = text.get_rect(center=(x + width / 2, y + height / 2))
    screen.blit(text, text_rect)


def gameLoop(que: int):
    game_over = False
    game_close = False

    x1, y1 = width / 2, height / 2
    x1_change, y1_change = 0, 0

    snake_List = []
    Length_of_snake = 1

    food_x = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
    food_y = round(random.randrange(0, height - snake_block) / 10.0) * 10.0

    while not game_over:

        while game_close is True:
            screen.fill(black)
            message(f"Вы проиграли! Ваш счет сосавляет {Length_of_snake - 1} очков", red)
            play_again.draw(screen)
            close_game.draw(screen)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_again.rect.collidepoint(event.pos):
                        db.check_record(Length_of_snake - 1)
                        que += 1
                        gameLoop(que)
                    elif close_game.rect.collidepoint(event.pos):
                        db.check_record(Length_of_snake - 1)
                        game_over = True
                        game_close = False

        while que == 1:
            screen.fill(black)
            record = db.fetchone('SELECT record FROM config')
            message(f"      Добро пожаловать в старую Змейку!", red)
            if record is not None:
                message(f"                  Ваш личный рекорд {record[0]}", red, 30)
            play_game.draw(screen)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_game.rect.collidepoint(event.pos):
                        que -= 1
                        gameLoop(que)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        screen.fill(black)
        pygame.draw.rect(screen, green, [food_x, food_y, snake_block, snake_block])
        snake_head = [x1, y1]
        snake_List.append(snake_head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_head:
                game_close = True

        our_snake(snake_block, snake_List)

        pygame.display.update()

        if x1 == food_x and y1 == food_y:
            food_x = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
            food_y = round(random.randrange(0, height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()


gameLoop(queue)
