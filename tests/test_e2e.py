import re
import pytest
from typing import List

from pages.articles import ArticlesPage
from pages.homepage import HomePage
from tests.conftest import driver
from utilties.utils import translate_text, word_histo, add_driver_wait, download_file

@pytest.mark.usefixtures("setup")
class TestWebsite:
    article_titles:List[str] = []
    translated_headers:str = ""

    @pytest.mark.dependency()
    def test_validate_website_language(self, logger):
        # simplest way to validate the language is checking the lang tag
        # alternate way is to parse a portion of document and detect it against translator API's
        logger.info(f"test case: validate the website language")
        driver_wait = add_driver_wait(self.driver, 10)
        home_page = HomePage(self.driver, driver_wait, logger)
        home_page.open_url()
        expected_language = "es-ES"
        lang = home_page.get_page_lang()
        assert lang == expected_language, f"language expected: {expected_language}, actual: {lang}"
        logger.info("*" * 80)

    @pytest.mark.dependency(depends=["TestWebsite::test_validate_website_language"])
    def test_scrape_articles(self, logger, request):
        driver_wait = add_driver_wait(self.driver, 10)
        home_page = HomePage(self.driver, driver_wait, logger)
        home_page.open_url()
        home_page.accept_cookies()
        opinions_page = home_page.click_opinion()
        articles = opinions_page.get_articles()
        articles_page = ArticlesPage(self.driver, driver_wait, logger)

        default_window = self.driver.window_handles[0]

        scrape_count = int(request.config.getoption("--count"))
        logger.info(f"Fetching first {scrape_count} articles from the list")
        for article in articles[:scrape_count]:
            articles_page.open_article(article)
            title = articles_page.get_title()
            articles_page.get_content()
            TestWebsite.article_titles.append(title)
            img_url = articles_page.get_img_url()
            if img_url:
                folder_name = "images"
                file_name = download_file(img_url, title, folder_name)
                logger.info(f"downloaded image file as {file_name}")
            else:
                logger.info(f"no downloadable images found for the title {title}")
            self.driver.close()
            logger.debug("switching to default content")
            self.driver.switch_to.window(default_window)
        logger.info("*" * 80)

    @pytest.mark.dependency(depends=["TestWebsite::test_scrape_articles"])
    def test_translate_headers(self, logger):
        logger.info(f"test case: translate headers from opinion articles")
        titles = TestWebsite.article_titles
        logger.info(f"translating headers for titles {titles}")
        for title in titles:
            trans = translate_text(title, "es", "en")
            logger.info(f"original: {title} translated: {trans}")
            # noticed punctual marks in title at times, which results in split and count actions
            # removed comma and periods for now in the titles
            TestWebsite.translated_headers = TestWebsite.translated_headers + " " + re.sub(r'[,.]','',trans)
        logger.info("*" * 80)

    @pytest.mark.dependency(depends=["TestWebsite::test_translate_headers"])
    def test_count_header_words(self, logger):
        logger.info(f"test case: count repetition of words from the translated titles")
        headers = TestWebsite.translated_headers
        logger.info(f"counting words for \"{headers.strip()}\"")
        word_dict = word_histo(headers)
        logger.info("repeated words list")
        at_least_one_repetition = False
        for word, count in word_dict.items():
            if count > 1:
                at_least_one_repetition = True
                logger.info(f"{word} : {count}")
        if not at_least_one_repetition:
            logger.info("no words with repetition found")
        logger.info("*" * 80)