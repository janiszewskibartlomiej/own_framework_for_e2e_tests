import os
import time
from datetime import date

from dotenv import load_dotenv
from selenium.common import exceptions
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.expected_conditions import staleness_of, url_changes
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

import utils.constants as constant
from utils.automation_functions import (
    get_path_from_directory_name,
    change_win_sep, wait
)

load_dotenv()


class BasePage:
    """
    common methods for every browser
    """

    def __init__(self, driver):
        self.base_url = os.environ.get("BASE_URL")
        self.driver = driver
        self.timeout = 20
        self.short_timeout = 1
        self.RE = RePatterns()

    def click_on_and_wait_for_a_new_page(self, by_locator: tuple):
        old_page = self.driver.find_element_by_tag_name("html")
        web_element = WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable(by_locator)
        )
        web_element.click()
        WebDriverWait(self.driver, self.timeout).until(EC.staleness_of(old_page))

    def click_on(self, by_locator: tuple):
        web_element = WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable(by_locator)
        )
        web_element.click()
        while not self.page_is_loading():
            wait()
            continue
        return web_element

    def get_src_attribute(self, by_locator: tuple) -> str:
        icon = self.get_element(by_locator=by_locator)
        return icon.get_attribute("innerHTML")

    def icon_is_green(self, string) -> bool:
        if constant.ICON_YES in string:
            return True
        elif constant.ICON_NO in string:
            return False

    def assert_element_text_in_page_source(self, element_text: str):
        while not self.page_is_loading():
            continue

        assert element_text in self.driver.page_source, f"{element_text} not in page source"

    def assert_path_in_current_url(self, path: str):
        assert_path_in_url = WebDriverWait(self.driver, self.timeout).until(
            EC.url_contains(url=path)
        )
        assert assert_path_in_url is True

    def enter_text(self, by_locator: tuple, text: str):
        element = WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(by_locator)
        )
        element.clear()
        element.send_keys(text)

    def enter_text_and_click_enter(self, by_locators: tuple, text: str):
        element = WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(by_locators)
        )
        element.clear()
        element.send_keys(text + Keys.ENTER)

    def enter_text_and_click_enter_and_wait_for_a_new_page(self, by_locators: tuple, text: str):
        old_page = self.driver.find_element_by_tag_name("html")
        element = WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(by_locators)
        )
        element.clear()
        element.send_keys(text + Keys.ENTER)
        WebDriverWait(self.driver, self.timeout).until(staleness_of(old_page))

    def wait_for_new_page(self, current_page):
        WebDriverWait(self.driver, self.timeout).until(url_changes(current_page))

    def page_is_loading(self):
        page_status = self.driver.execute_script("return document.readyState")
        if page_status == "complete":
            return True
        else:
            yield False

    def refreshing_page_and_wait_for_element_n_seconds(
            self, text_to_verifying: str, by_locators: tuple, n_seconds: int
    ) -> int:
        time_to_refresh = None
        start_time = time.time().__int__()
        web_element = self.get_element(by_locator=by_locators)

        while text_to_verifying != web_element.text:
            self.driver.refresh()
            web_element = self.get_element(by_locator=by_locators)
            end_time = time.time().__int__()
            time_to_refresh = end_time - start_time
            if time_to_refresh < n_seconds:
                continue
            else:
                raise exceptions.TimeoutException(
                    msg=f"Element not visible for a {n_seconds} seconds"
                )
        return time_to_refresh or 0

    def refreshing_page_and_wait_for_text_in_page_source_n_seconds(
            self, text_to_verifying: str, n_seconds: int
    ):
        start_time = time.time().__int__()
        while text_to_verifying not in self.driver.page_source:
            self.driver.refresh()
            end_time = time.time().__int__()
            time_to_refresh = end_time - start_time
            if time_to_refresh < n_seconds:
                continue
            else:
                msg = f"Refreshing time is more then {n_seconds} seconds"
                raise exceptions.TimeoutException(msg=msg)

    def is_clickable(self, by_locator: tuple) -> bool:
        element = WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable(by_locator)
        )
        return bool(element)

    def element_is_visible(self, by_locator: tuple) -> bool:
        element = WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(by_locator)
        )
        return bool(element)

    def element_is_not_visible(self, by_locator: tuple) -> bool:
        element = WebDriverWait(self.driver, self.timeout).until(
            EC.invisibility_of_element_located(by_locator)
        )
        return bool(element)

    def get_element(self, by_locator: tuple):
        element = WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(by_locator)
        )
        return element

    def element_is_on_a_page(self, by_locator: tuple) -> bool:
        try:
            element = WebDriverWait(self.driver, self.short_timeout).until(
                EC.presence_of_element_located(by_locator)
            )
            return bool(element)
        except TimeoutException:
            return False

    def get_element_text(self, by_locator: tuple):
        element = WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(by_locator)
        )
        return element.text

    def get_all_elements(self, by_locator: tuple[str, str]) -> list[WebElement]:
        while not self.page_is_loading():
            wait(1)
            continue
        try:
            elements = WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_all_elements_located(by_locator)
            )
            return elements
        except TimeoutException:
            logger.debug('[NO RECORDS AVAILABLE ON THE PAGE]')
            return []

    def is_disappeared(self, by_locator: tuple) -> bool:
        result = WebDriverWait(self.driver, self.timeout).until(
            EC.invisibility_of_element_located(by_locator)
        )
        return result

    def get_value_from_element_by_query_selector(self, by_locator: tuple) -> str:
        value = self.driver.execute_script(
            f"""
            const element =  document.querySelector("{by_locator[1]}");
            return element.value
        """
        )
        return value

    def hover_to(self, by_locator: tuple) -> ActionChains:
        element = WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable(by_locator)
        )
        return ActionChains(self.driver).move_to_element(element).perform()

    def hover_to_and_click(self, by_locator: tuple) -> ActionChains:

        element = WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable(by_locator)
        )
        return ActionChains(self.driver).move_to_element(element).click().perform()

    def choose(self, drop_down_select: tuple, name: str):
        drop_down = WebDriverWait(self, self.timeout).until(
            EC.visibility_of_element_located(drop_down_select)
        )
        drop_down.find_element(By.NAME(name)).click()

    def get_visible_text_in_select_input(self, by_locator) -> str:
        element = Select(self.get_element(by_locator)).first_selected_option
        return element.text

        def element_inside_element_is_visible(self, web_element: WebElement, locator: tuple[str, str]) -> bool:
        try:
            element = WebDriverWait(self.driver, self.short_timeout).until(
                EC.visibility_of(web_element.find_element(*locator))
            )
            return bool(element)
        except (NoSuchElementException, StaleElementReferenceException, TimeoutException, ReadTimeoutError):
            return False

    def hover_to_and_click_by_js(self, web_element: WebElement) -> None:
        self.driver.execute_script(
            "var clickEvent = new MouseEvent('click', { \
            'view': window, \
            'bubbles': true, \
            'cancelable': false \
            }); \
            arguments[0].dispatchEvent(clickEvent);", web_element)

    def quit(self):
        self.driver.close()
        self.driver.quit()
        del driver

    def visit(self, location: str):
        url = self.driver.current_url + location
        return self.driver.get(url)

    def open_new_tab_and_switch(self):
        tab = self.driver.execute_script("window.open('');")
        return self.driver.switch_to.window(tab[1])

    def get_current_url(self):
        return self.driver.current_url

    def do_screenshot(self, name: str) -> str:
        while not self.page_is_loading():
            continue
        original_size = self.driver.get_window_size()
        required_width = self.driver.execute_script("return document.body.parentNode.scrollWidth")
        required_height = self.driver.execute_script("return document.body.parentNode.scrollHeight")
        self.driver.set_window_size(required_width, required_height)

        current_date = date.today()
        current_date_template = str(current_date).replace("-", "")

        test_reports_name = constant.TEST_REPORTS
        test_reports_path = get_path_from_directory_name(directory_name=test_reports_name)

        if not test_reports_path:
            tests_path = change_win_sep(
                path=get_path_from_directory_name(directory_name=constant.TESTS)
            )
            dir_test_reports = f"{tests_path}{os.sep}{test_reports_name}"
            os.umask(0)
            os.makedirs(dir_test_reports, mode=0o777)

            dir_target = f"{tests_path}{os.sep}{test_reports_name}{os.sep}{current_date_template}"
        else:
            dir_target = f"{test_reports_path}{os.sep}{current_date_template}"

        if not os.path.exists(dir_target):
            os.makedirs(dir_target, mode=0o777)

        t = time.localtime()
        current_time = time.strftime("%H-%M-%S", t)
        path = f"{dir_target}{os.sep}screenshot_{name}_t_{current_time}.png"
        self.driver.get_screenshot_as_file(path)
        self.driver.set_window_size(original_size["width"], original_size["height"])
        return path

    def login_as(
            self,
            username_locator: tuple,
            username,
            password_locator: tuple,
            password,
            button_locator: tuple,
            enter_key=False,
    ):
        self.enter_text(username_locator, username)
        if enter_key:
            self.enter_text_and_click_enter_and_wait_for_a_new_page(password_locator, password)
        else:
            self.enter_text(password_locator, password)
            self.click_on_and_wait_for_a_new_page(button_locator)

    def scroll_to(self, web_element):
        self.driver.execute_script("arguments[0].scrollIntoView();", web_element)

    def scroll_to_invisible_element(self, target):
        if isinstance(target, tuple):
            target = self.get_element(target)

        self.driver.execute_script("arguments[0].scrollIntoView(true);", target)

    def get_console_logs(self, logs: dict) -> dict:
        if self.driver.name == "chrome":
            while not self.page_is_loading():
                continue
            console_logs = self.driver.get_log("browser")
            messages = {
                el["timestamp"]: {"message": el["message"], "url": self.driver.current_url, }
                for el in console_logs
            }
            if isinstance(logs, dict):
                logs.update(messages)
            else:
                return dict(messages)
