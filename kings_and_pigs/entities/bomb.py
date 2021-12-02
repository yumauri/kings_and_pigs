import pygame
from ..events import SHAKE_WORLD
from ..functions import loader, event, play
from .animation import Animation
from .animated_entity import AnimatedEntity
from .hittable import Hittable


# box sprites loader
load_image = loader("kings_and_pigs/data/sprites/09-Bomb")


class Bomb(AnimatedEntity, Hittable):
    BOOM_FLOOR = 0
    BOOM_LEFT_WALL = 1
    BOOM_RIGHT_WALL = 2

    def __init__(self, x, y):
        off = load_image("Bomb Off.png")
        on = load_image("Bomb On (52x56).png")
        boom = load_image("Boooooom (52x56).png")

        self.animation_off = Animation(off, 1)
        self.animation_on = Animation(on, 4)
        self.animation_boom_floor = Animation(boom, 6)
        self.animation_boom_right_wall = self.animation_boom_floor.rotate(90)
        self.animation_boom_left_wall = self.animation_boom_floor.rotate(-90)

        super().__init__(x, y, self.animation_off)
        self.adjust_hit_box(left=19, right=18, top=25, bottom=17)

        self.is_on = False
        self.exists = True

    def on(self):
        self.is_on = True
        self.change_animation(self.animation_on)

    def get_hit_area(self):
        return self.rect

    def boom(self, direction, chamber, hero):
        self.exists = False

        def boomed():
            self.kill()

        if direction == Bomb.BOOM_RIGHT_WALL:
            self.change_animation(self.animation_boom_right_wall)
            self.animation_boom_right_wall.on_done(boomed, True)
        elif direction == Bomb.BOOM_LEFT_WALL:
            self.change_animation(self.animation_boom_left_wall)
            self.animation_boom_left_wall.on_done(boomed, True)
        else:
            self.change_animation(self.animation_boom_floor)
            self.animation_boom_floor.on_done(boomed, True)

        event(SHAKE_WORLD)
        play("boom")

        # check collisions with hero or any hittable object
        kill_area = self.get_hit_area()
        for target in [*chamber.active_sprites, hero]:
            if (
                target is not self
                and kill_area.colliderect(target.rect)
                and isinstance(target, Hittable)
            ):
                if kill_area.colliderect(target.get_hit_box()):
                    target.hit(target.HIT_FROM_TOP, chamber)

    def move(self, chamber, hero):
        hit_floor = False
        hit_left_wall = False
        hit_right_wall = False

        # horizontal move
        self.rect.x += self.vx

        # check collisions with walls
        hit_box = self.get_hit_box()
        for wall in chamber.walls:
            if hit_box.colliderect(wall.rect):
                if self.vx > 0:
                    self.rect.right = wall.rect.left + self.hit_box_d_right
                    self.vx = 0
                    hit_right_wall = True
                elif self.vx < 0:
                    self.rect.left = wall.rect.right - self.hit_box_d_left
                    self.vx = 0
                    hit_left_wall = True

        # check collisions with floors
        # if object already collides with some floors - just ignore them later
        collisions = []
        hit_box = self.get_hit_box()
        for floor in chamber.floors:
            if hit_box.colliderect(floor.rect):
                collisions.append(floor)

        # vertical move
        self.rect.y += self.vy

        # check collisions with floors
        hit_box = self.get_hit_box()
        for floor in chamber.floors:
            if hit_box.colliderect(floor.rect) and floor not in collisions:
                if self.vy > 0:
                    self.rect.bottom = floor.rect.top + self.hit_box_d_bottom
                    self.vy = 0
                    hit_floor = True

        # ka-boooom!
        if self.is_on:
            if hit_floor:
                self.boom(Bomb.BOOM_FLOOR, chamber, hero)
            elif hit_left_wall:
                self.boom(Bomb.BOOM_LEFT_WALL, chamber, hero)
            elif hit_right_wall:
                self.boom(Bomb.BOOM_RIGHT_WALL, chamber, hero)
        elif hit_floor:
            self.apply_friction(self.weight)

    def update(self, chamber, hero):
        super().update()
        if self.exists:
            self.apply_gravity(chamber.gravity)
            self.move(chamber, hero)
