import pygame
from kings_and_pigs import ANIMATION_FPS


class Animation:
    def __init__(self, sheet, n):
        w = sheet.get_width() // n
        h = sheet.get_height()

        self.n = n
        self.sheet = sheet
        self.tick = None
        self.frames = [
            sheet.subsurface(pygame.Rect((w * i, 0), (w, h))) for i in range(n)
        ]
        self.frame = self.frames[0]
        self.idx = 0
        self.loop = True
        self.should_update = True
        self.on_done_callbacks = []

    def flip(self):
        inverted = Animation(self.sheet, self.n)
        inverted.frames = [
            pygame.transform.flip(frame, True, False) for frame in inverted.frames
        ]
        inverted.frame = inverted.frames[0]
        return inverted

    def rotate(self, angle):
        rotated = Animation(self.sheet, self.n)
        rotated.frames = [
            pygame.transform.rotate(frame, angle) for frame in rotated.frames
        ]
        rotated.frame = rotated.frames[0]
        return rotated

    def reset(self):
        self.tick = None
        self.frame = self.frames[0]
        self.idx = 0
        self.loop = True
        self.should_update = True
        self.on_done_callbacks = []

    def on_done(self, callback, stop=False):
        self.on_done_callbacks.append(callback)
        if stop:
            self.loop = False

    def update(self):
        if not self.should_update:
            return

        now = pygame.time.get_ticks()
        if self.tick is None:
            self.tick = now
        elif now - self.tick >= 1000 / ANIMATION_FPS:
            if self.idx == len(self.frames) - 1:
                for cb in self.on_done_callbacks:
                    cb()
                self.on_done_callbacks = []
                if not self.loop:
                    self.should_update = False
                    return

            self.tick = now
            self.idx = (self.idx + 1) % len(self.frames)
            self.frame = self.frames[self.idx]
