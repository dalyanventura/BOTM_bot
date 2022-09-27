from sqlalchemy import Column, Integer, Text, Boolean
from botm.db import Base

class Joueurs(Base):
    __tablename__ = 'Joueurs'

    id_j = Column(Integer, primary_key=True)
    pseudo = Column(Text)
    points = Column(Integer)
    pick_nb = Column(Integer)
    Admin = Column(Boolean)

    def __init__(self, pk=0, ps="Marvin", pt=3000, pn=5, admin=False):
        self.id_j = pk
        self.pseudo = ps
        self.points = pt
        self.pick_nb = pn
        self.Admin = admin