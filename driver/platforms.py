from enum import Enum


class Platform(Enum):
    Web = 'Web'
    Android = 'Android'
    iOS = 'iOS'
    UNKNOWN = 'Unknown'


def setup_platform(platform_name):
    platform = platform_name.lower()
    if platform == 'web':
        return Platform.Web
    elif platform == 'android':
        return Platform.Android
    elif platform == 'ios':
        return Platform.iOS
    else:
        return Platform.UNKNOWN
