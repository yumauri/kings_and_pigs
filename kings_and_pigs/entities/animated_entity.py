from .entity import Entity


class AnimatedEntity(Entity):
    def __init__(self, x, y, animation):
        super().__init__(x, y, animation.frame)
        self.animation = animation

    def change_animation(self, animation):
        if self.animation is not animation:
            self.animation.reset()
            self.animation = animation
            self.image = animation.frame

    def update(self, *args, **kwargs):
        self.animation.update()
        self.image = self.animation.frame
