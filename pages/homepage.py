from selenium.webdriver.common.by import By
from pages.base import BasePage
from pages.opinions import OpinionsPage


class HomePage(BasePage):
    opinion = (By.XPATH, "//section//a[contains(text(),'Opinión')]")
    html = (By.TAG_NAME, "html")
    def click_opinion(self):
        self.logger.debug("waiting for opinion section to be visible")
        self.driver.find_element(*HomePage.opinion).click()
        return OpinionsPage(self.driver, self.driver_wait, self.logger)

    def get_page_lang(self):
        lang = self.driver.find_element(*HomePage.html).get_attribute("lang")
        self.logger.debug(f"url : {HomePage.url} has language attribute of {lang}")
        return lang