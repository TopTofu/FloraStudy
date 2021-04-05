class CSVParsingError(Exception):
    def __init__(self, arg):
        self.strerror = arg
