""" This module provides locals handling

:project: resa
:source: https://github.com/Kanasaru/resa
:license: CC-BY-SA-4.0
"""
import logging
from data.locales.en import lang_en
from data.locales.de import lang_de

STD_LANG = lang_en


def set_lang(code: str):
    global STD_LANG
    if code == 'de':
        STD_LANG = lang_de
    elif code == 'en':
        STD_LANG = lang_en
    else:
        logging.warning('Given locales code not defined. No changes done.')


def get(key: str):
    if key in STD_LANG:
        return STD_LANG[key]
    else:
        return f'[{key}]'
