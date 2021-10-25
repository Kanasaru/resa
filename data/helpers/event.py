class Event(object):
    def __init__(self, code, data):
        self.code = code
        self.data = data

    def get_name(self):
        return self.data

    def get_code(self):
        return self.code

    def __str__(self):
        return "EVENT [" + str(self.code) + "] " + str(self.data)


class EventList(object):
    def __init__(self):
        self.events = []

    def add(self, event):
        self.events.append(event)

    def remove(self):
        pass

    def get_events(self):
        return self.events
