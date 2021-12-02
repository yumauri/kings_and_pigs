import pygame
from .entity import Entity


class Block(Entity):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)
        self.mask = pygame.mask.from_surface(self.image)
