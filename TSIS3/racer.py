import pygame
import random
import math

W, H = 800, 600

ROAD_LEFT  = 150
ROAD_RIGHT = 650
LANE_COUNT = 4
LANE_W     = (ROAD_RIGHT - ROAD_LEFT) // LANE_COUNT

DIFFICULTY_PARAMS = {
    "easy":   {"enemy_interval": 120, "obs_interval": 180, "base_speed": 4,  "traffic_mult": 0.8},
    "normal": {"enemy_interval": 80,  "obs_interval": 120, "base_speed": 6,  "traffic_mult": 1.0},
    "hard":   {"enemy_interval": 50,  "obs_interval": 80,  "base_speed": 8,  "traffic_mult": 1.3},
}

POWERUP_COLORS = {
    "nitro":  (255, 200,  30),
    "shield": ( 30, 180, 255),
    "repair": ( 60, 220,  80),
}

ENEMY_COLORS = [
    (200, 80,  80),
    (80,  80,  200),
    (80,  200, 80),
    (200, 200, 80),
    (200, 80,  200),
]


def lane_center(lane):
    return ROAD_LEFT + lane * LANE_W + LANE_W // 2


class PlayerCar:
    W, H = 36, 60

    def __init__(self, color):
        self.color   = color
        self.lane    = 1
        self.x       = float(lane_center(self.lane))
        self.y       = float(H - 100)
        self.shield  = False
        self.nitro   = False
        self.nitro_t = 0
        self.shield_hits = 0

    def move_left(self):
        if self.lane > 0:
            self.lane -= 1

    def move_right(self):
        if self.lane < LANE_COUNT - 1:
            self.lane += 1

    def update(self):
        target = float(lane_center(self.lane))
        self.x += (target - self.x) * 0.2
        if self.nitro_t > 0:
            self.nitro_t -= 1
            if self.nitro_t == 0:
                self.nitro = False

    def activate_nitro(self, duration):
        self.nitro   = True
        self.nitro_t = duration

    def activate_shield(self):
        self.shield      = True
        self.shield_hits = 1

    def take_hit(self):
        if self.shield and self.shield_hits > 0:
            self.shield_hits -= 1
            if self.shield_hits == 0:
                self.shield = False
            return False
        return True

    def get_rect(self):
        return pygame.Rect(self.x - self.W // 2, self.y - self.H // 2, self.W, self.H)

    def draw(self, surface):
        r = self.get_rect()
        pygame.draw.rect(surface, self.color, r, border_radius=6)
        pygame.draw.rect(surface, (220, 220, 220), r, 2, border_radius=6)
        pygame.draw.rect(surface, (30, 30, 50),
                         (r.x + 5, r.y + 8, r.width - 10, 14), border_radius=3)
        pygame.draw.rect(surface, (30, 30, 50),
                         (r.x + 5, r.bottom - 22, r.width - 10, 14), border_radius=3)
        if self.shield:
            pygame.draw.ellipse(surface, (60, 160, 255, 120),
                                r.inflate(14, 14), 3)
        if self.nitro:
            for _ in range(3):
                fx = r.centerx + random.randint(-8, 8)
                fy = r.bottom + random.randint(4, 16)
                pygame.draw.circle(surface, (255, 140, 0), (fx, fy), random.randint(3, 6))


class EnemyCar:
    W, H = 34, 56

    def __init__(self, lane, speed, color=None):
        self.lane  = lane
        self.x     = float(lane_center(lane))
        self.y     = float(-self.H)
        self.speed = speed
        self.color = color or random.choice(ENEMY_COLORS)

    def update(self, scroll_speed):
        self.y += self.speed + scroll_speed * 0.4

    def off_screen(self):
        return self.y > H + self.H

    def get_rect(self):
        return pygame.Rect(self.x - self.W // 2, self.y - self.H // 2, self.W, self.H)

    def draw(self, surface):
        r = self.get_rect()
        pygame.draw.rect(surface, self.color, r, border_radius=5)
        pygame.draw.rect(surface, (200, 200, 200), r, 2, border_radius=5)
        pygame.draw.rect(surface, (20, 20, 40),
                         (r.x + 4, r.y + 8, r.width - 8, 12), border_radius=3)
        pygame.draw.rect(surface, (20, 20, 40),
                         (r.x + 4, r.bottom - 20, r.width - 8, 12), border_radius=3)


class Obstacle:
    TYPES = ["oil", "barrier", "pothole", "speedbump"]

    def __init__(self, lane, obs_type=None):
        self.lane     = lane
        self.type     = obs_type or random.choice(self.TYPES)
        self.x        = float(lane_center(lane))
        self.y        = float(-40)
        self.w        = 44 if self.type == "barrier" else 36
        self.h        = 18 if self.type in ("oil", "pothole") else 14

    def update(self, scroll_speed):
        self.y += scroll_speed

    def off_screen(self):
        return self.y > H + 60

    def get_rect(self):
        return pygame.Rect(self.x - self.w // 2, self.y - self.h // 2, self.w, self.h)

    def draw(self, surface):
        r = self.get_rect()
        if self.type == "oil":
            pygame.draw.ellipse(surface, (30, 20, 60), r)
            pygame.draw.ellipse(surface, (80, 40, 120), r, 2)
        elif self.type == "barrier":
            pygame.draw.rect(surface, (220, 60, 60), r, border_radius=3)
            pygame.draw.rect(surface, (255, 200, 50), r, 2, border_radius=3)
        elif self.type == "pothole":
            pygame.draw.ellipse(surface, (20, 20, 30), r)
            pygame.draw.ellipse(surface, (50, 50, 60), r, 2)
        elif self.type == "speedbump":
            pygame.draw.rect(surface, (200, 200, 60), r, border_radius=4)


class Coin:
    TYPES = {1: (255, 215, 0), 5: (192, 192, 192), 10: (255, 165, 0)}

    def __init__(self, lane, value=None):
        weights = [60, 30, 10]
        self.value = value or random.choices([1, 5, 10], weights=weights)[0]
        self.lane  = lane
        self.x     = float(lane_center(lane))
        self.y     = float(-20)
        self.r     = 10

    def update(self, scroll_speed):
        self.y += scroll_speed

    def off_screen(self):
        return self.y > H + 30

    def get_rect(self):
        return pygame.Rect(self.x - self.r, self.y - self.r, self.r * 2, self.r * 2)

    def draw(self, surface):
        color = self.TYPES.get(self.value, (255, 215, 0))
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), self.r)
        pygame.draw.circle(surface, (255, 255, 255), (int(self.x), int(self.y)), self.r, 2)
        font = pygame.font.SysFont("Consolas", 10, bold=True)
        t = font.render(str(self.value), True, (30, 30, 30))
        surface.blit(t, t.get_rect(center=(int(self.x), int(self.y))))


class PowerUp:
    def __init__(self, lane, kind=None):
        self.kind = kind or random.choice(["nitro", "shield", "repair"])
        self.lane = lane
        self.x    = float(lane_center(lane))
        self.y    = float(-30)
        self.r    = 14
        self.life = 300

    def update(self, scroll_speed):
        self.y    += scroll_speed
        self.life -= 1

    def expired(self):
        return self.life <= 0 or self.y > H + 40

    def get_rect(self):
        return pygame.Rect(self.x - self.r, self.y - self.r, self.r * 2, self.r * 2)

    def draw(self, surface):
        alpha = min(255, self.life * 2)
        color = POWERUP_COLORS[self.kind]
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), self.r)
        pygame.draw.circle(surface, (255, 255, 255), (int(self.x), int(self.y)), self.r, 2)
        font = pygame.font.SysFont("Consolas", 9, bold=True)
        label = {"nitro": "N", "shield": "S", "repair": "R"}[self.kind]
        t = font.render(label, True, (20, 20, 20))
        surface.blit(t, t.get_rect(center=(int(self.x), int(self.y))))


class NitroZone:
    W, H_ZONE = LANE_W - 8, 60

    def __init__(self, lane):
        self.lane = lane
        self.x    = ROAD_LEFT + lane * LANE_W + 4
        self.y    = float(-self.H_ZONE)

    def update(self, scroll_speed):
        self.y += scroll_speed

    def off_screen(self):
        return self.y > H + self.H_ZONE

    def get_rect(self):
        return pygame.Rect(self.x, int(self.y), self.W, self.H_ZONE)

    def draw(self, surface):
        r = self.get_rect()
        s = pygame.Surface((r.w, r.h), pygame.SRCALPHA)
        s.fill((255, 180, 0, 60))
        surface.blit(s, r.topleft)
        pygame.draw.rect(surface, (255, 200, 50), r, 2)
        font = pygame.font.SysFont("Consolas", 11, bold=True)
        t = font.render("NITRO", True, (255, 230, 80))
        surface.blit(t, t.get_rect(center=r.center))


class RoadRenderer:
    def __init__(self):
        self.scroll  = 0.0
        self.dash_h  = 40
        self.dash_gap = 30
        self.stripe_period = self.dash_h + self.dash_gap

    def update(self, speed):
        self.scroll = (self.scroll + speed) % self.stripe_period

    def draw(self, surface):
        pygame.draw.rect(surface, (38, 38, 52), (ROAD_LEFT, 0, ROAD_RIGHT - ROAD_LEFT, H))
        pygame.draw.rect(surface, (60, 60, 80), (ROAD_LEFT - 4, 0, 4, H))
        pygame.draw.rect(surface, (60, 60, 80), (ROAD_RIGHT, 0, 4, H))

        for lane in range(1, LANE_COUNT):
            lx = ROAD_LEFT + lane * LANE_W
            y = -self.stripe_period + self.scroll
            while y < H:
                pygame.draw.rect(surface, (90, 90, 110), (lx - 2, int(y), 4, self.dash_h))
                y += self.stripe_period


class GameState:
    RACE_DISTANCE = 3000

    def __init__(self, settings, player_name):
        self.settings     = settings
        self.player_name  = player_name
        diff              = settings.get("difficulty", "normal")
        self.params       = DIFFICULTY_PARAMS[diff]

        self.player       = PlayerCar(tuple(settings["car_color"]))
        self.road         = RoadRenderer()

        self.enemies      = []
        self.obstacles    = []
        self.coins        = []
        self.powerups     = []
        self.nitro_zones  = []

        self.scroll_speed  = float(self.params["base_speed"])
        self.score         = 0
        self.coin_count    = 0
        self.distance      = 0.0
        self.alive         = True

        self.active_powerup      = None
        self.active_powerup_time = 0

        self.enemy_timer  = 0
        self.obs_timer    = 0
        self.coin_timer   = 0
        self.pu_timer     = 0
        self.nz_timer     = 0

        self.key_cooldown = 0

    def _safe_lane(self, exclude_lanes=None):
        exclude = set(exclude_lanes or [])
        occupied = set()
        for e in self.enemies:
            if e.y < 200:
                occupied.add(e.lane)
        for o in self.obstacles:
            if o.y < 200:
                occupied.add(o.lane)
        free = [l for l in range(LANE_COUNT) if l not in occupied and l not in exclude]
        return random.choice(free) if free else random.randint(0, LANE_COUNT - 1)

    def update(self, keys):
        if not self.alive:
            return

        if self.key_cooldown > 0:
            self.key_cooldown -= 1
        else:
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.player.move_left()
                self.key_cooldown = 12
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.player.move_right()
                self.key_cooldown = 12

        speed = self.scroll_speed * (1.8 if self.player.nitro else 1.0)
        self.road.update(speed)
        self.player.update()

        self.distance += speed * 0.05
        self.score = int(self.distance) + self.coin_count * 10

        if self.active_powerup_time > 0:
            self.active_powerup_time -= 1
            if self.active_powerup_time == 0:
                self.active_powerup = None

        mult = self.params["traffic_mult"] * (1 + self.distance / 2000)

        self.enemy_timer += 1
        interval = max(25, int(self.params["enemy_interval"] / mult))
        if self.enemy_timer >= interval:
            self.enemy_timer = 0
            lane = self._safe_lane([self.player.lane])
            spd  = self.scroll_speed * random.uniform(0.3, 0.8) * mult
            self.enemies.append(EnemyCar(lane, spd))

        self.obs_timer += 1
        obs_interval = max(40, int(self.params["obs_interval"] / mult))
        if self.obs_timer >= obs_interval:
            self.obs_timer = 0
            lane = self._safe_lane([self.player.lane])
            self.obstacles.append(Obstacle(lane))

        self.coin_timer += 1
        if self.coin_timer >= 60:
            self.coin_timer = 0
            self.coins.append(Coin(random.randint(0, LANE_COUNT - 1)))

        self.pu_timer += 1
        if self.pu_timer >= 240:
            self.pu_timer = 0
            self.powerups.append(PowerUp(random.randint(0, LANE_COUNT - 1)))

        self.nz_timer += 1
        if self.nz_timer >= 300:
            self.nz_timer = 0
            self.nitro_zones.append(NitroZone(random.randint(0, LANE_COUNT - 1)))

        pr = self.player.get_rect()

        for e in self.enemies[:]:
            e.update(speed)
            if e.off_screen():
                self.enemies.remove(e)
                continue
            if pr.colliderect(e.get_rect()):
                self.enemies.remove(e)
                if self.player.take_hit():
                    self.alive = False
                    return

        for o in self.obstacles[:]:
            o.update(speed)
            if o.off_screen():
                self.obstacles.remove(o)
                continue
            if pr.colliderect(o.get_rect()):
                if o.type == "speedbump":
                    self.scroll_speed = max(2, self.scroll_speed * 0.7)
                else:
                    self.obstacles.remove(o)
                    if self.player.take_hit():
                        self.alive = False
                        return

        for c in self.coins[:]:
            c.update(speed)
            if c.off_screen():
                self.coins.remove(c)
            elif pr.colliderect(c.get_rect()):
                self.coins.remove(c)
                self.coin_count += c.value
                self.scroll_speed = min(20, self.scroll_speed + 0.05 * c.value)

        for p in self.powerups[:]:
            p.update(speed)
            if p.expired():
                self.powerups.remove(p)
            elif pr.colliderect(p.get_rect()):
                self.powerups.remove(p)
                self._apply_powerup(p.kind)

        for nz in self.nitro_zones[:]:
            nz.update(speed)
            if nz.off_screen():
                self.nitro_zones.remove(nz)
            elif pr.colliderect(nz.get_rect()):
                self.nitro_zones.remove(nz)
                self.player.activate_nitro(120)
                self.active_powerup = "nitro"
                self.active_powerup_time = 120

        if self.distance >= self.RACE_DISTANCE:
            self.score += 500
            self.alive = False

    def _apply_powerup(self, kind):
        self.active_powerup = kind
        if kind == "nitro":
            self.player.activate_nitro(180)
            self.active_powerup_time = 180
        elif kind == "shield":
            self.player.activate_shield()
            self.active_powerup_time = 600
        elif kind == "repair":
            self.player.shield = True
            self.player.shield_hits = 1
            self.active_powerup = "repair"
            self.active_powerup_time = 1

    def draw(self, surface, fonts):
        big, med, small, tiny = fonts

        surface.fill((15, 15, 25))
        pygame.draw.rect(surface, (20, 20, 30), (0, 0, ROAD_LEFT, H))
        pygame.draw.rect(surface, (20, 20, 30), (ROAD_RIGHT, 0, W - ROAD_RIGHT, H))

        self.road.draw(surface)

        for nz in self.nitro_zones:
            nz.draw(surface)
        for o in self.obstacles:
            o.draw(surface)
        for e in self.enemies:
            e.draw(surface)
        for c in self.coins:
            c.draw(surface)
        for p in self.powerups:
            p.draw(surface)
        self.player.draw(surface)

        self._draw_hud(surface, fonts)

    def _draw_hud(self, surface, fonts):
        big, med, small, tiny = fonts

        pygame.draw.rect(surface, (20, 20, 35), (0, 0, ROAD_LEFT - 4, H))

        def lbl(text, y, color=(180, 180, 200)):
            t = tiny.render(text, True, color)
            surface.blit(t, (8, y))

        lbl("SCORE",    10)
        lbl(str(self.score), 26, (255, 200, 50))
        lbl("COINS",    55)
        lbl(str(self.coin_count), 71, (255, 215, 0))
        lbl("SPEED",   100)
        lbl(f"{self.scroll_speed:.1f}", 116, (100, 200, 255))
        lbl("DIST",    145)
        lbl(f"{int(self.distance)}m", 161, (160, 255, 160))

        remain = max(0, self.RACE_DISTANCE - self.distance)
        lbl("LEFT",    190)
        lbl(f"{int(remain)}m", 206, (255, 150, 150))

        bar_h = 200
        bar_w = 12
        bx, by = 125, 10
        pygame.draw.rect(surface, (40, 40, 55), (bx, by, bar_w, bar_h))
        progress = min(1.0, self.distance / self.RACE_DISTANCE)
        fill_h = int(bar_h * progress)
        pygame.draw.rect(surface, (60, 200, 80), (bx, by + bar_h - fill_h, bar_w, fill_h))
        pygame.draw.rect(surface, (80, 80, 100), (bx, by, bar_w, bar_h), 1)

        if self.active_powerup and self.active_powerup_time > 0:
            pu_colors = {"nitro": (255, 200, 30), "shield": (30, 180, 255), "repair": (60, 220, 80)}
            c = pu_colors.get(self.active_powerup, (200, 200, 200))
            lbl("POWER", 250)
            lbl(self.active_powerup.upper(), 266, c)
            secs = self.active_powerup_time // 60
            lbl(f"{secs}s", 282, c)

        if self.player.shield:
            lbl("SHIELD", 310, (30, 180, 255))