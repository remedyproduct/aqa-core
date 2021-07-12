from allure_commons._allure import attach
from allure_commons.types import AttachmentType


def screenshot(screenshot_as_png, name='Screenshot'):
    attach(
        screenshot_as_png,
        name=name,
        attachment_type=AttachmentType.PNG
    )


def message(msg, name='Message'):
    attach(
        msg,
        name=name,
        attachment_type=AttachmentType.TEXT
    )


def error_message(msg, driver=None, png: bool = True, page_source: bool = True):
    message(msg, name='Error message')
    if driver is not None:
        if png:
            screenshot(driver.get_screenshot_as_png(), 'Error Screenshot')
        if page_source:
            message(driver.get_page_source(), 'Error Page Source')
