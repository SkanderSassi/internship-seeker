import json
import logging
import os
import time

import concurrent.futures
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from helpers import create_file, grab_offer, get_links_in_page, query_search
from config import OUTPUT_DIRECTORY, SEARCH_QUERIES, chrome_options

MAX_THREADS = 8
MAX_LINKS = 100
LINK = "https://www.optioncarriere.tn/"

CONFIG_XPATH = {
    "description": "//*/section[@class='content']",
    "total_offers": "//*[@id='search-content']/header/p[2]/span[1]",
    "company_name": "//*[@id='job']/div/header/p[1]",
    "offer_title": "//*[@id='job']/div/header/h1",
    "offer_details": "//*/ul[@class='details']/li",
    "offer_age": "//*/header/ul[@class='tags']/li[1]/span",
    "next_button" : "//*[@id='search-content']/p/a[@rel='next']",
    "job_link" : "//ul[@class='jobs']/*/article[@class='job clicky']/*//a"
}

if __name__ == "__main__":

    browser = webdriver.Chrome(os.environ.get("CHROME_DRIVER"))
    browser.get(LINK)
    link_set = set()
    try:
        for query in SEARCH_QUERIES:
            search_bar = browser.find_element_by_id("s")
            pages_remaining = True
            logging.info(f"Acquiring links for query {query}")
            query_search(search_bar, query)
            # ActionChains(browser).send_keys_to_element(search_bar, query).send_keys(Keys.ENTER).perform()
            while(pages_remaining and len(link_set) < 100): #while more pages exist    
                try:
                    next_button = browser.find_element_by_xpath(CONFIG_XPATH['next_button'])
                    
                    link_set.update(get_links_in_page(browser, 
                                                    CONFIG_XPATH['job_link'],
                                                    verbose=False) 
                                    )      
                    next_button.click()
                except NoSuchElementException:
                    pages_remaining = False
                time.sleep(2)
            if len(link_set) > MAX_LINKS:
                
                break
    finally:
        logging.info(f"Total links extracted {len(link_set)}")
        browser.close()
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as pool:
        futures = [pool.submit(grab_offer, url, CONFIG_XPATH, chrome_options) for url in link_set]
    future_results = [f.result() for f in futures]
    create_file(OUTPUT_DIRECTORY, "offers", "w+",json.dumps(future_results, indent=4), extension="json")
       
