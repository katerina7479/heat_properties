from sqlalchemy import Column, Integer, String, Float
from database import Base


class Property(Base):
    __tablename__ = 'property'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    symbol = Column(String(120), unique=True)
    melting_point = Column(Float())
    boiling_point = Column(Float())
    heat_of_vaporization = Column(Integer())
    heat_of_fusion = Column(Integer())

    def __init__(self, name, symbol, melting_point, boiling_point, heat_of_fusion, heat_of_vaporization):
        self.name = name
        self.symbol = symbol
        self.melting_point = melting_point
        self.boiling_point = boiling_point
        self.heat_of_vaporization = heat_of_fusion
        self.heat_of_fusion = heat_of_vaporization

    def __repr__(self):
        return '<Property for %s>' % (self.name)
