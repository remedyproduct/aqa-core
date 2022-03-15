from copy import copy
from drivers.driver_target_error import DriverTargetError
from drivers.mobile.mobile_device import get_mobile_device, MobileDevice
from drivers.platform.error import PlatformError
from drivers.platform.platforms import Platform, get_platform
from abc import ABC, abstractmethod
from drivers.web.browsers import get_web_browser, Browser
from helper.echo import echo, ECHO_COLORS
from locators.locator import Locator


class BaseDriver(ABC):
    """Base Driver tool is used to automate web and mobile application testing to verify that it works as expected."""

    def __init__(self, capabilities):
        self.capabilities = copy(capabilities)
        self.platform = self._set_platform()
        self.target = self._set_driver_target()
        self.driver = None
        self.KEYS = None
        self.TIME_TO_WAIT = 10

    def __str__(self):
        return ('Web[%s]' if self.platform == Platform.WEB else 'MobileDevice[%s]') % self.target.value

    """Base methods"""

    def check_params(self):
        for key in self.KEYS:
            if key not in self.capabilities.keys():
                raise KeyError('%s: "%s" key is not present. Please Fix it.' % (self.target.value, key))

    def is_mobile_platform(self):
        return self.platform is Platform.MOBILE

    def is_web_platform(self):
        return self.platform is Platform.WEB

    def is_android(self):
        if self.is_mobile_platform():
            return self.target == MobileDevice.ANDROID
        return False

    def is_ios(self):
        if self.is_mobile_platform():
            return self.target == MobileDevice.iOS
        return False

    def get_screenshot_as_png(self):
        return self.driver.get_screenshot_as_png()

    def get_page_source(self):
        return self.driver.page_source

    def get_window_size(self):
        return self.driver.get_window_size()

    def set_max_wait_time(self):
        self.TIME_TO_WAIT = 30

    def set_min_wait_time(self):
        self.TIME_TO_WAIT = 5

    def set_default_wait_time(self):
        self.TIME_TO_WAIT = 10

    def set_custom_wait_time(self, time_to_wait: int):
        self.TIME_TO_WAIT = time_to_wait

    def get_browser_version(self):
        if self.target == Browser.OPERA:
            return self.driver.capabilities['opera']['operadriverVersion']
        else:
            return self.driver.capabilities['browserVersion']

    """Abstract methods"""

    @abstractmethod
    def open_application(self):
        pass

    @abstractmethod
    def close_application(self):
        pass

    @abstractmethod
    def reopen_application(self):
        pass

    @abstractmethod
    def reset_application(self):
        pass

    @abstractmethod
    def explicit_wait(self, locator: Locator, dynamic_value=None):
        pass

    @abstractmethod
    def implicit_wait(self, locator: Locator, dynamic_value=None):
        pass

    @abstractmethod
    def item_search(self, locator: Locator, dynamic_value=None):
        pass

    @abstractmethod
    def displayed(self, locator: Locator, dynamic_value=None):
        pass

    @abstractmethod
    def not_displayed(self, locator: Locator, dynamic_value=None):
        pass

    @abstractmethod
    def click(self, locator: Locator, dynamic_value=None):
        pass

    @abstractmethod
    def clear(self, locator: Locator, dynamic_value=None):
        pass

    @abstractmethod
    def input(self, locator: Locator, text: str, slow=False, dynamic_value=None):
        pass

    @abstractmethod
    def clean_input(self, locator: Locator, text: str, slow=False, dynamic_value=None):
        pass

    @abstractmethod
    def text(self, locator: Locator, dynamic_value=None):
        pass

    @abstractmethod
    def scroll_up(self):
        pass

    @abstractmethod
    def scroll_down(self):
        pass

    @abstractmethod
    def dropdown_select(self, select_text: str, locator: Locator, dynamic_value=None):
        pass

    """Web only"""

    @abstractmethod
    def url(self, url: str):
        pass

    @abstractmethod
    def resize_screen(self, full: bool = True, width=1024, height=768):
        pass

    @abstractmethod
    def set_image(self, locator: Locator, file: str):
        pass

    @abstractmethod
    def switch_to_frame(self, iframe):
        pass

    @abstractmethod
    def switch_to_default_content(self):
        pass

    @abstractmethod
    def set_window_position(self, x: int, y: int):
        pass

    @abstractmethod
    def refresh_page(self):
        pass

    """Mobile only"""

    @abstractmethod
    def orientation(self, landscape: bool = False):
        pass

    @abstractmethod
    def tap(self, x, y, seconds=1, element=None):
        pass

    @abstractmethod
    def take_photo(self, locator: Locator = None, dynamic_value=None):
        pass

    """Private methods"""

    @staticmethod
    def _skip_method(method_name, reason: str = 'it was not implemented'):
        echo('"%s" method was skipped, because %s.' % (method_name, reason), ECHO_COLORS.WARNING)
        return False

    @staticmethod
    def _check_element(element, locator):
        if element is None:
            msg = "Can not find %s." % locator.description
            echo(msg, ECHO_COLORS.FAIL)
            raise Exception(msg)

    def _set_platform(self):
        try:
            return get_platform(self.capabilities['platformName'])
        except KeyError:
            raise PlatformError("Could not find the 'platformName' key in the file")

    def _set_driver_target(self):
        if self.platform == Platform.WEB:
            return get_web_browser(self.capabilities['browserName'])
        elif self.platform == Platform.MOBILE:
            return get_mobile_device(self.capabilities['platformName'])
        else:
            raise DriverTargetError(self.platform)
