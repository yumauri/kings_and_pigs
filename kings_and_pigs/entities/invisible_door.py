import pygame


class InvisibleDoor(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, type):
        super().__init__()
        self.image = pygame.Surface((w, h), pygame.SRCALPHA, 32)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.type = type
        self.chamber = None  # filled by castle
        self.backdoor = None  # when connecting all doors

    def set_destination(self, chamber):
        pass
