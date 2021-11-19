""" This module provides basic error handling classes

:project: resa
:source: https://github.com/Kanasaru/resa
:license: GNU General Public License v3
"""

__version__ = '1.0'


class Error(object):
    def __init__(self, code: int, data: any) -> None:
        """ Initializes a specific error

        :param code: integer of the error
        :param data: any kind of error information
        """
        self.code = code
        self.data = data

    def get_name(self) -> any:
        """ Returns the data of an error

        :return: data parameter
        """
        return self.data

    def get_code(self) -> int:
        """ Returns the code of an error

        :return: integer of the error
        """
        return self.code

    def __str__(self) -> str:
        """ Defines how an error is printed

        :return: error string created by its parameters
        """
        return f"ERROR [{str(self.code)}] {str(self.data)}"


class ErrorList(object):
    def __init__(self) -> None:
        """ Initializes an empty error list """
        self.errors = []

    def add(self, error: Error) -> None:
        """ Adds an error to the error list

        :param error: error object that should be added to the error list
        :return: None
        """
        self.errors.append(error)

    def get_errors(self) -> list:
        """ Returns the error list

        :return: list of all errors in error list
        """
        return self.errors

    def get_error_by_key(self, key: int) -> Error | bool:
        """ Returns error object from list which matches given key

        :param key: error code to search for in error list
        :return: error object if error is found in list or false if not
        """
        for error in self.errors:
            if error.code == key:
                return error
        return False
