import logging
import os
from selenium.webdriver.chrome.options import Options



logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)

INPUT_DIRECTORY = f"/home/{os.environ['USER']}/projects/internship-seeker/data"
OUTPUT_DIRECTORY = f"/home/{os.environ['USER']}/projects/internship-seeker/data/resultpdf"
DOWNLOAD_PATH = f"/home/{os.environ['USER']}/projects/internship-seeker/data"
MAX_PAGE = 24
LINKEDIN_URL = "https://www.linkedin.com/pulse/collection-de-plusieurs-catalogues-stages-pfe-2021-recruter-tn/"
GDRIVE_DL_BUTTON_XPATH = "//*/div[@data-tooltip='تنزيل' or @data-tooltip='Télécharger' or @data-tooltip='Download']"

SEARCH_QUERIES = ["data science", "deep learning", "machine learning", "data"]
OPTION_CARRIERE_LINK = "https://www.optioncarriere.tn/recherche/emplois?s=&l=Tunisie"



chrome_options = Options()
# chrome_options.add_argument('load-extension='+)
# chrome_options.add_argument("--headless")
chrome_options.add_experimental_option(
    "prefs",
    {
        "download.default_directory": DOWNLOAD_PATH,
        "download.prompt_for_download": False,
        "directory_upgrade": True,
    },
)
