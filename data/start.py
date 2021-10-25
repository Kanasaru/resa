import pygame
import data.eventcodes
from data import settings
from data.helpers import event
from data.game import Game
from data.forms import title, textbox


class Start(object):
    def __init__(self):
        pygame.init()

        self.surface = pygame.display.set_mode(settings.RESOLUTION)
        self.leave = False
        self.clock = pygame.time.Clock()
        self.events = data.helpers.event.EventList()
        self.game = None

        self.title_main = None

        pygame.display.set_caption(f"{settings.GAME_TITLE} in v{settings.GAME_VERSION} by {settings.GAME_AUTHOR}")

        self.build_titles()
        self.loop()

    def loop(self):
        while not self.leave:
            self.clock.tick(settings.FPS)
            self.handle_events()
            self.run_logic()
            self.render()

        self.exit()

    def handle_events(self):
        for event in self.title_main.get_events():
            if event.code == data.eventcodes.STARTGAME:
                self.game = Game(self.surface)
            elif event.code == data.eventcodes.LOADGAME:
                pass
            elif event.code == data.eventcodes.QUITGAME:
                self.leave = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.leave = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    z = pygame.mouse.get_pos()
                if event.button == 2:
                    pass
            else:
                pass

    def run_logic(self):
        self.title_main.run_logic()

    def render(self):
        self.surface.fill(settings.COLOR_WHITE)

        self.title_main.render(self.surface)

        pygame.display.flip()

    def exit(self):
        pygame.quit()
        print("Bye bye!")

    def build_titles(self):
        display_width = 1280
        self.title_main = data.forms.title.Title({
            "pos_x": 0,
            "pos_y": 0,
            "width": settings.RESOLUTION[0],
            "height": settings.RESOLUTION[0],
            "bg_color": settings.COLOR_TEAL,
            "colorkey": settings.COLOR_KEY,
        })
        tf_headline = data.forms.textbox.Textbox({
            "pos_y": 20,
            "text": "RESA",
            "font_size": 90,
            "text_font": settings.BASIC_FONT,
            "font_color": settings.COLOR_BLACK,
            "colorkey": settings.COLOR_KEY,
        })
        pos_x = display_width / 2 - tf_headline.width() / 2
        tf_headline.set_attr(("pos_x", pos_x))
        self.title_main.add(tf_headline)
        tf_version = data.forms.textbox.Textbox({
            "pos_x": self.title_main.get_attr("width") - 5,
            "pos_y": 5,
            "text": f"Version: {settings.GAME_VERSION}",
            "font_size": 14,
            "text_font": settings.BASIC_FONT,
            "font_color": settings.COLOR_BLACK,
            "position": "right",
            "colorkey": settings.COLOR_KEY,
        })
        self.title_main.add(tf_version)
