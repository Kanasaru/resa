""" This module provides game settings and sprites as constants

:project: resa
:source: https://github.com/Kanasaru/resa
:license: GNU General Public License v3
"""

import configparser
from ast import literal_eval

Config = configparser.ConfigParser()
Config.read('data/conf/config.ini')
Sprites = configparser.ConfigParser()
Sprites.read('data/conf/sprites.ini')

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
GRID = literal_eval(Config.get('GameSettings', 'Grid'))
MAP_PACE = Config.getint('GameSettings', 'MapPace')

# Fonts
BASIC_FONT = Config.get('Fonts', 'Standard')

# Music
MUSIC_BG_1 = Config.get('Music', 'BackgroundMusic')
MUSIC_VOLUME = Config.getfloat('Music', 'StartVolume')

# SpriteSheets
SPRITES_MENU_BUTTONS_KEY = Sprites.get('Buttons', 'MenuButtonsKey')
SPRITES_MENU_BUTTONS = Sprites.get('Buttons', 'MenuButtons')
SPRITES_MENU_BUTTONS_SIZE = literal_eval(Sprites.get('Buttons', 'MenuButtonsSize'))
SPRITE_SHEETS_WORLD = {
    Sprites.get('Objects', 'FieldTilesSolidID'): (
        Sprites.get('Objects', 'FieldTilesSolid'),
        literal_eval(Sprites.get('Objects', 'FieldTilesSolidSize'))),
    Sprites.get('Objects', 'FieldTilesDirtAtoWaterID'): (
        Sprites.get('Objects', 'FieldTilesDirtAtoWater'),
        literal_eval(Sprites.get('Objects', 'FieldTilesDirtAtoWaterSize'))),
    Sprites.get('Objects', 'FieldTilesDirtBtoWaterID'): (
        Sprites.get('Objects', 'FieldTilesDirtBtoWater'),
        literal_eval(Sprites.get('Objects', 'FieldTilesDirtBtoWaterSize'))),
    Sprites.get('Objects', 'FieldTilesGrassAtoWaterID'): (
        Sprites.get('Objects', 'FieldTilesGrassAtoWater'),
        literal_eval(Sprites.get('Objects', 'FieldTilesGrassAtoWaterSize'))),
    Sprites.get('Objects', 'FieldTilesGrassBtoWaterID'): (
        Sprites.get('Objects', 'FieldTilesGrassBtoWater'),
        literal_eval(Sprites.get('Objects', 'FieldTilesGrassBtoWaterSize'))),
    Sprites.get('Objects', 'FieldTilesSandAtoWaterID'): (
        Sprites.get('Objects', 'FieldTilesSandAtoWater'),
        literal_eval(Sprites.get('Objects', 'FieldTilesSandAtoWaterSize'))),
    Sprites.get('Objects', 'FieldTilesDirtAtoDirtBID'): (
        Sprites.get('Objects', 'FieldTilesDirtAtoDirtB'),
        literal_eval(Sprites.get('Objects', 'FieldTilesDirtAtoDirtBSize'))),
    Sprites.get('Objects', 'FieldTilesDirtAtoSandAID'): (
        Sprites.get('Objects', 'FieldTilesDirtAtoSandA'),
        literal_eval(Sprites.get('Objects', 'FieldTilesDirtAtoSandASize'))),
    Sprites.get('Objects', 'FieldTilesDirtBtoSandAID'): (
        Sprites.get('Objects', 'FieldTilesDirtBtoSandA'),
        literal_eval(Sprites.get('Objects', 'FieldTilesDirtBtoSandASize'))),
    Sprites.get('Objects', 'FieldTilesGrassAtoDirtAID'): (
        Sprites.get('Objects', 'FieldTilesGrassAtoDirtA'),
        literal_eval(Sprites.get('Objects', 'FieldTilesGrassAtoDirtASize'))),
    Sprites.get('Objects', 'FieldTilesGrassAtoDirtBID'): (
        Sprites.get('Objects', 'FieldTilesGrassAtoDirtB'),
        literal_eval(Sprites.get('Objects', 'FieldTilesGrassAtoDirtBSize'))),
    Sprites.get('Objects', 'FieldTilesGrassAtoGrassBID'): (
        Sprites.get('Objects', 'FieldTilesGrassAtoGrassB'),
        literal_eval(Sprites.get('Objects', 'FieldTilesGrassAtoGrassBSize'))),
    Sprites.get('Objects', 'FieldTilesGrassAtoSandAID'): (
        Sprites.get('Objects', 'FieldTilesGrassAtoSandA'),
        literal_eval(Sprites.get('Objects', 'FieldTilesGrassAtoSandASize'))),
    Sprites.get('Objects', 'FieldTilesGrassBtoDirtAID'): (
        Sprites.get('Objects', 'FieldTilesGrassBtoDirtA'),
        literal_eval(Sprites.get('Objects', 'FieldTilesGrassBtoDirtASize'))),
    Sprites.get('Entities', 'EntityTreesBroadleafID'): (
        Sprites.get('Entities', 'EntityTreesBroadleaf'),
        literal_eval(Sprites.get('Entities', 'EntityTreesBroadleafSize'))),
    Sprites.get('Entities', 'EntityTreesEvergreenID'): (
        Sprites.get('Entities', 'EntityTreesEvergreen'),
        literal_eval(Sprites.get('Entities', 'EntityTreesEvergreenSize'))),
    Sprites.get('Entities', 'EntityTreesPalmsID'): (
        Sprites.get('Entities', 'EntityTreesPalms'),
        literal_eval(Sprites.get('Entities', 'EntityTreesPalmsSize')))
}
