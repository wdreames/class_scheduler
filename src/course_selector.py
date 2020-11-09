
import os
import pause
import time
from datetime import datetime
from selenium import webdriver
from getpass import getpass

# Note that the registrar won't let you register for >18 credits and if you try to the program will mess up
# Also make sure to change the registration time!!! (line 40)

# Gathers user input
# Needs to be run on terminal for this to work!
id = input('Enter your student id: ')
password = getpass()

# Reads in input data from file
with open(os.path.join('data', 'data.txt'), 'rt') as file:
    keycode = file.readline().split(':')[1].strip()
    classes = [x.strip() for x in file.readline().split(':')[1].split(',')]
    semester = file.readline().split(':')[1].strip()

print('Connecting to CNU...')

# Makes a connection to the internet through a Chrome driver
driver = webdriver.Chrome(os.path.join(os.getcwd(), 'data', 'chromedriver'))
driver.get('https://banweb.cnu.edu/banweb/twbkwbis.P_WWWLogin')

try:
    # Logs into CNU Live and navigates to class registration
    driver.find_element_by_id('UserID').send_keys(id)
    driver.find_element_by_name('PIN').send_keys(password + '\n')  # '\n' used in place of 'enter'
    time.sleep(0.1)  # Pauses so that way it has time to load the next page
    driver.find_element_by_name('StuWeb-MainMenuLink').click()
    driver.find_element_by_link_text('Registration').click()
    driver.find_element_by_link_text('Add/Drop Classes').click()

    # Chooses Semester
    driver.find_element_by_xpath("//select[@name='term_in']/option[text()='{}']".format(semester)).click()
    driver.find_element_by_name('term_in').submit()

    # Enters the pin
    driver.find_element_by_name('pin').send_keys(keycode)

    # Waits until the exact opening time to enter the pin
    # Best to enter the exact moment that classes open rather than half a second early
    # Year, Month, Day, Hour (military-time), Minute, Second, Millisecond
    print(datetime.now())
    pause.until(datetime(2020, 11, 9, 11, 27, 30, 0))
    print(datetime.now())

    # Begins registration
    driver.find_element_by_name('pin').submit()

    # Enters all of the classes and submits
    for i in range(len(classes)):
        if i == len(classes) - 1:
            driver.find_element_by_id('crn_id' + str(i + 1)).send_keys(classes[i] + '\n')
        else:
            driver.find_element_by_id('crn_id' + str(i + 1)).send_keys(classes[i])
except Exception as e:
    print(e)
finally:
    # Keeps the tab open for another five minutes
    time.sleep(300)
    driver.quit()
