from flask_restful import Resource
from extensions import db
from models import Item
from serializers.item_schema import ItemSchema

class SimilarItemAPI(Resource):
    def get(self, desc):
        result = db.session.execute(
            db.select( Item ) \
              .where(Item.name.like(f"%{desc}%"))
        )

        # Serialize into Json
        item_serializer = ItemSchema()
        serialized_data = [
            item_serializer.dump(row[0])
            for row in result.all()
        ]

        return serialized_data
    
