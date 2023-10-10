import abc
import time
from typing import List

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By


class Scraper:
    def __init__(self, url: str):
        self.url = url
        self.connect()

    def check_xpath_exists(self, xpath: str) -> bool:
        try:
            self.driver.find_element(By.XPATH, xpath)
        except NoSuchElementException:
            return False
        return True

    @abc.abstractmethod
    def connect(self):
        pass

    @abc.abstractmethod
    def scrap(self) -> List[str]:
        pass


class RTBF_Scraper(Scraper):
    def __init__(self, url: str, nb_news: int = 2000):
        """
        Args:
            url (str): url to scrap for news
            nb_news (int, optional): number of news to scrap. Defaults to 2000.
        """
        super().__init__(url)
        self.nb_news = nb_news

    def connect(self):
        self.driver = webdriver.Firefox()
        self.driver.get(self.url)

        time.sleep(3)

    def scrap(self) -> List[str]:
        "Returns the category and title of each article"

        # find button to accept and close cookie settings
        button = self.driver.find_element(
            By.ID,
            "didomi-notice-agree-button",
        )
        self.driver.execute_script("arguments[0].click();", button)
        time.sleep(2)

        main_xpath = "/html/body/div[2]/div/div/div/div[3]/div"
        article_zone_xpath = main_xpath + "/ul"

        # find button to add more article and press it a hundred times
        button = self.driver.find_element(
            By.XPATH,
            main_xpath + "/div[4]/div/div/div/button",
        )

        # get the news
        results, counter = [], 2
        while len(results) < self.nb_news:
            # if no more news, then stop scraping
            non_available_page_xpath = (
                main_xpath + "/div[4]/div/div/div/section/div[1]/h1"
            )
            if (
                self.check_xpath_exists(non_available_page_xpath)
                and self.driver.find_element(By.XPATH, non_available_page_xpath).text
                == "Ce contenu est actuellement introuvable."
            ):
                break

            article_xpath = (
                article_zone_xpath + f"/li[{counter}]/div/div/div/div/article"
            )
            counter += 1

            # add news every 20 news
            if counter % 20 == 0:
                self.driver.execute_script("arguments[0].click();", button)
                time.sleep(1)

            if not self.check_xpath_exists(article_xpath):
                # advertising
                continue

            new_xpath = article_xpath + f"/div/div[2]"

            title = self.driver.find_element(
                By.XPATH, new_xpath + "/div/header/h3"
            ).text

            category_xpath = new_xpath + "/div/header/h4"
            if self.check_xpath_exists(category_xpath):
                category = self.driver.find_element(By.XPATH, category_xpath).text
            else:
                category = None

            result = " ".join([category, title]) if not category is None else title
            results.append(result)

        return results
