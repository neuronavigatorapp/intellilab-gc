from sqlalchemy import Column, Integer, String, Float
from .base import Base

class Compound(Base):
    __tablename__ = 'compounds'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    formula = Column(String)
    molecular_weight = Column(Float)
    method_tag = Column(String)
    retention_time = Column(Float)
    boiling_point = Column(Float)
