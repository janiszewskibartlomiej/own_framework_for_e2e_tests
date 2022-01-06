from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from page_objects.base_page import BasePage
from page_objects.react_categories_page import ReactCategoriesPage
from page_objects.react_footers_page import ReactFootersPage
from page_objects.react_headers_page import ReactHeadersPage
from page_objects.react_import_data_page import ReactImportDataPage
from page_objects.react_integrations_page import ReactIntegrationsPage
from page_objects.react_message_page import ReactMessagePage
from page_objects.react_models_page import ReactModelsPage
from page_objects.react_rules_page import ReactRulesPage
from page_objects.react_topics_page import ReactTopicsPage
from page_objects.react_trainings_data_page import ReactTrainingsDataPage


class ReactLeftMenu(BasePage):
    OVERVIEW_LINK_TEXT_LOCATOR = (By.CSS_SELECTOR, "a[href='/dashboard']")
    GENERAL_LINK_TEXT_LOCATOR = (By.CSS_SELECTOR, "a[href='/reports']")
    MESSAGES_DROPDOWN_LOCATOR = (By.CSS_SELECTOR, "[data-testid='messages_dropdown']")
    DATA_AND_MODELS_DROPDOWN_LOCATOR = (By.CSS_SELECTOR, "[data-testid='data_and_models_dropdown']")
    TRAININGS_DATA_LINK_TEXT_LOCATOR = (
        By.CSS_SELECTOR,
        "a[href='/trainings-data']",
    )
    IMPORT_DATA_LINK_TEXT_LOCATOR = (By.CSS_SELECTOR, "a[href='/csv-files']")
    MODELS_LINK_TEXT_LOCATOR = (
        By.CSS_SELECTOR,
        "a[href='/prediction-models']",
    )
    AUTOMATIONS_DROPDOWN_LOCATOR = (By.CSS_SELECTOR, "[data-testid='automations_dropdown']")
    CATEGORIES_LINK_TEXT_LOCATOR = (
        By.CSS_SELECTOR,
        "a[href='/rule-categories']",
    )
    TOPICS_LINK_TEXT_LOCATOR = (By.CSS_SELECTOR, "a[href='/topics']")
    RULES_LINK_TEXT_LOCATOR = (By.CSS_SELECTOR, "a[href='/rules']")
    MESSAGE_TEMPLATES_DROPDOWN_LOCATOR = (
        By.CSS_SELECTOR,
        "[data-testid='message_templates_dropdown']",
    )
    HEADERS_LINK_TEXT_LOCATOR = (
        By.CSS_SELECTOR,
        "a[href='/message-templates/headers']",
    )
    FOOTERS_LINK_TEXT_LOCATOR = (
        By.CSS_SELECTOR,
        "a[href='/message-templates/footers']",
    )
    SETTINGS_DROPDOWN_LOCATOR = (By.CSS_SELECTOR, "[data-testid='settings_dropdown']")
    INTEGRATIONS_LINK_TEXT_LOCATOR = (By.CSS_SELECTOR, "a[href='/producers']")
    ACTIONS_BUTTON = (By.CSS_SELECTOR, "[data-testid='actions_button']")

    def __init__(self, driver):
        super().__init__(driver)
        self.driver: WebDriver = driver

    @property
    def rules_link_text(self) -> str:
        return self.get_element_text(by_locator=self.RULES_LINK_TEXT_LOCATOR)

    def click_on_automation_dropdown(self) -> None:
        self.click_on(by_locator=self.AUTOMATIONS_DROPDOWN_LOCATOR)

    def click_on_general_link(self) -> ReactMessagePage:
        current_page = self.get_current_url()
        self.click_on(by_locator=self.MESSAGES_DROPDOWN_LOCATOR)
        self.click_on(by_locator=self.GENERAL_LINK_TEXT_LOCATOR)
        self.wait_for_new_page(current_page=current_page)
        return ReactMessagePage(driver=self.driver)

    def click_on_data_and_models_dropdown(self) -> None:
        self.click_on(by_locator=self.DATA_AND_MODELS_DROPDOWN_LOCATOR)

    def click_on_trainings_data_link(self) -> ReactTrainingsDataPage:
        current_page = self.get_current_url()
        self.click_on(by_locator=self.TRAININGS_DATA_LINK_TEXT_LOCATOR)
        self.wait_for_new_page(current_page=current_page)
        return ReactTrainingsDataPage(driver=self.driver)

    def click_on_import_data_link(self) -> ReactImportDataPage:
        current_page = self.get_current_url()
        self.click_on(by_locator=self.IMPORT_DATA_LINK_TEXT_LOCATOR)
        self.wait_for_new_page(current_page=current_page)
        return ReactImportDataPage(driver=self.driver)

    def click_on_models_link(self) -> ReactModelsPage:
        current_page = self.get_current_url()
        self.click_on(by_locator=self.MODELS_LINK_TEXT_LOCATOR)
        self.wait_for_new_page(current_page=current_page)
        return ReactModelsPage(driver=self.driver)

    def click_on_categories_link(self) -> ReactCategoriesPage:
        current_page = self.get_current_url()
        self.click_on(by_locator=self.CATEGORIES_LINK_TEXT_LOCATOR)
        self.wait_for_new_page(current_page=current_page)
        return ReactCategoriesPage(driver=self.driver)

    def click_on_topics_link(self) -> ReactTopicsPage:
        current_page = self.get_current_url()
        self.click_on(by_locator=self.TOPICS_LINK_TEXT_LOCATOR)
        self.wait_for_new_page(current_page=current_page)
        return ReactTopicsPage(driver=self.driver)

    def click_on_rules_link(self) -> ReactRulesPage:
        current_page = self.get_current_url()
        self.click_on(by_locator=self.RULES_LINK_TEXT_LOCATOR)
        self.wait_for_new_page(current_page=current_page)
        return ReactRulesPage(driver=self.driver)

    def click_on_message_templates_dropdown(self) -> None:
        self.click_on(by_locator=self.MESSAGE_TEMPLATES_DROPDOWN_LOCATOR)

    def click_on_headers_link(self) -> ReactHeadersPage:
        current_page = self.get_current_url()
        self.click_on(by_locator=self.HEADERS_LINK_TEXT_LOCATOR)
        self.wait_for_new_page(current_page=current_page)
        return ReactHeadersPage(driver=self.driver)

    def click_on_footers_link(self) -> ReactFootersPage:
        current_page = self.get_current_url()
        self.click_on(by_locator=self.FOOTERS_LINK_TEXT_LOCATOR)
        self.wait_for_new_page(current_page=current_page)
        return ReactFootersPage(driver=self.driver)

    def click_on_settings_dropdown(self) -> None:
        self.click_on(by_locator=self.SETTINGS_DROPDOWN_LOCATOR)

    def click_on_integrations_link(self) -> ReactIntegrationsPage:
        current_page = self.get_current_url()
        self.click_on(by_locator=self.INTEGRATIONS_LINK_TEXT_LOCATOR)
        self.wait_for_new_page(current_page=current_page)
        return ReactIntegrationsPage(driver=self.driver)
