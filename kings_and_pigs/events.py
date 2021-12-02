import pygame


# hero control keys
LEFT = [pygame.K_LEFT]
RIGHT = [pygame.K_RIGHT]
JUMP = [pygame.K_SPACE]
FALL = [pygame.K_DOWN]
ATTACK = [pygame.K_RCTRL, pygame.K_LCTRL, pygame.K_x]
GO_IN = [pygame.K_UP]

# control keys
PAUSE = [pygame.K_p]
QUIT = [pygame.K_q]
RESTART = [pygame.K_r]
YES = [pygame.K_y]
NO = [pygame.K_n]
NEXT_TRACK = [pygame.K_n]
ALL_MUTE = [pygame.K_m]
DEBUG_AI = [pygame.K_d]

# custom events to rule the world
SHAKE_WORLD = pygame.USEREVENT + 1
GO_CHAMBER = pygame.USEREVENT + 2
AUTO_NEXT_TRACK = pygame.USEREVENT + 3
PLAY_SOUND = pygame.USEREVENT + 4
DEAD = pygame.USEREVENT + 5
WIN = pygame.USEREVENT + 6
GAME_OVER = pygame.USEREVENT + 7
VICTORY = pygame.USEREVENT + 8
RESET = pygame.USEREVENT + 9
