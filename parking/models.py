from sqlalchemy import (
    Column,
    String,
    Boolean,
    DateTime
)
from sqlalchemy.sql import func
from parking import db


class Booking(db.Model):
    __tablename__ = "booking"
    id = Column(String(20), primary_key=True)
    model = Column(String(40), nullable=True)
    plate = Column(String(10), nullable=False)
    color = Column(String(10), nullable=False)
    name = Column(String(100), nullable=False)
    created = Column(DateTime(timezone=True), server_default=func.now())
    cancelled = Column(Boolean, default=False, nullable=False)
