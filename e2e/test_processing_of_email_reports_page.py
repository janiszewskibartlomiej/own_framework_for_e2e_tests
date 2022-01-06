import pytest

from steps.ui_steps import UiSteps
from utils.automation_functions import data_generator

test_data: dict = data_generator(test_name="processing_of_email")


@pytest.mark.parametrize(
    "data", test_data["data"], ids=test_data["names"],
)
@pytest.mark.messages
def test_processing_of_email_message_reports_page(request, driver, data: dict):
    # Given
    ui_steps: UiSteps = driver.ui_steps
    email_data = ui_steps.send_email(
        subject=data["subject"],
        message_content=data["body_text"],
        files_path=data["attachment_names"],
    )
    data["expected_subject"] = email_data["subject"]
    ui_steps.login_to_admin_panel()
    ui_steps.go_to_reports_page(
        timestamp=email_data["timestamp"],
        subject=email_data["subject"],
        status=data["expected_status"],
    )
    # When
    ui_steps.wait_for_email_and_all_done_status()
    columns_data = ui_steps.row_data_from_columns_in_reports_page
    # Then
    assert columns_data["from_email"] == data["expected_from_email"]
    assert columns_data["subject"] == data["expected_subject"]
    assert columns_data["status"] == data["expected_status"]
    assert columns_data["app_rating"] == data["expected_app_rating"]
    assert columns_data["app_version"] == data["expected_app_version"]
    assert columns_data["category_prediction"] == data["expected_category_prediction"]
    assert columns_data["topic_prediction"] == data["expected_topic_prediction"]
    assert columns_data["rule"] == data["expected_rule"]
    # When
    ui_steps.go_to_email_details()
    email_details_data = ui_steps.email_details_data
    # Then
    assert email_details_data["from_email"] == data["expected_from_email"]
    assert email_details_data["from_name"] == data["expected_from_name"]
    assert email_details_data["subject"] == email_data["subject"]
    assert email_details_data["body_text"] == data["expected_body_text"]
    assert email_details_data["is_reply"] == data["expected_is_reply"]
    assert email_details_data["has_attachment"] == data["expected_has_attachment"]
    assert email_details_data["attachment_names"] == data["expected_attachment_names"]
    assert email_details_data["app_rating"] == data["expected_app_rating"]
    assert email_details_data["app_version"] == data["expected_app_version"]
    assert email_details_data["sent_reply"] == data["expected_sent_reply"]
    assert email_details_data["language"] == data["expected_language"]
    assert email_details_data["category_prediction"] == data["expected_category_prediction"]
    assert email_details_data["category_prediction_is_clickable"] == data["expected_is_clickable"]
    assert email_details_data["topic_prediction"] == data["expected_topic_prediction"]
    assert email_details_data["topic_prediction_is_clickable"] == data["expected_is_clickable"]
    assert email_details_data["prediction_rating"] == data["expected_predictions_rating"]
    assert email_details_data["prediction_rating_is_clickable"] == data["expected_is_clickable"]
