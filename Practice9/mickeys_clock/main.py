"""
main.py  –  Mickey's Clock  🕐
================================
Entry point: initialises pygame, loads assets, runs the event loop.

Usage
-----
    python main.py

Controls
--------
    ESC / Q  →  quit
    F        →  toggle full-screen

Requirements
------------
    pip install pygame
"""

import sys
import os
import datetime
import pygame

from clock import MickeyClock


WINDOW_TITLE   = "Mickey's Clock"
WINDOW_W       = 520
WINDOW_H       = 560
TARGET_FPS     = 60          
CLOCK_RADIUS   = 210         

BG_TOP         = ( 25,  60, 120)   
BG_BOTTOM      = ( 10,  30,  70)   

HAND_IMG_NAME  = "mickey_hand.png"
IMAGES_DIR     = os.path.join(os.path.dirname(__file__), "images")



def draw_gradient_bg(surface: pygame.Surface) -> None:
    """Fill the surface with a vertical linear gradient."""
    h = surface.get_height()
    w = surface.get_width()
    for y in range(h):
        t   = y / h
        r   = int(BG_TOP[0] + (BG_BOTTOM[0] - BG_TOP[0]) * t)
        g   = int(BG_TOP[1] + (BG_BOTTOM[1] - BG_TOP[1]) * t)
        b   = int(BG_TOP[2] + (BG_BOTTOM[2] - BG_TOP[2]) * t)
        pygame.draw.line(surface, (r, g, b), (0, y), (w, y))


def draw_digital_time(surface: pygame.Surface, font: pygame.font.Font) -> None:
    """Render MM:SS in the lower portion of the window."""
    now  = datetime.datetime.now()
    text = now.strftime("%M:%S")
    surf = font.render(text, True, (240, 240, 240))
    rect = surf.get_rect(center=(surface.get_width() // 2,
                                 surface.get_height() - 36))
    shadow = font.render(text, True, (0, 0, 0))
    surface.blit(shadow, (rect.x + 2, rect.y + 2))
    surface.blit(surf, rect)


def load_hand_image(path: str) -> pygame.Surface:
    """Load the hand PNG, convert to RGBA for alpha-blending."""
    try:
        img = pygame.image.load(path).convert_alpha()
        return img
    except pygame.error as exc:
        print(f"[ERROR] Could not load '{path}': {exc}")
        print("        Run  images/generate_hand.py  first to create the asset.")
        sys.exit(1)



def main() -> None:
    pygame.init()
    pygame.display.set_caption(WINDOW_TITLE)

    screen = pygame.display.set_mode((WINDOW_W, WINDOW_H), pygame.RESIZABLE)

    clock_tick = pygame.time.Clock()
    full_screen = False

    hand_path = os.path.join(IMAGES_DIR, HAND_IMG_NAME)
    hand_img  = load_hand_image(hand_path)

    try:
        icon = pygame.transform.smoothscale(hand_img, (32, 32))
        pygame.display.set_icon(icon)
    except Exception:
        pass   
    
    font_digital = pygame.font.SysFont("Courier New", 38, bold=True)
    font_title   = pygame.font.SysFont("Arial",       20, bold=True)

    grad_surf = pygame.Surface(screen.get_size())
    draw_gradient_bg(grad_surf)

    mickey_clock = MickeyClock(
        screen=screen,
        center=(WINDOW_W // 2, WINDOW_H // 2 - 20),
        radius=CLOCK_RADIUS,
        hand_img=hand_img,
    )

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    running = False
                elif event.key == pygame.K_f:
                    full_screen = not full_screen
                    flags = pygame.FULLSCREEN if full_screen else pygame.RESIZABLE
                    screen = pygame.display.set_mode((WINDOW_W, WINDOW_H), flags)
                    mickey_clock = MickeyClock(
                        screen=screen,
                        center=(screen.get_width() // 2, screen.get_height() // 2 - 20),
                        radius=CLOCK_RADIUS,
                        hand_img=hand_img,
                    )

            elif event.type == pygame.VIDEORESIZE:
                grad_surf = pygame.Surface(screen.get_size())
                draw_gradient_bg(grad_surf)
                mickey_clock = MickeyClock(
                    screen=screen,
                    center=(screen.get_width() // 2, screen.get_height() // 2 - 20),
                    radius=int(min(screen.get_width(), screen.get_height()) * 0.40),
                    hand_img=hand_img,
                )

        screen.blit(grad_surf, (0, 0))

        title_surf = font_title.render(WINDOW_TITLE, True, (200, 220, 255))
        screen.blit(title_surf, (screen.get_width() // 2 - title_surf.get_width() // 2, 12))

        mickey_clock.draw()

        draw_digital_time(screen, font_digital)

        pygame.display.flip()
        clock_tick.tick(TARGET_FPS)

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()