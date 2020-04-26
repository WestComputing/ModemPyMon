from abc import ABC, abstractmethod, abstractproperty, abstractclassmethod, abstractstaticmethod
from bs4 import BeautifulSoup

import requests


def get_soup(url: str, page_name: str) -> BeautifulSoup:
    print(f"Requesting {page_name}...")
    result = requests.get(url)
    assert result.status_code == 200, f"Status code {result.status_code} returned."
    source = result.text
    soup = BeautifulSoup(source, 'html.parser')
    return soup


class Modem(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def is_detected(self) -> bool:
        pass
