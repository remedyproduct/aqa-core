from drivers.base_driver import BaseDriver
from helper.helper import hard_assert_true, sleep
from pages.error import PageNotContainLocatorError


class BasePage:
    def __init__(self, name: str, description: str, locators, driver: BaseDriver):
        self.driver = driver
        self.name = name
        self.description = description
        self.locators = locators

    def is_open(self):
        sleep(self.driver.wait_current)
        self._get_page_status(True)

    def is_close(self):
        sleep(self.driver.wait_current)
        self._get_page_status(False)

    def get_locator(self, locator_name: str):
        for locator in self.locators:
            if locator.name == locator_name:
                locator.verify_locator_is_not_empty()
                return locator
        raise PageNotContainLocatorError(locator_name, self.name, self.driver.platform)

    def _get_page_status(self, status: bool):
        for locator in self.locators:
            if locator.is_check():
                hard_assert_true(
                    self.driver.exists(locator) if status else self.driver.not_exists(locator),
                    "Can not find %s" % locator.description  # TODO update Msg
                )
