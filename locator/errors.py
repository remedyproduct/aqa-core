

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


class LocatorError(Exception):
    """Exception raised for errors in locator type or value.

    Attributes:
        name -- locator name
        value -- By or Value name which caused the error
        message -- explanation of the error
    """

    def __init__(self, name, value, message="You can't use the locator %s, because this %s is empty."):
        self.name = name
        self.value = value
        self.message = message % (name, value)
        super().__init__(self.message)
