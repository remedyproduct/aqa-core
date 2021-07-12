from drivers.mobile.driver import MobileDriver
from drivers.mobile.mobile_device import get_mobile_device, MobileDevice
from drivers.platform.error import PlatformError
from drivers.platform.platforms import get_platform, Platform
from drivers.web.driver import WebDriver


def get_driver(capabilities):
    try:
        platform = get_mobile_device(capabilities['platformName'])
        if platform is MobileDevice.iOS or platform is MobileDevice.ANDROID:
            return MobileDriver(capabilities)
        platform = get_platform(capabilities['platformName'])
        if platform is Platform.WEB:
            return WebDriver(capabilities)
    except KeyError:
        raise PlatformError("Could not find the 'platformName' key in the file")
