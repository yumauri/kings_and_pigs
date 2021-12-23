from ..functions import loader, play
from .animation import Animation
from .enemy import Enemy
from .box import Box
from .bomb import Bomb


# pig sprites loader
load_image = loader("kings_and_pigs/data/sprites/03-Pig")


class Pig(Enemy):
    def __init__(self, x, y, type=None, id=None):
        attack = load_image("Attack (34x28).png")
        dead = load_image("Dead (34x28).png")
        fall = load_image("Fall (34x28).png")
        ground = load_image("Ground (34x28).png")
        hit = load_image("Hit (34x28).png")
        idle = load_image("Idle (34x28).png")
        jump = load_image("Jump (34x28).png")
        run = load_image("Run (34x28).png")

        self.animation_left_idle = Animation(idle, 11)
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
        self.adjust_hit_box(left=8, right=15, top=13)
        self.adjust_direction = 7
        self.facing_right = False
        self.lives = 2
        self.can_pick = True

    def get_hit_area(self, chamber=None):
        area = self.get_hit_box()
        area.left += 10 if self.facing_right else -14
        area.top -= 12
        area.width += 4
        area.height += 12
        return area

    def jump(self, floors):
        was_jumped_successfully = super().jump(floors)
        if was_jumped_successfully:
            play("jump_pig")

    def attack(self, targets, chamber):
        was_attacked_successfully = super().attack(targets, chamber)
        if was_attacked_successfully:
            play("attack_pig")

    def hit(self, direction, chamber):
        was_hit = super().hit(direction, chamber)
        if was_hit and self.lives > 0:
            play("damaged_pig")

    def murder(self):
        play("damaged_pig")
        super().murder()

    def pick(self, targets):
        hit_box = self.get_hit_box()
        for target in targets:
            # if this is a box on the same level
            if isinstance(target, Box) and abs(target.rect.bottom - hit_box.bottom) < 5:
                # import here to avoid circular dependencies
                from .pig_throwing_box import PigThrowingBox

                # and this box is near the pig
                if (
                    not self.facing_right
                    and hit_box.left <= target.rect.right <= hit_box.right
                ) or (
                    self.facing_right
                    and hit_box.left <= target.rect.left <= hit_box.right
                ):
                    pig = PigThrowingBox(
                        self.rect.x + 4, self.rect.y - 2, self.type, self.id
                    )
                    pig.facing_right = self.facing_right
                    pig.pick()
                    target.kill()  # remove box
                    self.replace_with = pig
                    break

            # if this is a bomb on the same level
            if isinstance(target, Bomb):
                target_rect = target.get_hit_box()
                if abs(target_rect.bottom - hit_box.bottom) < 5:
                    # import here to avoid circular dependencies
                    from .pig_throwing_bomb import PigThrowingBomb

                    # and this box is near the pig
                    if (
                        not self.facing_right
                        and hit_box.left <= target_rect.right <= hit_box.right
                    ) or (
                        self.facing_right
                        and hit_box.left <= target_rect.left <= hit_box.right
                    ):
                        pig = PigThrowingBomb(
                            self.rect.x + 2, self.rect.y + 2, self.type, self.id
                        )
                        pig.facing_right = self.facing_right
                        pig.pick()
                        target.kill()  # remove bomb
                        self.replace_with = pig
                        break
