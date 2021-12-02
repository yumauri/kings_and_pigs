import sys
import platform
import pygame
from .entities import Game


def run():
    print("Platform:", platform.platform())
    print("Python version:", sys.version.replace("\n", " "))
    print(
        "PyGame version: {} (SDL {}.{}.{})".format(
            pygame.version.ver, *pygame.get_sdl_version()
        )
    )

    # init pygame
    pygame.mixer.pre_init()
    pygame.init()

    # create and start game
    game = Game()
    game.loop()
    pygame.quit()
    sys.exit()
