from scrapers.jbscraper import JBScraper
from scrapers.scorptecscraper import ScorptecScraper
from scrapers.msyscraper import MSYScraper

class ScraperManager():

    SCRAPERS_IN_USE = [
        JBScraper,
        ScorptecScraper,
        MSYScraper
    ]

    @staticmethod
    def scrape_all_data():
        """
        Run all scrapers and return combined results as a list.
        """
        data = []
        for scraper_class in ScraperManager.SCRAPERS_IN_USE:
            scraper = scraper_class()
            data = data + scraper.scrape()
        
        return data
