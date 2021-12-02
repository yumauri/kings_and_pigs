import random
from kings_and_pigs.entities.dialogue import ConfuseDialogue
from .state import State


class Confuse(State):
    def __init__(self, agent):
        super().__init__(agent)
        self.wait(random.randint(500, 1000))
        self.agent.enemy.say(ConfuseDialogue)

    def update(self, chamber):
        from .aware import Aware
        from .patrol import Patrol

        if self.agent.seeing_hero and self.agent.hero.lives > 0:
            self.agent.state = Aware(self.agent)

        self.update_waiting()
        if self.waiting:
            return

        self.agent.state = Patrol(self.agent)
