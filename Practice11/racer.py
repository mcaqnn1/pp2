import pygame
import random
import math

pygame.init()

WIDTH, HEIGHT = 500, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Гонщик")
clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 22, bold=True)
font_big = pygame.font.SysFont("consolas", 48, bold=True)

ROAD_LEFT  = 100
ROAD_RIGHT = 400
ROAD_WIDTH = ROAD_RIGHT - ROAD_LEFT
PLAYER_SPEED   = 5
SCROLL_SPEED   = 6
ENEMY_BASE_SPD = 4
COINS_PER_LEVEL = 5

COIN_TYPES = [
    {"name": "бронза", "value": 1,  "color": (180, 100, 40),  "r": 10},
    {"name": "серебро","value": 3,  "color": (180, 180, 190), "r": 13},
    {"name": "золото", "value": 5,  "color": (255, 210, 50),  "r": 16},
]

def draw_car(surface, cx, cy, color, roof_color):
    pygame.draw.rect(surface, color,       (cx-18, cy-30, 36, 60), border_radius=6)
    pygame.draw.rect(surface, roof_color,  (cx-12, cy-14, 24, 26), border_radius=4)
    pygame.draw.rect(surface, (160,215,255),(cx-10, cy-28, 20, 10), border_radius=3)
    pygame.draw.rect(surface, (255,245,150),(cx-16, cy-30,  7,  5), border_radius=2)
    pygame.draw.rect(surface, (255,245,150),(cx+ 9, cy-30,  7,  5), border_radius=2)
    pygame.draw.rect(surface, (255,50,30),  (cx-16, cy+25,  7,  5), border_radius=2)
    pygame.draw.rect(surface, (255,50,30),  (cx+ 9, cy+25,  7,  5), border_radius=2)

def draw_coin(surface, coin):
    cx, cy, r = int(coin["x"]), int(coin["y"]), coin["r"]
    pygame.draw.circle(surface, coin["color"], (cx, cy), r)
    pygame.draw.circle(surface, (255,255,255), (cx-r//3, cy-r//3), r//4)
    lbl = font.render(str(coin["value"]), True, (30,30,30))
    surface.blit(lbl, lbl.get_rect(center=(cx, cy)))

road_offset = 0

def draw_road(surface, offset):
    surface.fill((45, 110, 45))
    pygame.draw.rect(surface, (70,70,78), (ROAD_LEFT, 0, ROAD_WIDTH, HEIGHT))
    pygame.draw.rect(surface, (220,220,220), (ROAD_LEFT, 0, 8, HEIGHT))
    pygame.draw.rect(surface, (220,220,220), (ROAD_RIGHT-8, 0, 8, HEIGHT))
    for lane_x in (ROAD_LEFT + ROAD_WIDTH//3, ROAD_LEFT + 2*ROAD_WIDTH//3):
        for y in range(-60 + offset % 80, HEIGHT, 80):
            pygame.draw.rect(surface, (240,220,60), (lane_x-2, y, 4, 45), border_radius=2)

def draw_hud(surface, score, level):
    pygame.draw.rect(surface, (15,15,20), (0, 0, WIDTH, 40))
    pygame.draw.line(surface, (220,40,40), (0,40), (WIDTH,40), 2)
    surface.blit(font.render(f"Монеты: {score}", True, (255,210,50)), (10, 9))
    t = font.render(f"Уровень врага: {level}", True, (255,100,100))
    surface.blit(t, (WIDTH - t.get_width() - 10, 9))

def draw_gameover(surface, score):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0,0,0,160))
    surface.blit(overlay, (0,0))
    t1 = font_big.render("КОНЕЦ!", True, (255,60,60))
    t2 = font.render(f"Собрано монет: {score}", True, (255,210,50))
    t3 = font.render("Нажми R — заново", True, (200,200,200))
    surface.blit(t1, t1.get_rect(center=(WIDTH//2, HEIGHT//2-60)))
    surface.blit(t2, t2.get_rect(center=(WIDTH//2, HEIGHT//2)))
    surface.blit(t3, t3.get_rect(center=(WIDTH//2, HEIGHT//2+50)))

def reset():
    return {
        "player_x": WIDTH // 2,
        "player_y": HEIGHT - 100,
        "score": 0,
        "enemy_speed": ENEMY_BASE_SPD,
        "enemy_level": 1,
        "enemy": {"x": random.randint(ROAD_LEFT+25, ROAD_RIGHT-25), "y": -80},
        "coins": [],
        "coin_timer": 0,
        "gameover": False,
    }

state = reset()

while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            state = reset()

    if not state["gameover"]:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]  or keys[pygame.K_a]: state["player_x"] -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: state["player_x"] += PLAYER_SPEED
        state["player_x"] = max(ROAD_LEFT+20, min(ROAD_RIGHT-20, state["player_x"]))

        road_offset = (road_offset + SCROLL_SPEED) % 80

        state["enemy"]["y"] += state["enemy_speed"]
        if state["enemy"]["y"] > HEIGHT + 60:
            state["enemy"]["y"] = -80
            state["enemy"]["x"] = random.randint(ROAD_LEFT+25, ROAD_RIGHT-25)

        state["coin_timer"] += 1
        if state["coin_timer"] >= 60:
            state["coin_timer"] = 0
            ct = random.choices(COIN_TYPES, weights=[60, 30, 10])[0]
            state["coins"].append({
                "x": random.randint(ROAD_LEFT+20, ROAD_RIGHT-20),
                "y": -20, "value": ct["value"],
                "color": ct["color"], "r": ct["r"],
            })

        for coin in state["coins"]:
            coin["y"] += SCROLL_SPEED
        state["coins"] = [c for c in state["coins"] if c["y"] < HEIGHT+30]

        px, py = state["player_x"], state["player_y"]
        for coin in state["coins"][:]:
            if math.hypot(px-coin["x"], py-coin["y"]) < coin["r"]+18:
                state["score"] += coin["value"]
                state["coins"].remove(coin)
                level = state["score"] // COINS_PER_LEVEL + 1
                if level > state["enemy_level"]:
                    state["enemy_level"] = level
                    state["enemy_speed"] = ENEMY_BASE_SPD + (level-1) * 0.8

        ex, ey = state["enemy"]["x"], state["enemy"]["y"]
        if abs(px-ex) < 30 and abs(py-ey) < 45:
            state["gameover"] = True

    draw_road(screen, road_offset)
    for coin in state["coins"]:
        draw_coin(screen, coin)
    draw_car(screen, int(state["enemy"]["x"]), int(state["enemy"]["y"]), (50,80,220), (30,50,160))
    draw_car(screen, int(state["player_x"]), int(state["player_y"]), (220,40,40), (160,20,20))
    draw_hud(screen, state["score"], state["enemy_level"])
    if state["gameover"]:
        draw_gameover(screen, state["score"])
    pygame.display.flip()