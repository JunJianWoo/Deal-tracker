from datetime import datetime
from flask import request
from flask_restful import Resource
from marshmallow import Schema, fields, ValidationError, pre_load
from extensions import db
from models import Item, ItemPrice
from serializers.item_price_schema import ItemPriceSchema
from serializers.item_schema import ItemSchema

class FilterSchema(Schema):
    company_source = fields.List(fields.String(),load_default=[])
    min_price = fields.Float(load_default=0)
    max_price = fields.Float(load_default=1.0e308)

    @pre_load
    def normalise_company_source(self, raw_data, **kwargs):
        """ Pre-process list of strings from GET params """
        data = raw_data.to_dict()

        if 'company_source' in raw_data:
            data['company_source'] = raw_data.getlist('company_source')

        return data


class ItemPriceTodayAPI(Resource):
    def get(self):
        try:
            args = FilterSchema().load(request.args)
        except ValidationError as err:
            return {"errors":err.messages}, 400


        stmt = db.select(ItemPrice, Item) \
              .where(ItemPrice.date==datetime.now().date(), ItemPrice.discounted_price >= args['min_price'], ItemPrice.discounted_price <= args['max_price']) \
                .where(Item.company_source.in_(args['company_source'])) \
                    .join(Item) \
                        .order_by(Item.id)

        result = db.session.execute(stmt)

        # Serialize into Json
        item_serializer = ItemSchema()
        item_price_serializer = ItemPriceSchema()
        serialized_data = [
            item_serializer.dump(item) | item_price_serializer.dump(item_price)
            for item_price, item in result.all()
        ]

        return serialized_data