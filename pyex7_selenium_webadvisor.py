# pyex7_selenium_webadvisor.py - Interact with webadvisor course search
#Evan Gardner
#s1270495
#CS-371
#Spring 2023

from selenium import webdriver
from selenium.webdriver.support.ui import Select        # for dropdown menus
from selenium.webdriver.chrome.options import Options   # for "headless" Chrome
from selenium.webdriver.common.by import By
import time                                             # implement pauses
 
# Instance of Options class to configure headless Chrome
options = Options()
 
# Parameter to tell Chrome that it should run without UI (headless)
options.headless = True
 
# driver = webdriver.Chrome(options=options)
 
driver = webdriver.Chrome()
 
driver.get('https://www2.monmouth.edu/muwebadv/wa3/search/SearchClassesv2.aspx')
 
# Select the term
term_val = '23/SU'
 
time.sleep(3)
 
# Find the Term dropdown menu
# term_select = Select(driver.find_element_by_name('_ct10:MainContent:ddlTerm'))
term_select = Select(driver.find_element(By.NAME, '_ctl0:MainContent:ddlTerm'))
term_select.select_by_value(term_val)
 
# Select the subject
subj_val = 'CS'
 
# Find the Subject dropdown menu
 
subj_select = Select(driver.find_element(By.NAME,'_ctl0:MainContent:ddlSubj_1'))
subj_select.select_by_value(subj_val)
 
# Click the Submit button
driver.find_element(By.NAME, '_ctl0:MainContent:btnSubmit').click()
 
# Get resulting html and print it
print(driver.page_source)
 
# Close the browser window
driver.quit() 