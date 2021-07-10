import logging
import os
import concurrent.futures
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from helpers import grab_offer, get_links_in_page
from config import SEARCH_QUERIES

MAX_THREADS = 8
MAX_LINKS = 400
LINK = "https://www.optioncarriere.tn/recherche/emplois?s=&l=Tunisie"

CONFIG_XPATH = {
    "description": "//*/section[@class='content']",
    "total_offers": "//*[@id='search-content']/header/p[2]/span[1]",
    "company_name": "//*[@id='job']/div/header/p[1]",
    "offer_title": "//*[@id='job']/div/header/h1",
    "offer_details": "//*/ul[@class='details']/li",
    "offer_age": "//*/header/ul[@class='tags']/li[1]/span",
}

# # post xpath //ul[@class='jobs']/*/article[@class='job clicky']/*//a
# # link > https://www.optioncarriere.tn/recherche/emplois?s=&l=Tunisie
# # Searchbar id = 's'
# # article -> class = job clicky
# # header -> h1 -> Offer title
# # header -> p -> Company name (Conditional)
# # header -> ul[@class='details'] -> li -> Location etc..
# # header -> ul[@class='tags'] -> li -> Date etc..
# # div[@class='container'] -> section[@class='content'] -> Description
# # //*[@id="search-content"]/p/a -> Next

if __name__ == "__main__":

    browser = webdriver.Chrome(os.environ.get("CHROME_DRIVER"))
    browser.get(LINK)
    link_set = set()
    search_button = browser.find_element_by_id("s")
    
    for query in SEARCH_QUERIES:
        logging.info(f"Acquiring links for query {query}")
        ActionChains(browser).send_keys_to_element(search_button, query).send_keys(Keys.ENTER).perform()
        if len(link_set) > 300:
            break
        while(browser.find_element_by_xpath("//*[@id='search-content']/p/a")): #while more pages exist
            try:
                link_set.update(get_links_in_page(browser, "//ul[@class='jobs']/*/article[@class='job clicky']/*//a"))      
            except NoSuchElementException:
                continue

    # with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as pool:
    #     pool.map(grab_offer, link_set)
    # grab_offer(
    #     "https://www.optioncarriere.tn/jobad/tna28b52357d2a795994734657c9fd18fa",
    #     CONFIG_XPATH,
    # )
    
