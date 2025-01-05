from pages.base import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import visibility_of_element_located

class OpinionsPage(BasePage):
    article_links = (By.XPATH, "//a[text()='Columna']/following-sibling::h2/a")

    def get_articles(self):
        self.driver_wait.until(visibility_of_element_located(OpinionsPage.article_links))
        articles = self.driver.find_elements(*OpinionsPage.article_links)
        assert len(articles) > 0, "expected at least one article under the Opinion section"
        self.logger.info(f"found {len(articles)} articles under opinion section")
        return articles

