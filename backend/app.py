import atexit
from flask import Flask
from dotenv import load_dotenv
from extensions import db, migrate, api, cors
from resources.routes.item_price import ItemPriceTodayAPI
from resources.routes.items import SimilarItemAPI
from scheduler.scrape_data import DataScrapingScheduler
import os


PORT_NUMBER = 8000

def create_app(): 
    
# Flask Application Configuration
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URI']

    db.init_app(app)
    migrate.init_app(app)
    
    cors.init_app(app,  resources={
        "r/*": {"origins": os.environ['FRONTEND_URL']}
    })

    api.add_resource(ItemPriceTodayAPI, "/api/dealstoday")
    api.add_resource(SimilarItemAPI,"/api/similar/<string:desc>")
    api.init_app(app)

    scheduler = DataScrapingScheduler(app)
    atexit.register(lambda: scheduler.shutdown())

    return app


if __name__ == "__main__":
    load_dotenv() 
    app = create_app()
    app.run(port=PORT_NUMBER, debug=True)


# TODO:
# Search bar for similar items