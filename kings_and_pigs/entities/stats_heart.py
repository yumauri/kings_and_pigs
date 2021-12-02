from ..functions import loader
from .animation import Animation
from .animated_entity import AnimatedEntity


# stats heart sprites loader
load_image = loader("kings_and_pigs/data/sprites/12-Live and Coins")


class StatsHeart(AnimatedEntity):
    def __init__(self, x, y):
        idle = load_image("Small Heart Idle (18x14).png")
        hit = load_image("Small Heart Hit (18x14).png")

        self.animation_idle = Animation(idle, 8)
        self.animation_hit = Animation(hit, 2)

        super().__init__(x, y, self.animation_idle)

    def disappear(self):
        def disappear_is_done():
            self.kill()

        self.change_animation(self.animation_hit)
        self.animation_hit.on_done(disappear_is_done)
