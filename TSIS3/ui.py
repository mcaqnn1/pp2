import pygame

W, H = 800, 600

C_BG       = (15,  15,  25)
C_ROAD     = (40,  40,  55)
C_ACCENT   = (255, 200,  50)
C_WHITE    = (240, 240, 240)
C_GRAY     = (120, 120, 140)
C_RED      = (220,  60,  60)
C_GREEN    = ( 60, 200,  80)
C_BLUE     = ( 60, 130, 255)
C_DARK     = ( 25,  25,  38)


def get_fonts():
    big   = pygame.font.SysFont("Consolas", 52, bold=True)
    med   = pygame.font.SysFont("Consolas", 30, bold=True)
    small = pygame.font.SysFont("Consolas", 20)
    tiny  = pygame.font.SysFont("Consolas", 16)
    return big, med, small, tiny


class Button:
    def __init__(self, rect, label, color=C_ROAD, hover_color=C_ACCENT, text_color=C_WHITE):
        self.rect        = pygame.Rect(rect)
        self.label       = label
        self.color       = color
        self.hover_color = hover_color
        self.text_color  = text_color
        self._font       = None

    def _get_font(self):
        if not self._font:
            self._font = pygame.font.SysFont("Consolas", 22, bold=True)
        return self._font

    def draw(self, surface):
        mx, my = pygame.mouse.get_pos()
        hovered = self.rect.collidepoint(mx, my)
        c = self.hover_color if hovered else self.color
        tc = C_DARK if hovered else self.text_color
        pygame.draw.rect(surface, c, self.rect, border_radius=8)
        pygame.draw.rect(surface, C_ACCENT, self.rect, 2, border_radius=8)
        text = self._get_font().render(self.label, True, tc)
        surface.blit(text, text.get_rect(center=self.rect.center))

    def clicked(self, event):
        return (event.type == pygame.MOUSEBUTTONDOWN and
                event.button == 1 and
                self.rect.collidepoint(event.pos))


def draw_text(surface, font, text, color, center):
    surf = font.render(text, True, color)
    surface.blit(surf, surf.get_rect(center=center))


def draw_main_menu(surface, fonts):
    big, med, small, tiny = fonts
    surface.fill(C_BG)

    draw_text(surface, big, "RACER", C_ACCENT, (W // 2, 110))
    draw_text(surface, small, "TSIS 3  —  Advanced Racing", C_GRAY, (W // 2, 165))

    bw, bh = 260, 50
    bx = W // 2 - bw // 2
    buttons = {
        "play":        Button((bx, 230, bw, bh), "PLAY"),
        "leaderboard": Button((bx, 300, bw, bh), "LEADERBOARD"),
        "settings":    Button((bx, 370, bw, bh), "SETTINGS"),
        "quit":        Button((bx, 440, bw, bh), "QUIT", color=C_RED, hover_color=(255, 100, 100)),
    }
    for btn in buttons.values():
        btn.draw(surface)
    return buttons


def draw_settings(surface, fonts, settings):
    big, med, small, tiny = fonts
    surface.fill(C_BG)
    draw_text(surface, med, "SETTINGS", C_ACCENT, (W // 2, 60))

    bw, bh = 260, 46
    bx = W // 2 - bw // 2

    sound_lbl = "Sound: ON" if settings["sound"] else "Sound: OFF"
    sc = C_GREEN if settings["sound"] else C_RED
    buttons = {
        "sound":      Button((bx, 130, bw, bh), sound_lbl, color=sc),
        "color_red":  Button((bx - 90, 210, 80, bh), "RED",   color=(180, 40, 40)),
        "color_blue": Button((bx + 10,  210, 80, bh), "BLUE",  color=(40, 80, 200)),
        "color_green":Button((bx + 110, 210, 80, bh), "GREEN", color=(40, 160, 60)),
        "diff_easy":  Button((bx - 90, 290, 80, bh), "Easy",   color=C_GREEN if settings["difficulty"]=="easy"  else C_ROAD),
        "diff_normal":Button((bx + 10,  290, 80, bh), "Normal", color=C_ACCENT if settings["difficulty"]=="normal" else C_ROAD, text_color=C_DARK),
        "diff_hard":  Button((bx + 110, 290, 80, bh), "Hard",   color=C_RED if settings["difficulty"]=="hard"  else C_ROAD),
        "back":       Button((bx, 390, bw, bh), "BACK"),
    }

    draw_text(surface, small, "Car Colour:", C_WHITE, (W // 2, 193))
    draw_text(surface, small, "Difficulty:", C_WHITE, (W // 2, 273))

    preview = pygame.Rect(W // 2 - 18, 145, 36, 24)
    pygame.draw.rect(surface, tuple(settings["car_color"]), preview, border_radius=4)

    for btn in buttons.values():
        btn.draw(surface)
    return buttons


def draw_leaderboard(surface, fonts, entries):
    big, med, small, tiny = fonts
    surface.fill(C_BG)
    draw_text(surface, med, "LEADERBOARD", C_ACCENT, (W // 2, 50))

    headers = ["#", "Name", "Score", "Dist", "Coins"]
    col_x   = [60, 130, 340, 470, 590]
    draw_text(surface, tiny, "  #    Name               Score    Dist    Coins", C_GRAY, (W // 2, 95))
    pygame.draw.line(surface, C_GRAY, (40, 108), (W - 40, 108), 1)

    for i, e in enumerate(entries[:10]):
        y = 125 + i * 36
        color = C_ACCENT if i == 0 else (C_WHITE if i < 3 else C_GRAY)
        row = f" {i+1:<3}  {e['name']:<16}  {e['score']:>6}   {int(e['distance']):>4}m  {e['coins']:>5}"
        draw_text(surface, small, row, color, (W // 2, y))

    if not entries:
        draw_text(surface, small, "No scores yet!", C_GRAY, (W // 2, 300))

    back = Button((W // 2 - 130, 520, 260, 46), "BACK")
    back.draw(surface)
    return {"back": back}


def draw_game_over(surface, fonts, score, distance, coins, player_name):
    big, med, small, tiny = fonts
    surface.fill(C_BG)
    draw_text(surface, big,   "GAME OVER",                C_RED,    (W // 2, 90))
    draw_text(surface, small, f"Player: {player_name}",   C_WHITE,  (W // 2, 165))
    draw_text(surface, med,   f"Score:  {score}",         C_ACCENT, (W // 2, 215))
    draw_text(surface, small, f"Distance: {int(distance)} m", C_WHITE, (W // 2, 265))
    draw_text(surface, small, f"Coins:    {coins}",       C_WHITE,  (W // 2, 300))

    bw, bh = 220, 48
    bx = W // 2 - bw // 2
    buttons = {
        "retry": Button((bx, 370, bw, bh), "RETRY"),
        "menu":  Button((bx, 432, bw, bh), "MAIN MENU"),
    }
    for btn in buttons.values():
        btn.draw(surface)
    return buttons


def draw_name_input(surface, fonts, name_text):
    big, med, small, tiny = fonts
    surface.fill(C_BG)
    draw_text(surface, med,   "ENTER YOUR NAME", C_ACCENT, (W // 2, 180))
    draw_text(surface, small, "Press Enter to start", C_GRAY, (W // 2, 420))

    box = pygame.Rect(W // 2 - 160, 250, 320, 52)
    pygame.draw.rect(surface, C_ROAD, box, border_radius=6)
    pygame.draw.rect(surface, C_ACCENT, box, 2, border_radius=6)
    cursor = "|" if (pygame.time.get_ticks() // 500) % 2 == 0 else ""
    draw_text(surface, med, name_text + cursor, C_WHITE, box.center)