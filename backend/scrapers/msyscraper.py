from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from scrapers.scraper import Scraper
from util import createConfigSet

class MSYScraper(Scraper):

    CATEGORY_CONFIG_TXT = "msyfilter.txt"
    PAGE_SIZE_INDEX = 3
    WEBSITE = "MSY"

    def __init__(self):
        super().__init__()

        self.setStartLink(f"https://www.msy.com.au/hot-deals?sort=salenum&order=ASC&page=1&pagesize={self.PAGE_SIZE_INDEX}")
        self.categories = createConfigSet(self.CATEGORY_CONFIG_TXT)

    def extract_info(self):
        self.driver.get(self.startLink)
        cid = []
        productItem = []

        # Filter by category
        categoryDiv = self.driver.find_element(By.ID, 'mCSB_1_container')
        categoryList = categoryDiv.find_elements(By.TAG_NAME, 'li')
        for category in categoryList:
            self.driver.execute_script("arguments[0].scrollIntoView();", category)
            if category.find_element(By.CLASS_NAME, 'refine_text').text.strip().lower() in self.categories:
                checkbox = category.find_element(By.CLASS_NAME,'checkno')
                currentCid = checkbox.get_attribute("data-url") \
                                        .split("cid=")[-1]
                cid.append(currentCid)

        # Redirect to new categorised url
        newURL = f"{self.startLink}&cid={'-'.join(cid)}"
        self.driver.get(newURL)

        # Determine number of pages
        pageCountDiv = self.driver.find_element(By.CLASS_NAME, "block2") \
            .find_element(By.TAG_NAME, "ul")
        
        pageList = pageCountDiv.find_elements(By.TAG_NAME, "li")
        if len(pageList) > 0:
            pageCount = int(pageList[-2].text)
        else:
            pageCount = 1

        for i in range(1,pageCount+1):
            # Redirect to new page
            self.driver.get(f"page={i}".join(newURL.split("page=1")))

            # Obtain expected item count
            start = self.driver.find_element(By.ID, "shows_number_begin").text
            end = self.driver.find_element(By.ID, "shows_number_end").text
            amount = int(end) - int(start) + 1

            wait = WebDriverWait(self.driver, timeout=15)
            wait.until( lambda d: len(d.find_elements(By.CLASS_NAME, "goods_info.ele-goods-info")) == amount )
            productCards = self.driver.find_elements(By.CLASS_NAME, "goods_info.ele-goods-info")

            # Parse each item into fields
            for productCard in productCards:
                # Image
                imageDiv = productCard.find_element(By.CLASS_NAME, "goods_img")
                image_link = imageDiv.find_element(By.TAG_NAME,"img").get_attribute("src")

                # Site & Name
                linkContainer = imageDiv.find_element(By.TAG_NAME, "a")
                website_link = linkContainer.get_attribute("href")
                name = linkContainer.get_attribute("title")
                
                # Prices
                priceDiv = productCard \
                    .find_element(By.CLASS_NAME, "goods_price_stock.goods_price_section") \
                    .find_element(By.CLASS_NAME, "goods-price.ele-goods-price")
                discounted_price = round(float(priceDiv.text.replace(",","")))
                discounted_price = int(discounted_price)

                # Find Original Price
                try:
                    discountText = productCard.find_element(By.CLASS_NAME, "discount").text.lower()
                except NoSuchElementException:
                    continue

                if "save" in discountText:
                    occurIdx = discountText.index("save")
                    discountAmount = MSYScraper.priceFromString(discountText[occurIdx+6:])
                    
                    original_price = discountAmount + discounted_price
                else:
                    occurIdx = discountText.index("% off!")
                    
                    discountPercent = int( discountText[:occurIdx] )
                    original_price = discounted_price/(100-discountPercent)*100
                original_price = int(round(original_price))

                productItem.append({
                    "name": name,
                    "image_link": image_link,
                    "website_link": website_link,
                    "discounted_price": discounted_price,
                    "original_price": original_price,
                    "company_source": self.WEBSITE
                })

        return productItem
    
    def priceFromString(price_str):
        return float(price_str.replace(",",""))
        