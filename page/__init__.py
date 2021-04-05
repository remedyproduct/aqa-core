from driver.platforms import Platform
from locator import Locator
from locator.locator_by import setup_locator_by
from page.errors import PageNotContainLocatorError


class Pages(object):
    _platform = Platform.UNKNOWN
    _pages = None

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Pages, cls).__new__(cls)
        return cls.instance

    def update(self, platform, list_pages):
        self._platform = platform
        self._pages = []
        for page in list_pages:
            page_locators = []
            for locator in page['pageLocators']:
                page_locators.append(
                    Locator(
                        locator['locatorName'],
                        setup_locator_by(locator[platform.value]['locatorBy']),
                        locator[platform.value]['locatorValue'],
                        locator[platform.value]['locatorDynamic'],
                        locator['locatorDescription']
                    )
                )
            self._pages.append({
                "pageName": page['pageName'],
                "pageDescription": page['pageDescription'],
                "pageLocators": page_locators
            })

    def get_locator(self, page_name, locator_name):
        for page in self._pages:
            if page['pageName'] == page_name:
                for locator in page['pageLocators']:
                    if locator.name() == locator_name:
                        locator.verify_locator_is_not_empty()
                        return locator
        raise PageNotContainLocatorError(locator_name, page_name, self._platform.value)


pages = Pages()
