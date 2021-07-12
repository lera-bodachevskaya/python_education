class UserError(Exception):
    def __init__(self, text):
        self.txt = text


class ArgumentsError(UserError):
    def __init__(self, text):
        self.txt = text


class FileError(UserError):
    def __init__(self, text):
        self.txt = text


class OpenError(FileError):
    def __init__(self, text):
        self.txt = text


class FormatError(FileError):
    def __init__(self, text):
        self.txt = text


class PermissionError(FileError):
    def __init__(self, text):
        self.txt = text


class PathError(FileError):
    def __init__(self, text):
        self.txt = text
