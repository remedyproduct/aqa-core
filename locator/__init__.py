from selenium.webdriver.common.by import By

from locator.errors import LocatorDynamicValueError, LocatorError
from locator.locator_by import setup_locator_by


def create_locator(name, by, value, dynamic, description):
    return Locator(name, setup_locator_by(by), value, dynamic, description)


class Locator:
    def __init__(self, name: str, by: By, value: str, dynamic: bool, description: str):
        self._name = name
        self._by = by
        self._value = value
        self._dynamic = dynamic
        self._description = description

    def name(self):
        return self._name

    def value(self, dynamic_value=None):
        if self._dynamic and dynamic_value is None:
            raise LocatorDynamicValueError(self._name)
        self.verify_locator_is_not_empty()
        return self._value if self._dynamic is False else self._value % dynamic_value

    def verify_locator_is_not_empty(self):
        if self._by is None or self.value_not_empty() is False:
            raise LocatorError(self._name, 'By' if self._by is None else 'Value')

    def value_not_empty(self):
        return self._value != ''

    def by(self):
        return self._by

    def description(self):
        return self._description

    def is_dynamic(self):
        return self._dynamic
