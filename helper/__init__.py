import time
from random import randint
from datetime import datetime
import allure
from allure_commons.types import AttachmentType
import names


class TestHelper(object):
    _driver = None

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(TestHelper, cls).__new__(cls)
        return cls.instance

    def update(self, driver):
        self._driver = driver

    def do_screenshot(self, name):
        allure.attach(
            self._driver.get_screenshot_as_png(),
            name=name,
            attachment_type=AttachmentType.PNG
        )

    def message(self, message, name='Message'):
        allure.attach(message, name=name, attachment_type=allure.attachment_type.TEXT)

    def error_message(self, message, screen_and_source=True, hard_assert=True):
        allure.attach(message, name='Error message', attachment_type=allure.attachment_type.TEXT)
        if screen_and_source:
            self.do_screenshot('Error Screenshot')
            allure.attach(self._driver.source(), name='Error Page source', attachment_type=allure.attachment_type.TEXT)
        if hard_assert:
            raise Exception(message)

    def sleep(self, seconds=10):
        time.sleep(seconds)

    def hard_assert_true(self, result, message):
        if result is False:
            self.error_message(message)

    def hard_assert_false(self, result, message):
        if result is True:
            self.error_message(message)

    def get_first_name(self):
        return names.get_first_name()

    def get_last_name(self):
        return names.get_last_name()

    def get_contact_number(self, code=37525, size=7):
        range_start = 10 ** (size - 1)
        range_end = (10 ** size) - 1
        return str(code) + str(randint(range_start, range_end))

    def random_number(self, length):
        range_start = 10 ** (length - 1)
        range_end = (10 ** length) - 1
        return randint(range_start, range_end)

    def random_account_data(self, company, password='Mm11111111', code='%H%M%S.%d%m.%Y'):
        return {
            "email": "%s%s@gmail.com" % (company, datetime.now().strftime(code)),
            "password": "%s" % password
        }


test_helper = TestHelper()


print(test_helper.random_account_data('GradGab'))