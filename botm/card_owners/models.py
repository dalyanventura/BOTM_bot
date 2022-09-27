from sqlalchemy import Column, Integer, ForeignKey
from botm.db import Base


class CartesJoueurs(Base):
    __tablename__ = 'CartesJoueurs'

    id_carte = Column(Integer, ForeignKey('Cartes.id_carte'),  nullable=False, primary_key=True)
    id_j = Column(Integer, ForeignKey('Joueurs.id_j'), nullable=True, primary_key=True)
    nb_cartes = Column(Integer)

    def __init__(self, id_carte=0, id_joueur=0, nb_cartes=0):
        self.id_carte = id_carte
        self.id_j = id_joueur
        self.nb_cartes = nb_cartes