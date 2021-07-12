from selenium.webdriver.common.by import By
from drivers.base_driver import BaseDriver
from drivers.event_wrapper import event_wrapper as wrapper
from drivers.mobile.mobile_device import MobileDevice
from appium import webdriver as mobile
from helper.helper import sleep
from locators.locator import Locator
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

    @wrapper(method_name='Open application')
    def open_app(self):
        self.driver = mobile.Remote(self.capabilities['appium'], self.capabilities)
        self.driver.implicitly_wait(10)
        return self.driver is not None

    @wrapper(method_name='Close application')
    def close_app(self):
        self.driver.close_app()
        return True

    @wrapper(method_name='Reopen application')
    def reopen_app(self):
        self.driver.launch_app()
        self.driver.implicitly_wait(10)
        return self.driver is not None

    @wrapper(method_name='Refresh page')
    def refresh_page(self):
        return False

    @wrapper(method_name='Reset application')
    def reset_app(self):
        self.driver.reset()
        self.driver.implicitly_wait(10)
        return self.driver is not None

    @wrapper(method_name='Get text')
    def get_text(self, locator: Locator, dynamic_value=None):
        if self.wait(locator, dynamic_value):
            return self.driver.find_element(locator.by, locator.value(dynamic_value)).text

    # @wrapper(method_name='Take photo')
    def take_photo(self, locator: Locator = None, dynamic_value=None):
        if locator is not None:
            self.click(locator, dynamic_value)
        if self.target == MobileDevice.iOS:
            self.click(iOS_SELECT_TAKE_PHOTO)
            sleep(3)
            self.tap(50, 300, 1)
            self.tap(50, 300, 1)
            sleep(1)
            self.click(iOS_TAKE_PHOTO)
            sleep(3)
            self.click(iOS_COMPLETE_PHOTO)
        else:
            self._android_select_take_photo()
            self._android_take_photo()
            self._android_complete_photo()
        return True

    @wrapper(method_name='Dropdown select')
    def dropdown_select(self, select_text: str, locator: Locator, dynamic_value=None):
        if locator is not None:
            self.click(locator, dynamic_value)
        if self.target == MobileDevice.iOS:
            self.input(Locator(name='PICKER WHEEL SELECT',
                               by=By.XPATH,
                               value='//XCUIElementTypePicker[@name="ios_picker"]/XCUIElementTypePickerWheel',
                               dynamic=False, description='PICKER WHEEL SELECT', check_opening_page=False
                               ),
                       select_text)
            self.click(Locator(name='PICKER WHEEL DONE',
                               by=By.XPATH, value='//XCUIElementTypeOther[@name="done_button"]',
                               dynamic=False, description='PICKER WHEEL DONE', check_opening_page=False
                               ))
        else:
            self.click(Locator(name='ANDROID_SELECT',
                               by=By.XPATH, value='//android.widget.CheckedTextView[@text="%s"]',
                               dynamic=True, description='ANDROID_SELECT', check_opening_page=False
                               ),
                       select_text)
        return True

    def switch_to_frame(self, iframe):
        return False

    def switch_to_default_content(self):
        return False

    # private
    def _android_select_take_photo(self):
        sleep(1)
        self.click(ANDROID_SELECT_TAKE_PHOTO)
        sleep(3)

    def _android_take_photo(self):
        sleep(1)
        take_photo = None
        if self.is_exists(ANDROID_TAKE_PHOTO_1):
            take_photo = ANDROID_TAKE_PHOTO_1
        elif take_photo is None and self.is_exists(ANDROID_TAKE_PHOTO_2):
            take_photo = ANDROID_TAKE_PHOTO_2
        else:
            take_photo = ANDROID_TAKE_PHOTO_3
        self.click(take_photo)
        sleep(3)

    def _android_complete_photo(self):
        sleep(1)
        self.click(ANDROID_COMPLETE_PHOTO_1 if self.is_exists(ANDROID_COMPLETE_PHOTO_1) else ANDROID_COMPLETE_PHOTO_2)
        sleep(3)
