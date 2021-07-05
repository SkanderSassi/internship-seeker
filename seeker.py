import time
import logging
import traceback
from selenium.common.exceptions import NoSuchElementException
from helpers import click_element, open_new_tab, get_pdf
from config import LINKEDIN_URL, GDRIVE_DL_BUTTON_XPATH, browser

## Article
### Section -> H3 : Title | class: entry-emta -> Infos | Download_button_drive : /html/body/div[3]/div[3]/div/div[3]/div[2]/div[2]/div[3]
### Getting to pdf page: iframe -> get src -> /html/body/div[4]/div[3]/div/div[2]/div -> download_button_drive -> Click
## Next page //*/a[@class='nextpostslink']
## Get page -> 

browser.get(LINKEDIN_URL)
time.sleep(2)


try:
    offers = browser.find_elements_by_xpath("//*/ol/li/a")

    for offer in offers:
        try:
            company_name = offer.text
            open_new_tab(browser, offer.get_attribute('href'), company_name)
            browser.switch_to.window(browser.window_handles[-1])
            get_pdf(browser, GDRIVE_DL_BUTTON_XPATH)     ## Google download button not found
            browser.close() 
            browser.switch_to.window(browser.window_handles[0])
        except NoSuchElementException:
            logging.info(f"Element not found for company {company_name}")
            logging.info(f"Continuing")
            continue

finally:
    logging.info("Quitting now")
    for tab in browser.window_handles:
        browser.switch_to.window(tab)
        browser.close()
