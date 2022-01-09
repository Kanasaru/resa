""" This module provides display functions

:project: resa
:source: https://github.com/Kanasaru/resa
:license: CC-BY-SA-4.0
"""
import pygame


def get_screenmodes():
    """ Returns a dictionary of 'full' and 'win' screen sizes

    :return: dictionary['full' and 'win'][list of screen sizes]
    """
    screenmodes = {
        'full': list(),
        'win': list(),
    }
    desktop_sizes = pygame.display.get_desktop_sizes()
    desktop_w = desktop_sizes[0][0]
    desktop_h = desktop_sizes[0][1]

    for reso in pygame.display.list_modes():
        if reso[0] < 800 or reso[0] > 1280 or reso[1] < 600:
            pass
        else:
            insert = True
            for value in screenmodes['full']:
                w, h = value
                if reso[0] == w:
                    insert = False
            if insert:
                screenmodes['full'].append(reso)

    if desktop_w > 1280 and desktop_h > 960:
        screenmodes['win'].append((1280, 960))
    if desktop_w > 1000 and desktop_h > 600:
        screenmodes['win'].append((1000, 720))
    if desktop_w > 800 and desktop_h > 600:
        screenmodes['win'].append((800, 600))

    return screenmodes
