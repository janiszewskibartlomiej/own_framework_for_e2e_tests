import os

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webdriver import WebElement

from page_objects.react_message_details_page import ReactMessageDetailsPage
from page_objects.react_top_page_and_table import ReactTopPageAndTable


class ReactMessagePage(ReactTopPageAndTable):
    SHOW_DETAILS_LINK_TEXT_LOCATOR = (By.CSS_SELECTOR, "[data-testid='show_details_link']")
    SHOW_ROWS_PAGE_LOCATOR = (By.CSS_SELECTOR, "[data-testid='show_rows_page']")

    def __init__(self, driver):
        super().__init__(driver)
        self.driver: WebDriver = driver
        self.message_page_url = os.environ.get("REACT_BASE_URL") + "reports"

    def go_to_general_messages_page(self) -> None:
        self.driver.get(url=self.message_page_url)

    def click_on_show_details_by_row(self, index_row) -> ReactMessageDetailsPage:
        elements: list = self.get_all_elements(by_locator=self.SHOW_DETAILS_LINK_TEXT_LOCATOR)
        target: WebElement = elements[index_row]
        target.click()
        return ReactMessageDetailsPage(driver=self.driver)

    @property
    def number_of_show_details(self) -> int:
        return len(self.get_all_elements(by_locator=self.SHOW_DETAILS_LINK_TEXT_LOCATOR))

    @property
    def rows_page(self) -> int:
        return int(self.get_visible_text_in_select_input(by_locator=self.SHOW_ROWS_PAGE_LOCATOR))
