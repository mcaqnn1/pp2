import pygame
import random

pygame.init()

CELL  = 30
COLS  = 20
ROWS  = 20
WIDTH  = COLS * CELL
HEIGHT = ROWS * CELL + 50

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Змейка")
clock = pygame.time.Clock()
font     = pygame.font.SysFont("consolas", 20, bold=True)
font_big = pygame.font.SysFont("consolas", 46, bold=True)
font_sm  = pygame.font.SysFont("consolas", 15)

BG_DARK  = (20, 20, 25)
BG_LIGHT = (25, 25, 32)
SNAKE_COL = (60, 200, 80)
SNAKE_HD  = (40, 160, 55)

FOOD_TYPES = [
    {"name": "яблоко", "value": 1, "color": (220, 50,  50),  "lifetime": 8},
    {"name": "банан",  "value": 2, "color": (240, 210, 40),  "lifetime": 6},
    {"name": "вишня",  "value": 3, "color": (180, 30,  80),  "lifetime": 4},
    {"name": "звезда", "value": 5, "color": (100, 180, 255), "lifetime": 3},
]
MAX_FOOD = 4
FOOD_SPAWN_RATE = 3

UP, DOWN, LEFT, RIGHT = (0,-1),(0,1),(-1,0),(1,0)

def px(col, row):
    return col * CELL, row * CELL + 50

def draw_grid(surface):
    for r in range(ROWS):
        for c in range(COLS):
            x, y = px(c, r)
            pygame.draw.rect(surface, BG_DARK if (c+r)%2==0 else BG_LIGHT, (x,y,CELL,CELL))

def draw_snake(surface, snake):
    for i, (col, row) in enumerate(snake):
        x, y = px(col, row)
        color = SNAKE_HD if i == 0 else SNAKE_COL
        pygame.draw.rect(surface, color, (x+2, y+2, CELL-4, CELL-4), border_radius=7)
        if i == 0:
            pygame.draw.circle(surface, (255,255,255), (x+8,  y+9), 4)
            pygame.draw.circle(surface, (255,255,255), (x+22, y+9), 4)
            pygame.draw.circle(surface, (0,0,0),       (x+9,  y+10), 2)
            pygame.draw.circle(surface, (0,0,0),       (x+23, y+10), 2)

def draw_food(surface, food_list, now):
    for food in food_list:
        col, row  = food["pos"]
        x, y      = px(col, row)
        time_left = food["expire"] - now
        color     = food["color"]
        if time_left < 2:
            blink = int(now * 4) % 2 == 0
            color = tuple(min(255, c+80) for c in color) if blink else color
        cx, cy = x + CELL//2, y + CELL//2
        pygame.draw.circle(surface, color, (cx, cy), CELL//2-4)
        pygame.draw.circle(surface, (255,255,255), (cx-4, cy-4), 3)
        lbl = font_sm.render(f"+{food['value']}", True, (255,255,255))
        surface.blit(lbl, lbl.get_rect(center=(cx, cy)))
        ratio = max(0, time_left / food["lifetime"])
        bar_w = int((CELL-4) * ratio)
        bar_col = (80,220,80) if ratio > 0.5 else (240,180,40) if ratio > 0.25 else (240,60,60)
        pygame.draw.rect(surface, (40,40,40), (x+2, y+CELL-6, CELL-4, 4), border_radius=2)
        if bar_w > 0:
            pygame.draw.rect(surface, bar_col, (x+2, y+CELL-6, bar_w, 4), border_radius=2)

def draw_hud(surface, score, length):
    pygame.draw.rect(surface, (12,12,18), (0, 0, WIDTH, 50))
    pygame.draw.line(surface, (60,200,80), (0,50), (WIDTH,50), 2)
    surface.blit(font.render(f"Очки: {score}", True, (60,200,80)), (10, 14))
    t = font.render(f"Длина: {length}", True, (160,160,180))
    surface.blit(t, (WIDTH - t.get_width() - 10, 14))

def draw_gameover(surface, score):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0,0,0,170))
    surface.blit(overlay, (0,0))
    for txt, color, dy in [
        (font_big.render("КОНЕЦ!", True, (220,60,60)),   None, -60),
        (font.render(f"Очки: {score}", True, (255,210,50)), None, 0),
        (font.render("Нажми R — заново", True, (180,180,180)), None, 50),
    ]:
        surface.blit(txt, txt.get_rect(center=(WIDTH//2, HEIGHT//2+dy)))

def free_cell(snake, food_list):
    occupied = set(snake) | {f["pos"] for f in food_list}
    free = [(c,r) for c in range(COLS) for r in range(ROWS) if (c,r) not in occupied]
    return random.choice(free) if free else None

def spawn_food(snake, food_list, now):
    if len(food_list) >= MAX_FOOD:
        return
    pos = free_cell(snake, food_list)
    if not pos:
        return
    ft = random.choices(FOOD_TYPES, weights=[50,30,15,5])[0]
    food_list.append({"pos": pos, "value": ft["value"], "color": ft["color"],
                      "lifetime": ft["lifetime"], "expire": now + ft["lifetime"]})

def reset():
    snake = [(COLS//2, ROWS//2),(COLS//2-1, ROWS//2),(COLS//2-2, ROWS//2)]
    food  = []
    now   = pygame.time.get_ticks() / 1000
    spawn_food(snake, food, now)
    return {"snake": snake, "dir": RIGHT, "next_dir": RIGHT, "food": food,
            "score": 0, "move_timer": 0, "move_delay": 150,
            "food_timer": now + FOOD_SPAWN_RATE, "gameover": False}

state = reset()

while True:
    now_ms = pygame.time.get_ticks()
    now_s  = now_ms / 1000
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); exit()
        if event.type == pygame.KEYDOWN:
            d = state["dir"]
            if event.key in (pygame.K_UP,    pygame.K_w) and d != DOWN:  state["next_dir"] = UP
            if event.key in (pygame.K_DOWN,  pygame.K_s) and d != UP:    state["next_dir"] = DOWN
            if event.key in (pygame.K_LEFT,  pygame.K_a) and d != RIGHT: state["next_dir"] = LEFT
            if event.key in (pygame.K_RIGHT, pygame.K_d) and d != LEFT:  state["next_dir"] = RIGHT
            if event.key == pygame.K_r: state = reset()

    if not state["gameover"]:
        state["food"] = [f for f in state["food"] if f["expire"] > now_s]

        if now_s >= state["food_timer"]:
            spawn_food(state["snake"], state["food"], now_s)
            state["food_timer"] = now_s + FOOD_SPAWN_RATE

        if now_ms - state["move_timer"] >= state["move_delay"]:
            state["move_timer"] = now_ms
            state["dir"] = state["next_dir"]
            dx, dy = state["dir"]
            head = state["snake"][0]
            new_head = (head[0]+dx, head[1]+dy)

            if not (0 <= new_head[0] < COLS and 0 <= new_head[1] < ROWS) or new_head in state["snake"]:
                state["gameover"] = True
            else:
                state["snake"].insert(0, new_head)
                eaten = next((f for f in state["food"] if f["pos"] == new_head), None)
                if eaten:
                    state["score"] += eaten["value"]
                    state["food"].remove(eaten)
                    state["move_delay"] = max(80, 150 - state["score"] * 3)
                else:
                    state["snake"].pop()

    draw_grid(screen)
    draw_food(screen, state["food"], now_s)
    draw_snake(screen, state["snake"])
    draw_hud(screen, state["score"], len(state["snake"]))
    if state["gameover"]:
        draw_gameover(screen, state["score"])
    pygame.display.flip()