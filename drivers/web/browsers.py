from enum import Enum


class Browser(Enum):
    """It is a set of limited and immutable web browser names, that are supported by the framework"""

    """Chromium/Chrome:
     - Supported OS: Windows/macOS/Linux
     - Maintained by: Google"""
    CHROME = 'Chromium/Chrome'

    """Firefox:
     - Supported OS: Windows/macOS/Linux
     - Maintained by: Mozilla"""
    FIREFOX = 'Firefox'

    """Edge:
     - Supported OS: Windows 10
     - Maintained by: Microsoft"""
    EDGE = 'Edge'

    """Internet Explorer:
     - Supported OS: Windows
     - Maintained by: Selenium Project"""
    INTERNET_EXPLORER = 'Internet Explorer'

    """Safari:
     - Supported OS: macOS EI Capitan and newer
     - Maintained by: Apple"""
    SAFARI = 'Safari'

    """Opera:
    - Supported OS: Windows/macOS/Linux
    - Maintained by: Opera"""
    OPERA = 'Opera'

    """Unknown: for unsupported web browsers"""
    UNKNOWN = 'Unknown'


def get_web_browser(browser_name: str):
    """Get the name of a web browser from a set"""
    name = browser_name.lower()
    if name == 'chromium' or name == 'chrome' or name == 'chromium/chrome':
        return Browser.CHROME
    elif name == Browser.FIREFOX.value.lower():
        return Browser.FIREFOX
    elif name == Browser.EDGE.value.lower():
        return Browser.EDGE
    elif name == Browser.INTERNET_EXPLORER.value.lower():
        return Browser.INTERNET_EXPLORER
    elif name == Browser.SAFARI.value.lower():
        return Browser.SAFARI
    elif name == Browser.OPERA.value.lower():
        return Browser.OPERA
    else:
        return Browser.UNKNOWN
