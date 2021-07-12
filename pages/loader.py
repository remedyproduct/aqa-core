import json
from drivers.base_driver import BaseDriver
from drivers.platform.platforms import Platform
from locators.by import get_by
from locators.locator import Locator
from pages.base_page import BasePage
from pages.no_such_page_in_storage_error import NoSuchPageInStorage


class Loader(object):
    platform_name = None
    driver = None
    path = None

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Loader, cls).__new__(cls)
        return cls.instance

    def set_driver(self, driver):
        self.driver = driver
        self.platform_name = Platform.WEB.value if driver.platform == Platform.WEB else driver.target.value
        return self

    def set_file(self, path: str):
        self.path = path
        return self

    def update(self, driver: BaseDriver, path: str):
        self.set_driver(driver).set_file(path)
        return self

    def get_page(self, page_name):
        for page in self._get_pages():
            if page['pageName'] == page_name:
                page_locators = []
                for locator in page['pageLocators']:
                    page_locators.append(self._generate_locator(locator))
                return BasePage(page['pageName'], page['pageDescription'], page_locators, self.driver)
        raise NoSuchPageInStorage(page_name)

    def _get_pages(self):
        with open(self.path) as locators:
            return json.load(locators)['pages']

    def _generate_locator(self, locator):
        return Locator(
            locator['locatorName'],
            get_by(locator[self.platform_name]['locatorBy']),
            locator[self.platform_name]['locatorValue'],
            locator[self.platform_name]['locatorDynamic'],
            locator['locatorDescription'],
            self._get_locator_check_parameter(locator)
        )

    @staticmethod
    def _get_locator_check_parameter(locator):
        try:
            return locator['checkOpeningPage']
        except KeyError:
            return False
