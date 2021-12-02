import pygame
from ..events import RESET
from ..functions import loader
from ..database import Database
from .stats_diamond import StatsDiamond


# stats sprites loader
load_image = loader("kings_and_pigs/data/sprites")


class Outro:
    MESSAGE = 0
    ENTER_NAME = 1
    SCORE_TABLE = 2
    RESET = 3

    def __init__(self, w, h, score, win):
        self.width = w
        self.height = h
        self.score = score
        self.win = win

        self.background_layer = pygame.Surface([w, h], pygame.SRCALPHA, 32)
        self.active_layer = pygame.Surface([w, h], pygame.SRCALPHA, 32)
        self.background_layer.fill((0, 0, 0))
        self.stage = Outro.MESSAGE

        self.title = load_image("Kings and Pigs.png")
        self.cross = load_image("Cross.png")

        self.font = pygame.font.Font("kings_and_pigs/data/font.ttf", 20)
        self.font_name = pygame.font.Font("kings_and_pigs/data/font.ttf", 18)
        self.font_score = pygame.font.Font("kings_and_pigs/data/font.ttf", 10)

        self.text_enter_name = self.font.render(
            "enter you name", False, (100, 100, 100)
        )
        self.text_reset = self.font_score.render(
            "press R to reset", False, (100, 100, 100)
        )

        self.x = w / 2 - self.title.get_width() / 2
        self.y = 10

        self.name = ""

    def add_and_get_scores(self, name, score, win):
        db = Database()
        self.id = db.add_score(name, score, win)
        self.table = db.get_top_scores()
        db.close()

    def init_draw_objects(self):
        texts = []
        for row in self.table:
            name = row["name"]
            color = (200, 75, 75) if row["id"] == self.id else (200, 200, 200)
            texts.append(self.font_score.render(name, False, color))

        max_width = max(t.get_width() for t in texts)
        height = texts[0].get_height()
        max_height = height * len(self.table)
        start_y = self.height / 2 - max_height / 2

        self.diamonds = pygame.sprite.Group()

        for i, row in enumerate(self.table):
            text = texts[i]
            score = row["score"]
            win = row["win"]

            # draw name
            x = self.width / 2 - max_width / 2 - 20
            y = start_y + height * i
            self.background_layer.blit(text, (x, y))

            # draw cross if not win
            if not win:
                self.background_layer.blit(self.cross, (x - 12, y + 2))

            # draw line
            xe = x + max_width + 5
            ye = y + height
            pygame.draw.line(
                self.background_layer, (20, 20, 20), (x, ye), (xe, ye), width=1
            )

            # draw diamonds
            diamond = StatsDiamond(xe + 5, y)
            self.diamonds.add(diamond)

            # draw numbers
            layer = diamond.number(score)
            self.background_layer.blit(layer, (xe + 24, y + 2))

    def process_event(self, event):
        if self.stage == Outro.MESSAGE:
            self.stage = Outro.ENTER_NAME

        elif self.stage == Outro.ENTER_NAME:
            if event.key == pygame.K_RETURN:
                if not self.name:
                    self.name = "noname"
                self.add_and_get_scores(self.name, self.score, self.win)
                self.init_draw_objects()
                self.stage = Outro.SCORE_TABLE

            elif event.key == pygame.K_BACKSPACE:
                self.name = self.name[:-1]

            elif event.unicode and event.unicode.encode().isalpha():
                if len(self.name) < 20:
                    self.name += event.unicode

        elif self.stage == Outro.SCORE_TABLE:
            # handle A as well, because it is hard to tell A or R in the font :)
            if event.key == pygame.K_r or event.key == pygame.K_a:
                self.stage = Outro.RESET
                pygame.time.set_timer(RESET, 500, True)

    def update_message(self):
        pass

    def draw_message(self):
        pass

    def update(self):
        if self.stage == Outro.MESSAGE:
            self.update_message()

        if self.stage == Outro.SCORE_TABLE:
            self.diamonds.update()

        elif self.stage == Outro.RESET:
            self.y = min(self.y + 5, self.height / 2 - self.title.get_height() / 2)

    def draw(self):
        self.active_layer.fill((0, 0, 0, 0))

        if self.stage == Outro.MESSAGE:
            self.draw_message()

        elif self.stage == Outro.ENTER_NAME:
            self.active_layer.blit(self.title, (self.x, self.y))
            self.active_layer.blit(self.text_enter_name, (118, 70))

            name = self.font_name.render(self.name + "_", True, (200, 75, 75))
            x = self.width / 2 - name.get_width() / 2
            y = self.height / 2 - name.get_height() / 2
            self.active_layer.blit(name, (x, y))

        elif self.stage == Outro.SCORE_TABLE:
            self.active_layer.blit(self.title, (self.x, self.y))
            self.diamonds.draw(self.active_layer)

            x = self.width / 2 - self.text_reset.get_width() / 2
            y = self.height - 10 - self.text_reset.get_height()
            self.active_layer.blit(self.text_reset, (x, y))

        elif self.stage == Outro.RESET:
            self.background_layer.fill((0, 0, 0))
            self.active_layer.blit(self.title, (self.x, self.y))
