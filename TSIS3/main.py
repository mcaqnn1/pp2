import sys
import pygame
from persistence import load_settings, save_settings, load_leaderboard, add_score
from racer import GameState
from ui import (
    W, H,
    get_fonts,
    draw_main_menu,
    draw_settings,
    draw_leaderboard,
    draw_game_over,
    draw_name_input,
)

FPS = 60

STATE_MENU        = "menu"
STATE_NAME_INPUT  = "name_input"
STATE_GAME        = "game"
STATE_GAME_OVER   = "game_over"
STATE_LEADERBOARD = "leaderboard"
STATE_SETTINGS    = "settings"


def main():
    pygame.init()
    screen  = pygame.display.set_mode((W, H))
    pygame.display.set_caption("RACER — TSIS 3")
    clock   = pygame.time.Clock()
    fonts   = get_fonts()

    settings    = load_settings()
    leaderboard = load_leaderboard()

    state       = STATE_MENU
    player_name = ""
    game        = None
    buttons     = {}

    while True:
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if state == STATE_MENU:
            buttons = draw_main_menu(screen, fonts)
            for event in events:
                if buttons["play"].clicked(event):
                    state = STATE_NAME_INPUT
                    player_name = ""
                elif buttons["leaderboard"].clicked(event):
                    leaderboard = load_leaderboard()
                    state = STATE_LEADERBOARD
                elif buttons["settings"].clicked(event):
                    state = STATE_SETTINGS
                elif buttons["quit"].clicked(event):
                    pygame.quit()
                    sys.exit()

        elif state == STATE_NAME_INPUT:
            draw_name_input(screen, fonts, player_name)
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and player_name.strip():
                        game  = GameState(settings, player_name.strip())
                        state = STATE_GAME
                    elif event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                    elif event.key == pygame.K_ESCAPE:
                        state = STATE_MENU
                    elif len(player_name) < 16 and event.unicode.isprintable():
                        player_name += event.unicode

        elif state == STATE_GAME:
            keys = pygame.key.get_pressed()
            game.update(keys)
            game.draw(screen, fonts)

            for event in events:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    state = STATE_MENU

            if not game.alive:
                leaderboard = add_score(
                    game.player_name,
                    game.score,
                    game.distance,
                    game.coin_count,
                )
                state = STATE_GAME_OVER

        elif state == STATE_GAME_OVER:
            buttons = draw_game_over(
                screen, fonts,
                game.score, game.distance, game.coin_count, game.player_name
            )
            for event in events:
                if buttons["retry"].clicked(event):
                    game  = GameState(settings, game.player_name)
                    state = STATE_GAME
                elif buttons["menu"].clicked(event):
                    state = STATE_MENU

        elif state == STATE_LEADERBOARD:
            buttons = draw_leaderboard(screen, fonts, leaderboard)
            for event in events:
                if buttons["back"].clicked(event):
                    state = STATE_MENU

        elif state == STATE_SETTINGS:
            buttons = draw_settings(screen, fonts, settings)
            for event in events:
                if buttons["sound"].clicked(event):
                    settings["sound"] = not settings["sound"]
                    save_settings(settings)
                elif buttons["color_red"].clicked(event):
                    settings["car_color"] = [220, 60, 60]
                    save_settings(settings)
                elif buttons["color_blue"].clicked(event):
                    settings["car_color"] = [60, 100, 220]
                    save_settings(settings)
                elif buttons["color_green"].clicked(event):
                    settings["car_color"] = [60, 190, 80]
                    save_settings(settings)
                elif buttons["diff_easy"].clicked(event):
                    settings["difficulty"] = "easy"
                    save_settings(settings)
                elif buttons["diff_normal"].clicked(event):
                    settings["difficulty"] = "normal"
                    save_settings(settings)
                elif buttons["diff_hard"].clicked(event):
                    settings["difficulty"] = "hard"
                    save_settings(settings)
                elif buttons["back"].clicked(event):
                    state = STATE_MENU

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()