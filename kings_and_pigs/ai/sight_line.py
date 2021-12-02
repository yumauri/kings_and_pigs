import pygame


class SightLine(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height), pygame.SRCALPHA, 32)
        self.mask = pygame.mask.from_surface(self.image)
        self.initial_mask = self.mask
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def collides_with(self, block, offset_x, offset_y):
        x = self.rect[0] + int(offset_x) - block.rect[0]
        y = self.rect[1] + int(offset_y) - block.rect[1]
        dot = block.mask.overlap(self.mask, (x, y))
        if dot:
            return dot[0] + block.rect.x - offset_x, dot[1] + block.rect.y - offset_y

    def update(self, visible=False, start=None, end=None):
        self.image.fill((0, 0, 0, 0))
        if visible:
            pygame.draw.line(self.image, (255, 0, 0), start, end)
            self.mask = pygame.mask.from_surface(self.image)
        else:
            self.mask = self.initial_mask
