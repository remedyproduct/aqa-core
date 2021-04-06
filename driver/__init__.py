import time

from appium.webdriver.common.touch_action import TouchAction
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from appium import webdriver as mobile
from driver.browsers import Browser, setup_browser
from driver.errors import PlatformNotSupportedError
from driver.platforms import setup_platform, Platform
from helper import test_helper as helper
from page import Locator

ANDROID_CAPABILITIES = (
    'platformName', 'platformVersion', 'deviceName', 'udid', 'app', 'appWaitActivity', 'noReset', 'appium', 'fullReset'
)
IOS_CAPABILITIES = (
    'deviceName', 'platformName', 'platformVersion', 'udid', 'automationName', 'app', 'noReset', 'appium', 'fullReset'
)
WEB_CAPABILITIES = ('platformName', 'browserName', 'url', 'fullScreen')
DEFAULT_WAIT_TIME = 30


class Driver:
    _driver = None
    _browser: Browser = Browser.UNKNOWN
    _platform = Platform.UNKNOWN

    def __init__(self, capabilities):
        self._capabilities = capabilities
        self.set_platform_name()
        self.set_platform_settings()
        self._wait_time = DEFAULT_WAIT_TIME

    def __enter__(self):
        self.open_application()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_application()

    def set_platform_name(self, platform_name=None):
        try:
            name = platform_name if platform_name is not None else self._capabilities['platformName']
            self._platform = setup_platform(name)
        except KeyError:
            raise KeyError('Your capabilities have not "platformName" key. Please Fix it.')
        if self._platform == Platform.UNKNOWN:
            raise PlatformNotSupportedError(self._capabilities['platformName'])

    def set_platform_settings(self):
        platform_capabilities = self.get_platform_default_keys()
        for key in platform_capabilities:
            if key not in self._capabilities.keys():
                raise KeyError('"%s" key is not present. Please Fix it.' % key)

    def get_platform_default_keys(self):
        if self._platform == Platform.Android:
            return ANDROID_CAPABILITIES
        elif self._platform == Platform.iOS:
            return IOS_CAPABILITIES
        else:
            return WEB_CAPABILITIES

    # For All platforms
    def open_application(self):
        if self.verify_web_platform():
            self._browser = setup_browser(self._capabilities['browserName'])
            if self._browser == Browser.Chrome:
                self._driver = webdriver.Chrome(ChromeDriverManager().install())
                self.opening_to_url(self._capabilities['url'])
                try:
                    self.resize_screen(
                        self._capabilities['fullScreen'],
                        self._capabilities['width'],
                        self._capabilities['height']
                    )
                except KeyError:
                    self.resize_screen(self._capabilities['fullScreen'])

        if self.verify_mobile_platform():
            if self.verify_android_platform():
                capability = {
                    "platformName": "Android",
                    "platformVersion": self._capabilities['platformVersion'],
                    "deviceName": self._capabilities['deviceName'],
                    "udid": self._capabilities['udid'],
                    "app": self._capabilities['app'],
                    "appWaitActivity": self._capabilities['appWaitActivity'],
                    "noReset": self._capabilities['noReset'],
                    "fullReset": self._capabilities['fullReset']
                }
                self._driver = mobile.Remote("http://localhost:4723/wd/hub", capability)
                self._driver.implicitly_wait(10)
            else:
                capability = {
                    "platformName": "iOS",
                    "deviceName": self._capabilities['deviceName'],
                    "platformVersion": self._capabilities['platformVersion'],
                    "udid": self._capabilities['udid'],
                    "automationName": self._capabilities['automationName'],
                    "app": self._capabilities['app'],
                    "noReset": self._capabilities['noReset'],
                    "fullReset": self._capabilities['fullReset']
                }
                self._driver = mobile.Remote(self._capabilities['appium'], capability)
                self._driver.implicitly_wait(10)

    def close_application(self):
        if self._platform == Platform.Web:
            self._driver.close()
        else:
            self._driver.close_app()

    def reopen_application(self):
        if self.verify_mobile_platform():
            self._driver.launch_app()
            self._driver.implicitly_wait(10)
        else:
            self.close_application()
            self.open_application()

    def reset_application(self):
        if self.verify_mobile_platform():
            self._driver.reset()
            self._driver.implicitly_wait(10)
        else:
            self.close_application()
            self.open_application()

    # Web platform only
    def verify_web_platform(self):
        return self._platform == Platform.Web

    def opening_to_url(self, url):
        if self.verify_web_platform():
            self._driver.get(url)

    def resize_screen(self, full_screen: bool = True, width=1024, height=768):
        if self.verify_web_platform():
            if full_screen:
                self._driver.maximize_window()
            else:
                self._driver.set_window_position(0, 0)
                self._driver.set_window_size(width, height)

    # Mobile platforms only
    def verify_mobile_platform(self):
        return self._platform == Platform.Android or self._platform == Platform.iOS

    def verify_android_platform(self):
        return self._platform == Platform.Android

    def verify_ios_platform(self):
        return self._platform == Platform.iOS

    def orientation(self, landscape: bool = False):
        if self.verify_mobile_platform():
            if landscape:
                self._driver.orientation = "LANDSCAPE"
            else:
                self._driver.orientation = "PORTRAIT"

    def hide_keyboard(self):
        if self.verify_mobile_platform() and self._driver.is_keyboard_shown():
            self._driver.hide_keyboard()

    # Report or Error only
    def platform(self):
        return self._platform

    def get_screenshot_as_png(self):
        return self._driver.get_screenshot_as_png()

    def source(self):
        return self._driver.page_source

    def set_wait_time(self, seconds=DEFAULT_WAIT_TIME):
        self._wait_time = seconds

    # User interface control methods
    def wait_element(self, locator: Locator, dynamic_value=None, hard_assert=True):
        now = time.time()
        future = now + self._wait_time
        while time.time() < future:
            if self.exists(locator, dynamic_value):
                return True
        if hard_assert:
            helper.error_message(
                'Can not found "%s" locator with "%s" by and "%s" value. Description: %s.'
                % (locator.name(), locator.by(), locator.value(dynamic_value), locator.description())
            )

        return False

    def exists(self, locator: Locator, dynamic_value=None):
        try:
            return self._driver.find_element(locator.by(), locator.value(dynamic_value)).is_displayed()
        except NoSuchElementException:
            return False

    def not_exists(self, locator: Locator, dynamic_value=None):
        return False if self.wait_element(locator, dynamic_value, False) else True

    def click(self, locator: Locator, dynamic_value=None):
        if self.wait_element(locator, dynamic_value):
            self._driver.find_element(locator.by(), locator.value(dynamic_value)).click()

    def clear_field(self, locator: Locator, dynamic_value=None):
        if self.wait_element(locator, dynamic_value):
            self._driver.find_element(locator.by(), locator.value(dynamic_value)).clear()

    def enter_text(self, locator: Locator, text, dynamic_value=None):
        if self.wait_element(locator, dynamic_value):
            self._driver.find_element(locator.by(), locator.value(dynamic_value)).send_keys(text)

    def clear_and_enter_text(self, locator: Locator, text, dynamic_value=None):
        if self.wait_element(locator, dynamic_value):
            element = self._driver.find_element(locator.by(), locator.value(dynamic_value))
            element.clear()
            element.send_keys(text)

    def get_element_text(self, locator: Locator, dynamic_value=None):
        if self.wait_element(locator, dynamic_value):
            if self._platform == Platform.Web:
                element = self._driver.find_element(locator.by(), locator.value(dynamic_value))
                return element.text if element.text != '' else element.get_attribute("value")
            else:
                return self._driver.find_element(locator.by(), locator.value(dynamic_value)).text

    # TODO REMOVE
    def get_driver(self):
        return self._driver

    # TODO Mobile only
    def tap(self, x, y, seconds=1, element=None):
        if self.verify_mobile_platform():
            TouchAction(self._driver).tap(element, x, y, seconds).perform()

    def get_window_size(self):
        return self._driver.get_window_size()

    def scroll(self, locator: Locator, dynamic_value=None):
        if self.verify_mobile_platform():
            element_to_tap = self._driver.find_element(locator.by(), locator.value(dynamic_value))
            element_to_drag_to = element_to_tap
            self._driver.scroll(element_to_tap, element_to_drag_to)

    def swipe_from_bottom_to_top(self):
        if self.verify_mobile_platform():
            size = self.get_window_size()
            y_start = int(size['height'] * 0.80)
            y_end = int(size['height'] * 0.20)
            x_start = 0  # int(size['width'] / 2)
            time.sleep(2)
            self._driver.swipe(x_start, y_start, x_start, y_end, 3000)
            time.sleep(2)

    def swipe_from_top_to_bottom(self):
        if self.verify_mobile_platform():
            size = self.get_window_size()
            y_start = int(size['height'] * 0.80)
            y_end = int(size['height'] * 0.20)
            x_start = 0  # int(size['width'] / 2)
            time.sleep(2)
            self._driver.swipe(x_start, y_end, x_start, y_start, 3000)
            time.sleep(2)
