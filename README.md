# <center>TEST PLAN</center>

#### Language : Python 3.8 up >> https://www.python.org/downloads/

#### System and Browsers

- [x] Chrome 
- [x] FireFox
- [x] macOS
- [x] WIN10
- [x] Linux


#### External libraries == [requirements-test.txt](./requirements-test.txt)
* pytest
* selenium
* pytest-html           >> reports template
* allure-pytest         >> reports template with tests history
* python-dotenv         >> load env variables
* pandas                >> data processing
* webdriver-manager     >> browsers driver download  https://pypi.org/project/webdriver-manager/
* sty                   >> change color in command line
* behave                >> BDD
* pytest-xdist          >> tests in parallel
* easyimap              >> simple imap wrapper
* jsonref               >> convert '$ref' in json to variable

#### install command == `pip install -r requirements-test.txt`

#### install allure-pytest in console >> https://docs.qameta.io/allure/#_installing_a_commandline

***

#### <i>Please creating `.env` file with data >> example in .env.example</i>

In this file we can set:

* in 12 line we can enter number of days about keep tests history - html pytest report and screenshot (we run this
  method in every tests ! We can change number of days in every tests)
* in 13 line we can enter number of send email.
* in 14 line we can enter github token - it's important because we can change limit of download driver 60 per
  hour https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/creating-a-personal-access-token
* in 19 line we can set the time (in seconds) to wait for element which will be visible on page

***

#### <i>run tests in command line == `pytest` or "pytest" + flag key like "-k, -v, --lf"</i>

#### run test with reports [pytest-html and allure:](./run_all_tests_with_reports.py)

command from root ==`python ./run_all_tests_with_reports.py`
or `python3 ./run_all_tests_with_reports.py` run on linux distribute

* in 11 line (flag_name) we can enter name of test if we want run pytest with `-k` flag
* in 19 line (send_to) we can enter address email (string) - where we want send the reports
* in 20 line (send_copy) we can enter address email (string) - where we want send copy the reports
* in 21 line (subject) we can enter the subject (string) of the report

#### run allure report from zip file >> Before unzip we must start server like `python -m http.server`

#### in ["ui_steps.py"](steps/ui_steps.py) we cn use 'step' decorator to log message after end methods
params:
* name: str = "message"
* use_return: bool = True if we want use return value to print data in {} place holder
* use_args: bool = True if we want use arguments from method call

examples:

`@step(name="Wait for email #{}# = {} seconds \nand wait for all done status = {} seconds", use_return=True)`

    def wait_for_email_and_all_done_status(self) -> tuple:
        self.current_page: ReportsPage
        wait_for_email = self.current_page.wait_for_email()
        wait_for_status = self.current_page.wait_for_all_done_status()
        return self.current_page.timestamp, wait_for_email, wait_for_status"""

***

### TEST DATA WE PREPARE IN JSON FILE.

* Every test module load test data from json file.
* Name pattern is 'test_data_'{name of test without name of page}.json

Json file schema:

* Primary key == unique test case name
* Second key must be 'data'
* inside we may use key for run specific way test and expected conditions.

Directory for json is ["resources/tests_data"](resources/tests_data)


***

## <center>Test cases:</center>

### [test_processing_of_email_reports_page:](e2e/test_processing_of_email_reports_page.py)

### [test_sent_many_emails_reports_page:](e2e/test_sent_many_emails_reports_page.py)

### [test_model_trainings_data_page:](e2e/test_model_trainings_data_page.py)

* in *.env* file we can set the time out (in seconds) >> WAIT_FOR_ELEMENT. This is time out of alert popup,

### [test_login_on_react_login_page.py:](e2e/test_login_on_react_login_page.py)

* Successfully login test cases
* Failure login test cases

### [test_menu_on_react_login_page:](e2e/test_menu_on_react_home_page.py)

### [test_details_on_react_message_details_page](e2e/test_details_on_react_message_details_page.py)
