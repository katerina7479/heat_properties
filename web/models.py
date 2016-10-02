from sqlalchemy import Column, Integer, String, Float
from database import Base


class Property(Base):
    __tablename__ = 'property'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    symbol = Column(String(120), unique=True)
    melting_point = Column(Integer())
    boiling_point = Column(Integer())
    heat_of_vaporization = Column(Float())
    heat_of_fusion = Column(Float())

    def __init__(self, name, symbol, melting, boiling, fusion, vaporization):
        self.name = name
        self.symbol = symbol
        self.melting_point = melting
        self.boiling_point = boiling
        self.heat_of_vaporization = fusion
        self.heat_of_fusion = vaporization

    def __repr__(self):
        return '<Property %r>' % (self.name)
