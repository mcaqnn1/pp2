import pygame
import sys
from ball import Ball

pygame.init()

SCREEN_W, SCREEN_H = 800, 600
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("🔴 Moving Ball")
clock = pygame.time.Clock()
font_small = pygame.font.SysFont("Arial", 16)
font_big   = pygame.font.SysFont("Arial", 22, bold=True)

ball = Ball(SCREEN_W, SCREEN_H)

BG_COLOR     = (255, 255, 255)
BORDER_COLOR = (220, 220, 220)
TEXT_COLOR   = (80, 80, 80)

def draw_hud():
    """Overlay: position + controls hint."""
    pos_text = font_small.render(
        f"Position: ({ball.x}, {ball.y})", True, TEXT_COLOR)
    hint_text = font_small.render(
        "Arrow keys to move  •  ESC to quit", True, TEXT_COLOR)
    screen.blit(pos_text,  (12, 10))
    screen.blit(hint_text, (12, 30))

    title = font_big.render("Moving Ball", True, (220, 30, 30))
    screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 10))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_UP:
                ball.move('up')
            elif event.key == pygame.K_DOWN:
                ball.move('down')
            elif event.key == pygame.K_LEFT:
                ball.move('left')
            elif event.key == pygame.K_RIGHT:
                ball.move('right')

    screen.fill(BG_COLOR)
    pygame.draw.rect(screen, BORDER_COLOR, (0, 0, SCREEN_W, SCREEN_H), 3)

    ball.draw(screen)
    draw_hud()

    pygame.display.flip()
    clock.tick(60)