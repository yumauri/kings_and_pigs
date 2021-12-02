import pygame


class Entity(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.vx = 0
        self.vy = 0
        self.weight = 1

        # to dynamically replace this sprite
        self.replace_with = None

        # to dynamically add new sprites
        self.emit_new = None

    def change_image(self, image):
        if self.image is not image:
            self.image = image
            x = self.rect.x
            y = self.rect.y
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

    def apply_gravity(self, gravity):
        self.vy += gravity

    def apply_friction(self, weight):
        if self.vx > 0:
            self.vx = max(self.vx - weight, 0)
        elif self.vx < 0:
            self.vx = min(self.vx + weight, 0)

    def move(self, chamber):
        # horizontal move
        self.rect.x += self.vx

        # check collisions with walls
        walls_hit_list = pygame.sprite.spritecollide(self, chamber.walls, False)
        for wall in walls_hit_list:
            if self.vx > 0:
                self.rect.right = wall.rect.left
                self.vx = 0
            elif self.vx < 0:
                self.rect.left = wall.rect.right
                self.vx = 0

        # check collisions with floors
        # if object already collides with some floors - just ignore them later
        collisions = []
        floors_hit_list = pygame.sprite.spritecollide(self, chamber.floors, False)
        for floor in floors_hit_list:
            if floor is not self:
                collisions.append(floor)

        # vertical move
        self.rect.y += self.vy
        on_ground = False

        # check collisions with floors
        floors_hit_list = pygame.sprite.spritecollide(self, chamber.floors, False)
        for floor in floors_hit_list:
            if floor is not self and floor not in collisions:
                if self.vy > 0:
                    self.rect.bottom = floor.rect.top
                    self.vy = 0
                    on_ground = True

        if on_ground:
            self.apply_friction(self.weight)
