import os
from selenium import webdriver
from datetime import datetime
import time
import pause

# Enter your preferred classes here:
classes = ['8116']
# Also make sure to change the registration time!!! (line 40)

# Makes a connection to the internet through a Chrome driver
driver = webdriver.Chrome(os.path.join(os.getcwd(), 'data', 'chromedriver'))
driver.get('https://banweb.cnu.edu/banweb/twbkwbis.P_WWWLogin')

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
    driver.find_element_by_xpath("//select[@name='term_in']/option[text()='Fall Semester 2020']").click()
    driver.find_element_by_name('term_in').submit()

    # Waits until the exact opening time to enter the pin
    # Best to enter the exact moment that classes open rather than half a second early
    # Year, Month, Day, Hour (military-time), Minute, Second, Millisecond
    print(datetime.now())
    pause.until(datetime(2020, 5, 29, 8, 0, 0, 0))
    print(datetime.now())

    # Enters the Alternate PIN
    driver.find_element_by_name('pin').send_keys(keycode)
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
