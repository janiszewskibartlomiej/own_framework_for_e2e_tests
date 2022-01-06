import pytest
from selenium.common import exceptions

from steps.ui_steps import UiSteps
from utils.automation_functions import data_generator

test_data_successful: dict = data_generator(test_name="login_successful_on_react_login_page")


@pytest.mark.parametrize(
    "data", test_data_successful["data"], ids=test_data_successful["names"],
)
@pytest.mark.successful_login
@pytest.mark.react_login
@pytest.mark.react
def test_successful_login_on_react_login_page(request, driver, data):
    # Given
    ui_steps: UiSteps = driver.ui_steps
    ui_steps.go_to_react_login_page()
    ui_steps.save_console_logs()
    # When
    ui_steps.login_to_react_homepage(enter_key=data["enter_key"])
    current_url = ui_steps.driver.current_url
    rules_link_text = ui_steps.rules_link_text
    ui_steps.save_console_logs()
    # Then
    assert current_url == data["expected_url"]
    assert rules_link_text == data["expected_link_text"]
    ui_steps.assert_status_in_console_logs()


test_data_failed: dict = data_generator(test_name="login_failure_on_react_login_page")


@pytest.mark.parametrize(
    "data", test_data_failed["data"], ids=test_data_failed["names"],
)
@pytest.mark.failed_login
@pytest.mark.react_login
@pytest.mark.react
def test_failed_login_on_react_login_page(request, driver, data):
    # Given
    ui_steps: UiSteps = driver.ui_steps
    ui_steps.go_to_react_login_page()
    ui_steps.save_console_logs()
    # When
    with pytest.raises(exceptions.TimeoutException):
        ui_steps.login_to_react_homepage(
            enter_key=data["enter_key"], user=data["username"], password=data["password"]
        )
    alert_message = ui_steps.react_login_alert_text
    ui_steps.save_console_logs()
    # Then
    assert alert_message == data["expected_alert_message"]
    ui_steps.assert_status_in_console_logs()
