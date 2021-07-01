from logging import info
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys



class Seeker():
    def __init__(self, urls, searchbar_ids, search_queries) -> None:
        
        self.driver = webdriver.Chrome(os.environ.get('CHROME_DRIVER'))
        self.urls = urls
        
    def launch_session(self):
        info("Launching scraping session..")
        for url in self.urls:
            
            self.driver.get(url)
        info("Session ended")
            
    def _search_jobs(self, id_searchbar, search_query):
        
        search_bar = self.driver.find_element_by_id(id_searchbar)
        search_bar.send_keys(search_query)
    
    
        
        

    
        
    
    
    