import pygame


class Ball:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.radius = 25
        self.speed = 20
        self.color = (220, 30, 30)  # Red

        self.x = screen_width // 2
        self.y = screen_height // 2

    def move(self, direction):
        """Move the ball by 20px; ignore input that would push it off-screen."""
        if direction == 'up':
            if self.y - self.speed >= self.radius:
                self.y -= self.speed
        elif direction == 'down':
            if self.y + self.speed <= self.screen_height - self.radius:
                self.y += self.speed
        elif direction == 'left':
            if self.x - self.speed >= self.radius:
                self.x -= self.speed
        elif direction == 'right':
            if self.x + self.speed <= self.screen_width - self.radius:
                self.x += self.speed

    def draw(self, screen):
        """Draw the ball and a subtle shadow for depth."""
        shadow_surf = pygame.Surface((self.radius * 2 + 10, self.radius * 2 + 10), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow_surf, (0, 0, 0, 40),
                            (5, self.radius + 8, self.radius * 2, self.radius // 2))
        screen.blit(shadow_surf, (self.x - self.radius - 5, self.y - self.radius - 5))

        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

        highlight_pos = (self.x - self.radius // 3, self.y - self.radius // 3)
        pygame.draw.circle(screen, (255, 120, 120), highlight_pos, self.radius // 5)