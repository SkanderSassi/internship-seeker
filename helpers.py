import logging
import os
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def click_element(page_element, xpath_to_element, is_download=False):
    if is_download:
        logging.info("Starting download")
    ActionChains(page_element).click(
        page_element.find_element_by_xpath(xpath_to_element)
    ).perform()
    if is_download:
        logging.info("Download finished")


def get_pdf(browser, download_button_path):

    WebDriverWait(browser, 20).until(
        EC.presence_of_element_located((By.XPATH, "//*/iframe"))
    )
    
    iframe = browser.find_element_by_xpath("//*/p/iframe")
    window_id_old = browser.current_window_handle  # save old id to go back to it
    link = iframe.get_attribute("src")
    open_new_tab(browser, link.replace("preview", "view"), window_id_old + "_2") # to go directly to download page
    browser.switch_to.window(browser.window_handles[-1])
    WebDriverWait(browser, 20).until(
        EC.presence_of_element_located((By.XPATH, f"{download_button_path}"))
    )
    logging.info("Downloading pdf")
    click_element(
        browser, download_button_path, is_download=True
    )  # Download from drive page
    logging.info("Finished downloading")
    logging.info("Changing to old tab")
    browser.close()
    browser.switch_to.window(window_id_old)


def get_newest_file_path(path):
    files = os.listdir(path)
    paths = [os.path.join(path, basename) for basename in files]
    return max(paths, key=os.path.getmtime)


def open_new_tab(browser, url, tab_id):
    logging.info("Opening new tab")
    browser.execute_script(
        f"window.open('{url}'),'job{tab_id}'"
    )
    logging.info(f"Tab opened, Tab id: {tab_id}")
