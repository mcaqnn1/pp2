"""
clock.py  –  MickeyClock rendering engine
==========================================
Draws an analogue clock face and rotates two Mickey-hand sprites:
  • Right hand  →  minute hand
  • Left hand   →  second hand

Rotation convention (pygame):
  • pygame.transform.rotate() rotates COUNTER-clockwise for positive angles.
  • Clock hands move clockwise, so we negate the computed angle.
  • 0 s / 0 min  ≡  12 o'clock  ≡  hand pointing straight UP.
    In pygame-image space the hand already points UP (glove at top, cuff at
    bottom), so the base angle is 0°.
"""

import math
import datetime
import pygame


FACE_BG          = (255, 255, 240)   
FACE_OUTLINE     = ( 30,  30,  30)   
TICK_MAJOR       = ( 30,  30,  30)
TICK_MINOR       = (120, 120, 120)
CENTER_DOT       = ( 20,  20,  20)
SHADOW_COLOUR    = (  0,   0,   0,  60)   


class MickeyClock:
    """
    Encapsulates the clock face and both rotating hand sprites.

    Parameters
    ----------
    screen   : pygame.Surface  – the display surface
    center   : (int, int)      – pixel position of the clock center
    radius   : int             – radius of the clock face
    hand_img : pygame.Surface  – the source Mickey-hand image (RGBA, pointing UP)
    """

    def __init__(
        self,
        screen: pygame.Surface,
        center: tuple[int, int],
        radius: int,
        hand_img: pygame.Surface,
    ) -> None:
        self.screen  = screen
        self.center  = center
        self.radius  = radius

        hand_length  = int(radius * 0.85)
        src_w, src_h = hand_img.get_size()
        scale_factor = hand_length / src_h
        new_w        = max(1, int(src_w * scale_factor))
        self._hand_src = pygame.transform.smoothscale(hand_img, (new_w, hand_length))

        self._shadow_src = self._tint_surface(self._hand_src.copy(), SHADOW_COLOUR)


    def draw(self) -> None:
        """Draw the full clock (face + hands) for the current wall-clock time."""
        now     = self._get_time()
        min_deg = self._minute_angle(now.minute, now.second)
        sec_deg = self._second_angle(now.second, getattr(now, "microsecond", 0))

        self._draw_face()
        self._draw_hand(sec_deg, is_left=True,  alpha=230) 
        self._draw_hand(min_deg, is_left=False, alpha=255)   
        self._draw_center_dot()


    @staticmethod
    def _get_time() -> datetime.datetime:
        """Return local time, guarding against leap-second edge cases."""
        try:
            return datetime.datetime.now()
        except Exception:                        
            return datetime.datetime(1970, 1, 1, 0, 0, 0)


    @staticmethod
    def _minute_angle(minute: int, second: int) -> float:
        """
        Clockwise degrees from 12 o'clock for the minute hand.
        Smooth movement: each second advances the minute hand by 0.1°.
        """
        return (minute % 60) * 6.0 + second * 0.1

    @staticmethod
    def _second_angle(second: int, microsecond: int = 0) -> float:
        """
        Clockwise degrees from 12 o'clock for the second hand.
        Sub-second smooth sweep using microseconds.
        Leap seconds (second == 60) are clamped to 59.
        """
        second = min(second, 59)          
        frac   = microsecond / 1_000_000 
        return (second + frac) * 6.0      


    def _draw_face(self) -> None:
        """Draw circular clock face with tick marks and hour numerals."""
        cx, cy = self.center
        r      = self.radius

        pygame.draw.circle(self.screen, (180, 180, 180), (cx + 4, cy + 4), r)

        pygame.draw.circle(self.screen, FACE_BG, (cx, cy), r)

        
        pygame.draw.circle(self.screen, FACE_OUTLINE, (cx, cy), r, 4)

        for i in range(60):
            angle_rad = math.radians(i * 6 - 90)
            if i % 5 == 0:                   
                inner = r - 18
                outer = r - 4
                colour = TICK_MAJOR
                width  = 3
            else:                            
                inner = r - 10
                outer = r - 4
                colour = TICK_MINOR
                width  = 1

            x1 = cx + int(inner * math.cos(angle_rad))
            y1 = cy + int(inner * math.sin(angle_rad))
            x2 = cx + int(outer * math.cos(angle_rad))
            y2 = cy + int(outer * math.sin(angle_rad))
            pygame.draw.line(self.screen, colour, (x1, y1), (x2, y2), width)

        font_size = max(14, r // 6)
        font = pygame.font.SysFont("Arial", font_size, bold=True)
        for hour in range(1, 13):
            angle_rad = math.radians(hour * 30 - 90)
            tx = cx + int((r - 34) * math.cos(angle_rad))
            ty = cy + int((r - 34) * math.sin(angle_rad))
            surf = font.render(str(hour), True, FACE_OUTLINE)
            rect = surf.get_rect(center=(tx, ty))
            self.screen.blit(surf, rect)

    def _draw_hand(self, clockwise_deg: float, *, is_left: bool, alpha: int) -> None:
        """
        Rotate the Mickey-hand sprite and blit it onto the clock.

        The hand image points UP in its own coordinate space (glove at top).
        pygame.transform.rotate() rotates counter-clockwise, so we negate
        the clockwise degree value to get correct clockwise motion.

        The pivot point is at the *bottom* of the rotated hand (where the
        cuff meets the clock centre).  We therefore blit so that the bottom-
        centre of the rotated image lands on self.center.
        """
        cx, cy = self.center

        rotated = pygame.transform.rotate(self._hand_src, -clockwise_deg)
        rotated.set_alpha(alpha)

        
        orig_w, orig_h = self._hand_src.get_size()
        rot_w,  rot_h  = rotated.get_size()

        pivot_local = pygame.math.Vector2(orig_w / 2, orig_h)

        pivot_rotated = pivot_local.rotate(clockwise_deg)   # pygame Vector rotates CCW for + values

        # Top-left of the blit so the rotated pivot lands on the clock centre
        blit_x = cx - (rot_w / 2 + pivot_rotated.x - orig_w / 2)
        blit_y = cy - (rot_h / 2 + pivot_rotated.y - orig_h / 2)

        if is_left:
            rotated = pygame.transform.flip(rotated, True, False)

        self.screen.blit(rotated, (int(blit_x), int(blit_y)))

    def _draw_center_dot(self) -> None:
        """Draw a small filled circle at the clock centre."""
        pygame.draw.circle(self.screen, CENTER_DOT, self.center, 8)
        pygame.draw.circle(self.screen, (200, 200, 200), self.center, 4)


    @staticmethod
    def _tint_surface(
        surface: pygame.Surface,
        colour: tuple[int, int, int, int],
    ) -> pygame.Surface:
        """Return a copy of *surface* tinted with *colour* (RGBA)."""
        tinted = surface.copy().convert_alpha()
        tinted.fill(colour, special_flags=pygame.BLEND_RGBA_MULT)
        return tinted