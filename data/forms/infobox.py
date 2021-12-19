""" This module provides labels as form objects that can be used in titles

:project: resa
:source: https://github.com/Kanasaru/resa
:license: GNU General Public License v3
"""

from data.settings import conf
import pygame
from data.forms.form import Form


class InfoBox(Form):
    def __init__(self, text: str, pos_y, display_time: int = 3000) -> None:
        Form.__init__(self, (0, 0))

        # render font and check width
        self.font = pygame.font.Font(conf.std_font, conf.std_font_size)
        self.font_image = self.font.render(text, True, conf.COLOR_WHITE)
        self.font_rect = self.font_image.get_rect()

        self.image = pygame.Surface((conf.resolution[0] / 2, self.font_rect.height + 20))
        self.rect = self.image.get_rect()
        self.image.fill(conf.COLOR_BLACK)
        self.image.set_alpha(192)

        self.image.blit(self.font_image, ((self.rect.width - self.font_rect.width) / 2, 10))

        self.pos_x = (conf.resolution[0] - self.rect.width) / 2
        self.goal_pos_y = pos_y
        self.pos_y = 0 - self.font_rect.height
        self.pos_start = self.pos_y

        self.timer = pygame.time.Clock()
        self.time = 0
        self.display_time = display_time
        self.fade_in = True
        self.fade_out = False

    def update(self):
        time = self.timer.tick()

        if self.fade_in:
            if self.pos_y < self.goal_pos_y:
                self.pos_y += 1
            else:
                self.fade_in = False
        elif self.fade_out:
            if self.pos_y > self.pos_start:
                self.pos_y -= 1
            else:
                self.kill()
        elif self.time >= self.display_time:
            self.fade_out = True
        else:
            self.time += time

        self.rect.x = self.pos_x
        self.rect.y = self.pos_y
