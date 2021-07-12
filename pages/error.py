

class PageNotContainLocatorError(Exception):
    """Exception raised for errors for page does not find a locator.

    Attributes:
        locator_name, page_name and platform -- platform which caused the error
        message -- explanation of the error
    """

    def __init__(self, locator_name, page_name, platform, message="Can't find the %s for %s page, platform - %s."):
        self.locator_name = locator_name
        self.page_name = page_name
        self.platform = platform
        self.message = message % (locator_name, page_name, platform)
        super().__init__(self.message)
