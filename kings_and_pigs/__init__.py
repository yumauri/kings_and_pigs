import os


# to hide pygame welcome message
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"


#
# game global constants
#

TITLE = "Kings and Pigs"

# map grid size
GRID_SIZE = 32

# size of a virtual screen
WIDTH = 14 * GRID_SIZE  # 448 px
HEIGHT = 7 * GRID_SIZE  # 224 px

# real window size (double size of virtual screen)
WINDOW_WIDTH = WIDTH * 2  # 896 px
WINDOW_HEIGHT = HEIGHT * 2  # 448 px

# game and animations frames per second
GAME_FPS = 60
ANIMATION_FPS = 10
