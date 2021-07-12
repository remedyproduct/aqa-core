

class LocatorDynamicValueError(Exception):
    """Exception raised for errors in locator dynamic value.

    Attributes:
        locator_name -- locator name which caused the error
        message -- explanation of the error
    """

    def __init__(self, locator_name, message="You can't use %s locator, because it dynamic. Please add dynamic value."):
        self.locator_name = locator_name
        self.message = message % locator_name
        super().__init__(self.message)
