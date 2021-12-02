import re
import random
from .state import State


class Patrol(State):
    def __init__(self, agent):
        super().__init__(agent)
        self.go_right = self.agent.enemy.facing_right
        self.initial_position = self.agent.enemy.rect.x
        self.distance = float("inf")

        # determine patrolling distance
        parsed = re.search(r"patrol (\d+)", self.agent.enemy.type)
        if parsed is not None:
            self.distance = int(parsed.group(1))

    def update(self, chamber):
        from .aware import Aware
        from .idle import Idle

        if self.agent.seeing_hero and self.agent.hero.lives > 0:
            self.agent.state = Aware(self.agent)
            return

        self.update_waiting()
        if self.waiting:
            return

        # with probability 2% stop
        if random.random() < 0.02:
            self.agent.enemy.stop()
            self.wait(random.randint(500, 1500))

            # with probability 40% after stop - change direction
            if random.random() < 0.4:
                self.go_right = not self.go_right
            return

        # with 1% probability change state to idle
        if random.random() < 0.01:
            self.agent.state = Idle(self.agent)
            return

        # move enemy
        if self.go_right:
            self.agent.enemy.move_right()
        else:
            self.agent.enemy.move_left()

        # upon reaching wall, cliff or max distance - stop and wait
        new_position = self.agent.enemy.rect.x + self.agent.enemy.vx
        if (
            not self.can_move(self.agent.enemy, chamber)
            or abs(self.initial_position - new_position) > self.distance
        ):
            self.agent.enemy.stop()
            self.wait(random.randint(500, 1500))
            self.go_right = not self.go_right
