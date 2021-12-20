import uuid
from .creature import Creature


class Enemy(Creature):
    def __init__(self, x, y, animation_idle, type=None, id=None):
        super().__init__(x, y, animation_idle)
        self.type = "" if type is None else type
        self.id = uuid.uuid4() if id is None else id

    def murder(self):
        self.die()
