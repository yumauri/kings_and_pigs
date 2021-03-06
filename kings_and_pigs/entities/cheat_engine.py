import re
import pygame


class Cheat:
    name: str
    code: str
    enabled: bool
    exact_pattern: re.Pattern[str]
    pattern: re.Pattern[str]
    actual: str

    def __init__(self, name: str, code: str):
        self.name = name
        self.code = code
        self.enabled = False
        self.exact_pattern = re.compile("^" + code.replace("#", "\\d") + "$")
        self.pattern = re.compile("^" + code.replace("#", "\\d?") + "$")

    def pick(self):
        if self.enabled:
            self.enabled = False
            return True
        return False


class CheatEngine:
    def __init__(self, width, height):
        self.locked = False
        self.code = ""
        self.codes = [
            Cheat("debug", "kpdebug"),
            Cheat("god_mode", "kpgod"),
            Cheat("full_health", "kpheal"),
            Cheat("full_score", "kprich"),
            Cheat("suicide", "kpdie"),
            Cheat("win", "kpwin"),
            Cheat("kill_all", "kpkillall"),
            Cheat("goto", "kpgoto##"),
        ]
        self.timeout = pygame.time.get_ticks()
        self.layer = pygame.Surface([width, height], pygame.SRCALPHA, 32)
        self.font = pygame.font.Font(None, 12)

    def lock(self):
        self.timeout = pygame.time.get_ticks()
        self.locked = True

    def unlock(self):
        self.locked = False

    def add(self, char):
        self.code += char

    def reset(self):
        self.code = ""
        self.unlock()

    def process_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.unicode:
                self.add(event.unicode)

                correct = False
                for cheat in self.codes:
                    if self.code == cheat.code or cheat.exact_pattern.match(self.code):
                        correct = True
                        cheat.enabled = not cheat.enabled
                        if cheat.enabled:
                            cheat.actual = self.code
                        break
                    elif cheat.code.startswith(self.code) or cheat.pattern.match(self.code):
                        correct = True
                        break

                if correct:
                    self.lock()
                else:
                    self.reset()

    def update(self):
        now = pygame.time.get_ticks()
        if self.locked:
            if now - self.timeout > 1000:
                self.reset()

    def draw(self):
        self.layer.fill((0, 0, 0, 0))
        if self.debug.enabled:
            y = 0
            for cheat in self.codes:
                if cheat.enabled:
                    name = self.font.render(cheat.name + ": true", True, (0, 0, 0))
                    pygame.draw.rect(
                        self.layer,
                        (255, 255, 255, 100),
                        (100 - 1, y - 1, name.get_width() + 2, 10),
                    )
                    self.layer.blit(name, (100, y))
                    y += 10

            if self.locked:
                current = self.font.render(self.code, True, (100, 0, 0))
                pygame.draw.rect(
                    self.layer,
                    (255, 255, 255, 100),
                    (150 - 1, -1, current.get_width() + 2, 10),
                )
                self.layer.blit(current, (150, 0))

    def __getattr__(self, key):
        for cheat in self.codes:
            if cheat.name == key:
                return cheat
        return None
