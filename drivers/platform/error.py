class PlatformError(Exception):
    """Exception raised for errors in platform not supported.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        super().__init__(message)
