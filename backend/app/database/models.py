from sqlalchemy import Column, Integer, String, Float, Boolean, Date, Time
from .database import Base

class MenuItem(Base):
    __tablename__ = "menu_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    category = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    image_url = Column(String, nullable=True)
    vegetarian = Column(Boolean, default=False)
    availability = Column(Boolean, default=True)

class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(String, primary_key=True, index=True)
    customer_name = Column(String)
    date = Column(Date)
    time = Column(Time)
    guests = Column(Integer)
    status = Column(String, default="confirmed")
