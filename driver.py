import logging
import traceback
import time
import os
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)

URL = "https://www.optioncarriere.tn"

# URLS_FILE = "list_of_sites.txt"
SEARCHBAR_IDS = ["s"]
SEARCH_QUERIES = ["data science"]


browser = webdriver.Chrome(os.environ["CHROME_DRIVER"])

browser.get(URL)
time.sleep(2)

search_bar = browser.find_element_by_id("s")
ActionChains(browser).send_keys_to_element(search_bar, "data science").send_keys(
    Keys.ENTER
).perform()

job_list = []
try:
    while(browser.find_element_by_xpath("//*/p/*[@rel = 'next']")):
        try:
            jobs = browser.find_elements_by_xpath(
                "//ul[@class='jobs']/li/article[@class='job clicky']/header/h2/a"
            )
            action = ActionChains(browser)
            logging.info(f"Found {len(jobs)} jobs")
            logging.info(f"Opening new tabs..")

            job_id = 0
            for job in jobs:
                # if job_id > 5 :
                #     print(job_list)
                #     break
                data_log = dict()
                logging.info(f"Opening {job.get_attribute('href')}")
                browser.execute_script(
                    f"window.open('{job.get_attribute('href')}'),'job{job_id}'"
                )

                logging.info("Link opened")
                time.sleep(3)
                browser.switch_to.window(browser.window_handles[-1])

                logging.info("Extracting data")
                parent_path = browser.find_element_by_xpath("//*[@id='job']/div")
                infos = parent_path.find_element_by_xpath("./header")
                details = infos.find_element_by_xpath("./ul[1]")
                content = parent_path.find_element_by_xpath("./section[@class='content']")

                data_log["offer_title"] = infos.find_element_by_xpath("./h1").text
                data_log["company_name"] = (
                    infos.find_element_by_xpath("./p[@class='company']").text
                    if len(infos.find_elements_by_xpath("./p[@class='company']")) > 0
                    else "Unknown"
                )
                data_log["details"] = details.text
                data_log["content"] = content.text

                job_list.append(data_log)

                logging.info("Job appended : {}".format(data_log["offer_title"]))
                job_id += 1
                browser.switch_to.window(browser.window_handles[0])
        finally:
            for handle in browser.window_handles[1:]:
                browser.switch_to.window(handle)
                browser.close()
            browser.switch_to.window(browser.window_handles[0])
        logging.info("Trying to switch pages")
        ActionChains(browser).click(browser.find_element_by_xpath("//*/p/*[@rel = 'next']")).perform()
    
except NoSuchElementException:
    logging.info("No more pages")

except Exception as e:
    traceback.print_exc()

finally:
    logging.info("Finishing up..")
    browser.switch_to.window(browser.window_handles[0])
    browser.close()
    logging.info("Saving data to file")
    print(job_list[1:6])
