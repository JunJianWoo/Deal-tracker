from flask_restful import Resource
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from scrapers.scraper_manager import ScraperManager
from extensions import db
from models import Item, ItemPrice, FetchHistory
from datetime import datetime

class ScrapeDataAPI(Resource):
    def post(self):
        # Check whether fetched
        stmt = db.select(FetchHistory).where(FetchHistory.date==datetime.now().date())
        if db.session.execute(stmt).first() is not None:
            return { "status": "already fetched today" }, 304
        
        # Fetch if not already performed today
        itemsAdded = 0
        itemPriceAdded = 0
        try:
            scrape_results = ScraperManager.scrape_all_data()
            for args in scrape_results['data']:
                # Create Item if not exists
                result = db.session.execute(db.select(Item.id).where(Item.name==args['name']).where(Item.company_source == args['company_source']))
                item = result.first()
                if item is None:
                    item = Item(name= args['name'], 
                                website_link= args['website_link'],
                                image_link = args['image_link'],
                                company_source = args['company_source']
                                )
                    db.session.add(item)
                    itemsAdded += 1
                
                # Create ItemPrice if not exists
                result = db.session.execute(db.select(ItemPrice.id, ItemPrice.date).where(ItemPrice.id==item.id).where(ItemPrice.date==datetime.now().date()))
                if result.first() is None:
                    itemPrice = ItemPrice(id= item.id, 
                                        date = datetime.now().date(),
                                        original_price= args['original_price'], 
                                        discounted_price= args['discounted_price'])
                    db.session.add(itemPrice)
                    itemPriceAdded += 1

                db.session.flush() # Fail fast

            history = FetchHistory(date=datetime.now().date(), 
                                   items_created=itemsAdded, 
                                   item_prices_created = itemPriceAdded,
                                    websites_failed=scrape_results['websites_failed'],
                                    successful_scrapes=scrape_results['successful_scrapes'])
            db.session.add(history)
            db.session.commit()
        except SQLAlchemyError|IntegrityError as e:
            db.session.rollback()
            print("Error:", e)
            return {"status": "error"}

        return {"status": "success"}

# TODO: Cronify and schedule this job


