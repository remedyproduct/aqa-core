from enum import Enum


class MobileDevice(Enum):
    """It is a set of limited and immutable mobile names, that are supported by the framework"""

    """Android:
     - Supported OS: Windows/macOS/Linux
     - Maintained by: Google"""
    ANDROID = 'Android'

    """iOS:
     - Supported OS: macOS EI Capitan and newer
     - Maintained by: Apple"""
    iOS = 'iOS'

    """Unknown: for unsupported mobile platforms"""
    UNKNOWN = 'Unknown'


def get_mobile_device(mobile_device_name: str):
    """Get the name of a mobile platforms from a set"""
    name = mobile_device_name.lower()
    if name == MobileDevice.ANDROID.value.lower():
        return MobileDevice.ANDROID
    elif name == MobileDevice.iOS.value.lower():
        return MobileDevice.iOS
    else:
        return MobileDevice.UNKNOWN
