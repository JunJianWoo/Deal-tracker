from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from scrapers.scraper import Scraper
from util import createConfigSet


class ScorptecScraper(Scraper):
    """
    Scrapes Scorptec Online Store based on category 
    Note: Circumvents bot tests by re-opening and closing driver
    """
    CATEGORY_CONFIG_TXT = "scorptecfilter.txt"
    WEBSITE = "Scorptec"

    def __init__(self):
        super().__init__()

        self.setStartLink("https://www.scorptec.com.au/product/clearance?page=1")
        self.categories = createConfigSet(self.CATEGORY_CONFIG_TXT)

    
    def extract_info(self):
        self.driver.get(self.startLink)
        productItem = []

        # Filter based on category
        if len(self.categories) > 0:
            filterItems = self.driver.find_element(By.ID,'filter-item-category').find_elements(By.CLASS_NAME, 'filter-item-value')
            for filterItem in filterItems:
                if filterItem.get_attribute('data-cat') is not None:
                    itemName = filterItem.find_element(By.CLASS_NAME, "filter-item-name").text
                    if itemName.strip().lower() in self.categories:
                        checkMark = filterItem.find_element(By.CLASS_NAME, "checkmark")
                        self.driver.execute_script("arguments[0].scrollIntoView();", checkMark)
                        checkMark.click()

        # Circumvent bot tests
        url = self.driver.current_url
        url_components = url.split('page=1')
        total_page = int(self.driver.find_element(By.ID, "total-page").text)

        self.driver.quit()

        page_no = 1
        while page_no <= total_page:
            # Go to site (page and filtered)
            self.driver = webdriver.Chrome()
            self.driver.get(f"page={page_no}".join(url_components))

            elementRange = self.driver.find_element(By.ID, 'product-list-show').text.split(' ')
            amount = int(elementRange[-1]) - int(elementRange[0]) + 1

            # Wait until all items have loaded in
            wait = WebDriverWait(self.driver, timeout=30)
            wait.until(lambda d: self._satisfyLoadCondition(d, amount))

            # Parse HTML into fields
            productCards = self.driver.find_elements(By.CSS_SELECTOR,'.row.product-list-detail[data-infilter="1"]')
            productCards = list(filter(lambda x: "element-hidden" not in x.get_attribute("class") , productCards))
            for productCard in productCards:
                name = productCard.get_attribute("data-shortintro")

                # Get image container
                try:
                    imageDiv = productCard.find_element(By.CLASS_NAME,"detail-image-wrapper")
                except NoSuchElementException:
                    wait = WebDriverWait(imageDiv, timeout=15)
                    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "detail-image-wrapper")))
                    imageDiv = productCard.find_element(By.CLASS_NAME,"detail-image-wrapper")

                # Site and Image
                websiteLink = imageDiv.find_element(By.TAG_NAME,'a').get_attribute("href")
                imageLink = imageDiv.find_element(By.TAG_NAME,'img').get_attribute("src")
                
                # Prices
                priceDiv = productCard.find_element(By.CLASS_NAME,"detail-product-prices")
                discountedPrice = priceDiv.find_element(By.CLASS_NAME,"detail-product-price").text[1:]

                # Filter out refurbished goods 
                try:
                    originalPrice = priceDiv.find_element(By.CLASS_NAME,"detail-product-before-price").text[1:]
                except NoSuchElementException:
                    continue

                productItem.append({
                    "name": name,
                    "imageLink": imageLink,
                    "websiteLink": websiteLink,
                    "discountedPrice": discountedPrice,
                    "originalPrice": originalPrice,
                    "companySource": self.WEBSITE
                })

            page_no += 1
            self.driver.quit()

        return productItem
    

    def _satisfyLoadCondition(self, driver, amount):
        """
        Checks all on-screen items have loaded in 
        """
        items = driver.find_elements(By.CSS_SELECTOR,'.row.product-list-detail[data-infilter="1"]')
        items = list(filter(lambda x: "element-hidden" not in x.get_attribute("class") , items))

        return len(items) == amount

