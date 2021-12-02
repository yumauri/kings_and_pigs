import pygame
from .events import PLAY_SOUND


def load_image(filename, color_key=None):
    image = pygame.image.load(filename)
    if color_key is not None:
        image = image.convert()
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


def loader(path):
    return lambda filename, color_key=None: load_image(f"{path}/{filename}", color_key)


def play(name):
    pygame.event.post(pygame.event.Event(PLAY_SOUND, sound=name))


def event(event_type, **kwargs):
    pygame.event.post(pygame.event.Event(event_type, **kwargs))
