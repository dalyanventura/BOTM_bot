#!/usr/bin/python

import config
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import pandas as pd
from rich import print as rprint

import numpy
from psycopg2.extensions import register_adapter, AsIs

def addapt_numpy_float64(numpy_float64):
    return AsIs(numpy_float64)
def addapt_numpy_int64(numpy_int64):
    return AsIs(numpy_int64)

register_adapter(numpy.float64, addapt_numpy_float64)
register_adapter(numpy.int64, addapt_numpy_int64)

# Base class used by my classes (my entities)
Base = declarative_base()  # Required


# Definition of the Contact class
class Joueurs(Base):
    __tablename__ = 'Joueurs'

    id_j = Column(Integer, primary_key=True)
    pseudo = Column(Text)
    points = Column(Integer)
    pick_nb = Column(Integer)

    def __init__(self, pk=0, ps="Marvin", pt=3000, pn=5):
        self.id_j = pk
        self.pseudo = ps
        self.points = pt
        self.pick_nb = pn

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

class CartesJoueurs(Base):
    __tablename__ = 'CartesJoueurs'

    id_carte = Column(Integer, ForeignKey('Cartes.id_carte'),  nullable=False, primary_key=True)
    id_j = Column(Integer, ForeignKey('Joueurs.id_j'), nullable=True, primary_key=True)
    nb_cartes = Column(Integer)

    def __init__(self, id_carte=0, id_joueur=0, nb_cartes=0):
        self.id_carte = id_carte
        self.id_j = id_joueur
        self.nb_cartes = nb_cartes

# The main part
if __name__ == '__main__':

    joueurs_cartes = pd.read_csv('joueurs_cartes.tsv', sep='\t')

    rprint(joueurs_cartes)

    # engine = create_engine('sqlite:///demo.db', echo=False)
    engine = create_engine(config.DATABASE_URI, echo=False)

    print("--- Construct all tables for the database (here just one table) ---")

    print("--- Create three new contacts and push its into the database ---")
    Session = sessionmaker(bind=engine)
    session = Session()

    for i in range(len(joueurs_cartes)):
        id_cartes = session.query(Cartes.id_carte).filter(Cartes.nom == joueurs_cartes['Nom_carte'][i], Cartes.niveau == joueurs_cartes['Niveau'][i],
                                                          Cartes.univers == joueurs_cartes['Univers'][i], Cartes.force == joueurs_cartes['Force'][i],
                                                          Cartes.mana == joueurs_cartes['Mana'][i], Cartes.vitesse == joueurs_cartes['Vitesse'][i],
                                                          Cartes.popularite == joueurs_cartes['Popularité'][i]).first()
        # print(id_cartes)
        try:
            c_j = CartesJoueurs(id_cartes[0], joueurs_cartes['ID_j'][i], joueurs_cartes['Nombre_cartes'][i])
        except TypeError:
            print("Carte non trouvée : ", joueurs_cartes['Nom_carte'][i], joueurs_cartes['Niveau'][i], joueurs_cartes['Univers'][i],
                    joueurs_cartes['Force'][i], joueurs_cartes['Mana'][i], joueurs_cartes['Vitesse'][i], joueurs_cartes['Popularité'][i])
        session.add(c_j)

    session.commit()

    # Close the session
    session.close()

    print("--- End of the program ---")

    # Close the database
    engine.dispose()
