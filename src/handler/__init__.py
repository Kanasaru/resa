from src.handler.event import EventHandler
from src.handler.spritesheet import SpriteSheetHandler, SpriteSheet
from src.handler.sound import SoundHandler
from src.handler.music import MusicHandler
from src.handler.gamedata import GameDataHandler, Settings
from src.handler.gamestate import GameStateHandler
from src.handler.debug import DebugHandler

""" EventHandler """
RESA_EH = EventHandler()

""" ConfigurationHandler """
RESA_CH = Settings()
RESA_CH.load_config_file('data/conf/config.ini')
RESA_CH.load_sprite_file('data/conf/sprites.ini')

STD_COLOR_KEY = (1, 0, 0)
PATH_SOUNDS = RESA_CH.sounds
PATH_MUSIC = RESA_CH.bg_music

""" SpriteSheetHandler """
RESA_SSH = SpriteSheetHandler()
for key, value in RESA_CH.sp_general.items():
    sheet = SpriteSheet(key, value[0], value[1])
    sheet.colorkey = None
    RESA_SSH.add(sheet)
for key, value in RESA_CH.sp_forms.items():
    sheet = SpriteSheet(key, value[0], value[1])
    sheet.colorkey = STD_COLOR_KEY
    RESA_SSH.add(sheet)
for key, value in RESA_CH.sp_world.items():
    sheet = SpriteSheet(key, value[0], value[1])
    sheet.colorkey = None
    RESA_SSH.add(sheet)
for key, value in RESA_CH.sp_houses.items():
    sheet = SpriteSheet(key, value[0], value[1])
    sheet.colorkey = None
    RESA_SSH.add(sheet)

""" GameDataHandler """
RESA_GDH = GameDataHandler()
RESA_GDH.game_time_speed = RESA_CH.game_speed

""" GameStateHandler """
RESA_GSH = GameStateHandler()

""" SoundHandler """
RESA_SH = SoundHandler(PATH_SOUNDS)

""" MusicHandler """
RESA_MH = MusicHandler(PATH_MUSIC)
RESA_MH.set_endevent(RESA_EH.RESA_MUSIC_ENDED_EVENT)
RESA_MH.load()

""" DebugHandler """
RESA_DH = DebugHandler()
