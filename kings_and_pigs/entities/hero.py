import pygame
from kings_and_pigs import GAME_FPS
from ..events import GO_CHAMBER, DEAD, WIN
from ..functions import loader, play, event
from .animation import Animation
from .creature import Creature
from .hittable import Hittable
from .appliable import Appliable
from .door import Door
from .invisible_door import InvisibleDoor
from .box import Box, BOX_DESTROY_FORCE


# hero sprites loader
load_image = loader("kings_and_pigs/data/sprites/01-King Human")


class Hero(Creature):
    def __init__(self, cheats):
        attack = load_image("Attack (78x58).png")
        dead = load_image("Dead (78x58).png")
        door_in = load_image("Door In (78x58).png")
        door_out = load_image("Door Out (78x58).png")
        fall = load_image("Fall (78x58).png")
        ground = load_image("Ground (78x58).png")
        hit = load_image("Hit (78x58).png")
        idle = load_image("Idle (78x58).png")
        jump = load_image("Jump (78x58).png")
        run = load_image("Run (78x58).png")

        self.animation_right_idle = Animation(idle, 11)
        self.animation_left_idle = self.animation_right_idle.flip()
        self.animation_right_run = Animation(run, 8)
        self.animation_left_run = self.animation_right_run.flip()
        self.animation_right_jump = Animation(jump, 1)
        self.animation_left_jump = self.animation_right_jump.flip()
        self.animation_right_fall = Animation(fall, 1)
        self.animation_left_fall = self.animation_right_fall.flip()
        self.animation_right_ground = Animation(ground, 1)
        self.animation_left_ground = self.animation_right_ground.flip()
        self.animation_right_attack = Animation(attack, 3)
        self.animation_left_attack = self.animation_right_attack.flip()
        self.animation_right_hit = Animation(hit, 2)
        self.animation_left_hit = self.animation_right_hit.flip()
        self.animation_right_dead = Animation(dead, 4)
        self.animation_left_dead = self.animation_right_dead.flip()
        self.animation_right_door_in = Animation(door_in, 8)
        self.animation_left_door_in = self.animation_right_door_in.flip()
        self.animation_right_door_out = Animation(door_out, 8)
        self.animation_left_door_out = self.animation_right_door_out.flip()

        super().__init__(0, 0, self.animation_right_idle)
        self.adjust_hit_box(left=25, right=40, top=17, bottom=14)
        self.adjust_direction = 15

        # make hero jump a little bit higher, than enemy
        # otherwise it is torture to pass "garden" level
        self.jump_power = 9.5

        self.cross_invisible_door_vy = 0
        self.gone_through_invisible_door = False

        self.score = 0
        self.max_score = 99
        self.lives = 3
        self.max_lives = 3
        self.max_invincibility = GAME_FPS

        self.cheats = cheats

    def get_hit_area(self):
        area = self.get_hit_box()
        area.left += 22 if self.facing_right else -37
        area.top -= 12
        area.width += 15
        area.height += 25
        return area

    def jump(self, floors):
        was_jumped_successfully = super().jump(floors)
        if was_jumped_successfully:
            play("jump")

    def fall_down(self, walls):
        was_fell_successfully = super().fall_down(walls)
        if was_fell_successfully:
            play("fall")

    def attack(self, targets, chamber):
        was_attacked_successfully = super().attack(targets, chamber)
        if was_attacked_successfully:
            play("attack")

    def hit(self, direction, chamber):
        # if cheats code for invincibility is active
        if self.cheats.god_mode.enabled:
            return

        was_hit = super().hit(direction, chamber)
        if was_hit:
            play("damaged")

    def fall_on_ground(self, floor, chamber, force):
        super().fall_on_ground(floor, chamber, force)

        # if fall on the box from the high - destroy the box
        if isinstance(floor, Box) and force > BOX_DESTROY_FORCE:
            floor.hit(Hittable.HIT_FROM_TOP, chamber)

    def check_world_boundaries(self, width, height):
        if not self.is_withing_world_boundaries(width, height):
            self.lives = 0
            self.die()

    def go_in(self, targets):
        hit_box = self.get_hit_box()
        for target in targets:
            # if this is a door on the same level
            if (
                isinstance(target, Door)
                and abs(target.rect.bottom - hit_box.bottom) < 5
            ):
                # and this door is near the hero
                if (
                    hit_box.left >= target.rect.left + 10
                    and hit_box.right <= target.rect.right - 10
                ):
                    self.in_action = True

                    def go_next_chamber():
                        event(GO_CHAMBER, door=target)

                    # open the door
                    target.open()

                    # hero goes into the door
                    if self.facing_right:
                        self.change_animation(self.animation_right_door_in)
                        self.animation_right_door_in.on_done(go_next_chamber, True)
                    else:
                        self.change_animation(self.animation_left_door_in)
                        self.animation_left_door_in.on_done(go_next_chamber, True)

                    break

    def check_go_in_invisible_doors(self, doors):
        hit_box = self.get_hit_box()
        for door in doors:
            if hit_box.colliderect(door.rect):
                event(GO_CHAMBER, door=door)
                self.cross_invisible_door_vy = self.vy
                self.gone_through_invisible_door = True
                return

    def go_out(self, door):
        hit_box = self.get_hit_box()

        # can go out only from usual door
        if isinstance(door, InvisibleDoor):
            if self.cross_invisible_door_vy == 0:
                if self.vx > 0 or self.facing_right:
                    self.rect.left = door.rect.right + 3 - self.hit_box_d_left
                    self.rect.top = (
                        door.rect.centery - 3 - hit_box.height // 2 - self.hit_box_d_top
                    )
                elif self.vx < 0 or not self.facing_right:
                    self.rect.right = (
                        door.rect.left - 3 - hit_box.width + self.hit_box_d_right
                    )
                    self.rect.top = (
                        door.rect.centery - 3 - hit_box.height // 2 - self.hit_box_d_top
                    )
            else:
                # assume that a can only fall through horizontal invisible door
                self.rect.left = (
                    door.rect.centerx - hit_box.width // 2 - self.hit_box_d_left
                )
                self.rect.top = door.rect.bottom + 3 - self.hit_box_d_top

            self.vy = 0  # to show falling
            self.gone_through_invisible_door = False
            return

        self.in_action = True

        def went_in():
            door.close()
            self.in_action = False

        self.rect.x = door.rect.centerx - hit_box.width / 2 - self.hit_box_d_left
        if not self.facing_right:
            self.rect.x -= self.adjust_direction
        self.rect.y = door.rect.bottom - self.rect.height

        door.change_animation(door.animation_opened)
        if self.facing_right:
            self.change_animation(self.animation_right_door_out)
            self.animation_right_door_out.on_done(went_in, True)
        else:
            self.change_animation(self.animation_left_door_out)
            self.animation_left_door_out.on_done(went_in, True)

    def process_appliable(self, items):
        hit_box = self.get_hit_box()
        for item in items:
            if hit_box.colliderect(item.rect) and isinstance(item, Appliable):
                item.apply(self)

    def respawn(self, chamber):
        self.rect.x = chamber.spawn_x
        self.rect.y = chamber.spawn_y
        self.lives = self.max_lives
        self.invincibility = 0
        self.facing_right = True

    def die(self):
        super().die()
        event(DEAD)

    def update(self, chamber, *args):
        super().update(chamber, self)
        if self.lives > 0:

            # process cheats
            if self.cheats.full_health.pick():
                play("healed")
                self.lives = 3
            if self.cheats.full_score.pick():
                play("diamond")
                self.score = self.max_score
            if self.cheats.suicide.pick():
                play("damaged")
                self.die()
            if self.cheats.win.pick():
                event(WIN)

            self.process_appliable(chamber.active_sprites)
            self.check_go_in_invisible_doors(chamber.invisible_doors)
            if not self.gone_through_invisible_door:
                self.check_world_boundaries(chamber.width, chamber.height)
