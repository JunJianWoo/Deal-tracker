from typing import List
from flask_restful import Resource, reqparse
from database import db, Item, ItemPrice
from datetime import datetime
from flask import request

class ItemPriceTodayAPI(Resource):

    filter_parser = reqparse.RequestParser()
    filter_parser.add_argument('companySource', type=str, action="append", help = 'Sources of item to be included (leave empty for all)')
    filter_parser.add_argument('minPrice', type=float, default= 0, help= 'Minimum price for item to be included')
    filter_parser.add_argument('maxPrice',type=float, default ="1.0e308", help='Maximum price for item to still be included')

    def post(self):
        args = self.filter_parser.parse_args()

        stmt = db.select(ItemPrice, Item) \
              .where(ItemPrice.date==datetime.now().date(), ItemPrice.discountedPrice >= args.minPrice, ItemPrice.discountedPrice <= args.maxPrice) \
                .where(Item.companySource.in_(args.companySource if args.companySource else [])) \
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