'''Application Models'''
from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    UniqueConstraint
)

from sqlalchemy.orm import relationship
from database import Base


class Substance(Base):
    '''Class for Chemical Substance'''
    __tablename__ = 'substance'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(50), nullable=False, index=True)
    symbol = Column(String(120), nullable=False, index=True)
    latent_heats = relationship("LatentHeats", uselist=False, back_populates="substance")

    # Unique constraint together
    UniqueConstraint('name', 'symbol', name='uix_1')

    def __init__(self, name, symbol, id=None):
        '''Initialize the model, optional id field'''
        self.name = name
        self.symbol = symbol
        if id:
            self.id = id

    def __repr__(self):
        '''Model representation'''
        return '<Substance %s, %s>' % (self.name, self.symbol)


class LatentHeats(Base):
    '''Model for Heat properties'''
    __tablename__ = 'latent_heats'
    melting_point = Column(Float())
    boiling_point = Column(Float())
    heat_of_vaporization = Column(Integer())
    heat_of_fusion = Column(Integer())
    substance_id = Column(Integer, ForeignKey('substance.id'),  primary_key=True, nullable=False, index=True)

    # One-to-one relationship with Substance
    substance = relationship("Substance", uselist=False, back_populates="latent_heats")

    def __init__(self, substance_id,
                 melting_point, boiling_point,
                 heat_of_fusion, heat_of_vaporization):
        '''Initialize model with substance_id required'''
        self.substance_id = substance_id
        self.melting_point = melting_point
        self.boiling_point = boiling_point
        self.heat_of_vaporization = heat_of_fusion
        self.heat_of_fusion = heat_of_vaporization

    def __repr__(self):
        '''Model representation'''
        return '<Latent Heats for %s>' % (self.substance.name)
