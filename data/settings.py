""" This module provides game settings and sprites as constants

:project: resa
:source: https://github.com/Kanasaru/resa
:license: GNU General Public License v3
"""

import configparser
from ast import literal_eval


class Settings(object):
    def __init__(self):
        self.parser = configparser.ConfigParser()

        self.title = 'Resa'
        self.version = '0.4.1-alpha'
        self.author = 'Kanasaru'
        self.www = 'bitbyteopen.org'
        self.fps = 60
        self.resolution = (1000, 600)
        self.grid_size = (40, 20)
        self.background_image = None
        self.game_speed = 1440
        self.map_pace = 10
        self.save_file = 'saves/game.xml'
        self.std_font = None
        self.volume = .2
        self.bg_music = None

        self.sp_menu_btn_key = None
        self.sp_menu_btn = None
        self.sp_menu_btn_size = None
        self.sp_world = None

        self.COLOR_KEY = (1, 0, 0)
        self.COLOR_BLACK = (0, 0, 0)
        self.COLOR_WHITE = (255, 255, 255)
        self.COLOR_RED = (255, 0, 0)
        self.COLOR_BLUE = (0, 0, 255)
        self.COLOR_YELLOW = (255, 255, 0)
        self.COLOR_CYAN = (0, 255, 255)
        self.COLOR_GRAY = (128, 128, 128)
        self.COLOR_GREEN = (0, 128, 0)

    def load_config_file(self, filepath):
        self.parser.read(filepath)

        self.resolution = literal_eval(self.parser.get('Screen', 'Resolution'))
        self.background_image = self.parser.get('Screen', 'BackgroundImage')
        self.save_file = self.parser.get('GameSettings', 'SaveFile')
        self.std_font = self.parser.get('Fonts', 'Standard')
        self.bg_music = self.parser.get('Music', 'BackgroundMusic')
        self.volume = self.parser.getfloat('Music', 'StartVolume')

    def load_sprite_file(self, filepath):
        self.parser.read(filepath)

        self.sp_menu_btn_key = self.parser.get('Buttons', 'MenuButtonsKey')
        self.sp_menu_btn = self.parser.get('Buttons', 'MenuButtons')
        self.sp_menu_btn_size = literal_eval(self.parser.get('Buttons', 'MenuButtonsSize'))
        self.sp_world = {
            self.parser.get('Objects', 'FieldTilesSolidID'): (
                self.parser.get('Objects', 'FieldTilesSolid'),
                literal_eval(self.parser.get('Objects', 'FieldTilesSolidSize'))),
            self.parser.get('Objects', 'FieldTilesDirtAtoWaterID'): (
                self.parser.get('Objects', 'FieldTilesDirtAtoWater'),
                literal_eval(self.parser.get('Objects', 'FieldTilesDirtAtoWaterSize'))),
            self.parser.get('Objects', 'FieldTilesDirtBtoWaterID'): (
                self.parser.get('Objects', 'FieldTilesDirtBtoWater'),
                literal_eval(self.parser.get('Objects', 'FieldTilesDirtBtoWaterSize'))),
            self.parser.get('Objects', 'FieldTilesGrassAtoWaterID'): (
                self.parser.get('Objects', 'FieldTilesGrassAtoWater'),
                literal_eval(self.parser.get('Objects', 'FieldTilesGrassAtoWaterSize'))),
            self.parser.get('Objects', 'FieldTilesGrassBtoWaterID'): (
                self.parser.get('Objects', 'FieldTilesGrassBtoWater'),
                literal_eval(self.parser.get('Objects', 'FieldTilesGrassBtoWaterSize'))),
            self.parser.get('Objects', 'FieldTilesSandAtoWaterID'): (
                self.parser.get('Objects', 'FieldTilesSandAtoWater'),
                literal_eval(self.parser.get('Objects', 'FieldTilesSandAtoWaterSize'))),
            self.parser.get('Objects', 'FieldTilesDirtAtoDirtBID'): (
                self.parser.get('Objects', 'FieldTilesDirtAtoDirtB'),
                literal_eval(self.parser.get('Objects', 'FieldTilesDirtAtoDirtBSize'))),
            self.parser.get('Objects', 'FieldTilesDirtAtoSandAID'): (
                self.parser.get('Objects', 'FieldTilesDirtAtoSandA'),
                literal_eval(self.parser.get('Objects', 'FieldTilesDirtAtoSandASize'))),
            self.parser.get('Objects', 'FieldTilesDirtBtoSandAID'): (
                self.parser.get('Objects', 'FieldTilesDirtBtoSandA'),
                literal_eval(self.parser.get('Objects', 'FieldTilesDirtBtoSandASize'))),
            self.parser.get('Objects', 'FieldTilesGrassAtoDirtAID'): (
                self.parser.get('Objects', 'FieldTilesGrassAtoDirtA'),
                literal_eval(self.parser.get('Objects', 'FieldTilesGrassAtoDirtASize'))),
            self.parser.get('Objects', 'FieldTilesGrassAtoDirtBID'): (
                self.parser.get('Objects', 'FieldTilesGrassAtoDirtB'),
                literal_eval(self.parser.get('Objects', 'FieldTilesGrassAtoDirtBSize'))),
            self.parser.get('Objects', 'FieldTilesGrassAtoGrassBID'): (
                self.parser.get('Objects', 'FieldTilesGrassAtoGrassB'),
                literal_eval(self.parser.get('Objects', 'FieldTilesGrassAtoGrassBSize'))),
            self.parser.get('Objects', 'FieldTilesGrassAtoSandAID'): (
                self.parser.get('Objects', 'FieldTilesGrassAtoSandA'),
                literal_eval(self.parser.get('Objects', 'FieldTilesGrassAtoSandASize'))),
            self.parser.get('Objects', 'FieldTilesGrassBtoDirtAID'): (
                self.parser.get('Objects', 'FieldTilesGrassBtoDirtA'),
                literal_eval(self.parser.get('Objects', 'FieldTilesGrassBtoDirtASize'))),
            self.parser.get('Entities', 'EntityTreesBroadleafID'): (
                self.parser.get('Entities', 'EntityTreesBroadleaf'),
                literal_eval(self.parser.get('Entities', 'EntityTreesBroadleafSize'))),
            self.parser.get('Entities', 'EntityTreesEvergreenID'): (
                self.parser.get('Entities', 'EntityTreesEvergreen'),
                literal_eval(self.parser.get('Entities', 'EntityTreesEvergreenSize'))),
            self.parser.get('Entities', 'EntityTreesPalmsID'): (
                self.parser.get('Entities', 'EntityTreesPalms'),
                literal_eval(self.parser.get('Entities', 'EntityTreesPalmsSize')))
        }


conf = Settings()
conf.load_config_file('data/conf/config.ini')
conf.load_sprite_file('data/conf/sprites.ini')
