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

    joueurs = pd.read_csv('../player.tsv', sep='\t')
    cartes = pd.read_csv('../cartes.tsv', sep='\t')

    rprint(cartes)
    rprint(joueurs)

    # engine = create_engine('sqlite:///demo.db', echo=False)
    engine = create_engine(config.DATABASE_URI, echo=False)

    print("--- Construct all tables for the database (here just one table) ---")
    Base.metadata.create_all(engine)  # Only for the first time

    print("--- Create three new contacts and push its into the database ---")
    Session = sessionmaker(bind=engine)
    session = Session()

    # for i in range(len(joueurs)):
    #     j = Joueurs(i, joueurs['Pseudo'][i], joueurs['Points'][i], joueurs['Picks'][i])
    #     session.add(j)

    for i in range(len(cartes)):
        c = Cartes(i, cartes['Nom'][i], cartes['Univers'][i], cartes['Niveau'][i], cartes['Force'][i], cartes['Mana'][i], cartes['Vitesse'][i], cartes['Popularité'][i], cartes['Prix'][i], cartes['Image'][i])
        session.add(c)

    session.commit()

    print("--- Print all contacts ---")
    for contact in session.query(Joueurs).all():
        print(contact.id_j, contact.pseudo, contact.points, contact.pick_nb)

    for carte in session.query(Cartes).all():
        print(carte.id_carte, carte.nom, carte.niveau, carte.univers, carte.force, carte.mana, carte.vitesse, carte.popularite, carte.prix, carte.image)

    # Close the session
    session.close()

    print("--- End of the program ---")

    # Close the database
    engine.dispose()

    #
    # doe = Contact(1)
    # session.add(doe)
    #
    # james = Contact(3, "James", "Bond")
    # session.add(james)
    #
    # jason = Contact(4, "Jason", "Bourne")
    # session.add(jason)
    #
    # # session.add_all( [ doe, james, jason ] )
    # session.commit()
    #
    # print("--- First select by primary key ---")
    # contact = session.query(Contact).get(3)
    # print(contact)
    #
    # print("--- Second select by firstName ---")
    # searchedContacts = session.query(Contact).filter(Contact.firstName.startswith("Ja"))
    # for c in searchedContacts: print(c)
    #
    # print("--- Third select all contacts ---")
    # agenda = session.query(Contact)  # .filter_by( firstName='James' )
    # for c in agenda: print(c)
    #
    # print("--- Try to update a specific contact ---")
    # contact = session.query(Contact).get(1)
    # contact.lastName += "!"
    # session.commit()  # Mandatory
    #
    # print("--- Try to delete a specific contact ---")
    # session.delete(contact)
    # session.commit()  # Mandatory