from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import JSON, Date, Integer, ForeignKey, String
from datetime import datetime
from uuid import UUID, uuid1
from extensions import db

class Item(db.Model):
    id: Mapped[UUID] = mapped_column(primary_key=True,default=uuid1)
    name: Mapped[str] = mapped_column(String(200))
    image_link: Mapped[str] = mapped_column(String(400))
    website_link: Mapped[str] = mapped_column(String(400))
    company_source: Mapped[str] = mapped_column(String(40))

    def to_dict(self):
        """Serialize into json format"""
        return {
            "id": str(self.id),
            "name": str(self.name),
            "image_link": self.image_link,
            "website_link": self.website_link,
            "company_source": self.company_source
        }

class ItemPrice(db.Model):
    id: Mapped[UUID] = mapped_column(ForeignKey(Item.id), primary_key=True)
    date: Mapped[datetime.date] = mapped_column(Date, primary_key=True)
    original_price: Mapped[int] = mapped_column(Integer)
    discounted_price: Mapped[int] = mapped_column(Integer)

    def to_dict(self):
        """Serialize into json format"""
        return {
            "id": str(self.id),
            "date": str(self.date),
            "original_price": self.original_price,
            "discounted_price": self.discounted_price
        }
    

class FetchHistory(db.Model):
    date: Mapped[datetime.date] = mapped_column(Date, primary_key=True)
    items_created: Mapped[int] = mapped_column(Integer)
    item_prices_created: Mapped[int] = mapped_column(Integer)
    websites_failed: Mapped[list[str]] = mapped_column(JSON, default = [])
    successful_scrapes: Mapped[int] = mapped_column(Integer)
    
