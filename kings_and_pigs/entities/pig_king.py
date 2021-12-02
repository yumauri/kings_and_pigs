from ..events import WIN
from ..functions import loader, play, event
from .animation import Animation
from .enemy import Enemy


# pig sprites loader
load_image = loader("kings_and_pigs/data/sprites/02-King Pig")


class PigKing(Enemy):
    def __init__(self, x, y, type=None, id=None):
        attack = load_image("Attack (38x28).png")
        dead = load_image("Dead (38x28).png")
        fall = load_image("Fall (38x28).png")
        ground = load_image("Ground (38x28).png")
        hit = load_image("Hit (38x28).png")
        idle = load_image("Idle (38x28).png")
        jump = load_image("Jump (38x28).png")
        run = load_image("Run (38x28).png")

        self.animation_left_idle = Animation(idle, 12)
        self.animation_right_idle = self.animation_left_idle.flip()
        self.animation_left_run = Animation(run, 6)
        self.animation_right_run = self.animation_left_run.flip()
        self.animation_left_jump = Animation(jump, 1)
        self.animation_right_jump = self.animation_left_jump.flip()
        self.animation_left_fall = Animation(fall, 1)
        self.animation_right_fall = self.animation_left_fall.flip()
        self.animation_left_ground = Animation(ground, 1)
        self.animation_right_ground = self.animation_left_ground.flip()
        self.animation_left_attack = Animation(attack, 5)
        self.animation_right_attack = self.animation_left_attack.flip()
        self.animation_left_hit = Animation(hit, 2)
        self.animation_right_hit = self.animation_left_hit.flip()
        self.animation_left_dead = Animation(dead, 4)
        self.animation_right_dead = self.animation_left_dead.flip()

        super().__init__(x, y, self.animation_right_idle, type, id)
        self.adjust_hit_box(left=12, right=15, top=13)
        self.adjust_direction = 3
        self.facing_right = False
        self.lives = 3

    def get_hit_area(self):
        area = self.get_hit_box()
        area.left += 10 if self.facing_right else -14
        area.top -= 12
        area.width += 4
        area.height += 12
        return area

    def jump(self, floors):
        was_jumped_successfully = super().jump(floors)
        if was_jumped_successfully:
            play("jump_pig_king")

    def attack(self, targets, chamber):
        was_attacked_successfully = super().attack(targets, chamber)
        if was_attacked_successfully:
            play("attack_pig_king")

    def hit(self, direction, chamber):
        was_hit = super().hit(direction, chamber)
        if was_hit and self.lives > 0:
            play("damaged_pig_king")

    def die(self):
        super().die()
        event(WIN)
