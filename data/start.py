import pygame
import data.eventcodes
from data import settings
from data.helpers import event
from data.game import Game
from data.forms import title, textbox, button


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

        pygame.mixer.music.load('resources/music/sb_indreams.mp3')
        pygame.mixer.music.play(-1, 0.0)
        pygame.mixer.music.set_volume(.2)
        self.pause = False

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
                print("Let's start!")
                # self.game = Game(self.surface)
            elif event.code == data.eventcodes.LOADGAME:
                print("Load Game!")
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
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_p:
                    if self.pause:
                        pygame.mixer.music.unpause()
                        self.pause = False
                    else:
                        pygame.mixer.music.pause()
                        self.pause = True
            else:
                pass

            self.title_main.handle_event(event)

        self.title_main.clear_events()

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
        self.title_main = data.forms.title.Title("main", {
            "pos_x": 0,
            "pos_y": 0,
            "width": settings.RESOLUTION[0],
            "height": settings.RESOLUTION[0],
            "bg_color": settings.COLOR_TEAL,
            "colorkey": settings.COLOR_KEY,
            "bg_image": "resources/images/bg_default.png",
        })
        tf_headline = data.forms.textbox.Textbox("tf_headline", {
            "pos_y": 20,
            "text": "RESA",
            "font_size": 90,
            "text_font": settings.BASIC_FONT,
            "font_color": settings.COLOR_BLACK,
            "colorkey": settings.COLOR_KEY,
        })
        pos_x = self.title_main.width() / 2 - tf_headline.width() / 2
        tf_headline.set_attr(("pos_x", pos_x))
        self.title_main.add(tf_headline)
        tf_version = data.forms.textbox.Textbox("tf_version", {
            "pos_x": self.title_main.width() - 5,
            "pos_y": 5,
            "text": f"Version: {settings.GAME_VERSION}",
            "font_size": 14,
            "text_font": settings.BASIC_FONT,
            "font_color": settings.COLOR_BLACK,
            "position": "right",
            "colorkey": settings.COLOR_KEY,
        })
        self.title_main.add(tf_version)
        width, height = tf_headline.get_dimensions()
        position_y = height + 100
        b_newgame = data.forms.button.Button("b_newgame", {
            "pos_y": position_y,
            "text": "New Game",
            "callback_event": data.helpers.event.Event(
                data.eventcodes.STARTGAME,
                data.eventcodes.STARTGAME
            ),
            "colorkey": settings.COLOR_KEY,
            "spritesheet": "resources/images/sprites/buttons.png"
        })
        b_newgame.set_attr({
            "pos_x": self.title_main.width() / 2 - b_newgame.width() / 2
        })
        self.title_main.add(b_newgame)
        position_y = b_newgame.get_attr("pos_y") + b_newgame.height() + 20
        b_loadgame = data.forms.button.Button("b_loadgame", {
            "pos_y": position_y,
            "text": "Load Game",
            "callback_event": data.helpers.event.Event(
                data.eventcodes.LOADGAME,
                data.eventcodes.LOADGAME
            ),
            "colorkey": settings.COLOR_KEY,
            "spritesheet": "resources/images/sprites/buttons.png"
        })
        b_loadgame.set_attr({
            "pos_x": self.title_main.width() / 2 - b_loadgame.width() / 2
        })
        self.title_main.add(b_loadgame)
        position_y = b_loadgame.get_attr("pos_y") + b_loadgame.height() + 20
        b_quitgame = data.forms.button.Button("b_quitgame", {
            "pos_y": position_y,
            "text": "Quit Game",
            "callback_event": data.helpers.event.Event(
                data.eventcodes.QUITGAME,
                data.eventcodes.QUITGAME
            ),
            "colorkey": settings.COLOR_KEY,
            "spritesheet": "resources/images/sprites/buttons.png"
        })
        b_quitgame.set_attr({
            "pos_x": self.title_main.width() / 2 - b_quitgame.width() / 2
        })
        self.title_main.add(b_quitgame)
