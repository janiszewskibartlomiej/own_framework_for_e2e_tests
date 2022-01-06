from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.select import Select

from page_objects.base_page import BasePage


class EmailDetailsPage(BasePage):
    FROM_EMAIL_LOCATOR = (By.CSS_SELECTOR, "#report_from_email")
    FROM_NAME_LOCATOR = (By.CSS_SELECTOR, "#report_from_name")
    SUBJECT_LOCATOR = (By.CSS_SELECTOR, "#report_subject")
    BODY_TEXT_LOCATOR = (By.CSS_SELECTOR, "#report_body_text")
    IS_REPLY_LOCATOR = (By.CSS_SELECTOR, "#report_is_reply")
    HAS_ATTACHMENT_LOCATOR = (By.CSS_SELECTOR, "#report_has_attachment")
    ATTACHMENT_NAMES_LOCATOR = (By.CSS_SELECTOR, "#report_attachment_names")
    APP_RATING_LOCATOR = (By.CSS_SELECTOR, "#report_app_rating")
    APP_VERSION_LOCATOR = (By.CSS_SELECTOR, "#report_app_version")
    SENT_REPLY_LOCATOR = (By.CSS_SELECTOR, "#report_sent_message")
    LANGUAGE_LOCATOR = (By.CSS_SELECTOR, "#report_language")
    SELECT_CATEGORY_PREDICTION_LOCATOR = (By.CSS_SELECTOR, "#id_rule_category")
    SELECT_TOPIC_PREDICTION = (By.CSS_SELECTOR, "#id_topic_prediction")
    SELECT_PREDICTIONS_RATING_LOCATOR = (By.CSS_SELECTOR, "#id_rating_status")

    def __init__(self, driver):
        super().__init__(driver)
        self.driver: WebDriver = driver

    def category_prediction(self):
        return Select(self.get_element(by_locator=self.SELECT_CATEGORY_PREDICTION_LOCATOR))

    def topic_prediction(self):
        return Select(self.get_element(by_locator=self.SELECT_TOPIC_PREDICTION))

    def prediction_rating(self):
        return Select(self.get_element(by_locator=self.SELECT_PREDICTIONS_RATING_LOCATOR))

    @property
    def from_email_text(self) -> str:
        return self.get_element_text(by_locator=self.FROM_EMAIL_LOCATOR)

    @property
    def form_name_text(self) -> str:
        return self.get_element_text(by_locator=self.FROM_NAME_LOCATOR)

    @property
    def subject_text(self) -> str:
        return self.get_element_text(by_locator=self.SUBJECT_LOCATOR)

    @property
    def body_text(self) -> str:
        return self.get_element_text(by_locator=self.BODY_TEXT_LOCATOR)

    @property
    def is_reply(self) -> bool:
        src_icon = self.get_src_attribute(by_locator=self.IS_REPLY_LOCATOR)
        return self.icon_is_green(string=src_icon)

    @property
    def has_attachment(self) -> bool:
        src_icon = self.get_src_attribute(by_locator=self.HAS_ATTACHMENT_LOCATOR)
        return self.icon_is_green(string=src_icon)

    @property
    def attachment_names_text(self) -> str:
        return self.get_element_text(by_locator=self.ATTACHMENT_NAMES_LOCATOR)

    @property
    def app_ratting_text(self) -> str:
        return self.get_element_text(by_locator=self.APP_RATING_LOCATOR)

    @property
    def app_version_text(self) -> str:
        return self.get_element_text(by_locator=self.APP_VERSION_LOCATOR)

    @property
    def sent_reply_text(self) -> str:
        return self.get_element_text(by_locator=self.SENT_REPLY_LOCATOR)

    @property
    def language_text(self) -> str:
        return self.get_element_text(by_locator=self.LANGUAGE_LOCATOR)

    @property
    def details_data(self) -> dict:
        return {
            "from_email": self.from_email_text,
            "from_name": self.form_name_text,
            "subject": self.subject_text,
            "body_text": self.body_text,
            "is_reply": self.is_reply,
            "has_attachment": self.has_attachment,
            "attachment_names": self.attachment_names_text,
            "app_rating": self.app_ratting_text,
            "app_version": self.app_version_text,
            "sent_reply": self.sent_reply_text,
            "language": self.language_text,
            "category_prediction": self.category_prediction().first_selected_option.text,
            "category_prediction_is_clickable": self.is_clickable(
                by_locator=self.SELECT_CATEGORY_PREDICTION_LOCATOR
            ),
            "topic_prediction": self.topic_prediction().first_selected_option.text,
            "topic_prediction_is_clickable": self.is_clickable(
                by_locator=self.SELECT_TOPIC_PREDICTION
            ),
            "prediction_rating": self.prediction_rating().first_selected_option.text,
            "prediction_rating_is_clickable": self.is_clickable(
                by_locator=self.SELECT_PREDICTIONS_RATING_LOCATOR
            ),
        }
