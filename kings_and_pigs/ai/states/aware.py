import random
from kings_and_pigs.entities.dialogue import AwareDialogue
from .state import State


class Aware(State):
    def __init__(self, agent):
        super().__init__(agent)
        self.wait(random.randint(500, 1000))
        self.agent.enemy.say(AwareDialogue)

    def search_throwable_nearby(self, chamber):
        hit_box = self.agent.enemy.get_hit_box()
        for items in [chamber.bombs, chamber.boxes]:
            for target in items:
                target_rect = target.get_hit_box()
                if (
                    abs(target_rect.bottom - hit_box.bottom) < 5
                    and abs(target_rect.centerx - hit_box.centerx) < 64
                ):
                    return target

    def update(self, chamber):
        from .pick import Pick
        from .attack import Attack
        from .idle import Idle

        if self.agent.hero.lives <= 0:
            self.agent.state = Idle(self.agent)
            return

        self.update_waiting()
        if self.waiting:
            return

        # if enemy can pick things
        if self.agent.enemy.can_pick:
            # pick some nearby object with probability 80%
            if random.random() > 0.2:
                target = self.search_throwable_nearby(chamber)
                if target:
                    self.agent.state = Pick(self.agent, target)
                    return

        # otherwise - attack
        self.agent.state = Attack(self.agent)
