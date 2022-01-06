import os

from selenium.webdriver.common.by import By

from page_objects.base_page import BasePage
from page_objects.email_details_page import EmailDetailsPage


class ReportsPage(BasePage):
    # schema
    XPATH_FOLLOWING_SIBLING = '//td[contains(text(),"{timestamp}")]/following-sibling::td[{column}]'
    XPATH_TIMESTAMP = '//td[contains(text(),"{timestamp}")]'

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.timestamp = None
        self.email_subject = None
        self.status = None
        self.wait_for_element = int(os.environ.get(key="WAIT_FOR_ELEMENT", default=120))

    # column data locator
    def get_from_email_locator(self) -> tuple:
        xpath = self.XPATH_TIMESTAMP.format(timestamp=self.timestamp) + "/preceding-sibling::td[1]"
        return By.XPATH, xpath

    def get_subject_locator(self) -> tuple:
        xpath = self.XPATH_TIMESTAMP.format(timestamp=self.timestamp)
        return By.XPATH, xpath

    def get_xpath_following_sibling(self, column: int) -> tuple:
        xpath = self.XPATH_FOLLOWING_SIBLING.format(timestamp=self.timestamp, column=column)
        return By.XPATH, xpath

    def get_status_locator(self) -> tuple:
        return self.get_xpath_following_sibling(column=1)

    def get_category_prediction_locator(self) -> tuple:
        return self.get_xpath_following_sibling(column=5)

    def get_rule_locator(self) -> tuple:
        return self.get_xpath_following_sibling(column=7)

    def get_topic_prediction_locator(self) -> tuple:
        return self.get_xpath_following_sibling(column=6)

    def get_app_rating_locator(self) -> tuple:
        return self.get_xpath_following_sibling(column=3)

    def get_app_version_locator(self) -> tuple:
        return self.get_xpath_following_sibling(column=4)

    # columns text
    @property
    def from_email_text(self) -> str:
        return self.get_element_text(by_locator=self.get_from_email_locator())

    @property
    def status_text(self):
        return self.get_element_text(by_locator=self.get_status_locator())

    @property
    def subject_text(self) -> str:
        return self.get_element_text(by_locator=self.get_subject_locator())

    @property
    def app_rating_text(self) -> str:
        return self.get_element_text(by_locator=self.get_app_rating_locator())

    @property
    def app_version_text(self) -> str:
        return self.get_element_text(by_locator=self.get_app_version_locator())

    @property
    def category_prediction_text(self) -> str:
        return self.get_element_text(by_locator=self.get_category_prediction_locator())

    @property
    def topic_prediction_text(self) -> str:
        return self.get_element_text(by_locator=self.get_topic_prediction_locator())

    @property
    def rule_text(self) -> str:
        return self.get_element_text(by_locator=self.get_rule_locator())

    # wait for data
    def wait_for_email(self) -> int:
        self.refreshing_page_and_wait_for_text_in_page_source_n_seconds(
            text_to_verifying=self.email_subject, n_seconds=self.wait_for_element
        )
        time_to_refresh = self.refreshing_page_and_wait_for_element_n_seconds(
            text_to_verifying=self.email_subject,
            by_locators=self.get_subject_locator(),
            n_seconds=self.wait_for_element,
        )
        return time_to_refresh

    def wait_for_all_done_status(self) -> int:
        time_to_refresh = self.refreshing_page_and_wait_for_element_n_seconds(
            text_to_verifying=self.status,
            by_locators=self.get_status_locator(),
            n_seconds=self.wait_for_element,
        )
        return time_to_refresh

    # row data
    @property
    def row_data(self) -> dict:
        return {
            "from_email": self.from_email_text,
            "subject": self.subject_text,
            "status": self.status_text,
            "app_rating": self.app_rating_text,
            "app_version": self.app_version_text,
            "category_prediction": self.category_prediction_text,
            "topic_prediction": self.topic_prediction_text,
            "rule": self.rule_text,
        }

    # details email
    def click_on_email(self) -> EmailDetailsPage:
        self.click_on_and_wait_for_a_new_page(by_locator=self.get_from_email_locator())
        return EmailDetailsPage(driver=self.driver)
