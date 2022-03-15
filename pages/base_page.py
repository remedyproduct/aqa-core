import math
import time

from drivers.base_driver import BaseDriver
from helper.echo import echo, ECHO_COLORS
from helper.helper import hard_assert_true, sleep
from pages.error import PageNotContainLocatorError


class BasePage:
    def __init__(self, name: str, description: str, locators, driver: BaseDriver):
        self.driver = driver
        self.name = name
        self.description = description
        self.locators = locators

    def is_open(self):
        self._get_page_status(True)

    def is_close(self):
        self._get_page_status(False)

    def get_locator(self, locator_name: str):
        for locator in self.locators:
            if locator.name == locator_name:
                locator.verify_locator_is_not_empty()
                return locator
        raise PageNotContainLocatorError(locator_name, self.name, self.driver.platform)

    def _get_page_status(self, status: bool):
        echo(
            'Verify "%s" page is %s. The method has been started.'
            % (self.name, 'Open' if status else 'Closed'),
            ECHO_COLORS.WARNING
        )
        index = 0
        start_time = time.time()
        for locator in self.locators:
            if index == 2 and self.driver.is_mobile_platform():
                break
            if locator.is_check():
                hard_assert_true(
                    self.driver.displayed(locator) if status else self.driver.not_displayed(locator),
                    "Can not find %s." % locator.description  # TODO update Msg
                )
                index += 1
        echo('The %s method was over. Its time is %s seconds.'
             % ('Open' if status else 'Close', math.ceil(time.time() - start_time)), ECHO_COLORS.WARNING
             )
