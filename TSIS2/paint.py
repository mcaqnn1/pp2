import sys
import pygame
from datetime import datetime
from tools import (
    PencilTool, LineTool, RectangleTool, SquareTool, CircleTool,
    RightTriangleTool, EquilateralTriangleTool, DiamondTool,
    EraserTool, FillTool, TextTool,
)

WINDOW_W, WINDOW_H = 1200, 780
TOOLBAR_W = 220
CANVAS_W = WINDOW_W - TOOLBAR_W
CANVAS_H = WINDOW_H

BRUSH_SIZES = {1: 2, 2: 5, 3: 10}

PALETTE = [
    (0,   0,   0),   (255, 255, 255), (128, 128, 128), (192, 192, 192),
    (255,   0,   0), (128,   0,   0), (255, 128,   0), (128,  64,   0),
    (255, 255,   0), (128, 128,   0), (0,   255,   0), (0,   128,   0),
    (0,   255, 255), (0,   128, 128), (0,     0, 255), (0,     0, 128),
    (255,   0, 255), (128,   0, 128), (255, 192, 203), (165,  42,  42),
]

BG_TOOLBAR   = (30,  30,  38)
BG_CANVAS    = (255, 255, 255)
ACCENT       = (90, 180, 255)
TEXT_COLOR   = (210, 210, 220)
BORDER_COLOR = (55,  55,  70)
BTN_NORMAL   = (45,  45,  58)
BTN_HOVER    = (60,  60,  78)
BTN_ACTIVE   = (90, 130, 200)


class Button:
    def __init__(self, rect, label, key=None):
        self.rect    = pygame.Rect(rect)
        self.label   = label
        self.key     = key
        self.active  = False
        self.hovered = False

    def draw(self, surface, font):
        color = BTN_ACTIVE if self.active else (BTN_HOVER if self.hovered else BTN_NORMAL)
        pygame.draw.rect(surface, color, self.rect, border_radius=6)
        pygame.draw.rect(surface, BORDER_COLOR, self.rect, 1, border_radius=6)
        text = font.render(self.label, True, TEXT_COLOR)
        surface.blit(text, text.get_rect(center=self.rect.center))

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False


class ColourSwatch:
    SIZE = 22

    def __init__(self, rect, color):
        self.rect  = pygame.Rect(rect)
        self.color = color

    def draw(self, surface, selected):
        pygame.draw.rect(surface, self.color, self.rect, border_radius=3)
        border = (255, 255, 255) if selected else BORDER_COLOR
        pygame.draw.rect(surface, border, self.rect, 2 if selected else 1, border_radius=3)

    def hit(self, pos):
        return self.rect.collidepoint(pos)


class PaintApp:
    TOOLS = [
        ("Pencil",        "pencil"),
        ("Line",          "line"),
        ("Rectangle",     "rect"),
        ("Square",        "square"),
        ("Circle",        "circle"),
        ("Right Tri",     "rtri"),
        ("Equil Tri",     "etri"),
        ("Diamond",       "diamond"),
        ("Eraser",        "eraser"),
        ("Fill",          "fill"),
        ("Text",          "text"),
    ]

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))
        pygame.display.set_caption("Paint — TSIS 2")

        self.font_ui   = pygame.font.SysFont("Segoe UI", 13)
        self.font_head = pygame.font.SysFont("Segoe UI", 14, bold=True)

        self.canvas = pygame.Surface((CANVAS_W, CANVAS_H))
        self.canvas.fill(BG_CANVAS)
        self.canvas_offset = (TOOLBAR_W, 0)

        self.current_color  = (0, 0, 0)
        self.brush_size_key = 2
        self.current_tool   = "pencil"

        self._tools = {
            "pencil":  PencilTool(),
            "line":    LineTool(),
            "rect":    RectangleTool(),
            "square":  SquareTool(),
            "circle":  CircleTool(),
            "rtri":    RightTriangleTool(),
            "etri":    EquilateralTriangleTool(),
            "diamond": DiamondTool(),
            "eraser":  EraserTool(),
            "fill":    FillTool(),
            "text":    TextTool(),
        }

        self._status = ""
        self._status_timer = 0
        self._build_toolbar()

    def _build_toolbar(self):
        self.tool_buttons    = []
        self.size_buttons    = []
        self.colour_swatches = []

        x0, y0 = 10, 50
        bw, bh, gap = TOOLBAR_W - 20, 28, 3

        for i, (label, key) in enumerate(self.TOOLS):
            btn = Button((x0, y0 + i * (bh + gap), bw, bh), label, key=key)
            btn.active = (key == self.current_tool)
            self.tool_buttons.append(btn)

        size_y = y0 + len(self.TOOLS) * (bh + gap) + 18
        for i, (lbl, k) in enumerate([("Thin  (1)", 1), ("Med   (2)", 2), ("Thick (3)", 3)]):
            btn = Button((x0, size_y + i * (bh + gap), bw, bh), lbl, key=str(k))
            btn.active = (k == self.brush_size_key)
            self.size_buttons.append(btn)

        pal_y = size_y + 3 * (bh + gap) + 18
        sw = ColourSwatch.SIZE
        cols = (TOOLBAR_W - 20) // (sw + 3)
        for i, c in enumerate(PALETTE):
            rect = (x0 + (i % cols) * (sw + 3), pal_y + (i // cols) * (sw + 3), sw, sw)
            self.colour_swatches.append(ColourSwatch(rect, c))

        self._pal_y = pal_y

    @property
    def brush_size(self):
        return BRUSH_SIZES[self.brush_size_key]

    @property
    def active_tool(self):
        return self._tools[self.current_tool]

    def _canvas_pos(self, pos):
        return (pos[0] - self.canvas_offset[0], pos[1] - self.canvas_offset[1])

    def _on_canvas(self, pos):
        x, y = self._canvas_pos(pos)
        return 0 <= x < CANVAS_W and 0 <= y < CANVAS_H

    def _save(self):
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"canvas_{ts}.png"
        pygame.image.save(self.canvas, filename)
        self._status = f"Saved: {filename}"
        self._status_timer = 180

    def _set_tool(self, key):
        self.current_tool = key
        for btn in self.tool_buttons:
            btn.active = (btn.key == key)

    def _set_size(self, k):
        self.brush_size_key = k
        for btn in self.size_buttons:
            btn.active = (btn.key == str(k))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if isinstance(self.active_tool, TextTool) and self.active_tool.is_editing:
                    self.active_tool.on_key(event, self.canvas, self.current_color, self.brush_size_key)
                    continue
                if event.key == pygame.K_1:
                    self._set_size(1)
                elif event.key == pygame.K_2:
                    self._set_size(2)
                elif event.key == pygame.K_3:
                    self._set_size(3)
                elif event.key == pygame.K_s and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                    self._save()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for btn in self.tool_buttons:
                    if btn.handle_event(event):
                        self._set_tool(btn.key)
                for btn in self.size_buttons:
                    if btn.handle_event(event):
                        self._set_size(int(btn.key))
                for sw in self.colour_swatches:
                    if sw.hit(event.pos):
                        self.current_color = sw.color
                if self._on_canvas(event.pos):
                    self.active_tool.on_mouse_down(
                        self._canvas_pos(event.pos), self.canvas, self.current_color, self.brush_size)

            if event.type == pygame.MOUSEMOTION:
                for btn in self.tool_buttons:
                    btn.handle_event(event)
                for btn in self.size_buttons:
                    btn.handle_event(event)
                if self._on_canvas(event.pos):
                    self.active_tool.on_mouse_move(
                        self._canvas_pos(event.pos), self.canvas, self.current_color,
                        self.brush_size, pygame.mouse.get_pressed())

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if self._on_canvas(event.pos):
                    self.active_tool.on_mouse_up(
                        self._canvas_pos(event.pos), self.canvas, self.current_color, self.brush_size)

    def draw(self):
        self.screen.fill(BG_TOOLBAR)
        pygame.draw.rect(self.screen, BORDER_COLOR, (TOOLBAR_W - 2, 0, CANVAS_W + 4, CANVAS_H + 4))
        self.screen.blit(self.canvas, self.canvas_offset)

        self.screen.blit(self.font_head.render("PAINT", True, ACCENT), (12, 14))
        self.screen.blit(self.font_head.render("TOOLS", True, (130, 130, 160)), (12, 34))

        for btn in self.tool_buttons:
            btn.draw(self.screen, self.font_ui)

        size_label_y = self.size_buttons[0].rect.y - 16
        self.screen.blit(self.font_head.render("BRUSH SIZE", True, (130, 130, 160)), (12, size_label_y))
        for btn in self.size_buttons:
            btn.draw(self.screen, self.font_ui)

        self.screen.blit(self.font_head.render("COLOUR", True, (130, 130, 160)), (12, self._pal_y - 16))
        for sw in self.colour_swatches:
            sw.draw(self.screen, sw.color == self.current_color)

        prev_y = self._pal_y + 58
        pygame.draw.rect(self.screen, self.current_color, (12, prev_y, 36, 36), border_radius=4)
        pygame.draw.rect(self.screen, BORDER_COLOR, (12, prev_y, 36, 36), 1, border_radius=4)
        self.screen.blit(self.font_ui.render("Active", True, TEXT_COLOR), (54, prev_y + 11))

        size_dot_y = prev_y + 48
        for i, (k, s) in enumerate(BRUSH_SIZES.items()):
            c = ACCENT if k == self.brush_size_key else (90, 90, 110)
            pygame.draw.circle(self.screen, c, (20 + i * 36, size_dot_y), s // 2 + 1)

        if self._status_timer > 0:
            self._status_timer -= 1
            surf = self.font_ui.render(self._status, True, (100, 220, 120))
            self.screen.blit(surf, (TOOLBAR_W + 8, CANVAS_H - 20))
        else:
            hint = self.font_ui.render("Ctrl+S = Save   1/2/3 = Brush size", True, (80, 80, 100))
            self.screen.blit(hint, (TOOLBAR_W + 8, CANVAS_H - 20))

        pygame.display.flip()

    def run(self):
        clock = pygame.time.Clock()
        while True:
            self.handle_events()
            self.draw()
            clock.tick(60)


if __name__ == "__main__":
    PaintApp().run()