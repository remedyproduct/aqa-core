

class PlatformNotSupportedError(Exception):
    """Exception raised for errors in platform not supported.

    Attributes:
        platform -- platform which caused the error
        message -- explanation of the error
    """

    def __init__(self, platform, message="Your %s platform is not supported."):
        self.platform = platform
        self.message = message % platform
        super().__init__(self.message)
