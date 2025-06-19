from flask_restful import Resource
from scrapers.scraper_manager import ScraperManager
from database import db, Item, ItemPrice, FetchHistory
from uuid import uuid1
from datetime import datetime

class ScrapeDataAPI(Resource):
    def post(self):
        itemsAdded = 0
        itemPriceAdded = 0

        stmt = db.select(FetchHistory).where(FetchHistory.date==datetime.now().date())

        if db.session.execute(stmt).first() is not None:
            return {
                "status": "already fetched today"
            }, 304
        else:
            for args in ScraperManager.scrape_all_data():
                # Create Item if not exists
                result = db.session.execute(db.select(Item.id).where(Item.name==args['name']).where(Item.companySource == args['companySource']))
                item = result.first()
                if item is None:
                    item = Item(id= uuid1(), 
                                name= args['name'], 
                                websiteLink= args['websiteLink'],
                                imageLink = args['imageLink'],
                                companySource = args['companySource']
                                )
                    db.session.add(item)
                    itemsAdded += 1

                # Create ItemPrice if not exists
                result = db.session.execute(db.select(ItemPrice.id, ItemPrice.date).where(ItemPrice.id==item.id).where(ItemPrice.date==datetime.now().date()))
                if result.first() is None:
                    itemPrice = ItemPrice(id= item.id, 
                                        date = datetime.now().date(),
                                        originalPrice= args['originalPrice'], 
                                        discountedPrice= args['discountedPrice']
                                        )
                    db.session.add(itemPrice)
                    itemPriceAdded += 1


            history = FetchHistory(date=datetime.now().date(), itemCreated=itemsAdded, itemPriceCreated = itemPriceAdded)
            db.session.add(history)

            db.session.commit()
            return {"status": "success",
                "items_added": itemsAdded,
                "pricing_added": itemPriceAdded
                }




