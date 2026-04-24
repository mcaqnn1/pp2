import pygame

pygame.init()

width = 800
height = 600

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Paint")

clock = pygame.time.Clock()

color = (0, 0, 0)
radius = 5

drawing = False
last_pos = None

mode = "brush"

colors = [
    (0,0,0),
    (255,0,0),
    (0,255,0),
    (0,0,255),
    (255,255,0),
    (255,255,255)
]

def draw_palette():
    x = 10
    for c in colors:
        pygame.draw.rect(screen, c, (x, 10, 30, 30))
        x += 40

run = True

while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()

            x = 10
            for c in colors:
                rect = pygame.Rect(x, 10, 30, 30)
                if rect.collidepoint(mx, my):
                    color = c
                x += 40

            drawing = True
            last_pos = (mx, my)

        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                mode = "brush"
            if event.key == pygame.K_2:
                mode = "rect"
            if event.key == pygame.K_3:
                mode = "circle"
            if event.key == pygame.K_4:
                mode = "eraser"

    if drawing:
        mx, my = pygame.mouse.get_pos()

        if mode == "brush":
            pygame.draw.line(screen, color, last_pos, (mx, my), radius)

        if mode == "rect":
            pygame.draw.rect(screen, color, (mx, my, 60, 40))

        if mode == "circle":
            pygame.draw.circle(screen, color, (mx, my), 30)

        if mode == "eraser":
            pygame.draw.line(screen, (0,0,0), last_pos, (mx, my), radius*3)

        last_pos = (mx, my)

    draw_palette()

    pygame.display.update()
    clock.tick(60)

pygame.quit()