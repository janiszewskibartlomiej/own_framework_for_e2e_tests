import os
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from page_objects.base_page import BasePage
from utils.automation_functions import (
    data_loader,
    save_to_json,
    get_path_to_file_in_test_reports_by_current_date,
)
from utils.paths_builder import data_folder_path


class Sitemap(BasePage):
    ALL_HREF_WITHOUT_BASE_LOCATOR = (By.CSS_SELECTOR, "a[href]:not([href='\/'])")
    ACTIVE_ARROW_NEXT_PAGE_LOCATOR = (
        By.CSS_SELECTOR,
        "button[aria-label='Next page']:not([disabled])",
    )
    SPINNER_BORDER_LOCATOR = (By.CSS_SELECTOR, ".MuiPaper-root div.spinner-border")

    def __init__(self, driver):
        super().__init__(driver)
        self.driver: WebDriver = driver

    @property
    def href_list(self) -> list:
        all_elements = self.get_all_elements(by_locator=self.ALL_HREF_WITHOUT_BASE_LOCATOR)
        return [
            el.get_attribute("href")
            for el in all_elements
            if os.environ.get("REACT_BASE_URL").split(".")[-2] in el.get_attribute("href")
               and "http" in el.get_attribute("href")
        ]

    def click_on_active_arrow_next_page(self) -> None:
        if self.element_is_on_a_page(by_locator=self.ACTIVE_ARROW_NEXT_PAGE_LOCATOR):
            self.scroll_to_invisible_element(target=self.ACTIVE_ARROW_NEXT_PAGE_LOCATOR)
            self.click_on(by_locator=self.ACTIVE_ARROW_NEXT_PAGE_LOCATOR)
            self.element_is_not_visible(by_locator=self.SPINNER_BORDER_LOCATOR)

    def get_new_sitemap_from_endpoints(self, all_endpoints) -> list:
        endpoints_list = []
        urls = data_loader(test_name="endpoints_from_home_page")
        for url in urls["sitemap"]:
            self.driver.get(url=url)
            self.element_is_not_visible(by_locator=self.SPINNER_BORDER_LOCATOR)
            endpoints_list.extend(self.href_list)
            if all_endpoints:
                while self.element_is_on_a_page(by_locator=self.ACTIVE_ARROW_NEXT_PAGE_LOCATOR):
                    self.click_on_active_arrow_next_page()
                    endpoints_list.extend(self.href_list)
        return endpoints_list

    @staticmethod
    def save_sitemap_to_json(data: dict, name: str) -> str:
        target = f"{data_folder_path()}{os.sep}{name}.json"
        save_to_json(data=data, path=target)
        return target

    @staticmethod
    def save_console_logs_to_json(data: dict) -> str:
        path = get_path_to_file_in_test_reports_by_current_date(
            name=f"console_logs_{int(time.time() * 1000)}.json"
        )
        save_to_json(data=data, path=path)
        return path
