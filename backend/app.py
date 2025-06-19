from flask import Flask
from flask_restful import Api
from dotenv import load_dotenv
from database import db
from resources.item_price import ItemPriceTodayAPI
from resources.scrape_data import ScrapeDataAPI
from resources.item import SimilarItemAPI
from flask_cors import CORS
import os

load_dotenv() 

# Flask Application Configuration
app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URI']
CORS(app)

# Links App and Database
db.init_app(app)

with app.app_context():
    db.create_all()

api.add_resource(ItemPriceTodayAPI,"/api/dealstoday")
api.add_resource(ScrapeDataAPI, "/api/fetchdeals")
api.add_resource(SimilarItemAPI,"/api/similar/<string:desc>")


if __name__ == "__main__":
    app.run(port=8000, debug=True)


# TODO:
# Search bar for similar items
# Remove CORS