import time
import logging
import traceback
from selenium.common.exceptions import NoSuchElementException
from helpers import  create_file, get_text_post, open_new_tab, get_pdf
from config import LINKEDIN_URL, DOWNLOAD_PATH, GDRIVE_DL_BUTTON_XPATH, browser

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
            logging.info(f"Handling company {company_name}")
            open_new_tab(browser, offer.get_attribute("href"), company_name)
            browser.switch_to.window(browser.window_handles[-1])
            get_pdf(
                browser, GDRIVE_DL_BUTTON_XPATH
            )  ## Google download button not found
        except NoSuchElementException:
            logging.info(f"Company {company_name} does not have pdf-book")  # Get text from page to a .txt file
            file_content = get_text_post(browser, content_xpath="//*/section[@class='post-content']")
            create_file(
                path=DOWNLOAD_PATH,
                base_file_name=company_name,
                access_mode="a+",
                content=file_content,
            )

            logging.info(f"Info logged")            
        finally:
            browser.close()
            browser.switch_to.window(browser.window_handles[0])

finally:
    logging.info("Quitting now")
    # for tab in browser.window_handles:
    #     browser.switch_to.window(tab)
    #     browser.close()
