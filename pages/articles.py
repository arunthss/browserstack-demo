from pages.base import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import visibility_of_element_located
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException

class ArticlesPage(BasePage):
    title = (By.XPATH, "//article//h1")
    content = (By.XPATH, "//article//h1/following-sibling::h2")
    img_url = (By.XPATH, "//h1/ancestor::article//img[@srcset]")
    def get_title(self):
        try:
            title_text = self.driver.find_element(*ArticlesPage.title).text
            self.logger.debug(f"article title {title_text}")
            return title_text
        except NoSuchElementException:
            return 'n/a'

    def get_content(self):
        try:
            content_text = self.driver.find_element(*ArticlesPage.content).text
            self.logger.debug(f"article content {content_text}")
            return content_text
        except NoSuchElementException:
            return 'n/a'

    def get_img_url(self):
        images = self.driver.find_elements(By.XPATH, "//h1/ancestor::article//img[@srcset]")
        if len(images):
            self.logger.info("downloadable images found for the given page")
            img_url = images[0].get_attribute("src")
            return img_url

    def open_article(self, article):
        link = article.get_attribute("href")
        self.logger.debug(f"found article with link {link}")
        self.driver.switch_to.new_window('tab')
        self.logger.debug("opening link on new tab")
        self.driver.get(link)
