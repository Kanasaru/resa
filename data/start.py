import pygame
import data.eventcodes
from data import settings
from data.helpers import event
from data.game import Game
from data.forms import textbox, button, title


class Start(object):
    def __init__(self):
        pygame.init()

        self.start_game = False
        self.leave_game = False
        self.pause = False

        self.game = None
        self.title_main = None
        self.clock = pygame.time.Clock()
        self.surface = pygame.display.set_mode(settings.RESOLUTION)

        pygame.display.set_caption(f"{settings.GAME_TITLE}")

        self.load_music()
        self.build_titles()
        self.loop()

    def loop(self):
        self.start_music(settings.MUSIC_VOLUME, settings.MUSIC_LOOP)
        while not self.leave_game:
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
                self.leave_game = True
            else:
                pass

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.leave_game = True
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
        self.title_main = data.forms.title.Title(
            "main",
            pygame.Rect(0, 0, settings.RESOLUTION[0], settings.RESOLUTION[1]),
            settings.COLOR_BLACK,
            settings.MENU_BG_IMG
        )
        tf_headline = data.forms.textbox.Textbox(
            "tf_headline",
            (self.title_main.width() / 2, 20),
            "RESA",
            90
        )
        tf_headline.align(tf_headline.CENTER)
        tf_version = data.forms.textbox.Textbox(
            "tf_version",
            (self.title_main.width() - 5, 5),
            f"Version: {settings.GAME_VERSION}",
            14
        )
        tf_version.align(tf_version.RIGHT)
        tf_credits = data.forms.textbox.Textbox(
            "tf_credits",
            (self.title_main.width() / 2, self.title_main.height() - 24),
            f"Created and Designed by {settings.GAME_AUTHOR} | {settings.GAME_WWW}",
            14
        )
        tf_credits.align(tf_credits.CENTER)
        width, height = tf_headline.get_dimensions()
        position_y = height + 100
        b_newgame = data.forms.button.Button(
            "b_newgame",
            pygame.Rect(self.title_main.width() / 2, position_y, 220, 60),
            settings.SPRITES_MENU_BUTTONS,
            (220, 60),
            "New Game",
            data.helpers.event.Event(data.eventcodes.STARTGAME, data.eventcodes.STARTGAME)
        )
        b_newgame.align(b_newgame.CENTER)
        b_newgame.set_spritesheet(settings.SPRITES_MENU_BUTTONS, (220, 60))
        position_y += b_newgame.height() + 20
        b_loadgame = data.forms.button.Button(
            "b_loadgame",
            pygame.Rect(self.title_main.width() / 2, position_y, 220, 60),
            settings.SPRITES_MENU_BUTTONS,
            (220, 60),
            "Load Game",
            data.helpers.event.Event(data.eventcodes.LOADGAME, data.eventcodes.LOADGAME)
        )
        b_loadgame.align(b_loadgame.CENTER)
        b_loadgame.disable()
        b_loadgame.set_spritesheet(settings.SPRITES_MENU_BUTTONS, (220, 60))
        position_y += b_loadgame.height() + 20
        b_quitgame = data.forms.button.Button(
            "b_quitgame",
            pygame.Rect(self.title_main.width() / 2, position_y, 220, 60),
            settings.SPRITES_MENU_BUTTONS, (220, 60),
            "Quit Game",
            data.helpers.event.Event(data.eventcodes.QUITGAME, data.eventcodes.QUITGAME)
        )
        b_quitgame.align(b_quitgame.CENTER)

        self.title_main.add(tf_headline)
        self.title_main.add(tf_version)
        self.title_main.add(tf_credits)
        self.title_main.add(b_newgame)
        self.title_main.add(b_loadgame)
        self.title_main.add(b_quitgame)
