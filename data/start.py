import pygame
import data.eventcodes
from data import settings
from data.helpers import event
from data.game import Game
import data.forms


class Start(object):
    def __init__(self):
        pygame.init()

        self.surface = pygame.display.set_mode(settings.RESOLUTION)
        self.leave = False
        self.clock = pygame.time.Clock()
        self.events = data.helpers.event.EventList()
        self.game = None
        self.start_game = False

        pygame.display.set_caption(f"{settings.GAME_TITLE} in v{settings.GAME_VERSION} by {settings.GAME_AUTHOR}")

        self.load_music()
        self.pause = False

        self.title_main = None
        self.build_titles()

        self.loop()

    def loop(self):
        self.start_music(settings.MUSIC_VOLUME, settings.MUSIC_LOOP)
        while not self.leave:
            self.clock.tick(settings.FPS)
            self.handle_events()
            self.run_logic()
            self.render()

        self.exit()

    def handle_events(self):
        for event in self.title_main.get_events():
            if event.code == data.eventcodes.STARTGAME:
                self.start_game = True
            elif event.code == data.eventcodes.LOADGAME:
                print("Load Game!")
            elif event.code == data.eventcodes.QUITGAME:
                self.leave = True
            else:
                pass

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.leave = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_p:
                    self.pause_music()
            else:
                pass

            self.title_main.handle_event(event)

        self.title_main.clear_events()

    def run_logic(self):
        if self.start_game:
            if self.game is not None and self.game.exit_game:
                self.load_music()
                self.start_music(settings.MUSIC_VOLUME, settings.MUSIC_LOOP)
                self.start_game = False
                self.game = None
            else:
                self.clr_screen()
                self.stop_music()
                self.game = Game(self.surface)

        self.title_main.run_logic()

    def render(self):
        self.surface.fill(settings.COLOR_WHITE)

        self.title_main.render(self.surface)

        pygame.display.flip()

    def exit(self):
        pygame.quit()
        print("Bye bye!")

    def clr_screen(self):
        self.surface.fill(settings.COLOR_BLACK)
        pygame.display.flip()

    def load_music(self):
        pygame.mixer.music.load(settings.MUSIC_BG_1)

    def start_music(self, volume, loop):
        pygame.mixer.music.play(loop)
        pygame.mixer.music.set_volume(volume)

    def pause_music(self):
        if self.pause:
            pygame.mixer.music.unpause()
            self.pause = False
        else:
            pygame.mixer.music.pause()
            self.pause = True

    def stop_music(self):
        pygame.mixer.music.stop()

    def build_titles(self):
        self.title_main = data.forms.title.Title("main", {
            "width": settings.RESOLUTION[0],
            "height": settings.RESOLUTION[1],
            "colorkey": settings.COLOR_KEY,
            "bg_image": settings.MENU_BG_IMG,
        })
        tf_headline = data.forms.textbox.Textbox("tf_headline", {
            "pos_y": 20,
            "text": "RESA",
            "font_size": 90,
            "text_font": settings.BASIC_FONT,
            "font_color": settings.COLOR_BLACK,
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
            "alignment": data.forms.textbox.RIGHT,
        })
        self.title_main.add(tf_version)
        tf_credits = data.forms.textbox.Textbox("tf_credits", {
            "pos_x": self.title_main.width() / 2,
            "pos_y": self.title_main.height() - 24,
            "text": f"Created and Designed by {settings.GAME_AUTHOR}",
            "font_size": 14,
            "text_font": settings.BASIC_FONT,
            "font_color": settings.COLOR_BLACK,
            "alignment": data.forms.textbox.CENTER,
        })
        self.title_main.add(tf_credits)
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
            "spritesheet": "resources/images/sprites/buttons.png",
            "clickable": False,
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
