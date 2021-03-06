import logging
import os
import re
import time
import unicodedata
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
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
        logging.info("Download started")


def get_pdf(browser, download_button_path):

    # WebDriverWait(browser, 30).until(
    #     EC.presence_of_element_located((By.XPATH, "//*/iframe[@loading='lazy']"))
    # )

    iframe = browser.find_element_by_xpath("//*/iframe[@loading='lazy']")

    window_id_old = browser.current_window_handle  # save old id to go back to it
    link = iframe.get_attribute("src")
    open_new_tab(
        browser, link.replace("preview", "view"), window_id_old + "_2"
    )  # to go directly to download page
    browser.switch_to.window(browser.window_handles[-1])
    WebDriverWait(browser, 30).until(
        EC.presence_of_element_located((By.XPATH, f"{download_button_path}"))
    )
    logging.info("Downloading pdf")
    click_element(
        browser, download_button_path, is_download=True
    )  # Download from drive page
    logging.info("Finished downloading")
    browser.close()
    browser.switch_to.window(window_id_old)


def get_newest_file_path(path):
    files = os.listdir(path)
    paths = [os.path.join(path, basename) for basename in files]
    return max(paths, key=os.path.getmtime)

def open_new_tab(browser, url, tab_id):
    logging.info("Opening new tab")
    browser.execute_script(f"window.open('{url}'),'job{tab_id}'")

def create_file(path, base_file_name, access_mode, content, extension="txt"):
    logging.info(f"Creating file {base_file_name}.{extension}")
    with open(f"{path}/{base_file_name}.{extension}", access_mode, encoding="utf-8") as fp:
        fp.write(content)
    logging.info(f"File created at {path}/{base_file_name}.txt")

def get_text_post(browser, content_xpath):
    final_text = []
    paragraph_texts = browser.find_elements_by_xpath(content_xpath + "/p")
    div_texts = browser.find_elements_by_xpath(content_xpath + "/div")
    for text in paragraph_texts:
        text = text.lower()
        if text.text != "":
            final_text.append(re.sub("[^a-z]+", "", text.text))
    for text in div_texts:
        if text.text != "":
            final_text.append(re.sub("[^a-z]+", "", text.text))
    return " ".join(final_text)


def get_company(browser, company_xpath):
    try:
        return browser.find_element_by_xpath(company_xpath).text
    except NoSuchElementException:
        return "UnknownCompany"


def get_description(browser, description_xpath):
    description = browser.find_element_by_xpath(description_xpath).text
    description = unicodedata.normalize('NFD', description)
    description = description.encode('ascii', 'ignore')
    description = description.decode('utf-8')
    description = re.sub("\n+", " ", description)
    description = re.sub(r'\W+'," ", description)

    return description

def get_offer_age(browser, age_xpath):
    text = browser.find_element_by_xpath(age_xpath).text
    return re.sub("[^0-9]+", "", text)

def get_title(browser, title_xpath):
    return browser.find_element_by_xpath(title_xpath).text

def get_details(browser, details_xpath):
    return browser.find_element_by_xpath(details_xpath).text

def get_links_in_page(browser, post_xpath, verbose=False):
    offers = browser.find_elements_by_xpath(post_xpath)
    if verbose:
        print(f"Extracted {len(offers)} links")
    return [offer.get_attribute('href') for offer in offers]

def query_search(search_bar_element, query):
    search_bar_element.clear()
    search_bar_element.send_keys(query)
    search_bar_element.send_keys(Keys.ENTER)

def grab_offer(url, config, browser_options):
    time.sleep(2)
    try:
        browser = webdriver.Chrome(os.environ.get("CHROME_DRIVER"), options=browser_options)
        logging.info(f"Visting link {url}")
        browser.get(url)
        extracted_data = {"company_name" : get_company(browser, config["company_name"]).lower() ,
                        "description" : get_description(browser, config['description']).lower() ,
                        "offer_details" : get_details(browser, config["offer_details"]).lower(),
                        "offer_title" : get_title(browser, config["offer_title"]).lower(),
                        "offer_age": get_offer_age(browser, config["offer_age"]),
                        "url": url
                        }
        logging.info(f"""Handling company :{extracted_data['company_name']}, 
                    Offer : {extracted_data['offer_title']},
                    Posted : {extracted_data['offer_age']} days"""
        )
    finally:
        browser.close()
    return extracted_data
