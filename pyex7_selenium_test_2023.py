# pyex7_selenium_test_2023.py - simple selenium example using Google Chrome
#Evan Gardner
#s1270495
#CS-371
#Spring 2023

from selenium import webdriver
from selenium.webdriver.common.keys import Keys # to emulate typing
import time                 # implement pauses

# WINDOWS: Make sure that chromedriver.exe is in the same folder as
#          this .py script
#
# MACOS  : Make sure that chromedriver is in a $PATH-included file
#          system location such as /usr/local/bin 
#          (mv chromedriver /usr/local/bin)
driver = webdriver.Chrome()

driver.get('http://www.python.org')
print(driver.title)         # print title of web site
assert 'Python' in driver.title

elem = driver.find_element_by_name('q') # find the search box at python.org
elem.clear()                # clear the search box
time.sleep(5)               # pause 5 sec
elem.send_keys('pycon')     # 'type' the word 'pycon' in the search box
time.sleep(5)
elem.send_keys(Keys.RETURN) # hit Return after typing in search box

assert "No results found." not in driver.page_source

print(driver.page_source)   # show search results html page source

time.sleep(10)

driver.quit()               # close the browser window
