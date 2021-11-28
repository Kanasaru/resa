""" This module provides some time functions

:project: resa
:source: https://github.com/Kanasaru/resa
:license: GNU General Public License v3
"""

__version__ = '1.0'


def seconds_to_clock(seconds: int):
    """ Transforms seconds into time string

    :param seconds: seconds to transform
    :returns: clock format like '00:00:00'
    """
    seconds = abs(seconds)
    hours = seconds // 3600
    minutes = (seconds - (hours * 3600)) // 60
    seconds -= (seconds - (hours * 3600)) - (seconds - (minutes * 60))

    if hours < 10:
        hours = "0" + str(hours)
    else:
        hours = str(hours)
    if minutes < 10:
        minutes = "0" + str(minutes)
    else:
        minutes = str(minutes)
    if seconds < 10:
        seconds = "0" + str(seconds)
    else:
        seconds = str(seconds)

    return f'{hours}:{minutes}:{seconds}'
