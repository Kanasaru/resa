import pygame


class EventHandler(object):
    def __init__(self):
        """ pygame.USEREVENTs """
        self.TITLE_EVENT = pygame.USEREVENT + 1
        self.MUSIC_ENDED_EVENT = pygame.USEREVENT + 2
        self.AUTOSAVE_EVENT = pygame.USEREVENT + 3
        self.GAME_EVENT = pygame.USEREVENT + 4
        self.GAME_CLOCK = pygame.USEREVENT + 5
        # pygame.USEREVENT + 6
        # pygame.USEREVENT + 7
        # pygame.USEREVENT + 8
        # pygame.USEREVENT

        """ Resa TITLE EVENTs """
        # BUTTON & SWITCH EVENTS  | 1xxx
        self.BTN_STARTGAME = 1000
        self.BTN_QUITGAME = 1001
        self.BTN_LOADGAME = 1002
        self.BTN_LEAVEGAME = 1003
        self.BTN_SAVEGAME = 1004
        self.BTN_OPTIONS = 1005
        self.BTN_MAINMENU = 1006
        self.BTN_CHG_RESOLUTION = 1007
        self.BTN_EDITOR = 1008
        self.SWT_FULLSCREEN = 1009
        # MESSAGEBOX EVENTs | 2xxx
        self.QUITGAME_TRUE = 2002
        self.QUITGAME_FALSE = 2003

        """ Resa GAME EVENTs """
        # CONTROL EVENTs | 5xxx
        self.CTRL_MAP_MOVE = 5000
        self.BUILDMODE = 6000
        self.EDITOR_SELECT = 70000
        self.EDITOR_PLACE = 70001
        self.EDITOR_LEAVE = 70002
        self.EDITOR_LOAD = 70003
        self.EDITOR_SAVE = 70004

        self.BUILD_MENU = 6001
