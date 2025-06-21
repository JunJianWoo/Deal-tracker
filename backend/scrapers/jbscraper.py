from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from util import createConfigSet
from scrapers.scraper import Scraper

class JBScraper(Scraper):
    """
    Scrapes JB Hi-Fi Online Store on Deals based on Brand.
    """
    BRAND_CONFIG_TXT = "jbfilter.txt"
    WEBSITE="JB Hi-Fi"

    def __init__(self):
        super().__init__()

        # Construct page based on brands
        brandSet = createConfigSet(self.BRAND_CONFIG_TXT, prefix="Brand=")
        self.setStartLink(f"https://www.jbhifi.com.au/collections/all-products-on-sale?hitsPerPage=1000&{'&'.join(brandSet)}")
        
    def extract_info(self):
        try:
            self.driver.get(self.startLink) 
        except:
            return []
        productItem = []

        # Wait until all product card loads
        wait = WebDriverWait(self.driver, timeout=20)
        wait.until(JBScraper.all_product_cards_loaded)

        # Load pictures in higher resolution (pictures out of window are rendered lazily)
        self.driver.execute_script("window.scrollTo({top: document.body.scrollHeight, behaviour: 'smooth'});")
        productCards = self.driver.find_elements(By.CLASS_NAME, "ProductCard")

        # Parse HTML elements into fields
        for productCard in productCards:
            imageAnchor = productCard.find_element(By.TAG_NAME,"a")
            website_link = imageAnchor.get_attribute("href")

            image = imageAnchor.find_element(By.TAG_NAME,'img')
            image_link = image.get_attribute("src")
            image_link = image_link.replace("_32x32.jpg","_600x600.jpg")
            name = image.get_attribute("alt")

            priceDiv = productCard.find_element(By.CLASS_NAME,"ProductCard_priceContainer")
            oriPriceDiv = priceDiv.find_element(By.CLASS_NAME,"StrikeText_styles_container__rkpz4f0")
            original_price = oriPriceDiv.find_elements(By.TAG_NAME,'span')[-1].text
            original_price = int(round(float(original_price)))

            discounted_price = priceDiv.find_elements(By.CLASS_NAME,"PriceFont_fontStyle__w0cm2q1")[-1].text
            discounted_price = int(round(float(discounted_price)))
            productItem.append({
                "name": name,
                "image_link": image_link,
                "website_link": website_link,
                "discounted_price": discounted_price,
                "original_price": original_price,
                "company_source": self.WEBSITE
            })
        
        return productItem
    
    def all_product_cards_loaded(driver):
        try:
            amount_expected = int(driver.find_element(By.CLASS_NAME, "infinite-hits-text").text.split(' ')[1])
            amount_loaded = len(driver.find_elements(By.CLASS_NAME, "ProductCard"))
            return amount_expected == amount_loaded
        except:
            return False