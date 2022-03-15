from datetime import datetime, timedelta
from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import NoSuchElementException, TimeoutException, InvalidElementStateException
from drivers.event_wrapper import event_wrapper as wrapper
from drivers.mobile.mobile_device import MobileDevice
from appium import webdriver as mobile
from helper.helper import sleep
from ..base_driver import BaseDriver
from ..mobile.LOCATORS import *

ANDROID_KEYS = ['platformName', 'platformVersion', 'deviceName', 'udid', 'app', 'noReset', 'appWaitActivity', 'appium']
iOS_KEYS = ['platformName', 'platformVersion', 'deviceName', 'udid', 'app', 'noReset', 'automationName', 'appium']


class MobileDriver(BaseDriver):
    """Appium Driver tool is used to automate mobile application testing to verify that it works as expected.
    It supports many devices with Android and iOS platforms."""

    def __init__(self, capabilities):
        global ANDROID_KEYS, iOS_KEYS
        """Mobile Capabilities keys:
        1. platformName: str
        2. platformVersion: str
        3. deviceName: str
        4. udid: str
        5. app: str
        6. noReset: bool
        7. appium: str
        Android Capabilities keys:
        8. appWaitActivity: str
        iOS Capabilities keys:
        8. automationName: str"""
        super().__init__(capabilities)
        self.KEYS = ANDROID_KEYS if self.target is MobileDevice.ANDROID else iOS_KEYS
        self.check_params()

    @wrapper(method_name='Open Application')
    def open_application(self):
        self.driver = mobile.Remote(self.capabilities['appium'], self.capabilities)

    @wrapper(method_name='Close Application')
    def close_application(self):
        self.driver.close_app()

    @wrapper(method_name='Reopen Application')
    def reopen_application(self):
        self.close_application()
        self.open_application()

    @wrapper(method_name='Reset Application')
    def reset_application(self):
        self.driver.reset()

    @wrapper(method_name='Explicit Wait')
    def explicit_wait(self, locator: Locator, dynamic_value=None):
        t_start = datetime.now()
        t_end = t_start + timedelta(seconds=self.TIME_TO_WAIT)
        while True:
            if datetime.now() >= t_end:
                break
            try:
                element = self.driver.find_element(locator.by, locator.value(dynamic_value))
                if element.is_displayed():
                    return element
            except NoSuchElementException:
                continue
            except TimeoutException:
                continue
        return None

    @wrapper(method_name='Implicit Wait')
    def implicit_wait(self, locator: Locator, dynamic_value=None):
        t_start = datetime.now()
        t_end = t_start + timedelta(seconds=self.TIME_TO_WAIT)
        while True:
            if datetime.now() >= t_end:
                break
            try:
                element = self.driver.find_element(locator.by, locator.value(dynamic_value))
                if element.is_displayed():
                    return element
            except NoSuchElementException:
                sleep(1)
                continue
            except TimeoutException:
                continue
        return None

    @wrapper(method_name='Item Search')
    def item_search(self, locator: Locator, dynamic_value=None):
        return self.implicit_wait(locator, dynamic_value)

    @wrapper(method_name='Displayed')
    def displayed(self, locator: Locator, dynamic_value=None):
        try:
            element = self.item_search(locator, dynamic_value)
            if element is not None:
                return element.is_displayed()
            else:
                return False
        except NoSuchElementException:
            return False
        except AttributeError:
            return False

    @wrapper(method_name='Not Displayed')
    def not_displayed(self, locator: Locator, dynamic_value=None):
        try:
            element = self.item_search(locator, dynamic_value)
            if element is not None:
                return False
            else:
                return True
        except NoSuchElementException:
            return True

    @wrapper(method_name='Click')
    def click(self, locator: Locator, dynamic_value=None):
        element = self.item_search(locator, dynamic_value)
        self._check_element(element, locator)
        element.click()

    @wrapper(method_name='Clear')
    def clear(self, locator: Locator, dynamic_value=None):
        element = self.item_search(locator, dynamic_value)
        self._check_element(element, locator)
        element.clear()
        self.hide_keyboard()

    @wrapper(method_name='Input')
    def input(self, locator: Locator, text: str, slow=False, dynamic_value=None):
        element = self.item_search(locator, dynamic_value)
        self._check_element(element, locator)
        element.send_keys(text)
        self.hide_keyboard()

    @wrapper(method_name='Clean Input')
    def clean_input(self, locator: Locator, text: str, slow=False, dynamic_value=None):
        element = self.item_search(locator, dynamic_value)
        self._check_element(element, locator)
        element.clear()
        element.send_keys(text)
        self.hide_keyboard()

    @wrapper(method_name='Text')
    def text(self, locator: Locator, dynamic_value=None):
        element = self.item_search(locator, dynamic_value)
        self._check_element(element, locator)
        return element.text

    @wrapper(method_name='Scroll Up')
    def scroll_up(self):
        if self.is_ios():
            sleep(2)
        size = self.get_window_size()
        y_start = int(size['height'] * 0.80)
        y_end = int(size['height'] * 0.20)
        x_start = 0
        self.driver.swipe(x_start, y_end, x_start, y_start, 3000)

    @wrapper(method_name='Scroll Down')
    def scroll_down(self):
        if self.is_ios():
            sleep(2)
        size = self.get_window_size()
        y_start = int(size['height'] * 0.80)
        y_end = int(size['height'] * 0.20)
        x_start = 0
        self.driver.swipe(x_start, y_start, x_start, y_end, 3000)

    @wrapper(method_name='Dropdown Select')
    def dropdown_select(self, select_text: str, locator: Locator, dynamic_value=None):
        self.item_search(locator, dynamic_value).click()
        if self.target == MobileDevice.iOS:
            self.item_search(iOS_PICKER_WHEEL_SELECT).send_keys(select_text)
            self.item_search(iOS_PICKER_WHEEL_DONE).click()
        else:
            self.item_search(ANDROID_SELECT, select_text).click()

    @wrapper(method_name='URL')
    def url(self, url: str):
        self._skip_method('url')

    @wrapper(method_name='Resize Screen')
    def resize_screen(self, full: bool = True, width=1024, height=768):
        self._skip_method('resize_screen')

    @wrapper(method_name='Set Image')
    def set_image(self, locator: Locator, file: str):
        self._skip_method('set_image')

    @wrapper(method_name='Switch To Frame')
    def switch_to_frame(self, iframe):
        self._skip_method('switch_to_frame')

    @wrapper(method_name='Switch To Default Content')
    def switch_to_default_content(self):
        self._skip_method('switch_to_default_content')

    @wrapper(method_name='Set Window Position')
    def set_window_position(self, x: int, y: int):
        self._skip_method('set_window_position')

    @wrapper(method_name='Refresh Page')
    def refresh_page(self):
        self._skip_method('refresh_page')

    @wrapper(method_name='Orientation')
    def orientation(self, landscape: bool = False):
        if landscape:
            self.driver.orientation = 'LANDSCAPE'
        else:
            self.driver.orientation = 'PORTRAIT'

    @wrapper(method_name='Tap')
    def tap(self, x, y, seconds=1, element=None):
        TouchAction(self.driver).tap(element, x, y, seconds).perform()

    @wrapper(method_name='Take Photo')
    def take_photo(self, locator: Locator = None, dynamic_value=None):
        self.item_search(locator, dynamic_value).click()
        if self.target == MobileDevice.iOS:
            self.click(iOS_SELECT_TAKE_PHOTO)
            sleep(3)
            self.tap(50, 300, 1)
            self.tap(50, 300, 1)
            sleep(1)
            self.item_search(iOS_TAKE_PHOTO).click()
            sleep(3)
            self.item_search(iOS_COMPLETE_PHOTO).click()
        else:
            self._android_select_take_photo()
            self._android_take_photo()
            self._android_complete_photo()

    """Private methods"""

    def hide_keyboard(self):
        if self.driver.is_keyboard_shown():
            try:
                if self.is_ios():
                    self.driver.hide_keyboard('return')
                else:
                    self.driver.hide_keyboard()
            except InvalidElementStateException:
                if self.is_ios() and self.driver.is_keyboard_shown():
                    TouchAction(self.driver).tap(None, 100, 100, 1).perform()

    def _android_select_take_photo(self):
        self.item_search(ANDROID_SELECT_TAKE_PHOTO).click()

    def _android_take_photo(self):
        take_photo = None
        if self.item_search(ANDROID_TAKE_PHOTO_1):
            take_photo = ANDROID_TAKE_PHOTO_1
        elif take_photo is None and self.item_search(ANDROID_TAKE_PHOTO_2):
            take_photo = ANDROID_TAKE_PHOTO_2
        elif take_photo is None and self.item_search(ANDROID_TAKE_PHOTO_3):
            take_photo = ANDROID_TAKE_PHOTO_3
        else:
            take_photo = ANDROID_TAKE_PHOTO_4
        self.item_search(take_photo).click()

    def _android_complete_photo(self):
        complete_photo = None
        if self.item_search(ANDROID_COMPLETE_PHOTO_1):
            complete_photo = ANDROID_COMPLETE_PHOTO_1
        elif complete_photo is None and self.item_search(ANDROID_COMPLETE_PHOTO_2):
            complete_photo = ANDROID_COMPLETE_PHOTO_2
        else:
            complete_photo = ANDROID_COMPLETE_PHOTO_3
        self.item_search(complete_photo).click()
