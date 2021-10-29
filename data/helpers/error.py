class Error(object):
    def __init__(self, code, data):
        self.code = code
        self.data = data

    def get_name(self):
        return self.data

    def get_code(self):
        return self.code

    def __str__(self):
        return "ERROR [" + str(self.code) + "] " + str(self.data)


class ErrorList(object):
    def __init__(self):
        self.errors = []

    def add(self, error):
        self.errors.append(error)

    def remove(self):
        pass

    def get_errors(self):
        return self.errors

    def get_error_by_key(self, key):
        for error in self.errors:
            if error.code == key:
                return error
        return "Unknown Error"
