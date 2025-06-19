from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
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
        wait.until(lambda d: len(d.find_elements(By.CLASS_NAME, "ProductCard")) == int(d.find_element(By.CLASS_NAME, "infinite-hits-text").text.split(' ')[1]) )

        # Load pictures in higher resolution (pictures out of window are rendered lazily)
        self.driver.execute_script("window.scrollTo({top: document.body.scrollHeight, behaviour: 'smooth'});")
        productCards = self.driver.find_elements(By.CLASS_NAME, "ProductCard")

        # Parse HTML elements into fields
        for productCard in productCards:

            imageDiv = productCard.find_element(By.CLASS_NAME,"ProductCard_imageLink")
            websiteLink = imageDiv.get_attribute("href")
            image = imageDiv.find_element(By.TAG_NAME,'img')


            imageLink = image.get_attribute("src")
            imageLink = imageLink.replace("_32x32.jpg","_600x600.jpg")
            name = image.get_attribute("alt")

            priceDiv = productCard.find_element(By.CLASS_NAME,"ProductCard_priceContainer")
            oriPriceDiv = priceDiv.find_element(By.CLASS_NAME,"StrikeText_styles_container__rkpz4f0")
            originalPrice = oriPriceDiv.find_elements(By.TAG_NAME,'span')[-1].text
            originalPrice = int(round(float(originalPrice)))

            discountedPrice = priceDiv.find_elements(By.CLASS_NAME,"PriceFont_fontStyle__w0cm2q1")[-1].text
            discountedPrice = int(round(float(discountedPrice)))
            productItem.append({
                "name": name,
                "imageLink": imageLink,
                "websiteLink": websiteLink,
                "discountedPrice": discountedPrice,
                "originalPrice": originalPrice,
                "companySource": self.WEBSITE
            })
        
        return productItem
