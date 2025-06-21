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
        failed_scraping = []
        for scraper_class in ScraperManager.SCRAPERS_IN_USE:
            scraper = scraper_class()
            if (items := scraper.scrape()):
                data = data + items
            else:
                failed_scraping.append(scraper.WEBSITE)
    
        return {
            "data": data,
            "websites_failed": failed_scraping,
            "successful_scrapes": len(ScraperManager.SCRAPERS_IN_USE) - len(failed_scraping)
        }
