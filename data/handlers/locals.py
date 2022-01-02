""" This module provides locals handling

:project: resa
:source: https://github.com/Kanasaru/resa
:license: CC-BY-SA-4.0
"""
import logging
from data.settings import conf
from data.locales.en import lang_en
from data.locales.de import lang_de


class LocalsHandler(object):
    def __init__(self):
        pass

    @staticmethod
    def init():
        conf.lang = lang_en

    @staticmethod
    def set_lang(code: str):
        if code == 'de':
            conf.lang = lang_de
        elif code == 'en':
            conf.lang = lang_en
        else:
            logging.warning('Given locals code not defined. No changes done.')

    @staticmethod
    def lang(key: str):
        if key in conf.lang:
            return conf.lang[key]
        else:
            return f'[{key}]'
