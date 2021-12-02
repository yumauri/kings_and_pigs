import pygame


class State:
    def __init__(self, agent):
        self.agent = agent
        self.agent.enemy.stop()
        self.enter = pygame.time.get_ticks()

        self.start_waiting = None
        self.wait_for = 0
        self.waiting = False

    def update_waiting(self):
        if self.waiting:
            now = pygame.time.get_ticks()
            if now - self.start_waiting >= self.wait_for:
                self.waiting = False

    def wait(self, ms):
        self.start_waiting = pygame.time.get_ticks()
        self.wait_for = ms
        self.waiting = True

    def can_move(self, enemy, chamber):
        x, y = enemy.rect.x, enemy.rect.y

        # check collisions with walls
        enemy.rect.x += enemy.vx
        hit_box = enemy.get_hit_box()
        for wall in chamber.walls:
            if hit_box.colliderect(wall.rect):
                enemy.rect.x = x
                return False
        enemy.rect.x = x

        # check collisions for floors
        will_fall = True
        enemy.rect.y += 1
        enemy.rect.x += hit_box.width * (1, -1)[enemy.vx < 0]
        hit_box = enemy.get_hit_box()
        for floor in chamber.floors:
            if hit_box.colliderect(floor.rect):
                will_fall = False
                break
        enemy.rect.x, enemy.rect.y = x, y
        if will_fall:
            return False

        # if there is no wall and no edge cliff - enemy can move further
        return True

    def __str__(self):
        return self.__class__.__name__

    def update(self, chamber):
        pass

    def draw(self):
        pass
