from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from page_objects.react_top_page_and_table import ReactTopPageAndTable


class ReactMessageDetailsPage(ReactTopPageAndTable):
    H1_HEADER_LOCATOR = (By.CSS_SELECTOR, "div.container-fluid > h1")
    RIGHT_ARROW_IN_CONTENT = (By.CSS_SELECTOR, "svg.iEfbRH")
    CONTENTS_DIV_SCHEMA = (
        "//div[@class='container-fluid'] / h1//following-sibling::div/ div[{number_of_content}]"
    )
    FIRST_CONTENT_LOCATOR = (By.CSS_SELECTOR, "[data-testid='first_content']")
    SECOND_CONTENT_LOCATOR = (By.CSS_SELECTOR, "[data-testid='second_content']")
    DATETIME_IN_CONTENT_LOCATOR = (By.CSS_SELECTOR, "[data-testid = 'datetime_in_content']")
    CONTENT_LOCATOR = (By.CSS_SELECTOR, "data-testid='contents_div'")

    def __init__(self, driver):
        super().__init__(driver)
        self.driver: WebDriver = driver

    def right_arrow_is_clickable(self) -> bool:
        text = self.get_element_text(by_locator=self.DATETIME_IN_CONTENT_LOCATOR)
        list_of_pages = text.split(" ")
        if list_of_pages[0] != list_of_pages[2]:
            return True
        else:
            return False

    def click_on_right_arrow_in_content(self) -> None:
        if self.element_is_visible(by_locator=self.DATETIME_IN_CONTENT_LOCATOR):
            current_page = self.get_current_url()
            self.hover_to_and_click(by_locator=self.RIGHT_ARROW_IN_CONTENT)
            self.wait_for_new_page(current_page=current_page)

    def verify_contents_are_visible(self) -> bool:
        self.element_is_visible(by_locator=self.DATETIME_IN_CONTENT_LOCATOR)
        first_is_visible = self.element_is_visible(by_locator=self.FIRST_CONTENT_LOCATOR)
        first_have_content: str = self.get_element_text(by_locator=self.FIRST_CONTENT_LOCATOR)
        second_is_visible = self.element_is_visible(by_locator=self.SECOND_CONTENT_LOCATOR)
        second_have_content = self.get_element_text(by_locator=self.SECOND_CONTENT_LOCATOR)
        first = bool(len(first_have_content.replace("\n", "")) > 50) and first_is_visible
        second = bool(len(second_have_content.replace("\n", "")) > 100) and second_is_visible
        return first and second
