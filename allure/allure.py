from allure_commons._allure import attach
from allure_commons.types import AttachmentType

FILE_WEB = """
<environment>

  <parameter>
    <key>Product</key>
    <value>%s</value>
  </parameter>

  <parameter>
    <key>Product Version</key>
    <value>%s</value>
  </parameter>

  <parameter>
    <key>URL</key>
    <value>%s</value>
  </parameter>

  <parameter>
    <key>Platform</key>
    <value>%s</value>
  </parameter>

  <parameter>
    <key>Browser</key>
    <value>%s</value>
  </parameter>

  <parameter>
    <key>Browser Version</key>
    <value>%s</value>
  </parameter>

</environment>
"""


def environment(capabilities, product_version, browser_version):
    data = FILE_WEB % (
        capabilities["product"],
        product_version,
        capabilities["url"],
        capabilities["platformName"],
        capabilities["browserName"],
        browser_version
    )
    # with open(get_project_absolute_path() + 'allure-result/environment.xml', 'w') as file:
    with open('allure-results/environment.xml', 'w') as file:
        file.write(data)


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
