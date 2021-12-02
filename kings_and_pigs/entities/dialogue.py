import pygame
from ..functions import loader
from .animation import Animation
from .animated_entity import AnimatedEntity


# dialogue sprites loader
load_image = loader("kings_and_pigs/data/sprites/13-Dialogue Boxes")


class Dialogue(AnimatedEntity):
    def __init__(self, x, y, show, hide):
        self.animation_show = Animation(show, 3)
        self.animation_hide = Animation(hide, 2)

        # make dialog to bo visible a bit longer
        # by duplicating latest frame 5 more times
        self.animation_show.frames.extend([self.animation_show.frames[-1]] * 5)

        super().__init__(x, y, self.animation_show)

        def disappeared():
            self.kill()

        def appeared():
            self.change_animation(self.animation_hide)
            self.animation_hide.on_done(disappeared, True)

        self.animation_show.on_done(appeared, True)


class AwareDialogue(Dialogue):
    def __init__(self, x, y):
        show = load_image("!!! In (24x8).png")
        hide = load_image("!!! Out (24x8).png")
        super().__init__(x, y, show, hide)


class AttackDialogue(Dialogue):
    def __init__(self, x, y):
        show = load_image("Attack In (24x8).png")
        hide = load_image("Attack Out (24x8).png")
        super().__init__(x, y, show, hide)


class ConfuseDialogue(Dialogue):
    def __init__(self, x, y):
        show = load_image("Interrogation In (24x8).png")
        hide = load_image("Interrogation Out (24x8).png")
        super().__init__(x, y, show, hide)
