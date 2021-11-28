""" This module provides game settings as constants

:project: resa
:source: https://github.com/Kanasaru/resa
:license: GNU General Public License v3
"""

import configparser
from ast import literal_eval

Config = configparser.ConfigParser()
Config.read('data/conf/config.ini')

# GameInformation
GAME_TITLE = Config.get('GameInformation', 'Title')
GAME_VERSION = Config.get('GameInformation', 'Version')
GAME_AUTHOR = Config.get('GameInformation', 'Author')
GAME_WWW = Config.get('GameInformation', 'www')

# Screen
RESOLUTION = literal_eval(Config.get('Screen', 'Resolution'))
FPS = Config.getint('Screen', 'FPS')
MENU_BG_IMG = Config.get('Screen', 'BackgroundImage')

# GameSettings
SAVE_FILE = Config.get('GameSettings', 'SaveFile')
INGAME_SPEED = Config.getint('GameSettings', 'InGameSpeed')
WORLD_SIZE = literal_eval(Config.get('GameSettings', 'WorldSize'))
GRID = literal_eval(Config.get('GameSettings', 'Grid'))
MAP_PACE = Config.getint('GameSettings', 'MapPace')

# Fonts
BASIC_FONT = Config.get('Fonts', 'Standard')

# SpriteSheets
SPRITES_MENU_BUTTONS = Config.get('SpriteSheets', 'MenuButtons')

# Music
MUSIC_BG_1 = Config.get('Music', 'BackgroundMusic')
MUSIC_VOLUME = Config.getfloat('Music', 'StartVolume')
