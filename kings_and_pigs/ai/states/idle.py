import random
from .state import State


class Idle(State):
    def __init__(self, agent):
        super().__init__(agent)

    def update(self, chamber):
        from .aware import Aware
        from .patrol import Patrol

        if self.agent.seeing_hero and self.agent.hero.lives > 0:
            self.agent.state = Aware(self.agent)
            return

        # with 2% probability turn to the other side
        if random.random() < 0.02:
            self.agent.enemy.turn()
            return

        # with 1% probability change state to patrolling
        if random.random() < 0.01:
            self.agent.state = Patrol(self.agent)
            return
