from ..functions import loader, play
from .animation import Animation
from .animated_entity import AnimatedEntity


# door sprites loader
load_image = loader("kings_and_pigs/data/sprites/11-Door")


class Door(AnimatedEntity):
    def __init__(self, x, y, type):
        idle = load_image("Idle.png")
        opening = load_image("Opening (46x56).png")
        closing = load_image("Closiong (46x56).png")

        self.animation_closed = Animation(idle, 1)
        self.animation_closing = Animation(closing, 3)
        self.animation_opening = Animation(opening, 5)
        self.animation_opened = Animation(self.animation_opening.frames[-1], 1)

        super().__init__(x, y, self.animation_closed)

        self.type = type
        self.chamber = None  # filled by castle
        self.backdoor = None  # when connecting all doors

        self.in_action = False

    def open(self):
        if self.in_action:
            return

        def opened():
            self.in_action = False

        self.change_animation(self.animation_opening)
        self.animation_opening.on_done(opened, True)

        play("door_open")

    def close(self):
        if self.in_action:
            return

        def closed():
            self.in_action = False
            self.change_animation(self.animation_closed)

        self.change_animation(self.animation_closing)
        self.animation_closing.on_done(closed, True)

        play("door_close")

    def set_destination(self, chamber):
        pass
