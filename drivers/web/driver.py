from drivers.base_driver import BaseDriver
from drivers.event_wrapper import event_wrapper as wrapper
from drivers.web.browsers import Browser
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.microsoft import IEDriverManager
from webdriver_manager.opera import OperaDriverManager
from locators.locator import Locator


class WebDriver(BaseDriver):
    """Selenium WebDriver tool is used to automate web application testing to verify that it works as expected.
    It supports many browsers such as Chromium/Chrome, Firefox, Edge, Internet Explorer, Safari and Opera."""

    def __init__(self, capabilities):
        """Capabilities keys:
        main - platformName: str, browserName: str, url: str, fullScreen: str
        not necessary - width: int, height: int"""
        super().__init__(capabilities)
        self.KEYS = ['platformName', 'browserName', 'url', 'fullScreen']
        self.check_params()

    @wrapper(method_name='Open application')
    def open_app(self):
        if self.target is Browser.CHROME:
            self.driver = webdriver.Chrome(ChromeDriverManager().install())
        elif self.target is Browser.FIREFOX:
            self.driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
        elif self.target is Browser.INTERNET_EXPLORER:
            self.driver = webdriver.Ie(IEDriverManager().install())
        elif self.target is Browser.EDGE:
            self.driver = webdriver.Edge(EdgeChromiumDriverManager().install())
        elif self.target is Browser.OPERA:
            self.driver = webdriver.Opera(executable_path=OperaDriverManager().install())
        elif self.target is Browser.SAFARI:
            self.driver = webdriver.Safari()
        self.url(self.capabilities['url'])
        self._resize_screen()

    @wrapper(method_name='Close application')
    def close_app(self):
        self.driver.close()
        return True

    @wrapper(method_name='Reopen application')
    def reopen_app(self):
        self.close_app()
        self.open_app()
        return self.driver is not None

    @wrapper(method_name='Reset application')
    def reset_app(self):
        self.reopen_app()
        return self.driver is not None

    @wrapper(method_name='Refresh page')
    def refresh_page(self):
        self.driver.refresh()
        return self.driver is not None

    @wrapper(method_name='Get text')
    def get_text(self, locator: Locator, dynamic_value=None):
        if self.wait(locator, dynamic_value):
            element = self.driver.find_element(locator.by, locator.value(dynamic_value))
            return element.text if element.text != '' else element.get_attribute("value")

    @wrapper(method_name='Take photo')
    def take_photo(self, locator: Locator = None, dynamic_value=None):
        return False

    @wrapper(method_name='Dropdown select')
    def dropdown_select(self, select_text: str, locator: Locator, dynamic_value=None):
        return False

    def switch_to_frame(self, iframe):
        self.driver.switch_to.frame(iframe)
        return True

    def switch_to_default_content(self):
        self.driver.switch_to.default_content()
        return True

    def _resize_screen(self):
        try:
            self.resize_screen(
                self.capabilities['fullScreen'],
                self.capabilities['width'],
                self.capabilities['height']
            )
        except KeyError:
            self.resize_screen(self.capabilities['fullScreen'])
