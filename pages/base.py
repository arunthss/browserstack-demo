from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import visibility_of_element_located
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException

class BasePage:
    url = "https://elpais.com/"
    expected_title = "EL PAÍS: el periódico global"
    cookies_modal = (By.ID, "didomi-notice")
    modal_accept = (By.ID, "didomi-notice-agree-button")

    def __init__(self, driver, driver_wait, logger):
        self.driver = driver
        self.driver_wait = driver_wait
        self.logger = logger

    def accept_cookies(self):
        try:
            self.logger.debug("waiting for cookies modal to appear")
            self.driver_wait.until(visibility_of_element_located(BasePage.cookies_modal))
            self.driver.find_element(*BasePage.modal_accept).click()
            self.logger.debug("cookies modal accepted")
        except TimeoutException:
            # logic to handle the accept cookies modal (if present)
            self.logger.debug("cookies model not found... continuing")
        except ElementNotInteractableException:
            # noticed an alert pop up in firefox browser intermittently intercepting webdriver clicks
            # handling with js click
            cmd = f"document.querySelector('#{BasePage.modal_accept[1]}').click();"
            self.logger.debug("selenium call failed; attempting with js click")
            self.logger.debug(f"cmd: {cmd}")
            self.driver.execute_script(cmd)

    def open_url(self):
        self.logger.info(f"opening url: {BasePage.url}")
        self.driver.get(BasePage.url)
        page_title = self.driver.title
        self.logger.info(f"page opened with title {page_title}")
        assert page_title == BasePage.expected_title, "page title mismatch"