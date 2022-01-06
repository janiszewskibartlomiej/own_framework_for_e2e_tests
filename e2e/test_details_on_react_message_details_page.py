import pytest

from steps.ui_steps import UiSteps
from utils.automation_functions import data_generator

test_data: dict = data_generator(test_name="details_on_react_message_details_page")


@pytest.mark.parametrize(
    "data", test_data["data"], ids=test_data["names"],
)
@pytest.mark.react_message_details
@pytest.mark.react_full_db
@pytest.mark.react
def test_details_on_react_message_details_page(request, driver, data):
    # Given
    ui_steps: UiSteps = driver.ui_steps
    ui_steps.go_to_react_login_page()
    ui_steps.save_console_logs()
    ui_steps.login_to_react_homepage(enter_key=data["enter_key"])
    ui_steps.save_console_logs()
    ui_steps.go_to_general_messages_page()
    ui_steps.save_console_logs()
    # When
    for index_row in range(ui_steps.number_of_show_details):
        ui_steps.go_to_message_details_page(index_row=index_row)
        ui_steps.save_console_logs()
        (h1_header, content,) = ui_steps.verify_h1_header_and_content_on_message_details_page()
        # Then
        assert h1_header == data["expected_h1_header"]
        assert content
        ui_steps.go_to_general_messages_page()

    ui_steps.assert_status_in_console_logs()
