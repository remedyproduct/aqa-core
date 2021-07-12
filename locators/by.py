from selenium.webdriver.common.by import By


def get_by(locator_by: str):
    """Get the type of a ui element from a set"""
    by = locator_by.lower()
    if by == 'id':
        return By.ID
    elif by == 'xpath':
        return By.XPATH
    elif by == 'link_text':
        return By.LINK_TEXT
    elif by == 'partial_link_text':
        return By.PARTIAL_LINK_TEXT
    elif by == 'name':
        return By.NAME
    elif by == 'tag':
        return By.TAG_NAME
    elif by == 'class':
        return By.CLASS_NAME
    elif by == 'css':
        return By.CSS_SELECTOR
    else:
        return None
