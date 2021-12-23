import pygame
from kings_and_pigs import GRID_SIZE
from ..events import SHAKE_WORLD
from ..functions import event
from .animated_entity import AnimatedEntity
from .hittable import Hittable
from .dead import Dead


class Creature(AnimatedEntity, Hittable):
    def __init__(self, x, y, animation_idle):
        super().__init__(x, y, animation_idle)
        self.adjust_hit_box()
        self.adjust_direction = 0

        self.speed = 2
        self.jump_power = 9
        self.lives = 1

        self.dx = 0
        self.vx = 0
        self.vy = 0
        self.facing_right = True
        self.on_ground = True
        self.in_action = False
        self.invincibility = 0
        self.max_invincibility = 0

        self.can_pick = False
        self.can_throw = False

    def get_hit_box(self):
        hit_box = super().get_hit_box()
        if not self.facing_right:
            hit_box.left += self.adjust_direction  # hit box compensation
        return hit_box

    def get_hit_area(self, chamber=None):
        return self.get_hit_box()

    def step_left(self):
        if not self.in_action:
            if not self.facing_right:
                self.dx = -self.speed
            else:
                self.facing_right = False
                self.rect.x -= self.adjust_direction  # creature rect compensation

    def step_right(self):
        if not self.in_action:
            if self.facing_right:
                self.dx = self.speed
            else:
                self.facing_right = True
                self.rect.x += self.adjust_direction  # creature rect compensation

    def move_left(self):
        if not self.in_action:
            self.vx = -self.speed
            if self.facing_right:
                self.facing_right = False
                self.rect.x -= self.adjust_direction  # creature rect compensation

    def move_right(self):
        if not self.in_action:
            self.vx = self.speed
            if not self.facing_right:
                self.facing_right = True
                self.rect.x += self.adjust_direction  # creature rect compensation

    def turn(self):
        if not self.in_action:
            if self.facing_right:
                self.facing_right = False
                self.rect.x -= self.adjust_direction  # creature rect compensation
            else:
                self.facing_right = True
                self.rect.x += self.adjust_direction  # creature rect compensation

    def stop(self):
        self.vx = 0

    def jump(self, floors):
        if self.in_action or not self.on_ground:
            return

        # check if creature was just fall off the cliff
        # because jump event comes a bit later, this is VERY irritating
        dx, dy = 0, 0
        hit_box = self.get_hit_box()
        if self.vx != 0 and 0 < self.vy <= 4:
            dx = self.vy * self.vx
            dy = self.vy * (self.vy + 1) // 2
            if (hit_box.bottom - dy) % GRID_SIZE == 0:
                # move creature back to the ground
                self.rect.y -= dy
                self.rect.x -= dx

        # creature can jump only from floor, so,
        # check, will hero collide with any floor if move him a bit lower?

        was_jumped_successfully = False
        self.rect.y += 1

        # check collisions for floors
        hit_box = self.get_hit_box()
        for floor in floors:
            if hit_box.colliderect(floor.rect):
                self.vy = -1 * self.jump_power
                was_jumped_successfully = True
                break

        # return position adjustment
        self.rect.y += dy
        self.rect.x += dx

        # return vertical position back
        self.rect.y -= 1

        # to indicate in child classes, if creature was jumped successfully
        return was_jumped_successfully

    def fall_down(self, walls):
        if not self.on_ground:
            return

        # creature can fall down only through floor (not walls), so,
        # check, will hero collide with any floor if move him a bit lower?

        was_fell_successfully = True
        self.rect.y += 1

        # check collisions for floors
        hit_box = self.get_hit_box()
        for floor in walls:
            if hit_box.colliderect(floor.rect):
                was_fell_successfully = False
                break

        # return vertical position back, if was not fell
        if not was_fell_successfully:
            self.rect.y -= 1

        # to indicate in child classes, if creature was fell successfully
        return was_fell_successfully

    def fall_on_ground(self, floor, chamber, force):
        if self.in_action:
            return

        def fall_is_done():
            self.in_action = False

        self.in_action = True
        if self.facing_right:
            self.change_animation(self.animation_right_ground)
            self.animation_right_ground.on_done(fall_is_done)
        else:
            self.change_animation(self.animation_left_ground)
            self.animation_left_ground.on_done(fall_is_done)

    def attack(self, targets, chamber):
        if self.in_action:
            return

        def attack_is_done():
            self.in_action = False

        self.in_action = True
        if self.facing_right:
            self.change_animation(self.animation_right_attack)
            self.animation_right_attack.on_done(attack_is_done)
        else:
            self.change_animation(self.animation_left_attack)
            self.animation_left_attack.on_done(attack_is_done)

        event(SHAKE_WORLD)

        kill_area = self.get_hit_area(chamber)
        if kill_area:
            for target in targets:
                if (
                    target is not self
                    and kill_area.colliderect(target.rect)
                    and isinstance(target, Hittable)
                ):
                    if kill_area.colliderect(target.get_hit_box()):
                        if self.facing_right:
                            target.hit(target.HIT_FROM_BOTTOM_LEFT, chamber)
                        else:
                            target.hit(target.HIT_FROM_BOTTOM_RIGHT, chamber)

        # to indicate in child classes, if creature was attacked successfully
        return True

    def hit(self, direction, chamber):
        if self.invincibility > 0:
            return
        self.invincibility = self.max_invincibility

        def hit_is_done():
            self.in_action = False
            self.lives -= 1
            if self.lives <= 0:
                self.die()

        self.in_action = True

        self.vy = -2
        if direction in [
            Hittable.HIT_FROM_RIGHT,
            Hittable.HIT_FROM_TOP_RIGHT,
            Hittable.HIT_FROM_BOTTOM_RIGHT,
        ]:
            self.dx = -7
        elif direction in [
            Hittable.HIT_FROM_LEFT,
            Hittable.HIT_FROM_TOP_LEFT,
            Hittable.HIT_FROM_BOTTOM_LEFT,
        ]:
            self.dx = 7
        else:
            self.dx = -7 if self.facing_right else 7

        if self.facing_right:
            self.change_animation(self.animation_right_hit)
            self.animation_right_hit.on_done(hit_is_done)
        else:
            self.change_animation(self.animation_left_hit)
            self.animation_left_hit.on_done(hit_is_done)

        event(SHAKE_WORLD)

        # to indicate in child classes, if creature was hit
        return True

    def move(self, chamber):
        # horizontal move
        self.rect.x += self.vx + self.dx

        # check collisions with walls
        hit_box = self.get_hit_box()
        for wall in chamber.walls:
            if hit_box.colliderect(wall.rect):
                if self.vx > 0 or self.dx > 0:
                    self.rect.right = wall.rect.left + self.hit_box_d_right
                    if not self.facing_right:
                        self.rect.left -= self.adjust_direction
                    self.vx = 0
                elif self.vx < 0 or self.dx < 0:
                    self.rect.left = wall.rect.right - self.hit_box_d_left
                    if not self.facing_right:
                        self.rect.left -= self.adjust_direction
                    self.vx = 0

        # reset single step movement
        self.dx = 0

        # check collisions with floors
        # if we didn't move vertically, and hero collides with some floors - just ignore them later
        collisions = []
        hit_box = self.get_hit_box()
        for floor in chamber.floors:
            if hit_box.colliderect(floor.rect):
                collisions.append(floor)

        # vertical move
        self.rect.y += self.vy
        was_on_ground = self.on_ground
        self.on_ground = False

        # check collisions with floors
        hit_box = self.get_hit_box()
        for floor in chamber.floors:
            if hit_box.colliderect(floor.rect) and floor not in collisions:
                if self.vy > 0:
                    self.rect.bottom = floor.rect.top + self.hit_box_d_bottom
                    if not was_on_ground:
                        self.fall_on_ground(floor, chamber, self.vy)
                    self.vy = 0
                    self.on_ground = True

        # check collisions with ceiling
        for wall in chamber.walls:
            if hit_box.colliderect(wall.rect):
                if self.vy < 0:
                    self.rect.top = wall.rect.bottom - self.hit_box_d_top
                    self.vy = 0

    def update_animation(self):
        if self.in_action:
            return

        # change animation depending of creature position and status
        if self.on_ground:
            if self.vx != 0:
                if self.facing_right:
                    self.change_animation(self.animation_right_run)
                else:
                    self.change_animation(self.animation_left_run)
            else:
                if self.facing_right:
                    self.change_animation(self.animation_right_idle)
                else:
                    self.change_animation(self.animation_left_idle)
        else:
            if self.vy < 0:
                if self.facing_right:
                    if self.animation_right_jump is not None:
                        self.change_animation(self.animation_right_jump)
                else:
                    if self.animation_left_jump is not None:
                        self.change_animation(self.animation_left_jump)
            elif self.vy > 0:
                if self.facing_right:
                    if self.animation_right_fall is not None:
                        self.change_animation(self.animation_right_fall)
                else:
                    if self.animation_left_fall is not None:
                        self.change_animation(self.animation_left_fall)

    def die(self):
        dead_image = None

        def dead_is_done():
            self.replace_with = Dead(self.rect.x, self.rect.y, dead_image)

        self.in_action = True

        if self.facing_right:
            self.change_animation(self.animation_right_dead)
            self.animation_right_dead.on_done(dead_is_done, True)
            dead_image = self.animation_right_dead.frames[-1]
        else:
            self.change_animation(self.animation_left_dead)
            self.animation_left_dead.on_done(dead_is_done, True)
            dead_image = self.animation_left_dead.frames[-1]

    def say(self, dialogue):
        hit_box = self.get_hit_box()
        x = hit_box.centerx - 12
        y = hit_box.y - 23
        self.emit_new = dialogue(x, y)

    def is_withing_world_boundaries(self, width, height):
        hit_box = self.get_hit_box()
        return (
            hit_box.left > 0
            and hit_box.bottom > 0  # can go to the top up to toes
            and hit_box.right < width
            and hit_box.bottom < height
        )

    def update(self, chamber, hero):
        super().update()

        # reduce invincibility on each frame draw
        self.invincibility = max(self.invincibility - 1, 0)

        # apply gravity only when within world boundaries
        if self.is_withing_world_boundaries(chamber.width, chamber.height):
            self.apply_gravity(chamber.gravity)

        self.move(chamber)
        self.update_animation()
