""" This module provides basic event handling classes

:project: resa
:source: https://github.com/Kanasaru/resa
:license: GNU General Public License v3
"""

__version__ = '1.0'


class Event(object):
    def __init__(self, code, data) -> None:
        """ Initializes a specific event

        :param code: integer of the event
        :param data: any kind of event information
        """
        self.code = code
        self.data = data

    def get_name(self) -> any:
        """ Returns the data of an event

        :return: data parameter
        """
        return self.data

    def get_code(self) -> int:
        """ Returns the code of an event

        :return: integer of the event
        """
        return self.code

    def __str__(self) -> str:
        """ Defines how an event is printed

        :return: event string created by its parameters
        """
        return "EVENT [" + str(self.code) + "] " + str(self.data)


class EventList(object):
    def __init__(self) -> None:
        """ Initializes an empty event list """
        self.events = []

    def add(self, event: Event) -> None:
        """ Adds an event to the event list

        :param event: event object that should be added to the event list
        :return: None
        """
        self.events.append(event)

    def get_events(self) -> list:
        """ Returns the event list

        :return: list of all events in event list
        """
        return self.events
