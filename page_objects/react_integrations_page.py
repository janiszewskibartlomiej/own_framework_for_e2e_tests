from selenium.webdriver.remote.webdriver import WebDriver

from page_objects.react_top_page_and_table import ReactTopPageAndTable


class ReactIntegrationsPage(ReactTopPageAndTable):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver: WebDriver = driver
