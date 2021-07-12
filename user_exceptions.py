class UserError(Exception):
    def __init__(self, text):
        self.txt = text


class ArgumentsError(UserError):
    def __init__(self, text):
        self.txt = text
