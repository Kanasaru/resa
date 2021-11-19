""" This module provides game error codes

:project: resa
:source: https://github.com/Kanasaru/resa
:license: GNU General Public License v3
"""

from data.helpers.error import Error, ErrorList

resa_error_list = ErrorList()

E_KEY = 10001
resa_error_list.add(Error(E_KEY, "Given key does not exist"))
E_KEYTYPE = 10002
resa_error_list.add(Error(E_KEYTYPE, "Wrong type of given key"))
E_FORMAT = 10003
resa_error_list.add(Error(E_FORMAT, "Wrong format of given attributes"))
E_FILE = 10004
resa_error_list.add(Error(E_FILE, "Given file not found or does not exists"))
