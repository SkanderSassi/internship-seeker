import logging
import traceback
import time
import os
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver


logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)

MAX_PAGE = 24
URL_DOWNLOAD = "https://drive.google.com/file/d/13f6LTkYOHWEJy61cNvX1B5BQdAfE255l/view"
LINKEDIN_URL = "https://www.linkedin.com/pulse/collection-de-plusieurs-catalogues-stages-pfe-2021-recruter-tn/"
GDRIVE_DL_BUTTON_XPATH = "//*/div[@data-tooltip='تنزيل']"


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
