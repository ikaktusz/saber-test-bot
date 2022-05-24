class OperandsException(Exception):
    """
    Custom exception, too many operands in string.
    """
    def __init__(self, message):
        super().__init__(message)


class LettersInStringException(Exception):
    """
    Custom exception, there were letters in the string.
    """
    def __init__(self, message):
        super().__init__(message)


class NumLengthException(Exception):
    """
    Custom exception, number too long.
    """
    def __init__(self, message):
        super().__init__(message)