"""
Music Player — keyboard-controlled pygame music player.

Controls:
  P   Play / Pause
  S   Stop
  N   Next track
  B   Back (previous track)
  Q   Quit
"""

import pygame
import sys
import math
from player import MusicPlayer

W, H      = 700, 480
FPS       = 60
MUSIC_DIR = "music"

C_BG      = ( 18,  18,  24)
C_PANEL   = ( 28,  28,  38)
C_BORDER  = ( 50,  50,  68)
C_ACCENT  = (255, 180,  50)
C_ACCENT2 = (255, 130,  30)
C_TEXT    = (230, 230, 240)
C_SUBTEXT = (130, 130, 155)
C_BAR_BG  = ( 45,  45,  60)
C_PLAYING = ( 60, 220, 120)
C_PAUSED  = (255, 200,  60)
C_STOPPED = (160, 160, 180)
C_HI      = ( 38,  38,  55)

pygame.init()
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("♪  Music Player")
clock  = pygame.time.Clock()


def load_font(size, bold=False):
    for name in ["DejaVuSans", "Helvetica", "Arial", "FreeSans"]:
        try:
            return pygame.font.SysFont(name, size, bold=bold)
        except Exception:
            pass
    return pygame.font.Font(None, size)


font_title  = load_font(28, bold=True)
font_medium = load_font(17)
font_small  = load_font(14)
font_mono   = load_font(14)
font_keys   = load_font(13)

player = MusicPlayer(MUSIC_DIR)


def rr(surf, color, rect, radius=10, alpha=255):
    s = pygame.Surface((rect[2], rect[3]), pygame.SRCALPHA)
    pygame.draw.rect(s, (*color, alpha), (0, 0, rect[2], rect[3]), border_radius=radius)
    surf.blit(s, (rect[0], rect[1]))


def txt(surf, text, font, color, x, y):
    surf.blit(font.render(text, True, color), (x, y))


def txt_c(surf, text, font, color, cx, y):
    s = font.render(text, True, color)
    surf.blit(s, (cx - s.get_width() // 2, y))


def truncate(text, font, max_w):
    if font.size(text)[0] <= max_w:
        return text
    while text and font.size(text + "…")[0] > max_w:
        text = text[:-1]
    return text + "…"


def draw_progress_bar(surf, x, y, w, h, progress):
    rr(surf, C_BAR_BG, (x, y, w, h), 5)
    fill_w = max(int(w * progress), 0)
    if fill_w > 0:
        rr(surf, C_ACCENT, (x, y, fill_w, h), 5)
    pygame.draw.circle(surf, C_ACCENT, (x + fill_w, y + h // 2), h)


def draw_vinyl(surf, cx, cy, r, angle):
    """Spinning record with grooves."""
    pygame.draw.circle(surf, (26, 26, 38), (cx, cy), r)
    # Grooves (concentric rings)
    for gr in range(r - 6, 12, -7):
        s = pygame.Surface((gr * 2, gr * 2), pygame.SRCALPHA)
        pygame.draw.circle(s, (255, 255, 255, 35), (gr, gr), gr, 1)
        surf.blit(s, (cx - gr, cy - gr))
    shine_angle = math.radians(angle)
    for offset in range(0, 20, 4):
        sx = cx + int((r - offset) * 0.6 * math.cos(shine_angle))
        sy = cy + int((r - offset) * 0.6 * math.sin(shine_angle))
        pygame.draw.circle(surf, (255, 255, 255, 18), (sx, sy), 3)
    pygame.draw.circle(surf, C_ACCENT2, (cx, cy), 20)
    pygame.draw.circle(surf, (18, 18, 24), (cx, cy), 6)
    
    arm_angle  = math.radians(-38)
    arm_len    = r + 20
    pivot      = (cx + r - 8, cy - r + 8)
    end_pt     = (cx + int(arm_len * math.cos(arm_angle)),
                  cy + int(arm_len * math.sin(arm_angle)))
    pygame.draw.line(surf, C_SUBTEXT, pivot, end_pt, 2)
    pygame.draw.circle(surf, C_ACCENT, end_pt, 4)


KEY_HINTS = [("P", "Play/Pause"), ("S", "Stop"), ("N", "Next"), ("B", "Back"), ("Q", "Quit")]


def draw_key_hints(surf, x, y):
    for i, (key, label) in enumerate(KEY_HINTS):
        kx = x + i * 118
        rr(surf, C_BORDER, (kx, y, 24, 20), 4)
        txt_c(surf, key, font_keys, C_ACCENT, kx + 12, y + 3)
        txt(surf, label, font_keys, C_SUBTEXT, kx + 30, y + 4)


def draw_playlist(surf, px, py, pw, ph):
    import os
    rr(surf, C_PANEL, (px, py, pw, ph), 10)
    pygame.draw.rect(surf, C_BORDER, (px, py, pw, ph), 1, border_radius=10)

    header = font_small.render(f"PLAYLIST  ({len(player.playlist)} tracks)", True, C_SUBTEXT)
    surf.blit(header, (px + 12, py + 10))

    row_h    = 28
    max_rows = (ph - 36) // row_h
    start    = max(0, player.track_index - max_rows // 2)
    start    = min(start, max(0, len(player.playlist) - max_rows))

    for i, path in enumerate(player.playlist[start: start + max_rows]):
        name = os.path.splitext(os.path.basename(path))[0]
        ri   = start + i
        ry   = py + 34 + i * row_h

        if ri == player.track_index:
            rr(surf, C_HI, (px + 6, ry, pw - 12, row_h - 2), 6)
            color  = C_ACCENT
            prefix = "▶  "
        else:
            color  = C_TEXT
            prefix = f"{ri + 1:02d}.  "

        label = truncate(prefix + name, font_small, pw - 28)
        txt(surf, label, font_small, color, px + 14, ry + 7)

    if not player.playlist:
        msg = font_small.render("No audio files in ./music/", True, C_SUBTEXT)
        surf.blit(msg, (px + 12, py + ph // 2))


vinyl_angle = 0.0

while True:
    dt = clock.tick(FPS) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if   event.key == pygame.K_q: pygame.quit(); sys.exit()
            elif event.key == pygame.K_p: player.toggle_play_pause()
            elif event.key == pygame.K_s: player.stop()
            elif event.key == pygame.K_n: player.next_track()
            elif event.key == pygame.K_b: player.prev_track()

    player.check_track_ended()

    if player.state == "PLAYING":
        vinyl_angle = (vinyl_angle + 90 * dt) % 360

    screen.fill(C_BG)

    # Header
    rr(screen, C_PANEL, (0, 0, W, 56), 0)
    pygame.draw.line(screen, C_BORDER, (0, 56), (W, 56))
    txt(screen, "♪  MUSIC PLAYER", font_title, C_ACCENT, 20, 13)

    state      = player.state
    badge_col  = {MusicPlayer.PLAYING: C_PLAYING,
                  MusicPlayer.PAUSED:  C_PAUSED,
                  MusicPlayer.STOPPED: C_STOPPED}[state]
    bw = font_small.size(state)[0] + 20
    rr(screen, badge_col, (W - bw - 16, 17, bw, 22), 11)
    txt_c(screen, state, font_small, C_BG, W - bw // 2 - 16, 20)

    lx       = 30
    vinyl_cx = lx + 88
    vinyl_cy = 162

    draw_vinyl(screen, vinyl_cx, vinyl_cy, 80, vinyl_angle)

    name = player.current_name if player.playlist else "— No tracks —"
    txt(screen, truncate(name, font_title, 295), font_title, C_TEXT, lx, 256)


    if player.playlist:
        idx = f"Track  {player.track_index + 1}  /  {len(player.playlist)}"
    else:
        idx = "Track  —  /  —"
    txt(screen, idx, font_medium, C_SUBTEXT, lx, 292)

    bar_x, bar_y, bar_w, bar_h = lx, 328, 308, 8
    draw_progress_bar(screen, bar_x, bar_y, bar_w, bar_h, player.progress)

    pos_s = MusicPlayer.fmt_time(player.position_seconds)
    dur_s = MusicPlayer.fmt_time(player.track_length_seconds)
    txt(screen, pos_s, font_mono, C_SUBTEXT, bar_x, 342)
    dur_surf = font_mono.render(dur_s, True, C_SUBTEXT)
    screen.blit(dur_surf, (bar_x + bar_w - dur_surf.get_width(), 342))

    for i in range(38):
        phase = vinyl_angle * 0.04 + i * 0.45
        bh    = 5 + int(13 * abs(math.sin(phase)))
        col   = C_ACCENT if i % 3 != 0 else C_ACCENT2
        pygame.draw.rect(screen, col, (lx + i * 8, 378 - bh, 5, bh), border_radius=2)

    draw_key_hints(screen, lx, 418)

    pygame.draw.line(screen, C_BORDER, (353, 68), (353, H - 10), 1)
    draw_playlist(screen, 366, 68, 318, H - 80)

    pygame.display.flip()