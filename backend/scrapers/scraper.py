from typing import List, Dict
from selenium import webdriver
from abc import ABC, abstractmethod

class Scraper(ABC):
    """
    Generic abstract class for a web scraper
    """
    @abstractmethod
    def __init__(self):
        self.startLink = ""
        self.driver = None

    def setStartLink(self, startLink):
        self.startLink = startLink
    
    def scrape(self) -> List[Dict]:
        self.driver = webdriver.Chrome()
        products = self.extract_info()
        self.driver.quit()
        print(f"Driver Quit Occurs")

    @abstractmethod
    def extract_info(self) -> List[Dict]:
        """
        Handles parsing the HTML elements in website to get product information
        """
        pass
