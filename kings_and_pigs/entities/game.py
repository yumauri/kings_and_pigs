import pygame
import random
from kings_and_pigs import *
from ..events import *
from ..ai import AI
from ..player import Player
from .volume_control import VolumeControl
from .cheat_engine import CheatEngine
from .splash import Splash
from .game_over import GameOver
from .victory import Victory
from .entity import Entity
from .castle import Castle
from .hero import Hero
from .enemy import Enemy
from .stats import Stats


class Game:
    SPLASH = 0
    PLAYING = 1
    PAUSED = 2
    GAME_OVER = 3
    VICTORY = 4
    QUIT = 5
    RESTART = 6

    def __init__(self):
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.screen = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA, 32)

        font = pygame.font.Font("kings_and_pigs/data/font.ttf", 20)
        self.text_quit = font.render("quit? y/n", False, (200, 200, 200))
        self.text_restart = font.render("restart? y/n", False, (200, 200, 200))

        pygame.display.set_caption(TITLE)

        self.clock = pygame.time.Clock()
        self.done = False
        self.finish = False

        self.ai = None
        self.player = Player()
        self.volume_control = VolumeControl(self.player, WINDOW_WIDTH - 300, 0)
        self.splash()

        self.shake_x = 0
        self.shake_y = 0

        # to avoid vertical moving camera when hero jumps
        self.last_camera_y = None
        self.new_camera_y = None

        self.fade = 255
        self.fade_step = -10

    def splash(self):
        self.stage = Game.SPLASH
        self.splash_screen = Splash(WIDTH, HEIGHT)

    def start(self):
        self.fade = 255
        self.fade_step = -10
        self.stage = Game.PLAYING
        self.finish = False
        self.cheats = CheatEngine(WIDTH, HEIGHT)
        self.hero = Hero(self.cheats)
        self.stats = Stats(self.hero)
        self.castle = Castle()
        self.chamber = self.castle.chamber
        self.hero.respawn(self.chamber)
        self.ai = AI(WIDTH, HEIGHT, self.chamber, self.hero, self.cheats)
        self.last_camera_y = None
        self.new_camera_y = None

    def game_over(self):
        self.stage = Game.GAME_OVER
        self.outro_screen = GameOver(WIDTH, HEIGHT, self.hero.score)

    def victory(self):
        self.stage = Game.VICTORY
        self.outro_screen = Victory(WIDTH, HEIGHT, self.hero.score)

    def process_events(self):
        for event in pygame.event.get():
            if self.stage == Game.PLAYING:
                self.cheats.process_event(event)

            if event.type == pygame.QUIT:
                self.done = True

            elif (
                event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONDOWN
            ):
                self.volume_control.process_event(event)

            elif event.type == pygame.KEYDOWN:
                if self.stage == Game.SPLASH:
                    self.start()
                    self.player.play()

                elif self.stage == Game.PLAYING:
                    if event.key in LEFT:
                        self.hero.step_left()
                    elif event.key in RIGHT:
                        self.hero.step_right()
                    elif event.key in JUMP:
                        self.hero.jump(self.chamber.floors)
                    elif event.key in FALL:
                        self.hero.fall_down(self.chamber.walls)
                    elif event.key in ATTACK:
                        self.hero.attack(self.chamber.active_sprites, self.chamber)
                    elif event.key in GO_IN:
                        self.hero.go_in(self.chamber.active_sprites)
                    elif event.key in PAUSE and not self.cheats.locked:
                        self.stage = Game.PAUSED
                        self.player.pause()
                    elif event.key in QUIT and not self.cheats.locked:
                        self.stage = Game.QUIT
                        self.player.pause()
                    elif event.key in RESTART and not self.cheats.locked:
                        self.stage = Game.RESTART
                        self.player.pause()
                    elif event.key in NEXT_TRACK and not self.cheats.locked:
                        self.player.play_next()
                    elif event.key in ALL_MUTE and not self.cheats.locked:
                        self.volume_control.mute()

                elif self.stage == Game.PAUSED:
                    if event.key in PAUSE:
                        self.stage = Game.PLAYING
                        self.player.unpause()

                elif self.stage == Game.QUIT:
                    if event.key in YES:
                        self.done = True

                    elif event.key in NO:
                        self.stage = Game.PLAYING
                        self.player.unpause()

                elif self.stage == Game.RESTART:
                    if event.key in YES:
                        self.start()
                        self.player.play()

                    elif event.key in NO:
                        self.stage = Game.PLAYING
                        self.player.unpause()

                elif self.stage == Game.GAME_OVER or self.stage == Game.VICTORY:
                    self.outro_screen.process_event(event)

            elif event.type == SHAKE_WORLD and self.stage == Game.PLAYING:
                self.shake_x = random.choice([-4, -3, -2, 2, 3, 4])
                self.shake_y = random.choice([-4, -3, -2, 2, 3, 4])

            elif event.type == GO_CHAMBER and self.stage == Game.PLAYING:
                self.castle.use_door(event.door)
                self.fade_step = 10

            elif event.type == PLAY_SOUND and self.stage == Game.PLAYING:
                self.player.sound(event.sound)

            elif event.type == AUTO_NEXT_TRACK:
                self.player.queue_next()

            elif event.type == DEAD:
                self.fade_step = 2
                self.player.stop()
                self.finish = True
                pygame.time.set_timer(GAME_OVER, 2000, True)

            elif event.type == WIN:
                self.fade_step = 2
                self.player.stop()
                self.finish = True
                pygame.time.set_timer(VICTORY, 2000, True)

            elif event.type == GAME_OVER:
                self.player.sound("death")
                self.game_over()

            elif event.type == VICTORY:
                self.player.sound("win")
                self.victory()

            elif event.type == RESET:
                self.splash()

            # pass event to AI
            if self.ai is not None:
                self.ai.process_event(event)

        pressed = pygame.key.get_pressed()

        if self.stage == Game.PLAYING:
            if any(pressed[k] for k in LEFT):
                self.hero.move_left()
            elif any(pressed[k] for k in RIGHT):
                self.hero.move_right()
            else:
                self.hero.stop()

    def update(self):
        if self.stage == Game.SPLASH:
            self.splash_screen.update()

        elif self.stage == Game.PLAYING:
            self.fade = max(min(self.fade + self.fade_step, 255), 0)
            if self.fade_step > 0 and self.fade == 255 and self.hero.lives > 0:
                self.fade_step *= -1
                if not self.finish:
                    door = self.castle.swap_chamber()
                    self.chamber = self.castle.chamber
                    self.ai.chamber = self.chamber
                    self.last_camera_y = None
                    self.new_camera_y = None
                    self.hero.go_out(door)
            elif self.fade_step < 0 and self.fade == 0:
                self.fade_step = 0

            self.hero.update(self.chamber)
            self.chamber.active_sprites.update(self.chamber, self.hero)
            self.stats.update()
            self.replace_and_emit()

            # pass negative offset, because we want to get offset,
            # relative to chamber, not relative to view
            offset_x, offset_y = self.calculate_offset()
            self.ai.update(-offset_x, -offset_y)

            # process cheats
            self.cheats.update()
            if self.cheats.kill_all.pick():
                for enemy in self.chamber.enemies:
                    enemy.murder()

        elif self.stage == Game.GAME_OVER or self.stage == Game.VICTORY:
            self.outro_screen.update()

    def replace_and_emit(self):
        for sprite in self.chamber.active_sprites:

            # replace sprite with another sprites
            replace_with = sprite.replace_with
            if replace_with is not None:
                sprite.kill()
                if isinstance(replace_with, Entity):
                    replace_with = [replace_with]
                for replacement in replace_with:
                    self.chamber.active_sprites.add(replacement)
                    if isinstance(replacement, Enemy):
                        self.chamber.enemies.add(replacement)
                sprite.replace_with = None

            # add new sprites
            emit_new = sprite.emit_new
            if emit_new is not None:
                if isinstance(sprite.emit_new, Entity):
                    emit_new = [emit_new]
                for emitment in emit_new:
                    self.chamber.active_sprites.add(emitment)
                    if isinstance(emitment, Enemy):
                        self.chamber.enemies.add(emitment)
                sprite.emit_new = None

    def calculate_offset(self):
        hero_hit_box = self.hero.get_hit_box()
        hero_x = hero_hit_box.centerx
        hero_y = hero_hit_box.centery

        # to avoid vertical moving camera when hero jumps
        if self.last_camera_y is None or self.new_camera_y is None:
            self.last_camera_y = self.new_camera_y = hero_y
        if self.hero.on_ground:
            self.new_camera_y = hero_y
            if self.new_camera_y != self.last_camera_y:
                self.last_camera_y += (-1, 1)[self.new_camera_y > self.last_camera_y]
                hero_y = self.last_camera_y
        else:
            hero_y = self.last_camera_y

        x = -1 * hero_x + WIDTH / 2
        y = -1 * hero_y + HEIGHT / 2

        if hero_x < WIDTH / 2:
            x = 0
        elif hero_x > self.chamber.width - WIDTH / 2:
            x = -1 * self.chamber.width + WIDTH

        if hero_y < HEIGHT / 2:
            y = 0
        elif hero_y > self.chamber.height - HEIGHT / 2:
            y = -1 * self.chamber.height + HEIGHT

        if self.shake_x > 0:
            self.shake_x = self.shake_x - 1
        elif self.shake_x < 0:
            self.shake_x = self.shake_x + 1

        if self.shake_y > 0:
            self.shake_y = self.shake_y - 1
        elif self.shake_y < 0:
            self.shake_y = self.shake_y + 1

        return x + self.shake_x, y + self.shake_y

    def draw(self):
        if self.stage == Game.SPLASH:
            self.splash_screen.draw()
            self.screen.blit(self.splash_screen.background_layer, [0, 0])
            self.screen.blit(self.splash_screen.active_layer, [0, 0])

        elif (
            self.stage == Game.PLAYING
            or self.stage == Game.PAUSED
            or self.stage == Game.QUIT
            or self.stage == Game.RESTART
        ):
            offset_x, offset_y = self.calculate_offset()

            self.chamber.active_layer.fill((0, 0, 0, 0))
            self.chamber.active_sprites.draw(self.chamber.active_layer)

            self.chamber.active_layer.blit(
                self.hero.image, [self.hero.rect.x, self.hero.rect.y]
            )

            self.screen.blit(self.chamber.background_layer, [offset_x, offset_y])
            self.screen.blit(self.chamber.walls_layer, [offset_x, offset_y])
            self.screen.blit(self.chamber.floors_layer, [offset_x, offset_y])
            self.screen.blit(self.chamber.decorations_layer, [offset_x, offset_y])
            self.screen.blit(self.chamber.inactive_layer, [offset_x, offset_y])
            self.screen.blit(self.chamber.active_layer, [offset_x, offset_y])

            # draw hero stats

            self.stats.active_layer.fill((0, 0, 0, 0))
            self.stats.active_sprites.draw(self.stats.active_layer)
            if self.stats.score_layer:
                self.stats.active_layer.blit(self.stats.score_layer, [34, 27])

            self.screen.blit(self.stats.background_layer, [7, 7])
            self.screen.blit(self.stats.active_layer, [7, 7])

            # draw AI layer

            # pass negative offset, because we want to get offset,
            # relative to chamber, not relative to view
            self.ai.draw(-offset_x, -offset_y)
            self.screen.blit(self.ai.layer, [0, 0])

            # draw cheat engine layer

            self.cheats.draw()
            self.screen.blit(self.cheats.layer, [0, 0])

            # fade screen when changing chamber
            if self.fade > 0:
                fade_layer = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA, 32)
                fade_layer.set_alpha(self.fade)
                fade_layer.fill((0, 0, 0))
                self.screen.blit(fade_layer, [0, 0])

            # fade and distort screen when paused
            if (
                self.stage == Game.PAUSED
                or self.stage == Game.QUIT
                or self.stage == Game.RESTART
            ):
                pause_layer = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA, 32)
                pause_layer.set_alpha(150)
                pause_layer.fill((0, 0, 0))

                # draw || pause sign
                if self.stage == Game.PAUSED:
                    pygame.draw.rect(
                        pause_layer,
                        (200, 200, 200),
                        pygame.Rect(WIDTH / 2 - 25, HEIGHT / 2 - 20, 20, 40),
                    )
                    pygame.draw.rect(
                        pause_layer,
                        (200, 200, 200),
                        pygame.Rect(WIDTH / 2 + 5, HEIGHT / 2 - 20, 20, 40),
                    )

                self.screen.blit(pause_layer, [0, 0])

                # distort whole screen by scaling and upscaling it
                distorted_layer = pygame.transform.scale(
                    self.screen, (WIDTH // 2, HEIGHT // 2)
                )
                distorted_layer = pygame.transform.scale(
                    distorted_layer, (WIDTH, HEIGHT)
                )
                self.screen.blit(distorted_layer, [0, 0])

                # ask, if player really wants to quit?
                if self.stage == Game.QUIT:
                    x = WIDTH / 2 - self.text_quit.get_width() / 2
                    y = HEIGHT / 2 - self.text_quit.get_height() / 2
                    self.screen.blit(self.text_quit, (x, y))

                # ask, if player really wants to restart?
                if self.stage == Game.RESTART:
                    x = WIDTH / 2 - self.text_restart.get_width() / 2
                    y = HEIGHT / 2 - self.text_restart.get_height() / 2
                    self.screen.blit(self.text_restart, (x, y))

        elif self.stage == Game.GAME_OVER or self.stage == Game.VICTORY:
            self.outro_screen.draw()
            self.screen.blit(self.outro_screen.background_layer, [0, 0])
            self.screen.blit(self.outro_screen.active_layer, [0, 0])

        # draw screen on the window
        # we need this to upscale whole screen x2 times
        self.window.blit(
            pygame.transform.scale(self.screen, self.window.get_rect().size), (0, 0)
        )

        # draw sound controls
        if self.stage == Game.PLAYING:
            self.volume_control.draw()
            if self.fade > 0:
                self.volume_control.layer.set_alpha(255 - self.fade)
            self.window.blit(self.volume_control.layer, [WINDOW_WIDTH - 300, 0])

        pygame.display.flip()

    def loop(self):
        while not self.done:
            self.process_events()
            self.update()
            self.draw()
            self.clock.tick(GAME_FPS)
