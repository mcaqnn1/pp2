import pygame
import math

pygame.init()

WIDTH, HEIGHT = 900, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Краска")
clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 15, bold=True)

TOOLBAR_W  = 160
CANVAS_RECT = pygame.Rect(TOOLBAR_W, 0, WIDTH - TOOLBAR_W, HEIGHT)

WHITE     = (255, 255, 255)
GRAY      = (200, 200, 200)
PANEL_BG  = (40,  40,  48)
BTN_NORMAL= (60,  60,  72)
BTN_HOVER = (80,  80,  98)
BTN_ACTIVE= (80, 140, 220)
BTN_TEXT  = (220, 220, 230)

PALETTE = [
    (0,0,0),(255,255,255),(200,50,50),(50,180,50),
    (50,100,220),(255,200,0),(180,80,220),(255,130,0),
    (0,200,200),(255,100,150),(100,60,20),(150,150,150),
]

TOOLS = [
    {"id": "pencil",    "label": "✏️  Карандаш"},
    {"id": "line",      "label": "╱  Линия"},
    {"id": "square",    "label": "□  Квадрат"},
    {"id": "rect",      "label": "▭  Прямоуг."},
    {"id": "rtriangle", "label": "◺  Прям.тр."},
    {"id": "etriangle", "label": "△  Равн.тр."},
    {"id": "rhombus",   "label": "◇  Ромб"},
    {"id": "circle",    "label": "○  Круг"},
    {"id": "eraser",    "label": "⬜ Ластик"},
]

state = {
    "tool": "pencil", "draw_color": (0,0,0),
    "size": 3, "drawing": False,
    "start": None, "filled": False,
}

canvas  = pygame.Surface((CANVAS_RECT.width, CANVAS_RECT.height))
canvas.fill(WHITE)
preview = pygame.Surface((CANVAS_RECT.width, CANVAS_RECT.height), pygame.SRCALPHA)

def get_square_pts(x1,y1,x2,y2):
    side = min(abs(x2-x1), abs(y2-y1))
    sx = side if x2>=x1 else -side
    sy = side if y2>=y1 else -side
    return [(x1,y1),(x1+sx,y1),(x1+sx,y1+sy),(x1,y1+sy)]

def get_right_triangle_pts(x1,y1,x2,y2):
    return [(x1,y2),(x1,y1),(x2,y2)]

def get_equilateral_triangle_pts(x1,y1,x2,y2):
    base = x2-x1
    h = abs(base)*math.sqrt(3)/2
    top_y = y2-h if y1<=y2 else y2+h
    return [(x1,y2),(x2,y2),((x1+x2)/2, top_y)]

def get_rhombus_pts(x1,y1,x2,y2):
    cx,cy = (x1+x2)/2,(y1+y2)/2
    return [(cx,y1),(x2,cy),(cx,y2),(x1,cy)]

def draw_shape(surface, tool, x1, y1, x2, y2, color, size, filled):
    lw = 0 if filled else size
    if tool == "line":
        pygame.draw.line(surface, color, (x1,y1), (x2,y2), size)
    elif tool == "rect":
        pygame.draw.rect(surface, color,
            pygame.Rect(min(x1,x2),min(y1,y2),abs(x2-x1),abs(y2-y1)), lw)
    elif tool == "square":
        pygame.draw.polygon(surface, color, get_square_pts(x1,y1,x2,y2), lw)
    elif tool == "rtriangle":
        pygame.draw.polygon(surface, color, get_right_triangle_pts(x1,y1,x2,y2), lw)
    elif tool == "etriangle":
        pts = [(int(p[0]),int(p[1])) for p in get_equilateral_triangle_pts(x1,y1,x2,y2)]
        pygame.draw.polygon(surface, color, pts, lw)
    elif tool == "rhombus":
        pts = [(int(p[0]),int(p[1])) for p in get_rhombus_pts(x1,y1,x2,y2)]
        pygame.draw.polygon(surface, color, pts, lw)
    elif tool == "circle":
        cx,cy = (x1+x2)//2,(y1+y2)//2
        r = int(math.hypot(x2-x1,y2-y1)/2)
        if r > 0: pygame.draw.circle(surface, color, (cx,cy), r, lw)

PALETTE_RECTS = {}
SIZE_RECTS    = {}
FILL_RECT     = [None]
CLEAR_RECT    = [None]

def draw_toolbar(surface, state):
    pygame.draw.rect(surface, PANEL_BG, (0,0,TOOLBAR_W,HEIGHT))
    pygame.draw.line(surface, (70,70,85), (TOOLBAR_W-1,0),(TOOLBAR_W-1,HEIGHT), 2)
    y = 10
    surface.blit(font.render("ИНСТРУМЕНТЫ", True, (120,120,140)), (10,y)); y+=22

    for tool in TOOLS:
        active = state["tool"] == tool["id"]
        mx,my  = pygame.mouse.get_pos()
        btn    = pygame.Rect(8, y, TOOLBAR_W-16, 30)
        col    = BTN_ACTIVE if active else (BTN_HOVER if btn.collidepoint(mx,my) else BTN_NORMAL)
        pygame.draw.rect(surface, col, btn, border_radius=5)
        surface.blit(font.render(tool["label"], True, BTN_TEXT), (14, y+7))
        tool["rect"] = btn
        y += 34

    y += 6
    pygame.draw.line(surface, (70,70,85), (8,y),(TOOLBAR_W-8,y)); y+=8
    surface.blit(font.render("ЦВЕТ", True, (120,120,140)), (10,y)); y+=18

    for i, c in enumerate(PALETTE):
        cx = 10 + (i%4)*34
        cy = y  + (i//4)*34
        r  = pygame.Rect(cx, cy, 28, 28)
        pygame.draw.rect(surface, c, r, border_radius=5)
        if c == state["draw_color"]:
            pygame.draw.rect(surface, WHITE, r, 3, border_radius=5)
        PALETTE_RECTS[i] = r
    y += (len(PALETTE)//4)*34 + 8

    pygame.draw.line(surface, (70,70,85),(8,y),(TOOLBAR_W-8,y)); y+=8
    surface.blit(font.render("ВЫБРАН:", True, (120,120,140)),(10,y)); y+=18
    pygame.draw.rect(surface, state["draw_color"], (10,y,50,26), border_radius=5)
    pygame.draw.rect(surface, GRAY, (10,y,50,26), 2, border_radius=5); y+=34

    surface.blit(font.render(f"ТОЛЩИНА: {state['size']}", True, (120,120,140)),(10,y)); y+=18
    for i, s in enumerate([1,3,6,12]):
        br = pygame.Rect(10+i*35, y, 30, 26)
        pygame.draw.rect(surface, BTN_ACTIVE if state["size"]==s else BTN_NORMAL, br, border_radius=4)
        pygame.draw.circle(surface, BTN_TEXT, (10+i*35+15, y+13), s//2+1)
        SIZE_RECTS[i] = (br, s)
    y += 34

    pygame.draw.line(surface, (70,70,85),(8,y),(TOOLBAR_W-8,y)); y+=8
    fr = pygame.Rect(8,y,TOOLBAR_W-16,28)
    pygame.draw.rect(surface, BTN_ACTIVE if state["filled"] else BTN_NORMAL, fr, border_radius=5)
    surface.blit(font.render("⬛ Заливка", True, BTN_TEXT),(14,y+6))
    FILL_RECT[0] = fr; y+=36

    cr = pygame.Rect(8,y,TOOLBAR_W-16,28)
    pygame.draw.rect(surface, (160,50,50), cr, border_radius=5)
    surface.blit(font.render("🗑  Очистить", True, BTN_TEXT),(14,y+6))
    CLEAR_RECT[0] = cr

while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); exit()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx,my = event.pos
            if mx < TOOLBAR_W:
                for tool in TOOLS:
                    if tool.get("rect") and tool["rect"].collidepoint(mx,my):
                        state["tool"] = tool["id"]
                for i,(r,s) in SIZE_RECTS.items():
                    if r.collidepoint(mx,my): state["size"] = s
                for i,r in PALETTE_RECTS.items():
                    if r.collidepoint(mx,my): state["draw_color"] = PALETTE[i]
                if FILL_RECT[0]  and FILL_RECT[0].collidepoint(mx,my):
                    state["filled"] = not state["filled"]
                if CLEAR_RECT[0] and CLEAR_RECT[0].collidepoint(mx,my):
                    canvas.fill(WHITE)
            elif CANVAS_RECT.collidepoint(mx,my):
                cx,cy = mx-TOOLBAR_W, my
                state["drawing"] = True
                state["start"]   = (cx,cy)
                if state["tool"] in ("pencil","eraser"):
                    col = WHITE if state["tool"]=="eraser" else state["draw_color"]
                    sz  = state["size"]*4 if state["tool"]=="eraser" else state["size"]
                    pygame.draw.circle(canvas, col, (cx,cy), sz)

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if state["drawing"] and state["start"]:
                mx,my = event.pos
                cx,cy = mx-TOOLBAR_W, my
                if state["tool"] not in ("pencil","eraser"):
                    x1,y1 = state["start"]
                    draw_shape(canvas, state["tool"], x1,y1,cx,cy,
                               state["draw_color"], state["size"], state["filled"])
            state["drawing"] = False
            state["start"]   = None
            preview.fill((0,0,0,0))

        if event.type == pygame.MOUSEMOTION:
            mx,my = event.pos
            if state["drawing"] and CANVAS_RECT.collidepoint(mx,my):
                cx,cy = mx-TOOLBAR_W, my
                if state["tool"] == "pencil":
                    if state["start"]:
                        pygame.draw.line(canvas, state["draw_color"],
                                         state["start"],(cx,cy), state["size"])
                    state["start"] = (cx,cy)
                elif state["tool"] == "eraser":
                    pygame.draw.circle(canvas, WHITE, (cx,cy), state["size"]*4)
                    state["start"] = (cx,cy)
                else:
                    preview.fill((0,0,0,0))
                    x1,y1 = state["start"]
                    tmp = pygame.Surface((CANVAS_RECT.width, CANVAS_RECT.height), pygame.SRCALPHA)
                    draw_shape(tmp, state["tool"], x1,y1,cx,cy,
                               state["draw_color"], state["size"], state["filled"])
                    preview.blit(tmp,(0,0))

    screen.fill(PANEL_BG)
    screen.blit(canvas, (TOOLBAR_W,0))
    screen.blit(preview,(TOOLBAR_W,0))
    draw_toolbar(screen, state)
    pygame.display.flip()