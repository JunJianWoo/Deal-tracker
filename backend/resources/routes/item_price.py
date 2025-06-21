from flask_restful import Resource, reqparse
from extensions import db
from models import Item, ItemPrice
from datetime import datetime

class ItemPriceTodayAPI(Resource):

    filter_parser = reqparse.RequestParser()
    filter_parser.add_argument('company_source', type=str, action="append", help = 'Sources of item to be included (leave empty for all)')
    filter_parser.add_argument('minPrice', type=float, default= 0, help= 'Minimum price for item to be included')
    filter_parser.add_argument('maxPrice',type=float, default ="1.0e308", help='Maximum price for item to still be included')

    def post(self):
        args = self.filter_parser.parse_args()

        stmt = db.select(ItemPrice, Item) \
              .where(ItemPrice.date==datetime.now().date(), ItemPrice.discounted_price >= args.minPrice, ItemPrice.discounted_price <= args.maxPrice) \
                .where(Item.company_source.in_(args.company_source if args.company_source else [])) \
                    .join(Item) \
                        .order_by(Item.id)

        result = db.session.execute(stmt)

        # Serialize into Json
        serialized_data = []
        for row in result.all():
            itemPrice, item = row
            serialized_data.append( item.to_dict() | itemPrice.to_dict() )

        # return serialized_data
        return serialized_data
    

class ItemPriceNotTodayAPI(Resource):
    def get(self):
        pass