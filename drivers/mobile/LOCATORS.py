from locators.locator import Locator
from selenium.webdriver.common.by import By

# FOR TAKE PHOTO
# ANDROID
ANDROID_SELECT_TAKE_PHOTO = Locator(
    name='ANDROID SELECT TAKE PHOTO TEXT',
    by=By.XPATH, value='//android.widget.TextView[@text="Take Photo…"]',
    dynamic=False, description='ANDROID SELECT TAKE PHOTO TEXT', check_opening_page=False
)
ANDROID_TAKE_PHOTO_1 = Locator(
    name='ANDROID TAKE PHOTO 1',
    by=By.XPATH, value='(//GLButton[@content-desc="NONE"])[2]',
    dynamic=False, description='ANDROID TAKE PHOTO 1', check_opening_page=False
)
ANDROID_TAKE_PHOTO_2 = Locator(
    name='ANDROID TAKE PHOTO 2',
    by=By.XPATH, value='//android.widget.ImageView[@content-desc="Shutter"]',
    dynamic=False, description='ANDROID TAKE PHOTO 2', check_opening_page=False
)
ANDROID_TAKE_PHOTO_3 = Locator(
    name='ANDROID TAKE PHOTO 3',
    by=By.XPATH, value='//android.view.View[@content-desc="Shutter button"]',
    dynamic=False, description='ANDROID TAKE PHOTO 3', check_opening_page=False
)
ANDROID_COMPLETE_PHOTO_1 = Locator(
    name='ANDROID COMPLETE PHOTO 1',
    by=By.XPATH, value='//*[@text="OK"]',
    dynamic=False, description='ANDROID COMPLETE PHOTO 1', check_opening_page=False
)
ANDROID_COMPLETE_PHOTO_2 = Locator(
    name='ANDROID COMPLETE PHOTO 2',
    by=By.XPATH, value='//android.widget.ImageView[@content-desc="Done"]',
    dynamic=False, description='ANDROID COMPLETE PHOTO 2', check_opening_page=False
)
# iOS
iOS_SELECT_TAKE_PHOTO = Locator(
    name='iOS SELECT TAKE PHOTO TEXT',
    by=By.XPATH, value='//XCUIElementTypeButton[@name="Take Photo…"]',
    dynamic=False, description='iOS SELECT TAKE PHOTO TEXT', check_opening_page=False
)
iOS_TAKE_PHOTO = Locator(
    name='iOS TAKE PHOTO',
    by=By.XPATH, value='//XCUIElementTypeButton[@name="PhotoCapture"]',
    dynamic=False, description='iOS TAKE PHOTO 1', check_opening_page=False
)
iOS_COMPLETE_PHOTO = Locator(
    name='iOS COMPLETE PHOTO',
    by=By.XPATH, value='//XCUIElementTypeStaticText[@name="Use Photo"]',
    dynamic=False, description='iOS COMPLETE PHOTO', check_opening_page=False
)
