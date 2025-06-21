from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from scrapers.scraper_manager import ScraperManager
from extensions import db
from models import Item, ItemPrice, FetchHistory
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from util import singleton

@singleton
class DataScrapingScheduler:
    SCHEDULED_TIME_HOUR = 4
    SCHEDULED_TIME_MINUTE = 0

    def __init__(self, app):
        self.scheduler = BackgroundScheduler()
        self.app = app

        self._job_with_context()

        # Schedule future jobs
        self.scheduler.add_job(self._job_with_context, 'cron', hour=self.SCHEDULED_TIME_HOUR, minute=self.SCHEDULED_TIME_MINUTE)
        self.start()

    def start(self):
        self.scheduler.start()

    def shutdown(self):
        self.scheduler.shutdown(wait=False)

    def get_jobs(self):
        return self.scheduler.get_jobs()
    
    def _job_with_context(self):
        with self.app.app_context():
            return self._web_scrape_job()

    def _web_scrape_job(self):
        # Check whether fetched
        stmt = db.select(FetchHistory).where(FetchHistory.date==datetime.now().date())
        if db.session.execute(stmt).first() is not None:
            return {'status': 'skipped', 'reason': 'already fetched today'}
        
        # Fetch if not already performed today
        items_added = 0
        item_prices_added = 0
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
                    items_added += 1
                
                # Create ItemPrice if not exists
                result = db.session.execute(db.select(ItemPrice.id, ItemPrice.date).where(ItemPrice.id==item.id).where(ItemPrice.date==datetime.now().date()))
                if result.first() is None:
                    itemPrice = ItemPrice(id= item.id, 
                                        date = datetime.now().date(),
                                        original_price= args['original_price'], 
                                        discounted_price= args['discounted_price'])
                    db.session.add(itemPrice)
                    item_prices_added += 1

                db.session.flush() # Fail fast

            history = FetchHistory(date=datetime.now().date(), 
                                   items_created=items_added, 
                                   item_prices_created = item_prices_added,
                                    websites_failed=scrape_results['websites_failed'],
                                    successful_scrapes=scrape_results['successful_scrapes'])
            db.session.add(history)
            db.session.commit()
        except SQLAlchemyError|IntegrityError as e:
            db.session.rollback()
            print("Error:", e)
            return {'status': 'failed', 'reason': 'SQL error'}

        return {"status": "success"}
