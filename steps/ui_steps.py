import os
import time

import utils.constants as const
from page_objects.base_page import BasePage
from page_objects.email_details_page import EmailDetailsPage
from page_objects.ml_flow_page import MlFlowPage
from page_objects.react_categories_page import ReactCategoriesPage
from page_objects.react_footers_page import ReactFootersPage
from page_objects.react_headers_page import ReactHeadersPage
from page_objects.react_home_page import ReactHomePage
from page_objects.react_import_data_page import ReactImportDataPage
from page_objects.react_integrations_page import ReactIntegrationsPage
from page_objects.react_left_menu import ReactLeftMenu
from page_objects.react_login_page import ReactLoginPage
from page_objects.react_message_details_page import ReactMessageDetailsPage
from page_objects.react_message_page import ReactMessagePage
from page_objects.react_models_page import ReactModelsPage
from page_objects.react_rules_page import ReactRulesPage
from page_objects.react_topics_page import ReactTopicsPage
from page_objects.react_trainings_data_page import ReactTrainingsDataPage
from page_objects.reports_page import ReportsPage
from page_objects.sitemap import Sitemap
from utils.automation_functions import (
    print_message_in_color,
    removing_directories_in_reports_by_number_of_day,
    send_email,
    check_status_code_in_dict,
)
from utils.decorator import step


class UiSteps:
    def __init__(self, driver):
        self.driver = driver
        self.current_page = None
        self.logs = {}
        self.sitemap = {"sitemap": []}

    # region common methods
    @step(name='>> Screenshot is done; Path >> "{}" <<', use_return=True)
    def do_screenshot(self, name) -> str:
        self.current_page = BasePage(driver=self.driver)
        path = self.current_page.do_screenshot(name=name)
        print_message_in_color(
            message=f'>> Screenshot is done; Path >> "{path}" <<', rgb_color="249,215,28",
        )
        return path

    @property
    def clean_test_reports(self) -> str:
        removed_directories = removing_directories_in_reports_by_number_of_day()
        return removed_directories

    def send_email(
            self, subject, message_content, files_path, number_sent_email=1, send_copy=None
    ) -> dict:
        email_data = send_email(
            subject=subject,
            message_content=message_content,
            send_copy=send_copy,
            files_path=files_path,
            number_sent_email=number_sent_email,
        )
        return email_data

    def save_console_logs(self) -> None:
        self.current_page = BasePage(driver=self.driver)
        self.current_page.get_console_logs(logs=self.logs)

    def assert_status_in_console_logs(self):
        check_status_code_in_dict(logs=self.logs)

    # end region common methods

    # region trainings
    @step(name='>> Successful choice and accept training "{}" <<', use_args=True)
    def choice_trainings_version(self, training_version) -> None:
        self.current_page.mark_checkbox_all_rows()
        self.current_page.select_all_items_link()
        self.current_page.click_on_gear()

        if training_version == const.CATEGORIZATION_MODEL:
            self.current_page.click_on_train_new_categorisation_model()

        elif training_version == const.TOPIC_CLASSIFICATION_MODEL:
            self.current_page.click_on_train_new_topic_classification_model()

        elif training_version == const.SENTIMENT_CLASSIFICATION_MODEL:
            self.current_page.click_on_train_new_sentiment_model()

        self.current_page.wait_for_alert_and_accept()

    @step(name='>> Alert message is "{}" <<', use_return=True)
    @property
    def alert_message(self) -> str:
        alert_message = self.current_page.wait_for_alert_and_get_message()
        return alert_message

    @step(name=">> Successful login to ml flow page <<")
    def login_to_ml_flow(self) -> None:
        self.current_page = MlFlowPage(driver=self.driver)
        self.current_page.login_to_ml_flow_page()

    @step(name='>> Runs data is visible for trainings version = "{placeholder}" <<', use_args=True)
    def wait_for_runs_data_by_trainings_version(self, training_version: str) -> None:
        if training_version == const.CATEGORIZATION_MODEL:
            self.current_page.click_on_category_classification_in_sidebar()

        elif training_version == const.TOPIC_CLASSIFICATION_MODEL:
            self.current_page.click_on_topic_classification_in_sidebar()

        elif training_version == const.SENTIMENT_CLASSIFICATION_MODEL:
            self.current_page.click_on_sentiment_classification_in_sidebar()

        self.current_page.wait_for_runs_data()

    @step(name='>> Icon color is "{}" <<', use_return=True)
    @property
    def icon_color(self) -> str:
        icon_color = self.current_page.color_of_icon
        return icon_color

    @step(name=">> I'm scrolling to model directory <<")
    def scroll_to_model_directory_and_expand_them(self) -> None:
        self.current_page.scroll_to_model_directory_and_click_on()

    @step(name='>> Length of model directory is "{}" <<', use_return=True)
    @property
    def length_of_elements_in_model_directory(self) -> int:
        current_element: list = self.current_page.elements_in_model_directory
        length = len(current_element)
        return length

    @step(name='>> Status is "{}" <<', use_return=True)
    @property
    def volume_of_status(self) -> str:
        self.current_page.click_on_green_icon()
        status = self.current_page.volume_of_status
        return status

    @step(name='>> Is artifact info path visible "{}" <<', use_return=True)
    def is_artifact_info_path(self) -> bool:
        is_artifact = self.current_page.is_artifact_info_path_visible()
        return is_artifact

    # end region trainings

    # region reports
    @step(name=">> Successful get data from columns in reports page <<")
    @property
    def row_data_from_columns_in_reports_page(self) -> dict:
        self.current_page: ReportsPage
        data = self.current_page.row_data
        return data

    @step(name="Wait for email #{}# = {} seconds \nand wait for all done status = {} seconds", use_return=True)
    def wait_for_email_and_all_done_status(self) -> tuple:
        self.current_page: ReportsPage
        wait_for_email = self.current_page.wait_for_email()
        wait_for_status = self.current_page.wait_for_all_done_status()
        return self.current_page.timestamp, wait_for_email, wait_for_status

    # end region reports

    # region email details
    @step(name=">> Successful go to  email details <<")
    def go_to_email_details(self) -> None:
        self.current_page: ReportsPage
        self.current_page = self.current_page.click_on_email()

    @step(name=">> Successful get data from email details page <<")
    @property
    def email_details_data(self) -> dict:
        self.current_page: EmailDetailsPage
        data = self.current_page.details_data
        return data

    # end region email details

    # region load test
    @step(name="Emails list = {}")
    def send_repeat_emails(
            self,
            subject,
            message_content,
            files_path,
            send_copy=None,
            repeat=int(os.environ.get(key="REPEAT_SEND_EMAIL", default="99")),
    ) -> list:
        emails_list = []

        index = 1
        for _ in range(1, repeat + 1):
            email_data = send_email(
                subject=subject,
                message_content=message_content,
                send_copy=send_copy,
                files_path=files_path,
                number_sent_email=index,
            )
            index += 1
            time.sleep(0.1)
            emails_list.append(email_data)

        print_message_in_color(
            message=f"Sum of send emails = {emails_list.__len__()}, \n emails list = {emails_list}",
            rgb_color="229,190,001",
        )
        return emails_list

    # end region load test

    # region tests react login
    @step(name=">> Successful visit react login page <<")
    def go_to_react_login_page(self) -> None:
        self.current_page = ReactLoginPage(driver=self.driver)
        self.current_page.go_to_login_page()

    @step(name=">> Successful login to react homepage <<")
    def login_to_react_homepage(
            self,
            enter_key,
            user=os.environ.get("LOGIN_ADMIN_PANEL"),
            password=os.environ.get("PASSWORD_ADMIN_PANEL"),
    ) -> None:
        self.current_page = ReactLoginPage(driver=self.driver)
        self.current_page = self.current_page.login(
            enter_key=enter_key, user=user, password=password
        )

    @step(name=">> Successful get text from rules link <<")
    @property
    def rules_link_text(self) -> str:
        self.current_page = ReactLeftMenu(driver=self.driver)
        self.current_page.click_on_automation_dropdown()
        text = self.current_page.rules_link_text
        return text

    @step(name=">> Successful get text from alert message <<")
    @property
    def react_login_alert_text(self) -> str:
        self.current_page = ReactLoginPage(driver=self.driver)
        text = self.current_page.alert_message
        return text

    # end tests react login

    # region tests react menu
    @step(name=">> Successful get h1 header home page and headers content <<")
    def verify_h1_header_and_headers_content_on_home_page(self) -> tuple:
        self.current_page: ReactHomePage
        current_h1 = self.current_page.h1_header
        current_content: list = self.current_page.headers_content_in_dashboard
        result = current_h1, current_content
        return result

    @step(name=">> Successful get h1 and headers of inputs search on message page <<")
    def verify_h1_header_and_headers_of_inputs_search_on_messages_page(self) -> tuple:
        self.current_page = ReactLeftMenu(driver=self.driver)
        self.current_page: ReactMessagePage = self.current_page.click_on_general_link()
        current_h1 = self.current_page.h1_header
        search_inputs = self.current_page.search_inputs_list
        result = current_h1, search_inputs
        return result

    @step(name=">> Successful get h1 header and headers of inputs search and table headers on trainings data page <<")
    def verify_h1_header_and_headers_of_inputs_search_and_table_headers_on_trainings_data_page(
            self,
    ) -> tuple:
        self.current_page = ReactLeftMenu(driver=self.driver)
        self.current_page.click_on_data_and_models_dropdown()
        self.current_page: ReactTrainingsDataPage = self.current_page.click_on_trainings_data_link()
        current_h1 = self.current_page.h1_header
        search_inputs = self.current_page.search_inputs_list
        table_headers = self.current_page.table_headers_list
        result = current_h1, search_inputs, table_headers
        return result

    @step(name=">> Successful get h1 header and table headers on import data page <<")
    def verify_h1_header_and_table_headers_on_import_data_page(self) -> tuple:
        self.current_page = ReactLeftMenu(driver=self.driver)
        self.current_page: ReactImportDataPage = self.current_page.click_on_import_data_link()
        current_h1 = self.current_page.h1_header
        table_headers = self.current_page.table_headers_list
        result = current_h1, table_headers
        return result

    @step(name=">> Successful get h1 header ans table headers on models page <<")
    def verify_h1_header_and_table_headers_on_models_page(self) -> tuple:
        self.current_page = ReactLeftMenu(driver=self.driver)
        self.current_page: ReactModelsPage = self.current_page.click_on_models_link()
        current_h1 = self.current_page.h1_header
        table_headers = self.current_page.table_headers_list
        result = current_h1, table_headers
        return result

    @step(name=">> Successful get h1 header and table headers on categories page <<")
    def verify_h1_header_and_table_headers_on_categories_page(self) -> tuple:
        self.current_page = ReactLeftMenu(driver=self.driver)
        self.current_page.click_on_automation_dropdown()
        self.current_page: ReactCategoriesPage = self.current_page.click_on_categories_link()
        current_h1 = self.current_page.h1_header
        table_headers = self.current_page.table_headers_list
        result = current_h1, table_headers
        return result

    @step(name=">> Successful get h1 header and table headers on topic page <<")
    def verify_h1_header_and_table_headers_on_topics_page(self) -> tuple:
        self.current_page = ReactLeftMenu(driver=self.driver)
        self.current_page: ReactTopicsPage = self.current_page.click_on_topics_link()
        current_h1 = self.current_page.h1_header
        table_headers = self.current_page.table_headers_list
        result = current_h1, table_headers
        return result

    @step(name=">> Successful get h1 header and table headers on rules page <<")
    def verify_h1_header_and_table_headers_on_rules_page(self) -> tuple:
        self.current_page = ReactLeftMenu(driver=self.driver)
        self.current_page: ReactRulesPage = self.current_page.click_on_rules_link()
        current_h1 = self.current_page.h1_header
        table_headers = self.current_page.table_headers_list
        result = current_h1, table_headers
        return result

    @step(name=">> Successful get h1 header and table headers on headers page <<")
    def verify_h1_header_and_table_headers_on_headers_page(self) -> tuple:
        self.current_page = ReactLeftMenu(driver=self.driver)
        self.current_page.click_on_message_templates_dropdown()
        self.current_page: ReactHeadersPage = self.current_page.click_on_headers_link()
        current_h1 = self.current_page.h1_header
        table_headers = self.current_page.table_headers_list
        result = current_h1, table_headers
        return result

    @step(name=">> Successful get h1 header and table headers on footers page <<")
    def verify_h1_header_and_table_headers_on_footers_page(self) -> tuple:
        self.current_page = ReactLeftMenu(driver=self.driver)
        self.current_page: ReactFootersPage = self.current_page.click_on_footers_link()
        current_h1 = self.current_page.h1_header
        table_headers = self.current_page.table_headers_list
        result = current_h1, table_headers
        return result

    @step(name=">> Successful get h1 header and table headers on integrations page <<")
    def verify_h1_header_and_table_headers_on_integrations_page(self) -> tuple:
        self.current_page = ReactLeftMenu(driver=self.driver)
        self.current_page.click_on_settings_dropdown()
        self.current_page: ReactIntegrationsPage = self.current_page.click_on_integrations_link()
        current_h1 = self.current_page.h1_header
        table_headers = self.current_page.table_headers_list
        result = current_h1, table_headers
        return result

    @step(name=">> Successful go to message page <<")
    def go_to_general_messages_page(self) -> None:
        self.current_page = ReactMessagePage(driver=self.driver)
        self.current_page.go_to_general_messages_page()

    # end region tests react menu

    # region tests react message details
    @step(name=">> Successful get number of rows page = {} <<", use_return=True)
    @property
    def rows_page(self) -> int:
        self.current_page = ReactMessagePage(driver=self.driver)
        rows = self.current_page.rows_page
        return rows

    @step(name=">> Successful get number of show details link text = {} <<")
    @property
    def number_of_show_details(self) -> int:
        self.current_page = ReactMessagePage(driver=self.driver)
        number = self.current_page.number_of_show_details
        return number

    @step(name=">> Successful go to message details page by index row = {} <<", use_args=True)
    def go_to_message_details_page(self, index_row) -> None:
        self.current_page = ReactMessagePage(driver=self.driver)
        current_page = self.current_page.get_current_url()
        self.current_page = self.current_page.click_on_show_details_by_row(index_row=index_row)
        self.current_page.wait_for_new_page(current_page=current_page)

    @step(name=">> Right arrow is clickable in message details<<")
    def right_arrow_is_clickable_in_message_details(self) -> bool:
        self.current_page: ReactMessageDetailsPage
        return self.current_page.right_arrow_is_clickable()

    @step(name=">> Successful get h1 header and verify contents text on message details page <<")
    def verify_h1_header_and_content_on_message_details_page(self) -> tuple:
        self.current_page = ReactMessageDetailsPage(driver=self.driver)
        current_h1 = self.current_page.h1_header
        contents_have_text = self.current_page.verify_contents_are_visible()
        return current_h1, contents_have_text

    @step(name=">> Successful click on right arrow in content on message details<<")
    def click_on_right_arrow_in_content_on_message_details_page(self) -> None:
        self.current_page: ReactMessageDetailsPage
        self.current_page.click_on_right_arrow_in_content()

    # region test by sitemap

    @step(name=">> Successful get href list from home page and save endpoints")
    def get_href_list_from_home_page(self) -> list:
        self.current_page = Sitemap(driver=self.driver)
        href = self.current_page.href_list
        self.sitemap["sitemap"].extend(href)
        self.sitemap["sitemap"] = list(set(self.sitemap["sitemap"]))
        self.current_page.save_sitemap_to_json(
            data=self.sitemap, name="test_data_endpoints_from_home_page"
        )
        return href

    @step(name=">> Successful build sitemap and save file, \n path: {}<<", use_return=True)
    def build_sitemap_from_endpoints(self, all_endpoints=False) -> str:
        self.current_page: Sitemap
        sitemap_list = self.current_page.get_new_sitemap_from_endpoints(all_endpoints=all_endpoints)
        self.sitemap["sitemap"].extend(sitemap_list)
        self.sitemap["sitemap"] = list(set(self.sitemap["sitemap"]))

        path = self.current_page.save_sitemap_to_json(data=self.sitemap, name="sitemap")
        return path

    def get_all_console_logs_from_sitemap(self) -> None:
        for url in self.sitemap["sitemap"]:
            try:
                self.driver.get(url=url)
                self.save_console_logs()
            except Exception:
                print(f"Error Handler in url {url}")
                Sitemap.save_console_logs_to_json(data=self.logs)
                continue
        Sitemap.save_console_logs_to_json(data=self.logs)
