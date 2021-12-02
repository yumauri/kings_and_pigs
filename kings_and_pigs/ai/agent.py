import pygame
from .sight_line import SightLine
from .states import Idle, Patrol


class Agent:
    def __init__(self, width, height, enemy, hero):
        self.view_width = width
        self.view_height = height
        self.enemy = enemy
        self.hero = hero
        self.sights = [
            SightLine(width, height),
            SightLine(width, height),
            SightLine(width, height),
        ]
        self.seeing_hero = False
        self.layer = pygame.Surface([width, height], pygame.SRCALPHA, 32)
        self.font = pygame.font.Font(None, 16)

        # initial state could be either Idle or Patrol
        self.state = Patrol(self) if "patrol" in self.enemy.type else Idle(self)

    def check_hero_visibility(self, chamber, offset_x, offset_y):
        if self.hero.lives <= 0:
            return False

        hero_hit_box = self.hero.get_hit_box()
        self_hit_box = self.enemy.get_hit_box()

        self.seeing_hero = True

        # if facing hero side - check collisions with walls and floors
        if (self.enemy.facing_right and self_hit_box.left <= hero_hit_box.left) or (
            not self.enemy.facing_right and self_hit_box.right >= hero_hit_box.right
        ):
            self.sights[0].update(
                True,
                (self_hit_box.centerx - offset_x, self_hit_box.y + 3 - offset_y),
                (hero_hit_box.centerx - offset_x, hero_hit_box.y - offset_y),
            )
            self.sights[1].update(
                True,
                (self_hit_box.centerx - offset_x, self_hit_box.y + 3 - offset_y),
                (
                    hero_hit_box.centerx - offset_x,
                    hero_hit_box.y + (hero_hit_box.height - 3) // 2 - offset_y,
                ),
            )
            self.sights[2].update(
                True,
                (self_hit_box.centerx - offset_x, self_hit_box.y + 3 - offset_y),
                (hero_hit_box.centerx - offset_x, hero_hit_box.bottom - 3 - offset_y),
            )

            # check collisions
            open_view = [True for _ in self.sights]
            for block in chamber.inactive_sprites:
                for i, sight in enumerate(self.sights):
                    if open_view[i] and sight.collides_with(block, offset_x, offset_y):
                        open_view[i] = False
                if not any(open_view):
                    break
            self.seeing_hero = any(open_view)

        # facing opposite side from hero - agent doesn't see hero
        else:
            self.seeing_hero = False
            for sight in self.sights:
                sight.update()

    def update(self, chamber, offset_x, offset_y):
        self.check_hero_visibility(chamber, offset_x, offset_y)

        # change state only when enemy stands on the firm ground
        if self.enemy.on_ground:
            self.state.update(chamber)

    def draw(self, chamber, offset_x, offset_y, debug=False):
        self.layer.fill((0, 0, 0, 0))

        # in case of debug
        if debug:

            # draw lines of sight
            for sight in self.sights:
                self.layer.blit(sight.image, [0, 0])

            # draw collisions points
            for block in chamber.inactive_sprites:
                for i, sight in enumerate(self.sights):
                    dot = sight.collides_with(block, offset_x, offset_y)
                    if dot:
                        pygame.draw.circle(self.layer, (0, 255, 0, 200), dot, 3)

            # draw agent state
            hit_box = self.enemy.get_hit_box()
            state = self.font.render(str(self.state), True, (0, 0, 0))
            x = hit_box.centerx - state.get_width() / 2 - offset_x
            y = hit_box.top - state.get_height() - 10 - offset_y
            pygame.draw.rect(
                self.layer,
                (255, 255, 255),
                (x - 2, y - 2, state.get_width() + 4, state.get_height() + 4),
            )
            self.layer.blit(state, (x, y))
