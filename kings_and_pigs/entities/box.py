import pygame
import random
import math
from ..events import SHAKE_WORLD
from ..functions import loader, play, event
from .entity import Entity
from .animation import Animation
from .animated_entity import AnimatedEntity
from .hittable import Hittable
from .heart import Heart
from .diamond import Diamond


# box sprites loader
load_image = loader("kings_and_pigs/data/sprites/08-Box")

BOX_DESTROY_FORCE = 10.5
BOX_PIECE_LIFETIME = 2000  # 2 seconds


class BoxPiece(Entity):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)
        self.appear = pygame.time.get_ticks()

    def update(self, chamber, hero):
        self.apply_gravity(chamber.gravity)
        self.move(chamber)

        # disappearance
        now = pygame.time.get_ticks()
        if now - self.appear >= BOX_PIECE_LIFETIME:
            alpha = self.image.get_alpha()
            alpha = max(alpha - 10, 0)
            if alpha > 0:
                self.image.set_alpha(alpha)
            else:
                self.kill()


class Box(AnimatedEntity, Hittable):
    def __init__(self, x, y):
        idle = load_image("Idle.png")
        hit = load_image("Hit.png")

        self.piece_bl = load_image("Box Pieces 1.png")
        self.piece_tl = load_image("Box Pieces 2.png")
        self.piece_tr = load_image("Box Pieces 3.png")
        self.piece_br = load_image("Box Pieces 4.png")

        self.animation_idle = Animation(idle, 1)
        self.animation_hit = Animation(hit, 1)

        super().__init__(x, y, self.animation_idle)
        self.adjust_hit_box()

    def hit(self, direction, chamber):
        def hit_is_done():
            # create four box pieces
            r = self.rect
            piece_bl = BoxPiece(r.x, r.y + r.height - 10, self.piece_bl)
            piece_tl = BoxPiece(r.x, r.y, self.piece_tl)
            piece_tr = BoxPiece(r.x + r.width - 10, r.y - 3, self.piece_tr)
            piece_br = BoxPiece(r.x + r.width - 10, r.y + r.height - 10, self.piece_br)
            chamber.active_sprites.add(piece_bl, piece_tl, piece_tr, piece_br)

            # add heart with 5% probability
            heart = None
            if random.random() < 0.05:
                heart = Heart(r.centerx - 9, r.centery - 7)
                chamber.active_sprites.add(heart)

            # add diamond with 20% probability
            diamond = None
            if random.random() < 0.2:
                diamond = Diamond(r.centerx - 9, r.centery - 7)
                chamber.active_sprites.add(diamond)

            # destroy box
            self.kill()

            # disperse pieces depending on hit direction
            if direction == Hittable.HIT_FROM_TOP:
                piece_tl.vx, piece_tl.vy = -3, 0
                piece_tr.vx, piece_tr.vy = 3, 0
            elif direction == Hittable.HIT_FROM_RIGHT:
                piece_bl.vx, piece_bl.vy = -1, 3
                piece_tl.vx, piece_tl.vy = -1, -3
                piece_tr.vx, piece_tr.vy = -1, 0
                piece_br.vx, piece_br.vy = -1, 0
                if heart:
                    heart.vx, heart.vy = -1, 0
                if diamond:
                    diamond.vx, diamond.vy = -1, 0
            elif direction == Hittable.HIT_FROM_BOTTOM:
                piece_bl.vx, piece_bl.vy = -3, 1
                piece_br.vx, piece_br.vy = 3, 1
            elif direction == Hittable.HIT_FROM_LEFT:
                piece_bl.vx, piece_bl.vy = 1, 3
                piece_tl.vx, piece_tl.vy = 1, -3
                piece_tr.vx, piece_tr.vy = 1, 0
                piece_br.vx, piece_br.vy = 1, 0
                if heart:
                    heart.vx, heart.vy = 1, 0
                if diamond:
                    diamond.vx, diamond.vy = 1, 0
            elif direction == Hittable.HIT_FROM_TOP_RIGHT:
                piece_bl.vx, piece_bl.vy = -1, 2
                piece_tl.vx, piece_tl.vy = -2, 0
                piece_tr.vx, piece_tr.vy = -3, 2
                piece_br.vx, piece_br.vy = -3, 3
                if heart:
                    heart.vx, heart.vy = -2, 2
                if diamond:
                    diamond.vx, diamond.vy = -2, 2
            elif direction == Hittable.HIT_FROM_BOTTOM_RIGHT:
                piece_bl.vx, piece_bl.vy = -3, -2
                piece_tl.vx, piece_tl.vy = -3, -5
                piece_tr.vx, piece_tr.vy = -2, -3
                piece_br.vx, piece_br.vy = 0, -2
                if heart:
                    heart.vx, heart.vy = -2, -2
                if diamond:
                    diamond.vx, diamond.vy = -2, -2
            elif direction == Hittable.HIT_FROM_BOTTOM_LEFT:
                piece_bl.vx, piece_bl.vy = 0, -2
                piece_tl.vx, piece_tl.vy = 2, -3
                piece_tr.vx, piece_tr.vy = 3, -5
                piece_br.vx, piece_br.vy = 3, -2
                if heart:
                    heart.vx, heart.vy = 2, -2
                if diamond:
                    diamond.vx, diamond.vy = 2, -2
            elif direction == Hittable.HIT_FROM_TOP_LEFT:
                piece_bl.vx, piece_bl.vy = 1, 2
                piece_tl.vx, piece_tl.vy = 2, 0
                piece_tr.vx, piece_tr.vy = 3, 2
                piece_br.vx, piece_br.vy = 3, 3
                if heart:
                    heart.vx, heart.vy = 2, 2
                if diamond:
                    diamond.vx, diamond.vy = 2, 2

            # add some randomness in position
            piece_bl.vx += random.uniform(-1, +1)
            piece_bl.vy += random.uniform(-1, +1)
            if heart:
                heart.vx += random.uniform(-1, +1)
                heart.vy += random.uniform(-1, +1)
            if diamond:
                diamond.vx += random.uniform(-1, +1)
                diamond.vy += random.uniform(-1, +1)

        self.change_animation(self.animation_hit)
        self.animation_hit.on_done(hit_is_done)

        event(SHAKE_WORLD)
        play("destroy_box")

    def move(self, chamber, hero):
        vx, vy = self.vx, self.vy
        super().move(chamber)

        # check collisions with hero
        hit_hero = False
        if vy != 0 and self.vy != 0:
            hero_hit_box = hero.get_hit_box()
            if hero_hit_box.colliderect(self.rect):
                hit_hero = True
                self.vx = 0
                if self.vx < 0 or (self.vx == 0 and hero.facing_right):
                    hero.hit(Hittable.HIT_FROM_RIGHT, chamber)
                else:
                    hero.hit(Hittable.HIT_FROM_LEFT, chamber)

        # calculate box speed vector
        force = math.hypot(vx, vy)
        if force >= BOX_DESTROY_FORCE or hit_hero:
            # hit the ground
            if vy != 0 and self.vy == 0:
                if vx > 0:  # diagonally from left to right
                    self.hit(Hittable.HIT_FROM_BOTTOM_LEFT, chamber)
                elif vx < 0:  # diagonally from right to left
                    self.hit(Hittable.HIT_FROM_BOTTOM_RIGHT, chamber)
                else:  # vertically
                    self.hit(Hittable.HIT_FROM_BOTTOM, chamber)
            # hit the left wall
            elif vx < 0 and self.vx == 0:
                if vy > 0:  # diagonally from top to bottom
                    self.hit(Hittable.HIT_FROM_TOP_LEFT, chamber)
                elif vy < 0:  # diagonally from bottom to top
                    self.hit(Hittable.HIT_FROM_BOTTOM_LEFT, chamber)
                else:  # horizontally
                    self.hit(Hittable.HIT_FROM_LEFT, chamber)
            # hit the right wall
            elif vx > 0 and self.vx == 0:
                if vy > 0:  # diagonally from top to bottom
                    self.hit(Hittable.HIT_FROM_TOP_RIGHT, chamber)
                elif vy < 0:  # diagonally from bottom to top
                    self.hit(Hittable.HIT_FROM_BOTTOM_RIGHT, chamber)
                else:  # horizontally
                    self.hit(Hittable.HIT_FROM_RIGHT, chamber)

    def update(self, chamber, hero):
        super().update()
        self.apply_gravity(chamber.gravity)
        self.move(chamber, hero)
