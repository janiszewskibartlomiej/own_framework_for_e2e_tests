from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from page_objects.react_top_page_and_table import ReactTopPageAndTable


class ReactHomePage(ReactTopPageAndTable):
    DASHBOARD_HEADERS = (
        By.CSS_SELECTOR,
        ".container-fluid div p:first-child:not(.recharts-tooltip-label),h2",
    )
    H2_HEADERS = (By.CSS_SELECTOR, "h2")

    def __init__(self, driver):
        super().__init__(driver)
        self.driver: WebDriver = driver

    @property
    def headers_content_in_dashboard(self) -> list:
        self.get_element(by_locator=self.H2_HEADERS)
        headers = self.get_all_elements(by_locator=self.DASHBOARD_HEADERS)
        return [el.text for el in headers]
