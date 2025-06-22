from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from models import ItemPrice

class ItemPriceSchema(SQLAlchemySchema):
    class Meta:
        model = ItemPrice
        load_instance = True

    id = auto_field()
    date = auto_field()
    original_price = auto_field()
    discounted_price = auto_field()
