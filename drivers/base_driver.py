from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from appium import webdriver as mobile
from allure.allure import error_message
from drivers.driver_target_error import DriverTargetError
from drivers.event_wrapper import event_wrapper as wrapper
from drivers.mobile.mobile_device import get_mobile_device, MobileDevice
from drivers.platform.error import PlatformError
from drivers.platform.platforms import Platform, get_platform
from abc import ABC, abstractmethod
from drivers.web.browsers import get_web_browser
from helper.echo import *
from locators.locator import Locator
import datetime
import time


class BaseDriver(ABC):
    """Base Driver tool is used to automate web and mobile application testing to verify that it works as expected."""

    def __init__(self, capabilities):
        self.capabilities = capabilities
        self.platform = self._set_platform()
        self.target = self._set_driver_target()
        self.driver = None
        self.KEYS = None
        self.wait_default = 5
        self.wait_current = 5
        self.set_wait_time_default()

    def __str__(self):
        return ('Browser(%s)' if self.platform == Platform.WEB else 'MobileDevice(%s)') % self.target.value

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

    def set_wait_time(self, seconds=5):
        self.wait_current = seconds

    def set_wait_time_default(self, seconds=None):
        if seconds is not None:
            self.wait_default = seconds
        self.wait_current = self.wait_default

    def is_exists(self, locator: Locator, dynamic_value=None):
        t_start = datetime.datetime.now()
        t_end = t_start + datetime.timedelta(seconds=self.wait_current)
        while True:
            if datetime.datetime.now() >= t_end:
                break
            try:
                if self.driver.find_element(locator.by, locator.value(dynamic_value)).is_displayed():
                    return True
            except NoSuchElementException:
                continue
        return False

    @wrapper(method_name='exists')
    def exists(self, locator: Locator, dynamic_value=None):
        try:
            return self.driver.find_element(locator.by, locator.value(dynamic_value)).is_displayed()
        except NoSuchElementException:
            return False

    @wrapper(method_name='not exists')
    def not_exists(self, locator: Locator, dynamic_value=None):
        try:
            self.driver.find_element(locator.by, locator.value(dynamic_value))
            return False
        except NoSuchElementException:
            return True

    @wrapper(method_name='wait')
    def wait(self, locator: Locator, dynamic_value=None, hard_assert=True):
        t_start = datetime.datetime.now()
        t_end = t_start + datetime.timedelta(seconds=self.wait_current)
        while True:
            if datetime.datetime.now() >= t_end:
                break
            try:
                if self.driver.find_element(locator.by, locator.value(dynamic_value)).is_displayed():
                    return True
                if self.is_web_platform():
                    self.driver.execute_script(
                        "arguments[0].scrollIntoView();",
                        self.driver.find_element(locator.by, locator.value(dynamic_value))
                    )
            except NoSuchElementException:
                continue
            except TimeoutException:
                continue
        if hard_assert:
            msg = '[Data: %s] [Method: %s] [Status: %s] + [Hard Assert]' % (self, 'wait', 'Fail')
            echo(msg, color=ECHO_COLORS.FAIL)
            error_message(msg, self)
            assert False, msg
        return False

    @wrapper(method_name='click')
    def click(self, locator: Locator, dynamic_value=None):
        if self.wait(locator, dynamic_value):
            self.driver.find_element(locator.by, locator.value(dynamic_value)).click()
            return True
        return False

    @wrapper(method_name='clear')
    def clear(self, locator: Locator, dynamic_value=None):
        if self.wait(locator, dynamic_value):
            element = self.driver.find_element(locator.by, locator.value(dynamic_value))
            if self.is_mobile_platform():
                element.clear()
            else:
                element.send_keys(''.join(map(str, ['\b' for i in self.get_text(locator, dynamic_value)])))
            return True
        return False

    @wrapper(method_name='input')
    def input(self, locator: Locator, text, dynamic_value=None):
        if self.wait(locator, dynamic_value):
            self.driver.find_element(locator.by, locator.value(dynamic_value)).send_keys(text)
            return True
        return False

    @wrapper(method_name='clear & input')
    def clear_and_input(self, locator: Locator, text, dynamic_value=None):
        if self.wait(locator, dynamic_value):
            self.clear(locator, dynamic_value)
            self.input(locator, text, dynamic_value)
            return True
        return False

    """Mobile only"""

    @wrapper(method_name='Orientation')
    def orientation(self, landscape: bool = False):
        if self.is_mobile_platform():
            if landscape:
                self.driver.orientation = 'LANDSCAPE'
            else:
                self.driver.orientation = 'PORTRAIT'
            return True
        return False

    def hide_keyboard(self):
        if self.is_mobile_platform():
            self.driver.hide_keyboard()

    @wrapper(method_name='Tap')
    def tap(self, x, y, seconds=1, element=None):
        if self.is_mobile_platform():
            TouchAction(self.driver).tap(element, x, y, seconds).perform()
            return True
        return False

    @wrapper(method_name='Scroll')
    def scroll(self, locator1: Locator, locator2: Locator, dynamic_value1=None, dynamic_value2=None):
        if self.is_mobile_platform():
            element1 = self.driver.find_element(locator1.by, locator1.value(dynamic_value1))
            element2 = self.driver.find_element(locator2.by, locator2.value(dynamic_value2))
            action = TouchAction(self.driver)
            action.press(element1).move_to(element2).release().perform()
            return True
        return False

    @wrapper(method_name='Swipe from bottom to top')
    def swipe_from_bottom_to_top(self):
        if self.is_mobile_platform():
            size = self.get_window_size()
            y_start = int(size['height'] * 0.80)
            y_end = int(size['height'] * 0.20)
            x_start = 0
            time.sleep(2)
            self.driver.swipe(x_start, y_start, x_start, y_end, 3000)
            time.sleep(2)
            return True
        return False

    @wrapper(method_name='Swipe from top to bottom')
    def swipe_from_top_to_bottom(self):
        if self.is_mobile_platform():
            size = self.get_window_size()
            y_start = int(size['height'] * 0.80)
            y_end = int(size['height'] * 0.20)
            x_start = 0
            time.sleep(2)
            self.driver.swipe(x_start, y_end, x_start, y_start, 3000)
            time.sleep(2)
            return True
        return False

    """Web only"""

    @wrapper(method_name='URL')
    def url(self, url: str):
        if self.is_web_platform():
            self.driver.get(url)
            return True
        return False

    @wrapper(method_name='Resize screen')
    def resize_screen(self, full: bool = True, width=1024, height=768):
        if self.is_web_platform():
            if full:
                self.driver.maximize_window()
            else:
                self.set_window_position(0, 0)
                self.driver.set_window_size(width, height)
            return True
        return False

    @wrapper(method_name='Set window position')
    def set_window_position(self, x, y):
        if self.is_web_platform():
            self.driver.set_window_position(x, y)
            return True
        return False

    """Abstract methods"""

    @abstractmethod
    def open_app(self):
        pass

    @abstractmethod
    def close_app(self):
        pass

    @abstractmethod
    def reopen_app(self):
        pass

    @abstractmethod
    def reset_app(self):
        pass

    @abstractmethod
    def refresh_page(self):
        pass

    @abstractmethod
    def get_text(self, locator: Locator, dynamic_value=None):
        pass

    @abstractmethod
    def take_photo(self, locator: Locator = None, dynamic_value=None):
        pass

    @abstractmethod
    def dropdown_select(self, select_text: str, locator: Locator, dynamic_value=None):
        pass

    @abstractmethod
    def switch_to_frame(self, iframe):
        pass

    @abstractmethod
    def switch_to_default_content(self):
        pass

    """Private methods"""

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

    # TODO Remove
    def get_driver(self):
        return self.driver
