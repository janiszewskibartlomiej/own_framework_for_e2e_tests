import os
import sys
import time
from datetime import datetime

import pytest
from py.xml import html
from resources.automation_functions import print_message_in_color
from selenium import webdriver
from selenium.webdriver import ActionChains, DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from steps.ui_steps import UiSteps

render_collapsed = True

PROJECT_ROOT = os.path.dirname(os.path.abspath("."))
sys.path.append(PROJECT_ROOT)


def pytest_html_results_table_header(cells):
    cells.insert(1, html.th("Time", class_="sortable time", col="time"))
    cells.pop()


def pytest_html_results_table_row(report, cells):
    cells.insert(1, html.td(datetime.now(), class_="col-time"))
    cells.pop()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    report.description = str(item.function.__doc__)


def pytest_html_report_title(report):
    report.title = "pytest html report on DEV instance in AWS"


def pytest_html_results_summary(prefix, summary, postfix):
    prefix.extend([html.p("Domain: //.eu-central-1.elb.amazonaws.com")])


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    pytest_html = item.config.pluginmanager.getplugin("html")
    outcome = yield
    report = outcome.get_result()
    setattr(item, "rep_" + report.when, report)

    extra = getattr(report, "extra", [])
    if report.when == "call":
        # always add url to report
        extra.append(pytest_html.extras.url(os.environ.get("BASE_URL")))
        xfail = hasattr(report, "wasxfail")
        if (report.skipped and xfail) or (report.failed and not xfail):
            # only add additional html on failure
            extra.append(pytest_html.extras.html("<div>Additional HTML</div>"))
        report.extra = extra


headless = False


@pytest.fixture(params=["chrome", "firefox"])
def driver(
        request,
        chrome_del_cache=False,
        chrome_headless=headless,
        firefox_del_cache=False,
        firefox_headless=headless,
):
    # chrome
    driver = None
    if request.param == "chrome":
        caps = DesiredCapabilities().CHROME
        caps["pageLoadStrategy"] = "normal"
        caps["goog:loggingPrefs"] = {"browser": "ALL"}
        caps["acceptInsecureCerts"] = True

        chrome_options = webdriver.ChromeOptions()
        if chrome_headless:
            chrome_options.headless = True
            chrome_options.add_argument("--disable-gpu")

        driver = webdriver.Chrome(
            executable_path=ChromeDriverManager().install(),
            options=chrome_options,
            desired_capabilities=caps,
        )

        if chrome_del_cache:
            driver.get("chrome://settings/clearBrowserData")
            action = ActionChains(driver)
            time.sleep(2)
            action.send_keys(Keys.ENTER).perform()
    # firefox
    if request.param == "firefox":
        caps = DesiredCapabilities().FIREFOX
        caps["pageLoadStrategy"] = "normal"
        caps["acceptInsecureCerts"] = True

        profile = webdriver.FirefoxProfile()
        profile.accept_untrusted_certs = True

        if firefox_del_cache:
            profile.set_preference("browser.cache.disk.enable", False)
            profile.set_preference("browser.cache.memory.enable", False)
            profile.set_preference("browser.cache.offline.enable", False)
            profile.set_preference("network.http.use-cache", False)

        firefox_options = webdriver.FirefoxOptions()
        firefox_options.log.level = "debug"

        if firefox_headless:
            firefox_options.headless = True

        driver = webdriver.Firefox(
            executable_path=GeckoDriverManager().install(),
            firefox_profile=profile,
            options=firefox_options,
            desired_capabilities=caps,
        )
    driver.implicitly_wait(1)
    driver.set_window_size(width=1920, height=1080)

    ui_steps = UiSteps(driver=driver)
    message = ui_steps.clean_test_reports
    print(message)
    driver.ui_steps = ui_steps
    driver.STEPS_LIST = []

    yield driver

    if request.node.rep_call.outcome == "failed":
        ui_steps.do_screenshot(name=request.node.name)
    else:
        print_message_in_color(
            message=f"{request.node.name} is done !" + "\U0001F44D", rgb_color="0,255,0"
        )

    driver.quit()
    del driver
