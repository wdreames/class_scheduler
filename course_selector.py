import os
import pause
import time
import datetime
from selenium import webdriver
from getpass import getpass

# Note that the registrar won't let you register for >18 credits and if you try to the program will mess up
# Also make sure to change the registration time!!! (line 40)

# Gathers user input
# Needs to be run on terminal for this to work!
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

print('Testing Username and Password...')

# Run driver without waiting
# Wait until close to login
# Run and wait until correct time

driverConfirmation = webdriver.Chrome(os.path.join(os.getcwd(), 'data', 'chromedriver'))
driverConfirmation.get('https://banweb.cnu.edu/banweb/twbkwbis.P_WWWLogin')
# Logs into CNU Live and navigates to class registration
driverConfirmation.find_element_by_id('UserID').send_keys(student_id)
driverConfirmation.find_element_by_name('PIN').send_keys(password + '\n')  # '\n' used in place of 'enter'

# Pauses so that way it has time to load the next page
time.sleep(0.1)
driverConfirmation.find_element_by_name('StuWeb-MainMenuLink').click()
driverConfirmation.find_element_by_link_text('Registration').click()
driverConfirmation.find_element_by_link_text('Add/Drop Classes').click()

# Chooses Semester
driverConfirmation.find_element_by_xpath("//select[@name='term_in']/option[text()='{}']".format(semester)).click()
driverConfirmation.find_element_by_name('term_in').submit()

# Enters the pin
driverConfirmation.find_element_by_name('pin').send_keys(keycode)

# Begins registration
driverConfirmation.find_element_by_name('pin').submit()
pause.sleep(5)
driverConfirmation.quit()

window_start_time = registration_date - datetime.timedelta(minutes=5)
print('Waiting until {} to start...'.format(window_start_time))
pause.until(window_start_time)

print('Connecting to CNU...')

# Makes a connection to the internet through a Chrome driver
driver = webdriver.Chrome(os.path.join(os.getcwd(), 'data', 'chromedriver'))
driver.get('https://banweb.cnu.edu/banweb/twbkwbis.P_WWWLogin')

try:
    # Logs into CNU Live and navigates to class registration
    driver.find_element_by_id('UserID').send_keys(student_id)
    driver.find_element_by_name('PIN').send_keys(password + '\n')  # '\n' used in place of 'enter'
    # Pauses so that way it has time to load the next page
    time.sleep(0.1)
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
    altered_reg_date = registration_date + datetime.timedelta(milliseconds=2500)
    print('Current time:  {}'.format(datetime.datetime.now()))
    print('Waiting until: {}'.format(altered_reg_date))
    pause.until(altered_reg_date)
    # TODO: Important: If the time you log in when testing is earlier than it should be,
    # TODO: add a slight delay to the program so it can register at the correct time
    # TODO: (don't want to be half a second early)

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
    time.sleep(3000)
    driver.quit()
