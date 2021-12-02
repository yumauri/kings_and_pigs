import pygame


class Hittable:
    HIT_FROM_TOP = 0
    HIT_FROM_RIGHT = 1
    HIT_FROM_BOTTOM = 2
    HIT_FROM_LEFT = 3
    HIT_FROM_TOP_RIGHT = 4
    HIT_FROM_BOTTOM_RIGHT = 5
    HIT_FROM_BOTTOM_LEFT = 6
    HIT_FROM_TOP_LEFT = 7

    def adjust_hit_box(self, *, left=0, right=0, top=0, bottom=0):
        self.hit_box_d_left = left
        self.hit_box_d_right = right
        self.hit_box_d_top = top
        self.hit_box_d_bottom = bottom

    def get_hit_box(self):
        return pygame.Rect(
            self.rect.left + self.hit_box_d_left,
            self.rect.top + self.hit_box_d_top,
            self.rect.width - (self.hit_box_d_left + self.hit_box_d_right),
            self.rect.height - (self.hit_box_d_top + self.hit_box_d_bottom),
        )

    def hit(self, direction, chamber):
        pass
