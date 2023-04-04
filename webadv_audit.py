# webadv_audit.py - Python script to automate the process of getting a student's audit from WebAdvisor
# Student IDs: s1270495, 1285106, 1332481
# Names: Evan Gardner, Robert Reichard, Dmitry Bezborodov
# Course: CS-371
# Session: Spring 2023
# Assignment: Python Project 1

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import requests
import getpass
import sys
import re
import time

def main():
    
    # Get id from args and check if valid
    input_args = sys.argv
    id = user_id(input_args)
    
    if (id == 'invalid'):
        help()
        
    # Ask for password
    password = getpass.getpass(prompt="Enter password for "+id+": ").strip()
    
    # Set up the driver
    driver = webdriver.Chrome()
    driver.implicitly_wait(5) # Necessary!
    driver.get('https://webadvisor.monmouth.edu')
    
    # Find login button and click
    login = driver.find_element('id', 'acctLogin')
    login.find_element('tag name', 'a').click()
    driver.implicitly_wait(5) # Necessary!
    driver.get(driver.current_url)
    
    # Input the username and continue
    usernameInput = driver.find_element('id', 'userNameInput')
    usernameInput.send_keys(id)
    driver.find_element('id', 'nextButton').click()
    
    # Input password and enter 
    passwordInput = driver.find_element('id', 'passwordInput')
    passwordInput.send_keys(password)
    driver.find_element('id', 'submitButton').click()
    time.sleep(3)

    # Click the "Students" button
    wait = WebDriverWait(driver, 3)
    students_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Students")))
    students_link.click()
    time.sleep(3)

    # Click the "Academic Audit/Pgm Eval" button
    audit = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Academic Audit/Pgm Eval')]")))
    audit.click()
    time.sleep(3)

    # Click the "Major" so that the audit can be submitted to be displayed
    major = wait.until(EC.element_to_be_clickable((By.ID, "LIST_VAR1_1")))
    major.click()
    time.sleep(3)

    # Click the "Submit" button
    submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='submit'][name='SUBMIT2']")))
    submit.click()
    time.sleep(3)

    # rettrieve the current url
    url = driver.current_url

    # Parse the HTML
    time.sleep(10)  # Wait for the page to fully load
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # Get the student name and remove the "Student: " part
    name = soup.find('td', {'class': 'PersonName'}).strong.text.strip()
    name = name.replace('Student: ', '')

    # Get the program, catalog, Anticipated Completion Date
    # Find the main table that holds all the other tables
    studentTable = soup.find('table', {'id': 'StudentTable'})

    # Find the rows that hold the program, catalog, and Anticipated Completion Date
    program_row = studentTable.find('td', string=re.compile('^Program:'))
    catalog_row = studentTable.find('td', string=re.compile('^Catalog:'))
    completion_row = re.search(r'Anticipated<br>\s*Completion\s*Date:\s*</td><td\s+valign="bottom">(\d{2}/\d{2}/\d{2})</td>', html)

    # extract the program, catalog, and Anticipated Completion Date
    program = program_row.next_sibling.text.strip()
    catalog = catalog_row.next_sibling.text.strip()
    anticipated_completion_date = completion_row.group(1)



    # Print the results
    print ('\n\n')
    print ('Academic Audit Summary')
    print ('=========================')
    print('Name:', name)
    print('Program:', program)
    print('Catalog:', catalog)
    print('Anticipated Completion Date:', anticipated_completion_date)
    # print('Advisor:', advisor)
    # print('Class Level:', class_level)
    # print('Graduation requirements that are "In Progress":', in_progress_reqs)
    # print('Graduation requirements that are "Not Started":', not_started_reqs)
    # print('Credits earned at 200+ level:', credits_200)
    # print('Total credits earned:', total_credits)

    # Close the driver
    driver.close()


# Check if the student id is formated correctly
def user_id(args):
    
    if(len(args) != 2):
        return 'invalid'
        
    elif(re.match(r's\d{7}', args[1])):
        return args[1]
    else:
        print('invalid input of ID')
        return 'invalid'
    
    
# Print help and quit
def help():
    
    print(''' Usage: python3 webadv_audit.py [--option] [student id, e.g., s1100841]	
   where [--option] can be:
      --help:	     Display this help information and exit
      --save-pdf: Save PDF copy of entire audit to the current folder
                  as audit.pd''')
    
    quit()
    
main()

