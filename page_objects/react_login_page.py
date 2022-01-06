import os

from selenium.webdriver.common.by import By

from page_objects.base_page import BasePage
from page_objects.react_home_page import ReactHomePage


class ReactLoginPage(BasePage):
    LOGIN_INPUT = (By.CSS_SELECTOR, "input[name='username']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input[name='password']")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "#kt_login_signin_submit")
    ALERT_MESSAGE_LOCATOR = (By.CSS_SELECTOR, "[data-testid='alert_message']")

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.base_url = os.environ.get("REACT_BASE_URL")

    def go_to_login_page(self) -> None:
        self.driver.get(self.base_url)

    def login(self, enter_key, user, password, ) -> ReactHomePage:
        current_page = self.get_current_url()
        self.enter_text(by_locator=self.LOGIN_INPUT, text=user)

        if enter_key:
            self.enter_text_and_click_enter(by_locators=self.PASSWORD_INPUT, text=password)
        else:
            self.enter_text(by_locator=self.PASSWORD_INPUT, text=password)
            self.click_on(by_locator=self.LOGIN_BUTTON)
            self.wait_for_new_page(current_page=current_page)
        return ReactHomePage(driver=self.driver)

    @property
    def alert_message(self) -> str:
        return self.get_element_text(by_locator=self.ALERT_MESSAGE_LOCATOR)
