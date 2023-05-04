# webadv_audit.py - Python script to automate the process of getting a student's audit from WebAdvisor
# Student IDs: s1270495, 1285106, 1332481
# Names: Evan Gardner, Robert Reichard, Dmitry Bezborodov
# Course: CS-371
# Session: Spring 2023
# Assignment: Python Project 1

from selenium import webdriver                                          # Selenium is used to automate the process of getting the audit
from selenium.webdriver.support.ui import WebDriverWait                 # WebDriverWait is used to wait for the page to load
from selenium.webdriver.support import expected_conditions as EC        # EC is used to check if the page has loaded
from selenium.webdriver.common.by import By                             # By is used to find elements by their id
from selenium.webdriver.common.keys import Keys                         # Keys is used to press the enter key
from bs4 import BeautifulSoup                                           # BeautifulSoup is used to parse the HTML
import requests                                                         # Requests is used to get the HTML
import getpass                                                          # Getpass is used to get the password without echoing it
import sys                                                              # Sys is used to get the command line arguments
import re                                                               # Regex is used to parse the HTML
import time                                                             # Time is used to wait for the page to load
import base64                                                           # Base64 is used to encode the image

# Function to get the user id from the command line arguments
def main():
    
    # Get id from args and check if valid
    input_args = sys.argv
    
    # Check if the user wants to save the pdf
    if "--help" in input_args:
        # Print help message
        help()
    # Check if the user wants to save the pdf
    elif "--save-pdf" in input_args:
        save_pdf = True
        input_args.remove("--save-pdf")  # remove the option from input_args list
    # If the user does not want to save the pdf
    else:
        save_pdf = False
    
    # Check if the user wants to save the html
    id = user_id(input_args)
    
    # If the user does not want to save the html
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
    
    # Input password and if it is incorrect, exit the application
    try:
        # Input password and enter
        passwordInput = driver.find_element('id', 'passwordInput')
        passwordInput.send_keys(password)
        driver.find_element('id', 'submitButton').click()
        time.sleep(1)
        
        # Check for error message
        if driver.find_element('id', 'errorTextPassword'):
            print("Incorrect user ID or password. Exiting. Quitting the application.")
            sys.exit(1)
    except Exception as e:
        # If there is no error message, then the login was successful
        pass

    # Click the "Students" button
    wait = WebDriverWait(driver, 1)
    students_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Students")))
    students_link.click()
    time.sleep(1)

    # Click the "Academic Audit/Pgm Eval" button
    audit = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Academic Audit/Pgm Eval')]")))
    audit.click()
    time.sleep(1)

    # Click the "Major" so that the audit can be submitted to be displayed
    major = wait.until(EC.element_to_be_clickable((By.ID, "LIST_VAR1_1")))
    major.click()
    time.sleep(1)

    # Click the "Submit" button
    submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='submit'][name='SUBMIT2']")))
    submit.click()
    time.sleep(1)

    # rettrieve the current url
    url = driver.current_url

    # Parse the HTML
    time.sleep(5)  # Wait for the page to fully load
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # Get the student name and remove the "Student: " part
    name = soup.find('td', {'class': 'PersonName'}).strong.text.strip()
    name = name.replace('Student: ', '')

    # Get the program, catalog, Anticipated Completion Date
    # Find the main table that holds all the other tables
    studentTable = soup.find('table', {'id': 'StudentTable'})
    studentInfo = studentTable.find('table', {'border': '0', 'cellpadding': '2'})

    # Find the rows that hold the program, catalog, and Anticipated Completion Date
    program_row = studentInfo.find('td', string=re.compile('^Program:'))
    catalog_row = studentInfo.find('td', string=re.compile('^Catalog:'))
    completion_row = re.search(r'Anticipated<br>\s*Completion\s*Date:\s*</td><td\s+valign="bottom">(\d{2}/\d{2}/\d{2})</td>', html)

    # extract the program, catalog, and Anticipated Completion Date
    program = program_row.next_sibling.text.strip()
    catalog = catalog_row.next_sibling.text.strip()
    anticipated_completion_date = completion_row.group(1)

    # get the element with additional info
    additionalInfo = studentInfo.parent.parent.find_next_sibling('tr')
    
    # # Extract advisor and class level info
    advisor = re.search(r'<br/> Advisor:(.+?)<br/>', str(additionalInfo), re.DOTALL)
    class_level = re.search(r'<br/> Class Level:(.+?)<br/>', str(additionalInfo), re.DOTALL)

    # Extract the advisor and class level
    studentData = studentTable.find_all(id = "RequirementTable")

    # Get the credits earned at 200+ level and total credits earned
    req200 = str
    reqTotal = str
    
    # Get the credits earned at 200+ level and total credits earned
    for table in studentData:
        if "54 Minimum Credits At the 200+ Level" in table.text:
            req200 = table.text
        elif "120 Minimum Credits to Graduate" in table.text:
            reqTotal = table.text

    # Extract the credits earned at 200+ level and total credits earned
    credits_200 = re.search('Credits Earned: (\d+)', req200).group(1)
    total_credits = re.search('Credits Earned: (\d+)', reqTotal).group(1)

    # Get the requirements
    in_progress_reqs, not_started_reqs = requirements(soup)

    # Print the summary of the audit to the console using the extracted data retrieved from the HTML
    print ('\n\n')
    print ('Academic Audit Summary')
    print ('=========================')
    print('Name:', name)
    print('Program:', program)
    print('Catalog:', catalog)
    print('Anticipated Completion Date:', anticipated_completion_date)
    print('Advisor:', advisor.group(1))
    print('Class level:', class_level.group(1))
    print("Requirments:")
    print("=====================================")
    # Print the all of the requirements and thier status
    getRequirements(soup)

    # Print the requirements that are in progress
    if (len(in_progress_reqs) != 0 ):
        print('\nGraduation requirements that are "In Progress":\n')
        for req in in_progress_reqs:
            print('\t' + req)
    else:
        print("\tNo requirements in progress")

    # Print the requirements that are not started
    if (len(not_started_reqs) != 0 ):
        print('\nGraduation requirements that are "Not Started":\n')
        for req in not_started_reqs:
            print('\t' + req)
    else:
        print("\tNo requirements not started")

    # Print the credits earned at 200+ level and total credits earned
    print('\nCredits earned at 200+ level:', credits_200 + '/54')
    print('Total credits earned:', total_credits + '/120')

    # Save the PDF
    if save_pdf:
        # start the PDF download
        print('=========================')
        print('Saving PDF copy of audit...')
        output_file = open('audit.pdf', 'wb')

        # get the PDF data
        pdf_data = driver.execute_cdp_cmd('Page.printToPDF', {})
        output_file.write(base64.b64decode(pdf_data['data']))
        output_file.close()

        # print the location of the saved PDF
        print('Saved PDF copy of audit to', output_file.name)

        # close the driver
        driver.close()

# Check if the student id is formated correctly
def user_id(args):
    
    # Check if the student id is formated correctly
    if(len(args) != 2):
        return 'invalid'
    elif(re.match(r's\d{7}', args[1])):
        return args[1]
    else:
        print('invalid input of ID')
        return 'invalid'
    
    
# Print help and quit
def help():
    
    # print the help message
    print(''' Usage: python3 webadv_audit.py [--option] [student id, e.g., s1100841]	
    where [--option] can be:
      --help:	     Display this help information and exit
      --save-pdf: Save PDF copy of entire audit to the current folder
                  as audit.pd''')
    
    # quit the program
    quit()

# Function for printing the requirements from the page
def getRequirements(document):
    # Find all the tables with requirements
    reqTables = document.find_all('table', {'id':'RequirementTable'})
    # Find all elements witha a requirements
    for table in reqTables:
        
        # Find the requirement name
        reqName = table.find('span', {'class' : 'ReqName'})
        # print numbered requirements
        print('\n' + reqName.text)
        
        # Find all the sub requirements
        subReqs = table.find_all('td', {'class': 'SubReqName'})
        reqGroups = table.find_all('td', {'class':'ReqGroupName'})
        
        # Find all the sub requirements
        for subreq in subReqs:
            # print letter requirements
            print("\t" + subreq.text.strip())
            
        # Find all the sub requirements
        for reqGroup in reqGroups:
            # print other requirements
            print ("\t\t" + reqGroup.text.strip())      

# Function for finding the requirements that are in progress or not started
def requirements(document):
    # Find all the tables with requirements
    reqTables = document.find_all('table', {'id':'RequirementTable'})
    reqs = []
    # Find all elements witha a requirements
    for reqTable in reqTables:
        reqs += reqTable.find_all('span', {'class':'ReqName'}) + \
                reqTable.find_all('td', {'class':'SubReqName'}) + \
                reqTable.find_all('td', {'class':'ReqGroupName'})

    # Find all the requirements that are in progress or not started
    in_progress_reqs = []
    not_started_reqs = []

    # Loop through all the requirements
    for req in reqs:
        # If requirement is InProgress, add into an array
        if req.find('b', {'class': 'StatusInProgress'}):
            reqName = req.text.strip()
            in_progress_reqs.append(reqName)
        # If requirement is notStarted, add into an array
        elif req.find('b', {'class': 'StatusNotStarted'}):
            reqName = req.text.strip()
            not_started_reqs.append(reqName)

    # Return the arrays of requirements that are in progress or not started
    return in_progress_reqs, not_started_reqs

# Main function
main()