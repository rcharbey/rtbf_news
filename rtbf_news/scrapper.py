import abc
from typing import List

import requests
from bs4 import BeautifulSoup


class Scrapper:
    def __init__(self, url: str):
        self.url = url

    @abc.abstractmethod
    def scrapp(self) -> List[str]:
        pass


class RTBF_Scrapper(Scrapper):
    def scrapp(self) -> List[str]:
        "Returns a list of (category, title) corresponding to each article"

        result = []

        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, "html.parser")
        news = soup.find_all(
            "div", class_="group flex cursor-pointer lg:min-h-horizontal-card"
        )

        for new in news:
            category = new.find("h4").text
            title = new.find("h3").text
            result.append((category, title))

        return result
