from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    ForeignKey
)

from sqlalchemy.orm import relationship
from database import Base

class Substance(Base):
    __tablename__ = 'substance'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(50), unique=True, nullable=False, index=True)
    symbol = Column(String(120), unique=True, nullable=False, index=True)
    latent_heats = relationship("LatentHeats", uselist=False, back_populates="substance")

    def __init__(self, name, symbol, id=None):
        self.name = name
        self.symbol = symbol
        if id:
            self.id = id

    def __repr__(self):
        return '<Substance %s, %s>' % (self.name, self.symbol)


class LatentHeats(Base):
    __tablename__ = 'latent_heats'
    melting_point = Column(Float())
    boiling_point = Column(Float())
    heat_of_vaporization = Column(Integer())
    heat_of_fusion = Column(Integer())
    substance_id = Column(Integer, ForeignKey('substance.id'),  primary_key=True, nullable=False, index=True)

    substance = relationship("Substance", uselist=False, back_populates="latent_heats")

    def __init__(self, substance_id,
                 melting_point, boiling_point,
                 heat_of_fusion, heat_of_vaporization):
        self.substance_id = substance_id
        self.melting_point = melting_point
        self.boiling_point = boiling_point
        self.heat_of_vaporization = heat_of_fusion
        self.heat_of_fusion = heat_of_vaporization

    def __repr__(self):
        return '<Latent Heats for %s>' % (self.substance.name)
