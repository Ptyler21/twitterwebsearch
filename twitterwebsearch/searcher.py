"""
Module for using the web interface of Twitter's search.
"""
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


TWITTER_SEARCH_URL = 'https://twitter.com/search-home'
SEARCH_FIELD = 'search-home-input'
WAIT_FOR_CLASS = 'AdaptiveSearchTitle-title'
SCROLLER_SCRIPT = '''
    footer = document.getElementsByClassName('stream-footer')[0];
    scroller = setInterval(function() { footer.scrollIntoView(); }, 250);
'''

POLL_TIME = 1 # seconds


def search(query):
    driver = webdriver.Firefox()
    driver.get(TWITTER_SEARCH_URL)
     
    elem = driver.find_element_by_id(SEARCH_FIELD)
    elem.send_keys(query)
    elem.send_keys(Keys.ENTER)
    
    res = ''
    try:
        elem = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, WAIT_FOR_CLASS))
        )
        driver.execute_script(SCROLLER_SCRIPT)
    finally:
        old_size = size = 0
        delta = not 0
        while delta != 0:
            time.sleep(POLL_TIME)
            
            old_size = size
            size = len(driver.page_source)
            delta = size - old_size
            
        res = driver.page_source
        driver.quit()
        
    return res
