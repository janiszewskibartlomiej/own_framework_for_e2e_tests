import pytest

from steps.ui_steps import UiSteps
from utils.automation_functions import data_generator

test_data: dict = data_generator(test_name="model_trainings")


@pytest.mark.parametrize(
    "data", test_data["data"], ids=test_data["names"],
)
@pytest.mark.trainings
def test_model_trainings_data_page(request, driver, data):
    # Given
    ui_steps: UiSteps = driver.ui_steps
    ui_steps.login_to_admin_panel()
    ui_steps.go_to_trainings_data_page()
    # When
    ui_steps.choice_trainings_version(training_version=data["trainings_version"])
    alert_message = ui_steps.alert_message
    # Then
    assert alert_message == data["expected_alert_message"], "Training failed."
    # When
    ui_steps.login_to_ml_flow()
    ui_steps.wait_for_runs_data_by_trainings_version(training_version=data["trainings_version"])
    icon_status = ui_steps.icon_color
    # Then
    assert icon_status == data["expected_icon_color"], "Icon status is not green/successful"
    # When
    volume_of_status = ui_steps.volume_of_status
    ui_steps.scroll_to_model_directory_and_expand_them()
    length_of_elements_in_model_directory = ui_steps.length_of_elements_in_model_directory
    is_artifact_info_path = ui_steps.is_artifact_info_path
    # Then
    assert volume_of_status == data["expected_status"], "Status in not Finished"
    assert length_of_elements_in_model_directory > 0, "Model directory haven't attachment"
    assert is_artifact_info_path, "Model haven't path in artifact"
