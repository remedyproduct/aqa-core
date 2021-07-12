

class NoSuchPageInStorage(Exception):
    """Exception raised when page can not be find in storage.

    Attributes:
        page_name -- page which caused the error
        message -- explanation of the error
    """

    def __init__(self, page_name, message="No such '%s' in the repository"):
        self.message = message % page_name
        super().__init__(self.message)
