from sqlalchemy import Column, Integer, String
from .base import Base

class Instrument(Base):
    __tablename__ = 'instruments'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    model = Column(String)
    serial = Column(String)
    location = Column(String)
    status = Column(String)
