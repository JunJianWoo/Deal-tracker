from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey, Date, Integer
from uuid import UUID
from datetime import datetime

# Database
class Base(DeclarativeBase, MappedAsDataclass):
    pass

db = SQLAlchemy(model_class=Base)

class Item(db.Model):
    id: Mapped[UUID] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    imageLink: Mapped[str] = mapped_column(String(400))
    websiteLink: Mapped[str] = mapped_column(String(400))
    companySource: Mapped[str] = mapped_column(String(40))

    def to_dict(self):
        return {
            "id": str(self.id),
            "name": str(self.name),
            "imageLink": self.imageLink,
            "websiteLink": self.websiteLink,
            "companySource": self.companySource
        }

class ItemPrice(db.Model):
    id: Mapped[UUID] = mapped_column(ForeignKey(Item.id), primary_key=True)
    date: Mapped[datetime.date] = mapped_column(Date, primary_key=True)
    originalPrice: Mapped[int] = mapped_column(Integer)
    discountedPrice: Mapped[int] = mapped_column(Integer)

    def to_dict(self):
        return {
            "id": str(self.id),
            "date": str(self.date),
            "originalPrice": self.originalPrice,
            "discountedPrice": self.discountedPrice
        }
    
class FetchHistory(db.Model):
    date: Mapped[datetime.date] = mapped_column(Date, primary_key=True)
    itemCreated: Mapped[int] = mapped_column(Integer)
    itemPriceCreated: Mapped[int] = mapped_column(Integer)

