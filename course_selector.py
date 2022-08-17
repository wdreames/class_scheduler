import os
import pause
import time
import datetime
from getpass import getpass
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Note that the registrar won't let you register for >18 credits and if you try to the program will mess up

# Gathers user input
student_id = input('Enter your student id: ')
password = getpass()

# Reads in input data from file
with open(os.path.join('data', 'registration_info.txt'), 'rt') as file:
    # The .split(':', 1)[1] is used to get rid of the text explaining how each line should be used
    keycode = file.readline().split(':', 1)[1].strip()
    classes = [x.strip() for x in file.readline().split(':', 1)[1].split(',')]
    semester = file.readline().split(':', 1)[1].strip()
    date_str = file.readline().split(':', 2)[2].strip()

registration_date = datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M')

print('Testing Username, Password, and Registration Key...')

# Logs into CNU Live and navigates to class registration
driverTest = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driverTest.get('https://banweb.cnu.edu/banweb/twbkwbis.P_WWWLogin')

try:
    driverTest.find_element(By.ID, 'UserID').send_keys(student_id)
    driverTest.find_element(By.NAME, 'PIN').send_keys(password + '\n')  # '\n' used in place of 'enter'

    # Waits for the page to load
    element = WebDriverWait(driverTest, 20).until(
        EC.presence_of_element_located((By.NAME, 'StuWeb-MainMenuLink'))
    )
    driverTest.find_element(By.NAME, 'StuWeb-MainMenuLink').click()
    driverTest.find_element(By.LINK_TEXT, 'Registration').click()
    driverTest.find_element(By.LINK_TEXT, 'Add/Drop Classes').click()

    # Chooses Semester
    driverTest.find_element(By.XPATH, "//select[@name='term_in']/option[text()='{}']".format(semester)).click()
    driverTest.find_element(By.NAME, 'term_in').submit()

    # Enters the pin
    driverTest.find_element(By.NAME, 'pin').send_keys(keycode)
    driverTest.find_element(By.NAME, 'pin').submit()

    # If no errors have occurred up to this point, the test was successful
    print('Credentials are valid.')
    pause.sleep(5)
    driverTest.quit()
except Exception as e:
    print('Error: Invalid credentials')
    print(e)
    exit(1)

window_start_time = registration_date - datetime.timedelta(minutes=5)
print('Waiting until {} to start...'.format(window_start_time))
pause.until(window_start_time)

print('Connecting to CNU...')

# Makes a connection to the internet through a Chrome driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get('https://banweb.cnu.edu/banweb/twbkwbis.P_WWWLogin')

try:
    # Logs into CNU Live and navigates to class registration
    driver.find_element(By.ID, 'UserID').send_keys(student_id)
    driver.find_element(By.NAME, 'PIN').send_keys(password + '\n')  # '\n' used in place of 'enter'
    # Pauses so that way it has time to load the next page
    time.sleep(0.1)
    driver.find_element(By.NAME, 'StuWeb-MainMenuLink').click()
    driver.find_element(By.LINK_TEXT, 'Registration').click()
    driver.find_element(By.LINK_TEXT, 'Add/Drop Classes').click()

    # Chooses Semester
    driver.find_element(By.XPATH, "//select[@name='term_in']/option[text()='{}']".format(semester)).click()
    driver.find_element(By.NAME, 'term_in').submit()

    # Enters the pin
    driver.find_element(By.NAME, 'pin').send_keys(keycode)

    # Waits until the exact opening time to enter the pin
    altered_reg_date = registration_date + datetime.timedelta(milliseconds=1500)
    print('Current time:  {}'.format(datetime.datetime.now()))
    print('Waiting until: {}'.format(altered_reg_date))
    pause.until(altered_reg_date)

    # Begins registration
    driver.find_element(By.NAME, 'pin').submit()

    # Enter all courses and submit for registration
    for i in range(len(classes)):
        if i == len(classes) - 1:
            driver.find_element(By.ID, 'crn_id' + str(i + 1)).send_keys(classes[i] + '\n')
        else:
            driver.find_element(By.ID, 'crn_id' + str(i + 1)).send_keys(classes[i])

    print('Completed course registration at {}.'.format(datetime.datetime.now()))
except Exception as e:
    print('An error occurred during the course registration process:')
    print(e)
finally:
    # Keeps the tab open for another five minutes
    print('The browser will remain open for an additional 5 minutes for manual use.')
    print('Enter Ctrl+C to exit.')
    time.sleep(3000)
    driver.quit()
