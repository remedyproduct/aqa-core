import unittest
from driver import Driver, Platform, PlatformNotSupportedError


class TestWebDriver(unittest.TestCase):

    def test_init_driver_passes(self):
        capabilities = {
            "platformName": "Web",
            "url": "https://www.google.com/",
            "browserName": "Chrome",
            "fullScreen": True
        }
        driver = Driver(capabilities)
        self.assertEqual(type(driver), Driver, 'New driver is not Driver class.')
        self.assertEqual(driver.platform(), Platform.Web, 'New driver is not for Web platform.')

    def test_init_driver_platform_name_fails(self):
        capabilities = {
            "url": "https://www.google.com/",
            "browserName": "Chrome",
            "fullScreen": True
        }
        msg = 'Your capabilities have not "platformName" key. Please Fix it.'
        with self.assertRaisesRegex(KeyError, msg):
            Driver(capabilities)

    def test_init_driver_platform_name_unknown_fails(self):
        capabilities = {
            "platformName": "Web22",
            "url": "https://www.google.com/",
            "browserName": "Chrome",
            "fullScreen": True
        }
        msg = 'Your Web22 platform is not supported.'
        with self.assertRaisesRegex(PlatformNotSupportedError, msg):
            Driver(capabilities)

    def test_init_driver_url_fails(self):
        capabilities = {
            "platformName": "Web",
            "browserName": "Chrome",
            "fullScreen": True
        }
        msg = '"url" key is not present. Please Fix it.'
        with self.assertRaisesRegex(Exception, msg):
            Driver(capabilities)

    def test_init_driver_browser_name_fails(self):
        capabilities = {
            "platformName": "Web",
            "url": "https://www.google.com/",
            "fullScreen": True
        }
        msg = '"browserName" key is not present. Please Fix it.'
        with self.assertRaisesRegex(Exception, msg):
            Driver(capabilities)

    def test_init_driver_full_screen_fails(self):
        capabilities = {
            "platformName": "Web",
            "url": "https://www.google.com/",
            "browserName": "Chrome"
        }
        msg = '"fullScreen" key is not present. Please Fix it.'
        with self.assertRaisesRegex(Exception, msg):
            Driver(capabilities)


if __name__ == '__main__':
    unittest.main()
