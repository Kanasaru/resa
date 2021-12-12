""" This module provides game event codes

:project: resa
:source: https://github.com/Kanasaru/resa
:license: GNU General Public License v3
"""
import pygame

""" pygame.USEREVENTs """
RESA_TITLE_EVENT = pygame.USEREVENT + 1
RESA_MUSIC_ENDED_EVENT = pygame.USEREVENT + 2
# pygame.USEREVENT + 3
# pygame.USEREVENT + 4
# pygame.USEREVENT + 5
# pygame.USEREVENT + 6
# pygame.USEREVENT + 7
# pygame.USEREVENT + 8
# pygame.USEREVENT

""" Resa title events | 1xxx """
RESA_STARTGAME = 1000
RESA_QUITGAME = 1001
RESA_LOADGAME = 1002
RESA_STOPGAME = 1003
RESA_SAVEGAME = 1004
RESA_OPTIONS = 1005
RESA_MAINMENU = 1006
RESA_CHG_RESOLUTION = 1007
