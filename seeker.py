import logging
import traceback
import time
import os
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from helpers import clickElement
## Article
### Section -> H3 : Title | class: entry-emta -> Infos | Download_button_drive : /html/body/div[3]/div[3]/div/div[3]/div[2]/div[2]/div[3]
### Getting to pdf page: iframe -> get src -> /html/body/div[4]/div[3]/div/div[2]/div -> download_button_drive -> Click
## Next page //*/a[@class='nextpostslink']

MAX_PAGE = 24
GDRIVE_DOWNLOAD_XPATH = "/html/body/div[3]/div[3]/div/div[3]/div[2]/div[2]/div[3]"
URL_DOWNLOAD = "https://drive.google.com/file/d/13f6LTkYOHWEJy61cNvX1B5BQdAfE255l/view"
URL = "https://recruter.tn/sofrecom-propose-son-catalogue-des-stages-dete-2021/"

chrome_options = Options()
chrome_options.add_experimental_option(
    "prefs",
    {
        "download.default_directory": f"/home/{os.environ['USER']}/projects/internship-seeker/pdfs",
        "download.prompt_for_download": False,
        "directory_upgrade": True,
    },
)
browser = webdriver.Chrome(os.environ.get("CHROME_DRIVER"), options=chrome_options)

browser.get(URL_DOWNLOAD)
time.sleep(2)

try:
    clickElement(browser, xpath_to_element=GDRIVE_DOWNLOAD_XPATH)
    

except NoSuchElementException:
    print("Element not found")
finally:
    browser.close()
