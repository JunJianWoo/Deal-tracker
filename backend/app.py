from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from dotenv import load_dotenv
from extensions import db
from models import Item
from resources.routes.item_price import ItemPriceTodayAPI
from resources.routes.scrape_data import ScrapeDataAPI
from resources.routes.items import SimilarItemAPI
from flask_cors import CORS
import os

load_dotenv() 
PORT_NUMBER = 8000

def create_app(): 
# Flask Application Configuration
    app = Flask(__name__)
    api = Api(app)
    
    CORS(app)

    # Bind App and Database together
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URI']
    db.init_app(app)
    migrate = Migrate(app,db)

    with app.app_context():
        db.create_all()

    api.add_resource(ItemPriceTodayAPI,"/api/dealstoday")
    api.add_resource(ScrapeDataAPI, "/api/fetchdeals")
    api.add_resource(SimilarItemAPI,"/api/similar/<string:desc>")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(port=PORT_NUMBER, debug=True)

# TODO:
# Search bar for similar items
# Remove CORS