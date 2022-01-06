import os

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from page_objects.base_page import BasePage


class TrainingsDataPage(BasePage):
    CHECKBOX_IN_HEADER_LOCATOR = (By.CSS_SELECTOR, "thead span.form-check-sign span")
    GEAR_BUTTON_LOCATOR = (
        By.CSS_SELECTOR,
        "button[class~='dropdown-toggle'] > i.tim-icons",
    )
    SELECT_ALL_ITEMS_lINK_LOCATOR = (By.ID, "select-all")
    SELECTED_ALL_ITEMS_LINK_LOCATOR = (By.XPATH, "//p[text()='Selected all items']")

    # dropdown
    DROPDOWN_LOCATOR = (By.CSS_SELECTOR, "ul[x-placement='bottom-end']")
    TRAIN_NEW_CATEGORISATION_MODEL_LOCATOR = (
        By.CSS_SELECTOR,
        "a[data-url='/trainingdata/train-new-categorisation-model/']",
    )

    TRAIN_NEW_TOPIC_CLASSIFICATION_MODEL_LOCATOR = (
        By.CSS_SELECTOR,
        "a[data-url='/trainingdata/training-data-train-new-topic-classification-model/']",
    )

    TRAIN_NEW_SENTIMENT_CLASSIFICATION_MODEL_LOCATOR = (
        By.CSS_SELECTOR,
        "a[data-url='/trainingdata/training-data-train-new-sentiment-classification-model/']",
    )

    def __init__(self, driver):
        super().__init__(driver)
        self.driver: WebDriver = driver
        self.wait_for_element = int(os.getenv(key="WAIT_FOR_ELEMENT_N_SECONDS", default="60"))

    def mark_checkbox_all_rows(self) -> None:
        self.driver.execute_script(
            f"const checkbox = document.querySelector('{self.CHECKBOX_IN_HEADER_LOCATOR[1]}');"
            "checkbox.click();"
        )

    def select_all_items_link(self) -> None:
        self.click_on(by_locator=self.SELECT_ALL_ITEMS_lINK_LOCATOR)
        WebDriverWait(driver=self.driver, timeout=self.wait_for_element).until(
            EC.visibility_of_element_located(locator=self.SELECTED_ALL_ITEMS_LINK_LOCATOR)
        )

    def click_on_gear(self) -> None:
        self.click_on(by_locator=self.GEAR_BUTTON_LOCATOR)

    def click_on_train_new_categorisation_model(self) -> None:
        self.driver.execute_script(
            f'const el = document.querySelector("{self.TRAIN_NEW_CATEGORISATION_MODEL_LOCATOR[1]}");'
            "el.click()"
        )

    def click_on_train_new_topic_classification_model(self) -> None:
        self.driver.execute_script(
            f'const el = document.querySelector("{self.TRAIN_NEW_TOPIC_CLASSIFICATION_MODEL_LOCATOR[1]}");'
            "el.click()"
        )

    def click_on_train_new_sentiment_model(self) -> None:
        self.driver.execute_script(
            f'const el = document.querySelector("{self.TRAIN_NEW_SENTIMENT_CLASSIFICATION_MODEL_LOCATOR[1]}");'
            "el.click()"
        )

    def wait_for_alert_and_accept(self) -> None:
        WebDriverWait(driver=self.driver, timeout=self.wait_for_element).until(
            EC.alert_is_present()
        )
        alert_object = self.driver.switch_to.alert
        alert_object.accept()
        WebDriverWait(driver=self.driver, timeout=self.wait_for_element).until_not(
            EC.alert_is_present()
        )

    def wait_for_alert_and_get_message(self) -> str:
        WebDriverWait(driver=self.driver, timeout=self.wait_for_element).until(
            EC.alert_is_present()
        )
        alert_object = self.driver.switch_to.alert
        alert_message = alert_object.text
        alert_object.accept()
        return alert_message
