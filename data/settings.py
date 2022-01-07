""" This module provides general game settings

:project: resa
:source: https://github.com/Kanasaru/resa
:license: CC-BY-SA-4.0
"""

import configparser
from ast import literal_eval


class Settings(object):
    def __init__(self) -> None:
        """ Provides standard game settings and consts """
        self.parser = configparser.ConfigParser()

        # information
        self.title = 'Resa'
        self.version = '0.5.2-alpha'
        self.author = 'Kanasaru'
        self.www = 'bitbyteopen.org'

        # display settings
        self.icon = 'resources/images/icon.png'
        self.fps = 60
        self.resolution = None
        self.fullscreen = False
        self.grid_zoom = 20
        self.background_image = None
        self.map_border_thickness = 5

        # standard game values
        self.game_speed = 1440
        self.map_pace = 10
        self.save_file = 'saves/game.xml'
        self.std_font = None
        self.std_font_size = 20
        self.msg_font_size = 16
        self.volume = .2
        self.bg_music = None
        self.sounds = 'resources/sounds'
        self.screenshot_path = 'saves/'
        self.autosave = False
        self.autosave_interval = 240000

        # sprite sheets
        self.sp_menu_btn_key = None
        self.sp_menu_btn = None
        self.sp_menu_btn_size = None
        self.sp_menu_swt_key = None
        self.sp_menu_swt = None
        self.sp_menu_swt_size = None
        self.sp_world = None

        # tree spawn rate
        self.tree_spawn_bl = 70
        self.tree_spawn_eg = 90
        self.tree_spawn_p = 50

        # islands temperatures
        self.temp_north = -20
        self.temp_center = 20
        self.temp_south = 40

        # standard colors
        self.COLOR_KEY = (1, 0, 0)
        self.COLOR_BLACK = (0, 0, 0)
        self.COLOR_WHITE = (255, 255, 255)
        self.COLOR_RED = (255, 0, 0)
        self.COLOR_BLUE = (0, 0, 255)
        self.COLOR_YELLOW = (255, 255, 0)
        self.COLOR_CYAN = (0, 255, 255)
        self.COLOR_GRAY = (128, 128, 128)
        self.COLOR_GREEN = (0, 128, 0)

    def load_config_file(self, filepath: str) -> None:
        """ Loads settings from file and replaces standard value

        :param filepath: config filepath
        :return: None
        """
        self.parser.read(filepath)

        self.background_image = self.parser.get('Screen', 'BackgroundImage')
        self.save_file = self.parser.get('GameSettings', 'SaveFile')
        self.bg_music = self.parser.get('Music', 'BackgroundMusic')
        self.volume = self.parser.getfloat('Music', 'StartVolume')

    def load_sprite_file(self, filepath: str) -> None:
        """ Loads sprite sheets from config file

        :param filepath: sprite sheet config filepath
        :return: None
        """
        self.parser.read(filepath)

        self.sp_menu_btn_key = self.parser.get('Buttons', 'MenuButtonsKey')
        self.sp_menu_btn = self.parser.get('Buttons', 'MenuButtons')
        self.sp_menu_btn_size = literal_eval(self.parser.get('Buttons', 'MenuButtonsSize'))
        self.sp_menu_swt_key = self.parser.get('Switches', 'MenuSwitchesKey')
        self.sp_menu_swt = self.parser.get('Switches', 'MenuSwitches')
        self.sp_menu_swt_size = literal_eval(self.parser.get('Switches', 'MenuSwitchesSize'))
        self.sp_world = {
            self.parser.get('Objects', 'TilesID'): (
                self.parser.get('Objects', 'TilesSheet'),
                literal_eval(self.parser.get('Objects', 'TilesSize'))),
            self.parser.get('Entities', 'TreesID'): (
                self.parser.get('Entities', 'TreesSheet'),
                literal_eval(self.parser.get('Entities', 'TreesSize')))
        }


# global config object
conf = Settings()
conf.load_config_file('data/conf/config.ini')
conf.load_sprite_file('data/conf/sprites.ini')
