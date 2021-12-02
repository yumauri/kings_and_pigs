import pygame
from .entity import Entity


class Dead(Entity):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)

    def update(self, chamber, hero):
        self.apply_gravity(chamber.gravity)
        self.move(chamber)
