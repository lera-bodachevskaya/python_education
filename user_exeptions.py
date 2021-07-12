class UserError(Exception):
    def __init__(self, text):
        self.txt = text


class ArgumentsError(UserError):
    def __init__(self, text):
        self.txt = text


class ImageError(UserError):
    def __init__(self, text):
        self.txt = text


class ShowError(ImageError):
    def __init__(self, text):
        self.txt = text


class ImageFormatError(ImageError):
    def __init__(self, text):
        self.txt = text


class FileError(UserError):
    def __init__(self, text):
        self.txt = text


class SaveError(FileError):
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


class ConversionError(UserError):
    def __init__(self, text):
        self.txt = text


class HistogramError(ConversionError):
    def __init__(self, text):
        self.txt = text


class SegmentationError(ConversionError):
    def __init__(self, text):
        self.txt = text


class EqualizeError(ConversionError):
    def __init__(self, text):
        self.txt = text
