import os

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from page_objects.base_page import BasePage


class MlFlowPage(BasePage):
    ICON_IN_RUNS_LIST_LOCATOR = (By.CSS_SELECTOR, "div.ag-body-viewport a i")
    CATEGORY_CLASSIFICATION_LOCATOR = (
        By.CSS_SELECTOR,
        "div[title='category_classification']>a",
    )
    TOPIC_CLASSIFICATION_LOCATOR = (
        By.CSS_SELECTOR,
        "div[title='topic_classification']>a",
    )
    SENTIMENT_CLASSIFICATION_LOCATOR = (
        By.CSS_SELECTOR,
        "div[title='sentiment_classification']>a",
    )
    MODEL_DIRECTORY_LOCATOR = (By.CSS_SELECTOR, "div[artifact-name='model'] > div")
    ELEMENTS_LIST_IN_MODEL_DIRECTOR_LOCATOR = (
        By.XPATH,
        "//div[@artifact-name='model']//following::li",
    )
    VOLUME_OF_STATUS_LOCATOR = (
        By.XPATH,
        "//span[text()='Status']//following-sibling::span",
    )
    ARTIFACT_INFO_PATH_LOCATOR = (By.CSS_SELECTOR, "div.artifact-info-path")

    def __init__(self, driver):
        super().__init__(driver)
        self.driver: WebDriver = driver

    def login_to_ml_flow_page(self) -> None:
        base_url = os.environ.get("BASE_URL")
        login = os.getenv(key="ML_FLOW_LOGIN")
        password = os.getenv(key="ML_FLOW_PASSWORD")
        url = f"https://{login}:{password}@{base_url[8:]}mlflow-admin/"
        self.driver.get(url=url)

    def click_on_green_icon(self) -> None:
        self.click_on(by_locator=self.ICON_IN_RUNS_LIST_LOCATOR)

    def click_on_category_classification_in_sidebar(self) -> None:
        self.click_on(by_locator=self.CATEGORY_CLASSIFICATION_LOCATOR)

    def click_on_topic_classification_in_sidebar(self) -> None:
        self.click_on(by_locator=self.TOPIC_CLASSIFICATION_LOCATOR)

    def click_on_sentiment_classification_in_sidebar(self) -> None:
        self.click_on(by_locator=self.SENTIMENT_CLASSIFICATION_LOCATOR)

    def wait_for_runs_data(self) -> None:
        icon = False
        while not icon:
            try:
                icon = self.get_element(by_locator=self.ICON_IN_RUNS_LIST_LOCATOR)
            except Exception as e:
                print(f"Exception >>{e.__class__}. Wait for data and refresh page.")
                self.driver.refresh()
                continue

    def scroll_to_model_directory_and_click_on(self) -> None:
        web_element: WebElement = self.get_element(by_locator=self.MODEL_DIRECTORY_LOCATOR)
        self.scroll_to(web_element=web_element)
        web_element.click()

    @property
    def elements_in_model_directory(self) -> list:
        web_elements = WebDriverWait(self.driver, timeout=self.timeout).until(
            EC.visibility_of_all_elements_located(self.ELEMENTS_LIST_IN_MODEL_DIRECTOR_LOCATOR)
        )
        return web_elements

    @property
    def volume_of_status(self) -> str:
        web_element = self.get_element_text(by_locator=self.VOLUME_OF_STATUS_LOCATOR)
        return web_element

    def is_artifact_info_path_visible(self) -> bool:
        web_element = self.get_element(by_locator=self.ARTIFACT_INFO_PATH_LOCATOR)
        return bool(web_element)

    @property
    def color_of_icon(self) -> str:
        WebDriverWait(driver=self.driver, timeout=self.timeout).until(
            EC.visibility_of_element_located(self.ICON_IN_RUNS_LIST_LOCATOR)
        )
        color = self.driver.execute_script(
            f'const el = document.querySelector("{self.ICON_IN_RUNS_LIST_LOCATOR[1]}");'
            " return el.style.color"
        )
        return color
