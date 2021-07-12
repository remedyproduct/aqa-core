from selenium.webdriver.common.by import By
from locators.dynamic_value_error import LocatorDynamicValueError
from locators.empty_error import LocatorError


class Locator:
    def __init__(self, name: str, by: By, value: str, dynamic: bool, description: str, check_opening_page: bool):
        self.name = name
        self.by = by
        self._value = value
        self._dynamic = dynamic
        self.description = description
        self._check_opening_page = check_opening_page

    def __str__(self):
        return 'locator(%s)' % self.description

    def value(self, dynamic_value=None):
        if self._dynamic and dynamic_value is None:
            raise LocatorDynamicValueError(self.name)
        self.verify_locator_is_not_empty()
        return self._value if self._dynamic is False else self._value % dynamic_value

    def verify_locator_is_not_empty(self):
        if self.by is None or self.value_not_empty() is False:
            raise LocatorError(self.name, 'By' if self.by is None else 'Value')

    def value_not_empty(self):
        return self._value != ''

    def is_dynamic(self):
        return self._dynamic

    def is_check(self):
        return self._check_opening_page
