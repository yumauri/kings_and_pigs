import random
from kings_and_pigs import GRID_SIZE
from kings_and_pigs.entities.dialogue import AttackDialogue
from .state import State


class Attack(State):
    def __init__(self, agent):
        super().__init__(agent)
        self.agent.enemy.say(AttackDialogue)
        self.delayed = False

    def update(self, chamber):
        from .search import Search
        from .idle import Idle

        if self.agent.hero.lives <= 0:
            self.agent.state = Idle(self.agent)
            return

        if not self.agent.seeing_hero:
            self.agent.state = Search(self.agent)
            return

        self.update_waiting()
        if self.waiting:
            return

        targets = [*chamber.active_sprites, self.agent.hero]
        hero_hit_box = self.agent.hero.get_hit_box()
        self_hit_box = self.agent.enemy.get_hit_box()
        dx = hero_hit_box.centerx - self_hit_box.centerx
        dy = hero_hit_box.bottom - self_hit_box.bottom

        # if we can throw something
        if self.agent.enemy.can_throw:

            # on the same level can throw box/bomb up to 4 tiles
            if abs(dy) < 5 and abs(dx) <= 4 * GRID_SIZE:
                self.agent.enemy.stop()
                self.agent.enemy.attack(targets, chamber)
                self.wait(random.randint(1000, 1500))
                return

            # if hero is below - can throw box/bomb up to 5 tiles
            if dy > 0 and abs(dx) <= 5 * GRID_SIZE:
                self.agent.enemy.stop()
                self.agent.enemy.attack(targets, chamber)
                self.wait(random.randint(1000, 1500))
                return

            # if hero is above - can throw box/bomb up to 3 tiles
            if dy < 0 and abs(dx) <= 3 * GRID_SIZE:
                self.agent.enemy.stop()
                self.agent.enemy.attack(targets, chamber)
                self.wait(random.randint(1000, 1500))
                return

            # if far away - try to shorten the distance
            if self.agent.enemy.facing_right:
                self.agent.enemy.move_right()
            else:
                self.agent.enemy.move_left()

            # if cannot move (carrying enemy cannot jump) - just stand there
            if not self.can_move(self.agent.enemy, chamber):
                self.agent.enemy.stop()

        # nothing to throw - but enemy can jump :)
        else:
            self_hit_area = self.agent.enemy.get_hit_area()

            # if can hit - just hit!
            if self_hit_area.colliderect(hero_hit_box):
                self.agent.enemy.stop()
                if not self.delayed:
                    # add delay 100-200ms before hit,
                    # because otherwise enemy is super-fast uber-enemy %)
                    self.delayed = True
                    self.wait(random.randint(100, 200))
                else:
                    self.delayed = False
                    self.agent.enemy.attack(targets, chamber)
                    self.wait(random.randint(1000, 1500))
                return

            # shorten distance enough to hit
            if self.agent.enemy.facing_right:
                self.agent.enemy.move_right()
            else:
                self.agent.enemy.move_left()

            # if hero is below or above - also try to jump
            if abs(dy) >= 5:
                # with probability 5%
                if random.random() < 0.05:
                    self.agent.enemy.jump(chamber.floors)
