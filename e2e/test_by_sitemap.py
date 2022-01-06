import pytest

from steps.ui_steps import UiSteps
from utils.automation_functions import data_generator

test_data: dict = data_generator(test_name="sitemap_from_react_pages")


@pytest.mark.parametrize(
    "data", test_data["data"], ids=test_data["names"],
)
@pytest.mark.sitemap
@pytest.mark.react
def test_by_sitemap(request, driver, data):
    # Given
    if driver.name == "chrome":
        ui_steps: UiSteps = driver.ui_steps
        ui_steps.go_to_react_login_page()
        ui_steps.login_to_react_homepage(enter_key=data["enter_key"])
        # When
        ui_steps.get_href_list_from_home_page()
        ui_steps.build_sitemap_from_endpoints()
        ui_steps.get_all_console_logs_from_sitemap()
        # Then
        ui_steps.assert_status_in_console_logs()
    else:
        pytest.skip("GeckoDriver can't get console logs")
