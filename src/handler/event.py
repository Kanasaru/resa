import pygame


class EventHandler(object):
    def __init__(self):
        """ pygame.USEREVENTs """
        self.RESA_TITLE_EVENT = pygame.USEREVENT + 1
        self.RESA_MUSIC_ENDED_EVENT = pygame.USEREVENT + 2
        self.RESA_AUTOSAVE_EVENT = pygame.USEREVENT + 3
        self.RESA_GAME_EVENT = pygame.USEREVENT + 4
        self.RESA_GAME_CLOCK = pygame.USEREVENT + 5
        # pygame.USEREVENT + 6
        # pygame.USEREVENT + 7
        # pygame.USEREVENT + 8
        # pygame.USEREVENT

        """ Resa TITLE EVENTs """
        # BUTTON & SWITCH EVENTS  | 1xxx
        self.RESA_BTN_STARTGAME = 1000
        self.RESA_BTN_QUITGAME = 1001
        self.RESA_BTN_LOADGAME = 1002
        self.RESA_BTN_LEAVEGAME = 1003
        self.RESA_BTN_SAVEGAME = 1004
        self.RESA_BTN_OPTIONS = 1005
        self.RESA_BTN_MAINMENU = 1006
        self.RESA_BTN_CHG_RESOLUTION = 1007
        self.RESA_BTN_EDITOR = 1008
        self.RESA_SWT_FULLSCREEN = 1009
        # MESSAGEBOX EVENTs | 2xxx
        self.RESA_QUITGAME_TRUE = 2002
        self.RESA_QUITGAME_FALSE = 2003

        """ Resa GAME EVENTs """
        # CONTROL EVENTs | 5xxx
        self.RESA_CTRL_MAP_MOVE = 5000
        self.RESA_BUILDMODE = 6000
        self.RESA_EDITOR_SELECT = 70000
        self.RESA_EDITOR_PLACE = 70001
        self.RESA_EDITOR_LEAVE = 70002
        self.RESA_EDITOR_LOAD = 70003
        self.RESA_EDITOR_SAVE = 70004

        self.RESA_BUILD_MENU = 6001
