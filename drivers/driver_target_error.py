from drivers.platform.platforms import Platform


class DriverTargetError(Exception):
    """An exception is raised for the driver target when we don't know what the target is.

    Attributes:
        platform -- platform which caused the error
        message -- explanation of the error
    """

    def __init__(self, platform: Platform, message="Your %s platform has not '%s' attribute on file."):
        self.platform = platform
        self.message = message % (platform.value(), 'browserName' if Platform.WEB else 'platformName')
        super().__init__(self.message)
