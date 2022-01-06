import pytest

from steps.ui_steps import UiSteps
from utils.automation_functions import data_generator

test_data: dict = data_generator(test_name="menu_on_react_home_page")


@pytest.mark.parametrize(
    "data", test_data["data"], ids=test_data["names"],
)
@pytest.mark.react_menu
@pytest.mark.react
def test_menu_on_react_login_page(request, driver, data):
    # Given
    ui_steps: UiSteps = driver.ui_steps
    ui_steps.go_to_react_login_page()
    ui_steps.save_console_logs()
    ui_steps.login_to_react_homepage(enter_key=data["enter_key"])
    # When
    (
        home_page_h1,
        headers_content_in_dashboard,
    ) = ui_steps.verify_h1_header_and_headers_content_on_home_page()
    # Then
    ui_steps.save_console_logs()
    assert home_page_h1 == data["expected_h1_overview"]
    assert headers_content_in_dashboard == data["expected_headers_content_in_dashboard"]
    # When
    (
        messages_h1,
        message_headers_input_search,
    ) = ui_steps.verify_h1_header_and_headers_of_inputs_search_on_messages_page()
    ui_steps.save_console_logs()
    # Then
    assert messages_h1 == data["expected_h1_messages"]
    assert message_headers_input_search == data["expected_headers_input_search"]
    # When
    (
        trainings_data_h1,
        trainings_data_headers_input_search,
        trainings_data_table_headers,
    ) = (
        ui_steps.verify_h1_header_and_headers_of_inputs_search_and_table_headers_on_trainings_data_page()
    )
    ui_steps.save_console_logs()

    # Then
    assert trainings_data_h1 == data["expected_h1_trainings_data"]
    assert (
            trainings_data_headers_input_search == data["expected_headers_input_search_trainings_data"]
    )
    assert trainings_data_table_headers == data["expected_table_headers_trainings_data"]
    # When
    (
        import_data_h1,
        import_data_table_headers,
    ) = ui_steps.verify_h1_header_and_table_headers_on_import_data_page()
    ui_steps.save_console_logs()
    # Then
    assert import_data_h1 == data["expected_h1_import_data"]
    assert import_data_table_headers == data["expected_table_headers_import_data"]
    # When
    (
        models_h1,
        models_table_headers,
    ) = ui_steps.verify_h1_header_and_table_headers_on_models_page()
    ui_steps.save_console_logs()
    # Then
    assert models_h1 == data["expected_h1_models"]
    assert models_table_headers == data["expected_table_headers_models"]
    # When
    (
        categories_h1,
        categories_table_headers,
    ) = ui_steps.verify_h1_header_and_table_headers_on_categories_page()
    ui_steps.save_console_logs()
    # Then
    assert categories_h1 == data["expected_h1_categories"]
    assert categories_table_headers == data["expected_table_headers_categories"]
    # When
    (
        topics_h1,
        topics_table_headers,
    ) = ui_steps.verify_h1_header_and_table_headers_on_topics_page()
    ui_steps.save_console_logs()
    # Then
    assert topics_h1 == data["expected_h1_topics"]
    assert topics_table_headers == data["expected_table_headers_topics"]
    # When
    (rules_h1, rules_table_headers,) = ui_steps.verify_h1_header_and_table_headers_on_rules_page()
    ui_steps.save_console_logs()
    # Then
    assert rules_h1 == data["expected_h1_rules"]
    assert rules_table_headers == data["expected_table_headers_rules"]
    # When
    (
        headers_h1,
        headers_table_headers,
    ) = ui_steps.verify_h1_header_and_table_headers_on_headers_page()
    ui_steps.save_console_logs()
    # Then
    assert headers_h1 == data["expected_h1_headers"]
    assert headers_table_headers == data["expected_table_headers_on_headers"]
    # When
    (
        footers_h1,
        footers_table_headers,
    ) = ui_steps.verify_h1_header_and_table_headers_on_footers_page()
    ui_steps.save_console_logs()
    # Then
    assert footers_h1 == data["expected_h1_footers"]
    assert footers_table_headers == data["expected_table_headers_footers"]
    # When
    (
        integrations_h1,
        integrations_table_headers,
    ) = ui_steps.verify_h1_header_and_table_headers_on_integrations_page()
    ui_steps.save_console_logs()
    # Then
    assert integrations_h1 == data["expected_h1_integrations"]
    assert integrations_table_headers == data["expected_table_headers_integrations"]
    ui_steps.assert_status_in_console_logs()
