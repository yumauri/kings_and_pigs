from ..functions import loader, play
from .animation import Animation
from .animated_entity import AnimatedEntity
from .appliable import Appliable


# diamond sprites loader
load_image = loader("kings_and_pigs/data/sprites/12-Live and Coins")


class Diamond(AnimatedEntity, Appliable):
    def __init__(self, x, y):
        idle = load_image("Big Diamond Idle (18x14).png")
        hit = load_image("Big Heart Hit (18x14).png")

        self.animation_idle = Animation(idle, 10)
        self.animation_hit = Animation(hit, 2)
        self.available = True

        super().__init__(x, y, self.animation_idle)

    def apply(self, hero):
        if not self.available:
            return

        def apply_is_done():
            self.kill()
            hero.score = min(hero.score + 1, hero.max_score)

        if hero.score < hero.max_score:
            self.available = False
            self.change_animation(self.animation_hit)
            self.animation_hit.on_done(apply_is_done)
            play("diamond")

    def update(self, chamber, hero):
        super().update()
        self.apply_gravity(chamber.gravity)
        self.move(chamber)
