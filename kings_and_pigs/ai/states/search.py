import random
from .state import State


class Search(State):
    def __init__(self, agent, initial=None):
        super().__init__(agent)
        self.initial = initial
        self.wait(random.randint(1000, 2000))

    def update(self, chamber):
        from .attack import Attack
        from .confuse import Confuse

        if self.agent.seeing_hero:
            self.agent.state = Attack(self.agent)
            return

        self.update_waiting()
        if not self.waiting:
            # too long in Search state -> change to Confuse
            self.agent.state = Confuse(self.agent)
            return

        # if don't see hero - try to return to the initial position, if any
        if self.initial:
            hit_box = self.agent.enemy.get_hit_box()
            (left, bottom), facing_right = self.initial

            # if we fall off the cliff
            if abs(bottom - hit_box.bottom) > 5:
                self.agent.state = Confuse(self.agent)
                return

            if hit_box.left - left < -3:
                self.agent.enemy.move_right()
            elif hit_box.left - left > 3:
                self.agent.enemy.move_left()
            elif self.agent.enemy.facing_right != facing_right:
                self.agent.enemy.turn()
            else:
                self.agent.state = Confuse(self.agent)

        # if there wasn't any initial position - return to patrolling
        else:
            self.agent.state = Confuse(self.agent)
