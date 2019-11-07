import os
from selenium import webdriver
from datetime import datetime
import time
import pause

# Enter your preferred classes here:
classes = ['10', '9223']
# Also make sure to change the registration time!!! (line 38)

# Makes a connection to the internet through a Chrome driver
driver = webdriver.Chrome(os.path.join(os.getcwd(), 'data', 'chromedriver'))
driver.get('https://banweb.cnu.edu:9997/bpdbdad/twbkwbis.P_WWWLogin')

# Pulls out the prerequisites from the website
try:
    id = ''
    password = ''
    keycode = ''
    with open(os.path.join('data', 'keys.txt'), 'rt') as file:  # Reads in input data from file
        id = file.readline().strip()
        password = file.readline().strip()
        keycode = file.readline().strip()

    # Logs into CNU Live and navigates to class registration
    driver.find_element_by_id('UserID').send_keys(id)
    driver.find_element_by_name('PIN').send_keys(password + '\n')  # '\n' used in place of 'enter'
    driver.find_element_by_name('StuWeb-MainMenuLink').click()
    driver.find_element_by_link_text('Registration').click()
    driver.find_element_by_link_text('Add/Drop Classes').click()

    # Chooses Semester
    driver.find_element_by_xpath("//select[@name='term_in']/option[text()='Spring Semester 2020']").click()
    driver.find_element_by_name('term_in').submit()

    # Waits until the exact opening time to enter the pin
    # print(datetime.now())
    # pause.until(datetime(2019, 11, 6, 23, 15, 0, 0))
    # print(datetime.now())

    # Enters the Alternate PIN
    driver.find_element_by_name('pin').send_keys(keycode)
    driver.find_element_by_name('pin').submit()

    # Enters all of the classes and submits
    for i in range(len(classes)):
        if i == len(classes) - 1:
            driver.find_element_by_id('crn_id' + str(i + 1)).send_keys(classes[i] + '\n')
        else:
            driver.find_element_by_id('crn_id' + str(i + 1)).send_keys(classes[i])

    # Keeps the tab open for another two minutes
    time.sleep(120)
except Exception as e:
    print(e)
finally:
    driver.quit()  # Closes and quits the Chrome browser
