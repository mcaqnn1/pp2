import pygame
from collections import deque


class Tool:
    def __init__(self):
        self.active = False

    def on_mouse_down(self, pos, canvas, color, size):
        pass

    def on_mouse_move(self, pos, canvas, color, size, buttons):
        pass

    def on_mouse_up(self, pos, canvas, color, size):
        pass


class PencilTool(Tool):
    def __init__(self):
        super().__init__()
        self._prev = None

    def on_mouse_down(self, pos, canvas, color, size):
        self._prev = pos
        canvas.set_at(pos, color)

    def on_mouse_move(self, pos, canvas, color, size, buttons):
        if buttons[0] and self._prev:
            pygame.draw.line(canvas, color, self._prev, pos, size)
            self._prev = pos

    def on_mouse_up(self, pos, canvas, color, size):
        self._prev = None


class EraserTool(Tool):
    def __init__(self):
        super().__init__()
        self._prev = None

    def on_mouse_down(self, pos, canvas, color, size):
        self._prev = pos

    def on_mouse_move(self, pos, canvas, color, size, buttons):
        if buttons[0] and self._prev:
            pygame.draw.line(canvas, (255, 255, 255), self._prev, pos, size * 3)
            self._prev = pos

    def on_mouse_up(self, pos, canvas, color, size):
        self._prev = None


class LineTool(Tool):
    def __init__(self):
        super().__init__()
        self._start = None
        self._snapshot = None

    def on_mouse_down(self, pos, canvas, color, size):
        self._start = pos
        self._snapshot = canvas.copy()

    def on_mouse_move(self, pos, canvas, color, size, buttons):
        if buttons[0] and self._start:
            canvas.blit(self._snapshot, (0, 0))
            pygame.draw.line(canvas, color, self._start, pos, size)

    def on_mouse_up(self, pos, canvas, color, size):
        if self._start:
            canvas.blit(self._snapshot, (0, 0))
            pygame.draw.line(canvas, color, self._start, pos, size)
        self._start = None
        self._snapshot = None


class RectangleTool(Tool):
    def __init__(self):
        super().__init__()
        self._start = None
        self._snapshot = None

    def on_mouse_down(self, pos, canvas, color, size):
        self._start = pos
        self._snapshot = canvas.copy()

    def on_mouse_move(self, pos, canvas, color, size, buttons):
        if buttons[0] and self._start:
            canvas.blit(self._snapshot, (0, 0))
            pygame.draw.rect(canvas, color, _make_rect(self._start, pos), size)

    def on_mouse_up(self, pos, canvas, color, size):
        if self._start:
            canvas.blit(self._snapshot, (0, 0))
            pygame.draw.rect(canvas, color, _make_rect(self._start, pos), size)
        self._start = None
        self._snapshot = None


class SquareTool(Tool):
    def __init__(self):
        super().__init__()
        self._start = None
        self._snapshot = None

    def _end_pos(self, start, pos):
        side = min(abs(pos[0] - start[0]), abs(pos[1] - start[1]))
        dx = side if pos[0] >= start[0] else -side
        dy = side if pos[1] >= start[1] else -side
        return (start[0] + dx, start[1] + dy)

    def on_mouse_down(self, pos, canvas, color, size):
        self._start = pos
        self._snapshot = canvas.copy()

    def on_mouse_move(self, pos, canvas, color, size, buttons):
        if buttons[0] and self._start:
            canvas.blit(self._snapshot, (0, 0))
            pygame.draw.rect(canvas, color, _make_rect(self._start, self._end_pos(self._start, pos)), size)

    def on_mouse_up(self, pos, canvas, color, size):
        if self._start:
            canvas.blit(self._snapshot, (0, 0))
            pygame.draw.rect(canvas, color, _make_rect(self._start, self._end_pos(self._start, pos)), size)
        self._start = None
        self._snapshot = None


class CircleTool(Tool):
    def __init__(self):
        super().__init__()
        self._start = None
        self._snapshot = None

    def on_mouse_down(self, pos, canvas, color, size):
        self._start = pos
        self._snapshot = canvas.copy()

    def on_mouse_move(self, pos, canvas, color, size, buttons):
        if buttons[0] and self._start:
            canvas.blit(self._snapshot, (0, 0))
            r = _make_rect(self._start, pos)
            if r.width > 0 and r.height > 0:
                pygame.draw.ellipse(canvas, color, r, size)

    def on_mouse_up(self, pos, canvas, color, size):
        if self._start:
            canvas.blit(self._snapshot, (0, 0))
            r = _make_rect(self._start, pos)
            if r.width > 0 and r.height > 0:
                pygame.draw.ellipse(canvas, color, r, size)
        self._start = None
        self._snapshot = None


class RightTriangleTool(Tool):
    def __init__(self):
        super().__init__()
        self._start = None
        self._snapshot = None

    def on_mouse_down(self, pos, canvas, color, size):
        self._start = pos
        self._snapshot = canvas.copy()

    def on_mouse_move(self, pos, canvas, color, size, buttons):
        if buttons[0] and self._start:
            canvas.blit(self._snapshot, (0, 0))
            pygame.draw.polygon(canvas, color, [self._start, (self._start[0], pos[1]), pos], size)

    def on_mouse_up(self, pos, canvas, color, size):
        if self._start:
            canvas.blit(self._snapshot, (0, 0))
            pygame.draw.polygon(canvas, color, [self._start, (self._start[0], pos[1]), pos], size)
        self._start = None
        self._snapshot = None


class EquilateralTriangleTool(Tool):
    def __init__(self):
        super().__init__()
        self._start = None
        self._snapshot = None

    def on_mouse_down(self, pos, canvas, color, size):
        self._start = pos
        self._snapshot = canvas.copy()

    def on_mouse_move(self, pos, canvas, color, size, buttons):
        if buttons[0] and self._start:
            canvas.blit(self._snapshot, (0, 0))
            pygame.draw.polygon(canvas, color, _equilateral_pts(self._start, pos), size)

    def on_mouse_up(self, pos, canvas, color, size):
        if self._start:
            canvas.blit(self._snapshot, (0, 0))
            pygame.draw.polygon(canvas, color, _equilateral_pts(self._start, pos), size)
        self._start = None
        self._snapshot = None


class DiamondTool(Tool):
    def __init__(self):
        super().__init__()
        self._start = None
        self._snapshot = None

    def on_mouse_down(self, pos, canvas, color, size):
        self._start = pos
        self._snapshot = canvas.copy()

    def on_mouse_move(self, pos, canvas, color, size, buttons):
        if buttons[0] and self._start:
            canvas.blit(self._snapshot, (0, 0))
            pygame.draw.polygon(canvas, color, _diamond_pts(self._start, pos), size)

    def on_mouse_up(self, pos, canvas, color, size):
        if self._start:
            canvas.blit(self._snapshot, (0, 0))
            pygame.draw.polygon(canvas, color, _diamond_pts(self._start, pos), size)
        self._start = None
        self._snapshot = None


class FillTool(Tool):
    def on_mouse_down(self, pos, canvas, color, size):
        _flood_fill(canvas, pos, color)


class TextTool(Tool):
    def __init__(self):
        super().__init__()
        self._pos = None
        self._text = ""
        self._active = False
        self._snapshot = None

    def _font(self, size):
        return pygame.font.SysFont("Arial", max(14, size * 3))

    def on_mouse_down(self, pos, canvas, color, size):
        if self._active and self._text:
            self._commit(canvas, color, size)
        self._pos = pos
        self._text = ""
        self._active = True
        self._snapshot = canvas.copy()

    def on_key(self, event, canvas, color, size):
        if not self._active:
            return
        if event.key == pygame.K_RETURN:
            self._commit(canvas, color, size)
        elif event.key == pygame.K_ESCAPE:
            self._cancel(canvas)
        elif event.key == pygame.K_BACKSPACE:
            self._text = self._text[:-1]
            self._preview(canvas, color, size)
        elif event.unicode:
            self._text += event.unicode
            self._preview(canvas, color, size)

    def _preview(self, canvas, color, size):
        canvas.blit(self._snapshot, (0, 0))
        canvas.blit(self._font(size).render(self._text + "|", True, color), self._pos)

    def _commit(self, canvas, color, size):
        canvas.blit(self._font(size).render(self._text, True, color), self._pos)
        self._active = False
        self._text = ""
        self._snapshot = None

    def _cancel(self, canvas):
        if self._snapshot:
            canvas.blit(self._snapshot, (0, 0))
        self._active = False
        self._text = ""
        self._snapshot = None

    @property
    def is_editing(self):
        return self._active


def _make_rect(p1, p2):
    return pygame.Rect(min(p1[0], p2[0]), min(p1[1], p2[1]),
                       abs(p2[0] - p1[0]), abs(p2[1] - p1[1]))


def _equilateral_pts(start, end):
    import math
    base = end[0] - start[0]
    h = int(abs(base) * math.sqrt(3) / 2)
    sign = 1 if end[1] >= start[1] else -1
    return [start, end, (start[0] + base // 2, start[1] + sign * h)]


def _diamond_pts(start, end):
    cx = (start[0] + end[0]) // 2
    cy = (start[1] + end[1]) // 2
    return [(cx, start[1]), (end[0], cy), (cx, end[1]), (start[0], cy)]


def _flood_fill(canvas, start_pos, fill_color):
    w, h = canvas.get_size()
    sx, sy = start_pos
    if not (0 <= sx < w and 0 <= sy < h):
        return
    target = canvas.get_at((sx, sy))[:3]
    fill_rgb = fill_color[:3] if len(fill_color) > 3 else fill_color
    if target == fill_rgb:
        return
    queue = deque([(sx, sy)])
    visited = {(sx, sy)}
    while queue:
        x, y = queue.popleft()
        canvas.set_at((x, y), fill_color)
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if (nx, ny) not in visited and 0 <= nx < w and 0 <= ny < h:
                if canvas.get_at((nx, ny))[:3] == target:
                    visited.add((nx, ny))
                    queue.append((nx, ny))