import pygame
from ..functions import loader


# stats sprites loader
load_image = loader("kings_and_pigs/data/sprites")


class Splash:
    def __init__(self, w, h):
        self.background_layer = pygame.Surface([w, h], pygame.SRCALPHA, 32)
        self.active_layer = pygame.Surface([w, h], pygame.SRCALPHA, 32)
        self.background_layer.fill((0, 0, 0))

        title = load_image("Kings and Pigs.png")

        font = pygame.font.Font("kings_and_pigs/data/font.ttf", 10)
        self.text = font.render("press any key", False, (100, 100, 100))

        x = w / 2 - title.get_width() / 2
        y = h / 2 - title.get_height() / 2
        self.tx = w / 2 - self.text.get_width() / 2
        self.ty = h / 2 - self.text.get_height() / 2 + title.get_height() + 5

        self.background_layer.blit(title, (x, y))

        self.appear = pygame.time.get_ticks()
        self.show_hint = False
        self.alpha = 0
        self.d = 5

    def update(self):
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

    def draw(self):
        self.active_layer.fill((0, 0, 0, 0))
        if self.show_hint:
            self.text.set_alpha(self.alpha)
            self.active_layer.blit(self.text, (self.tx, self.ty))
