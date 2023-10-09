import abc
from typing import List

import requests
from bs4 import BeautifulSoup


class Scraper:
    def __init__(self, url: str):
        self.url = url

    @abc.abstractmethod
    def scrap(self) -> List[str]:
        pass


class RTBF_Scraper(Scraper):
    def scrap(self) -> List[str]:
        "Returns the category and title of each article"

        results = []

        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, "html.parser")
        news = soup.find_all(
            "div", class_="group flex cursor-pointer lg:min-h-horizontal-card"
        )

        for new in news:
            category = new.find("h4").text if not new.find("h4") is None else None
            title = new.find("h3").text
            result = " ".join([category, title]) if not category is None else title
            results.append(result)

        return results
