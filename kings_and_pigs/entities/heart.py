import pygame
from ..functions import loader, play
from .animation import Animation
from .animated_entity import AnimatedEntity
from .appliable import Appliable


# heart sprites loader
load_image = loader("kings_and_pigs/data/sprites/12-Live and Coins")


class Heart(AnimatedEntity, Appliable):
    def __init__(self, x, y):
        idle = load_image("Big Heart Idle (18x14).png")
        hit = load_image("Big Heart Hit (18x14).png")

        self.animation_idle = Animation(idle, 8)
        self.animation_hit = Animation(hit, 2)
        self.available = True

        super().__init__(x, y, self.animation_idle)

    def apply(self, hero):
        if not self.available:
            return

        def apply_is_done():
            self.kill()
            hero.lives = min(hero.lives + 1, hero.max_lives)

        if hero.lives < hero.max_lives:
            self.available = False
            self.change_animation(self.animation_hit)
            self.animation_hit.on_done(apply_is_done)
            play("healed")

    def update(self, chamber, hero):
        super().update()
        self.apply_gravity(chamber.gravity)
        self.move(chamber)
