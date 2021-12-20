import pygame
from ..events import DEBUG_AI
from .agent import Agent


class AI:
    def __init__(self, width, height, chamber, hero, cheats):
        self.view_width = width
        self.view_height = height
        self.agents = []
        self.chamber = chamber
        self.hero = hero
        self.layer = pygame.Surface([width, height], pygame.SRCALPHA, 32)
        self.debug = not True
        self.cheats = cheats

    def process_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in DEBUG_AI and not self.cheats.locked:
                self.debug = not self.debug

    def update_agents(self, offset_x, offset_y):
        # get all visible enemies in the visible part of the chamber
        visible_enemies = []
        for enemy in self.chamber.enemies:
            hit_box = enemy.get_hit_box()
            if (
                offset_x <= hit_box.left
                and hit_box.right <= offset_x + self.view_width
                and offset_y <= hit_box.top
                and hit_box.bottom <= offset_y + self.view_height
            ):
                visible_enemies.append(enemy)

        # update agents according to visible enemies
        for agent in self.agents[:]:

            # if agent's enemy is not in list of visible enemies
            if agent.enemy not in visible_enemies:

                # but agent's enemy's id IN the list -> enemy just changed sprite
                ids = [enemy.id for enemy in visible_enemies]
                if agent.enemy.id in ids:
                    agent.enemy = visible_enemies.pop(ids.index(agent.enemy.id))

                # else, enemy become invisible -> remove agent
                else:
                    agent.enemy.stop()  # stop enemy
                    self.agents.remove(agent)

            # agent enemy in the list - skip this enemy
            else:
                visible_enemies.remove(agent.enemy)

        # for each new enemy -> create new agent
        for enemy in visible_enemies:
            self.agents.append(
                Agent(self.view_width, self.view_height, enemy, self.hero)
            )

    def update(self, offset_x, offset_y):
        self.update_agents(offset_x, offset_y)
        for agent in self.agents:
            agent.update(self.chamber, offset_x, offset_y)

    def draw(self, offset_x, offset_y):
        self.layer.fill((0, 0, 0, 0))
        for agent in self.agents:
            agent.draw(self.chamber, offset_x, offset_y, self.debug)
            self.layer.blit(agent.layer, [0, 0])
