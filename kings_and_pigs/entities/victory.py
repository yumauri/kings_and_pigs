import random
import pygame
from .outro import Outro


class Victory(Outro):
    def __init__(self, w, h, score):
        super().__init__(w, h, score, True)

        self.text_victory = self.font.render("you win!", False, (200, 75, 75))
        self.text_any_key = self.font_score.render(
            "press any key", False, (100, 100, 100)
        )

        self.particles = []
        self.appear = pygame.time.get_ticks()
        self.show_hint = False
        self.alpha = 0
        self.d = 5

    def update_message(self):
        # add more firework particles
        if random.random() < 0.06:
            x = random.randrange(0, self.width)
            y = random.randrange(0, self.height)
            for i in range(20):
                self.particles.append(
                    [
                        [x, y],  # initial position
                        [
                            random.randint(0, 40) / 6 - 4,  # x velocity
                            random.randint(0, 40) / 6 - 4,  # y velocity
                        ],
                        random.randint(3, 4),  # particle size
                    ]
                )

        # move, resize and remove particles
        for particle in self.particles:
            particle[0][0] += particle[1][0]  # move by x axis
            particle[0][1] += particle[1][1]  # move by y axis
            particle[1][1] += 0.1  # increase y velocity
            particle[2] -= 0.04  # decrease size
            if particle[2] <= 0:
                self.particles.remove(particle)

        if not self.show_hint:
            now = pygame.time.get_ticks()
            if now - self.appear >= 1500:
                self.show_hint = True
        else:
            if self.alpha <= 0:
                self.d = 5
            elif self.alpha >= 255:
                self.d = -5
            self.alpha = min(max(self.alpha + self.d, 0), 255)

    def draw_message(self):
        # draw particles with random colors
        for particle in self.particles:
            c1 = random.randrange(0, 255)
            c2 = random.randrange(0, 255)
            c3 = random.randrange(0, 255)
            pygame.draw.circle(
                self.active_layer,
                (c1, c2, c3),
                [int(particle[0][0]), int(particle[0][1])],
                int(particle[2]),
            )

        # draw "you win!" message
        self.active_layer.blit(self.text_victory, (155, 100))

        # show hint
        if self.show_hint:
            self.text_any_key.set_alpha(self.alpha)
            self.active_layer.blit(self.text_any_key, (175, 120))
