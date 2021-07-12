from enum import Enum
from drivers.mobile.mobile_device import MobileDevice


class Platform(Enum):
    """It is a set of limited and immutable platform names, that are supported by the framework"""

    """Web:
     - Supported OS: Windows/macOS/Linux
     - Maintained by: Selenium"""
    WEB = 'Web'

    """Mobile:
     - Supported OS: Windows/macOS/Linux for Android and macOS for iOS
     - Maintained by: Appium"""
    MOBILE = 'Mobile'

    """Unknown: for unsupported platforms"""
    UNKNOWN = 'Unknown'


def get_platform(platform_name: str):
    """Get the name of a platforms from a set"""
    name = platform_name.lower()
    if name == Platform.WEB.value.lower():
        return Platform.WEB
    elif name == MobileDevice.iOS.value.lower() or name == MobileDevice.ANDROID.value.lower():
        return Platform.MOBILE
    else:
        return Platform.UNKNOWN
