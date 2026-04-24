import pygame
import random

pygame.init()

width = 400
height = 600

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Racer")

clock = pygame.time.Clock()

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
yellow = (255,255,0)

player_x = 180
player_y = 500
player_speed = 5

enemy_x = random.randint(60, 300)
enemy_y = -100
enemy_speed = 5

coin_x = random.randint(60, 300)
coin_y = -200
coin_speed = 4

coins = 0

font = pygame.font.SysFont(None, 30)

run = True
game_over = False

while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if not game_over:
        if keys[pygame.K_LEFT]:
            player_x -= player_speed
        if keys[pygame.K_RIGHT]:
            player_x += player_speed

    screen.fill(white)

    pygame.draw.rect(screen, black, (150, 0, 100, height))

    pygame.draw.rect(screen, red, (player_x, player_y, 40, 60))

    pygame.draw.rect(screen, black, (enemy_x, enemy_y, 40, 60))

    pygame.draw.circle(screen, yellow, (coin_x, coin_y), 10)

    if not game_over:
        enemy_y += enemy_speed
        coin_y += coin_speed

    if enemy_y > height:
        enemy_y = -150

        good = False
        while not good:
            enemy_x = random.randint(60, 300)
            if abs(enemy_x - player_x) > 80:
                good = True

    if coin_y > height:
        coin_y = -100
        coin_x = random.randint(60, 300)

    player_rect = pygame.Rect(player_x, player_y, 40, 60)
    enemy_rect = pygame.Rect(enemy_x, enemy_y, 40, 60)
    coin_rect = pygame.Rect(coin_x-10, coin_y-10, 20, 20)

    if player_rect.colliderect(enemy_rect):
        game_over = True

    if player_rect.colliderect(coin_rect):
        coins += 1
        coin_y = -100
        coin_x = random.randint(60, 300)

    text = font.render("Coins: " + str(coins), True, black)
    screen.blit(text, (250, 10))

    if game_over:
        text2 = font.render("GAME OVER - press R", True, red)
        screen.blit(text2, (80, 300))

        if keys[pygame.K_r]:
            player_x = 180
            enemy_y = -100
            coin_y = -200
            coins = 0
            game_over = False

    pygame.display.update()
    clock.tick(60)

pygame.quit()