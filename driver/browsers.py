from enum import Enum


class Browser(Enum):
    Chrome = 'Chrome'
    UNKNOWN = 'Unknown'


def setup_browser(platform_name):
    platform = platform_name.lower()
    if platform == 'chrome':
        return Browser.Chrome
    else:
        return Browser.UNKNOWN
