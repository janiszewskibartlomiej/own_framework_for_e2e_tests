import os
import sys

sys.path.append(os.path.abspath(os.curdir))

import resources.constants as constant
from resources.automation_functions import (
    run_pytest_html_and_allure_report,
    send_email,
)

flag_name = "react"
by_name = sys.argv[1] if len(sys.argv) == 2 else flag_name

if __name__ == "__main__":
    reports = run_pytest_html_and_allure_report(by_mark=by_name)

    send_email(
        send_to=os.environ.get("ADMIN_EMAIL"),
        send_copy=os.environ.get("SEND_COPY"),
        subject=constant.REPORTS_OF_TESTS,
        files_path=reports,
    )
