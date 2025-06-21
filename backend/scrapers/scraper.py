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
        try:
            data = self.extract_info()
        except Exception as e:
            raise e
            data = None
        finally:
            self.driver.quit()
            print(f"Driver Quit Occurs")
        
        return data

    @abstractmethod
    def extract_info(self) -> List[Dict]:
        """
        Parses the website's HTML to extract product info.

        Returns a list of dicts with keys:
        - "name", "image_link", "website_link", "discounted_price", 
          "original_price", "company_source"
        """
        pass
