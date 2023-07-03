#!/usr/bin/env python

from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
display = Display(visible=0, size=(800, 600))
display.start()

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--profile-directory=Default')
chrome_options.add_argument('--user-data-dir=~/.config/google-chrome')

driver = webdriver.Chrome(options=chrome_options)
url = 'https://www.google.com'
driver.get(url) 
get_url = driver.current_url 
print(get_url)

display.stop()
