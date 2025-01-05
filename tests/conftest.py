import logging
import os.path
import sys
from idlelib.autocomplete import TRY_A

from selenium import webdriver
import pytest

driver = None

def pytest_addoption(parser):
    parser.addoption(
        "--browser", action="store", default="firefox", help="browser to use; default chrome"
    )

    parser.addoption(
        "--count", action="store", default="5", help="count of articles to scrape; default 5"
    )

@pytest.fixture(scope="module", autouse=True)
def logger():
    logs_folder = os.path.abspath(os.path.join(".", 'logs'))
    if not os.path.exists(logs_folder):
        os.mkdir(logs_folder)
    logger = logging.getLogger("e2e")
    formatter = logging.Formatter("%(asctime)s: %(levelname)s: %(name)s: %(message)s")
    fh = logging.FileHandler(os.path.join(logs_folder, "e2e.log"), encoding="utf-16")
    sh = logging.StreamHandler()

    fh.setFormatter(formatter)
    sh.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(sh)
    logger.setLevel(logging.DEBUG)
    logger.info("log file created")
    return logger

@pytest.fixture(scope="class")
def setup(request):
    global driver
    browser_name = request.config.getoption("--browser")
    if browser_name == "firefox":
        driver = webdriver.Firefox()
    elif browser_name == "edge":
        driver = webdriver.Edge()
    elif browser_name == "safari":
        if "darwin" not in sys.platform.lower():
            exit(1)
        driver = webdriver.Safari()
    else:
        driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(10)
    request.cls.driver = driver
    yield driver
    driver.quit()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    """
        Extends the PyTest Plugin to take and embed screenshot in html report, whenever test fails.
    """
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])

    if report.when == 'call' or report.when == "setup":
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            file_name = report.nodeid.replace("::", "_") + ".png"
            _capture_screenshot(file_name)
            if file_name:
                html = '<div><img src="%s" alt="screenshot" style="width:304px;height:228px;" ' \
                       'onclick="window.open(this.src)" align="right"/></div>' % file_name
                extra.append(pytest_html.extras.html(html))
        report.extra = extra


def _capture_screenshot(name):
    driver.get_screenshot_as_file(name)
