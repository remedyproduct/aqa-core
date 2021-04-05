import unittest
from driver import Driver, Platform, ANDROID_CAPABILITIES, PlatformNotSupportedError


class TestAndroidDriver(unittest.TestCase):

    def test_init_driver_passes(self):
        capabilities = {
            "platformName": "Android",
            "udid": "c81c0db9",
            "appWaitActivity": "*",
            "deviceName": "V2023",
            "platformVersion": "10",
            "app": "test.apk",
            "noReset": True,
            "fullReset": False,
            "appium": "http://localhost:4723/wd/hub"
        }
        driver = Driver(capabilities)
        self.assertEqual(type(driver), Driver, 'New driver is not Driver class.')
        self.assertEqual(driver.platform(), Platform.Android, 'New driver is not for Web platform.')
        self.assertTrue(driver.verify_mobile_platform(), 'No')

    def test_init_driver_platform_name_key_fails(self):
        capabilities = {
            "udid": "c81c0db9",
            "appWaitActivity": "*",
            "deviceName": "V2023",
            "platformVersion": "10",
            "app": "test.apk",
            "noReset": False,
            "appium": "http://localhost:4723/wd/hub"
        }
        msg = 'Your capabilities have not "platformName" key. Please Fix it.'
        with self.assertRaisesRegex(KeyError, msg):
            Driver(capabilities)

    def test_init_driver_platform_name_unknown_fails(self):
        capabilities = {
            "platformName": "Android22",
            "udid": "c81c0db9",
            "appWaitActivity": "*",
            "deviceName": "V2023",
            "platformVersion": "10",
            "app": "test.apk",
            "noReset": False,
            "appium": "http://localhost:4723/wd/hub"
        }
        msg = 'Your Android22 platform is not supported.'
        with self.assertRaisesRegex(PlatformNotSupportedError, msg):
            Driver(capabilities)

    def test_init_driver_udid_fails(self):
        capabilities = {
            "platformName": "Android",
            "appWaitActivity": "*",
            "deviceName": "V2023",
            "platformVersion": "10",
            "app": "test.apk",
            "noReset": False,
            "appium": "http://localhost:4723/wd/hub"
        }
        msg = '"udid" key is not present. Please Fix it.'
        with self.assertRaisesRegex(KeyError, msg):
            Driver(capabilities)

    def test_init_driver_device_name_fails(self):
        capabilities = {
            "platformName": "Android",
            "udid": "c81c0db9",
            "appWaitActivity": "*",
            "platformVersion": "10",
            "app": "test.apk",
            "noReset": False,
            "appium": "http://localhost:4723/wd/hub"
        }
        msg = '"deviceName" key is not present. Please Fix it.'
        with self.assertRaisesRegex(KeyError, msg):
            Driver(capabilities)

    def test_init_driver_platform_version_fails(self):
        capabilities = {
            "platformName": "Android",
            "udid": "c81c0db9",
            "appWaitActivity": "*",
            "deviceName": "V2023",
            "app": "test.apk",
            "noReset": False,
            "appium": "http://localhost:4723/wd/hub"
        }
        msg = '"platformVersion" key is not present. Please Fix it.'
        with self.assertRaisesRegex(KeyError, msg):
            Driver(capabilities)

    def test_init_driver_app_fails(self):
        capabilities = {
            "platformName": "Android",
            "udid": "c81c0db9",
            "appWaitActivity": "*",
            "deviceName": "V2023",
            "platformVersion": "10",
            "noReset": False,
            "appium": "http://localhost:4723/wd/hub"
        }
        msg = '"app" key is not present. Please Fix it.'
        with self.assertRaisesRegex(KeyError, msg):
            Driver(capabilities)

    def test_init_no_reset_fails(self):
        capabilities = {
            "platformName": "Android",
            "udid": "c81c0db9",
            "appWaitActivity": "*",
            "deviceName": "V2023",
            "platformVersion": "10",
            "app": "test.apk",
            "appium": "http://localhost:4723/wd/hub"
        }
        msg = '"noReset" key is not present. Please Fix it.'
        with self.assertRaisesRegex(KeyError, msg):
            Driver(capabilities)

    def test_init_app_wait_activity_fails(self):
        capabilities = {
            "platformName": "Android",
            "udid": "c81c0db9",
            "deviceName": "V2023",
            "platformVersion": "10",
            "app": "test.apk",
            "noReset": False,
            "appium": "http://localhost:4723/wd/hub"
        }
        msg = '"appWaitActivity" key is not present. Please Fix it.'
        with self.assertRaisesRegex(KeyError, msg):
            Driver(capabilities)

    def test_init_appium_fails(self):
        capabilities = {
            "platformName": "Android",
            "udid": "c81c0db9",
            "appWaitActivity": "*",
            "deviceName": "V2023",
            "platformVersion": "10",
            "app": "360.apk",
            "noReset": False
        }
        msg = '"appium" key is not present. Please Fix it.'
        with self.assertRaisesRegex(KeyError, msg):
            Driver(capabilities)


if __name__ == '__main__':
    unittest.main()
