from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

def get_html(url, wait_second=1):
    options = Options()
    options.set_headless(True)
    driver = webdriver.Chrome(chrome_options=options)
    driver.get(url)
    time.sleep(wait_second)
#    html = driver.page_source.encode('utf-8')
#    return str(html)
    html = driver.page_source.encode('utf-8').decode('utf-8')
    return html

