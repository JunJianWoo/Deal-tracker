from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from models import Item

class ItemSchema(SQLAlchemySchema):
    class Meta:
        model = Item
        load_instance = True

    id = auto_field()
    name = auto_field()
    image_link = auto_field()
    website_link = auto_field()
    company_source = auto_field()