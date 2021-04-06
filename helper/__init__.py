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

    @staticmethod
    def message(message, name='Message'):
        allure.attach(message, name=name, attachment_type=allure.attachment_type.TEXT)

    def error_message(self, message, screen_and_source=True, hard_assert=True):
        allure.attach(message, name='Error message', attachment_type=allure.attachment_type.TEXT)
        if screen_and_source:
            self.do_screenshot('Error Screenshot')
            allure.attach(self._driver.source(), name='Error Page source', attachment_type=allure.attachment_type.TEXT)
        if hard_assert:
            raise Exception(message)

    def sleep(self, seconds=10):
        self.message("Sleep: %s seconds" % seconds, "Sleep")
        time.sleep(seconds)

    def hard_assert_true(self, result, message):
        if result is False:
            self.error_message(message)

    def hard_assert_false(self, result, message):
        if result is True:
            self.error_message(message)

    def get_first_name(self, gender=None):
        first_name = names.get_first_name(
            gender=gender if gender is not None else self.get_random_item(['male', 'female'])
        )
        self.message("First Name: %s" % first_name, "Create new random first name")
        return first_name

    def get_last_name(self):
        last_name = names.get_last_name()
        self.message("Last Name: %s" % last_name, "Create new random last name")
        return last_name

    def get_full_name(self, gender=None):
        full_name = names.get_full_name(
            gender=gender if gender is not None else self.get_random_item(['male', 'female'])
        )
        self.message("Full Name: %s" % full_name, "Create new random full name")
        return full_name

    def get_contact_number(self, code=37525, size=7):
        range_start = 10 ** (size - 1)
        range_end = (10 ** size) - 1
        contact_number = str(code) + str(randint(range_start, range_end))
        self.message("Contact Number: %s" % contact_number, "Get random contact number")
        return contact_number

    def get_random_number(self, length):
        range_start = 10 ** (length - 1)
        range_end = (10 ** length) - 1
        random_number = randint(range_start, range_end)
        self.message("Random Number: %s" % random_number, "Get random number by %s length" % length)
        return random_number

    def get_random_account_data(self, company, password='Mm11111111', code='%H%M%S.%d%m.%Y'):
        account = {
            "email": "%s%s@gmail.com" % (company, datetime.now().strftime(code)),
            "password": "%s" % password
        }
        self.message("Account: " % account, "Create random Account")
        return account

    def get_random_item(self, array):
        item = array[randint(0, len(array) - 1)]
        self.message("Item: %s" % item, "Get random item from list: %s" % array)
        return item


test_helper = TestHelper()
