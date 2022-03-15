from time import sleep
from datetime import datetime, timedelta
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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

    DROPDOWN_SELECT: Locator = Locator(
        name='DROPDOWN SELECT',
        by=By.XPATH, value='//*[text()[contains(.,"%s")]]',
        dynamic=True, description='DROPDOWN SELECT', check_opening_page=False
    )

    def __init__(self, capabilities):
        """Capabilities keys:
        main - platformName: str, browserName: str, url: str, fullScreen: str
        not necessary - width: int, height: int"""
        super().__init__(capabilities)
        self.KEYS = ['platformName', 'browserName', 'url', 'fullScreen']
        self.check_params()

    @wrapper(method_name='Open Application')
    def open_application(self):
        if self.target is Browser.CHROME:
            self.driver = self._setup_chrome_driver()
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

    @wrapper(method_name='Close Application')
    def close_application(self):
        self.driver.close()

    @wrapper(method_name='Reopen Application')
    def reopen_application(self):
        self.close_application()
        self.open_application()

    @wrapper(method_name='Reset Application')
    def reset_application(self):
        self.reopen_application()

    @wrapper(method_name='Explicit Wait')
    def explicit_wait(self, locator: Locator, dynamic_value=None):
        t_start = datetime.now()
        t_end = t_start + timedelta(seconds=self.TIME_TO_WAIT)
        while True:
            if datetime.now() >= t_end:
                break
            try:
                WebDriverWait(self.driver, self.TIME_TO_WAIT).until(
                    EC.presence_of_element_located(
                        (locator.by, locator.value(dynamic_value))
                    )
                )
                element = self.driver.find_element(locator.by, locator.value(dynamic_value))
                if element.is_displayed():
                    return element
            except:
                continue
        return None

    @wrapper(method_name='Implicit Wait')
    def implicit_wait(self, locator: Locator, dynamic_value=None):
        t_start = datetime.now()
        t_end = t_start + timedelta(seconds=self.TIME_TO_WAIT)
        self.driver.implicitly_wait(self.TIME_TO_WAIT)
        while True:
            if datetime.now() >= t_end:
                break
            try:
                WebDriverWait(self.driver, self.TIME_TO_WAIT).until(
                    EC.presence_of_element_located((locator.by, locator.value(dynamic_value)))
                )
                element = self.driver.find_element(locator.by, locator.value(dynamic_value))
                if element.is_displayed():
                    return element
            except:
                continue
            sleep(1)
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
        self.item_search(locator, dynamic_value).click()

    @wrapper(method_name='Clear')
    def clear(self, locator: Locator, dynamic_value=None):
        element = self.item_search(locator, dynamic_value)
        self._clear_field(element)

    @wrapper(method_name='Input')
    def input(self, locator: Locator, text: str, slow=False, dynamic_value=None):
        element = self.item_search(locator, dynamic_value)
        self._input_text(element, text, slow)

    @wrapper(method_name='Clean Input')
    def clean_input(self, locator: Locator, text: str, slow=False, dynamic_value=None):
        element = self.item_search(locator, dynamic_value)
        self._clear_field(element)
        self._input_text(element, text, slow)

    @wrapper(method_name='Text')
    def text(self, locator: Locator, dynamic_value=None):
        element = self.item_search(locator, dynamic_value)
        return self._get_text(element)

    @wrapper(method_name='Scroll Up')
    def scroll_up(self):
        self.driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)

    @wrapper(method_name='Scroll Down')
    def scroll_down(self):
        self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

    @wrapper(method_name='Dropdown Select')
    def dropdown_select(self, select_text: str, locator: Locator, dynamic_value=None):
        element = self.item_search(locator, dynamic_value)
        element.click()
        element2 = self.item_search(self.DROPDOWN_SELECT, select_text)
        element2.click()

    @wrapper(method_name='URL')
    def url(self, url: str):
        self.driver.get(url)

    @wrapper(method_name='Resize Screen')
    def resize_screen(self, full: bool = True, width=1024, height=768):
        if full:
            self.driver.maximize_window()
        else:
            self.set_window_position(0, 0)
            self.driver.set_window_size(width, height)

    @wrapper(method_name='Set Image')
    def set_image(self, locator: Locator, file: str):
        element = self.driver.find_element(locator.by, locator.value())
        element.send_keys(file)

    @wrapper(method_name='Switch To Frame')
    def switch_to_frame(self, iframe):
        self.driver.switch_to.frame(self.item_search(Locator(
            name='Switch Frame',
            by=By.XPATH, value='(//iframe)[%s]' % iframe,
            dynamic=False, description='Switch Frame', check_opening_page=False
        )))

    @wrapper(method_name='Switch To Default Content')
    def switch_to_default_content(self):
        self.driver.switch_to.default_content()

    @wrapper(method_name='Set Window Position')
    def set_window_position(self, x: int, y: int):
        self.driver.set_window_position(x, y)

    @wrapper(method_name='Refresh Page')
    def refresh_page(self):
        self.driver.refresh()

    @wrapper(method_name='Orientation')
    def orientation(self, landscape: bool = False):
        self._skip_method('orientation')

    @wrapper(method_name='Tap')
    def tap(self, x, y, seconds=1, element=None):
        self._skip_method('tap')

    @wrapper(method_name='Take Photo')
    def take_photo(self, locator: Locator = None, dynamic_value=None):
        self._skip_method('take_photo')

    """Private methods"""

    @staticmethod
    def _get_text(element):
        return element.text if element.text != '' else element.get_attribute("value")

    def _clear_field(self, element):
        element.send_keys(''.join(map(str, ['\b' for i in self._get_text(element)])))

    @staticmethod
    def _input_text(element, text: str, slow=False):
        index = 0
        pause = [3, 5, 7]
        for char in text:
            if index in pause and slow:
                sleep(1)
            element.send_keys(char)
            index += 1

    def _resize_screen(self):
        try:
            self.resize_screen(
                self.capabilities['fullScreen'],
                self.capabilities['width'],
                self.capabilities['height']
            )
        except KeyError:
            self.resize_screen(self.capabilities['fullScreen'])

    def _setup_chrome_driver(self):
        if 'options' in self.capabilities.keys():
            if self.capabilities["options"]:
                chrome_options = Options()
                chrome_options.add_argument("--headless")
                chrome_options.add_argument("--no-sandbox")
                chrome_options.add_argument("--disable-gpu")
                return webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
        return webdriver.Chrome(ChromeDriverManager().install())
