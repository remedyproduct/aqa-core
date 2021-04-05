import json
import unittest
from selenium.webdriver.common.by import By
from driver import Platform
from locator import Locator
from page import pages, PageNotContainLocatorError


class TestPage(unittest.TestCase):

    def test_pages_update_passes(self):
        platform = Platform.Web
        with open('resources/test_pages_passes.json') as pages_file:
            data = json.load(pages_file)['pages']
            pages.update(platform, data)
        locator = pages.get_locator('Login', 'Username/Email')
        self.assertEqual(type(locator), Locator, 'New locator is not Locator class.')
        self.assertEqual(locator.name(), 'Username/Email', 'Name of the new locator is incorrect.')
        self.assertEqual(locator.value(), 'username', 'Value of the new locator is incorrect.')
        self.assertEqual(locator.by(), By.NAME, 'By of the new locator is incorrect.')
        self.assertEqual(
            locator.description(),
            'Username/Email input field', 'Description of the new locator is incorrect.'
        )
        self.assertFalse(locator.is_dynamic(), 'Dynamic value of the new locator is incorrect.')

    def test_pages_update_fails(self):
        platform = Platform.Web
        with open('resources/test_pages_fails.json') as pages_file:
            data = json.load(pages_file)['pages']
        with self.assertRaisesRegex(KeyError, platform.value):
            pages.update(platform, data)

    def test_pages_missed_locator_fails(self):
        platform = Platform.Web
        with open('resources/test_pages_passes.json') as pages_file:
            data = json.load(pages_file)['pages']
            pages.update(platform, data)
        locator_name = 'Email/Username'
        page_name = 'Login'
        pages.update(platform, data)
        msg = "Can't find the Email/Username for Login page, platform - Web."
        with self.assertRaisesRegex(PageNotContainLocatorError, msg):
            pages.get_locator(page_name, locator_name)


if __name__ == '__main__':
    unittest.main()
