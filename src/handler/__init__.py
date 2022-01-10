import pygame
from src.handler.spritesheet import SpriteSheetHandler, SpriteSheet
from src.handler.sound import SoundHandler
from src.handler.music import MusicHandler
from src.handler.gamedata import GameDataHandler, Settings
from src.handler.debug import DebugHandler

""" pygame.USEREVENTs """
RESA_TITLE_EVENT = pygame.USEREVENT + 1
RESA_MUSIC_ENDED_EVENT = pygame.USEREVENT + 2
RESA_AUTOSAVE_EVENT = pygame.USEREVENT + 3
RESA_GAME_EVENT = pygame.USEREVENT + 4
# pygame.USEREVENT + 5
# pygame.USEREVENT + 6
# pygame.USEREVENT + 7
# pygame.USEREVENT + 8
# pygame.USEREVENT

""" Resa TITLE EVENTs """
# BUTTON & SWITCH EVENTS  | 1xxx
RESA_BTN_STARTGAME = 1000
RESA_BTN_QUITGAME = 1001
RESA_BTN_LOADGAME = 1002
RESA_BTN_LEAVEGAME = 1003
RESA_BTN_SAVEGAME = 1004
RESA_BTN_OPTIONS = 1005
RESA_BTN_MAINMENU = 1006
RESA_BTN_CHG_RESOLUTION = 1007
RESA_BTN_EDITOR = 1008
RESA_SWT_FULLSCREEN = 1009
# MESSAGEBOX EVENTs | 2xxx
RESA_QUITGAME_TRUE = 2002
RESA_QUITGAME_FALSE = 2003

""" Resa GAME EVENTs """
# CONTROL EVENTs | 5xxx
RESA_CTRL_MAP_MOVE = 5000
RESA_BUILDMODE = 6000
RESA_EDITOR_SELECT = 70000
RESA_EDITOR_PLACE = 70001
RESA_EDITOR_LEAVE = 70002
RESA_EDITOR_LOAD = 70003
RESA_EDITOR_SAVE = 70004

conf = Settings()
conf.load_config_file('data/conf/config.ini')
conf.load_sprite_file('data/conf/sprites.ini')

STD_COLOR_KEY = (1, 0, 0)
PATH_SOUNDS = conf.sounds
PATH_MUSIC = conf.bg_music

hdl_sh_titles = SpriteSheetHandler()
hdl_sh_titles.add(SpriteSheet(conf.sp_menu_btn_key, conf.sp_menu_btn, conf.sp_menu_btn_size, STD_COLOR_KEY))
hdl_sh_titles.add(SpriteSheet(conf.sp_menu_swt_key, conf.sp_menu_swt, conf.sp_menu_swt_size, STD_COLOR_KEY))

hdl_sh_world = SpriteSheetHandler()
for key, value in conf.sp_world.items():
    sheet = SpriteSheet(key, value[0], value[1])
    sheet.colorkey = None
    hdl_sh_world.add(sheet)

hdl_sound = SoundHandler(PATH_SOUNDS)

hdl_music = MusicHandler(PATH_MUSIC)
hdl_music.set_endevent(RESA_MUSIC_ENDED_EVENT)
hdl_music.load()

hdl_debug = DebugHandler()

hdl_gamedata = GameDataHandler()
hdl_gamedata.game_time_speed = conf.game_speed
