import unittest

from selenium.webdriver.common.by import By

from locator import create_locator, Locator, LocatorDynamicValueError, LocatorError


class TestLocator(unittest.TestCase):

    def test_init_locator_passes(self):
        name = 'Login button'
        by = 'Id'
        value = 'login'
        dynamic = False
        description = '"Login button" on "Login" page'
        locator = create_locator(name, by, value, dynamic, description)
        self.assertEqual(type(locator), Locator, 'New locator is not Locator class.')
        self.assertEqual(locator.name(), name, 'New locator name is not valid.')
        self.assertEqual(locator.value(), value, 'New locator value is not valid.')
        self.assertFalse(locator.is_dynamic(), 'New locator dynamic is not False.')
        self.assertTrue(locator.value_not_empty(), 'New locator value is empty.')
        self.assertEqual(locator.by(), By.ID, 'New locator by is not valid.')
        self.assertEqual(locator.description(), description, 'New locator by is not valid.')

    def test_init_locator_value_fails(self):
        name = 'Login button'
        by = 'Id'
        value = 'login'
        dynamic = True
        description = '"Login button" on "Login" page'
        locator = create_locator(name, by, value, dynamic, description)
        self.assertTrue(locator.is_dynamic(), 'New locator dynamic is not True.')
        msg = 'You can\'t use %s locator, because it dynamic. Please add dynamic value.' % name
        with self.assertRaisesRegex(LocatorDynamicValueError, msg):
            locator.value()

    def test_init_locator_value_is_not_empty_fails(self):
        name = 'Login button'
        by = 'Id'
        value = ''
        dynamic = False
        description = '"Login button" on "Login" page'
        locator = create_locator(name, by, value, dynamic, description)
        self.assertFalse(locator.is_dynamic(), 'New locator dynamic is not False.')
        msg = "You can't use the locator Login button, because this Value is empty."
        with self.assertRaisesRegex(LocatorError, msg):
            locator.value()

    def test_init_locator_by_is_not_empty_fails(self):
        name = 'Login button'
        by = ''
        value = 'login'
        dynamic = False
        description = '"Login button" on "Login" page'
        locator = create_locator(name, by, value, dynamic, description)
        self.assertFalse(locator.is_dynamic(), 'New locator dynamic is not False.')
        msg = "You can't use the locator Login button, because this By is empty."
        with self.assertRaisesRegex(LocatorError, msg):
            locator.value()


if __name__ == '__main__':
    unittest.main()
