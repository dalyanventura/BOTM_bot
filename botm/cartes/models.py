from sqlalchemy import Column, Integer, Text
from botm.db import Base

class Cartes(Base):
    __tablename__ = 'Cartes'

    id_carte = Column(Integer, primary_key=True)
    nom = Column(Text)
    niveau = Column(Integer)
    univers = Column(Text)
    force = Column(Integer)
    mana = Column(Integer)
    vitesse = Column(Integer)
    popularite = Column(Integer)
    prix = Column(Integer)
    image = Column(Text)

    def __init__(self, pk=0, n="Son Goku", un="Dragon Ball",  nv=4, f=90, m=90, v=90, p=90, px=1800, i="image"):
        self.id_carte = pk
        self.nom = n
        self.niveau = nv
        self.univers = un
        self.force = f
        self.mana = m
        self.vitesse = v
        self.popularite = p
        self.prix = px
        self.image = i