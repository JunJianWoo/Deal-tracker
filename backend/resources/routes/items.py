from flask_restful import Resource
from extensions import db
from models import Item

class SimilarItemAPI(Resource):
    def get(self, desc):
        result = db.session.execute(
            db.select( Item ) \
              .where(Item.name.like(f"%{desc}%"))
        )

        # Serialize into Json
        serialized_data = []
        for row in result.all():
            item = row[0]
            serialized_data.append( item.to_dict()) 

        return serialized_data
    
