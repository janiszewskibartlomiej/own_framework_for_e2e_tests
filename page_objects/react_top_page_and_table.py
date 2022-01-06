import time

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from page_objects.base_page import BasePage


class ReactTopPageAndTable(BasePage):
    HEADERS_OF_TABLE = (
        By.CSS_SELECTOR,
        "[data-testid='headers_of_table']",
    )
    SEARCH_INPUTS = (By.CSS_SELECTOR, "[data-testid='search_inputs']")
    DASHBOARD_HEADERS = (By.CSS_SELECTOR, ".container-fluid div p:first-child,h2")
    SPINNER_BORDER_LOCATOR = (By.CSS_SELECTOR, ".spinner-border")
    H1_HEADER_LOCATOR = (By.CSS_SELECTOR, "h1")
    LOAD_PAGE_SPINNER_LOCATOR = (By.CSS_SELECTOR, ".splash-spinner")

    def __init__(self, driver):
        super().__init__(driver)
        self.driver: WebDriver = driver

    @property
    def table_headers_list(self) -> list:
        headers = self.get_all_elements(by_locator=self.HEADERS_OF_TABLE)
        return [el.text for el in headers]

    @property
    def search_inputs_list(self) -> list:
        inputs = None
        if self.is_disappeared(by_locator=self.SPINNER_BORDER_LOCATOR):
            inputs = self.get_all_elements(by_locator=self.SEARCH_INPUTS)
        return [el.text for el in inputs]

    @property
    def h1_header(self) -> str:
        if self.is_disappeared(by_locator=self.LOAD_PAGE_SPINNER_LOCATOR):
            while not self.page_is_loading():
                time.sleep(0.2)
            return self.get_element_text(by_locator=self.H1_HEADER_LOCATOR)
