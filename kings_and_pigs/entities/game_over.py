import pygame
from .outro import Outro


class GameOver(Outro):
    def __init__(self, w, h, score):
        super().__init__(w, h, score, False)

        self.text_game_over = self.font.render("game over", False, (100, 100, 100))
        self.text_any_key = self.font_score.render(
            "press any key", False, (100, 100, 100)
        )

        self.appear = pygame.time.get_ticks()
        self.show_hint = False
        self.alpha = 0
        self.d = 5

    def update_message(self):
        if not self.show_hint:
            now = pygame.time.get_ticks()
            if now - self.appear >= 1500:
                self.show_hint = True
        else:
            if self.alpha <= 0:
                self.d = 5
            elif self.alpha >= 255:
                self.d = -5
            self.alpha = min(max(self.alpha + self.d, 0), 255)

    def draw_message(self):
        self.active_layer.blit(self.text_game_over, (155, 100))
        if self.show_hint:
            self.text_any_key.set_alpha(self.alpha)
            self.active_layer.blit(self.text_any_key, (175, 120))
