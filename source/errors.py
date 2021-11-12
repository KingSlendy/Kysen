class RuntimeException(Exception):
    pass


class Error:
    def __init__(self, message):
        self.message = message


    def __repr__(self):
        return f"{type(self).__name__}: {self.message}"


class IllegalCharError(Error):
    def __init__(self, char):
        self.message = f"illegal character '{char}'."


class SyntaxError(Error):
    pass