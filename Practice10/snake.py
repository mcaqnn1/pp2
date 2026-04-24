import pygame
import random

pygame.init()

width = 600
height = 400

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake")

clock = pygame.time.Clock()

snake_block = 10

font = pygame.font.SysFont(None, 25)

def draw_snake(snake_list):
    for x in snake_list:
        pygame.draw.rect(screen, (0, 255, 0), [x[0], x[1], snake_block, snake_block])

def draw_text(text, x, y):
    value = font.render(text, True, (255, 255, 255))
    screen.blit(value, [x, y])

def game():
    x = width / 2
    y = height / 2

    x_change = 0
    y_change = 0

    snake_list = []
    snake_length = 1

    snake_speed = 10
    score = 0
    level = 1

    food_x = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
    food_y = round(random.randrange(0, height - snake_block) / 10.0) * 10.0

    run = True
    lose = False

    while run:

        while lose:
            screen.fill((0, 0, 0))
            draw_text("You lost! Q-quit C-play", 200, 180)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        run = False
                        lose = False
                    if event.key == pygame.K_c:
                        game()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -snake_block
                    y_change = 0
                elif event.key == pygame.K_RIGHT:
                    x_change = snake_block
                    y_change = 0
                elif event.key == pygame.K_UP:
                    y_change = -snake_block
                    x_change = 0
                elif event.key == pygame.K_DOWN:
                    y_change = snake_block
                    x_change = 0

        if x >= width or x < 0 or y >= height or y < 0:
            lose = True

        x += x_change
        y += y_change

        screen.fill((0, 0, 0))

        pygame.draw.rect(screen, (255, 0, 0), [food_x, food_y, snake_block, snake_block])

        head = []
        head.append(x)
        head.append(y)
        snake_list.append(head)

        if len(snake_list) > snake_length:
            del snake_list[0]

        for part in snake_list[:-1]:
            if part == head:
                lose = True

        draw_snake(snake_list)

        draw_text("Score: " + str(score), 10, 10)
        draw_text("Level: " + str(level), 10, 30)

        pygame.display.update()

        if x == food_x and y == food_y:
            good = False
            while not good:
                food_x = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
                food_y = round(random.randrange(0, height - snake_block) / 10.0) * 10.0
                good = True
                for part in snake_list:
                    if part[0] == food_x and part[1] == food_y:
                        good = False

            snake_length += 1
            score += 1

            if score % 3 == 0:
                level += 1
                snake_speed += 2

        clock.tick(snake_speed)

    pygame.quit()
    quit()

game()