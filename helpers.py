import logging
import os
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.action_chains import ActionChains


def clickElement(page_element, xpath_to_element, is_download=False):
    if is_download: logging.info("Starting download")
    ActionChains(page_element).click(
        page_element.find_element_by_xpath(xpath_to_element)
    ).perform()
    if is_download: logging.info("Download finished")
    
def getNewestFilePath(path):
    files = os.listdir(path)
    paths = [os.path.join(path, basename) for basename in files]
    return max(paths, key=os.path.getmtime)