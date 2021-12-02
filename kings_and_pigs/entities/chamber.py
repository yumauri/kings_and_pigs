import re
import pygame
import pytmx
from kings_and_pigs import GRID_SIZE
from .block import Block
from .door import Door
from .invisible_door import InvisibleDoor
from .box import Box
from .bomb import Bomb
from .pig import Pig
from .pig_throwing_box import PigThrowingBox
from .pig_throwing_bomb import PigThrowingBomb
from .pig_king import PigKing


class Chamber:
    def __init__(self, file_path):
        map = self.map = pytmx.load_pygame(file_path)
        w = self.width = map.width * GRID_SIZE
        h = self.height = map.height * GRID_SIZE

        self.gravity = 1

        self.walls = pygame.sprite.Group()
        self.floors = pygame.sprite.Group()
        self.doors = pygame.sprite.Group()
        self.invisible_doors = pygame.sprite.Group()
        self.boxes = pygame.sprite.Group()
        self.bombs = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

        self.active_sprites = pygame.sprite.Group()
        self.inactive_sprites = pygame.sprite.Group()

        self.spawn_x, self.spawn_y = -1, -1
        respawn = self.get_respawn_point()
        if respawn:
            self.spawn_x, self.spawn_y = respawn

        enemies_map_layer = self.get_enemies_objects()
        for enemy in enemies_map_layer:
            if enemy.type and "king" in enemy.type:
                pig = PigKing(enemy.x, enemy.y, enemy.type)
            elif enemy.type and "box" in enemy.type:
                pig = PigThrowingBox(enemy.x, enemy.y, enemy.type)
            elif enemy.type and "bomb" in enemy.type:
                pig = PigThrowingBomb(enemy.x, enemy.y, enemy.type)
            else:
                pig = Pig(enemy.x, enemy.y, enemy.type)
            pig.facing_right = enemy.type and "right" in enemy.type
            self.enemies.add(pig)

        doors_map_layer = self.get_doors_objects()
        for door in doors_map_layer:
            self.doors.add(Door(door.x, door.y, door.type))

        invisible_doors_map_layer = self.get_invisible_doors_objects()
        for door in invisible_doors_map_layer:
            self.invisible_doors.add(
                InvisibleDoor(door.x, door.y, door.width, door.height, door.type)
            )

        boxes_map_layer = self.get_boxes_objects()
        for box in boxes_map_layer:
            self.boxes.add(Box(box.x, box.y))

        bombs_map_layer = self.get_bombs_objects()
        for bomb in bombs_map_layer:
            self.bombs.add(Bomb(bomb.x, bomb.y))

        self.background_layer = pygame.Surface([w, h], pygame.SRCALPHA, 32)
        self.walls_layer = pygame.Surface([w, h], pygame.SRCALPHA, 32)
        self.floors_layer = pygame.Surface([w, h], pygame.SRCALPHA, 32)
        self.decorations_layer = pygame.Surface([w, h], pygame.SRCALPHA, 32)
        self.inactive_layer = pygame.Surface([w, h], pygame.SRCALPHA, 32)
        self.active_layer = pygame.Surface([w, h], pygame.SRCALPHA, 32)

        self.draw_layers("background.*", self.background_layer)
        self.draw_layers("walls.*", self.walls_layer, self.walls)
        self.draw_layers("floors.*", self.floors_layer, self.floors)
        self.draw_layers("decorations.*", self.decorations_layer)

        self.active_sprites.add(*self.doors, *self.boxes, *self.bombs, *self.enemies)
        self.inactive_sprites.add(*self.walls, *self.floors)

        # draw all inactive sprites, they will not move or change
        self.inactive_sprites.draw(self.inactive_layer)

        # hero can jump on top of the box
        # but boxes are not inactive sprites
        self.floors.add(*self.boxes)

        # according to https://www.pygame.org/docs/ref/surface.html#pygame.Surface.convert
        # > It is a good idea to convert all Surfaces before they are blitted many times.
        # so, convert all layers of the chamber, to make them drawing faster.
        # don't know though does this changes anything at all ¯\_(ツ)_/¯
        self.background_layer.convert()
        self.walls_layer.convert()
        self.floors_layer.convert()
        self.decorations_layer.convert()
        self.inactive_layer.convert()
        self.active_layer.convert()

    def draw_layers(self, pattern, surface, group=None):
        map_layers_names = sorted(self.map.layernames.keys())
        for name in map_layers_names:
            if re.match(pattern, name):
                layer = pygame.Surface([self.width, self.height], pygame.SRCALPHA, 32)
                map_layer = self.map.get_layer_by_name(name)
                for x, y, image in map_layer.tiles():
                    layer.blit(image, (x * GRID_SIZE, y * GRID_SIZE))
                    if group is not None:
                        group.add(Block(x * GRID_SIZE, y * GRID_SIZE, image))
                surface.blit(layer, (0, 0))

    def get_respawn_point(self):
        if "spawn" in self.map.objects_by_name:
            spawn = self.map.get_object_by_name("spawn")
            return spawn.x, spawn.y

    def get_enemies_objects(self):
        if "enemies" in self.map.layernames:
            return self.map.get_layer_by_name("enemies")
        return []

    def get_boxes_objects(self):
        if "boxes" in self.map.layernames:
            return self.map.get_layer_by_name("boxes")
        return []

    def get_bombs_objects(self):
        if "bombs" in self.map.layernames:
            return self.map.get_layer_by_name("bombs")
        return []

    def get_doors_objects(self):
        if "doors" in self.map.layernames:
            return self.map.get_layer_by_name("doors")
        return []

    def get_invisible_doors_objects(self):
        if "invisible_doors" in self.map.layernames:
            return self.map.get_layer_by_name("invisible_doors")
        return []
