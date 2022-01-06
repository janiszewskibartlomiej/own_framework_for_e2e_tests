import pytest

from steps.ui_steps import UiSteps
from utils.automation_functions import data_generator

test_data: dict = data_generator(test_name="sent_many_emails")


@pytest.mark.parametrize(
    "data", test_data["data"], ids=test_data["names"],
)
@pytest.mark.load
def test_sent_many_emails_reports_page(request, driver, data: dict):
    # Given
    ui_steps: UiSteps = driver.ui_steps
    emails_list = ui_steps.send_repeat_emails(
        subject=data["subject"],
        message_content=data["body_text"],
        files_path=data["attachment_names"],
    )
    ui_steps.login_to_admin_panel()

    for email in emails_list:
        ui_steps.go_to_reports_page(
            timestamp=email["timestamp"], subject=email["subject"], status=data["expected_status"]
        )
        # When
        ui_steps.wait_for_email_and_all_done_status()
        current_status = ui_steps.current_page.status_text
        # Than
        assert (
                current_status == data["expected_status"]
        ), f"Wait #{email['timestamp']}# for expected status max {ui_steps.current_page.wait_for_element} seconds"
