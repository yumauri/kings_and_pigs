import pygame
from ..functions import loader
from .animation import Animation
from .animated_entity import AnimatedEntity


# diamond sprites loader
load_image = loader("kings_and_pigs/data/sprites/12-Live and Coins")


class StatsDiamond(AnimatedEntity):
    def __init__(self, x, y):
        idle = load_image("Small Diamond (18x14).png")
        numbers = load_image("Numbers (6x8).png")

        self.animation_idle = Animation(idle, 8)
        self.numbers = Animation(numbers, 10)

        super().__init__(x, y, self.animation_idle)

    def digit(self, d):
        d = d - 1 if d != 0 else 9
        return self.numbers.frames[d]

    def number(self, n):
        layer = pygame.Surface([12, 8], pygame.SRCALPHA, 32)
        if n < 10:
            layer.blit(self.digit(n), (0, 0))
        else:
            layer.blit(self.digit(n // 10), (0, 0))
            layer.blit(self.digit(n % 10), (5, 0))
        return layer
