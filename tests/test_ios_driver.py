import unittest
from driver import Driver, Platform, ANDROID_CAPABILITIES, PlatformNotSupportedError


class TestAndroidDriver(unittest.TestCase):

    def test_init_driver_passes(self):
        capabilities = {
            "deviceName": "Ivan’s iPhone",
            "platformName": "iOS",
            "platformVersion": "14.2",
            "udid": "00008020-001A51042EBB002E",
            "automationName": "XCUITest",
            "app": "test.ipa",
            "noReset": True,
            "appium": "http://localhost:4723/wd/hub",
            "fullReset": False
        }
        driver = Driver(capabilities)
        self.assertEqual(type(driver), Driver, 'New driver is not Driver class.')
        self.assertEqual(driver.platform(), Platform.iOS, 'New driver is not for Web platform.')

    def test_init_driver_platform_name_key_fails(self):
        capabilities = {
            "deviceName": "Ivan’s iPhone",
            "platformVersion": "14.2",
            "udid": "00008020-001A51042EBB002E",
            "automationName": "XCUITest",
            "app": "test.ipa",
            "noReset": True,
            "appium": "http://localhost:4723/wd/hub"
        }
        msg = 'Your capabilities have not "platformName" key. Please Fix it.'
        with self.assertRaisesRegex(KeyError, msg):
            Driver(capabilities)

    def test_init_driver_platform_name_unknown_fails(self):
        capabilities = {
            "deviceName": "Ivan’s iPhone",
            "platformName": "iOS22",
            "platformVersion": "14.2",
            "udid": "00008020-001A51042EBB002E",
            "automationName": "XCUITest",
            "app": "test.ipa",
            "noReset": True,
            "appium": "http://localhost:4723/wd/hub"
        }
        msg = 'Your iOS22 platform is not supported.'
        with self.assertRaisesRegex(PlatformNotSupportedError, msg):
            Driver(capabilities)

    def test_init_driver_udid_fails(self):
        capabilities = {
            "deviceName": "Ivan’s iPhone",
            "platformName": "iOS",
            "platformVersion": "14.2",
            "automationName": "XCUITest",
            "app": "test.ipa",
            "noReset": True,
            "appium": "http://localhost:4723/wd/hub"
        }
        msg = '"udid" key is not present. Please Fix it.'
        with self.assertRaisesRegex(KeyError, msg):
            Driver(capabilities)

    def test_init_driver_device_name_fails(self):
        capabilities = {
            "platformName": "iOS",
            "platformVersion": "14.2",
            "udid": "00008020-001A51042EBB002E",
            "automationName": "XCUITest",
            "app": "test.ipa",
            "noReset": True,
            "appium": "http://localhost:4723/wd/hub"
        }
        msg = '"deviceName" key is not present. Please Fix it.'
        with self.assertRaisesRegex(KeyError, msg):
            Driver(capabilities)

    def test_init_driver_platform_version_fails(self):
        capabilities = {
            "deviceName": "Ivan’s iPhone",
            "platformName": "iOS",
            "udid": "00008020-001A51042EBB002E",
            "automationName": "XCUITest",
            "app": "test.ipa",
            "noReset": True,
            "appium": "http://localhost:4723/wd/hub"
        }
        msg = '"platformVersion" key is not present. Please Fix it.'
        with self.assertRaisesRegex(KeyError, msg):
            Driver(capabilities)

    def test_init_driver_app_fails(self):
        capabilities = {
            "deviceName": "Ivan’s iPhone",
            "platformName": "iOS",
            "platformVersion": "14.2",
            "udid": "00008020-001A51042EBB002E",
            "automationName": "XCUITest",
            "noReset": True,
            "appium": "http://localhost:4723/wd/hub"
        }
        msg = '"app" key is not present. Please Fix it.'
        with self.assertRaisesRegex(KeyError, msg):
            Driver(capabilities)

    def test_init_no_reset_fails(self):
        capabilities = {
            "deviceName": "Ivan’s iPhone",
            "platformName": "iOS",
            "platformVersion": "14.2",
            "udid": "00008020-001A51042EBB002E",
            "automationName": "XCUITest",
            "app": "test.ipa",
            "appium": "http://localhost:4723/wd/hub"
        }
        msg = '"noReset" key is not present. Please Fix it.'
        with self.assertRaisesRegex(KeyError, msg):
            Driver(capabilities)

    def test_init_automation_name_fails(self):
        capabilities = {
            "deviceName": "Ivan’s iPhone",
            "platformName": "iOS",
            "platformVersion": "14.2",
            "udid": "00008020-001A51042EBB002E",
            "app": "test.ipa",
            "noReset": True,
            "appium": "http://localhost:4723/wd/hub"
        }
        msg = '"automationName" key is not present. Please Fix it.'
        with self.assertRaisesRegex(KeyError, msg):
            Driver(capabilities)

    def test_init_appium_fails(self):
        capabilities = {
            "deviceName": "Ivan’s iPhone",
            "platformName": "iOS",
            "platformVersion": "14.2",
            "udid": "00008020-001A51042EBB002E",
            "automationName": "XCUITest",
            "app": "test.ipa",
            "noReset": True
        }
        msg = '"appium" key is not present. Please Fix it.'
        with self.assertRaisesRegex(KeyError, msg):
            Driver(capabilities)


if __name__ == '__main__':
    unittest.main()
