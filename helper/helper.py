import time
from random import randint
from datetime import datetime
import names
from allure.allure import *


def sleep(seconds=10):
    msg = 'Sleep %s seconds' % seconds
    message(msg, msg)
    time.sleep(seconds)


def hard_assert_true(result, msg, driver=None, png: bool = True, page_source: bool = True):
    if result is False:
        error_message(msg, driver, png, page_source)
        assert False, msg


def hard_assert_false(result, msg, driver=None, png: bool = True, page_source: bool = True):
    if result is True:
        error_message(msg, driver, png, page_source)
        assert False, msg


def get_random_item(array):
    item = array[randint(0, len(array) - 1)]
    message("Item: %s" % item, "Get random item from list: %s" % array)
    return item


def get_first_name(gender=None):
    first_name = names.get_first_name(
        gender=gender if gender is not None else get_random_item(['male', 'female'])
    )
    message("First Name: %s" % first_name, "Create new random first name")
    return first_name


def get_last_name():
    last_name = names.get_last_name()
    message("Last Name: %s" % last_name, "Create new random last name")
    return last_name


def get_full_name(gender=None):
    full_name = names.get_full_name(
        gender=gender if gender is not None else get_random_item(['male', 'female'])
    )
    message("Full Name: %s" % full_name, "Create new random full name")
    return full_name


def get_contact_number(code=37525, size=7):
    range_start = 10 ** (size - 1)
    range_end = (10 ** size) - 1
    contact_number = str(code) + str(randint(range_start, range_end))
    message("Contact Number: %s" % contact_number, "Get random contact number")
    return contact_number


def get_random_number(length):
    range_start = 10 ** (length - 1)
    range_end = (10 ** length) - 1
    random_number = randint(range_start, range_end)
    message("Random Number: %s" % random_number, "Get random number by %s length" % length)
    return random_number


def get_random_account_data(company, password='Mm11111111', code='%H%M%S.%d%m.%Y'):
    account = {
        "email": "%s%s@gmail.com" % (company, datetime.now().strftime(code)),
        "password": "%s" % password
    }
    message("Account: %s" % account, "Create random Account")
    return account
