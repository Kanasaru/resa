import pygame
import data.forms.title
import data.forms.button
import data.forms.textbox
import data.eventcodes
import data.helpers.event
from data import settings
import data.world.map


class Game(object):

    def __init__(self, surface):
        self.exit_game = False
        self.clock = pygame.time.Clock()
        self.surface = surface

        self.surface.fill(settings.COLOR_WHITE)
        self.panel = data.forms.title.Title("panel", {
            "width": settings.RESOLUTION[0],
            "height": 30,
            "bg_color": settings.COLOR_BLACK,
        })
        self.panel.add(data.forms.textbox.Textbox("tf_version", {
            "pos_x": 5,
            "pos_y": 5,
            "text": f"v{settings.GAME_VERSION}",
            "font_size": 14,
            "text_font": settings.BASIC_FONT,
            "font_color": settings.COLOR_WHITE,
        }))
        b_quit = data.forms.button.Button(
            "b_quit",
            pygame.Rect(self.panel.width() - 5, 3, 70, 24),
            settings.SPRITES_MENU_BUTTONS,
            (220, 60),
            "Quit",
            data.helpers.event.Event(data.eventcodes.STOPGAME, data.eventcodes.STOPGAME)
        )
        b_quit.align(data.forms.button.RIGHT)
        b_quit.set_font(settings.BASIC_FONT, 13)
        self.panel.add(b_quit)
        b_save = data.forms.button.Button(
            "b_save",
            pygame.Rect(self.panel.width() - 80, 3, 70, 24),
            settings.SPRITES_MENU_BUTTONS, (220, 60),
            "Save",
            data.helpers.event.Event(data.eventcodes.SAVEGAME, data.eventcodes.SAVEGAME)
        )
        b_save.align(data.forms.button.RIGHT)
        b_save.set_font(settings.BASIC_FONT, 13)
        self.panel.add(b_save)
        self.panel.add(data.forms.textbox.Textbox("tf_resources", {
            "pos_x": self.panel.width() / 2,
            "pos_y": 5,
            "text": f"Wood: 0 | Stone: 0 | Marble: 0 | Tools: 0 | Gold: 0",
            "font_size": 14,
            "text_font": settings.BASIC_FONT,
            "font_color": settings.COLOR_WHITE,
            "alignment": data.forms.textbox.CENTER,
        }))

        self.load_msg()

        self.map = data.world.map.Loader(
            (settings.RESOLUTION[0] - 2, settings.RESOLUTION[1] - self.panel.height() - 2),
            (40, 20)
        )

        self.loop()

    def loop(self):
        while not self.exit_game:
            self.clock.tick(settings.FPS)
            self.handle_events()
            self.run_logic()
            self.render()

    def handle_events(self):
        for event in self.panel.get_events():
            if event.code == data.eventcodes.STOPGAME:
                self.exit_game = True
            elif event.code == data.eventcodes.SAVEGAME:
                print("Save Game!")
            else:
                pass

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit_game = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    z = pygame.mouse.get_pos()
                if event.button == 2:
                    pass
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_F3:
                    pass
            else:
                pass
            self.panel.handle_event(event)
            self.map.handle_event(event)

        self.panel.clear_events()

    def run_logic(self):
        self.panel.run_logic()
        self.update_panel()
        self.map.run_logic()

    def render(self):
        self.surface.fill(settings.COLOR_WHITE)
        self.map.render()
        pygame.Surface.blit(self.surface, self.map.get_surface(), (1, self.panel.height() + 1))
        self.panel.render(self.surface)
        pygame.display.flip()

    def update_panel(self):
        pass

    def load_msg(self):
        load_screen = data.forms.title.Title("load_screen", {
            "width": settings.RESOLUTION[0],
            "height": settings.RESOLUTION[1],
            "bg_color": settings.COLOR_BLACK,
        })
        load_screen.add(data.forms.textbox.Textbox("tf_load_screen", {
            "pos_x": settings.RESOLUTION[0] / 2,
            "pos_y": settings.RESOLUTION[1] / 2,
            "text": f"Loading world...",
            "font_size": 20,
            "text_font": settings.BASIC_FONT,
            "font_color": settings.COLOR_WHITE,
            "alignment": data.forms.textbox.CENTER,
        }))
        load_screen.render(self.surface)
        pygame.display.flip()
