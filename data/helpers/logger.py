""" This module provides logging by config file

:project: resa
:source: https://github.com/Kanasaru/resa
:license: GNU General Public License v3
"""

__version__ = '1.0'

import logging.config

logging.config.fileConfig('data/conf/logging.conf')
