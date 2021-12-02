import pygame
from ..functions import loader
from .stats_heart import StatsHeart
from .stats_diamond import StatsDiamond


# stats sprites loader
load_image = loader("kings_and_pigs/data/sprites/12-Live and Coins")


class Stats:
    def __init__(self, hero):
        self.hero = hero

        self.bar = load_image("Live Bar.png")
        w = self.bar.get_width()
        h = self.bar.get_height() + 2  # adjust for diamonds

        self.hearts = [StatsHeart(11 + 11 * i, 10) for i in range(hero.lives)]
        self.diamond = StatsDiamond(16, 25)

        self.active_sprites = pygame.sprite.Group()
        self.active_sprites.add(*self.hearts)

        self.background_layer = pygame.Surface([w, h], pygame.SRCALPHA, 32)
        self.active_layer = pygame.Surface([w, h], pygame.SRCALPHA, 32)
        self.score_layer = None

        self.background_layer.blit(self.bar, (0, 0))

    def update(self):
        # updates hearts count in stats
        while len(self.hearts) > self.hero.lives and len(self.hearts) > 0:
            self.hearts.pop().disappear()
        while len(self.hearts) < self.hero.lives:
            i = len(self.hearts)
            heart = StatsHeart(11 + 11 * i, 10)
            self.hearts.append(heart)
            self.active_sprites.add(heart)

        # updates diamonds count in stats
        if self.hero.score > 0:
            if self.diamond not in self.active_sprites:
                self.active_sprites.add(self.diamond)
            self.score_layer = self.diamond.number(self.hero.score)
        elif self.diamond in self.active_sprites:
            self.diamond.kill()
            self.score_layer = None

        # update all active sprites, to have animation
        self.active_sprites.update()
