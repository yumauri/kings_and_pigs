from ..functions import loader
from .animation import Animation
from .enemy import Enemy
from .bomb import Bomb
from .pig import Pig


# pig sprites loader
load_image = loader("kings_and_pigs/data/sprites/05-Pig Throwing a Bomb")


class PigThrowingBomb(Enemy):
    def __init__(self, x, y, type=None, id=None):
        idle = load_image("Idle (26x26).png")
        run = load_image("Run (26x26).png")
        pick = load_image("Picking Bomb (26x26).png")
        # throw = load_image("Throwing Boom (26x26).png")

        self.animation_left_idle = Animation(idle, 10)
        self.animation_right_idle = self.animation_left_idle.flip()
        self.animation_left_run = Animation(run, 6)
        self.animation_right_run = self.animation_left_run.flip()
        self.animation_left_jump = None
        self.animation_right_jump = None
        self.animation_left_fall = None
        self.animation_right_fall = None
        self.animation_left_pick = Animation(pick, 4)
        self.animation_right_pick = self.animation_left_pick.flip()
        # self.animation_left_throw = Animation(throw, 5)
        # self.animation_right_throw = self.animation_left_throw.flip()

        super().__init__(x, y, self.animation_right_idle, type, id)
        self.adjust_hit_box(left=9, right=6, top=9)
        self.adjust_direction = -3
        self.facing_right = False
        self.lives = 2
        self.can_throw = True

    def get_hit_area(self, chamber=None):
        area = self.get_hit_box()
        area.left += 10 if self.facing_right else -160
        area.top -= 15
        area.width += 150
        area.height += 15
        return area

    def jump(self, floors):
        pass  # cannot jump

    def fall_on_ground(self, floor, chamber, force):
        pass  # do nothing

    def attack(self, targets, chamber):
        # attack = throw a bomb
        bomb = Bomb(self.rect.x - 10, self.rect.y - 18)
        pig = Pig(self.rect.x - 2, self.rect.y - 2, self.type, self.id)
        pig.facing_right = self.facing_right
        bomb.on()
        bomb.vy = -8
        bomb.vx = 8 if self.facing_right else -8
        self.replace_with = [pig, bomb]

    def hit(self, direction, chamber):
        # when hero hits - hit the pig
        bomb = Bomb(self.rect.x - 10, self.rect.y - 18)
        pig = Pig(self.rect.x - 2, self.rect.y - 2, self.type, self.id)
        pig.facing_right = self.facing_right
        pig.hit(direction, chamber)
        self.replace_with = [bomb, pig]

    def murder(self):
        bomb = Bomb(self.rect.x - 10, self.rect.y - 18)
        pig = Pig(self.rect.x - 2, self.rect.y - 2, self.type, self.id)
        pig.facing_right = self.facing_right
        pig.murder()
        self.replace_with = [bomb, pig]

    def pick(self):
        if self.in_action:
            return

        def pick_is_done():
            self.in_action = False

        self.in_action = True
        if self.facing_right:
            self.change_animation(self.animation_right_pick)
            self.animation_right_pick.on_done(pick_is_done)
        else:
            self.change_animation(self.animation_left_pick)
            self.animation_left_pick.on_done(pick_is_done)
