import os
import re
import time

from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.common.by import By

import utils.constants as const
from page_objects.base_page import BasePage
from utils.automation_functions import get_email_objects, wait


class ZendeskPage(BasePage):
    USER_EMAIL = (By.CSS_SELECTOR, "#user_email")
    USER_PASSWORD = (By.CSS_SELECTOR, "#user_password")
    SIGN_IN_BUTTON = (By.CSS_SELECTOR, "#sign-in-submit-button")
    HOME_VIEW_BUTTON = (By.CSS_SELECTOR, "#ember1597")
    DASHBOARD_BUTTON = (By.CSS_SELECTOR, "button[value='dashboard']")
    TAG_ON_HEADER_TICKET_VIEW = (By.CSS_SELECTOR, "a[role='menuitem']")
    TAG_VALUE_ON_TAGS_INPUT_ON_TICKET_VIEW = (By.CSS_SELECTOR, "li[class='zd-tag-item']")
    MESSAGE_SEND_TO_ZENDESK_TICKET_VIEW = (By.CSS_SELECTOR, "div[class~='zd-comment']")
    RESPONSE_MESSAGE_CONTENT_ON_TICKET_VIEW = (By.CSS_SELECTOR, "div[class='zd-comment']")
    REQUESTER_UPDATED_SORT_LINK = (By.XPATH, "// span[text() = 'Requester updated']")
    TICKET_STATUS_LABEL = (By.CSS_SELECTOR, "span.ticket_status_label.toolbar")
    SUBJECT_IN_MESSAGE = (By.CSS_SELECTOR, "input[data-test-id='omni-header-subject']")

    def __init__(self, driver):
        super().__init__(driver)
        self.driver: webdriver.Chrome = driver

        self.base_url = os.environ.get("ZENDESK_SERVER_DOMAIN")
        self.driver.get(self.base_url)

        self.driver.switch_to.frame(0)

        self.login_as(
            username_locator=self.USER_EMAIL,
            username=os.environ.get("ZENDESK_SERVER_LOGIN"),
            password_locator=self.USER_PASSWORD,
            password=os.environ.get("ZENDESK_SERVER_PASSWORD"),
            button_locator=self.SIGN_IN_BUTTON,
            enter_key=True,
        )

        while const.ZENDESK_DASHBOARD_ENDPOINT not in self.driver.current_url:
            self.driver.get(self.base_url + const.ZENDESK_DASHBOARD_ENDPOINT)

    @staticmethod
    def get_subject_locator_by_timestamp(timestamp: int) -> tuple:
        xpath = f"//span[contains(text(),'{timestamp}')]"
        subject_locator = (By.XPATH, xpath)
        return subject_locator

    @staticmethod
    def get_tag_locator_by_timestamp(timestamp: int) -> tuple:
        xpath = (
            f"(//span[contains(text(),'{timestamp}')]/ancestor::td/preceding-sibling::td/div)[3]"
        )
        subject_locator = (By.XPATH, xpath)
        return subject_locator

    def get_endpoint_href_by_timestamp_on_subject_message(self, timestamp: int):
        xpath = f"//span[contains(text(),'{timestamp}')]/parent::a"
        subject_locator = (By.XPATH, xpath)
        href: str = self.get_element(by_locator=subject_locator).get_attribute("href")
        endpoint = re.search("tickets/\d+", href)
        return endpoint.group()

    def refreshing_page_and_wait_for_element_text_n_seconds(
            self, text_to_verifying: str, by_locators: tuple, n_seconds: int, sort_link: bool
    ) -> int:
        time_to_refresh = None
        start_time = time.time().__int__()
        web_element = self.get_element(by_locator=by_locators)

        find_timestamp_in_locator = re.findall(r"\d+", by_locators[1])
        if find_timestamp_in_locator:
            timestamp = find_timestamp_in_locator[-1]
        else:
            subject_text = self.get_value_from_element_by_query_selector(
                by_locator=self.SUBJECT_IN_MESSAGE
            )
            find_timestamp = re.findall(r"\d+", subject_text)
            timestamp = find_timestamp[-1]

        while text_to_verifying != web_element.text:
            time.sleep(1)
            self.driver.refresh()

            if sort_link:
                self.click_on(self.REQUESTER_UPDATED_SORT_LINK)

            web_element = self.get_element(by_locator=by_locators)
            end_time = time.time().__int__()
            time_to_refresh = end_time - start_time
            if time_to_refresh < n_seconds:
                continue
            else:
                break

        if sort_link:
            print(
                f"Wait for email #{timestamp}# in zendesk dashboard = {time_to_refresh or 0} second"
            )
        else:
            print(
                f"Wait for email #{timestamp}# in zendesk message = {time_to_refresh or 0} second"
            )

        return time_to_refresh

    def refreshing_page_and_wait_for_message_in_page_source_n_seconds(
            self, text_to_verifying: str, n_seconds: int
    ):
        start_time = time.time().__int__()
        while text_to_verifying not in self.driver.page_source:
            time.sleep(1)
            self.driver.refresh()
            self.click_on(by_locator=self.REQUESTER_UPDATED_SORT_LINK)
            end_time = time.time().__int__()
            time_to_refresh = end_time - start_time
            if time_to_refresh < n_seconds:
                continue
            else:
                msg = f"Refreshing time is more then {n_seconds} seconds"
                raise exceptions.TimeoutException(msg=msg)

    def get_background_color_from_content_message(self):
        color_background = self.driver.execute_script(
            """const element =  document.querySelectorAll("div[class='zd-comment']");
            let color = getComputedStyle(element[element.length -1].parentElement.parentElement).backgroundColor;
            return color;"""
        )
        return color_background

    def get_border_style_from_content_message(self):
        border: str = self.driver.execute_script(
            """const element =  document.querySelectorAll("div[class='zd-comment']");
            let borderStyle = getComputedStyle(element[element.length -1].parentElement.parentElement).border;
            return borderStyle;"""
        )
        border_list_parameters = border.split(" ")

        border_color = " ".join(border_list_parameters[2:])

        border_style: dict = {
            "Style": border_list_parameters[1],
            "Color": border_color,
        }
        return border_style

    def get_tag_shortcut_from_dashboard(self, subject_endpoint: str) -> str:
        value = self.driver.execute_script(
            f"""const element =  document.querySelector("a[href='{subject_endpoint}']");
            return element.parentElement.previousElementSibling.previousElementSibling.innerText;"""
        )
        return value

    def get_tag_shortcut_from_dashboard_page(self, by_subject: str) -> str:
        value = self.driver.execute_script(
            f"const element =  $(\"span:contains('{by_subject}')\");"
            "return element[0].parentElement.parentElement.previousElementSibling.previousElementSibling.innerText;"
        )
        return value

    @staticmethod
    def get_auto_response_message(subject) -> list:
        email_objects = get_email_objects(
            host=os.environ.get("SMTP_SERVER"),
            user=os.environ.get("SENDER_EMAIL"),
            password=os.environ.get("EMAIL_PASSWORD"),
            port=os.environ.get("IMAP_PORT"),
        )

        while not email_objects:
            wait(3)

        messages = []

        for email in email_objects:
            if (
                    subject in email.title
                    and os.environ.get("ZENDESK_SERVER_EMAIL") in email.return_path
            ):
                email_body: str = email.body
                split_message = email_body.split("----------------------------------------------")
                messages.append(split_message[1].replace("*", ""))

        return messages
