# class_scheduler

This is a program designed to register a student for a specified list of classes at Christopher Newport University. This program uses an inputted registration time slot to register the student for their classes as soon as their time slot opens.

## Installation Prerequisites:
1. Install Google Chrome (https://www.google.com/chrome/downloads/)
2. Install Python (https://www.python.org/downloads/)
3. Install pip (https://pip.pypa.io/en/stable/installation/)
4. Run `# pip install virtualenv` on the command line
5. Install git (https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

## Installation
1. Clone the git repository to your local machine:

`# git clone https://github.com/wdreames/class_scheduler.git`

3. Create a virtual environment

`# virtualenv env`

3. Activate the environment

`# source ./env/bin/activate`

4. Install the necessary requirements

`# pip install -r requirements.txt`

## Configuration Instructions
1. Open `data/registration_info.txt`
2. Enter your 6 digit registration pin. Ex: `Registration key: 829379`
3. Enter a comma-separated list of CRN numberes for each course you want to register for. Note that the registrar will not let you register for more than 18 credits. If you try to do this the program will produce an error. Ex: `CRN Numbers: 8223, 8282, 8164, 8109, 8123`
5. Enter the current semester. Ex: `Semester for Registration: Fall Semester 2022`. Note that this must be formatted exactly as it appears in CNU Live.
6. Enter your registration time slot. Ex: `Registration date and time (YYYY-MM-DD HH:MM): 2022-03-24 07:00` would set your time slot as March 24th, 2022 at 7:00 A.M.

The `data/registration_info.txt` configuration file should look similar to this once your have completed this process:
```
Registration key: 829379
CRN Numbers: 8223, 8282, 8164, 8109, 8123
Semester for Registration: Fall Semester 2022
Registration date and time (YYYY-MM-DD HH:MM): 2022-03-24 07:00
```

## Running the Program

1. Run `# python3 course_selectory.py` on the command line
2. Enter your CNU student ID when prompted
3. Enter your CNU password when prompted. Your password is gathered using a secure input, so **it will not display anything as you type**.
4. From here, will be automated and the program will register you for your classes as soon as your time slot opens.
5. If any errors occur, confirm all of your information inside configuration file is correct, then run the program again.
6. Once the program completes, the window used for registration will remain open for an additional 5 minutes. This is done to give you time to make any desired manual changes to your schedule.