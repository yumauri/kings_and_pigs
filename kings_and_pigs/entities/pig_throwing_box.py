from ..functions import loader
from .animation import Animation
from .enemy import Enemy
from .box import Box
from .pig import Pig


# pig sprites loader
load_image = loader("kings_and_pigs/data/sprites/04-Pig Throwing a Box")


class PigThrowingBox(Enemy):
    def __init__(self, x, y, type=None, id=None):
        idle = load_image("Idle (26x30).png")
        run = load_image("Run (26x30).png")
        pick = load_image("Picking Box (26x30).png")
        # throw = load_image("Throwing Box (26x30).png")

        self.animation_left_idle = Animation(idle, 9)
        self.animation_right_idle = self.animation_left_idle.flip()
        self.animation_left_run = Animation(run, 6)
        self.animation_right_run = self.animation_left_run.flip()
        self.animation_left_jump = None
        self.animation_right_jump = None
        self.animation_left_fall = None
        self.animation_right_fall = None
        self.animation_left_pick = Animation(pick, 5)
        self.animation_right_pick = self.animation_left_pick.flip()
        # self.animation_left_throw = Animation(throw, 5)
        # self.animation_right_throw = self.animation_left_throw.flip()

        super().__init__(x, y, self.animation_right_idle, type, id)
        self.adjust_hit_box(left=5, right=10, top=5)
        self.adjust_direction = 5
        self.facing_right = False
        self.lives = 2
        self.can_throw = True

    def get_hit_area(self):
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
        # attack = throw a box
        box = Box(self.rect.x + 4, self.rect.y + 3)
        pig = Pig(self.rect.x - 4, self.rect.y + 2, self.type, self.id)
        pig.facing_right = self.facing_right
        box.vy = -8
        box.vx = 8 if self.facing_right else -8
        self.replace_with = [pig, box]

    def hit(self, direction, chamber):
        # when hero hits - destroy the box and hit the pig separately
        box = Box(self.rect.x + 4, self.rect.y + 3)
        pig = Pig(self.rect.x - 4, self.rect.y + 2, self.type, self.id)
        pig.facing_right = self.facing_right
        box.hit(direction, chamber)
        pig.hit(direction, chamber)
        self.replace_with = [box, pig]

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
