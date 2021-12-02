import pygame
from ..functions import loader


# volume control icons sprites loader
load_image = loader("kings_and_pigs/data/sprites")


class VolumeControl:
    def __init__(self, player, dx, dy):
        self.player = player
        self.dx, self.dy = dx, dy

        self.music_on = load_image("music_on.png")
        self.music_off = load_image("music_off.png")
        self.sound_on = load_image("sound_on.png")
        self.sound_off = load_image("sound_off.png")

        # resize images
        self.music_on = pygame.transform.scale(self.music_on, (20, 20))
        self.music_off = pygame.transform.scale(self.music_off, (20, 20))
        self.sound_on = pygame.transform.scale(self.sound_on, (20, 20))
        self.sound_off = pygame.transform.scale(self.sound_off, (20, 20))

        self.layer = pygame.Surface([300, 30], pygame.SRCALPHA, 32)

    def mute(self):
        muted = self.player.mute_music or self.player.mute_sounds
        self.player.mute(music=not muted, sound=not muted)

    def process_event(self, event):
        x, y = event.pos
        x -= self.dx
        y -= self.dy

        sound_x = 25
        music_x = 175
        width = 105

        if (0 < x < 20 or 150 < x < 170) and 5 < y < 25:
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)

        if event.type == pygame.MOUSEMOTION and any(event.buttons):
            # change sounds volume by drag
            if sound_x <= x <= sound_x + width and 5 < y < 20:
                self.player.set_volume(sound=((x - sound_x) / width))

            # change music volume by drag
            elif music_x <= x <= music_x + width and 5 < y < 20:
                self.player.set_volume(music=((x - music_x) / width))

        if event.type == pygame.MOUSEBUTTONDOWN:
            # mute/unmute sounds
            if 0 < x < 20 and 5 < y < 25:
                self.player.mute(sound=not self.player.mute_sounds)

            # mute/unmute music
            elif 150 < x < 170 and 5 < y < 25:
                self.player.mute(music=not self.player.mute_music)

            # change sounds volume by click
            elif sound_x <= x <= sound_x + width and 5 < y < 20:
                self.player.set_volume(sound=((x - sound_x) / width))

            # change music volume by click
            elif music_x <= x <= music_x + width and 5 < y < 20:
                self.player.set_volume(music=((x - music_x) / width))

    def draw(self):
        self.layer.fill((0, 0, 0, 0))

        # draw icons
        if self.player.volume_sounds > 0 and not self.player.mute_sounds:
            self.layer.blit(self.sound_on, (0, 5))
        else:
            self.layer.blit(self.sound_off, (0, 5))

        if self.player.volume_music > 0 and not self.player.mute_music:
            self.layer.blit(self.music_on, (150, 5))
        else:
            self.layer.blit(self.music_off, (150, 5))

        # draw bars
        sound_x = 25
        music_x = 175
        width = 105
        height = 15
        pygame.draw.polygon(
            self.layer,
            (255, 255, 255, 100),
            [(sound_x, 20), (sound_x + width, 20 - height), (sound_x + width, 20)],
        )
        pygame.draw.polygon(
            self.layer,
            (255, 255, 255, 100),
            [(music_x, 20), (music_x + width, 20 - height), (music_x + width, 20)],
        )

        # draw volume levels
        sound_pos = width * self.player.volume_sounds
        music_pos = width * self.player.volume_music
        sound_y = height * self.player.volume_sounds
        music_y = height * self.player.volume_music
        pygame.draw.polygon(
            self.layer,
            (255, 255, 255),
            [
                (sound_x, 20),
                (sound_x + sound_pos, 20 - sound_y),
                (sound_x + sound_pos, 20),
            ],
        )
        pygame.draw.polygon(
            self.layer,
            (255, 255, 255),
            [
                (music_x, 20),
                (music_x + music_pos, 20 - music_y),
                (music_x + music_pos, 20),
            ],
        )
