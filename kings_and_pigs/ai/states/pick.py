import random
from .state import State


class Pick(State):
    def __init__(self, agent, target):
        super().__init__(agent)
        self.target = target
        hit_box = self.agent.enemy.get_hit_box()
        self.initial = (hit_box.left, hit_box.bottom), self.agent.enemy.facing_right

    def update(self, chamber):
        from .search import Search

        # check if target is still on the same level
        # (maybe I fell off the cliff)
        hit_box = self.agent.enemy.get_hit_box()
        target_rect = self.target.get_hit_box()
        if abs(target_rect.bottom - hit_box.bottom) >= 5:
            self.agent.state = Search(self.agent)
            return

        # if near the target - pick it
        if (
            self.agent.enemy.facing_right
            and hit_box.left <= target_rect.left <= hit_box.right
        ) or (
            not self.agent.enemy.facing_right
            and hit_box.left <= target_rect.right <= hit_box.right
        ):
            self.agent.enemy.stop()
            self.agent.enemy.pick([self.target])
            self.agent.state = Search(self.agent, self.initial)
            return

        # near the target, but facing other direction - turn
        if (
            not self.agent.enemy.facing_right
            and hit_box.left <= target_rect.left <= hit_box.right
        ) or (
            self.agent.enemy.facing_right
            and hit_box.left <= target_rect.right <= hit_box.right
        ):
            self.agent.enemy.stop()
            self.agent.enemy.turn()
            return

        # otherwise check direction and go to the target
        if hit_box.right < target_rect.left:
            self.agent.enemy.move_right()
        elif hit_box.left > target_rect.right:
            self.agent.enemy.move_left()

        # inside target boundaries - randomly go to left or right
        elif random.random() < 0.5:
            self.agent.enemy.move_right()
        else:
            self.agent.enemy.move_left()
